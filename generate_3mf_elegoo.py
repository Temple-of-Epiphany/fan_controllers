#!/usr/bin/env python3
"""
Generate 3MF files for Elegoo Centauri Carbon 1 printer.

Author: Colin Bitterfield
Email: colin@bitterfield.com
Date Created: 2025-12-12
Version: 1.0.0

Generates deduplicated 3MF files with each containing all 4 STL components
for a specific configuration, ready for Elegoo Slicer.
"""

import subprocess
import os
import sys
from pathlib import Path
import tempfile
import shutil

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

    print(f"  Generating: {component_name}.stl")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"  Error: {e.stderr}")
        return None

def create_3mf_from_stls(stl_files, output_file, config_name):
    """
    Create a single 3MF file containing all 4 STL components.

    Note: This creates a basic 3MF. For best results, import the 3MF
    into Elegoo Slicer and arrange/configure the parts there.
    """
    try:
        import trimesh
        import numpy as np
    except ImportError:
        print("\nError: trimesh library required for 3MF generation")
        print("Install with: pip3 install trimesh numpy")
        return False

    try:
        # Load all meshes
        meshes = []
        for stl_file in stl_files:
            mesh = trimesh.load(stl_file)
            meshes.append(mesh)

        # Create a scene with all meshes
        scene = trimesh.Scene()

        # Arrange meshes in a line (you can adjust positioning)
        offset_x = 0
        for i, mesh in enumerate(meshes):
            # Position each part with some spacing
            if i > 0:
                offset_x += meshes[i-1].bounds[1][0] - meshes[i-1].bounds[0][0] + 10  # 10mm gap

            mesh.apply_translation([offset_x, 0, 0])
            scene.add_geometry(mesh, node_name=COMPONENTS[i+1])

        # Export as 3MF
        scene.export(output_file)
        return True
    except Exception as e:
        print(f"  Error creating 3MF: {e}")
        return False

def create_config_readme(output_dir):
    """Create a README with model mapping and print instructions."""
    readme_path = output_dir / "README.md"

    with open(readme_path, 'w') as f:
        f.write("# Victron MPPT Cooling Mount - Elegoo Centauri Carbon 1\n\n")
        f.write("## Print Settings Recommendations\n\n")
        f.write("**Printer:** Elegoo Centauri Carbon 1\n\n")
        f.write("**Recommended Settings:**\n")
        f.write("- **Material:** PETG or ABS (heat resistant, operating temps up to 80°C)\n")
        f.write("- **Layer Height:** 0.2mm\n")
        f.write("- **Infill:** 20-30%\n")
        f.write("- **Perimeters/Walls:** 3-4\n")
        f.write("- **Top/Bottom Layers:** 4-5\n")
        f.write("- **Supports:** None required (designed for printability)\n")
        f.write("- **Build Plate Adhesion:** Brim recommended for large parts\n\n")

        f.write("## Assembly Hardware\n\n")
        f.write("**For 50mm fan models (most controllers):**\n")
        f.write("- M4×25mm screws\n")
        f.write("- M4 nuts\n")
        f.write("- 50mm fans (40×40mm mounting pattern)\n\n")

        f.write("**For 40mm fan models (75/10-15, 100/15):**\n")
        f.write("- M3×20mm screws\n")
        f.write("- M3 nuts\n")
        f.write("- 40mm fans (30×30mm mounting pattern)\n\n")

        f.write("## Configuration Files\n\n")
        f.write("Each 3MF file contains all 4 components for a complete assembly:\n")
        f.write("1. Front fan mount plate (with fan cutouts and recessed nut wells)\n")
        f.write("2. Left mounting rail (with controller-specific mounting holes)\n")
        f.write("3. Right mounting rail (mirror of left)\n")
        f.write("4. Rear ventilation grill (honeycomb pattern)\n\n")

        f.write("## Configurations\n\n")

        for config_name, config_data in CONFIGS.items():
            f.write(f"### {config_name}\n\n")
            f.write(f"**File:** `{config_name}.3mf`\n\n")
            f.write(f"**Description:** {config_data['description']}\n\n")
            f.write("**Compatible Models:**\n")
            for model in config_data['models']:
                f.write(f"- {model}\n")
            f.write("\n")

        f.write("## Import into Elegoo Slicer\n\n")
        f.write("1. Open Elegoo Slicer\n")
        f.write("2. File → Import → Import STL/OBJ/AMF/3MF\n")
        f.write("3. Select the appropriate `.3mf` file for your controller\n")
        f.write("4. All 4 parts will be imported together\n")
        f.write("5. Arrange parts on build plate as needed\n")
        f.write("6. Configure print settings (or use saved profile)\n")
        f.write("7. Slice and print!\n\n")

    print(f"\nCreated README: {readme_path}")

def main():
    """Generate all 3MF files with all components."""
    # Find OpenSCAD executable
    openscad_cmd = find_openscad()
    print(f"Using OpenSCAD: {openscad_cmd}\n")

    # Create output directories
    output_dir = Path("output_3mf_elegoo")
    stl_temp_dir = output_dir / "temp_stls"
    output_dir.mkdir(exist_ok=True)
    stl_temp_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("Victron MPPT Cooling Mount - Elegoo Centauri Carbon 1")
    print("=" * 70)
    print(f"\nGenerating 3MF files with all 4 components per config...")
    print(f"Output directory: {output_dir.absolute()}\n")

    total_configs = len(CONFIGS)
    successful = 0

    # Generate one 3MF per configuration
    for config_name, config_data in CONFIGS.items():
        print(f"\n{'=' * 70}")
        print(f"Config: {config_name}")
        print(f"Description: {config_data['description']}")
        print(f"Models: {len(config_data['models'])}")
        print(f"{'=' * 70}")

        # Use first model as representative for this config
        representative_model = config_data['models'][0]

        # Generate all 4 STL components
        stl_files = []
        for component_num in range(1, 5):
            stl_file = generate_stl(
                representative_model,
                component_num,
                stl_temp_dir,
                config_name,
                openscad_cmd
            )
            if stl_file:
                stl_files.append(stl_file)

        # Create 3MF with all components
        if len(stl_files) == 4:
            output_3mf = output_dir / f"{config_name}.3mf"
            print(f"  Creating 3MF: {output_3mf.name}")
            if create_3mf_from_stls(stl_files, output_3mf, config_name):
                successful += 1
                print(f"  ✓ Success: {output_3mf.name}")
            else:
                print(f"  ✗ Failed to create 3MF")
        else:
            print(f"  ✗ Failed to generate all components ({len(stl_files)}/4)")

    # Clean up temp STLs
    print("\nCleaning up temporary files...")
    shutil.rmtree(stl_temp_dir)

    # Create documentation
    create_config_readme(output_dir)

    print(f"\n{'=' * 70}")
    print(f"Generation Complete")
    print(f"{'=' * 70}")
    print(f"3MF files created: {successful}/{total_configs}")
    print(f"Total models supported: {sum(len(c['models']) for c in CONFIGS.values())}")
    print(f"\nOutput location: {output_dir.absolute()}")
    print("\nImport the .3mf files into Elegoo Slicer to print!")

if __name__ == "__main__":
    main()
