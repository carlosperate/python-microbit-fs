# microbit-micropython-fs

[![Test](https://github.com/carlosperate/python-microbit-fs/actions/workflows/test.yml/badge.svg)](https://github.com/carlosperate/python-microbit-fs/actions/workflows/test.yml)
[![PyPI versions](https://img.shields.io/pypi/pyversions/microbit-micropython-fs.svg)](https://pypi.org/project/ubittool/)
[![PyPI - License](https://img.shields.io/pypi/l/microbit-micropython-fs.svg)](LICENSE)

A Python library and command line tool to inject and extract files from
[MicroPython](https://microbit-micropython.readthedocs.io)
Intel Hex file for the [BBC micro:bit](https://microbit.org).

## Features

- **Inject files** into a MicroPython hex file for flashing to micro:bit.
- **Extract files** from an existing MicroPython hex file.
- **Get device info** including filesystem size and MicroPython version.
- **Command-line interface** for easy scripting and automation.
- Supports both micro:bit V1 and V2 boards.

## Installation

To install this terminal tool we recommend using [uv](https://docs.astral.sh/uv/):

```
uv tool install microbit-micropython-fs
```

It can also be installed via pip as a normal Python package:

```bash
pip install microbit-micropython-fs
```

## Command Line Interface

The package includes a `microbit-fs` command for working with hex files from
the terminal.

### Usage

Display device information:

```bash
microbit-fs info micropython.hex
```

List files in a hex file:

```bash
microbit-fs list micropython_with_files.hex
```

Add files to a hex file:

```bash
# Add a single file (creates micropython_output.hex)
microbit-fs add micropython.hex main.py

# Add multiple files with a custom output file
microbit-fs add micropython.hex main.py helper.py --output output.hex
```

Extract files from a hex file:

```bash
# Extract all files to the current directory
microbit-fs get micropython_with_files.hex

# Extract all files to a specific directory
microbit-fs get micropython_with_files.hex --output-dir ./extracted

# Extract a specific file
microbit-fs get micropython_with_files.hex --filename main.py

# Overwrite existing files without prompting
microbit-fs get micropython_with_files.hex --force
```


## Quick Start

### Add files to a MicroPython hex

```python
import microbit_micropython_fs as micropython

# Read your MicroPython hex file
with open("micropython.hex") as f:
    micropython_hex = f.read()

# Create files to add
files = [
    micropython.File.from_text("main.py", "from microbit import *\ndisplay.scroll('Hello!')"),
    micropython.File.from_text("helper.py", "def greet(name):\n    return f'Hello {name}'"),
]

# Add files and get new hex string
new_hex = micropython.add_files(micropython_hex, files)

with open("micropython_with_files.hex", "w") as f:
    f.write(new_hex)
```

### Get files from a MicroPython hex

```python
import microbit_micropython_fs as micropython

# Read hex file with embedded files
with open("micropython_with_files.hex") as f:
    hex_data = f.read()

# Get all files
files = micropython.get_files(hex_data)

for file in files:
    print(f"{file.name}: {file.size} bytes")
    print(file.get_text())
```

### Get device information

```python
import microbit_micropython_fs as micropython

with open("micropython.hex") as f:
    hex_data = f.read()

info = micropython.get_device_info(hex_data)
print(f"Device: micro:bit {info.device_version.value}")
print(f"MicroPython: {info.micropython_version}")
print(f"Filesystem size: {info.fs_size} bytes")
print(f"Flash page size: {info.flash_page_size} bytes")
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for project management.

### Setup

```bash
git clone https://github.com/carlosperate/python-microbit-fs.git
cd python-microbit-fs
uv sync --all-extras
```

### Development Commands

This project includes a `make.py` script to automate common development tasks.

```bash
# Run all checks (lint, typecheck, format check, test with coverage)
python make.py check

# Format code (ruff check --fix + ruff format)
python make.py format

# Show all available commands
python make.py help
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- This project has been ported (AI assisted) from the original
  [microbit-fs](https://github.com/microbit-foundation/microbit-fs)
  TypeScript library.
- This project packs the files inside a micro:bit MicroPython hex, which
  can then be flashed to a micro:bit.
  To read and write files from a running micro:bit device over USB,
  the [microFs](https://github.com/ntoll/microfs) CLI tool can be used.
