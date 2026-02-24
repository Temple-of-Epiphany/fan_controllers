#!/usr/bin/env python3
"""
File:        find_openscad.py
Author:      Colin Bitterfield
Email:       colin@bitterfield.com
Created:     2025-02-21
Updated:     2025-02-21
Version:     1.0.0

Description:
    Locates the OpenSCAD command-line binary on macOS 26.x (and earlier).
    Searches in order:
      1. Cached path in ~/.config/openscad_skill/config.json
      2. OPENSCAD_BIN environment variable
      3. PATH (via `which`)
      4. Spotlight / mdfind — finds all installed .app bundles by bundle ID
      5. Known fixed locations (DMG, Homebrew, MacPorts, snapshot)

    If a binary is found, its path is printed and cached for future calls.
    If nothing is found, exits with code 1 and a human-readable message so
    Claude can ask the user where OpenSCAD is installed.

Usage:
    python3 find_openscad.py              # discover and print binary path
    python3 find_openscad.py --verify     # also run `openscad --version`
    python3 find_openscad.py --set PATH   # manually cache a binary path
    python3 find_openscad.py --clear      # clear cached path
    python3 find_openscad.py --json       # output JSON result

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

# ── Configuration ────────────────────────────────────────────────────────────

CONFIG_DIR  = Path.home() / ".config" / "openscad_skill"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Bundle identifier used by the macOS .app
BUNDLE_ID = "org.openscad.OpenSCAD"

# Known fixed paths, checked in priority order
KNOWN_PATHS = [
    # Standard DMG install — classic .app bundle form
    "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
    # Non-bundle install — some DMG/pkg installers drop a plain folder
    "/Applications/OpenSCAD/Contents/MacOS/OpenSCAD",
    "/Applications/OpenSCAD/OpenSCAD",
    # Development snapshot — bundle form
    "/Applications/OpenSCAD-snapshot.app/Contents/MacOS/OpenSCAD",
    # Non-bundle snapshot folder
    "/Applications/OpenSCAD-snapshot/Contents/MacOS/OpenSCAD",
    "/Applications/OpenSCAD-snapshot/OpenSCAD",
    # Nightly / date-stamped snapshot (glob handled separately)
    # Homebrew — Apple Silicon (macOS 26 default)
    "/opt/homebrew/bin/openscad",
    "/opt/homebrew/Caskroom/openscad/current/OpenSCAD.app/Contents/MacOS/OpenSCAD",
    # Homebrew — Intel Mac
    "/usr/local/bin/openscad",
    "/usr/local/Caskroom/openscad/current/OpenSCAD.app/Contents/MacOS/OpenSCAD",
    # MacPorts
    "/opt/local/bin/openscad",
    # Snapshot cask (homebrew)
    "/opt/homebrew/Caskroom/openscad@snapshot/current/OpenSCAD.app/Contents/MacOS/OpenSCAD",
    "/usr/local/Caskroom/openscad@snapshot/current/OpenSCAD.app/Contents/MacOS/OpenSCAD",
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_config(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def is_executable(path: str) -> bool:
    p = Path(path)
    return p.exists() and p.is_file() and os.access(path, os.X_OK)


def get_version(binary: str) -> str | None:
    """Return version string or None if binary fails."""
    try:
        result = subprocess.run(
            [binary, "--version"],
            capture_output=True, text=True, timeout=10
        )
        # OpenSCAD prints version to stderr
        output = (result.stdout + result.stderr).strip()
        return output if output else None
    except Exception:
        return None


def find_via_which() -> str | None:
    """Check PATH via `which`."""
    found = shutil.which("openscad")
    if found and is_executable(found):
        return found
    return None


def find_via_mdfind() -> list[str]:
    """
    Use Spotlight (mdfind) to find all installed OpenSCAD app bundles
    by bundle identifier. Returns a list of binary paths extracted from
    discovered .app bundles, newest/most specific first.
    """
    try:
        result = subprocess.run(
            ["mdfind", f"kMDItemCFBundleIdentifier == '{BUNDLE_ID}'"],
            capture_output=True, text=True, timeout=15
        )
        app_paths = [p.strip() for p in result.stdout.splitlines() if p.strip()]
    except FileNotFoundError:
        # mdfind not available (unlikely on macOS, but be safe)
        return []

    binaries = []
    for app in app_paths:
        binary = str(Path(app) / "Contents" / "MacOS" / "OpenSCAD")
        if is_executable(binary):
            binaries.append(binary)

    return binaries


def find_via_glob() -> list[str]:
    """
    Scan /Applications for date-stamped snapshot builds like:
      OpenSCAD-2025.04.15.app
    Also catches plain-folder installs like:
      /Applications/OpenSCAD/
    """
    found = []
    apps_dir = Path("/Applications")

    # .app bundles (sorted newest first by name)
    for app in sorted(apps_dir.glob("OpenSCAD*.app"), reverse=True):
        binary = str(app / "Contents" / "MacOS" / "OpenSCAD")
        if is_executable(binary):
            found.append(binary)

    # Plain folder installs (non-bundle layout)
    for folder in sorted(apps_dir.glob("OpenSCAD*"), reverse=True):
        if folder.is_dir() and not str(folder).endswith(".app"):
            for candidate in [
                folder / "Contents" / "MacOS" / "OpenSCAD",
                folder / "OpenSCAD",
            ]:
                if is_executable(str(candidate)):
                    found.append(str(candidate))

    return found


def discover() -> tuple[str | None, str]:
    """
    Run all discovery strategies in priority order.
    Returns (binary_path_or_None, source_description).
    """
    # 1. Cached
    cfg = load_config()
    cached = cfg.get("binary_path")
    if cached and is_executable(cached):
        return cached, "cached config"

    # 2. Environment variable
    env_bin = os.environ.get("OPENSCAD_BIN")
    if env_bin and is_executable(env_bin):
        return env_bin, "OPENSCAD_BIN env var"

    # 3. PATH
    which_result = find_via_which()
    if which_result:
        return which_result, "PATH (which)"

    # 4. Spotlight / mdfind
    mdfind_results = find_via_mdfind()
    if mdfind_results:
        # Prefer stable (/Applications/OpenSCAD.app) over snapshots
        for b in mdfind_results:
            if "snapshot" not in b.lower() and "nightly" not in b.lower():
                return b, "Spotlight (mdfind)"
        return mdfind_results[0], "Spotlight (mdfind, snapshot)"

    # 5. Known fixed paths
    for path in KNOWN_PATHS:
        if is_executable(path):
            return path, "known path"

    # 6. Glob scan of /Applications
    glob_results = find_via_glob()
    if glob_results:
        return glob_results[0], "glob scan of /Applications"

    return None, "not found"


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Locate the OpenSCAD binary on macOS"
    )
    parser.add_argument("--verify",  action="store_true",
                        help="Also run openscad --version to confirm it works")
    parser.add_argument("--set",     metavar="PATH",
                        help="Manually set and cache a binary path")
    parser.add_argument("--clear",   action="store_true",
                        help="Clear the cached binary path")
    parser.add_argument("--json",    action="store_true",
                        help="Output result as JSON")
    args = parser.parse_args()

    # Handle --clear
    if args.clear:
        cfg = load_config()
        cfg.pop("binary_path", None)
        save_config(cfg)
        print("Cleared cached OpenSCAD binary path.")
        return

    # Handle --set
    if args.set:
        path = os.path.expanduser(args.set)
        if not is_executable(path):
            print(f"ERROR: '{path}' is not executable or does not exist.",
                  file=sys.stderr)
            sys.exit(1)
        cfg = load_config()
        cfg["binary_path"] = path
        save_config(cfg)
        print(f"Cached OpenSCAD binary: {path}")
        if args.verify:
            ver = get_version(path)
            print(f"Version: {ver or '(could not determine)'}")
        return

    # Discover
    binary, source = discover()

    if binary is None:
        msg = (
            "OpenSCAD binary not found on this system.\n\n"
            "Searched:\n"
            "  • OPENSCAD_BIN environment variable\n"
            "  • PATH (which openscad)\n"
            "  • Spotlight (mdfind by bundle ID org.openscad.OpenSCAD)\n"
            "  • Known locations: /Applications/OpenSCAD.app, Homebrew, MacPorts\n"
            "  • Glob scan of /Applications/OpenSCAD*.app\n\n"
            "To fix:\n"
            "  1. Install OpenSCAD: https://openscad.org/downloads.html\n"
            "     or:  brew install --cask openscad\n"
            "     or:  sudo port install openscad\n"
            "  2. Once installed, re-run this script, OR:\n"
            "     python3 find_openscad.py --set /path/to/OpenSCAD\n"
        )
        if args.json:
            print(json.dumps({"found": False, "error": msg.strip()}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    # Cache the discovered path for next time
    cfg = load_config()
    if cfg.get("binary_path") != binary:
        cfg["binary_path"] = binary
        save_config(cfg)

    version = get_version(binary) if args.verify else None

    if args.json:
        print(json.dumps({
            "found":   True,
            "path":    binary,
            "source":  source,
            "version": version,
        }))
    else:
        print(binary)
        if args.verify:
            print(f"# Source:  {source}", file=sys.stderr)
            print(f"# Version: {version or '(unknown)'}", file=sys.stderr)


if __name__ == "__main__":
    main()
