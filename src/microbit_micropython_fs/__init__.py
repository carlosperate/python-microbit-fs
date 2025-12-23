"""
microbit-micropython-fs: Inject and extract files from MicroPython Intel Hex files.

This library provides a simple API for working with MicroPython filesystem
embedded in Intel Hex files for the BBC micro:bit.

Main functions:
    - add_files: Add files to a MicroPython hex file
    - get_files: Read files from a MicroPython hex file
    - get_device_info: Get device memory information from a hex file
"""

from microbit_micropython_fs.api import (
    add_files,
    get_device_info,
    get_files,
)
from microbit_micropython_fs.device_info import DeviceInfo, DeviceVersion
from microbit_micropython_fs.exceptions import (
    FilesystemError,
    InvalidFileError,
    InvalidHexError,
    NotMicroPythonError,
    StorageFullError,
)
from microbit_micropython_fs.file import File

__version__ = "0.1.0"

__all__ = [
    # Main API functions
    "add_files",
    "get_files",
    "get_device_info",
    # Data classes
    "File",
    "DeviceInfo",
    "DeviceVersion",
    # Exceptions
    "FilesystemError",
    "InvalidHexError",
    "NotMicroPythonError",
    "InvalidFileError",
    "StorageFullError",
]
