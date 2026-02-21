# Victron MPPT Dimensional Discrepancy Report

**Author:** Colin Bitterfield
**Email:** colin@bitterfield.com
**Date:** 2026-02-20
**Version:** 1.0.0
**Reference:** SmartSolar MPPT 150/60-Tr (SCC115060210) physical unit comparison

---

## Summary

During development of a parametric 3D-printed cooling mount system for Victron MPPT
solar charge controllers, three faults were identified when comparing published STEP
files against physical units and each other. These are reported to Victron for
correction of published documentation and CAD assets.

---

## Fault 1 — Dimensional Discrepancy: A4 Heatsink Body Width

**Severity:** High
**Affects:** SmartSolar MPPT 150/60-Tr, 150/70-Tr (SCC115060210, SCC115070210)
**Likely also affects:** All A4-class variants sharing the same heatsink body
(150/60-Tr VE.Can, 150/70-Tr VE.Can, 250/70-Tr VE.Can and BlueSolar equivalents)

### Description

The published STEP file specifies a nominal total heatsink width of **250mm**.
Measurement of a physical production unit in Fusion 360 yields **247mm** — a
discrepancy of **3mm**.

| Source | Total Width |
|--------|------------|
| STEP file (DimensionDrawing-SmartSolar-150_60A-&-150_70-Tr-3D.STEP) | 250mm |
| Physical unit measured in Fusion 360 | 247mm |
| Discrepancy | −3mm |

### Impact

The 3mm overstatement in the STEP file causes any accessory, bracket, or cooling
mount designed from the STEP data to be 3mm too wide. Specifically:

- The heatsink body does not reach the ends of side rails dimensioned from the STEP
- The flange mounting holes on the physical unit do not align with holes in parts
  designed to the STEP-file dimension

### Recommendation

Victron should re-measure production units and update the published STEP file for
the SmartSolar MPPT 150/60-Tr and 150/70-Tr (and all shared-body variants) to
reflect the actual manufactured dimension of 247mm.

---

## Fault 2 — STEP File Filename vs. Internal Content Mismatch

**Severity:** Medium
**File:** `SS-MPPT-250-60-70-MC4-3D.STEP`

### Description

The filename `SS-MPPT-250-60-70-MC4-3D.STEP` implies coverage of the full
SmartSolar MPPT 250/60-MC4 through 250/70-MC4 range (and by context with the
companion dimension drawing, 150/60-MC4 through 250/70-MC4).

However, the internal ISO 10303-21 FILE_NAME record within the file reads:

```
FILE_NAME('250-70-MC4-rev00', ...);
```

This identifies only the **250/70-MC4** variant, not the full 150/60–250/70 range
implied by the filename.

A separate STEP file, `DimensionDrawing-SmartSolar-150_60A-&-150_70A-MC4-3D.STEP`,
exists with internal identifier `150V45A-60A-70A-MC4-rev02`, which appears to cover
the 150V/60A and 150V/70A MC4 range specifically.

This creates ambiguity:

- Is `SS-MPPT-250-60-70-MC4` a 250V-only file that was mislabeled as a combined
  150–250V file?
- Or does it contain the 250/70-MC4 geometry that was incorrectly described as
  representative of the wider 150/60–250/70 range?

The geometry of these two STEP files appears to differ (different body configurations
and hole patterns), suggesting they represent physically distinct products.

### Impact

Third parties using the STEP files to design accessories for the 150/60-MC4 and
150/70-MC4 may select the wrong geometry depending on which file they reference.

### Recommendation

1. Clarify the internal FILE_NAME record in `SS-MPPT-250-60-70-MC4-3D.STEP` to
   accurately identify which models it covers.
2. Confirm whether the 150/60-MC4 and 150/70-MC4 share the geometry in
   `DimensionDrawing-SmartSolar-150_60A-&-150_70A-MC4-3D.STEP` (A4-type body) or
   the geometry in `SS-MPPT-250-60-70-MC4-3D.STEP` (B3-type body).
3. If they are the same product family, consolidate into a single clearly-named file;
   if physically distinct, ensure filenames and internal identifiers both clearly
   state the covered model range.

---

## Fault 3 — BlueSolar 150/60 and 150/70 Models Undocumented

**Severity:** Low–Medium
**Files:** `DimensionDrawing-BlueSolar-150_60-&-150_70-Tr-3D.STEP`
           `DimensionDrawing-BlueSolar-150_60-&-150_70-MC4-3D.STEP`

### Description

Two STEP files are published for BlueSolar variants of the 150/60 and 150/70 class:

| STEP File | Internal Identifier |
|-----------|---------------------|
| DimensionDrawing-BlueSolar-150_60-&-150_70-Tr-3D.STEP | DimensionDrawing BS 150-60-Tr - 150-70-Tr-rev01-3D.STEP |
| DimensionDrawing-BlueSolar-150_60-&-150_70-MC4-3D.STEP | DimensionDrawing BS 150-60-MC4 - 150-70-MC4-rev01-3D.STEP |

These files confirm that BlueSolar 150/60 and 150/70 products exist (both Tr and MC4
connection variants). However, **no product codes (SCC part numbers) are provided**
in available Victron documentation for these models.

The current Victron product catalog (as referenced in the VE.Direct MPPT documentation)
does not appear to list BlueSolar 150/60-Tr, BlueSolar 150/70-Tr, BlueSolar
150/60-MC4, or BlueSolar 150/70-MC4 with identifiable model codes.

### Impact

Third parties who download these STEP files have no way to cross-reference them with
specific purchasable products. Accessories or mounts designed from these files cannot
be listed against a known model number.

### Recommendation

Victron should either:
1. Publish the part numbers (SCC model codes) for the BlueSolar 150/60 and 150/70
   Tr and MC4 variants, or
2. Remove the STEP files from the public download repository if these products are
   discontinued or not available in all markets.

---

## Summary Table

| # | Fault | Severity | File(s) Affected |
|---|-------|----------|-----------------|
| 1 | A4 heatsink width 250mm (STEP) vs 247mm (physical) | High | DimensionDrawing-SmartSolar-150_60A-&-150_70-Tr-3D.STEP |
| 2 | Filename/internal-ID mismatch for MC4 STEP file | Medium | SS-MPPT-250-60-70-MC4-3D.STEP |
| 3 | BlueSolar 150/60–150/70 STEP files lack product codes | Low–Medium | DimensionDrawing-BlueSolar-150_60-*.STEP |

---

## Measurement Methodology

All STEP file analysis was performed by:

1. Parsing ISO 10303-21 CARTESIAN_POINT records to extract all geometry vertices
2. Identifying structural body wall positions from high-density vertex clusters
   (filtering out cable/connector assemblies that extend the bounding box)
3. Physical unit measurements performed in Autodesk Fusion 360 with the unit
   held in hand during caliper verification

Contact: Colin Bitterfield — colin@bitterfield.com
