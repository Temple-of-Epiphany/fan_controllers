# OpenSCAD Customizer Reference

The Customizer panel (View → Customizer) reads specially formatted variable declarations
and comments to auto-generate a GUI for adjusting model parameters without editing code.

## Enabling the Customizer

In OpenSCAD: View → Customizer (or press Ctrl+Shift+C on some versions).
The panel appears on the right. Changes update the preview in real time.

---

## Section Headers

Organizes parameters into collapsible groups:

```scad
/* [Section Name] */
var = value;

/* [Dimensions] */
width = 50;
height = 30;

/* [Options] */
add_lid = true;
```

Hidden section (variables not shown in GUI):
```scad
/* [Hidden] */
$fn = 32;
tol = 0.2;
_internal_offset = 3;  // leading underscore also hides from Customizer
```

---

## Widget Types

### Number input (plain)
```scad
// Wall thickness in mm
wall = 2;
```
→ Shows a text input box.

### Slider
Syntax: `// [min:max]` or `// [min:step:max]`

```scad
// Width of the part
width = 50;     // [10:200]

// Layer resolution
layer = 0.2;    // [0.1:0.05:0.4]
```

### Dropdown (numeric enum)
```scad
// Number of sides
sides = 6;      // [3,4,6,8,12]

// Quality preset
quality = 1;    // [1:Draft, 2:Standard, 3:Fine]
```

For labeled dropdowns, format is `[value:Label, value:Label]`.

### Checkbox (boolean)
```scad
// Include mounting holes
include_holes = true;

// Add lid
has_lid = false;
```
No annotation needed — booleans automatically become checkboxes.

### Text input
```scad
// Label text
label_text = "Sample";
```

---

## Complete Example

```scad
/*
 * Parametric Box with Lid
 */

/* [Box Dimensions] */
// Box outer width (mm)
box_w = 60;     // [20:200]

// Box outer depth (mm)
box_d = 40;     // [20:200]

// Box outer height (mm)
box_h = 25;     // [10:100]

// Wall thickness (mm)
wall = 2;       // [1:0.5:5]

/* [Lid] */
// Generate lid
include_lid = true;

// Lid height (mm)
lid_h = 8;      // [4:30]

// Lid lip depth (mm)
lid_lip = 3;    // [2:8]

/* [Holes] */
// Add mounting holes
add_holes = true;

// Hole type
hole_type = 0;  // [0:M3 (3.2mm), 1:M4 (4.2mm), 2:M5 (5.2mm)]

// Inset from corners (mm)
hole_inset = 6; // [4:20]

/* [Label] */
// Engrave label on lid
engrave_label = false;

// Label text
label_text = "BOX";

/* [Hidden] */
$fn = 32;
tol = 0.2;      // clearance tolerance

// Derived
hole_dia = [3.2, 4.2, 5.2][hole_type];

// --- Model ---
box_body(box_w, box_d, box_h, wall, add_holes, hole_dia, hole_inset);

if (include_lid) {
    translate([box_w + 10, 0, 0])
        box_lid(box_w, box_d, lid_h, lid_lip, wall,
                engrave_label, label_text);
}

module box_body(w, d, h, t, holes, hd, hi) {
    difference() {
        cube([w, d, h]);
        translate([t, t, t])
            cube([w-t*2, d-t*2, h]);  // hollow, open top
        if (holes) corner_holes(w, d, hi, hd, t);
    }
}

module box_lid(w, d, lh, lip, t, do_label, lbl) {
    difference() {
        union() {
            cube([w, d, t]);           // lid plate
            translate([t, t, t])       // inner lip
                cube([w-t*2, d-t*2, lip]);
        }
        if (do_label)
            translate([w/2, d/2, -0.01])
                label(lbl, sz=8, depth=t*0.6+0.01);
    }
}

module corner_holes(w, d, inset, dia, depth) {
    for (x=[inset, w-inset])
        for (y=[inset, d-inset])
            translate([x, y, -0.01])
                cylinder(h=depth+0.02, d=dia, $fn=32);
}

module label(txt, sz=8, depth=0.5) {
    linear_extrude(depth)
        text(txt, size=sz, font="Liberation Sans:style=Bold",
             halign="center", valign="center");
}
```

---

## Customizer from Command Line

When rendering from command line, override Customizer parameters with `-D`:

```bash
openscad -o box.stl box.scad -D 'box_w=80' -D 'box_d=60' -D 'add_holes=false'
```

Generate multiple variants:
```bash
for w in 40 60 80 100; do
    openscad -o "box_${w}mm.stl" box.scad -D "box_w=${w}"
done
```

---

## Tips

- Keep parameter names short but descriptive — they appear as labels in GUI.
- Inline comments become the widget label, so write them as readable descriptions.
- Use `/* [Hidden] */` for all internal constants and special variables.
- Group related parameters together — users work top-to-bottom in the panel.
- Provide sane defaults that produce a useful model on first render.
- `step` in sliders enables fine-grained control (e.g., `0.05` for layer heights).
