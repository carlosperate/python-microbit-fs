#!/usr/bin/env python3
"""
Main public API for microbit-micropython-fs.

This module provides the main functions for working with micro:bit MicroPython
filesystems in Intel Hex files.
"""

from typing import Any

from microbit_micropython_fs.device_info import DeviceInfo
from microbit_micropython_fs.exceptions import InvalidHexError, NotMicroPythonError
from microbit_micropython_fs.file import File
from microbit_micropython_fs.flash_regions import get_device_info_from_flash_regions
from microbit_micropython_fs.fs_reader import read_files_from_hex
from microbit_micropython_fs.fs_writer import create_hex_with_files
from microbit_micropython_fs.hex_utils import load_hex
from microbit_micropython_fs.uicr import get_device_info_from_uicr


def add_files(
    hex_data: str,
    files: list[File],
) -> str:
    """
    Add files to a micro:bit MicroPython Intel Hex file.

    Takes a micro:bit MicroPython hex file and a list of files to add,
    returning a new hex file with the files encoded in the filesystem region.

    :param hex_data: Intel Hex file content as a string.
    :param files: List of File objects to inject into the filesystem.
    :returns: New Intel Hex file content with the files injected.

    :raises InvalidHexError: If the hex data is invalid.
    :raises NotMicroPythonError: If the hex does not contain MicroPython.
    :raises InvalidFileError: If a file has invalid name or content.
    :raises StorageFullError: If the files don't fit in the filesystem.

    Example::

        >>> import microbit_micropython_fs as micropython
        >>> files = [micropython.File.from_text("main.py", "print('Hello!')")]
        >>> new_hex = micropython.add_files(micropython_hex, files)
    """
    try:
        ih = load_hex(hex_data)
    except Exception as e:
        raise InvalidHexError(f"Failed to parse Intel Hex data: {e}") from e
    device_info = _get_device_info_from_hex(ih)
    return create_hex_with_files(ih, device_info, files)


def get_files(hex_data: str) -> list[File]:
    """
    Get files from a micro:bit MicroPython Intel Hex file.

    Reads a micro:bit MicroPython hex file and returns all files found in the
    filesystem region.

    :param hex_data: Intel Hex file content as a string.
    :returns: List of File objects found in the filesystem.

    :raises InvalidHexError: If the hex data is invalid.
    :raises NotMicroPythonError: If the hex does not contain MicroPython.
    :raises FilesystemError: If the filesystem structure is corrupted.

    Example::

        >>> import microbit_micropython_fs as micropython
        >>> files = micropython.get_files(hex_with_files)
        >>> for f in files:
        ...     print(f"{f.name}: {f.size} bytes")
    """
    try:
        ih = load_hex(hex_data)
    except Exception as e:
        raise InvalidHexError(f"Failed to parse Intel Hex data: {e}") from e
    device_info = _get_device_info_from_hex(ih)
    return read_files_from_hex(ih, device_info)


def _get_device_info_from_hex(ih: Any) -> DeviceInfo:
    """
    Internal function to get device info from an already-loaded IntelHex.

    :param ih: IntelHex object.
    :returns: DeviceInfo containing memory layout information.

    :raises NotMicroPythonError: If the hex does not contain MicroPython.
    """
    # First try Flash Regions Table detection, as it's more likely to be a V2
    device_info = get_device_info_from_flash_regions(ih)
    if device_info is not None:
        return device_info

    # Try UICR detection next (works for V1 and pre-release V2)
    device_info = get_device_info_from_uicr(ih)
    if device_info is not None:
        return device_info

    raise NotMicroPythonError(
        "Could not detect MicroPython in hex file. "
        "The hex file may not contain MicroPython or may be corrupted."
    )


def get_device_info(hex_data: str) -> DeviceInfo:
    """
    Get device memory information from a MicroPython Intel Hex file.

    Extracts information about the flash memory layout, including
    filesystem boundaries and MicroPython version.

    :param hex_data: Intel Hex file content as a string.
    :returns: DeviceInfo containing memory layout information.

    :raises InvalidHexError: If the hex data is invalid.
    :raises NotMicroPythonError: If the hex does not contain MicroPython.

    Example::

        >>> import microbit_micropython_fs as micropython
        >>> info = micropython.get_device_info(micropython_hex)
        >>> print(f"FS Size: {info.fs_size} bytes")
        >>> print(f"MicroPython: {info.micropython_version}")
    """
    try:
        ih = load_hex(hex_data)
    except Exception as e:
        raise InvalidHexError(f"Failed to parse Intel Hex data: {e}") from e
    return _get_device_info_from_hex(ih)
