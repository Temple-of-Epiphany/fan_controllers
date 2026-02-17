#!/bin/bash
#
# Generate 3MF files with printer settings using PrusaSlicer/OrcaSlicer CLI
#
# Author: Colin Bitterfield
# Email: colin@bitterfield.com
# Date Created: 2025-12-12
# Version: 1.0.0
#
# This script generates STLs from OpenSCAD, then converts to 3MF with printer settings

set -e  # Exit on error

# Configuration
OUTPUT_DIR="output_3mf"
STL_DIR="${OUTPUT_DIR}/stls"
SCAD_FILE="solar_controller_cooling_mount.scad"

# Detect slicer (PrusaSlicer or OrcaSlicer)
if command -v prusa-slicer &> /dev/null; then
    SLICER="prusa-slicer"
    echo "Found PrusaSlicer"
elif command -v orca-slicer &> /dev/null; then
    SLICER="orca-slicer"
    echo "Found OrcaSlicer"
else
    echo "Error: Neither PrusaSlicer nor OrcaSlicer found"
    echo "Install one of:"
    echo "  - PrusaSlicer: https://www.prusa3d.com/prusaslicer/"
    echo "  - OrcaSlicer: https://github.com/SoftFever/OrcaSlicer"
    exit 1
fi

# Check for OpenSCAD
if ! command -v openscad &> /dev/null; then
    echo "Error: OpenSCAD not found"
    echo "Install from: https://openscad.org/downloads.html"
    exit 1
fi

# Create output directories
mkdir -p "${STL_DIR}"
mkdir -p "${OUTPUT_DIR}/3mf"

# Printer settings (modify as needed)
MATERIAL="PETG"  # PETG or ABS for heat resistance
INFILL="20"      # 20% infill
LAYER_HEIGHT="0.2"
PERIMETERS="3"

echo "=========================================="
echo "Victron MPPT Cooling Mount 3MF Generator"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  Material: ${MATERIAL}"
echo "  Infill: ${INFILL}%"
echo "  Layer Height: ${LAYER_HEIGHT}mm"
echo "  Perimeters: ${PERIMETERS}"
echo ""

# Configuration groups (deduplicated)
declare -A CONFIGS
CONFIGS=(
    ["A1_186x122"]="SCC020030200"
    ["A3_131x91.7"]="SCC110020070R"
    ["A4_250x171"]="SCC115060210"
    ["A4_MC4_250x212.6"]="SCC115060310"
    ["B1_295x204"]="SCC115085211"
    ["B2_294.6x213.9"]="SCC115085411"
    ["B2_MC4_294.6x246"]="SCC115085511"
    ["B3_248.5x170.7"]="SCC125060221"
    ["C1_112.9x99.7"]="SCC010010050R"
    ["C2_113.9x100.7"]="SCC010015200R"
)

COMPONENTS=("front_fan_mount" "left_rail" "right_rail" "rear_grill")

# Generate STLs and convert to 3MF
total=0
successful=0

for config in "${!CONFIGS[@]}"; do
    model="${CONFIGS[$config]}"
    echo ""
    echo "Processing config: ${config}"
    echo "  Representative model: ${model}"

    for i in {1..4}; do
        component="${COMPONENTS[$((i-1))]}"
        stl_file="${STL_DIR}/${config}_${component}.stl"
        mf_file="${OUTPUT_DIR}/3mf/${config}_${component}.3mf"

        total=$((total + 1))

        # Generate STL
        echo "  Generating: ${config}_${component}.stl"
        if openscad -o "${stl_file}" \
                    -D "model_code=\"${model}\"" \
                    -D "component=${i}" \
                    "${SCAD_FILE}" 2>/dev/null; then

            # Convert to 3MF with printer settings
            echo "  Converting to 3MF with printer settings..."
            if ${SLICER} --export-3mf \
                        --load-settings \
                        --filament-type "${MATERIAL}" \
                        --fill-density "${INFILL}%" \
                        --layer-height "${LAYER_HEIGHT}" \
                        --perimeters "${PERIMETERS}" \
                        "${stl_file}" \
                        --output "${mf_file}" 2>/dev/null; then
                successful=$((successful + 1))
                echo "  ✓ Success: ${config}_${component}.3mf"
            else
                echo "  ✗ Failed to convert ${component}"
            fi
        else
            echo "  ✗ Failed to generate ${component}"
        fi
    done
done

echo ""
echo "=========================================="
echo "Generation Complete"
echo "=========================================="
echo "Total files: ${successful}/${total}"
echo "STL files: ${STL_DIR}/"
echo "3MF files: ${OUTPUT_DIR}/3mf/"
echo ""

# Create README
cat > "${OUTPUT_DIR}/README.md" <<EOF
# Victron MPPT Cooling Mount 3MF Files

Generated: $(date)

## Printer Settings

- **Material:** ${MATERIAL}
- **Infill:** ${INFILL}%
- **Layer Height:** ${LAYER_HEIGHT}mm
- **Perimeters:** ${PERIMETERS}

## Configuration Files

Each configuration includes 4 files:
1. \`*_front_fan_mount.3mf\` - Front plate with fan cutouts
2. \`*_left_rail.3mf\` - Left mounting rail
3. \`*_right_rail.3mf\` - Right mounting rail
4. \`*_rear_grill.3mf\` - Rear ventilation grill

## Configurations

EOF

# Add config descriptions
cat >> "${OUTPUT_DIR}/README.md" <<'EOF'
- **A1_186x122**: 100/30-50, 150/35-45 (8 models)
- **A3_131x91.7**: 100/20 variants (4 models)
- **A4_250x171**: 150/60-70 Tr (2 models)
- **A4_MC4_250x212.6**: 150/60-70 MC4 (2 models)
- **B1_295x204**: 150/85-100, 250/85-100 Tr (4 models)
- **B2_294.6x213.9**: Tr VE.Can variants (6 models)
- **B2_MC4_294.6x246**: MC4 VE.Can variants (4 models)
- **B3_248.5x170.7**: 250/60-70 Tr (2 models)
- **C1_112.9x99.7**: 75/10-15 (4 models)
- **C2_113.9x100.7**: 100/15 (2 models)

See CONFIG_MAPPING.md for complete model numbers.
EOF

echo "README created: ${OUTPUT_DIR}/README.md"
