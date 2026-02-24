#!/usr/bin/env python3
"""
File:        openscad_runner.py
Author:      Colin Bitterfield
Email:       colin@bitterfield.com
Created:     2025-02-21
Updated:     2025-02-21
Version:     1.1.0

Description:
    Wrapper for running OpenSCAD CLI operations from Python scripts.
    Handles binary discovery via find_openscad.py, constructs render
    commands, and reports errors clearly.

    This script has no pip dependencies and runs in the base Python
    interpreter. It does not need the venv. The venv (managed by
    venv_manager.py) is only required for scripts that use lib3mf
    or trimesh (e.g., 3MF post-processing).

Usage (as a library):
    from openscad_runner import OpenSCADRunner

    runner = OpenSCADRunner()          # auto-discovers binary
    runner.render("model.scad", "model.stl", binary_stl=True)
    runner.render("model.scad", "model.3mf", variables={"width": 80})
    runner.render_batch("model.scad", variants=[
        {"name": "small",  "variables": {"box_w": 40}},
        {"name": "medium", "variables": {"box_w": 60}},
    ], fmt="3mf", output_dir="./output")

Usage (CLI):
    python3 openscad_runner.py model.scad model.stl
    python3 openscad_runner.py model.scad model.3mf -D box_w=80
    python3 openscad_runner.py model.scad model.3mf --color-mode none -v

Changelog:
    1.1.0 - Clarified venv usage scope; no changes to logic
    1.0.0 - Initial version
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ── Binary discovery ─────────────────────────────────────────────────────────

def _find_binary(required: bool = True) -> Optional[str]:
    """
    Locate the OpenSCAD binary using find_openscad.py.
    Returns the path string, or None if not found (when required=False).
    Raises RuntimeError with installation instructions if required=True.
    """
    script = Path(__file__).parent / "find_openscad.py"
    result = subprocess.run(
        [sys.executable, str(script), "--json"],
        capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        if data.get("found"):
            return data["path"]
    except (json.JSONDecodeError, KeyError):
        pass

    if required:
        raise RuntimeError(
            "OpenSCAD binary not found.\n"
            "Run: python3 find_openscad.py  to see installation instructions.\n"
            "Or:  python3 find_openscad.py --set /path/to/OpenSCAD  to set manually."
        )
    return None


# ── Runner class ─────────────────────────────────────────────────────────────

class OpenSCADRunner:
    """
    High-level interface for OpenSCAD CLI operations.

    Attributes:
        binary (str): Path to the OpenSCAD executable.
        verbose (bool): If True, print the full command before running.
    """

    def __init__(self, binary: Optional[str] = None, verbose: bool = False):
        """
        Args:
            binary: Explicit path to OpenSCAD binary. If None, auto-discovers.
            verbose: Print commands before execution.
        """
        self.binary  = binary or _find_binary(required=True)
        self.verbose = verbose

    def version(self) -> str:
        """Return the OpenSCAD version string."""
        result = subprocess.run(
            [self.binary, "--version"],
            capture_output=True, text=True, timeout=10
        )
        return (result.stdout + result.stderr).strip()

    def render(
        self,
        scad_file: str,
        output_file: str,
        variables: Optional[dict] = None,
        param_file: Optional[str] = None,
        param_set:  Optional[str] = None,
        binary_stl: bool = True,
        color_mode: str = "none",
        export_settings: Optional[dict] = None,
        quiet: bool = True,
        force_render: bool = False,
    ) -> subprocess.CompletedProcess:
        """
        Render a .scad file to the specified output format.

        Format is determined by the output file extension:
          .stl  → STL (binary by default)
          .3mf  → 3MF
          .svg  → SVG (2D)
          .dxf  → DXF (2D)
          .png  → PNG image
          .off  → OFF mesh

        Args:
            scad_file:       Path to the .scad source file.
            output_file:     Path for the output file (extension sets format).
            variables:       Dict of variable overrides  {name: value}.
            param_file:      Path to Customizer JSON parameter file.
            param_set:       Named parameter set to use from param_file.
            binary_stl:      If True (default), export binary STL not ASCII.
            color_mode:      3MF color mode: "none", "model", "selected-only".
            export_settings: Dict of -O key=value settings.
            quiet:           If True, suppress OpenSCAD info output (-q).
            force_render:    If True, add --render flag (full CGAL render).

        Returns:
            subprocess.CompletedProcess
        """
        cmd = [self.binary, "-o", output_file]

        # Format flags
        ext = Path(output_file).suffix.lower()
        if ext == ".stl" and binary_stl:
            cmd += ["--export-format", "binstl"]

        # Variable overrides
        for name, value in (variables or {}).items():
            if isinstance(value, str):
                cmd += ["-D", f'{name}="{value}"']
            elif isinstance(value, bool):
                cmd += ["-D", f"{name}={'true' if value else 'false'}"]
            else:
                cmd += ["-D", f"{name}={value}"]

        # Parameter file / set
        if param_file:
            cmd += ["-p", param_file]
        if param_set:
            cmd += ["-P", param_set]

        # 3MF-specific -O settings
        if ext == ".3mf":
            # Default: no embedded color (portable across slicers)
            settings = {"export-3mf/color-mode": color_mode}
            settings.update(export_settings or {})
            for k, v in settings.items():
                cmd += ["-O", f"{k}={v}"]
        elif export_settings:
            for k, v in (export_settings or {}).items():
                cmd += ["-O", f"{k}={v}"]

        # Flags
        if force_render:
            cmd.append("--render")
        if quiet:
            cmd.append("-q")

        # Source file last
        cmd.append(scad_file)

        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        if self.verbose:
            print("CMD:", " ".join(str(c) for c in cmd))

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(
                f"OpenSCAD failed (exit {result.returncode}):\n"
                f"  Command: {' '.join(str(c) for c in cmd)}\n"
                f"  stderr:  {result.stderr.strip()}"
            )

        return result

    def render_batch(
        self,
        scad_file: str,
        variants: list[dict],
        fmt: str = "3mf",
        output_dir: str = ".",
        name_key: str = "name",
        verbose: bool = False,
    ) -> list[str]:
        """
        Render multiple variants of a model.

        Args:
            scad_file:   Path to the .scad source.
            variants:    List of dicts, each with:
                           "name"      → output filename stem (required)
                           "variables" → dict of -D overrides (optional)
                           "param_set" → named param set from param_file (optional)
            fmt:         Output format extension without dot ("stl", "3mf", etc.)
            output_dir:  Directory for output files.
            name_key:    Key in each variant dict used as the output filename stem.
            verbose:     Print progress.

        Returns:
            List of output file paths.
        """
        fmt = fmt.lstrip(".")
        outputs = []

        for i, variant in enumerate(variants):
            stem     = variant.get(name_key, f"variant_{i:03d}")
            out_file = str(Path(output_dir) / f"{stem}.{fmt}")

            if verbose:
                print(f"[{i+1}/{len(variants)}] Rendering {stem}.{fmt} ...")

            self.render(
                scad_file   = scad_file,
                output_file = out_file,
                variables   = variant.get("variables"),
                param_set   = variant.get("param_set"),
                quiet       = not verbose,
            )
            outputs.append(out_file)
            if verbose:
                print(f"  → {out_file}")

        return outputs


# ── CLI convenience wrapper ──────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Render an OpenSCAD file to STL or 3MF"
    )
    parser.add_argument("scad",   help="Input .scad file")
    parser.add_argument("output", help="Output file (.stl, .3mf, .svg, .png, ...)")
    parser.add_argument("-D", "--define", action="append", metavar="VAR=VAL",
                        default=[], help="Variable override (repeatable)")
    parser.add_argument("-p", "--param-file", help="Customizer parameter JSON file")
    parser.add_argument("-P", "--param-set",  help="Parameter set name from JSON file")
    parser.add_argument("--ascii-stl", action="store_true",
                        help="Export ASCII STL instead of binary")
    parser.add_argument("--color-mode", default="none",
                        choices=["none", "model", "selected-only"],
                        help="3MF color mode (default: none)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    # Parse -D VAR=VAL pairs
    variables = {}
    for kv in args.define:
        if "=" in kv:
            k, v = kv.split("=", 1)
            # Try numeric conversion
            try:    variables[k] = int(v)
            except ValueError:
                try:    variables[k] = float(v)
                except ValueError:
                    variables[k] = v
        else:
            print(f"WARNING: Ignoring malformed -D value: {kv}", file=sys.stderr)

    runner = OpenSCADRunner(verbose=args.verbose)
    print(f"OpenSCAD: {runner.binary}", file=sys.stderr)

    runner.render(
        scad_file   = args.scad,
        output_file = args.output,
        variables   = variables,
        param_file  = args.param_file,
        param_set   = args.param_set,
        binary_stl  = not args.ascii_stl,
        color_mode  = args.color_mode,
        verbose     = args.verbose,
    )
    print(f"Written: {args.output}")
