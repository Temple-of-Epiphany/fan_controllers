#!/usr/bin/env python3
"""
Generate STL files for all Victron MPPT cooling mount configurations.

Author: Colin Bitterfield
Email: colin@bitterfield.com
Date Created: 2025-12-12
Version: 1.0.0

This script generates deduplicated STL files - one set per unique configuration
instead of duplicating identical models.
"""

import subprocess
import os
import sys
from pathlib import Path

# Configuration groups - models that share identical dimensions
CONFIGS = {
    "A1_186x122": {
        "models": [
            "SCC020030200", "SCC110030210", "SCC020050200", "SCC020035000",
            "SCC115045222", "SCC110050210", "SCC115035210", "SCC115045212"
        ],
        "description": "100/30-50, 150/35-45 (186×122mm, 3×50mm fans)"
    },
    "A3_131x91.7": {
        "models": [
            "SCC110020070R", "SCC110020170R", "SCC110020060R", "SCC110020160R"
        ],
        "description": "100/20 variants (131×91.7mm, 2×50mm fans)"
    },
    "A4_250x171": {
        "models": ["SCC115060210", "SCC115070210"],
        "description": "150/60-70 Tr (250×171mm, 4×50mm fans)"
    },
    "A4_MC4_250x212.6": {
        "models": ["SCC115060310", "SCC115070310"],
        "description": "150/60-70 MC4 (250×212.6mm, 4×50mm fans)"
    },
    "B1_295x204": {
        "models": [
            "SCC115085211", "SCC115110211", "SCC125085210", "SCC125110210"
        ],
        "description": "150/85-100, 250/85-100 Tr (295×204mm, 4×50mm fans)"
    },
    "B2_294.6x213.9": {
        "models": [
            "SCC115085411", "SCC115110410", "SCC115110420",
            "SCC125085411", "SCC125110411", "SCC125110441"
        ],
        "description": "150/85-100, 250/85-100 Tr VE.Can (294.6×213.9mm, 4×50mm fans)"
    },
    "B2_MC4_294.6x246": {
        "models": [
            "SCC115085511", "SCC115110511", "SCC125085511", "SCC125110512"
        ],
        "description": "150/85-100, 250/85-100 MC4 VE.Can (294.6×246mm, 4×50mm fans)"
    },
    "B3_248.5x170.7": {
        "models": ["SCC125060221", "SCC125070220"],
        "description": "250/60-70 Tr (248.5×170.7mm, 4×50mm fans)"
    },
    "C1_112.9x99.7": {
        "models": [
            "SCC010010050R", "SCC010015050R", "SCC075010060R", "SCC075015060R"
        ],
        "description": "75/10-15 (112.9×99.7mm, 2×40mm fans)"
    },
    "C2_113.9x100.7": {
        "models": ["SCC010015200R", "SCC110015060R"],
        "description": "100/15 (113.9×100.7mm, 2×40mm fans)"
    }
}

COMPONENTS = {
    1: "front_fan_mount",
    2: "left_rail",
    3: "right_rail",
    4: "rear_grill"
}

def find_openscad():
    """Find OpenSCAD executable on different platforms."""
    # Try command line first
    try:
        subprocess.run(["openscad", "--version"],
                      capture_output=True, check=True)
        return "openscad"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # macOS: Check for OpenSCAD.app
    macos_paths = [
        "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
        os.path.expanduser("~/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD")
    ]

    for path in macos_paths:
        if os.path.exists(path):
            return path

    print("Error: OpenSCAD not found!")
    print("\nPlease install OpenSCAD:")
    print("  macOS: Download from https://openscad.org/downloads.html")
    print("  Linux: sudo apt install openscad")
    print("  Windows: Download from https://openscad.org/downloads.html")
    sys.exit(1)

def generate_stl(model_code, component_num, output_dir, config_name, openscad_cmd):
    """Generate a single STL file using OpenSCAD CLI."""
    component_name = COMPONENTS[component_num]
    output_file = output_dir / f"{config_name}_{component_name}.stl"

    cmd = [
        openscad_cmd,
        "-o", str(output_file),
        "-D", f"model_code=\"{model_code}\"",
        "-D", f"component={component_num}",
        "solar_controller_cooling_mount.scad"
    ]

    print(f"Generating: {output_file.name}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating {output_file.name}: {e.stderr}")
        return False

def create_config_readme(output_dir):
    """Create a README mapping configurations to model numbers."""
    readme_path = output_dir / "CONFIG_MAPPING.md"

    with open(readme_path, 'w') as f:
        f.write("# Configuration to Model Mapping\n\n")
        f.write("This directory contains deduplicated STL files. Models with identical ")
        f.write("dimensions share the same STL files.\n\n")

        for config_name, config_data in CONFIGS.items():
            f.write(f"## {config_name}\n\n")
            f.write(f"**Description:** {config_data['description']}\n\n")
            f.write("**Compatible Models:**\n")
            for model in config_data['models']:
                f.write(f"- {model}\n")
            f.write("\n**Files:**\n")
            for component_name in COMPONENTS.values():
                f.write(f"- `{config_name}_{component_name}.stl`\n")
            f.write("\n---\n\n")

    print(f"\nCreated configuration mapping: {readme_path}")

def main():
    """Generate all STL files with deduplication."""
    # Find OpenSCAD executable
    openscad_cmd = find_openscad()
    print(f"Using OpenSCAD: {openscad_cmd}\n")

    # Create output directory
    output_dir = Path("output_stls")
    output_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("Victron MPPT Cooling Mount STL Generator")
    print("=" * 70)
    print(f"\nGenerating deduplicated STL files...")
    print(f"Output directory: {output_dir.absolute()}\n")

    total_files = 0
    successful = 0

    # Generate one set of STLs per configuration
    for config_name, config_data in CONFIGS.items():
        print(f"\n{'=' * 70}")
        print(f"Config: {config_name}")
        print(f"Description: {config_data['description']}")
        print(f"Models: {len(config_data['models'])}")
        print(f"{'=' * 70}")

        # Use first model as representative for this config
        representative_model = config_data['models'][0]

        # Generate all 4 components
        for component_num in range(1, 5):
            total_files += 1
            if generate_stl(representative_model, component_num, output_dir, config_name, openscad_cmd):
                successful += 1

    # Create mapping documentation
    create_config_readme(output_dir)

    print(f"\n{'=' * 70}")
    print(f"Generation complete!")
    print(f"{'=' * 70}")
    print(f"Total files generated: {successful}/{total_files}")
    print(f"Total unique configurations: {len(CONFIGS)}")
    print(f"Total models supported: {sum(len(c['models']) for c in CONFIGS.values())}")
    print(f"\nOutput location: {output_dir.absolute()}")

if __name__ == "__main__":
    main()
