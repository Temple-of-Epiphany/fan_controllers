# Slicer-Specific 3MF Extensions

## Overview

Standard 3MF contains only geometry, metadata, and materials. Each slicer adds
proprietary extension files inside the ZIP for print settings, per-object configs,
thumbnails, and build plate organization. These extensions are backwards-compatible —
other slicers simply ignore the unknown files.

---

## PrusaSlicer / Slic3r

**Extension files:**
```
Metadata/
├── Slic3r_PE.config          ← global printer + filament + print settings
├── Slic3r_PE_model.config    ← per-object and per-modifier settings
└── thumbnail.png             ← preview image (optional)
```

**Reading global config:**
```python
import zipfile, configparser

with zipfile.ZipFile("project.3mf") as z:
    if "Metadata/Slic3r_PE.config" in z.namelist():
        raw = z.read("Metadata/Slic3r_PE.config").decode("utf-8")
        cfg = configparser.ConfigParser()
        cfg.read_string("[root]\n" + raw)
        settings = dict(cfg["root"])

# Common keys:
settings["layer_height"]       # e.g., "0.2"
settings["fill_density"]       # e.g., "15%"
settings["support_material"]   # e.g., "0" or "1"
settings["perimeters"]         # e.g., "3"
settings["filament_colour"]    # e.g., "#FF8000"
settings["printer_model"]      # e.g., "MK4"
```

**Reading per-object config:**
```python
from xml.etree import ElementTree as ET

with zipfile.ZipFile("project.3mf") as z:
    if "Metadata/Slic3r_PE_model.config" in z.namelist():
        xml = z.read("Metadata/Slic3r_PE_model.config")
        root = ET.fromstring(xml)
        for obj in root.findall(".//object"):
            print("Object ID:", obj.get("id"))
            for meta in obj.findall("metadata"):
                print(f"  {meta.get('key')}: {meta.get('value')}")
```

**Injecting PrusaSlicer settings into an existing 3MF:**
```python
import zipfile, shutil, os

def inject_prusa_settings(src, dst, settings: dict):
    """Add or replace Slic3r_PE.config in a 3MF."""
    # Build INI-style config content
    config_lines = [f"{k} = {v}" for k, v in settings.items()]
    config_content = "\n".join(config_lines).encode("utf-8")

    with zipfile.ZipFile(src, "r") as zin, \
         zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        # Copy all existing files
        for item in zin.infolist():
            if item.filename != "Metadata/Slic3r_PE.config":
                zout.writestr(item, zin.read(item.filename))
        # Add/replace config
        zout.writestr("Metadata/Slic3r_PE.config", config_content)

inject_prusa_settings("model.3mf", "model_with_settings.3mf", {
    "layer_height": "0.2",
    "fill_density": "20%",
    "perimeters": "3",
    "support_material": "0",
})
```

---

## Orca Slicer

Orca is a fork of Bambu Studio with PrusaSlicer compatibility.

**Extension files:**
```
Metadata/
├── Slic3r_PE.config           ← same format as PrusaSlicer
├── Slic3r_PE_model.config     ← same format as PrusaSlicer
├── model_settings.config      ← Bambu-style plate/object config
└── slice_info.config          ← slice result metadata
```

Orca can read PrusaSlicer project 3MF files and vice versa for most settings.

---

## Bambu Studio

**Extension files:**
```
Metadata/
├── model_settings.config    ← plate and object configuration (proprietary)
├── slice_info.config        ← slice output metadata
├── thumbnail.png            ← main preview
└── thumbnail_small.png      ← small preview

Auxiliaries/
└── ...                      ← filament presets, project assets
```

Bambu's `model_settings.config` is a JSON-like key=value format but is not
documented publicly. It is not cross-compatible with PrusaSlicer.

**Extract Bambu thumbnail:**
```python
import zipfile
from PIL import Image
import io

with zipfile.ZipFile("bambu_project.3mf") as z:
    if "Metadata/thumbnail.png" in z.namelist():
        img_data = z.read("Metadata/thumbnail.png")
        img = Image.open(io.BytesIO(img_data))
        img.save("thumbnail.png")
        print(f"Thumbnail: {img.size}")
```

---

## Cura

Cura 5+ reads and writes standard 3MF for geometry. It does not embed print
settings into the 3MF file — settings stay in Cura project files (`.3mf.project`).
For slicer-portable files, plain 3MF geometry from OpenSCAD works well with Cura.

---

## IdeaMaker (Raise3D)

IdeaMaker reads standard 3MF geometry. Print settings are stored in its own
`.idea` project format, not embedded in the 3MF.

---

## Portable 3MF Recommendations

For maximum slicer compatibility when distributing models:

1. Use standard core 3MF — only `3D/3dmodel.model`, `[Content_Types].xml`, `_rels/.rels`
2. Include standard metadata: `Title`, `Author`, `Description`, `CreationDate`
3. Do not include slicer-specific config files unless targeting a specific slicer
4. Use millimeter units
5. Ensure mesh is manifold (watertight, no holes, correct winding)
6. Keep object names meaningful — slicers display them

---

## 3MF Spec Resources

- Core spec: https://github.com/3MFConsortium/spec_core
- Materials extension: https://github.com/3MFConsortium/spec_materials
- Slice extension: https://github.com/3MFConsortium/spec_slice
- Beam lattice: https://github.com/3MFConsortium/spec_beamlattice
- Official validator: https://www.3mf.io/3mf-consortium/3mf-validator/
