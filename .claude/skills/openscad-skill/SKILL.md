---
name: openscad
description: >
  Design, generate, and modify parametric 3D models using OpenSCAD's scripting language.
  Use this skill whenever a user asks to create, edit, or generate .scad files, 3D printable
  parts, parametric models, enclosures, brackets, mounts, gears, connectors, or any solid
  geometry using code. Triggers on requests like "write an OpenSCAD model", "create a 3D
  printable X", "generate a parametric Y in OpenSCAD", "add a Customizer panel", "make a
  .scad file for", or when the user shares existing .scad code and wants it modified,
  debugged, or extended. Also use when the user wants to learn OpenSCAD syntax or asks
  how to accomplish something in OpenSCAD specifically.
---

# OpenSCAD Skill

OpenSCAD is a programmers' solid 3D CAD modeller — models are defined entirely in code,
making them inherently parametric and version-controllable. This skill covers best practices
for writing clean, customizable, print-ready OpenSCAD scripts.

## Core Philosophy

- **Always parametric**: Every dimension should be a named variable, never a magic number.
- **Always documented**: Include a file header and inline comments explaining intent.
- **Customizer-ready**: Use the Customizer parameter block pattern so models are adjustable
  via the OpenSCAD GUI without editing code.
- **Print-quality geometry**: Use `$fn=32` minimum for curved surfaces (cylinders, spheres,
  circles). Use higher values (`$fn=64` or `$fn=128`) for large visible curves or precision fits.

---

## macOS Binary Discovery (macOS 26.x)

**Before running any OpenSCAD CLI command, the binary must be located.**
Always run discovery first — do not hard-code paths.

### Discovery Priority

Claude follows this order when locating the OpenSCAD binary:

1. **Cached path** — `~/.config/openscad_skill/config.json` (set on first find)
2. **`OPENSCAD_BIN` env var** — set by user for custom installs
3. **`PATH`** — works if installed via Homebrew or MacPorts to a bin directory
4. **Spotlight (`mdfind`)** — finds all `.app` bundles by bundle ID
5. **Known fixed paths** — checked in order (see table below)
6. **Glob scan** — `/Applications/OpenSCAD*.app` for snapshot/dated builds

### macOS Install Locations by Method

| Install method | Binary path |
|---|---|
| DMG (stable) — .app bundle | `/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD` |
| DMG (stable) — plain folder | `/Applications/OpenSCAD/Contents/MacOS/OpenSCAD` |
| DMG (snapshot) — .app bundle | `/Applications/OpenSCAD-snapshot.app/Contents/MacOS/OpenSCAD` |
| DMG (snapshot) — plain folder | `/Applications/OpenSCAD-snapshot/OpenSCAD` |
| Homebrew (Apple Silicon) | `/opt/homebrew/bin/openscad` |
| Homebrew (Intel) | `/usr/local/bin/openscad` |
| Homebrew cask (Apple Silicon) | `/opt/homebrew/Caskroom/openscad/current/OpenSCAD.app/Contents/MacOS/OpenSCAD` |
| MacPorts | `/opt/local/bin/openscad` |

### Using the Discovery Script

```bash
# Discover and print the binary path (caches result)
python3 scripts/find_openscad.py

# Verify it runs and show version
python3 scripts/find_openscad.py --verify

# JSON output (for programmatic use)
python3 scripts/find_openscad.py --json

# Manually cache a custom path
python3 scripts/find_openscad.py --set /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD

# Clear cached path (force re-discovery next run)
python3 scripts/find_openscad.py --clear
```

### Using the Runner (Python scripts)

```python
from scripts.openscad_runner import OpenSCADRunner

# Auto-discovers binary on first use, caches it
runner = OpenSCADRunner()
print(runner.version())   # confirm binary found

# Render to binary STL
runner.render("model.scad", "output/model.stl")

# Render to 3MF with variable override
runner.render("model.scad", "output/model.3mf",
              variables={"box_w": 80, "wall": 2.5})

# Batch render variants
runner.render_batch("model.scad", output_dir="output", fmt="3mf", variants=[
    {"name": "small",  "variables": {"box_w": 40}},
    {"name": "medium", "variables": {"box_w": 60}},
    {"name": "large",  "variables": {"box_w": 100}},
], verbose=True)
```

### Virtual Environment

The runner itself has no pip dependencies and runs on the system Python directly.
The venv is only needed for scripts using `lib3mf` or `trimesh` (3MF post-processing).

For any script in this skill that does require packages:
```bash
# Setup (creates ~/.local/share/claude-skills/openscad/.venv)
python3 scripts/venv_manager.py setup --skill openscad --packages trimesh numpy

# Run a script inside the venv
python3 scripts/venv_manager.py python --skill openscad -- my_script.py

# Context manager form
# from scripts.venv_manager import ManagedVenv
# with ManagedVenv("openscad", packages=["trimesh"]) as vm:
#     vm.run_python("process_mesh.py")

# Rebuild if broken
python3 scripts/venv_manager.py destroy --skill openscad
python3 scripts/venv_manager.py setup --skill openscad --packages trimesh numpy
```

### If Binary is Not Found

If discovery fails, Claude should:
1. Tell the user OpenSCAD was not found on their system.
2. Ask: *"Is OpenSCAD installed? If so, where is it located?"*
3. Offer installation options:
   ```
   Option A — DMG:       https://openscad.org/downloads.html
   Option B — Homebrew:  brew install --cask openscad
   Option C — MacPorts:  sudo port install openscad
   Option D — Snapshot:  brew install --cask openscad@snapshot
   ```
4. Once the user confirms the path, cache it:
   ```bash
   python3 scripts/find_openscad.py --set "<path they provided>"
   ```

---

## File Header Template

Every generated .scad file must start with this header block:

```scad
/*
 * File:        <filename>.scad
 * Author:      Colin Bitterfield
 * Email:       colin@bitterfield.com
 * Created:     <YYYY-MM-DD>
 * Updated:     <YYYY-MM-DD>
 * Version:     1.1.0
 *
 * Description: <What this model is and what it does>
 *
 * Changelog:
 *   1.1.0 - Added STL/3MF export section and parameter JSON workflow
 *   1.0.0 - Initial version
 *
 * Print Notes:
 *   - Layer height: 0.2mm recommended
 *   - Infill: <suggest appropriate %>
 *   - Supports: <Yes/No, where>
 *   - Material: <PLA/PETG/ASA recommendation>
 */
```

---

## Customizer Panel Pattern

OpenSCAD's Customizer reads specially formatted comments to create a GUI panel.
**Always include a Customizer block** so users can adjust parameters without editing code.

```scad
/* [Basic Dimensions] */
// Overall width in mm
width = 50;     // [10:200]

// Overall height in mm
height = 30;    // [5:150]

// Wall thickness in mm
wall = 2;       // [1:0.5:5]

/* [Mounting Holes] */
// Include mounting holes
include_holes = true;

// Hole diameter in mm
hole_dia = 3.2;  // [2:0.1:6]

// Number of holes
num_holes = 4;   // [2,4,6,8]

/* [Hidden] */
// Internal constants (hidden from Customizer)
$fn = 32;
tol = 0.2;  // print tolerance/clearance
```

**Customizer syntax rules:**
- Section headers: `/* [Section Name] */`
- Hidden parameters: `/* [Hidden] */`
- Slider: `value = default;  // [min:max]`
- Slider with step: `value = default;  // [min:step:max]`
- Dropdown: `value = default;  // [opt1, opt2, opt3]`
- Labeled dropdown: `value = 0;  // [0:Label A, 1:Label B]`
- Boolean checkbox: use `true` or `false` as default, no annotation needed
- Inline comment = label shown in GUI

---

## Resolution and Curve Quality

```scad
// GLOBAL setting at top of file (hidden from Customizer):
/* [Hidden] */
$fn = 32;   // Minimum for any production model

// Or override per-object for precision-critical features:
cylinder(h=10, r=5, $fn=64);    // smoother large cylinder
sphere(r=3, $fn=48);             // smoother sphere

// Common $fn guidelines:
//   $fn=32   → general use, good balance of quality/render speed
//   $fn=64   → visible exterior curves, larger diameters
//   $fn=128  → very large or precision-fit parts (slow to render)
//   $fn=16   → internal/hidden geometry only, drafts
```

**Never omit `$fn`** — the default (very low) produces faceted, unprintable cylinders.

---

## 3D Primitives

```scad
// Box
cube([width, depth, height]);
cube([10, 20, 5], center=true);

// Cylinder (always specify $fn)
cylinder(h=10, r=5, $fn=32);
cylinder(h=10, d=10, $fn=32);            // diameter form
cylinder(h=10, r1=5, r2=3, $fn=32);     // tapered (cone)

// Sphere
sphere(r=5, $fn=32);
sphere(d=10, $fn=32);

// Polyhedron (advanced custom geometry)
polyhedron(points=[...], faces=[...]);
```

## 2D Primitives (for extrusion)

```scad
circle(r=5, $fn=32);
circle(d=10, $fn=32);
square([10, 20]);
square([10, 20], center=true);
polygon(points=[[0,0],[10,0],[5,10]]);
text("Hello", size=8, font="Liberation Sans");
```

---

## Boolean Operations (CSG)

```scad
// Union — combine shapes
union() {
    cube([10,10,5]);
    cylinder(h=8, r=3, $fn=32);
}

// Difference — subtract second+ from first
difference() {
    cube([10,10,5]);
    cylinder(h=6, r=2, $fn=32);  // hole
}

// Intersection — keep only overlapping volume
intersection() {
    cube([10,10,10], center=true);
    sphere(r=6, $fn=32);
}
```

**Tip**: Extend drill/subtract cylinders ±0.01mm to avoid z-fighting:
```scad
difference() {
    cube([20,20,10]);
    translate([10,10,-0.01])
        cylinder(h=10.02, d=4, $fn=32);  // guaranteed through-hole
}
```

---

## Transformations

```scad
translate([x, y, z]) { ... }
rotate([x_deg, y_deg, z_deg]) { ... }
scale([x, y, z]) { ... }
mirror([1,0,0]) { ... }   // mirror across YZ plane
resize([new_x, new_y, new_z]) { ... }

// Align to top of object:
translate([0, 0, height/2]) sphere(r=3, $fn=32);

// Linear pattern
for (i = [0:3]) {
    translate([i*15, 0, 0]) cylinder(h=5, r=3, $fn=32);
}

// Circular pattern
for (a = [0:90:359]) {
    rotate([0,0,a]) translate([20,0,0]) cylinder(h=5, r=2, $fn=32);
}
```

---

## Modules (reusable components)

```scad
// Define a reusable module
module rounded_box(w, d, h, r=2) {
    hull() {
        for (x = [r, w-r]) {
            for (y = [r, d-r]) {
                translate([x, y, 0])
                    cylinder(h=h, r=r, $fn=32);
            }
        }
    }
}

// Call the module
rounded_box(50, 30, 10, r=3);

// Module with children (like a container)
module hollow_box(w, d, h, wall=2) {
    difference() {
        cube([w, d, h]);
        translate([wall, wall, wall])
            cube([w-wall*2, d-wall*2, h]);  // open top
    }
}
```

---

## Common Functional Patterns

### Mounting Hole Pattern (4-corner)
```scad
module corner_holes(w, d, inset, dia, depth) {
    for (x = [inset, w-inset]) {
        for (y = [inset, d-inset]) {
            translate([x, y, -0.01])
                cylinder(h=depth+0.02, d=dia, $fn=32);
        }
    }
}
```

### Counterbore / Countersink
```scad
module counterbore(shaft_d, head_d, head_depth, total_depth) {
    union() {
        cylinder(h=total_depth+0.02, d=shaft_d, $fn=32);
        cylinder(h=head_depth, d=head_d, $fn=32);
    }
}
```

### Snap Fit / Living Hinge
```scad
module snap_hook(length=10, width=4, thickness=1.2, overhang=0.8) {
    union() {
        cube([width, length, thickness]);
        translate([0, length, 0])
            rotate([0,0,0])
            linear_extrude(thickness)
                polygon([[0,0],[width,0],[width/2, overhang]]);
    }
}
```

### Text Label
```scad
module label(txt, sz=5, depth=0.4) {
    linear_extrude(depth)
        text(txt, size=sz, font="Liberation Sans:style=Bold",
             halign="center", valign="center");
}
```

---

## Extrusion

```scad
// Linear extrude 2D profile to 3D
linear_extrude(height=10) {
    circle(r=5, $fn=32);
}

// With twist and scale
linear_extrude(height=20, twist=90, scale=0.5, $fn=32) {
    square([10,10], center=true);
}

// Rotate extrude (lathe operation)
rotate_extrude($fn=64) {
    translate([10,0,0])
        circle(r=3, $fn=32);  // torus
}

// Rotate extrude partial (angle param, OpenSCAD 2019+)
rotate_extrude(angle=270, $fn=64) {
    translate([15,0,0]) square([4,2]);
}
```

---

## Variables and Functions

```scad
// Constants
PI = 3.14159265;

// Derived values
inner_r = outer_r - wall;
diagonal = sqrt(pow(width,2) + pow(depth,2));

// User-defined functions
function lerp(a, b, t) = a + (b-a)*t;
function clamp(v, lo, hi) = max(lo, min(hi, v));
function deg2rad(d) = d * PI / 180;

// Conditional expression
wall = (thick_walls) ? 3 : 1.5;
```

---

## Tolerance and Print Fit Guidelines

```scad
/* [Hidden] */
// Print tolerances (adjust for your printer)
tol    = 0.2;   // general clearance between mating parts
press  = 0.0;   // press fit (0 or slightly negative)
slide  = 0.3;   // sliding fit
loose  = 0.5;   // loose/rattle fit

// Usage: shaft fits into hole
shaft_d = 8;
hole_d  = shaft_d + slide*2;  // sliding fit

cylinder(h=20, d=hole_d, $fn=32);
```

---

## File Output and Rendering

### GUI Workflow
- **Preview** (`F5`): Fast CSG tree preview. Use for iteration.
- **Render** (`F6`): Full CGAL render — required before any export.
- **Export**: File → Export → Export as STL / 3MF / DXF / SVG / PNG / PDF.
- AMF is **deprecated** — always prefer 3MF over AMF for new work.

### Key CLI Commands

> **Always discover the binary first** — see the macOS Binary Discovery section above.
> Use `scripts/openscad_runner.py` for Python-driven rendering (handles discovery automatically).

```bash
# Direct CLI (after discovering binary path)
OPENSCAD=$(python3 scripts/find_openscad.py)

# Binary STL (recommended for production)
"$OPENSCAD" -o model.stl --export-format binstl model.scad

# 3MF (requires OpenSCAD built with lib3mf, 2019.05+)
"$OPENSCAD" -o model.3mf model.scad

# Override Customizer variables at export time
"$OPENSCAD" -o model.stl -D 'width=80' -D 'wall=3' model.scad

# Multiple formats in one pass
"$OPENSCAD" -o model.stl -o model.3mf model.scad

# Use a named Customizer parameter set from JSON
"$OPENSCAD" -o model.3mf -p params.json -P "standard" model.scad

# 3MF with no embedded color (portable, slicer-neutral)
"$OPENSCAD" -o model.3mf -O 'export-3mf/color-mode=none' model.scad
```

### STL vs 3MF

| | STL | 3MF |
|---|---|---|
| Color/material | ❌ | ✅ |
| Metadata | ❌ | ✅ |
| Multi-body grouping | ❌ | ✅ |
| Universal slicer support | ✅ | ✅ (modern) |
| File size | Larger (ASCII) | Smaller |

**Recommendation**: Export 3MF as primary for modern slicers (PrusaSlicer, Bambu,
Orca, Cura 5+). Provide binary STL as fallback for legacy tools.

> **Full export reference** — batch scripts, Makefile integration, parameter JSON
> format, image rendering, and version compatibility:
> see `references/export.md`

> **Post-processing 3MF** — metadata injection, merging, color, slicer configs:
> see the **3mf** skill.

---

## Best Practices Checklist

Before delivering any .scad file or running any render, verify:

- [ ] OpenSCAD binary located via `find_openscad.py` — do not assume it's in PATH
- [ ] File header with author, version, changelog, print notes

- [ ] File header with author, version, changelog, print notes
- [ ] All dimensions are named variables (no magic numbers)
- [ ] Customizer block with section headers and annotations
- [ ] `$fn=32` (or higher) set globally in `/* [Hidden] */` block
- [ ] Through-holes extend ±0.01 to avoid z-fighting artifacts
- [ ] Modules used for any repeated geometry
- [ ] Meaningful comments on non-obvious geometry decisions
- [ ] Tolerance variable defined for any press/fit/clearance features
- [ ] Model is centered or positioned sensibly on the build plate (Z=0 base)
- [ ] Export as 3MF (preferred) and/or binary STL; never AMF

---

## Reference Files and Scripts

**Scripts** (ready to run, handle binary discovery):
- `scripts/find_openscad.py` — Discover, cache, and verify the OpenSCAD binary on macOS
- `scripts/openscad_runner.py` — Python wrapper for CLI rendering with auto-discovery

**References:**
- `references/primitives.md` — Full primitive syntax and special variables
- `references/customizer.md` — Complete Customizer annotation syntax with full example
- `references/libraries.md` — BOSL2, NopSCADlib, MCAD, and hardware constants
- `references/export.md` — CLI export flags, batch scripts, Makefile, image rendering

See also the **3mf** skill for post-processing, enriching, and programmatically
building 3MF files after OpenSCAD export.
