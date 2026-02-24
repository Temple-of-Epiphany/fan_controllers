# OpenSCAD Libraries Reference

## Standard Library (built-in)

OpenSCAD ships with a small standard library. Include with:
```scad
use <MCAD/nuts_and_bolts.scad>
include <MCAD/units.scad>
```

Common MCAD modules (may vary by OpenSCAD version):
- `MCAD/nuts_and_bolts.scad` — nut/bolt profiles
- `MCAD/gears.scad` — involute gear generator
- `MCAD/springs.scad` — spring coil generator
- `MCAD/shapes.scad` — torus, cone helpers
- `MCAD/units.scad` — metric/imperial constants

---

## BOSL2 (Recommended Third-Party Library)

**BOSL2** (Belfry OpenSCAD Library v2) is the most comprehensive OpenSCAD library.
Install: clone to `~/.local/share/OpenSCAD/libraries/BOSL2/`

GitHub: https://github.com/BelfrySCAD/BOSL2

### Key BOSL2 modules

```scad
include <BOSL2/std.scad>

// Attachable rounded box
cuboid([50,30,20], rounding=3, anchor=BOTTOM);

// Cylinder with attachments
cyl(h=20, d=10, rounding=1);

// Thread generation
include <BOSL2/threading.scad>
threaded_rod(d=8, l=30, pitch=1.25);     // M8 rod
threaded_nut(od=13, id=8, h=6, pitch=1.25);

// Gears
include <BOSL2/gears.scad>
spur_gear(mod=2, teeth=20, thickness=6);

// Paths and sweeps
include <BOSL2/paths.scad>
path = arc(r=30, angle=180);
path_sweep(circle(d=4, $fn=16), path);

// Text on surface
include <BOSL2/strings.scad>

// Knurling
include <BOSL2/knurling.scad>
knurled_cylinder(d=20, h=30, knurl_depth=1);
```

---

## NopSCADlib

For electronics enclosures and hardware:
GitHub: https://github.com/nophead/NopSCADlib

```scad
include <NopSCADlib/lib.scad>
// Provides: PCB mounts, fans, PSUs, connectors, screws, etc.
```

---

## Writing Library Files

Create reusable libraries as separate .scad files:

```scad
// mylib.scad
// Use 'use' to import functions/modules without rendering geometry
// Use 'include' to import and also execute any top-level geometry

module rounded_rect(w, h, r) {
    offset(r=r) offset(r=-r) square([w,h]);
}

function inches(n) = n * 25.4;
function mm_to_in(n) = n / 25.4;
```

In main file:
```scad
use <mylib.scad>
linear_extrude(5) rounded_rect(50, 30, 3);
```

---

## Hardware Standard Dimensions

Common reference values (add to `/* [Hidden] */` as needed):

```scad
// M-series screw clearance holes (drill fit)
m2_clear  = 2.2;
m3_clear  = 3.2;
m4_clear  = 4.2;
m5_clear  = 5.2;
m6_clear  = 6.3;

// M-series screw head diameters (socket cap)
m2_head   = 3.8;
m3_head   = 5.5;
m4_head   = 7.0;
m5_head   = 8.5;
m6_head   = 10.0;

// M-series socket cap head heights
m2_head_h = 2.0;
m3_head_h = 3.0;
m4_head_h = 4.0;
m5_head_h = 5.0;

// Heat-set insert OD (for M3 Voron-style)
m3_insert_od = 4.6;
m3_insert_h  = 4.0;

// Common brass insert ODs
m2_insert_od = 3.5;
m4_insert_od = 5.6;
```
