# Fan Size Override Calculations

**Author:** Colin Bitterfield
**Email:** colin@bitterfield.com
**Date Created:** 2026-02-16
**Version:** 1.0.0

## Overview

When `fan_size_override` is set to a value other than 0 (AutoSelect), the system automatically recalculates the optimal number of fans that can fit in the available fan area.

## Calculation Formula

The fan count calculation uses a minimum 2mm gap between fans and at edges:

```
fan_count = floor((fan_area_width - min_gap) / (fan_size + min_gap))
fan_count = max(1, fan_count)  // Always at least 1 fan
```

Where:
- `fan_area_width` = Available width for fans (from controller database)
- `fan_size` = Overridden fan size (40mm or 50mm)
- `min_gap` = 2mm (minimum spacing between fans and edges)

## Test Cases

### A1 Config - BlueSolar 100/30 (SCC020030200)
- **Fan Area Width:** 157mm
- **Database Default:** 3×50mm fans

**Override to 40mm fans:**
```
fan_count = floor((157 - 2) / (40 + 2))
fan_count = floor(155 / 42)
fan_count = floor(3.69)
fan_count = 3 fans
```
Result: 3×40mm fans (120mm) with 37mm total gap = 9.25mm per gap ✓

**Override to 50mm fans (no change):**
```
fan_count = floor((157 - 2) / (50 + 2))
fan_count = floor(155 / 52)
fan_count = floor(2.98)
fan_count = 2 fans ← CHANGES FROM DATABASE VALUE!
```
**Note:** This gives 2×50mm instead of the database's 3×50mm because the database uses tighter spacing (1.75mm gaps). When override is active, system enforces 2mm minimum gap.

### A3 Config - BlueSolar 100/20 (SCC110020070R)
- **Fan Area Width:** 106mm
- **Database Default:** 2×50mm fans

**Override to 40mm fans:**
```
fan_count = floor((106 - 2) / (40 + 2))
fan_count = floor(104 / 42)
fan_count = floor(2.48)
fan_count = 2 fans
```
Result: 2×40mm fans (80mm) with 26mm total gap = 8.67mm per gap ✓

**Override to 50mm fans:**
```
fan_count = floor((106 - 2) / (50 + 2))
fan_count = floor(104 / 52)
fan_count = floor(2.0)
fan_count = 2 fans
```
Result: 2×50mm fans (100mm) with 6mm total gap = 2mm per gap ✓

### B1 Config - SmartSolar 150/85-Tr (SCC115085211)
- **Fan Area Width:** 242mm
- **Database Default:** 4×50mm fans

**Override to 40mm fans:**
```
fan_count = floor((242 - 2) / (40 + 2))
fan_count = floor(240 / 42)
fan_count = floor(5.71)
fan_count = 5 fans
```
Result: 5×40mm fans (200mm) with 42mm total gap = 7mm per gap ✓

**Override to 50mm fans:**
```
fan_count = floor((242 - 2) / (50 + 2))
fan_count = floor(240 / 52)
fan_count = floor(4.62)
fan_count = 4 fans
```
Result: 4×50mm fans (200mm) with 42mm total gap = 8.4mm per gap ✓

### C1 Config - BlueSolar 75/10 (SCC010010050R)
- **Fan Area Width:** 81.9mm
- **Database Default:** 2×40mm fans

**Override to 50mm fans:**
```
fan_count = floor((81.9 - 2) / (50 + 2))
fan_count = floor(79.9 / 52)
fan_count = floor(1.54)
fan_count = 1 fan
```
Result: 1×50mm fan (50mm) with 31.9mm total gap = 16mm per gap ✓

**Override to 40mm fans:**
```
fan_count = floor((81.9 - 2) / (40 + 2))
fan_count = floor(79.9 / 42)
fan_count = floor(1.90)
fan_count = 1 fan ← CHANGES FROM DATABASE VALUE!
```
**Note:** Database has 2×40mm fans with very tight spacing (0.95mm gaps). When override enforces 2mm minimum, only 1 fan fits.

## Important Notes

1. **Minimum Gap Enforcement:** The override calculation enforces a 2mm minimum gap, which may result in fewer fans than the database specifies for some configurations. This is intentional to ensure printability and assembly.

2. **Always Check Output:** When using fan_size_override, check the OpenSCAD console output for the recalculation notice:
   ```
   Fans: 3×40mm (Manual 40mm) [Recalculated from 3×50mm]
   ```

3. **Design Implications:**
   - Overriding to smaller fans may fit more fans (e.g., B1 config: 4×50mm → 5×40mm)
   - Overriding to larger fans may fit fewer fans (e.g., C1 config: 2×40mm → 1×50mm)
   - Rail mounting holes and plate dimensions adjust automatically
   - Honeycomb rear grill pattern remains centered in fan area

## Implementation Details

### New Functions (v2.3.0)

```scad
// Calculate optimal fan count for given fan size and available area
function calculate_fan_count(fan_area_width, fan_size) =
    let(
        min_gap = 2,  // Minimum 2mm gap between fans and edges
        max_count = floor((fan_area_width - min_gap) / (fan_size + min_gap))
    )
    max(1, max_count);  // Always at least 1 fan

// Get effective fan count (recalculates if fan size is overridden)
function get_effective_fan_count(ctrl) =
    fan_size_override == 0 ? get_fan_count(ctrl) :  // AutoSelect - use database
    calculate_fan_count(get_fan_area_width(ctrl), fan_size_override);  // Recalculate
```

### Console Output Enhancement

The system now displays recalculation notices:
```
Generating component 1 for BlueSolar MPPT 100/30
Dimensions: 186×122×23mm
Fans: 3×40mm (Manual 40mm) [Recalculated from 3×50mm]
Model: SCC020030200 | Component: front_fan_mount
Suggested STL name: SCC020030200_front_fan_mount.stl
```

## Usage Example

To override a controller to use 40mm fans instead of default:

1. Open `solar_controller_cooling_mount.scad`
2. Set model: `model_code = "SCC020030200";`
3. Set override: `fan_size_override = 40;`  // Force 40mm fans
4. Set component: `component = 1;`  // Front fan mount
5. Render and check console for recalculated fan count
6. Export STL

The system will automatically:
- Calculate how many 40mm fans fit (3 in this case)
- Adjust rail heights for 40mm fan clearance
- Update plate dimensions to match 40mm fan height
- Center fans with proper spacing in available area
