#!/usr/bin/env python3
"""
Convert STL files to 3MF format with optional printer settings.

Author: Colin Bitterfield
Email: colin@bitterfield.com
Date Created: 2025-12-12
Version: 1.0.0

Requires: trimesh, numpy
Install: pip install trimesh numpy

For printer settings integration, use PrusaSlicer/OrcaSlicer CLI instead.
"""

import sys
from pathlib import Path

try:
    import trimesh
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install trimesh numpy")
    sys.exit(1)

def stl_to_3mf(stl_path, output_path):
    """
    Convert STL to 3MF format.

    Args:
        stl_path: Path to input STL file
        output_path: Path to output 3MF file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load STL mesh
        mesh = trimesh.load(stl_path)

        # Export as 3MF
        mesh.export(output_path)

        return True
    except Exception as e:
        print(f"Error converting {stl_path.name}: {e}")
        return False

def batch_convert_directory(input_dir, output_dir=None):
    """
    Convert all STL files in a directory to 3MF.

    Args:
        input_dir: Directory containing STL files
        output_dir: Output directory (defaults to input_dir/3mf)
    """
    input_path = Path(input_dir)

    if output_dir is None:
        output_path = input_path / "3mf"
    else:
        output_path = Path(output_dir)

    output_path.mkdir(exist_ok=True)

    # Find all STL files
    stl_files = list(input_path.glob("*.stl"))

    if not stl_files:
        print(f"No STL files found in {input_path}")
        return

    print(f"Found {len(stl_files)} STL files")
    print(f"Output directory: {output_path.absolute()}\n")

    successful = 0
    for stl_file in stl_files:
        output_file = output_path / f"{stl_file.stem}.3mf"
        print(f"Converting: {stl_file.name} -> {output_file.name}")

        if stl_to_3mf(stl_file, output_file):
            successful += 1

    print(f"\n{'=' * 70}")
    print(f"Conversion complete: {successful}/{len(stl_files)} successful")
    print(f"Output location: {output_path.absolute()}")

def print_usage():
    """Print usage instructions."""
    print("""
Usage:
    # Convert single file
    python3 convert_to_3mf.py input.stl output.3mf

    # Convert all STL files in directory
    python3 convert_to_3mf.py input_directory/

    # Convert with custom output directory
    python3 convert_to_3mf.py input_directory/ output_directory/

Note: This creates basic 3MF files without printer settings.
For printer settings, use PrusaSlicer/OrcaSlicer CLI:

    # Example with PrusaSlicer
    prusa-slicer --export-3mf --load config.ini input.stl --output output.3mf

    # Example with OrcaSlicer
    orca-slicer --export-3mf --load config.json input.stl --output output.3mf
""")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    input_arg = sys.argv[1]
    input_path = Path(input_arg)

    if not input_path.exists():
        print(f"Error: {input_path} does not exist")
        sys.exit(1)

    # Directory conversion
    if input_path.is_dir():
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        batch_convert_directory(input_path, output_dir)

    # Single file conversion
    else:
        if len(sys.argv) < 3:
            output_path = input_path.with_suffix('.3mf')
        else:
            output_path = Path(sys.argv[2])

        print(f"Converting: {input_path.name} -> {output_path.name}")
        if stl_to_3mf(input_path, output_path):
            print(f"Success! Output: {output_path.absolute()}")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
