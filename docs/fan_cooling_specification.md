# Fan Cooling System Specification

**Author:** Colin Bitterfield  
**Email:** colin@bitterfield.com  
**Date Created:** 2025-08-24  
**Date Updated:** 2025-08-26  
**Version:** 0.2.0

## 1. System Overview

The fan cooling system is a parametric 3D printable base mount designed to sit under Victron solar charge controllers from the step_drawings directory. The system provides active cooling through strategically placed fans and generates custom mounting assemblies based on controller specifications and fan requirements.

## 2. Design Requirements

### 2.1 Primary Function
- Create base mount that sits under solar charge controllers
- Mount 1-x number of cooling fans for active cooling
- Provide secure mounting platform for controller placement
- Protect fans with hexagonal honeycomb grille pattern
- Accommodate various Victron controller models from step_drawings directory

### 2.2 Design Constraints
- All dimensions in metric units
- Minimum wall thickness: 4mm (except front/rear plates: 3-5mm adjustable)
- Standard 4mm hex bolts throughout system
- Front/rear plate thickness: 3.5mm default (adjustable 3-5mm for screw clearance)
- Material compatibility with 3D printing (PLA/PETG/ABS)

## 3. System Architecture

The cooling mount consists of 4 distinct pieces that create a base platform for solar charge controllers:

### 3.1 Four-Piece Assembly

#### 3.1.1 Front Fan Mount (Part 1)
- **Thickness:** 6mm (fixed for structural integrity)
- **Dimensions:** `plate_width × plate_length × plate_thickness`
  - `plate_width = total_width` (spans across rails)
  - `plate_length = fan_size + 4mm` (fan height + 4mm spacing)
  - `plate_thickness = 6mm` (fixed)
- **Function:** Front face where cooling fans mount
- **Supported Fan Sizes:** 40mm × 40mm or 50mm × 50mm (15mm thick)
- **Features:** 
  - Recessed nut wells: 3mm deep, 5.3mm diameter (both 40mm and 50mm fans)
  - Screw patterns: 30mm × 30mm (40mm fans, M3) or 40mm × 40mm (50mm fans, M4)
  - Fan opening: `fan_size - 8mm` diameter for mounting frame
  - Rail mounting holes at 1/4 and 3/4 of rail height
- **Color:** Blue

#### 3.1.2 Left Side Rail (Part 2)
- **Function:** Primary structural rail (key component)
- **Dimensions:** `rail_width × rail_length × rail_height`
  - `rail_width = 18mm` (standard width from flange data)
  - `rail_length = controller_length` (matches controller exactly)
  - `rail_height = (fan_size + 4) - heatsink_height` (clearance formula)
- **Mounting Features:**
  - Controller mounting holes: Sideways U, Circle, or Keyhole patterns
  - Plate connection holes: M4 holes at 1/4 and 3/4 of rail height
  - Through holes for controller attachment (varies by config)
- **Hole Patterns by Configuration:**
  - **A1:** Sideways U holes at 25mm and 96.5mm from edge (8mm wide)
  - **A3/C1/C2:** Circle holes from top (M4 diameter)
  - **B1/B2/B3:** Keyhole patterns from top with additional center holes
- **Color:** Black

#### 3.1.3 Right Side Rail (Part 3)
- **Function:** Mirror image of left rail for structural balance
- **Configuration:** Exact mirror of Part 2 (left rail)
- **Features:** Identical to left rail but mirrored across centerline
- **Color:** Black

#### 3.1.4 Rear Hexagonal Grill (Part 4)
- **Thickness:** 6mm (same as front plate)
- **Dimensions:** Same as front fan mount (`plate_width × plate_length × plate_thickness`)
- **Function:** Protective rear grille with airflow ventilation
- **Pattern:** Hexagonal honeycomb design optimized for airflow
  - **Hex diameter:** 10mm (reduced size for better packing density)
  - **Hex spacing:** 2mm between holes for structural integrity
  - **Pattern rotation:** 30 degrees for optimal orientation
  - **Coverage:** Full fan area top-to-bottom with 1mm margins
- **Grid Calculation:**
  - `x_spacing = hex_center_distance × 0.87` (hexagonal packing)
  - `y_spacing = hex_center_distance × 0.75` (row offset)
  - Alternating row offset for true honeycomb pattern
- **Rail mounting holes:** Same positions as front plate
- **Color:** Blue

## 4. OpenSCAD Lookup Table Implementation

### 4.1 Controller Selection System
The first critical component is creating a lookup table system to select which controller model to use from the step_drawings directory. This table maps model codes to controller specifications.

#### 4.1.1 Available Controller Models
Based on step_drawings directory contents:
- BS-SS-MPPT-100-30
- BS-SS-MPPT-100-50-150-35-150-45  
- Blue-Smart-Solar-charge-controller-MPPT-75V-10A-15A-3D
- BlueSolar-&-Smartsolar-MPPT-100-15
- BlueSolar-SmartSolar-MPPT-100V20A
- DimensionDrawing-BlueSolar-150_60-&-150_70-MC4-3D
- DimensionDrawing-BlueSolar-150_60-&-150_70-Tr-3D
- DimensionDrawing-SS-MPPT-150-250-70-MC4-VE.CAN-(L)-3D
- DimensionDrawing-SS-MPPT-150-250-70-Tr-VE.Can-(L)-3D
- DimensionDrawing-SS-MPPT-Tr-VE.Can-(XL)-3D
- DimensionDrawing-SmartSolar-150_60A-&-150_70-Tr-3D
- DimensionDrawing-SmartSolar-150_60A-&-150_70A-MC4-3D
- SS-MPPT-250-60-70-MC4-3D
- SmartSolar-MPPT-150-250-85-100-MC4-VE.Can
- SmartSolar-MPPT-250V-60-70-Tr-3D

### 4.2 Lookup Table Structure
The controller_models.scad file must contain:
```openscad
// Controller lookup table - maps model_code to dimensions and specifications
controller_data = [
    ["model_code", "model_name", "length", "width", "height", "flange_config", "heatsink_type"],
    // Example entries based on step_drawings
    ["BS-SS-MPPT-100-30", "BlueSolar/SmartSolar MPPT 100/30", 100, 60, 35, "standard", "heatsink"],
    ["MPPT-75-10-15", "Blue Smart Solar MPPT 75V 10A-15A", 95, 65, 30, "compact", "heatsink"],
    ["MPPT-100-15", "BlueSolar/SmartSolar MPPT 100-15", 95, 55, 25, "housing", "housing"],
    ["MPPT-100V20A", "BlueSolar/SmartSolar MPPT 100V20A", 100, 65, 30, "housing", "housing"],
    // Additional entries for each model in step_drawings...
];

// Available screw lengths for both M3 and M4
screw_lengths = [12, 16, 20, 25, 30, 35]; // mm

// Function to calculate optimal screw length based on fan size and plate thickness
function calculate_screw_length(fan_size = 50, fan_thickness = 15, plate_thickness = 3.5) =
    let(nut_inset = (fan_size == 50) ? 1 : 0, // 50mm fans have recessed nut wells, 40mm do not
        required_length = fan_thickness + plate_thickness - nut_inset)
    [for (length = screw_lengths) if (length >= required_length) length][0]; // First suitable length
```

## 5. Parametric System

### 5.1 Input Parameters
- **model_code:** Controller identifier from controller_models.scad lookup table
- **fan_size:** Fan dimensions (40mm or 50mm square) - determines screw pattern
- **fan_count:** Number of fans (1-x fans based on controller width)
- **plate_thickness:** Front/rear plate thickness (3mm to 5mm, default: 3.5mm)

### 5.2 Derived Calculations

**Critical Formulas:**
- **Rail Height:** `rail_height = (fan_size + 4) - heatsink_height`
- **Plate Length:** `plate_length = fan_size + 4` (53mm for 50mm fans, 44mm for 40mm fans)
- **Plate Width:** `plate_width = total_width` (spans full controller width)
- **Fan Area Width:** `fan_area_width` (from controller database)
- **Rail Positions:** 1/4 and 3/4 of rail height from bottom

**Fan Configuration:**
- **Fan Count:** Based on optimal configuration analysis (prioritizes 50mm fans)
- **Fan Spacing:** Centered within fan area with equal gaps
- **Screw Patterns:** 30mm × 30mm (40mm fan, M3) or 40mm × 40mm (50mm fan, M4)

**Hardware Specifications:**
- **All configurations use recessed nut wells:** 3mm deep, 5.3mm diameter
- **Screw lengths:** 12, 16, 20, 25, 30, 35mm available
- **Recommended screw length:** 20-25mm for 6mm plates with 15mm fan thickness

### 5.3 Coordinate System
- **X-Axis:** Width (left ↔ right)
- **Y-Axis:** Depth (front → back)
- **Z-Axis:** Height (bottom → top, Z0 = bottom)

## 6. Data Tables and Configuration

### 6.1 Controller Models (controller_models.scad)
- Controller dimensions and specifications derived from step_drawings
- Flange rail configuration mapping
- Model-specific mounting requirements
- Lookup table implementation for model selection
- **Heatsink vs Housing-based designs:**
  - 13 controllers have dedicated heatsink components (87%)
  - 2 controllers use housing-based mounting (BlueSolar MPPT 100-15, BlueSolar MPPT 100V20A)
  - Housing-based models: screw specifications integrated into main housing component

### 6.2 Fan Specifications (fan_specs.scad)
- **Available Fan Sizes:** 40mm × 40mm and 50mm × 50mm
- **Standard Thickness:** 15mm for all fans
- **Screw Patterns and Hardware:**
  - 40mm × 40mm fan: Screw centers at 30mm × 30mm, **M3 screws**, no recessed nut well
  - 50mm × 50mm fan: Screw centers at 40mm × 40mm, **M4 screws**, recessed nut well
- **Screw Inset:** 5mm from fan edges to screw center

### 6.3 Hardware Specifications
- **Fan Mounting (per fan):**
  - 4 × M3 screws + 4 × M3 hex nuts (40mm fans)
  - 4 × M4 screws + 4 × M4 hex nuts (50mm fans)
  - Available lengths for both M3/M4: 12, 16, 20, 25, 30, 35mm
- **Assembly Fasteners (per connection plate):**
  - Front plate: 4 × M4 screws + 4 × M4 flange nuts
  - Rear plate: 4 × M4 screws + 4 × M4 flange nuts
  - M4 flange nuts from nut_profiles.scad (default: M4×9.1×6.3)
- **Mounting Hole Shapes:** Three types for controller attachment
  - Circle: Standard round holes
  - Key hole: Keyhole-shaped slots for hanging mount
  - Sideways U: U-shaped slots for sliding mount

## 7. Assembly Specifications

### 7.1 Four-Piece Connection Method
- Front fan mount (Part 1) connects to side rails (Parts 2 & 3) with screws
- Rear hexagonal grill (Part 4) attaches with same screw pattern
- Screws centered on rails, positioned 25% from top/bottom
- Flange nuts inset into rails for secure connection
- Controller sits on top of assembled base mount

### 7.2 Assembly Order
1. Install flange nuts in rail recesses (Parts 2 & 3)
2. Mount cooling fans to front plate (Part 1)
3. Connect front plate to side rails
4. Attach hexagonal grill to rear (Part 4)
5. Place solar controller on top of assembled base
6. Secure entire assembly to mounting surface

## 8. Output Requirements

### 8.1 Pre-Render Information Display
Before model generation, system must output:
- Model Code
- Model Name  
- Fan Size (40mm or 50mm)
- Recommended Screw Size (M3 or M4)
- Calculated Screw Length (from available: 12, 16, 20, 25, 30, 35mm)
- Total Width
- Fan Width

### 8.2 File Generation
- Complete parametric OpenSCAD code
- Ready for cut-and-paste implementation
- Version control with locked/unlocked code blocks

## 9. Material and Manufacturing

### 9.1 3D Printing Requirements
- Layer height: 0.2-0.3mm recommended
- Infill: Minimum 20% for structural integrity
- Supports: Required for overhangs and bridges
- Post-processing: Clean support material, test-fit hardware

### 9.2 Hardware Requirements
- **Fan Mounting:** 4 screws + 4 hex nuts per fan
  - 40mm fans: M3 × 20mm screws + M3 hex nuts
  - 50mm fans: M4 × 20mm screws + M4 hex nuts
- **Assembly:** 8 total M4 screws + 8 M4 flange nuts (4 each for front/rear plates)
- **Cooling fans:** 40mm × 40mm or 50mm × 50mm, 15mm thick per specification
- **Surface mounting:** Wall mounting hardware (user-supplied)

## 10. Quality Assurance

### 10.1 Design Validation
- Verify all clearances meet minimum requirements
- Confirm screw length calculations
- Validate fan mounting patterns
- Check wall thickness compliance
- **Component-specific validation:**
  - Heatsink-based models: Ensure adequate clearance around heatsink components
  - Housing-based models: Extract screw specifications from housing component geometry

### 10.2 Testing Requirements
- Test fit all hardware before final assembly
- Verify fan airflow clearance
- Confirm controller heat dissipation
- Validate mounting stability

---

**Revision History:**
- v0.1.0 (2025-08-24): Initial specification document creation
- v0.1.1 (2025-08-24): Updated to clarify base mount design, added OpenSCAD lookup table implementation, detailed four-piece assembly structure
- v0.1.2 (2025-08-24): Updated fan specifications - 40x40mm and 50x50mm fans (15mm thick), screw patterns 30x30mm and 40x40mm respectively
- v0.1.3 (2025-08-24): Added screw type specifications - M3 for 40mm fans, M4 for 50mm fans
- v0.1.4 (2025-08-24): Updated screw lengths to 12,16,20,25,30,35mm, added recessed nut well specification (50mm fans only)
- v0.1.5 (2025-08-24): Detailed hardware count - 4 screws/nuts per fan, 4 screws/flange nuts per front/rear plate
- v0.1.6 (2025-08-24): Updated plate thickness to 3.5mm default (3-5mm adjustable), updated screw length calculations
- v0.1.7 (2025-08-24): Added heatsink component analysis - 13 models with heatsinks, 2 housing-based models (MPPT 100-15, 100V20A)
- v0.2.0 (2025-08-26): Final implementation update - Fixed plate thickness to 6mm, added critical formulas for rail height calculation `(fan_size + 4) - heatsink_height`, updated all component dimensions, refined honeycomb grill specifications, added complete hole pattern details for all configuration types, updated hardware to use recessed nut wells for both fan sizes