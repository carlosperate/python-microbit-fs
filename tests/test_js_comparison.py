"""Test comparison between Python and JavaScript implementations."""

from io import StringIO

import js_microbit_fs
from intelhex import IntelHex

import microbit_micropython_fs
from microbit_micropython_fs import File


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
    js_hex = js_microbit_fs.add_files(upy_v1_hex, files_data)

    # Compare the actual memory content (address -> byte), but ignore start address metadata
    ih_py = IntelHex()
    ih_py.loadhex(StringIO(py_hex))
    py_dict = ih_py.todict()
    if "start_addr" in py_dict:
        del py_dict["start_addr"]
    ih_js = IntelHex()
    ih_js.loadhex(StringIO(js_hex))
    js_dict = ih_js.todict()
    if "start_addr" in js_dict:
        del js_dict["start_addr"]

    assert py_dict == js_dict
