# OpenSCAD Export Reference

## All CLI Export Formats

Format is determined by the output file extension. Supported extensions:
`stl`, `3mf`, `amf` (deprecated), `off`, `wrl`, `csg`, `dxf`, `svg`,
`png`, `pdf`, `echo`, `ast`, `term`, `nef3`

```bash
# Basic export — format from extension
openscad -o model.stl  model.scad
openscad -o model.3mf  model.scad
openscad -o model.svg  model.scad   # 2D projection

# Explicit format override (useful when piping to stdout with -)
openscad -o model.stl --export-format binstl model.scad   # binary STL
openscad -o model.stl --export-format asciistl model.scad # ASCII STL

# Variable override
openscad -o model.stl -D 'width=80' -D 'wall=3' model.scad

# Multiple outputs in one pass
openscad -o model.stl -o model.3mf model.scad

# Force full CGAL render (not preview-mode)
openscad -o model.stl --render model.scad

# Suppress informational output
openscad -o model.stl -q model.scad
```

## STL: ASCII vs Binary

| | ASCII STL | Binary STL |
|---|---|---|
| CLI default | ✅ | ❌ |
| GUI default | ❌ | ✅ |
| File size | Larger (~5-10×) | Smaller |
| Human readable | ✅ | ❌ |
| Slicer compatible | ✅ | ✅ |
| Flag | `--export-format asciistl` | `--export-format binstl` |

Recommendation: always use `--export-format binstl` for production output.

## 3MF Export Settings (`-O` flags)

```bash
# Color mode: model (use object colors), none, selected-only
openscad -o model.3mf -O 'export-3mf/color-mode=none' model.scad

# Unit (default: millimeter)
openscad -o model.3mf -O 'export-3mf/unit=millimeter' model.scad

# Override default color (hex)
openscad -o model.3mf -O 'export-3mf/color=#1a73e8' model.scad

# Decimal precision (1–16, default 6)
openscad -o model.3mf -O 'export-3mf/decimal-precision=4' model.scad

# Add metadata (author, title from -O or model)
openscad -o model.3mf -O 'export-3mf/add-meta-data=true' model.scad
```

## Parameter JSON Files (Customizer sets)

Save named parameter sets for batch or CI rendering:

```json
{
  "fileFormatVersion": "1",
  "parameterSets": {
    "small": {
      "box_w": 40, "box_d": 30, "wall": 1.5
    },
    "standard": {
      "box_w": 60, "box_d": 40, "wall": 2
    },
    "large": {
      "box_w": 100, "box_d": 70, "wall": 3
    }
  }
}
```

```bash
# Render a specific named set
openscad -o standard.3mf -p params.json -P "standard" model.scad

# Render all sets
for set in small standard large; do
  openscad -o "${set}.3mf" -p params.json -P "${set}" model.scad
done
```

## Batch Rendering Script

```bash
#!/bin/bash
# render_variants.sh — parameter sweep, STL + 3MF per variant
MODEL="enclosure.scad"
WIDTHS=(40 60 80 100)

for w in "${WIDTHS[@]}"; do
  BASE="enclosure_${w}mm"
  echo "Rendering ${BASE}..."
  openscad -o "${BASE}.stl" --export-format binstl \
           -D "box_w=${w}" "${MODEL}" -q
  openscad -o "${BASE}.3mf" \
           -D "box_w=${w}" \
           -O 'export-3mf/color-mode=none' \
           "${MODEL}" -q
done
echo "Done."
```

## Makefile Integration

```makefile
SCAD    = enclosure.scad
TARGETS = enclosure.stl enclosure.3mf

all: $(TARGETS)

%.stl: $(SCAD)
	openscad -o $@ --export-format binstl $<

%.3mf: $(SCAD)
	openscad -o $@ -O 'export-3mf/color-mode=none' $<

clean:
	rm -f $(TARGETS)
```

## Image Rendering

```bash
# Default preview (F5-equivalent)
openscad -o preview.png model.scad \
  --imgsize=1920,1080 \
  --camera=0,0,0,55,0,25,200 \
  --colorscheme=Cornfield

# Full CGAL render
openscad -o render.png model.scad \
  --render \
  --imgsize=2560,1440

# Isometric view
openscad -o iso.png model.scad \
  --projection=ortho \
  --camera=1,1,1,0,0,0 \
  --imgsize=1920,1920

# Available colorschemes:
# Cornfield, Sunset, Metallic, Starnight, BeforeDawn,
# Nature, DeepOcean, Solarized, Tomorrow, Tomorrow Night, Monotone
```

## Version Compatibility

| Feature | Minimum version |
|---------|----------------|
| 3MF export | 2019.05 |
| SVG export | 2015.03 |
| AMF export | 2015.03 (deprecated, use 3MF) |
| PNG export | 2013.05 |
| PDF export | 2021.01 |
| Multiple `-o` flags | 2021+ |
| `-O` export settings | 2025+ |

Check your version: `openscad --version`

For 3MF export, OpenSCAD must be compiled with `lib3mf`. Some package manager
builds (especially FreeBSD, some Linux distros) may omit this dependency.
Verify: `openscad --info | grep lib3mf`
