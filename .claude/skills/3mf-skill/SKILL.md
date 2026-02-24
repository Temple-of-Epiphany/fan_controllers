---
name: 3mf
description: >
  Create, read, inspect, modify, merge, and enrich 3MF (3D Manufacturing Format) files
  programmatically. Use this skill whenever a user wants to work with .3mf files directly —
  including converting STL to 3MF, adding metadata or print settings to a 3MF, merging
  multiple 3MF or STL files into a single 3MF, embedding color or material data, extracting
  mesh data from a 3MF, validating a 3MF file, generating build plates with multiple objects,
  or scripting 3MF creation for CI/build pipelines. Also use when the user asks about 3MF
  file structure, what's inside a .3mf, slicer-specific 3MF extensions (PrusaSlicer, Bambu,
  Orca), or how to use the lib3mf Python bindings. Pairs with the openscad skill — use that
  skill to generate geometry first, then this skill to enrich or transform the output.
---

# 3MF Skill

3MF (3D Manufacturing Format) is the modern replacement for STL. It is a ZIP archive
containing XML files that describe geometry, materials, colors, metadata, and optionally
slicer print settings.

---

## ⚡ Startup Sequence — Run This Every Time

**Always execute this sequence at the start of any 3MF session before doing any work.**

### Step 1: Check Existing Configuration

Check these three sources in order for `slicer` and `printer` values:

**Source A — Project Memory (`memory_user_edits` / userMemories)**
Look for entries containing keywords: `slicer`, `printer`, `3mf_target`,
`3d printing`, `elegoo`, `orca`, `bambu`, `prusa`.

**Source B — Project Instructions**
Scan for a `[3D Printing]`, `[Slicer]`, or `[Printer]` section.

**Source C — `~/Projects/Claude.md`**
Read via OSAScript or Desktop Commander (never bash_tool for local files).
Look for slicer/printer lines in any 3D printing section.

### Step 2: Determine State and Act

**If slicer AND printer found in any source:**
→ Use those values. State briefly: *"Using [Slicer] on [Printer] (from [source])."*
→ Skip to Step 4.

**If either value is missing:**
→ Proceed to Step 3.

### Step 3: Ask the User

Present defaults and ask once — do not ask again if already in memory:

```
I need your target slicer and printer for this session.

  Default slicer:  Orca Slicer
  Default printer: Elegoo CC1

Press Enter to accept defaults, or specify: "Slicer: X, Printer: Y"
```

Accept response. Confirm back: *"Set to [Slicer] / [Printer]. Saving to memory."*

### Step 4: Persist to Project Memory

Call `memory_user_edits` to save — this survives across sessions:

```
# If adding for the first time:
memory_user_edits add: "3D printing target slicer: [slicer name]"
memory_user_edits add: "3D printing target printer: [printer name]"

# If replacing an existing entry (use replace with the line number):
memory_user_edits replace [N]: "3D printing target slicer: [new slicer name]"
```

Also suggest updating `~/Projects/Claude.md` if the user confirms this is
a permanent preference (prevents asking again in future sessions).

### Step 5: Set Up the Venv

```bash
python3 scripts/venv_manager.py setup --skill 3mf \
    --packages lib3mf trimesh numpy
```

Creates (or reuses) `~/.local/share/claude-skills/3mf/.venv`.
All Python code in this skill runs inside this venv — never bare `pip install`.

---

## Virtual Environment

All Python operations in this skill use an isolated venv managed by
`scripts/venv_manager.py`. This keeps dependencies off the system Python.

```bash
# Setup (first use or after destroy)
python3 scripts/venv_manager.py setup --skill 3mf \
    --packages lib3mf trimesh numpy

# Run a script inside the venv
python3 scripts/venv_manager.py python --skill 3mf -- my_script.py

# Pass arguments to the script
python3 scripts/venv_manager.py python --skill 3mf -- convert.py input.stl output.3mf

# Check installed packages and venv status
python3 scripts/venv_manager.py info --skill 3mf

# Rebuild from scratch (broken packages)
python3 scripts/venv_manager.py destroy --skill 3mf
python3 scripts/venv_manager.py setup --skill 3mf --packages lib3mf trimesh numpy
```

**Python context manager:**
```python
from scripts.venv_manager import ManagedVenv

with ManagedVenv("3mf", packages=["lib3mf", "trimesh", "numpy"]) as vm:
    vm.run_python("process.py", ["--input", "model.stl"])
```

**Rule:** Never use `pip install --break-system-packages` or bare `pip install`.
Always use `venv_manager.py`.

---

## 3MF File Structure

```
model.3mf (ZIP)
├── [Content_Types].xml
├── _rels/.rels
└── 3D/
    ├── 3dmodel.model         ← geometry + metadata
    └── _rels/3dmodel.model.rels
```

Slicer-extended 3MFs add:
```
├── Metadata/
│   ├── Slic3r_PE.config          (PrusaSlicer / Orca)
│   ├── Slic3r_PE_model.config    (per-object settings)
│   └── model_settings.config     (Bambu / Orca)
└── Auxiliaries/                   (thumbnails, plate configs)
```

Quick inspection (no venv needed):
```bash
unzip -l model.3mf
unzip -p model.3mf 3D/3dmodel.model | head -100
```

---

## Common Workflows

All Python code below runs inside the venv via `venv_manager.py`.

### 1. STL → 3MF Conversion

```python
#!/usr/bin/env python3
"""
File:        stl_to_3mf.py
Author:      Colin Bitterfield
Email:       colin@bitterfield.com
Created:     <YYYY-MM-DD>  Updated: <YYYY-MM-DD>  Version: 1.0.0
Description: Convert STL to 3MF with metadata.
Target:      Slicer: <from memory>  Printer: <from memory>
Run via:     python3 scripts/venv_manager.py python --skill 3mf -- stl_to_3mf.py in.stl out.3mf
Dependencies (venv): lib3mf, trimesh
"""
import lib3mf, trimesh, sys
from datetime import date

def convert(input_stl, output_3mf, title="", author="Colin Bitterfield"):
    wrapper = lib3mf.Wrapper()
    model   = wrapper.CreateModel()
    stl     = trimesh.load(input_stl)
    obj     = model.AddMeshObject()
    obj.SetName(title or input_stl)
    for v in stl.vertices:
        obj.AddVertex(lib3mf.Position(v[0], v[1], v[2]))
    for f in stl.faces:
        obj.AddTriangle(lib3mf.Triangle(int(f[0]), int(f[1]), int(f[2])))
    model.AddBuildItem(obj, wrapper.GetIdentityTransform())
    meta = model.GetMetaDataGroup()
    meta.AddMetaData("", "Title",        title or input_stl, "xs:string", False)
    meta.AddMetaData("", "Author",       author,             "xs:string", False)
    meta.AddMetaData("", "CreationDate", str(date.today()),  "xs:string", False)
    model.QueryWriter("3mf").WriteToFile(output_3mf)
    print(f"Written: {output_3mf}")

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
```

### 2. Inspect a 3MF File

```python
import lib3mf
wrapper = lib3mf.Wrapper()
model   = wrapper.CreateModel()
reader  = model.QueryReader("3mf")
reader.SetStrictModeActive(False)
reader.ReadFromFile("model.3mf")

it = model.GetMeshObjects()
while it.MoveNext():
    obj = it.GetCurrentMeshObject()
    print(f"{obj.GetName()}: {obj.GetVertexCount()} verts, "
          f"{obj.GetTriangleCount()} tris, valid={obj.IsValid()}")

meta = model.GetMetaDataGroup()
for i in range(meta.GetMetaDataCount()):
    m = meta.GetMetaData(i)
    print(f"  {m.GetName()}: {m.GetValue()}")
```

### 3. Merge Multiple Parts onto One Build Plate

```python
import lib3mf, trimesh
wrapper = lib3mf.Wrapper()
model   = wrapper.CreateModel()

def add_stl(model, path, name, x=0, y=0):
    stl = trimesh.load(path)
    obj = model.AddMeshObject()
    obj.SetName(name)
    for v in stl.vertices:
        obj.AddVertex(lib3mf.Position(v[0], v[1], v[2]))
    for f in stl.faces:
        obj.AddTriangle(lib3mf.Triangle(int(f[0]), int(f[1]), int(f[2])))
    t = wrapper.GetIdentityTransform()
    t.m_Field[0][3] = x
    t.m_Field[1][3] = y
    model.AddBuildItem(obj, t)

add_stl(model, "lid.stl",  "Lid",  x=0)
add_stl(model, "base.stl", "Base", x=70)
add_stl(model, "clip.stl", "Clip", x=140)
model.QueryWriter("3mf").WriteToFile("build_plate.3mf")
```

### 4. Add/Update Metadata

```python
import lib3mf
from datetime import date
wrapper = lib3mf.Wrapper()
model   = wrapper.CreateModel()
model.QueryReader("3mf").ReadFromFile("model.3mf")

def set_meta(group, name, value):
    for i in range(group.GetMetaDataCount()):
        if group.GetMetaData(i).GetName() == name:
            group.GetMetaData(i).SetValue(value)
            return
    group.AddMetaData("", name, value, "xs:string", False)

meta = model.GetMetaDataGroup()
set_meta(meta, "Author",      "Colin Bitterfield")
set_meta(meta, "Title",       "Enclosure Lid v2")
set_meta(meta, "Description", "HYLAS-ELEC junction box lid")
set_meta(meta, "Date",        str(date.today()))
model.QueryWriter("3mf").WriteToFile("model.3mf")
```

### 5. Validate a 3MF File

```python
import lib3mf
wrapper = lib3mf.Wrapper()
model   = wrapper.CreateModel()
reader  = model.QueryReader("3mf")
reader.SetStrictModeActive(False)
reader.ReadFromFile("model.3mf")
for i in range(reader.GetWarningCount()):
    code, msg = reader.GetWarning(i)
    print(f"Warning {code}: {msg}")
it = model.GetMeshObjects()
while it.MoveNext():
    obj = it.GetCurrentMeshObject()
    print(f"{obj.GetName()}: {'✅ Valid' if obj.IsValid() else '❌ Invalid'}")
```

### 6. Extract Mesh to STL

```python
import lib3mf, trimesh, numpy as np
wrapper = lib3mf.Wrapper()
model   = wrapper.CreateModel()
model.QueryReader("3mf").ReadFromFile("model.3mf")
meshes = []
it = model.GetMeshObjects()
while it.MoveNext():
    obj   = it.GetCurrentMeshObject()
    verts = [[v.m_Coordinates[i] for i in range(3)] for v in obj.GetVertices()]
    tris  = [[t.m_Indices[i]     for i in range(3)] for t in obj.GetTriangles()]
    meshes.append(trimesh.Trimesh(vertices=np.array(verts), faces=np.array(tris)))
trimesh.util.concatenate(meshes).export("extracted.stl")
```

---

## Slicer / Printer — Target-Specific Behavior

> Active slicer and printer come from project memory (set in Startup Sequence).
> **Default: Orca Slicer / Elegoo CC1.**

### Orca Slicer + Elegoo CC1

Orca reads PrusaSlicer-format config files (`Slic3r_PE.config`).

```python
import zipfile

def inject_orca_settings(src: str, dst: str, settings: dict) -> None:
    config_bytes = "\n".join(f"{k} = {v}" for k, v in settings.items()).encode()
    with zipfile.ZipFile(src, "r") as zin, \
         zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename not in ("Metadata/Slic3r_PE.config",
                                     "Metadata/Slic3r_PE_model.config"):
                zout.writestr(item, zin.read(item.filename))
        zout.writestr("Metadata/Slic3r_PE.config", config_bytes)

# Elegoo CC1 baseline settings for Orca
CC1_DEFAULTS = {
    "layer_height":       "0.2",
    "first_layer_height": "0.3",
    "fill_density":       "15%",
    "fill_pattern":       "gyroid",
    "perimeters":         "3",
    "support_material":   "0",
    "brim_width":         "5",
}
inject_orca_settings("model.3mf", "model_orca.3mf", CC1_DEFAULTS)
```

**Elegoo CC1 build volume:** 220×220×250mm (safe zone: 200×200mm, centered)
```python
# Center a part on the CC1 build plate
t = wrapper.GetIdentityTransform()
t.m_Field[0][3] = 110.0   # X center
t.m_Field[1][3] = 110.0   # Y center
```

### PrusaSlicer

Same config format as Orca. See `references/slicer-extensions.md`.

### Bambu Studio

Different config format. See `references/slicer-extensions.md`.

---

## Raw XML Approach (No Venv Required)

```python
import zipfile, shutil, os
from xml.etree import ElementTree as ET

def inject_metadata(src, dst, metadata: dict):
    ET.register_namespace("", "http://schemas.microsoft.com/3dmanufacturing/core/2015/02")
    tmp = src + ".tmp.zip"
    shutil.copy(src, tmp)
    with zipfile.ZipFile(tmp, "r") as zin:
        xml_data = zin.read("3D/3dmodel.model")
    root = ET.fromstring(xml_data)
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    for name, value in metadata.items():
        el = root.find(f"m:metadata[@name='{name}']", ns)
        if el is not None:
            el.text = value
        else:
            e = ET.SubElement(root, "metadata", {"name": name})
            e.text = value
    new_xml = ET.tostring(root, encoding="unicode")
    with zipfile.ZipFile(tmp, "r") as zin, \
         zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = new_xml.encode("utf-8") if item.filename == "3D/3dmodel.model" \
                   else zin.read(item.filename)
            zout.writestr(item, data)
    os.remove(tmp)
```

---

## File Header Template

```python
#!/usr/bin/env python3
"""
File:        <script_name>.py
Author:      Colin Bitterfield
Email:       colin@bitterfield.com
Created:     <YYYY-MM-DD>  Updated: <YYYY-MM-DD>  Version: 1.0.0
Description: <What this script does>
Target:      Slicer: <from memory>  Printer: <from memory>
Run via:     python3 scripts/venv_manager.py python --skill 3mf -- <script_name>.py
Changelog:
    1.0.0 - Initial version
Dependencies (venv): lib3mf, trimesh, numpy
"""
```

---

## Best Practices Checklist

- [ ] Startup sequence completed — slicer/printer confirmed or set from memory
- [ ] Venv ready: `venv_manager.py setup --skill 3mf --packages lib3mf trimesh numpy`
- [ ] All Python runs via `venv_manager.py python` or `ManagedVenv` — never bare pip
- [ ] File header with author, version, target slicer/printer, run instructions
- [ ] `IsValid()` check on all mesh objects before writing
- [ ] Metadata: Title, Author, Description, CreationDate at minimum
- [ ] Build items positioned within printer's safe build area
- [ ] Orca settings injected when target slicer is Orca (default)
- [ ] STL fallback exported if legacy tools need it

---

## Reference Files

- `references/3mf-spec.md` — Core 3MF XML schema, winding order, namespaces
- `references/lib3mf-api.md` — lib3mf Python API quick reference, transforms
- `references/slicer-extensions.md` — Orca/PrusaSlicer/Bambu/CC1 config formats
- `scripts/venv_manager.py` — Venv setup, teardown, and run helper

See also the **openscad** skill for generating source geometry.
