from __future__ import annotations

from pathlib import Path
from typing import Any

from py_mini_racer import MiniRacer

ctx_mr: MiniRacer | None = None

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


def load_js() -> None:
    microbit_fs_js = (TEST_DIR / "microbitfs" / "microbit-fs.js").read_text()
    global ctx_mr
    ctx_mr = MiniRacer()
    ctx_mr.eval(microbit_fs_js)


def add_files(micropython: str, files: dict[str, str]) -> str:
    global ctx_mr
    if ctx_mr is None:
        load_js()
    assert ctx_mr is not None
    ctx_mr.eval(TEXT_ENCODING_POLYFILL)
    ctx_mr.eval(f"const intelHexStr = `{micropython}`;")
    ctx_mr.eval("const micropythonFs = new microbitFs.MicropythonFsHex(intelHexStr);")
    for name, content in files.items():
        ctx_mr.eval(f"micropythonFs.create(`{name}`, `{content}`);")
    ihex_updated: Any = ctx_mr.eval("micropythonFs.getIntelHex();")
    return str(ihex_updated)


def main() -> None:
    load_js()
    if ctx_mr is None:
        raise RuntimeError("JavaScript environment not loaded.")
    micropython_hex_str = (TEST_DIR / "fixtures" / "upy-v1.0.1.hex").read_text()
    files_to_add = {
        "main.py": "print('Hello from main.py!')",
        "utils.py": "def add(a, b):\n    return a + b",
    }
    updated_hex = add_files(micropython_hex_str, files_to_add)
    print(updated_hex)
    fs_ls: Any = ctx_mr.eval("micropythonFs.ls()")
    print(list(fs_ls))


if __name__ == "__main__":
    main()
