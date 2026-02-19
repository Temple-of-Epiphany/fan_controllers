#!/usr/bin/env python3
"""
Generate per-model ElegooSlicer/OrcaSlicer 3MF files for Victron MPPT cooling mounts.

Author: Colin Bitterfield
Email: colin@bitterfield.com
Date Created: 2026-02-17
Date Updated: 2026-02-17
Version: 2.2.0

Generates one 3MF per controller model x fan size combination:
  - Default fan size (from database)
  - 40mm fan override (skipped if model default is already 40mm)

3MF plate layout (3 plates per file):
  Plate 1 "fan-mount":  Front fan mount (alone; rotated 45° if >245mm)
  Plate 2 "rails":      Left rail + Right rail (side by side)
  Plate 3 "grill":      Rear grill (alone; rotated 45° if >245mm)

Format: ElegooSlicer/BambuStudio/OrcaSlicer multi-plate 3MF
  - Each STL is a separate 3D/Objects/*.model file
  - 3D/3dmodel.model uses <components> wrappers, no inline mesh
  - Plate assignments via model_settings.config <model_instance> elements
  - BambuStudio and production (p:) XML namespaces
  - UUID assigned to every object and build item

Embedded settings: PETG material, 20% sparse infill hints
File naming: {Model_Name}_{fan_size}mm.3mf
  e.g., SmartSolar_MPPT_100-30_50mm.3mf

Output directory: output_orca_3mf/
"""

import math
import os
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

# ===== CONTROLLER DATABASE =====
# (model_code, display_name, default_fan_size)
CONTROLLERS = [
    # A1 Config - 3x50mm fans
    ("SCC020030200",  "BlueSolar MPPT 100-30",              50),
    ("SCC110030210",  "SmartSolar MPPT 100-30",             50),
    ("SCC020050200",  "BlueSolar MPPT 100-50",              50),
    ("SCC020035000",  "BlueSolar MPPT 150-35",              50),
    ("SCC115045222",  "BlueSolar MPPT 150-45",              50),
    ("SCC110050210",  "SmartSolar MPPT 100-50",             50),
    ("SCC115035210",  "SmartSolar MPPT 150-35",             50),
    ("SCC115045212",  "SmartSolar MPPT 150-45",             50),
    ("ORI121236120",  "Orion-Tr Smart 12-12-30A",           50),
    ("ORI122436120",  "Orion-Tr Smart 12-24-15A",           50),
    ("ORI241236120",  "Orion-Tr Smart 24-12-30A",           50),
    # A3 Config - 2x50mm fans
    ("SCC110020070R", "BlueSolar MPPT 100-20",              50),
    ("SCC110020170R", "BlueSolar MPPT 100-20 48V",          50),
    ("SCC110020060R", "SmartSolar MPPT 100-20",             50),
    ("SCC110020160R", "SmartSolar MPPT 100-20 48V",         50),
    # A4 Config - 4x50mm fans
    ("SCC115060210",  "SmartSolar MPPT 150-60-Tr",          50),
    ("SCC115070210",  "SmartSolar MPPT 150-70-Tr",          50),
    # A4_MC4 Config - 4x50mm fans
    ("SCC115060310",  "SmartSolar MPPT 150-60-MC4",         50),
    ("SCC115070310",  "SmartSolar MPPT 150-70-MC4",         50),
    # B1 Config - 4x50mm fans
    ("SCC115085211",  "SmartSolar MPPT 150-85-Tr",          50),
    ("SCC115110211",  "SmartSolar MPPT 150-100-Tr",         50),
    ("SCC125085210",  "SmartSolar MPPT 250-85-Tr",          50),
    ("SCC125110210",  "SmartSolar MPPT 250-100-Tr",         50),
    # B2 Config - 4x50mm fans (Tr VE.Can)
    ("SCC115085411",  "SmartSolar MPPT 150-85-Tr VE.Can",   50),
    ("SCC115110410",  "SmartSolar MPPT 150-100-Tr VE.Can",  50),
    ("SCC115110420",  "BlueSolar MPPT 150-100-Tr VE.Can",   50),
    ("SCC125085411",  "SmartSolar MPPT 250-85-Tr VE.Can",   50),
    ("SCC125110411",  "SmartSolar MPPT 250-100-Tr VE.Can",  50),
    ("SCC125110441",  "BlueSolar MPPT 250-100-Tr VE.Can",   50),
    # B2_MC4 Config - 4x50mm fans (MC4 VE.Can)
    ("SCC115085511",  "SmartSolar MPPT 150-85-MC4 VE.Can",  50),
    ("SCC115110511",  "SmartSolar MPPT 150-100-MC4 VE.Can", 50),
    ("SCC125085511",  "SmartSolar MPPT 250-85-MC4 VE.Can",  50),
    ("SCC125110512",  "SmartSolar MPPT 250-100-MC4 VE.Can", 50),
    # B3 Config - 4x50mm fans
    ("SCC125060221",  "SmartSolar MPPT 250-60-Tr",          50),
    ("SCC125070220",  "SmartSolar MPPT 250-70-Tr",          50),
    # C1 Config - 2x40mm fans (housing-based)
    ("SCC010010050R", "BlueSolar MPPT 75-10",               40),
    ("SCC010015050R", "BlueSolar MPPT 75-15",               40),
    ("SCC075010060R", "SmartSolar MPPT 75-10",              40),
    ("SCC075015060R", "SmartSolar MPPT 75-15",              40),
    # C2 Config - 2x40mm fans (housing-based)
    ("SCC010015200R", "SmartSolar MPPT 100-15-C2",          40),
    ("SCC110015060R", "SmartSolar MPPT 100-15",             40),
]

OVERRIDE_FAN_SIZE = 40
MATERIAL          = "PETG"
INFILL_PCT        = 20
SCAD_FILE         = "solar_controller_cooling_mount.scad"
OUTPUT_DIR        = Path("output_orca_3mf")
BED_SIZE          = 256.0    # Build plate width/depth (mm)
MAX_STRAIGHT      = 245.0    # Parts larger than this are rotated 45°
PLATE_STRIDE      = BED_SIZE * 1.2  # Virtual canvas offset between plates (~307.2mm)

# Component numbers (must match SCAD component variable)
COMP_FRONT = 1
COMP_LEFT  = 2
COMP_RIGHT = 3
COMP_REAR  = 4

COMP_NAMES = {
    COMP_FRONT: "Front Fan Mount",
    COMP_LEFT:  "Left Rail",
    COMP_RIGHT: "Right Rail",
    COMP_REAR:  "Rear Grill",
}


# ===== UUID HELPERS =====

_uuid_counter = 0

def make_uuid(prefix="0000"):
    """Generate a deterministic UUID-shaped string."""
    global _uuid_counter
    _uuid_counter += 1
    return f"{prefix}{_uuid_counter:04d}-b206-40ff-9872-83e8017abed1"


def reset_uuids():
    global _uuid_counter
    _uuid_counter = 0


# ===== STL PARSER =====

def read_binary_stl(path):
    """
    Parse a binary STL into (vertices, faces, bounds).

    Deduplicates vertices via coordinate-keyed dict.
    Returns:
        vertices: list of (x, y, z) centered at XY origin, bottom at Z=0
        faces:    list of (i, j, k) int index triples
        bounds:   (min_x, min_y, min_z, max_x, max_y, max_z) of ORIGINAL mesh
    """
    with open(path, 'rb') as f:
        header = f.read(80)
        n_tri = struct.unpack('<I', f.read(4))[0]

        vertex_map = {}
        raw_vertices = []
        faces = []
        UNPACK = struct.Struct('<3f')

        for _ in range(n_tri):
            f.read(12)  # skip normal
            tri = []
            for _ in range(3):
                v = UNPACK.unpack(f.read(12))
                key = (round(v[0], 4), round(v[1], 4), round(v[2], 4))
                if key not in vertex_map:
                    vertex_map[key] = len(raw_vertices)
                    raw_vertices.append(key)
                tri.append(vertex_map[key])
            faces.append(tuple(tri))
            f.read(2)   # attribute byte count

    if not raw_vertices:
        raise ValueError(f"No geometry in {path}")

    xs = [v[0] for v in raw_vertices]
    ys = [v[1] for v in raw_vertices]
    zs = [v[2] for v in raw_vertices]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)
    bounds = (min_x, min_y, min_z, max_x, max_y, max_z)

    # Center at XY origin, lift Z so bottom = 0
    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    vertices = [(x - cx, y - cy, z - min_z) for (x, y, z) in raw_vertices]

    return vertices, faces, bounds


# ===== GEOMETRY HELPERS =====

def needs_rotation(bounds):
    """Return True if the part is wider than MAX_STRAIGHT in X or Y."""
    min_x, min_y, min_z, max_x, max_y, max_z = bounds
    w = max_x - min_x
    l = max_y - min_y
    return max(w, l) > MAX_STRAIGHT


def rotated_45_fits(bounds):
    """Check that a 45°-rotated bounding box fits on BED_SIZE x BED_SIZE."""
    min_x, min_y, min_z, max_x, max_y, max_z = bounds
    w = max_x - min_x
    l = max_y - min_y
    diagonal = (w + l) / math.sqrt(2.0)
    return diagonal <= BED_SIZE


COS45 = math.cos(math.radians(45))
SIN45 = math.sin(math.radians(45))


def build_transform(rotate_45, tx, ty, tz):
    """
    Return a 3MF 3x4 transform string.
    Rotation is around Z axis (45° if rotate_45), then translate.
    Format: r00 r01 r02  r10 r11 r12  r20 r21 r22  tx ty tz
    """
    if rotate_45:
        return (f"{COS45:.9f} {-SIN45:.9f} 0 "
                f"{SIN45:.9f} {COS45:.9f} 0 "
                f"0 0 1 "
                f"{tx:.4f} {ty:.4f} {tz:.4f}")
    else:
        return f"1 0 0 0 1 0 0 0 1 {tx:.4f} {ty:.4f} {tz:.4f}"


# ===== XML BUILDERS =====

def build_object_model_xml(part_obj_id, vertices, faces, part_uuid):
    """
    Build the XML for a 3D/Objects/*.model file.
    Contains one object with the actual mesh.
    """
    ns = ('xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
          'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
          'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
          'requiredextensions="p"')
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<model unit="millimeter" xml:lang="en-US" {ns}>',
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>',
        ' <resources>',
        f'  <object id="{part_obj_id}" p:UUID="{part_uuid}" type="model">',
        '   <mesh>',
        '    <vertices>',
    ]
    for x, y, z in vertices:
        lines.append(f'     <vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>')
    lines.append('    </vertices>')
    lines.append('    <triangles>')
    for v1, v2, v3 in faces:
        lines.append(f'     <triangle v1="{v1}" v2="{v2}" v3="{v3}"/>')
    lines.append('    </triangles>')
    lines.append('   </mesh>')
    lines.append('  </object>')
    lines.append(' </resources>')
    lines.append(' <build/>')
    lines.append('</model>')
    return '\n'.join(lines)


def build_main_model_xml(objects, build_items):
    """
    Build the 3D/3dmodel.model XML.

    objects: list of dicts {wrapper_id, wrapper_uuid, part_obj_id, part_uuid, object_path}
    build_items: list of dicts {wrapper_id, item_uuid, transform}
    """
    ns = ('xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
          'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
          'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
          'requiredextensions="p"')
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<model unit="millimeter" xml:lang="en-US" {ns}>',
        ' <metadata name="Application">generate_orca_3mf.py-2.2.0</metadata>',
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>',
        ' <resources>',
    ]
    for obj in objects:
        lines.append(f'  <object id="{obj["wrapper_id"]}" p:UUID="{obj["wrapper_uuid"]}" type="model">')
        lines.append('   <components>')
        lines.append(
            f'    <component p:path="{obj["object_path"]}" '
            f'objectid="{obj["part_obj_id"]}" '
            f'p:UUID="{obj["part_uuid"]}" '
            f'transform="1 0 0 0 1 0 0 0 1 0 0 0"/>'
        )
        lines.append('   </components>')
        lines.append('  </object>')
    lines.append(' </resources>')
    build_uuid = make_uuid("bbbb")
    lines.append(f' <build p:UUID="{build_uuid}">')
    for item in build_items:
        lines.append(
            f'  <item objectid="{item["wrapper_id"]}" '
            f'p:UUID="{item["item_uuid"]}" '
            f'transform="{item["transform"]}" '
            f'printable="1"/>'
        )
    lines.append(' </build>')
    lines.append('</model>')
    return '\n'.join(lines)


def build_main_model_rels(object_paths):
    """Build 3D/_rels/3dmodel.model.rels listing all object model files."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for i, path in enumerate(object_paths, 1):
        lines.append(
            f' <Relationship Target="{path}" Id="rel-{i}" '
            f'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        )
    lines.append('</Relationships>')
    return '\n'.join(lines)


def build_root_rels():
    return """\
<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>"""


def build_content_types():
    return """\
<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="png" ContentType="image/png"/>
 <Default Extension="config" ContentType="application/xml"/>
</Types>"""


def build_model_settings(objects, plates, assemble_items):
    """
    Build Metadata/model_settings.config.

    objects: list of dicts {wrapper_id, part_obj_id, name, source_offset_x, source_offset_y, source_offset_z}
    plates:  list of dicts {plater_id, plater_name, object_ids: [(wrapper_id, instance_id, identify_id)]}
    assemble_items: list of dicts {wrapper_id, instance_id, transform_z}
    """
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<config>']

    for obj in objects:
        wid = obj['wrapper_id']
        pid = obj['part_obj_id']
        name = obj['name']
        sx = obj.get('source_offset_x', 0)
        sy = obj.get('source_offset_y', 0)
        sz = obj.get('source_offset_z', 0)
        lines.append(f'  <object id="{wid}">')
        lines.append(f'    <metadata key="name" value="{name}"/>')
        lines.append(f'    <metadata key="extruder" value="1"/>')
        lines.append(f'    <part id="{pid}" subtype="normal_part">')
        lines.append(f'      <metadata key="name" value="{name}"/>')
        lines.append(f'      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>')
        lines.append(f'      <metadata key="source_file" value="{name}.stl"/>')
        lines.append(f'      <metadata key="source_object_id" value="0"/>')
        lines.append(f'      <metadata key="source_volume_id" value="0"/>')
        lines.append(f'      <metadata key="source_offset_x" value="{sx:.4f}"/>')
        lines.append(f'      <metadata key="source_offset_y" value="{sy:.4f}"/>')
        lines.append(f'      <metadata key="source_offset_z" value="{sz:.4f}"/>')
        lines.append(f'      <mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>')
        lines.append(f'    </part>')
        lines.append(f'  </object>')

    for plate in plates:
        pid = plate['plater_id']
        lines.append('  <plate>')
        lines.append(f'    <metadata key="plater_id" value="{pid}"/>')
        lines.append(f'    <metadata key="plater_name" value="{plate["plater_name"]}"/>')
        lines.append(f'    <metadata key="locked" value="false"/>')
        lines.append(f'    <metadata key="filament_map_mode" value="Auto For Flush"/>')
        lines.append(f'    <metadata key="filament_maps" value="1 1"/>')
        lines.append(f'    <metadata key="thumbnail_file" value="Metadata/plate_{pid}.png"/>')
        lines.append(f'    <metadata key="thumbnail_no_light_file" value="Metadata/plate_no_light_{pid}.png"/>')
        lines.append(f'    <metadata key="top_file" value="Metadata/top_{pid}.png"/>')
        lines.append(f'    <metadata key="pick_file" value="Metadata/pick_{pid}.png"/>')
        for (wrapper_id, instance_id, identify_id) in plate['object_ids']:
            lines.append('    <model_instance>')
            lines.append(f'      <metadata key="object_id" value="{wrapper_id}"/>')
            lines.append(f'      <metadata key="instance_id" value="{instance_id}"/>')
            lines.append(f'      <metadata key="identify_id" value="{identify_id}"/>')
            lines.append('    </model_instance>')
        lines.append('  </plate>')

    if assemble_items:
        lines.append('  <assemble>')
        for ai in assemble_items:
            t = f"1 0 0 0 1 0 0 0 1 0 0 {ai['tz']:.6f}"
            lines.append(
                f'   <assemble_item object_id="{ai["wrapper_id"]}" instance_id="0" '
                f'transform="{t}" offset="0 0 0" />'
            )
        lines.append('  </assemble>')

    lines.append('</config>')
    return '\n'.join(lines)


def build_slice_info():
    return """\
<?xml version="1.0" encoding="UTF-8"?>
<config>
  <header>
    <header_item key="X-BBL-Client-Type" value="slicer"/>
    <header_item key="X-BBL-Client-Version" value="01.03.00.11"/>
    <header_item key="X-BBL-Client-Name" value="ElegooSlicer"/>
  </header>
</config>"""


# Minimal 1x1 white PNG (base64-decoded) for plate thumbnails
_BLANK_PNG = bytes([
    0x89,0x50,0x4e,0x47,0x0d,0x0a,0x1a,0x0a,0x00,0x00,0x00,0x0d,0x49,0x48,0x44,0x52,
    0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x01,0x08,0x02,0x00,0x00,0x00,0x90,0x77,0x53,
    0xde,0x00,0x00,0x00,0x0c,0x49,0x44,0x41,0x54,0x08,0xd7,0x63,0xf8,0xff,0xff,0x3f,
    0x00,0x05,0xfe,0x02,0xfe,0xdc,0xcc,0x59,0xe7,0x00,0x00,0x00,0x00,0x49,0x45,0x4e,
    0x44,0xae,0x42,0x60,0x82,
])


# ===== OPENSCAD =====

def find_openscad():
    try:
        subprocess.run(["openscad", "--version"], capture_output=True, check=True)
        return "openscad"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    for p in [
        "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
        os.path.expanduser("~/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"),
    ]:
        if os.path.exists(p):
            return p
    print("ERROR: OpenSCAD not found. Install from https://openscad.org/downloads.html")
    sys.exit(1)


def render_stl(openscad_cmd, scad_file, model_code, component_num, fan_override, out_path):
    cmd = [
        openscad_cmd,
        "-o", str(out_path),
        "--export-format", "binstl",
        "-D", f'model_code="{model_code}"',
        "-D", f"component={component_num}",
        "-D", f"fan_size_override={fan_override}",
        str(scad_file),
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return r.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0
    except subprocess.TimeoutExpired:
        return False


def render_png(openscad_cmd, scad_file, model_code, component_num, fan_override,
               out_path, width=300, height=300):
    """Render a PNG preview thumbnail via OpenSCAD. Returns True on success."""
    cmd = [
        openscad_cmd,
        "-o", str(out_path),
        "--export-format", "png",
        f"--imgsize={width},{height}",
        "--autocenter",
        "--viewall",
        "--camera=0,0,0,45,0,25,500",
        "-D", f'model_code="{model_code}"',
        "-D", f"component={component_num}",
        "-D", f"fan_size_override={fan_override}",
        str(scad_file),
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return r.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0
    except subprocess.TimeoutExpired:
        return False


def resize_png(data, width, height):
    """
    Resize PNG bytes to (width, height) using Pillow if available.
    Returns resized bytes, or None if Pillow is not installed.
    """
    try:
        import io
        from PIL import Image
        img = Image.open(io.BytesIO(data))
        img = img.resize((width, height), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except ImportError:
        return None


# ===== 3MF PACKAGER =====

def create_3mf(stl_paths, output_3mf, model_name, fan_size, png_paths=None):
    """
    Build a complete ElegooSlicer-compatible 3MF from 4 STL files.

    Plate layout:
      Plate 1 "fan-mount": COMP_FRONT
      Plate 2 "rails":     COMP_LEFT + COMP_RIGHT (side by side)
      Plate 3 "grill":     COMP_REAR
    """
    reset_uuids()
    bed_center = BED_SIZE / 2.0

    # --- Load meshes ---
    meshes = {}
    for comp_id in [COMP_FRONT, COMP_LEFT, COMP_RIGHT, COMP_REAR]:
        print(f"      Loading {COMP_NAMES[comp_id]}...", end=" ", flush=True)
        try:
            verts, faces, bounds = read_binary_stl(stl_paths[comp_id])
        except Exception as e:
            print(f"FAILED: {e}")
            return False
        w = bounds[3] - bounds[0]
        l = bounds[4] - bounds[1]
        print(f"{len(verts)} verts, {len(faces)} tris, {w:.1f}x{l:.1f}mm")
        meshes[comp_id] = {'verts': verts, 'faces': faces, 'bounds': bounds}

    # --- Assign IDs (each part gets part_obj_id and wrapper_id) ---
    # part_obj_id = odd (1,3,5,7), wrapper_id = even (2,4,6,8)
    # Order: FRONT=1/2, LEFT=3/4, RIGHT=5/6, REAR=7/8
    id_map = {
        COMP_FRONT: (1, 2),
        COMP_LEFT:  (3, 4),
        COMP_RIGHT: (5, 6),
        COMP_REAR:  (7, 8),
    }

    # --- Compute transforms ---
    # ElegooSlicer's virtual canvas layout (from working example analysis):
    #   Plate 1: X in [0, BED_SIZE],        Y in [0, BED_SIZE]  → center (128, 128)
    #   Plate 2: X > BED_SIZE (right)       Y in [0, BED_SIZE]  → center (128+stride, 128)
    #   Plate 3: X in [0, BED_SIZE],        Y < 0 (below)       → center (128, 128-stride)
    plate_cx = {
        1: bed_center,               # fan-mount: normal bed X
        2: bed_center + PLATE_STRIDE, # rails: shifted right
        3: bed_center,               # grill: same X as plate 1
    }
    plate_cy = {
        1: bed_center,               # fan-mount: normal bed Y
        2: bed_center,               # rails: same Y as plate 1
        3: bed_center - PLATE_STRIDE, # grill: shifted into negative Y
    }

    # FRONT: plate 1, possibly rotated
    front_bounds = meshes[COMP_FRONT]['bounds']
    front_rotate = needs_rotation(front_bounds)
    front_transform = build_transform(front_rotate, plate_cx[1], plate_cy[1], 0.0)

    # REAR: plate 3, possibly rotated
    rear_bounds = meshes[COMP_REAR]['bounds']
    rear_rotate = needs_rotation(rear_bounds)
    rear_transform = build_transform(rear_rotate, plate_cx[3], plate_cy[3], 0.0)

    # RAILS: plate 2, side by side, centered on plate 2's virtual canvas position
    l_bounds = meshes[COMP_LEFT]['bounds']
    r_bounds = meshes[COMP_RIGHT]['bounds']
    l_w = l_bounds[3] - l_bounds[0]
    r_w = r_bounds[3] - r_bounds[0]
    rail_gap = 10.0
    left_tx  = plate_cx[2] - l_w / 2.0 - rail_gap / 2.0
    right_tx = plate_cx[2] + r_w / 2.0 + rail_gap / 2.0
    left_transform  = build_transform(False, left_tx,  plate_cy[2], 0.0)
    right_transform = build_transform(False, right_tx, plate_cy[2], 0.0)

    transforms = {
        COMP_FRONT: front_transform,
        COMP_LEFT:  left_transform,
        COMP_RIGHT: right_transform,
        COMP_REAR:  rear_transform,
    }

    # --- Build object file paths and metadata ---
    object_file_map = {
        COMP_FRONT: f"3D/Objects/front_fan_mount.model",
        COMP_LEFT:  f"3D/Objects/left_rail.model",
        COMP_RIGHT: f"3D/Objects/right_rail.model",
        COMP_REAR:  f"3D/Objects/rear_grill.model",
    }

    part_uuids    = {cid: make_uuid(f"00{i*2-1:02d}0") for i, cid in enumerate([COMP_FRONT,COMP_LEFT,COMP_RIGHT,COMP_REAR], 1)}
    wrapper_uuids = {cid: make_uuid(f"00{i*2:02d}0")   for i, cid in enumerate([COMP_FRONT,COMP_LEFT,COMP_RIGHT,COMP_REAR], 1)}
    item_uuids    = {cid: make_uuid(f"aa{i*2:02d}0")   for i, cid in enumerate([COMP_FRONT,COMP_LEFT,COMP_RIGHT,COMP_REAR], 1)}

    # --- Assemble object list for main model ---
    objects_meta = []
    for comp_id in [COMP_FRONT, COMP_LEFT, COMP_RIGHT, COMP_REAR]:
        part_id, wrapper_id = id_map[comp_id]
        objects_meta.append({
            'wrapper_id':   wrapper_id,
            'wrapper_uuid': wrapper_uuids[comp_id],
            'part_obj_id':  part_id,
            'part_uuid':    part_uuids[comp_id],
            'object_path':  f"/{object_file_map[comp_id]}",
        })

    build_items = []
    for comp_id in [COMP_FRONT, COMP_LEFT, COMP_RIGHT, COMP_REAR]:
        _, wrapper_id = id_map[comp_id]
        build_items.append({
            'wrapper_id': wrapper_id,
            'item_uuid':  item_uuids[comp_id],
            'transform':  transforms[comp_id],
        })

    # --- Plate assignments ---
    identify_base = 6000
    plates = [
        {
            'plater_id': 1, 'plater_name': 'fan-mount',
            'object_ids': [(id_map[COMP_FRONT][1], 0, identify_base + 1)],
        },
        {
            'plater_id': 2, 'plater_name': 'rails',
            'object_ids': [
                (id_map[COMP_LEFT][1],  0, identify_base + 2),
                (id_map[COMP_RIGHT][1], 0, identify_base + 3),
            ],
        },
        {
            'plater_id': 3, 'plater_name': 'grill',
            'object_ids': [(id_map[COMP_REAR][1], 0, identify_base + 4)],
        },
    ]

    # model_settings object list
    settings_objects = []
    for comp_id in [COMP_FRONT, COMP_LEFT, COMP_RIGHT, COMP_REAR]:
        part_id, wrapper_id = id_map[comp_id]
        b = meshes[comp_id]['bounds']
        settings_objects.append({
            'wrapper_id':    wrapper_id,
            'part_obj_id':   part_id,
            'name':          COMP_NAMES[comp_id],
            'source_offset_x': (b[0] + b[3]) / 2.0,
            'source_offset_y': (b[1] + b[4]) / 2.0,
            'source_offset_z': b[2],
        })

    assemble_items = [
        {'wrapper_id': id_map[cid][1], 'tz': 0.0}
        for cid in [COMP_FRONT, COMP_LEFT, COMP_RIGHT, COMP_REAR]
    ]

    # --- Generate rotation notes for console ---
    if front_rotate:
        print(f"      Fan mount rotated 45° (width > {MAX_STRAIGHT}mm)")
    if rear_rotate:
        print(f"      Rear grill rotated 45° (width > {MAX_STRAIGHT}mm)")

    # --- Write 3MF ZIP ---
    print(f"      Writing {output_3mf.name}...", end=" ", flush=True)
    try:
        with zipfile.ZipFile(output_3mf, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Core structure
            zf.writestr("[Content_Types].xml", build_content_types())
            zf.writestr("_rels/.rels", build_root_rels())

            # Per-component object model files
            for comp_id in [COMP_FRONT, COMP_LEFT, COMP_RIGHT, COMP_REAR]:
                part_id, _ = id_map[comp_id]
                xml = build_object_model_xml(
                    part_id,
                    meshes[comp_id]['verts'],
                    meshes[comp_id]['faces'],
                    part_uuids[comp_id],
                )
                zf.writestr(object_file_map[comp_id], xml)

            # Main model (component wrappers only, no inline mesh)
            main_model = build_main_model_xml(objects_meta, build_items)
            zf.writestr("3D/3dmodel.model", main_model)

            # Rels for the main model → object files
            obj_paths = [f"/{p}" for p in object_file_map.values()]
            zf.writestr("3D/_rels/3dmodel.model.rels", build_main_model_rels(obj_paths))

            # Metadata
            settings_xml = build_model_settings(settings_objects, plates, assemble_items)
            zf.writestr("Metadata/model_settings.config", settings_xml)
            zf.writestr("Metadata/slice_info.config", build_slice_info())

            # Plate thumbnails: use rendered PNGs if available, else blank
            # Plate 1=fan mount (COMP_FRONT), 2=rails (COMP_LEFT), 3=grill (COMP_REAR)
            plate_comp = {1: COMP_FRONT, 2: COMP_LEFT, 3: COMP_REAR}
            for plate_num, comp_id in plate_comp.items():
                full_data  = _BLANK_PNG
                small_data = _BLANK_PNG
                if png_paths and comp_id in png_paths:
                    png_path = png_paths[comp_id]
                    if png_path.exists() and png_path.stat().st_size > 0:
                        full_data = png_path.read_bytes()
                        small_data = resize_png(full_data, 150, 150) or full_data
                zf.writestr(f"Metadata/plate_{plate_num}.png", full_data)
                zf.writestr(f"Metadata/plate_{plate_num}_small.png", small_data)
                # Extra slicer-expected image slots (blank; slicer generates real ones on save)
                zf.writestr(f"Metadata/plate_no_light_{plate_num}.png", full_data)
                zf.writestr(f"Metadata/top_{plate_num}.png", _BLANK_PNG)
                zf.writestr(f"Metadata/pick_{plate_num}.png", _BLANK_PNG)

        size_kb = output_3mf.stat().st_size // 1024
        print(f"done ({size_kb} KB)")
        return True

    except Exception as e:
        import traceback
        print(f"FAILED: {e}")
        traceback.print_exc()
        return False


# ===== MAIN =====

def sanitize(name):
    """Filesystem-safe name: spaces→_, dots→_, slashes stay as - (already in names)."""
    return name.replace(" ", "_").replace(".", "_")


def main():
    openscad_cmd = find_openscad()
    print(f"OpenSCAD: {openscad_cmd}")

    scad_path = Path(SCAD_FILE)
    if not scad_path.exists():
        print(f"ERROR: {SCAD_FILE} not found — run from the fan_controllers directory.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Build job list: (model_code, name, effective_fan_size, override_value)
    jobs = []
    for model_code, name, default_fan in CONTROLLERS:
        jobs.append((model_code, name, default_fan, 0))
        if default_fan != OVERRIDE_FAN_SIZE:
            jobs.append((model_code, name, OVERRIDE_FAN_SIZE, OVERRIDE_FAN_SIZE))

    total   = len(jobs)
    success = 0
    failed  = 0

    print(f"\nControllers: {len(CONTROLLERS)}")
    print(f"Total jobs:  {total}  (default + 40mm override where applicable)")
    print(f"Output:      {OUTPUT_DIR.absolute()}")
    print(f"Settings:    {MATERIAL}, {INFILL_PCT}% infill")
    print(f"Rotation:    parts wider than {MAX_STRAIGHT}mm rotated 45°")
    print(f"Plates:      fan-mount | rails (L+R) | grill")
    print("=" * 70)

    with tempfile.TemporaryDirectory(prefix="orca3mf_") as tmp:
        tmp_path = Path(tmp)

        for idx, (model_code, name, fan_size, fan_override) in enumerate(jobs, 1):
            safe   = sanitize(name)
            fname  = f"{safe}_{fan_size}mm.3mf"
            output = OUTPUT_DIR / fname

            print(f"\n[{idx}/{total}] {name}  ({fan_size}mm)")
            override_note = "default" if fan_override == 0 else f"{fan_override}mm override"
            print(f"  Code: {model_code}  Fan: {override_note}")

            # Render 4 STLs
            stl_paths = {}
            ok = True
            for comp_id in [COMP_FRONT, COMP_LEFT, COMP_RIGHT, COMP_REAR]:
                stl = tmp_path / f"{model_code}_{fan_size}_comp{comp_id}.stl"
                print(f"    Rendering {COMP_NAMES[comp_id]}...", end=" ", flush=True)
                if render_stl(openscad_cmd, scad_path, model_code, comp_id, fan_override, stl):
                    stl_paths[comp_id] = stl
                    print("ok")
                else:
                    print("FAILED")
                    ok = False
                    break

            if not ok:
                failed += 1
                continue

            # Render PNG thumbnails for 3 plates (front, left rail, grill)
            # Left rail is used as stand-in for the rails plate thumbnail
            png_paths = {}
            for comp_id in [COMP_FRONT, COMP_LEFT, COMP_REAR]:
                png = tmp_path / f"{model_code}_{fan_size}_plate{comp_id}.png"
                print(f"    Preview {COMP_NAMES[comp_id]}...", end=" ", flush=True)
                if render_png(openscad_cmd, scad_path, model_code, comp_id, fan_override, png):
                    png_paths[comp_id] = png
                    print("ok")
                else:
                    print("skipped")

            if create_3mf(stl_paths, output, name, fan_size, png_paths):
                success += 1
            else:
                failed += 1

    print("\n" + "=" * 70)
    print(f"Done: {success} succeeded, {failed} failed  (total {total})")
    print(f"Output: {OUTPUT_DIR.absolute()}")
    if success:
        print(f"\nIn ElegooSlicer/OrcaSlicer:")
        print(f"  File → Import → Import 3MF/STL/STEP...")
        print(f"  Apply PETG profile with {INFILL_PCT}% infill, then slice.")


if __name__ == "__main__":
    main()
