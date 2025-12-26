# microbit-micropython-fs

A Python library to inject and extract files from MicroPython Intel Hex files for the BBC micro:bit.

## Features

- **Inject files** into a MicroPython hex file for flashing to micro:bit
- **Extract files** from an existing MicroPython hex file
- **Get device info** including filesystem size and MicroPython version
- Supports both micro:bit V1 and V2 boards

## Installation

```bash
pip install microbit-micropython-fs
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

# Add files and get new hex
new_hex = micropython.add_files(micropython_hex, files)

# Save the new hex file
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

Clone the repository
```bash
git clone https://github.com/carlosperate/python-microbit-fs.git
cd python-microbit-fs
```

Install dependencies (uv creates virtual environment automatically):

```bash
uv sync --all-extras
```

### Development Commands

This project includes a `make.py` script to automate common development tasks.

```bash
# Run all checks (lint, typecheck, test)
python make.py check
# Run tests
python make.py test
# Format code (black + ruff fix)
python make.py format
# Build package
python make.py build
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

This project has been ported (AI assisted) from the original
[microbit-fs](https://github.com/microbit-foundation/microbit-fs)
TypeScript library.
