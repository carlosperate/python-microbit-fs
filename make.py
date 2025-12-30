#!/usr/bin/env python3
"""Run make-like commands for the project.

Usage: python make.py <command>

This replaces a Makefile with a cross-platform Python script.
"""

import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

# Project root directory (where this script lives)
ROOT = Path(__file__).parent.resolve()

PATHS_TO_CHECK = [
    ROOT / "src",
    ROOT / "tests",
    ROOT / "make.py",
]
CHECK_PATHS = [str(p.relative_to(Path.cwd())) for p in PATHS_TO_CHECK]

# Command registry
COMMANDS: dict[str, Callable[[], None]] = {}


def command(func: Callable[[], None]) -> Callable[[], None]:
    """Decorator to register a function as a command."""
    COMMANDS[func.__name__.replace("_", "-")] = func
    return func


def run(cmd: list[str], check: bool = True) -> int:
    """Run a command and return the exit code."""
    print("\n" + "=" * 80 + f"\n$ {' '.join(cmd)}\n" + "-" * 80)
    result = subprocess.run(cmd, cwd=ROOT)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result.returncode


@command
def clean() -> None:
    """Remove build artifacts and caches."""
    dirs_to_remove = [
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "build",
        "dist",
        "htmlcov",
        ".coverage",
    ]
    for name in dirs_to_remove:
        path = ROOT / name
        if path.is_dir():
            print(f"Removing {path}")
            shutil.rmtree(path)
        elif path.is_file():
            print(f"Removing {path}")
            path.unlink()

    # Remove __pycache__ directories recursively
    for pycache in ROOT.rglob("__pycache__"):
        print(f"Removing {pycache}")
        shutil.rmtree(pycache)

    # Remove .pyc files
    for pyc in ROOT.rglob("*.pyc"):
        print(f"Removing {pyc}")
        pyc.unlink()


@command
def lint() -> None:
    """Run ruff linter."""
    run(["uv", "run", "ruff", "check"] + CHECK_PATHS)


@command
def format() -> None:
    """Run code formatters (ruff)."""
    run(["uv", "run", "ruff", "check", "--fix"] + CHECK_PATHS)
    run(["uv", "run", "ruff", "format"] + CHECK_PATHS)


@command
def format_check() -> None:
    """Check code formatting without making changes."""
    run(["uv", "run", "ruff", "check"] + CHECK_PATHS)
    run(["uv", "run", "ruff", "format", "--check", "--diff"] + CHECK_PATHS)


@command
def typecheck() -> None:
    """Run mypy type checker."""
    run(["uv", "run", "mypy"] + CHECK_PATHS)


@command
def test() -> None:
    """Run tests with pytest."""
    run(["uv", "run", "pytest", "-n", "auto"])


@command
def test_cov() -> None:
    """Run tests with coverage report."""
    run(
        [
            "uv",
            "run",
            "pytest",
            "-n",
            "auto",
            "--cov=src",
            "--cov-report=term-missing",
        ]
    )


@command
def check() -> None:
    """Run all checks (lint, typecheck, test)."""
    lint()
    typecheck()
    format_check()
    test_cov()


@command
def build() -> None:
    """Build the package."""
    clean()
    run(["uv", "build"])


@command
def publish_test() -> None:
    """Publish to TestPyPI."""
    build()
    run(["uv", "publish", "--publish-url", "https://test.pypi.org/legacy/"])


@command
def publish() -> None:
    """Publish to PyPI."""
    build()
    run(["uv", "publish"])


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        print("Commands:")
        for name, func in COMMANDS.items():
            doc = func.__doc__ or ""
            print(f"  {name:14} {doc}")
        return 0

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(COMMANDS.keys())}")
        return 1

    COMMANDS[cmd]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
