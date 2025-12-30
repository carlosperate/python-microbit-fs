#!/usr/bin/env python3
"""
Command-line interface for microbit-micropython-fs.

This module provides CLI commands for working with micro:bit MicroPython
filesystems in Intel Hex files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from cyclopts import App

import microbit_micropython_fs as upyfs

app = App(
    name="microbit-fs",
    help="Inject and extract files from MicroPython Hex files for micro:bit.",
    version=upyfs.__version__,
)


@app.command
def info(hex_file: Path) -> None:
    """Display device and filesystem information from a MicroPython hex file.

    :param hex_file: Path to the Intel Hex file.
    """
    hex_data = hex_file.read_text()
    device_info = upyfs.get_device_info(hex_data)

    print(f"Device: micro:bit {device_info.device_version.value}")
    print(f"MicroPython version: {device_info.micropython_version}")
    print(f"Flash page size: {device_info.flash_page_size} bytes")
    print(f"Filesystem size: {device_info.fs_size} bytes")
    print(f"Filesystem start: 0x{device_info.fs_start_address:08X}")
    print(f"Filesystem end: 0x{device_info.fs_end_address:08X}")


@app.command(name="list")
def list_files(hex_file: Path) -> None:
    """List files stored in a MicroPython hex file.

    :param hex_file: Path to the Intel Hex file.
    """
    hex_data = hex_file.read_text()
    files = upyfs.get_files(hex_data)

    if not files:
        print("No files found in filesystem.")
        return

    total_size = 0
    for file in files:
        print(f"{file.name:40} {file.size:>8} bytes")
        total_size += file.size

    print(f"{'─' * 50}")
    print(f"{'Total':40} {total_size:>8} bytes ({len(files)} files)")


@app.command
def get(
    hex_file: Path,
    output_dir: Path = Path("."),
    filename: Optional[str] = None,
    force: bool = False,
) -> None:
    """Extract files from a MicroPython hex file.

    :param hex_file: Path to the Intel Hex file.
    :param output_dir: Directory to extract files to (default: current directory).
    :param filename: Extract only this specific file (default: extract all).
    :param force: Overwrite existing files without prompting (default: False).
    """
    hex_data = hex_file.read_text()
    files = upyfs.get_files(hex_data)

    if not files:
        print("No files found in filesystem.")
        return

    # Filter files if a specific filename was requested
    files_to_extract = files
    if filename is not None:
        files_to_extract = [f for f in files if f.name == filename]
        if not files_to_extract:
            raise SystemExit(f"Error: File not found in hex: {filename}")

    # Check for existing files before extracting (unless --force is used)
    if not force:
        existing_files = []
        for file in files_to_extract:
            output_path = output_dir / file.name
            if output_path.exists():
                existing_files.append(file.name)
        if existing_files:
            raise SystemExit(
                f"Error: Files already exist: {', '.join(existing_files)}\n"
                "Use --force to overwrite."
            )

    output_dir.mkdir(parents=True, exist_ok=True)

    for file in files_to_extract:
        output_path = output_dir / file.name
        output_path.write_bytes(file.content)
        print(f"Extracted: {file.name} ({file.size} bytes)")


@app.command
def add(
    hex_file: Path,
    files: list[Path],
    output: Optional[Path] = None,
) -> None:
    """Inject files into a MicroPython hex file.

    :param hex_file: Path to the input Intel Hex file.
    :param files: One or more files to add to the filesystem.
    :param output: Output hex file path (default: <input_name>_output.hex).
    """
    hex_data = hex_file.read_text()

    file_objects = []
    for file_path in files:
        content = file_path.read_bytes()
        file_objects.append(upyfs.File(name=file_path.name, content=content))
        print(f"Adding: {file_path.name} ({len(content)} bytes)")

    new_hex = upyfs.add_files(hex_data, file_objects)

    if output is not None:
        output_path = output
    else:
        # Generate default output filename: <name>_output.hex
        output_path = hex_file.parent / f"{hex_file.stem}_output.hex"
    output_path.write_text(new_hex)
    print(f"Written to: {output_path}")


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
