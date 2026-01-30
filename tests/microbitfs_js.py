from __future__ import annotations

from pathlib import Path
from typing import Any

from py_mini_racer import JSEvalException, MiniRacer

from micropython_microbit_fs.exceptions import StorageFullError

TEST_DIR = Path(__file__).parent

TEXT_ENCODING_POLYFILL = """
class TextEncoder {
    encode(str) {
        const utf8 = unescape(encodeURIComponent(str));
        const result = new Uint8Array(utf8.length);
        for (let i = 0; i < utf8.length; i++) {
            result[i] = utf8.charCodeAt(i);
        }
        return result;
    }
}
class TextDecoder {
    decode(bytes) {
        let str = '';
        for (let i = 0; i < bytes.length; i++) {
            str += String.fromCharCode(bytes[i]);
        }
        return decodeURIComponent(escape(str));
    }
}
"""

_ctx_mr: MiniRacer | None = None


def _get_ctx() -> MiniRacer:
    global _ctx_mr
    if _ctx_mr is None:
        microbit_fs_js = (TEST_DIR / "microbitfs" / "microbit-fs.js").read_text()
        _ctx_mr = MiniRacer()
        _ctx_mr.eval(microbit_fs_js)
        _ctx_mr.eval(TEXT_ENCODING_POLYFILL)
        _ctx_mr.eval("let intelHexStr; let micropythonFs;")
        empty_micropython_hex = (TEST_DIR / "fixtures" / "upy-v1.0.1.hex").read_text()
        _ctx_mr.eval(f"const baseMicroPythonHexStr = `{empty_micropython_hex}`;")
    return _ctx_mr


def add_files(micropython: str, files: dict[str, str]) -> str:
    """
    Add files to a micro:bit MicroPython Intel hex string.

    :param micropython: Intel hex string representing the MicroPython firmware.
    :param files: Dictionary of filenames and contents to add to the filesystem.
    :return: Updated Intel hex string with the new files added.
    """
    ctx_mr = _get_ctx()
    ctx_mr.eval(f"intelHexStr = `{micropython}`;")
    ctx_mr.eval("micropythonFs = new microbitFs.MicropythonFsHex(intelHexStr);")
    for name, content in files.items():
        ctx_mr.eval(f"micropythonFs.create(`{name}`, `{content}`);")
    try:
        ihex_updated: Any = ctx_mr.eval("micropythonFs.getIntelHex();")
    except JSEvalException as js_e:
        if "There is no storage space left" in str(js_e):
            raise StorageFullError("Not enough space in the filesystem.") from js_e
        else:
            raise
    return str(ihex_updated)


def get_files(micropython: str) -> dict[str, str]:
    """
    Get files from a micro:bit MicroPython Intel hex string.

    :param micropython: Intel hex string representing the MicroPython firmware.
    :return: Dictionary of filenames and their contents from the filesystem.
    """
    ctx_mr = _get_ctx()
    # First we need to create a new instance of MicropythonFsHex with an
    # MicroPython without any added files
    ctx_mr.eval(
        "micropythonFs = new microbitFs.MicropythonFsHex(baseMicroPythonHexStr);"
    )
    ctx_mr.eval(f"intelHexStr = `{micropython}`;")
    ctx_mr.eval("micropythonFs.importFilesFromIntelHex(intelHexStr);")
    fs_ls: Any = ctx_mr.eval("micropythonFs.ls();")
    files: dict[str, str] = {}
    for filename in fs_ls:
        content: Any = ctx_mr.eval(f"micropythonFs.read(`{filename}`);")
        files[filename] = str(content)
    ctx_mr.eval("delete micropythonFs; delete intelHexStr;")
    return files


def main() -> None:
    """Simple test/demo of adding and reading files a MicroPython hex."""
    micropython_hex_str = (TEST_DIR / "fixtures" / "upy-v1.0.1.hex").read_text()
    files_to_add = {
        "main.py": "print('Hello from main.py!')",
        "utils.py": "def add(a, b):\n    return a + b",
    }
    updated_hex = add_files(micropython_hex_str, files_to_add)
    print(updated_hex)
    fs_ls: Any = get_files(updated_hex)
    print("Files:", fs_ls)
    assert files_to_add.keys() == fs_ls.keys()
    for filename in files_to_add:
        assert fs_ls[filename] == files_to_add[filename]


if __name__ == "__main__":
    main()
