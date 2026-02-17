# CLAUDE.md - Solar Charge Controller Cooling Mount Project

**Author:** Colin Bitterfield  
**Email:** colin@bitterfield.com  
**Date Created:** 2025-08-24  
**Date Updated:** 2025-08-26  
**Version:** 0.3.0

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project creates 3D printable parametric cooling mounts for Victron solar charge controllers using OpenSCAD. The system generates 4-piece assemblies that provide active cooling for controllers with external heatsinks.

## Current Project Status: CONTROLLER_COOLING_MOUNT (COMPLETE)

The cooling mount system is **complete and functional** with the following components:

### 4-Piece Assembly System
1. **Front Fan Mount Plate** - 6mm thick with recessed nut wells (5.3mm × 3mm deep)
2. **Left Side Rail** - 18mm wide, height calculated as (fan_size + 4) - heatsink_height  
3. **Right Side Rail** - Mirror of left rail
4. **Rear Grill Plate** - 6mm thick with dense honeycomb ventilation (10mm hexagons, 2mm spacing)

### Technical Specifications

**Fan Configurations (Optimized for 50mm fans where possible):**
- A1 Config: 3×50mm fans (MPPT 100/30-50, 150/35-45) - 8 models
- A3 Config: 2×50mm fans (MPPT 100/20 variants) - 4 models  
- B1/B2/B3 Config: 4×50mm fans (Large controllers 150/85+, 250 series) - 13 models
- C1/C2 Config: 2×40mm fans (Housing-based 75/10-15, 100/15) - 6 models

**Mounting System:**
- Rails connect to controller flanges via U-shaped cutouts (A1) or round holes (others)
- Plates connect to rails via M4 holes positioned at 1/4 and 3/4 of rail height
- All screw holes use M4×25mm screws with 5.3mm recessed nut wells

**Key Measurements (MPPT 100/30 example):**
- Total width: 187mm (spans controller + heatsinks + flanges)
- Plate dimensions: 187×54×6mm (fan_size + 4mm height)
- Rail dimensions: 18×122×31mm (calculated: (50+4)-23 = 31mm height)
- U-hole positions: 25mm and 96.5mm from rail front (71.5mm spacing)

## Architecture & Files

### Primary OpenSCAD File
- `solar_controller_cooling_mount.scad` - Complete parametric system
  - 31 controller models in database with measured dimensions
  - 4 component modules: front_fan_mount(), left_rail(), right_rail(), rear_grill()
  - Usage: Set `model_code` and `component` variables (1-4)

### Database Structure
**Controller Database Fields:**
```
[model_code, name, total_width, length, heatsink_height, fan_area_width, fan_count, fan_type, flange_config, hole_shape]
```

**Flange Configurations:**
- A1: Sideways U holes, 18mm rail width
- A3: Circle holes, 18mm rail width  
- B1/B2/B3: Keyhole + rounded slot, 23.3mm rail width
- C1/C2: Circle holes, 0mm rail (housing-based)

### Key Calculation Formulas
```
plate_width = total_width (spans full controller)
plate_length = fan_size + 4mm  
plate_thickness = 6mm
rail_height = (fan_size + 4) - heatsink_height
rail_length = controller_length (exact match)
mounting_hole_positions = rail_height × 0.25 and rail_height × 0.75
```

### Documentation Files
- `docs/heatsink_measurements.md` - Complete STEP file analysis (15 files measured)
- `docs/fan_configuration_analysis.md` - Optimal fan sizing for each config
- `docs/fan_cooling_specification.md` - Technical specification document
- `docs/scad_data.csv` - Controller lookup table
- `docs/flange_data.csv` - Mounting hole specifications

### Measured STEP File Data
**15 unique STEP files analyzed with 4 measurements each:**
- Fan Width, Total Width, Length, Height
- 7 distinct physical dimensions identified (many models share dimensions)
- All measurements corrected from initial PDF misunderstandings

## Critical Design Knowledge

### Heatsink Geometry
- Shape: Reverse L (---|_) with vertical fins and horizontal mounting flanges
- Flanges positioned **OUTSIDE** the rails (corrected from initial assumptions)
- Each side has **2 screw holes** (not 4 as initially drawn)
- Heatsink heights reduced by 3.5mm to account for case thickness

### Coordinate System
- **Up/Down = Length** (Y-axis in OpenSCAD)
- **Left/Right = Width** (X-axis in OpenSCAD)  
- **Back/Forth = Height** (Z-axis in OpenSCAD)
- **Assembly orientation:** Fan side = top, Grill side = bottom

### Mounting Hardware
- M4 screws for 50mm fans (40×40mm spacing)
- M3 screws for 40mm fans (30×30mm spacing)  
- Available lengths: 12,16,20,25,30,35mm
- 50mm fans have recessed nut wells, 40mm fans don't

## Development Workflow

### Component Generation
```
1. Set model_code = "SCC020030200" (or any valid model)
2. Set component = 1 (front_fan) / 2 (left_rail) / 3 (right_rail) / 4 (rear_grill)  
3. Render and export STL for 3D printing
```

### Design Validation
- All mounting holes automatically align between components
- Rail height calculation ensures proper fan clearance above heatsinks
- Honeycomb pattern avoids rail mounting areas
- Fan spacing optimized for available area

## File Management Standards
- Version numbering: 0.1.0 format
- Author block: Colin Bitterfield, colin@bitterfield.com
- Specifications in ./docs for all scripts
- Backup versions to ./backups with timestamps
- No filename changes - version in content only

## Next Project: CONTROLLER_BOX

The cooling mount project is complete. Next project will create controller box components based on circuit board images in `source_drawings/41IFRU4PYSL._AC_US100_.jpg` and `415i9emxreL._AC_US100_.jpg`.

---

**Status:** Controller cooling mount system complete and tested. Ready for production use across all 31 Victron solar charge controller models.