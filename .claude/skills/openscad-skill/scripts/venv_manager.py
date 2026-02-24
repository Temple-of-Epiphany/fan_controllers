#!/usr/bin/env python3
"""
File:        venv_manager.py
Author:      Colin Bitterfield
Email:       colin@bitterfield.com
Created:     2025-02-21
Updated:     2025-02-21
Version:     1.0.0

Description:
    Manages a per-skill Python virtual environment for isolated dependency
    installation. Handles creation, activation (subprocess-level), package
    installation, and teardown. Designed for macOS 26.x with MacPorts
    Python as the preferred base interpreter.

    Venv location: ~/.local/share/claude-skills/<skill_name>/.venv
    This location is persistent across sessions (packages survive).
    The venv is NOT deleted on teardown — teardown only means we're
    done using it this session. Use --destroy for full removal.

Usage (CLI):
    python3 venv_manager.py setup   [--skill NAME] [--packages pkg1 pkg2 ...]
    python3 venv_manager.py python  [--skill NAME] -- script.py [args]
    python3 venv_manager.py run     [--skill NAME] -- command [args]
    python3 venv_manager.py info    [--skill NAME]
    python3 venv_manager.py destroy [--skill NAME]

Usage (as library):
    from scripts.venv_manager import VenvManager

    vm = VenvManager("3mf")
    vm.setup(["lib3mf", "trimesh", "numpy"])
    result = vm.run_python("my_script.py", ["--input", "model.stl"])
    # No explicit teardown needed — venv persists for reuse

Changelog:
    1.0.0 - Initial version
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

VENV_BASE    = Path.home() / ".local" / "share" / "claude-skills"
STATE_FILE   = "venv_state.json"

# Preferred Python interpreters in priority order (macOS 26 / MacPorts first)
PYTHON_CANDIDATES = [
    "/opt/local/bin/python3.12",   # MacPorts Python 3.12
    "/opt/local/bin/python3.11",   # MacPorts Python 3.11
    "/opt/local/bin/python3",      # MacPorts default
    "/opt/homebrew/bin/python3.12",
    "/opt/homebrew/bin/python3",
    "/usr/local/bin/python3",
    "/usr/bin/python3",
    sys.executable,                # fallback: whatever's running this script
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _find_python() -> str:
    """Return path to the best available Python 3 interpreter."""
    for candidate in PYTHON_CANDIDATES:
        if Path(candidate).exists() and os.access(candidate, os.X_OK):
            return candidate
    # Last resort: shutil.which
    found = shutil.which("python3") or shutil.which("python")
    if found:
        return found
    raise RuntimeError("No Python 3 interpreter found on this system.")


def _venv_dir(skill_name: str) -> Path:
    return VENV_BASE / skill_name / ".venv"


def _venv_python(skill_name: str) -> str:
    return str(_venv_dir(skill_name) / "bin" / "python3")


def _venv_pip(skill_name: str) -> str:
    return str(_venv_dir(skill_name) / "bin" / "pip3")


def _state_path(skill_name: str) -> Path:
    return VENV_BASE / skill_name / STATE_FILE


def _load_state(skill_name: str) -> dict:
    p = _state_path(skill_name)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def _save_state(skill_name: str, state: dict) -> None:
    p = _state_path(skill_name)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2))


# ── Core class ────────────────────────────────────────────────────────────────

class VenvManager:
    """
    Manages a persistent virtual environment for a named skill.

    The venv lives at ~/.local/share/claude-skills/<skill_name>/.venv
    and survives across sessions. Packages are only installed if not
    already present (checked via pip list + state file).
    """

    def __init__(self, skill_name: str, verbose: bool = False):
        self.skill_name = skill_name
        self.verbose    = verbose
        self.venv_path  = _venv_dir(skill_name)
        self.python     = _venv_python(skill_name)
        self.pip        = _venv_pip(skill_name)

    # ── Setup ─────────────────────────────────────────────────────────────

    def setup(self, packages: list[str] | None = None) -> None:
        """
        Create the venv if needed, then install any missing packages.

        Args:
            packages: List of pip package specs to ensure are installed.
                      E.g. ["lib3mf", "trimesh>=3.0", "numpy"].
        """
        self._create_if_needed()
        if packages:
            self._install_packages(packages)
        if self.verbose:
            print(f"[venv] Ready: {self.venv_path}", file=sys.stderr)

    def _create_if_needed(self) -> None:
        python_bin = self.venv_path / "bin" / "python3"
        if python_bin.exists():
            if self.verbose:
                print(f"[venv] Exists: {self.venv_path}", file=sys.stderr)
            return

        base_python = _find_python()
        if self.verbose:
            print(f"[venv] Creating with {base_python} ...", file=sys.stderr)

        self.venv_path.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [base_python, "-m", "venv", str(self.venv_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to create venv at {self.venv_path}:\n{result.stderr}"
            )

        # Upgrade pip silently
        subprocess.run(
            [self.python, "-m", "pip", "install", "--upgrade", "pip", "-q"],
            capture_output=True
        )

        state = _load_state(self.skill_name)
        state["created"] = True
        state["base_python"] = base_python
        state["installed_packages"] = []
        _save_state(self.skill_name, state)
        print(f"[venv] Created: {self.venv_path}", file=sys.stderr)

    def _install_packages(self, packages: list[str]) -> None:
        state    = _load_state(self.skill_name)
        existing = set(state.get("installed_packages", []))
        needed   = [p for p in packages if p.split(">=")[0].split("==")[0] not in existing]

        if not needed:
            if self.verbose:
                print("[venv] All packages already installed.", file=sys.stderr)
            return

        print(f"[venv] Installing: {', '.join(needed)}", file=sys.stderr)
        result = subprocess.run(
            [self.pip, "install", "-q"] + needed,
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"pip install failed:\n{result.stderr}"
            )

        # Record installed
        state["installed_packages"] = list(existing | set(p.split(">=")[0].split("==")[0]
                                                           for p in needed))
        _save_state(self.skill_name, state)

    # ── Run ───────────────────────────────────────────────────────────────

    def run_python(
        self,
        script: str,
        args: list[str] | None = None,
        capture: bool = False,
        cwd: str | None = None,
    ) -> subprocess.CompletedProcess:
        """
        Run a Python script inside the venv.

        Args:
            script:  Path to .py script.
            args:    Additional CLI arguments.
            capture: If True, capture stdout/stderr. If False, inherit stdio.
            cwd:     Working directory for the subprocess.
        """
        cmd = [self.python, script] + (args or [])
        if self.verbose:
            print(f"[venv] {' '.join(cmd)}", file=sys.stderr)
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=capture,
            cwd=cwd,
        )

    def run_module(
        self,
        module: str,
        args: list[str] | None = None,
        capture: bool = False,
        cwd: str | None = None,
    ) -> subprocess.CompletedProcess:
        """Run a Python module (-m) inside the venv."""
        cmd = [self.python, "-m", module] + (args or [])
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=capture,
            cwd=cwd,
        )

    def python_code(self, code: str, capture: bool = True) -> subprocess.CompletedProcess:
        """Execute a Python code string inside the venv via -c."""
        return subprocess.run(
            [self.python, "-c", code],
            capture_output=capture, text=capture
        )

    # ── Info ──────────────────────────────────────────────────────────────

    def info(self) -> dict:
        """Return info dict about this venv."""
        exists = (self.venv_path / "bin" / "python3").exists()
        state  = _load_state(self.skill_name) if exists else {}
        return {
            "skill":      self.skill_name,
            "venv_path":  str(self.venv_path),
            "exists":     exists,
            "python":     self.python if exists else None,
            "packages":   state.get("installed_packages", []),
            "base_python":state.get("base_python"),
        }

    def print_info(self) -> None:
        info = self.info()
        print(f"Skill:      {info['skill']}")
        print(f"Venv:       {info['venv_path']}")
        print(f"Exists:     {info['exists']}")
        if info["exists"]:
            print(f"Python:     {info['python']}")
            print(f"Base:       {info['base_python']}")
            print(f"Packages:   {', '.join(info['packages']) or '(none recorded)'}")

    # ── Destroy ───────────────────────────────────────────────────────────

    def destroy(self) -> None:
        """
        Permanently remove the venv directory and state file.
        Use when packages need to be rebuilt from scratch.
        """
        if self.venv_path.exists():
            shutil.rmtree(str(self.venv_path))
            print(f"[venv] Removed: {self.venv_path}", file=sys.stderr)
        state_p = _state_path(self.skill_name)
        if state_p.exists():
            state_p.unlink()
        skill_dir = VENV_BASE / self.skill_name
        if skill_dir.exists() and not any(skill_dir.iterdir()):
            skill_dir.rmdir()


# ── Convenience context manager ───────────────────────────────────────────────

class ManagedVenv:
    """
    Context manager that sets up the venv on enter and does nothing on exit
    (venv persists). Raises on setup failure.

    Usage:
        with ManagedVenv("3mf", packages=["lib3mf", "trimesh"]) as vm:
            vm.run_python("my_script.py")
    """
    def __init__(self, skill_name: str, packages: list[str] | None = None,
                 verbose: bool = False):
        self.vm       = VenvManager(skill_name, verbose=verbose)
        self.packages = packages

    def __enter__(self) -> VenvManager:
        self.vm.setup(self.packages)
        return self.vm

    def __exit__(self, *_):
        # Venv is persistent — nothing to tear down
        pass


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Manage a per-skill Python venv")
    parser.add_argument("command", choices=["setup", "python", "run", "info", "destroy"])
    parser.add_argument("--skill",    default="default", help="Skill name (default: 'default')")
    parser.add_argument("--packages", nargs="*", default=[], help="Packages to install")
    parser.add_argument("--verbose",  action="store_true")
    parser.add_argument("rest", nargs=argparse.REMAINDER,
                        help="After '--': script/command and its arguments")
    args = parser.parse_args()

    # Strip leading '--' from remainder
    rest = args.rest
    if rest and rest[0] == "--":
        rest = rest[1:]

    vm = VenvManager(args.skill, verbose=args.verbose)

    if args.command == "setup":
        vm.setup(args.packages or [])
        print(f"Venv ready: {vm.venv_path}")

    elif args.command == "python":
        vm.setup()
        if not rest:
            print("ERROR: Provide a script path after '--'", file=sys.stderr)
            sys.exit(1)
        r = vm.run_python(rest[0], rest[1:])
        sys.exit(r.returncode)

    elif args.command == "run":
        vm.setup()
        if not rest:
            print("ERROR: Provide a command after '--'", file=sys.stderr)
            sys.exit(1)
        # Replace first token with venv-local binary if it exists
        cmd_name = rest[0]
        venv_bin = vm.venv_path / "bin" / cmd_name
        cmd = [str(venv_bin) if venv_bin.exists() else cmd_name] + rest[1:]
        r = subprocess.run(cmd)
        sys.exit(r.returncode)

    elif args.command == "info":
        vm.print_info()

    elif args.command == "destroy":
        confirm = input(f"Destroy venv at {vm.venv_path}? [y/N] ").strip().lower()
        if confirm == "y":
            vm.destroy()
        else:
            print("Aborted.")


if __name__ == "__main__":
    main()
