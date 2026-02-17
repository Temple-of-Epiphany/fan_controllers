# Fan Configuration Analysis

**Author:** Colin Bitterfield  
**Email:** colin@bitterfield.com  
**Date Created:** 2025-08-25  
**Date Updated:** 2025-08-25  
**Version:** 0.1.0

## Fan Specifications

**40x40mm fans:**
- Physical size: 40×40×15mm
- Screw centers: 30×30mm (M3 screws)
- No recessed nut wells
- Effective area per fan: ~40×40 = 1600mm²

**50x50mm fans:**
- Physical size: 50×50×15mm  
- Screw centers: 40×40mm (M4 screws)
- Recessed nut wells
- Effective area per fan: ~50×50 = 2500mm²

## Optimal Fan Configuration Analysis

**Priority:** Use 50×50mm fans whenever possible for better cooling efficiency.

### Configuration by Controller Size

**1. A1 Config (Medium Controllers): Fan Area 157×122mm**
- Available area: 157mm width
- 50×50mm: 157 ÷ 50 = 3.14 → **3 fans** (150mm used, 7mm gap)
- 40×40mm: 157 ÷ 40 = 3.925 → 3 fans (120mm used, 37mm gap)
- **OPTIMAL: 3×50mm fans** (better cooling, similar fit)

**2. A3 Config (Small Controllers): Fan Area 106×97.7mm**  
- Available area: 106mm width
- 50×50mm: 106 ÷ 50 = 2.12 → **2 fans** (100mm used, 6mm gap)
- 40×40mm: 106 ÷ 40 = 2.65 → 2 fans (80mm used, 26mm gap)
- **OPTIMAL: 2×50mm fans** (better cooling, tighter fit)

**3. Large Format A: Fan Area 210×171mm**
- Available area: 210mm width  
- 50×50mm: 210 ÷ 50 = 4.2 → **4 fans** (200mm used, 10mm gap)
- 40×40mm: 210 ÷ 40 = 5.25 → 5 fans (200mm used, 10mm gap)
- **OPTIMAL: 4×50mm fans** (equivalent area coverage, better individual performance)

**4. Large Format B: Fan Area 208.5×170.7mm**
- Available area: 208.5mm width
- 50×50mm: 208.5 ÷ 50 = 4.17 → **4 fans** (200mm used, 8.5mm gap)
- 40×40mm: 208.5 ÷ 40 = 5.21 → 5 fans (200mm used, 8.5mm gap)  
- **OPTIMAL: 4×50mm fans** (better cooling efficiency)

**5. XL Format: Fan Area 242.6×204.1mm**
- Available area: 242.6mm width
- 50×50mm: 242.6 ÷ 50 = 4.85 → **4 fans** (200mm used, 42.6mm gap)
- Alternative: 242.6 ÷ 50 = could fit **5 fans** if staggered (250mm > 242.6mm - tight)
- 40×40mm: 242.6 ÷ 40 = 6.065 → 6 fans (240mm used, 2.6mm gap)
- **OPTIMAL: 4×50mm fans** (good gap for mounting, excellent cooling)

**6. C1 Config (Housing-Based): Fan Area 81.9×98.87mm**
- Available area: 81.9mm width
- 50×50mm: 81.9 ÷ 50 = 1.64 → **1 fan** (50mm used, 31.9mm gap - large gap)
- 40×40mm: 81.9 ÷ 40 = 2.05 → **2 fans** (80mm used, 1.9mm gap - tight fit)
- **OPTIMAL: 2×40mm fans** (better coverage despite smaller individual performance)

**7. C2 Config (Housing-Based): Fan Area 86.4×99.93mm**  
- Available area: 86.4mm width
- 50×50mm: 86.4 ÷ 50 = 1.73 → **1 fan** (50mm used, 36.4mm gap - large gap)
- 40×40mm: 86.4 ÷ 40 = 2.16 → **2 fans** (80mm used, 6.4mm gap - good fit)
- **OPTIMAL: 2×40mm fans** (better coverage)

## Summary Table

| Config | Fan Area (mm) | 50×50mm Option | 40×40mm Option | **OPTIMAL CHOICE** | Reasoning |
|--------|---------------|----------------|----------------|-------------------|-----------|
| A1 | 157×122 | 3 fans | 3 fans | **3×50mm** | Better cooling, similar fit |
| A3 | 106×97.7 | 2 fans | 2 fans | **2×50mm** | Better cooling, good fit |
| Large A | 210×171 | 4 fans | 5 fans | **4×50mm** | Equal coverage, better individual performance |
| Large B | 208.5×170.7 | 4 fans | 5 fans | **4×50mm** | Better cooling efficiency |
| XL | 242.6×204.1 | 4 fans | 6 fans | **4×50mm** | Good gap, excellent cooling |
| C1 | 81.9×98.87 | 1 fan (large gap) | 2 fans | **2×40mm** | Better coverage |
| C2 | 86.4×99.93 | 1 fan (large gap) | 2 fans | **2×40mm** | Better coverage |

## Key Design Implications

**Screw Requirements:**
- **50×50mm configs:** M4 screws (lengths: 12,16,20,25,30,35mm)
- **40×40mm configs:** M3 screws (lengths: 12,16,20,25,30,35mm)

**Mounting Design:**
- **50×50mm fans:** Must accommodate recessed nut wells
- **40×40mm fans:** Standard flat mounting (no recess needed)

**Airflow Performance:**
- Larger fans (50×50mm) typically provide better CFM per fan
- Fewer, larger fans reduce complexity and potentially noise
- Smaller controllers (C1/C2) benefit more from multiple smaller fans due to limited space

## OpenSCAD Implementation Impact

**Parametric Design Requirements:**
1. **Fan type selection:** 40mm vs 50mm based on controller config
2. **Fan count:** Variable based on optimal configuration (1-6 fans)
3. **Screw type:** M3 vs M4 based on fan size
4. **Nut well accommodation:** Recessed for 50mm, flat for 40mm
5. **Gap distribution:** Center fans with equal gaps on sides

**Lookup Table Updates Needed:**
- Add `fan_type` column (40mm/50mm)
- Add `fan_count` column (1-6)
- Add `screw_type` column (M3/M4)
- Add `nut_recess` column (true/false)