# Heatsink Dimensional Analysis for Solar Charge Controllers

**Author:** Colin Bitterfield  
**Email:** colin@bitterfield.com  
**Date Created:** 2025-08-24  
**Date Updated:** 2025-08-25  
**Version:** 0.2.0

## Overview

This document provides detailed heatsink measurements extracted from the 13 STEP files containing heatsink components. These dimensions are critical for clearance calculations in the cooling mount design.

## Measurement Methodology

**Coordinate System (CORRECTED):**
- **Up/Down = Length** (vertical dimension when mounted)
- **Left/Right = Width** (horizontal dimension across controller)
- **Back/Forth = Height** (depth/thickness dimension, protrusion from base)

**Note:** Initial PDF analysis extracted overall controller dimensions, not actual heatsink geometry. STEP file analysis reveals heatsink fins protrude only ~36-44mm above base with L-shaped mounting flanges.

## Corrected Heatsink Analysis Table

**IMPORTANT:** Previous measurements incorrectly listed overall controller dimensions as "heatsink height". Actual heatsink protrusion is ~36mm above base.

| Model Group | Controller Length×Width (mm) | Heatsink Height (back/forth mm) | Flange Foot Width (mm) | Config | Mounting Pattern | PDF Reference |
|-------------|------------------------------|--------------------------------|----------------------|--------|------------------|---------------|
| **Housing-Based (No External Heatsinks)** |
| MPPT 75/10-15 | 99.7×112.9 | 0 (housing) | 0 (housing) | C1 | Housing mount | BlueSolar-&-SmartSolar-MPPT-75-10-&-75-15.pdf |
| MPPT 100/15 | 100.7×113.9 | 0 (housing) | 0 (housing) | C2 | Housing mount | BlueSolar-&-Smartsolar-MPPT-100-15.pdf |
| MPPT 100/20 | 91.7×131 | **23.3** | **23.3** | A3 | 4×M4 flanges | BlueSolar-SmartSolar-MPPT-100V20A-(Dimensions).pdf |
| **Medium Controllers with Heatsinks** |
| MPPT 100/30-50 | 122×157 fan area | 26.5 | **18** | A1 | Sideways U holes | Total width: 187mm |
| MPPT 150/35-45 | 122×157 fan area | 26.5 | **18** | A1 | Sideways U holes | Total width: 187mm |
| **Large Controllers with Heatsinks** |
| MPPT 150/85-100 | 204×295 | ~36-44 | **23.3** | B1 | Multiple M4 | SmartSolar-MPPT-150-250-85-100-Tr-(dimensions).pdf |
| MPPT 250/85-100 | 204×295 | ~36-44 | **23.3** | B1 | Multiple M4 | SmartSolar-MPPT-150-250-85-100-Tr-(dimensions).pdf |
| MPPT X-Large VE.Can | **203.5**×294.6 | ~36-44 | **23.3** | B2 | Multiple M4 | DimensionDrawing-SS-MPPT-Tr-VE.Can-(XL).pdf |
| MPPT 250/60-70 | 170.7×248.5 | ~36-44 | **23.3** | B3 | Multiple M4 | SmartSolar-MPPT-250V-60-70-Tr.pdf |
| DimensionDrawing-BlueSolar-150_60-MC4 | TBD | TBD | TBD | TBD | TBD | Large controller series |
| DimensionDrawing-BlueSolar-150_60-Tr | TBD | TBD | TBD | TBD | TBD | Large controller series |
| DimensionDrawing-SS-MPPT-150-250-70-MC4-L | 295 | 273 | 268 | Multiple holes (R4, R8) | TBD | Large format, maximum heatsink height ~268mm |
| DimensionDrawing-SS-MPPT-150-250-70-Tr-L | 295 | 273 | 268 | Multiple holes (R4, R8) | TBD | Large format, maximum heatsink height ~268mm |
| DimensionDrawing-SS-MPPT-Tr-XL | 294.6 | 268.6 | 213.9 | Multiple holes (R4, R8) | TBD | Large format, heatsink height ~213.9mm |
| DimensionDrawing-SmartSolar-150_60A-Tr | TBD | TBD | TBD | TBD | TBD | Large controller series |
| DimensionDrawing-SmartSolar-150_60A-MC4 | TBD | TBD | TBD | TBD | TBD | Large controller series |
| SS-MPPT-250-60-70-MC4 | 248.5 | 226.5 | 182.2 | Multiple holes (R3, R6) | TBD | Medium-large format, heatsink height ~182.2mm |
| SmartSolar-MPPT-150-250-85-100-MC4 | 295 | 273 | 268 | Multiple holes (R4, R8) | TBD | Large format, maximum heatsink height ~268mm |
| SmartSolar-MPPT-250V-60-70-Tr | 248.5 | 226.5 | 182.2 | Multiple holes (R3, R6) | TBD | Medium-large format, heatsink height ~182.2mm |

## PDF Dimensional Analysis Results

### Successfully Extracted Dimensions

The following dimensional data has been extracted from PDF technical drawings using pdftotext:

**Compact Models (75V-100V, Lower Current):**
- **MPPT 75/10-15:** 99.7 x 84.1 x 112.9mm - Smallest footprint
- **MPPT 100/15:** 100.7 x 84.1 x 113.9mm - Housing-based heat dissipation
- **MPPT 100/20:** 131 x 118.6 x 98.6mm - Mid-size housing design

**Medium Models (100V, Higher Current):**
- **MPPT 100/30:** 186 x 176 x 131mm - Dedicated heatsink, R4 mounting
- **MPPT 100/50 & 150/35-45:** 186 x 176 x 132mm - Similar heatsink design, R4 mounting

**Large Models (150V-250V, High Current):**
- **MPPT 150/85-100 & 250/85-100:** 295 x 273 x 268mm - Largest heatsinks, R4/R8 mounting
- **MPPT 250/60-70:** 248.5 x 226.5 x 182.2mm - Medium-large format, R3/R6 mounting
- **MPPT XL Series:** 294.6 x 268.6 x 213.9mm - Industrial format, R4/R8 mounting

### CRITICAL DISCOVERY - Complete Analysis Results:

### CRITICAL DISCOVERY - Actual Measured Dimensions!

**MEASURED VALUES FROM STEP FILES:**

**#1: BS-SS-MPPT-100-30-(stp).STEP** ✅
- Fan Width: 157mm | Total Width: 187mm | Length: 122mm | Height: 26.5mm

**#2: BS-SS-MPPT-100-50-150-35-150-45-(step).STEP** ✅  
- Fan Width: 157mm | Total Width: 186mm | Length: 121.5mm | Height: 26.5mm

**#3: Blue-Smart-Solar-charge-controller-MPPT-75V-10A-15A-3D.STEP** ✅
- Fan Width: 81.923mm | Total Width: 121.8mm | Length: 98.87mm | Height: 0 (housing-based)
- **Note:** C1 Config - Circle holes in corners, no external heatsink

**#4: BlueSolar-&-Smartsolar-MPPT-100-15-(stp).STEP** ✅
- Fan Width: 86.399mm | Total Width: 113.807mm | Length: 99.932mm | Height: 0 (housing-based)
- **Note:** C2 Config - Circle holes in corners, no external heatsink

**#5: BlueSolar-SmartSolar-MPPT-100V20A--(3D).STEP** ✅
- Fan Width: 106mm | Total Width: 128mm | Length: 97.70mm | Height: 26.5mm
- **Note:** A3 Config - Small controller with external heatsink

**#6: DimensionDrawing-BlueSolar-150_60-&-150_70-MC4-3D.STEP** ✅
- Fan Width: 210mm | Total Width: 250mm | Length: 171mm | Height: 36mm
- **Note:** Large controller with external heatsinks - taller than A1/A3

**#7: DimensionDrawing-BlueSolar-150_60-&-150_70-Tr-3D.STEP** ✅
- Fan Width: 210mm | Total Width: 250mm | Length: 171mm | Height: 36mm
- **Note:** Identical to #6 - Same physical design, different connectors (MC4 vs Tr)

**#8: DimensionDrawing-SS-MPPT-150-250-70-MC4-VE.CAN-(L)-3D.STEP** ✅
- Fan Width: 208.50mm | Total Width: 244.5mm | Length: 170.70mm | Height: 38mm
- **Note:** VE.Can model - Slightly narrower than #6/#7, tallest heatsink yet

**#9: DimensionDrawing-SS-MPPT-150-250-70-Tr-VE.Can-(L)-3D.STEP** ✅
- Fan Width: 210mm | Total Width: 250mm | Length: 171mm | Height: 36mm
- **Note:** Identical to #6/#7 - Same physical design as BlueSolar-150_60/70 series (Tr connector variant)

**#10: DimensionDrawing-SS-MPPT-Tr-VE.Can-(XL)-3D.STEP** ✅
- Fan Width: 242.60mm | Total Width: 290.60mm | Length: 204.10mm | Height: 38.10mm
- **Note:** XL series B2 config - Large format controller, close to CSV estimate (294.6×203.5mm)

**#11: DimensionDrawing-SmartSolar-150_60A-&-150_70-Tr-3D.STEP** ✅
- Fan Width: 210.00mm | Total Width: 250.00mm | Length: 171.00mm | Height: 36.00mm
- **Note:** Identical to #6/#7/#9 - Same 250×171×36mm dimensions (SmartSolar variant of 150_60/70 series)

**#12: DimensionDrawing-SmartSolar-150_60A-&-150_70A-MC4-3D.STEP** ✅
- Fan Width: 210.00mm | Total Width: 250.00mm | Length: 171.00mm | Height: 36.00mm
- **Note:** Identical to #11 - Same 250×171×36mm dimensions (MC4 vs Tr connector variant only)

**#13: SS-MPPT-250-60-70-MC4-3D.STEP** ✅
- Fan Width: 208.50mm | Total Width: 244.50mm | Length: 170.70mm | Height: 38.00mm
- **Note:** Identical to #8 - Same 244.5×170.7×38mm dimensions (B3 config, 250/60-70 series)

**#14: SmartSolar-MPPT-150-250-85-100-MC4-VE.Can.STEP** ✅
- Fan Width: 242.60mm | Total Width: 290.60mm | Length: 204.10mm | Height: 38.10mm
- **Note:** Identical to #10 - Same 290.6×204.1×38.1mm dimensions (B1/B2 config, large format series)

**#15: SmartSolar-MPPT-250V-60-70-Tr-3D.STEP** ✅
- Fan Width: 208.50mm | Total Width: 244.50mm | Length: 170.70mm | Height: 38.00mm
- **Note:** Identical to #8/#13 - Same 244.5×170.7×38mm dimensions (B3 config, 250/60-70 series complete)

**SCREW HOLE MAPPING BY CONFIGURATION:**

**A1 Config (8 CSV models, 2 STEP files):** Sideways U holes, 18mm rail width
- Physical: 187×122×26.5mm | Fan: 157mm 
- Models: SCC020030200, SCC110030210, SCC020050200, SCC020035000, SCC115045222, SCC110050210, SCC115035210, SCC115045212
- STEP Files: #1 BS-SS-MPPT-100-30, #2 BS-SS-MPPT-100-50-150-35-150-45

**A3 Config (4 CSV models, 1 STEP file):** Circle holes, 18mm rail width  
- Physical: 128×97.7×26.5mm | Fan: 106mm
- Models: SCC110020070R, SCC110020170R, SCC110020060R, SCC110020160R
- STEP Files: #5 BlueSolar-SmartSolar-MPPT-100V20A

**B1 Config (5 CSV models, 0 unique STEP files):** Keyhole + Rounded slot, 23.3mm rail width
- Expected: ~295×204×23.3mm (CSV estimates)
- Models: SCC115110211, SCC115085211, SCC125110210, SCC125085210
- **NOTE:** These may share physical dimensions with B2 config (290.6×204.1×38.1mm measured)

**B2 Config (6 CSV models, 2 STEP files):** Keyhole + Rounded slot, 23.3mm rail width
- Physical: 290.6×204.1×38.1mm | Fan: 242.6mm
- Models: SCC115085411/412, SCC115110410/411, SCC115110420, SCC125085411, SCC125110411/412, SCC125110441  
- STEP Files: #10 SS-MPPT-Tr-VE.Can-(XL), #14 SmartSolar-MPPT-150-250-85-100-MC4-VE.Can

**B3 Config (2 CSV models, 3 STEP files):** Keyhole + Rounded slot, 23.3mm rail width
- Physical: 244.5×170.7×38mm | Fan: 208.5mm
- Models: SCC125060221, SCC125070220
- STEP Files: #8 SS-MPPT-150-250-70-MC4-VE.CAN-(L), #13 SS-MPPT-250-60-70-MC4, #15 SmartSolar-MPPT-250V-60-70-Tr

**C1 Config (4 CSV models, 1 STEP file):** Circle holes, 0mm rail (housing-based)
- Physical: 121.8×98.87×0mm | Fan: 81.9mm  
- Models: SCC010010050R, SCC010015050R, SCC075010060R, SCC075015060R
- STEP Files: #3 Blue-Smart-Solar-charge-controller-MPPT-75V-10A-15A-3D

**C2 Config (2 CSV models, 1 STEP file):** Circle holes, 0mm rail (housing-based)
- Physical: 113.8×99.93×0mm | Fan: 86.4mm
- Models: SCC010015200R, SCC110015060R  
- STEP Files: #4 BlueSolar-&-Smartsolar-MPPT-100-15

**UNACCOUNTED STEP FILES (5 models):** Same physical dimensions as other groups
- #6,#7,#9,#11,#12: All 250×171×36mm - **Need flange config assignment!**

**Controller Categories by Size:**
1. **Housing-Based (No External Heatsinks):** 2 groups - C1, C2 configs (7 total models)
2. **Small with External Heatsink:** 1 group - A3 config (4 models)  
3. **Medium with Heatsinks:** 1 group - A1 config (8 models)
4. **Large with Heatsinks:** 3 groups - B1, B2, B3 configs (13 total models)
3. **Medium with Heatsinks:** 6 models - A1 config (100/30-50, 150/35-45)  
4. **Large with Heatsinks:** 10 models - B1, B2, B3 configs (150/85+, 250 series)

**Corrected Design Parameters (A1 Config - Measured):**
- **Total Width:** 187mm (controller + heatsinks + flanges)
- **Fan Area:** 157mm × 122mm (usable space for fan mounting)
- **Heatsink Width:** 26.5mm each side (physical dimension)
- **Rail Width:** 18mm (from flange data, not 30mm estimated)
- **Mounting Pattern:** 2×Sideways U holes per side
- **Hole Positions:** Top Z=25mm, Bottom Z=96.5mm

**Reverse L-Shape (---|_) Confirmed:**
- **Vertical fins (`|`):** 36-44mm high for heat dissipation
- **Horizontal flanges (`_`):** 23.3mm wide for mounting (STANDARDIZED!)
- **Controller width:** 203.5mm maximum (B2 X-Large VE.Can models)

### Key Design Implications:
1. **Heatsink shape:** `---|_` reverse L on each side of controller
2. **Vertical fins (`|`):** Protrude only ~36-44mm from controller base (back/forth)
3. **Horizontal flanges (`_`):** Extend ~23.5mm outward for mounting (determines rail width)
4. **Side rails mount to horizontal flanges (`_`), NOT to vertical fins (`|`)**
5. **Fan clearance needed:** ~50mm above controller base for vertical fins
6. **Rail width requirement:** ~30mm based on horizontal flange width

### Clearance Requirements CORRECTED:
- **All Models:** ~50-60mm fan clearance above controller base
- **Side Rail Width:** Determined by flange foot width (~23.5-30mm typical)
- **Mounting Strategy:** Attach to L-shaped flange feet at controller edges

## File Mapping

### STEP Files with Heatsink Components (13 files):
1. `/step_drawings/BS-SS-MPPT-100-30-(stp).STEP` → `/source_drawings/BS-SS-MPPT-100-30.pdf`
2. `/step_drawings/BS-SS-MPPT-100-50-150-35-150-45-(step).STEP` → `/source_drawings/BS-SS-MPPT-100-50-150-35-150-45.pdf`
3. `/step_drawings/Blue-Smart-Solar-charge-controller-MPPT-75V-10A-15A-3D.STEP` → `/source_drawings/BlueSolar-&-SmartSolar-MPPT-75-10-&-75-15.pdf`
4. `/step_drawings/DimensionDrawing-BlueSolar-150_60-&-150_70-MC4-3D.STEP` → *No direct PDF match*
5. `/step_drawings/DimensionDrawing-BlueSolar-150_60-&-150_70-Tr-3D.STEP` → *No direct PDF match*
6. `/step_drawings/DimensionDrawing-SS-MPPT-150-250-70-MC4-VE.CAN-(L)-3D.STEP` → `/source_drawings/SmartSolar-MPPT-150-250-85-100-Tr-(dimensions).pdf`
7. `/step_drawings/DimensionDrawing-SS-MPPT-150-250-70-Tr-VE.Can-(L)-3D.STEP` → `/source_drawings/SmartSolar-MPPT-150-250-85-100-Tr-(dimensions).pdf`
8. `/step_drawings/DimensionDrawing-SS-MPPT-Tr-VE.Can-(XL)-3D.STEP` → `/source_drawings/DimensionDrawing-SS-MPPT-Tr-VE.Can-(XL).pdf`
9. `/step_drawings/DimensionDrawing-SmartSolar-150_60A-&-150_70-Tr-3D.STEP` → *No direct PDF match*
10. `/step_drawings/DimensionDrawing-SmartSolar-150_60A-&-150_70A-MC4-3D.STEP` → *No direct PDF match*
11. `/step_drawings/SS-MPPT-250-60-70-MC4-3D.STEP` → `/source_drawings/SmartSolar-MPPT-250V-60-70-Tr.pdf`
12. `/step_drawings/SmartSolar-MPPT-150-250-85-100-MC4-VE.Can.STEP` → `/source_drawings/SmartSolar-MPPT-150-250-85-100-Tr-(dimensions).pdf`
13. `/step_drawings/SmartSolar-MPPT-250V-60-70-Tr-3D.STEP` → `/source_drawings/SmartSolar-MPPT-250V-60-70-Tr.pdf`

### Housing-Based Models (No Separate Heatsink):
- `BlueSolar-&-Smartsolar-MPPT-100-15-(stp).STEP` → `/source_drawings/BlueSolar-&-Smartsolar-MPPT-100-15.pdf`
- `BlueSolar-SmartSolar-MPPT-100V20A--(3D).STEP` → `/source_drawings/BlueSolar-SmartSolar-MPPT-100V20A-(Dimensions).pdf`

## Clearance Requirements for Fan Mount Design

### Critical Measurements Needed:
1. **Heatsink Protrusion Height:** Maximum Z-height of heatsink above controller base
2. **Heatsink Footprint:** X,Y dimensions for clearance calculations
3. **Mounting Hole Patterns:** Location relative to heatsink for secure mounting
4. **Fin Orientation:** Airflow direction for optimal fan placement
5. **Material Thickness:** Wall thickness of heatsink fins for structural analysis

### Design Impact:
- **Fan Mount Height:** Must clear highest heatsink point + safety margin
- **Fan Positioning:** Align with heatsink fins for optimal airflow
- **Rail Height:** Calculated based on heatsink clearance requirements
- **Mounting Strategy:** Avoid interference with heatsink mounting points

## Data Collection Status

### Completed Tasks:
1. ✅ **PDF Analysis:** Successfully extracted dimensions from 8 PDF files using pdftotext
2. ✅ **Dimensional Categorization:** Identified 3 form factor groups (compact, medium, large)
3. ✅ **Height Analysis:** Determined heatsink heights from 98.6mm to 268mm
4. ✅ **Mounting Pattern Documentation:** Cataloged hole patterns (R2-R8 specifications)

### Remaining Tasks:
1. **CAD Software Analysis:** Measure fin spacing and detailed heatsink geometry from STEP files
2. **Manual Verification:** Cross-reference PDF measurements with STEP file analysis
3. **Fin Orientation Analysis:** Determine optimal airflow direction for each model
4. **Design Validation:** Finalize clearance calculations for fan mount design

### Tools Used:
- ✅ pdftotext (poppler-utils) for PDF dimension extraction
- ⏳ CAD software analysis pending for detailed heatsink geometry
- ⏳ Spreadsheet integration with scad_data.xlsx and specifications.txt

## Integration with OpenSCAD Design

### Ready for Implementation:
- **Height Clearances:** Documented for all 13 heatsink models
- **Footprint Dimensions:** Available for mounting system design
- **Form Factor Categories:** Enable scalable design approach
- **Mounting Patterns:** Support secure attachment design
- **Standardized Flange Width:** 23.3mm across all heatsink models

### **Missing Data Requirements for Complete Implementation:**
The CSV structure needs additional columns:
1. **`step_file`** - Link to corresponding STEP files
2. **`screw_hole_shape`** - Shape type (Circle, Key hole, Sideways U)
3. **`hole_positions`** - X,Y coordinates of mounting holes in flanges
4. **`hole_diameter`** - M4 hole size specifications

### **Screw Hole Shape Design Impact:**
- **Circle:** Standard bolt-through mounting (round holes)
- **Key hole:** Hang-and-slide mounting (keyhole slots - wide head, narrow shaft)
- **Sideways U:** Slide-in mounting from side (U-shaped slots)
- **Side rail design** must accommodate these different mounting methods
- **OpenSCAD implementation** needs conditional geometry based on hole shape

### Next Integration Steps:
1. Export dimensional data to scad_data.xlsx format
2. Update specifications.txt with clearance requirements
3. Generate OpenSCAD lookup tables with heatsink clearance data
4. Design universal mounting system accommodating all form factors

---

**File Path:** `/Users/colin/IdeaProjects/fan_controllers/docs/heatsink_measurements.md`

**Note:** This document requires manual measurement extraction from STEP/PDF files using appropriate CAD software tools.