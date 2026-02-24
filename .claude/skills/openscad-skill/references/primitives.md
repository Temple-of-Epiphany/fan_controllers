# OpenSCAD Primitives Reference

## 3D Primitives

### cube
```scad
cube(size);                     // size = number (cube) or [x,y,z]
cube([10,20,5]);                // rectangular box
cube([10,20,5], center=true);  // centered at origin
```

### cylinder
```scad
// Always specify $fn!
cylinder(h=height, r=radius, $fn=32);
cylinder(h=10, d=20, $fn=32);               // diameter shorthand
cylinder(h=10, r1=5, r2=0, $fn=32);        // cone (tip up)
cylinder(h=10, r1=0, r2=5, $fn=32);        // cone (tip down)
cylinder(h=10, r1=8, r2=5, $fn=32);        // frustum (truncated cone)
cylinder(h=10, d1=10, d2=0, $fn=32);       // cone via diameter
```

### sphere
```scad
// Always specify $fn!
sphere(r=radius, $fn=32);
sphere(d=diameter, $fn=32);
```

### polyhedron
```scad
polyhedron(
    points=[[x,y,z], ...],
    faces=[[pt_idx, ...], ...],  // faces listed with points in CW order (viewed from outside)
    convexity=1                   // increase for non-convex shapes
);
```

---

## 2D Primitives

### circle
```scad
circle(r=5, $fn=32);
circle(d=10, $fn=32);
```

### square
```scad
square(10);                     // 10×10
square([15,8]);                 // 15×8
square([15,8], center=true);   // centered
```

### polygon
```scad
polygon(points=[[0,0],[10,0],[5,10]]);
polygon(points=[...], paths=[[0,1,2],[3,4,5]]);  // with holes (paths)
```

### text
```scad
text(
    "string",
    size=10,
    font="Liberation Sans",          // use font name from system
    halign="left",                   // left | center | right
    valign="baseline",               // top | center | baseline | bottom
    spacing=1,                       // letter spacing multiplier
    direction="ltr",                 // ltr | rtl | ttb | btt
    language="en",
    script="latin"
);
```

Common font strings:
- `"Liberation Sans"` — default, usually available
- `"Liberation Sans:style=Bold"`
- `"Liberation Mono"`
- `"DejaVu Sans"`

---

## Import

```scad
import("file.stl");             // import STL geometry
import("file.dxf");             // import 2D DXF (use inside linear_extrude)
import("file.svg");             // import 2D SVG
surface("heightmap.png");       // heightmap from image (grayscale)
surface("heightmap.png", center=true, invert=false);
```

---

## Special Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `$fn`    | Fragment count for circles/curves | 0 (auto) |
| `$fa`    | Minimum angle per fragment | 12° |
| `$fs`    | Minimum fragment size (mm) | 2mm |
| `$t`     | Animation time (0–1) | 0 |
| `$vpt`   | Viewport translation | [0,0,0] |
| `$vpd`   | Viewport distance | 140 |
| `$vpr`   | Viewport rotation | [55,0,25] |
| `$children` | Number of child objects in module | — |

**Resolution**: When `$fn > 0`, it overrides `$fa` and `$fs`. Recommended: always set `$fn` explicitly.

```scad
// Equivalent resolutions:
cylinder(h=10, r=5, $fn=32);    // 32 segments
cylinder(h=10, r=5, $fn=64);    // 64 segments (smoother)
```

For the smallest visible radius that still prints cleanly:
```
$fn = max(32, round(2 * PI * radius / $fs));
```
