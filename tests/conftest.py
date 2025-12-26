"""Pytest configuration and shared fixtures."""

from pathlib import Path

import pytest

# Path to test fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return FIXTURES_DIR


@pytest.fixture(scope="session")
def upy_v1_hex() -> str:
    """Load the MicroPython V1 hex file."""
    hex_path = FIXTURES_DIR / "upy-v1.0.1.hex"
    return hex_path.read_text()


@pytest.fixture(scope="session")
def upy_v2_uicr_hex() -> str:
    """Load the MicroPython V2 hex file (UICR detection)."""
    hex_path = FIXTURES_DIR / "upy-v2-beta-uicr.hex"
    return hex_path.read_text()


@pytest.fixture(scope="session")
def upy_v2_region_hex() -> str:
    """Load the MicroPython V2 hex file (Flash Regions detection)."""
    hex_path = FIXTURES_DIR / "upy-v2-beta-region.hex"
    return hex_path.read_text()


@pytest.fixture(scope="session")
def makecode_hex() -> str:
    """Load the MakeCode hex file (non-MicroPython)."""
    hex_path = FIXTURES_DIR / "makecode.hex"
    return hex_path.read_text()
