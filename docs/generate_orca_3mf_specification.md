# generate_orca_3mf.py — Specification

**Author:** Colin Bitterfield
**Email:** colin@bitterfield.com
**Date Created:** 2026-02-17
**Date Updated:** 2026-02-17
**Version:** 1.0.0

---

## Purpose

Generates per-model OrcaSlicer-compatible 3MF files for all 41 Victron MPPT solar charge controller cooling mount configurations. Produces one 3MF per controller × fan size combination with proper multi-plate layout and embedded print settings.

---

## Inputs

| Input | Description |
|-------|-------------|
| `solar_controller_cooling_mount.scad` | OpenSCAD source (must be in same directory) |
| `CONTROLLERS` list (embedded) | 41 controller model definitions mirroring SCAD database |

---

## Outputs

Directory: `output_orca_3mf/`

| File Pattern | Example |
|---|---|
| `{Model_Name}_{fan_size}mm.3mf` | `SmartSolar_MPPT_100-30_50mm.3mf` |
| (40mm override variant) | `SmartSolar_MPPT_100-30_40mm.3mf` |

Models with a 40mm default fan (C1, C2 configs) receive only the default variant — the 40mm override would be identical geometry, so it is skipped.

**Expected output count:** ~76 files (41 default + 35 with 40mm override; 6 C1/C2 models have 40mm default so no override generated)

---

## 3MF File Structure

Each `.3mf` is a ZIP archive containing:

```
{model_name}_{fan_size}mm.3mf (ZIP)
├── [Content_Types].xml
├── _rels/
│   └── .rels
├── 3D/
│   └── 3dmodel.model          ← All 4 mesh objects (core 3MF spec)
└── Metadata/
    ├── model_settings.config  ← OrcaSlicer plate assignments
    └── project_settings.config ← PETG, 20% infill hints
```

---

## Plate Layout (3 Plates per 3MF)

| Plate | Contents | Rationale |
|-------|----------|-----------|
| 1 — Fan Mount | Front fan mount plate | Different footprint, prints alone |
| 2 — Rear Grill | Rear hexagonal ventilation grill | Different footprint, prints alone |
| 3 — Rails | Left rail + Right rail (side by side, 10mm gap) | Same profile, efficient to print together |

---

## Print Settings (Embedded)

| Setting | Value |
|---------|-------|
| Material | PETG |
| Sparse infill density | 20% |
| Layer height | 0.2mm |
| Wall loops | 4 |
| Top/bottom layers | 5 |
| Supports | None |

> **Note:** These settings are embedded as hints in `Metadata/project_settings.config`. OrcaSlicer may not automatically apply all values — verify your print profile before slicing. PETG is required for heat resistance near controllers operating up to 75°C.

---

## Fan Size Variants

| Variant | fan_size_override passed to OpenSCAD |
|---------|--------------------------------------|
| Default | `0` (SCAD uses database value) |
| 40mm override | `40` |

For C1/C2 controllers (75/10, 75/15, 100/15), the database fan size is already 40mm. The override would be identical geometry, so these models receive only one 3MF (default = 40mm).

---

## SCAD Parameters Invoked

```bash
openscad \
  -o {output.stl} \
  -D 'model_code="{MODEL_CODE}"' \
  -D 'component={1|2|3|4}' \
  -D 'fan_size_override={0|40}' \
  solar_controller_cooling_mount.scad
```

Components:
- `1` = Front fan mount
- `2` = Left rail
- `3` = Right rail
- `4` = Rear grill

---

## 3MF Object IDs

| Object ID | Component |
|-----------|-----------|
| 1 | Front fan mount |
| 2 | Left rail |
| 3 | Right rail |
| 4 | Rear grill |

---

## STL Parser

The script uses a pure-stdlib binary STL parser (no trimesh required):
- Reads binary STL format (80-byte header, uint32 triangle count, 12+36+2 bytes per triangle)
- Deduplicates vertices via a coordinate-keyed dict (rounded to 5 decimal places)
- Produces compact vertex/face arrays for efficient 3MF XML output
- Falls back to ASCII STL regex parser if binary detection fails

---

## Dependencies

| Dependency | Source | Notes |
|-----------|--------|-------|
| Python 3.8+ | System | stdlib only; no pip installs required |
| OpenSCAD | External | Installed at `/Applications/OpenSCAD.app` on macOS |

---

## Usage

```bash
# Run from fan_controllers project root
cd /path/to/fan_controllers
python3 generate_orca_3mf.py
```

Output appears in `./output_orca_3mf/`. Each file is ready to open in OrcaSlicer via **File → Import → Import 3MF**.

---

## File Naming Convention

Model names use hyphens for slashes (e.g., `100/30` → `100-30`) and underscores for spaces. Special characters are removed. This ensures valid filenames on all platforms.

Example mapping:

| SCAD Name | File Prefix |
|-----------|-------------|
| SmartSolar MPPT 150/85-Tr VE.Can | `SmartSolar_MPPT_150-85-Tr_VE_Can` |
| Orion-Tr Smart 12/12-30A | `Orion-Tr_Smart_12-12-30A` |

---

## Related Files

| File | Description |
|------|-------------|
| `solar_controller_cooling_mount.scad` | OpenSCAD source, v2.6.0 |
| `generate_all_stls.py` | Generates STL files only (deduplicated by config group) |
| `generate_complete_3mf.py` | Earlier 3MF generator (per config group, not per model) |
| `docs/fan_cooling_specification.md` | Hardware design specification |
