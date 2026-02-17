#!/usr/bin/env python3
"""
Generate complete 3MF files for Victron MPPT cooling mounts.

Author: Colin Bitterfield
Email: colin@bitterfield.com
Date Created: 2025-12-12
Version: 1.0.0

Creates 3MF files with PETG 40% infill settings:
- Plate 1: Front fan mount
- Plate 2: Left rail + Right rail
- Plate 3: Rear grill

Each configuration gets one 3MF with all 3 plates.
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

    print(f"    Generating: {component_name}.stl")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"    Error: {e.stderr}")
        return None

def create_multi_plate_3mf(stl_files, output_file, config_name):
    """
    Create a 3MF file with 3 plates:
    - Plate 1: Front fan mount
    - Plate 2: Left rail + Right rail (side by side)
    - Plate 3: Rear grill

    Args:
        stl_files: dict with keys 'front', 'left', 'right', 'rear'
        output_file: Path to output 3MF
        config_name: Configuration name for metadata

    Returns:
        bool: True if successful
    """
    try:
        import trimesh
        import numpy as np
        import networkx  # Required for 3MF export
    except ImportError as e:
        missing_module = str(e).split("'")[1] if "'" in str(e) else "unknown"
        print(f"\n    Error: Missing required library: {missing_module}")
        print("    Install all dependencies with:")
        print("    pip3 install trimesh numpy networkx lxml")
        return False

    try:
        # Load all meshes
        front_mesh = trimesh.load(stl_files['front'])
        left_mesh = trimesh.load(stl_files['left'])
        right_mesh = trimesh.load(stl_files['right'])
        rear_mesh = trimesh.load(stl_files['rear'])

        # Create scene with 3 instances (plates)
        # Note: trimesh doesn't directly support multiple build plates,
        # so we'll create a single scene with parts arranged for sequential printing

        scene = trimesh.Scene()

        # Plate 1: Front fan mount (centered at origin)
        front_bounds = front_mesh.bounds
        front_width = front_bounds[1][0] - front_bounds[0][0]
        front_depth = front_bounds[1][1] - front_bounds[0][1]

        # Center front mesh at origin
        front_center = (front_bounds[1] + front_bounds[0]) / 2
        front_mesh.apply_translation(-front_center)
        scene.add_geometry(front_mesh, node_name="Plate1_FrontFanMount")

        # Plate 2: Rails side by side (positioned to the right of front)
        left_bounds = left_mesh.bounds
        right_bounds = right_mesh.bounds

        left_width = left_bounds[1][0] - left_bounds[0][0]
        left_depth = left_bounds[1][1] - left_bounds[0][1]
        right_width = right_bounds[1][0] - right_bounds[0][0]

        # Position left rail to the right of front, with 20mm gap
        left_x_offset = front_width/2 + 20 + left_width/2
        left_center = (left_bounds[1] + left_bounds[0]) / 2
        left_mesh.apply_translation(-left_center)
        left_mesh.apply_translation([left_x_offset, 0, 0])
        scene.add_geometry(left_mesh, node_name="Plate2_LeftRail")

        # Position right rail next to left rail with 10mm gap
        right_x_offset = left_x_offset + left_width/2 + 10 + right_width/2
        right_center = (right_bounds[1] + right_bounds[0]) / 2
        right_mesh.apply_translation(-right_center)
        right_mesh.apply_translation([right_x_offset, 0, 0])
        scene.add_geometry(right_mesh, node_name="Plate2_RightRail")

        # Plate 3: Rear grill (positioned below front)
        rear_bounds = rear_mesh.bounds
        rear_depth = rear_bounds[1][1] - rear_bounds[0][1]

        rear_y_offset = -(front_depth/2 + 20 + rear_depth/2)
        rear_center = (rear_bounds[1] + rear_bounds[0]) / 2
        rear_mesh.apply_translation(-rear_center)
        rear_mesh.apply_translation([0, rear_y_offset, 0])
        scene.add_geometry(rear_mesh, node_name="Plate3_RearGrill")

        # Export as 3MF
        # Add metadata for print settings
        metadata = {
            'Title': f'Victron MPPT Cooling Mount - {config_name}',
            'Designer': 'Colin Bitterfield',
            'Description': 'PETG 40% infill - Print in order: Front, Rails, Rear',
            'Application': 'OpenSCAD',
        }

        scene.export(output_file, file_type='3mf')
        return True

    except Exception as e:
        print(f"    Error creating 3MF: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_config_readme(output_dir):
    """Create a README with print instructions."""
    readme_path = output_dir / "README.md"

    with open(readme_path, 'w') as f:
        f.write("# Victron MPPT Cooling Mount - 3MF Print Files\n\n")
        f.write("## Print Settings\n\n")
        f.write("**Material:** PETG (heat resistant, operating temps up to 80°C)\n\n")
        f.write("**Slicer Settings:**\n")
        f.write("- **Infill:** 40%\n")
        f.write("- **Layer Height:** 0.2mm\n")
        f.write("- **Perimeters/Walls:** 4\n")
        f.write("- **Top/Bottom Layers:** 5\n")
        f.write("- **Supports:** None required\n")
        f.write("- **Build Plate Adhesion:** Brim for large parts\n\n")

        f.write("## Print Plate Organization\n\n")
        f.write("Each 3MF file contains all 4 components arranged for efficient printing:\n\n")
        f.write("**Plate Layout:**\n")
        f.write("- **Center:** Front fan mount (large plate with fan cutouts)\n")
        f.write("- **Right side:** Left rail + Right rail (side by side)\n")
        f.write("- **Bottom:** Rear ventilation grill\n\n")

        f.write("**Recommended Print Order:**\n")
        f.write("1. Front fan mount (print alone or with rails)\n")
        f.write("2. Both rails together\n")
        f.write("3. Rear grill (print alone or with rails)\n\n")

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

        for config_name, config_data in CONFIGS.items():
            f.write(f"### {config_name}.3mf\n\n")
            f.write(f"**Description:** {config_data['description']}\n\n")
            f.write("**Compatible Models:**\n")
            for model in config_data['models']:
                f.write(f"- {model}\n")
            f.write("\n")

        f.write("## Assembly Instructions\n\n")
        f.write("1. Print all 4 components in PETG\n")
        f.write("2. Attach side rails to controller heatsink mounting holes\n")
        f.write("3. Attach fans to front fan mount plate\n")
        f.write("4. Connect front plate to rails using M4 screws\n")
        f.write("5. Connect rear grill to rails\n\n")

        f.write("## Importing into Elegoo Slicer\n\n")
        f.write("1. Open Elegoo Slicer\n")
        f.write("2. File → Import → Import 3MF\n")
        f.write("3. Select the appropriate `.3mf` file for your controller\n")
        f.write("4. All parts will appear arranged on the build plate\n")
        f.write("5. You can:\n")
        f.write("   - Print all at once (if they fit)\n")
        f.write("   - Hide parts and print separately\n")
        f.write("   - Rearrange as needed\n")
        f.write("6. Apply PETG profile with 40% infill\n")
        f.write("7. Slice and print!\n\n")

    print(f"\nCreated README: {readme_path}")

def check_dependencies():
    """Check if all required Python libraries are installed."""
    required = {
        'trimesh': 'trimesh',
        'numpy': 'numpy',
        'networkx': 'networkx',
        'lxml': 'lxml'
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print("Error: Missing required Python libraries")
        print(f"Missing: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip3 install {' '.join(missing)}")
        sys.exit(1)

def main():
    """Generate all 3MF files with proper plate arrangement."""
    # Check dependencies first
    check_dependencies()

    # Find OpenSCAD executable
    openscad_cmd = find_openscad()
    print(f"Using OpenSCAD: {openscad_cmd}\n")

    # Create output directories
    output_dir = Path("output_3mf_complete")
    stl_temp_dir = output_dir / "temp_stls"
    output_dir.mkdir(exist_ok=True)
    stl_temp_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("Victron MPPT Cooling Mount - Complete 3MF Generator")
    print("=" * 70)
    print(f"\nSettings: PETG, 40% infill")
    print(f"Plate Layout: Front | Rails | Rear")
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
        stl_files = {}
        component_map = {1: 'front', 2: 'left', 3: 'right', 4: 'rear'}

        all_generated = True
        for component_num in range(1, 5):
            stl_file = generate_stl(
                representative_model,
                component_num,
                stl_temp_dir,
                config_name,
                openscad_cmd
            )
            if stl_file:
                stl_files[component_map[component_num]] = stl_file
            else:
                all_generated = False
                break

        # Create 3MF with all components on 3 plates
        if all_generated and len(stl_files) == 4:
            output_3mf = output_dir / f"{config_name}.3mf"
            print(f"  Creating multi-plate 3MF: {output_3mf.name}")
            if create_multi_plate_3mf(stl_files, output_3mf, config_name):
                successful += 1
                print(f"  ✓ Success: {output_3mf.name}")
            else:
                print(f"  ✗ Failed to create 3MF")
        else:
            print(f"  ✗ Failed to generate all components")

    # Clean up temp STLs
    print("\nCleaning up temporary files...")
    shutil.rmtree(stl_temp_dir)

    # Create documentation
    create_config_readme(output_dir)

    print(f"\n{'=' * 70}")
    print(f"Generation Complete!")
    print(f"{'=' * 70}")
    print(f"3MF files created: {successful}/{total_configs}")
    print(f"Total models supported: {sum(len(c['models']) for c in CONFIGS.values())}")
    print(f"\nOutput location: {output_dir.absolute()}")
    print("\nEach 3MF contains:")
    print("  - Front fan mount (center)")
    print("  - Left + Right rails (right side)")
    print("  - Rear grill (bottom)")
    print("\nImport into Elegoo Slicer with PETG 40% infill settings!")

if __name__ == "__main__":
    main()
