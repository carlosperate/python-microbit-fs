"""Test comparison between Python and JavaScript implementations."""

from io import StringIO
from pathlib import Path

import microbitfs_js
from intelhex import IntelHex

import microbit_micropython_fs
from microbit_micropython_fs import File

# Use this list of MicroPython hex files to repeat all the tests
UPY_V1_0_1_HEX = [  # type: ignore[assignment]
    (Path(__file__).parent / "fixtures" / "upy-v1.0.1.hex").read_text(),
    (Path(__file__).parent / "fixtures" / "upy-v1.0.1.hex").read_text(),
]


def compare_ihexes(hex_str1: str, hex_str2: str, msg: str) -> None:
    """Compare two Intel Hex strings for equality."""
    ih1 = IntelHex()
    ih1.loadhex(StringIO(hex_str1))
    ih2 = IntelHex()
    ih2.loadhex(StringIO(hex_str2))
    ih_dict_1: dict = ih1.todict()
    ih_dict_2: dict = ih2.todict()
    # Compare the actual memory content (address -> byte), but ignore start address metadata
    if "start_addr" in ih_dict_1:
        del ih_dict_1["start_addr"]
    if "start_addr" in ih_dict_2:
        del ih_dict_2["start_addr"]
    assert ih_dict_1 == ih_dict_2, msg


def test_compare_python_and_js_output(upy_v1_hex: str) -> None:
    """Compare output of Python and JS libraries for adding files."""
    # Test data
    files_data = {
        "main.py": "print('Hello from main.py!')",
        "utils.py": "def add(a, b):\n    return a + b",
    }

    # Generate hex using Python library
    py_files = [File.from_text(name, content) for name, content in files_data.items()]
    py_hex = microbit_micropython_fs.add_files(upy_v1_hex, py_files)

    # Generate hex using JS library
    js_hex = microbitfs_js.add_files(UPY_V1_0_1_HEX[0], files_data)

    compare_ihexes(py_hex, js_hex, "Python and JS Intel Hex outputs do not match")
