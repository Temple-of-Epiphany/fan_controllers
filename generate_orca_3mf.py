#!/usr/bin/env python3
"""
Generate per-model OrcaSlicer 3MF files for all Victron MPPT cooling mounts.

Author: Colin Bitterfield
Email: colin@bitterfield.com
Date Created: 2026-02-17
Date Updated: 2026-02-17
Version: 1.0.0

Generates one 3MF per controller model x fan size combination:
  - Default fan size (from database)
  - 40mm fan override (skipped if model default is already 40mm)

3MF plate layout (3 plates per file):
  Plate 1: Front fan mount (alone)
  Plate 2: Rear grill (alone)
  Plate 3: Left rail + Right rail (side by side)

Embedded settings: PETG material hint, 20% sparse infill
File naming: {Model_Name}_{fan_size}mm.3mf
  e.g., SmartSolar_MPPT_100_30_50mm.3mf
        SmartSolar_MPPT_100_30_40mm.3mf

Output directory: output_orca_3mf/
"""

import os
import sys
import struct
import shutil
import zipfile
import subprocess
import tempfile
from pathlib import Path

# ===== CONTROLLER DATABASE =====
# (model_code, display_name, default_fan_size)
# Mirrors solar_controller_cooling_mount.scad controller_db[]
CONTROLLERS = [
    # A1 Config - 3x50mm fans
    ("SCC020030200",  "BlueSolar MPPT 100-30",             50),
    ("SCC110030210",  "SmartSolar MPPT 100-30",            50),
    ("SCC020050200",  "BlueSolar MPPT 100-50",             50),
    ("SCC020035000",  "BlueSolar MPPT 150-35",             50),
    ("SCC115045222",  "BlueSolar MPPT 150-45",             50),
    ("SCC110050210",  "SmartSolar MPPT 100-50",            50),
    ("SCC115035210",  "SmartSolar MPPT 150-35",            50),
    ("SCC115045212",  "SmartSolar MPPT 150-45",            50),
    ("ORI121236120",  "Orion-Tr Smart 12-12-30A",          50),
    ("ORI122436120",  "Orion-Tr Smart 12-24-15A",          50),
    ("ORI241236120",  "Orion-Tr Smart 24-12-30A",          50),
    # A3 Config - 2x50mm fans
    ("SCC110020070R", "BlueSolar MPPT 100-20",             50),
    ("SCC110020170R", "BlueSolar MPPT 100-20 48V",         50),
    ("SCC110020060R", "SmartSolar MPPT 100-20",            50),
    ("SCC110020160R", "SmartSolar MPPT 100-20 48V",        50),
    # A4 Config - 4x50mm fans
    ("SCC115060210",  "SmartSolar MPPT 150-60-Tr",         50),
    ("SCC115070210",  "SmartSolar MPPT 150-70-Tr",         50),
    # A4_MC4 Config - 4x50mm fans
    ("SCC115060310",  "SmartSolar MPPT 150-60-MC4",        50),
    ("SCC115070310",  "SmartSolar MPPT 150-70-MC4",        50),
    # B1 Config - 4x50mm fans
    ("SCC115085211",  "SmartSolar MPPT 150-85-Tr",         50),
    ("SCC115110211",  "SmartSolar MPPT 150-100-Tr",        50),
    ("SCC125085210",  "SmartSolar MPPT 250-85-Tr",         50),
    ("SCC125110210",  "SmartSolar MPPT 250-100-Tr",        50),
    # B2 Config - 4x50mm fans (Tr VE.Can)
    ("SCC115085411",  "SmartSolar MPPT 150-85-Tr VE.Can",  50),
    ("SCC115110410",  "SmartSolar MPPT 150-100-Tr VE.Can", 50),
    ("SCC115110420",  "BlueSolar MPPT 150-100-Tr VE.Can",  50),
    ("SCC125085411",  "SmartSolar MPPT 250-85-Tr VE.Can",  50),
    ("SCC125110411",  "SmartSolar MPPT 250-100-Tr VE.Can", 50),
    ("SCC125110441",  "BlueSolar MPPT 250-100-Tr VE.Can",  50),
    # B2_MC4 Config - 4x50mm fans (MC4 VE.Can)
    ("SCC115085511",  "SmartSolar MPPT 150-85-MC4 VE.Can",  50),
    ("SCC115110511",  "SmartSolar MPPT 150-100-MC4 VE.Can", 50),
    ("SCC125085511",  "SmartSolar MPPT 250-85-MC4 VE.Can",  50),
    ("SCC125110512",  "SmartSolar MPPT 250-100-MC4 VE.Can", 50),
    # B3 Config - 4x50mm fans
    ("SCC125060221",  "SmartSolar MPPT 250-60-Tr",         50),
    ("SCC125070220",  "SmartSolar MPPT 250-70-Tr",         50),
    # C1 Config - 2x40mm fans (housing-based)
    ("SCC010010050R", "BlueSolar MPPT 75-10",              40),
    ("SCC010015050R", "BlueSolar MPPT 75-15",              40),
    ("SCC075010060R", "SmartSolar MPPT 75-10",             40),
    ("SCC075015060R", "SmartSolar MPPT 75-15",             40),
    # C2 Config - 2x40mm fans (housing-based)
    ("SCC010015200R", "SmartSolar MPPT 100-15-C2",         40),
    ("SCC110015060R", "SmartSolar MPPT 100-15",            40),
]

OVERRIDE_FAN_SIZE = 40   # The alternate fan size to generate
MATERIAL      = "PETG"
INFILL_PCT    = 20       # Sparse infill %
SCAD_FILE     = "solar_controller_cooling_mount.scad"
OUTPUT_DIR    = Path("output_orca_3mf")

# OpenSCAD component numbers
COMP_FRONT = 1
COMP_LEFT  = 2
COMP_RIGHT = 3
COMP_REAR  = 4


# ===== STL READER =====

def read_binary_stl(path):
    """
    Parse a binary STL file into deduplicated vertices and face index lists.

    Returns:
        vertices: list of (x, y, z) float tuples
        faces: list of (i, j, k) integer index tuples
        bounds: (min_x, min_y, min_z, max_x, max_y, max_z)
    """
    with open(path, 'rb') as f:
        header = f.read(80)
        # Detect ASCII STL (starts with "solid")
        if header.lstrip().startswith(b'solid'):
            # Peek at whether it's really ASCII
            f.seek(0)
            content = f.read()
            if b'facet normal' in content:
                return _read_ascii_stl(content)
        f.seek(84)
        n_tri = struct.unpack('<I', f.read(4))[0] if len(header) == 80 else 0
        # Re-read properly
        f.seek(0)
        f.read(80)
        n_tri = struct.unpack('<I', f.read(4))[0]

        vertex_map = {}
        vertices = []
        faces = []
        UNPACK_3F = struct.Struct('<3f')

        for _ in range(n_tri):
            f.read(12)  # skip normal
            raw_verts = []
            for _ in range(3):
                v = UNPACK_3F.unpack(f.read(12))
                key = (round(v[0], 5), round(v[1], 5), round(v[2], 5))
                if key not in vertex_map:
                    vertex_map[key] = len(vertices)
                    vertices.append(key)
                raw_verts.append(vertex_map[key])
            faces.append(tuple(raw_verts))
            f.read(2)  # attribute byte count

    if not vertices:
        raise ValueError(f"No geometry found in {path}")

    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]
    bounds = (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))
    return vertices, faces, bounds


def _read_ascii_stl(content):
    """Parse ASCII STL bytes."""
    import re
    vertex_map = {}
    vertices = []
    faces = []
    pattern = re.compile(
        rb'facet normal\s+[\d.eE+\-]+\s+[\d.eE+\-]+\s+[\d.eE+\-]+'
        rb'\s+outer loop'
        rb'(?:\s+vertex\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)){3}'
        rb'\s+endloop\s+endfacet',
        re.DOTALL
    )
    vert_pattern = re.compile(
        rb'vertex\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)'
    )
    facets = re.findall(rb'outer loop(.*?)endloop', content, re.DOTALL)
    for facet in facets:
        verts_raw = vert_pattern.findall(facet)
        if len(verts_raw) != 3:
            continue
        face = []
        for vr in verts_raw:
            v = (round(float(vr[0]), 5), round(float(vr[1]), 5), round(float(vr[2]), 5))
            if v not in vertex_map:
                vertex_map[v] = len(vertices)
                vertices.append(v)
            face.append(vertex_map[v])
        faces.append(tuple(face))

    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]
    bounds = (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))
    return vertices, faces, bounds


# ===== 3MF XML BUILDERS =====

def _fmt_transform(tx=0.0, ty=0.0, tz=0.0):
    """Return a 3MF 3x4 transform string: identity rotation + translation."""
    return f"1 0 0 0 1 0 0 0 1 {tx:.4f} {ty:.4f} {tz:.4f}"


def _fmt_matrix16(tx=0.0, ty=0.0, tz=0.0):
    """Return a 16-value 4x4 identity + translation matrix for model_settings."""
    return f"1 0 0 0  0 1 0 0  0 0 1 0  {tx:.4f} {ty:.4f} {tz:.4f} 1"


def build_content_types_xml():
    return """\
<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
  <Default Extension="config" ContentType="application/xml"/>
</Types>"""


def build_rels_xml():
    return """\
<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Target="/3D/3dmodel.model" Id="rel-1"
    Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>"""


def build_3dmodel_xml(mesh_data):
    """
    Build the core 3MF model XML.

    mesh_data: list of dicts:
      {id, name, vertices, faces, bounds}

    Objects are placed flat at Z=0 (tz = -min_z), centered in XY.
    """
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<model unit="millimeter" xml:lang="en-US"'
        ' xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">',
        '  <resources>',
    ]

    for m in mesh_data:
        obj_id = m['id']
        lines.append(f'    <object id="{obj_id}" name="{m["name"]}" type="model">')
        lines.append('      <mesh>')
        lines.append('        <vertices>')
        for v in m['vertices']:
            lines.append(f'          <v x="{v[0]:.5f}" y="{v[1]:.5f}" z="{v[2]:.5f}"/>')
        lines.append('        </vertices>')
        lines.append('        <triangles>')
        for f in m['faces']:
            lines.append(f'          <t v1="{f[0]}" v2="{f[1]}" v3="{f[2]}"/>')
        lines.append('        </triangles>')
        lines.append('      </mesh>')
        lines.append('    </object>')

    lines.append('  </resources>')
    lines.append('  <build>')

    for m in mesh_data:
        bnd = m['bounds']
        # Center XY at origin, lift bottom to Z=0
        tx = -(bnd[0] + bnd[3]) / 2.0
        ty = -(bnd[1] + bnd[4]) / 2.0
        tz = -bnd[2]
        t = _fmt_transform(tx, ty, tz)
        lines.append(f'    <item objectid="{m["id"]}" transform="{t}"/>')

    lines.append('  </build>')
    lines.append('</model>')
    return '\n'.join(lines)


def build_model_settings_xml(mesh_data, plate_assignments):
    """
    Build Metadata/model_settings.config for OrcaSlicer plate assignments.

    plate_assignments: list of plates, each a dict:
      {plate_index, plate_name, object_ids: [(id, tx, ty)]}
    """
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<config>',
    ]

    for plate in plate_assignments:
        lines.append('  <plate>')
        lines.append(f'    <metadata key="plate_index" value="{plate["plate_index"]}"/>')
        lines.append(f'    <metadata key="plate_name" value="{plate["plate_name"]}"/>')
        for obj_id, tx, ty in plate['object_ids']:
            mat = _fmt_matrix16(tx, ty, 0.0)
            lines.append(f'    <model id="{obj_id}" matrix="{mat}"/>')
        lines.append('  </plate>')

    # Per-object metadata
    for m in mesh_data:
        lines.append(f'  <object id="{m["id"]}">')
        lines.append(f'    <metadata key="name" value="{m["name"]}"/>')
        lines.append(f'    <metadata key="extruder" value="1"/>')
        lines.append('  </object>')

    lines.append('</config>')
    return '\n'.join(lines)


def build_project_settings_xml(model_name, fan_size):
    """
    Build Metadata/project_settings.config with PETG + infill hint.
    OrcaSlicer reads this for default print settings.
    """
    return f"""\
<?xml version="1.0" encoding="utf-8"?>
<config>
  <print_settings>
    <metadata key="filament_type" value="{MATERIAL}"/>
    <metadata key="sparse_infill_density" value="{INFILL_PCT}%"/>
    <metadata key="layer_height" value="0.2"/>
    <metadata key="wall_loops" value="4"/>
    <metadata key="top_shell_layers" value="5"/>
    <metadata key="bottom_shell_layers" value="5"/>
    <metadata key="support_type" value="none"/>
    <metadata key="description" value="Victron MPPT Cooling Mount - {model_name} {fan_size}mm fans"/>
    <metadata key="author" value="Colin Bitterfield"/>
  </print_settings>
</config>"""


# ===== OPENSCAD INTERFACE =====

def find_openscad():
    """Locate OpenSCAD CLI executable."""
    try:
        subprocess.run(["openscad", "--version"], capture_output=True, check=True)
        return "openscad"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    macos_paths = [
        "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
        os.path.expanduser("~/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"),
    ]
    for p in macos_paths:
        if os.path.exists(p):
            return p

    print("ERROR: OpenSCAD not found.")
    print("Install from https://openscad.org/downloads.html")
    sys.exit(1)


def render_stl(openscad_cmd, scad_file, model_code, component_num,
               fan_override, output_path):
    """
    Render one STL via OpenSCAD CLI.

    Returns True on success, False on failure.
    """
    cmd = [
        openscad_cmd,
        "-o", str(output_path),
        "-D", f'model_code="{model_code}"',
        "-D", f"component={component_num}",
        "-D", f"fan_size_override={fan_override}",
        str(scad_file),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"      OpenSCAD error: {result.stderr[:200]}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print("      OpenSCAD timed out (300s)")
        return False


# ===== 3MF PACKAGER =====

def compute_plate_positions(mesh_data_map):
    """
    Compute plate positions for 3 plates:
      Plate 1: front fan mount (id=1) — centered at origin
      Plate 2: rear grill (id=4) — centered at origin
      Plate 3: left rail (id=2) + right rail (id=3) — side by side

    Returns: list of plate dicts for build_model_settings_xml()
    """
    front = mesh_data_map[COMP_FRONT]
    rear  = mesh_data_map[COMP_REAR]
    left  = mesh_data_map[COMP_LEFT]
    right = mesh_data_map[COMP_RIGHT]

    # Rail placement: left and right side by side with 10mm gap
    l_bnd = left['bounds']
    r_bnd = right['bounds']
    l_width = l_bnd[3] - l_bnd[0]
    r_width = r_bnd[3] - r_bnd[0]
    gap = 10.0
    total_rails = l_width + gap + r_width
    left_tx  = -total_rails / 2.0 + l_width / 2.0
    right_tx =  total_rails / 2.0 - r_width / 2.0

    plates = [
        {
            "plate_index": 1,
            "plate_name": "Fan Mount",
            "object_ids": [(COMP_FRONT, 0.0, 0.0)],
        },
        {
            "plate_index": 2,
            "plate_name": "Rear Grill",
            "object_ids": [(COMP_REAR, 0.0, 0.0)],
        },
        {
            "plate_index": 3,
            "plate_name": "Rails",
            "object_ids": [
                (COMP_LEFT,  left_tx,  0.0),
                (COMP_RIGHT, right_tx, 0.0),
            ],
        },
    ]
    return plates


def create_3mf(stl_paths, output_3mf, model_name, fan_size):
    """
    Build a 3MF ZIP from 4 STL files with OrcaSlicer plate metadata.

    stl_paths: dict {COMP_FRONT: path, COMP_LEFT: path, ...}
    output_3mf: Path to write .3mf
    """
    # Component display names
    comp_names = {
        COMP_FRONT: "Front Fan Mount",
        COMP_LEFT:  "Left Rail",
        COMP_RIGHT: "Right Rail",
        COMP_REAR:  "Rear Grill",
    }

    # Load all meshes
    mesh_data = []
    mesh_data_map = {}
    for comp_id in [COMP_FRONT, COMP_LEFT, COMP_RIGHT, COMP_REAR]:
        path = stl_paths[comp_id]
        print(f"      Loading {comp_names[comp_id]}...", end=" ", flush=True)
        try:
            vertices, faces, bounds = read_binary_stl(path)
        except Exception as e:
            print(f"FAILED ({e})")
            return False
        print(f"{len(vertices)} verts, {len(faces)} tris")
        entry = {
            'id': comp_id,
            'name': comp_names[comp_id],
            'vertices': vertices,
            'faces': faces,
            'bounds': bounds,
        }
        mesh_data.append(entry)
        mesh_data_map[comp_id] = entry

    # Sort mesh_data by id for consistent XML output
    mesh_data.sort(key=lambda m: m['id'])

    # Compute plate assignments
    plate_assignments = compute_plate_positions(mesh_data_map)

    # Build XML content
    print("      Building 3MF XML...", end=" ", flush=True)
    content_types  = build_content_types_xml()
    rels           = build_rels_xml()
    model_xml      = build_3dmodel_xml(mesh_data)
    settings_xml   = build_model_settings_xml(mesh_data, plate_assignments)
    project_xml    = build_project_settings_xml(model_name, fan_size)
    print("done")

    # Write ZIP
    print(f"      Writing {output_3mf.name}...", end=" ", flush=True)
    try:
        with zipfile.ZipFile(output_3mf, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types)
            zf.writestr("_rels/.rels", rels)
            zf.writestr("3D/3dmodel.model", model_xml)
            zf.writestr("Metadata/model_settings.config", settings_xml)
            zf.writestr("Metadata/project_settings.config", project_xml)
        size_kb = output_3mf.stat().st_size // 1024
        print(f"done ({size_kb} KB)")
        return True
    except Exception as e:
        print(f"FAILED ({e})")
        return False


# ===== MAIN =====

def sanitize(name):
    """Convert display name to safe filename segment."""
    return name.replace(" ", "_").replace("/", "-").replace(".", "_")


def main():
    openscad_cmd = find_openscad()
    print(f"OpenSCAD: {openscad_cmd}")

    scad_path = Path(SCAD_FILE)
    if not scad_path.exists():
        print(f"ERROR: {SCAD_FILE} not found. Run from the fan_controllers directory.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Build list of (model_code, name, fan_size) jobs to generate
    jobs = []
    for model_code, name, default_fan in CONTROLLERS:
        jobs.append((model_code, name, default_fan, 0))          # 0 = no override = default
        if default_fan != OVERRIDE_FAN_SIZE:
            jobs.append((model_code, name, OVERRIDE_FAN_SIZE, OVERRIDE_FAN_SIZE))  # 40mm override

    total = len(jobs)
    print(f"\nControllers: {len(CONTROLLERS)}")
    print(f"Jobs (model x fan size): {total}")
    print(f"Output: {OUTPUT_DIR.absolute()}")
    print(f"Settings: {MATERIAL}, {INFILL_PCT}% infill")
    print(f"Plates per 3MF: Fan Mount | Rear Grill | Rails (L+R)")
    print("=" * 70)

    success = 0
    failed  = 0

    with tempfile.TemporaryDirectory(prefix="orca3mf_") as tmp:
        tmp_path = Path(tmp)

        for idx, (model_code, name, fan_size, fan_override) in enumerate(jobs, 1):
            safe_name = sanitize(name)
            fname = f"{safe_name}_{fan_size}mm.3mf"
            output_3mf = OUTPUT_DIR / fname

            print(f"\n[{idx}/{total}] {name}  ({fan_size}mm)")
            print(f"  Code: {model_code}  Override: {fan_override if fan_override else 'none (default)'}")
            print(f"  Output: {fname}")

            # Generate 4 STLs
            stl_paths = {}
            comp_names_short = {
                COMP_FRONT: "front_fan_mount",
                COMP_LEFT:  "left_rail",
                COMP_RIGHT: "right_rail",
                COMP_REAR:  "rear_grill",
            }
            stl_ok = True
            for comp_id, comp_name in comp_names_short.items():
                stl_path = tmp_path / f"{model_code}_{fan_size}_{comp_name}.stl"
                print(f"    Rendering {comp_name}...", end=" ", flush=True)
                ok = render_stl(
                    openscad_cmd, scad_path,
                    model_code, comp_id, fan_override,
                    stl_path
                )
                if ok and stl_path.exists() and stl_path.stat().st_size > 0:
                    stl_paths[comp_id] = stl_path
                    print("ok")
                else:
                    print("FAILED")
                    stl_ok = False
                    break

            if not stl_ok:
                print(f"  SKIPPED: STL generation failed")
                failed += 1
                continue

            # Pack into 3MF
            if create_3mf(stl_paths, output_3mf, name, fan_size):
                success += 1
            else:
                failed += 1

    # Summary
    print("\n" + "=" * 70)
    print(f"Complete: {success} succeeded, {failed} failed out of {total} jobs")
    print(f"Output: {OUTPUT_DIR.absolute()}")
    if success > 0:
        print(f"\nImport into OrcaSlicer:")
        print(f"  File -> Import -> Import 3MF/STL/STEP...")
        print(f"  Each 3MF has 3 plates: Fan Mount | Grill | Rails")
        print(f"  Apply PETG profile with {INFILL_PCT}% infill before slicing")


if __name__ == "__main__":
    main()
