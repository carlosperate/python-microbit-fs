"""Tests for device info detection from MicroPython hex files."""

import pytest

from microbit_micropython_fs import DeviceVersion, get_device_info
from microbit_micropython_fs.exceptions import InvalidHexError, NotMicroPythonError


class TestGetDeviceInfoV1:
    """Tests for micro:bit V1 MicroPython hex files."""

    def test_v1_page_size(self, upy_v1_hex: str) -> None:
        """V1 should have 1024 byte page size."""
        info = get_device_info(upy_v1_hex)
        assert info.flash_page_size == 1024

    def test_v1_flash_size(self, upy_v1_hex: str) -> None:
        """V1 should have 256 KB flash."""
        info = get_device_info(upy_v1_hex)
        assert info.flash_size == 256 * 1024

    def test_v1_flash_addresses(self, upy_v1_hex: str) -> None:
        """V1 flash should start at 0 and end at 256 KB."""
        info = get_device_info(upy_v1_hex)
        assert info.flash_start_address == 0
        assert info.flash_end_address == 256 * 1024

    def test_v1_runtime_addresses(self, upy_v1_hex: str) -> None:
        """V1 runtime should start at 0."""
        info = get_device_info(upy_v1_hex)
        assert info.runtime_start_address == 0
        micropython_last_byte_used = 0x388B8
        micropython_end_page = micropython_last_byte_used // info.flash_page_size + 1
        assert info.runtime_end_address == (micropython_end_page * info.flash_page_size)

    def test_v1_fs_addresses(self, upy_v1_hex: str) -> None:
        """V1 filesystem addresses should be calculated correctly."""
        info = get_device_info(upy_v1_hex)
        # V1 FS starts where runtime ends
        assert info.fs_start_address == info.runtime_end_address
        # V1 FS ends at flash end
        assert info.fs_end_address == info.flash_end_address

    def test_v1_fs_size(self, upy_v1_hex: str) -> None:
        """V1 filesystem size should be approximately 29 KB."""
        info = get_device_info(upy_v1_hex)
        # 256KB - 227KB runtime = 29KB filesystem
        assert info.fs_size == 28 * 1024

    def test_v1_device_version(self, upy_v1_hex: str) -> None:
        """V1 should be detected as V1."""
        info = get_device_info(upy_v1_hex)
        assert info.device_version == DeviceVersion.V1

    def test_v1_micropython_version(self, upy_v1_hex: str) -> None:
        """V1 should have the correct MicroPython version string."""
        info = get_device_info(upy_v1_hex)
        expected_micropython_versions = (
            "micro:bit v1.0.1+b0bf4a9 on 2018-12-13; "
            "MicroPython v1.9.2-34-gd64154c73 on 2017-09-01"
        )
        assert info.micropython_version == expected_micropython_versions


class TestGetDeviceInfoV2Uicr:
    """Tests for micro:bit V2 MicroPython hex files with UICR detection."""

    def test_v2_uicr_page_size(self, upy_v2_uicr_hex: str) -> None:
        """V2 should have 4096 byte page size."""
        info = get_device_info(upy_v2_uicr_hex)
        assert info.flash_page_size == 4096

    def test_v2_uicr_flash_size(self, upy_v2_uicr_hex: str) -> None:
        """V2 should have 512 KB flash."""
        info = get_device_info(upy_v2_uicr_hex)
        assert info.flash_size == 512 * 1024

    def test_v2_uicr_flash_addresses(self, upy_v2_uicr_hex: str) -> None:
        """V2 flash should start at 0 and end at 512 KB."""
        info = get_device_info(upy_v2_uicr_hex)
        assert info.flash_start_address == 0
        assert info.flash_end_address == 512 * 1024

    def test_v2_uicr_runtime_addresses(self, upy_v2_uicr_hex: str) -> None:
        """V2 runtime should start at 0."""
        info = get_device_info(upy_v2_uicr_hex)
        assert info.runtime_start_address == 0
        micropython_end_page = 109
        assert info.runtime_end_address == (micropython_end_page * info.flash_page_size)

    def test_v2_uicr_fs_addresses(self, upy_v2_uicr_hex: str) -> None:
        """V2 UICR filesystem addresses should be correct."""
        info = get_device_info(upy_v2_uicr_hex)
        # V2 FS for V2 UICR hex starts at 0x6D000 as defined in linker file
        assert info.fs_start_address == 0x6D000
        # V2 FS ends at 0x73000 as defined in linker file
        assert info.fs_end_address == 0x73000

    def test_v2_uicr_fs_size(self, upy_v2_uicr_hex: str) -> None:
        """V2 UICR filesystem size should be 20 KB (24KB available - 1 page)."""
        info = get_device_info(upy_v2_uicr_hex)
        assert info.fs_size == 20 * 1024

    def test_v2_uicr_device_version(self, upy_v2_uicr_hex: str) -> None:
        """V2 should be detected as V2."""
        info = get_device_info(upy_v2_uicr_hex)
        assert info.device_version == DeviceVersion.V2

    def test_v2_uicr_micropython_version(self, upy_v2_uicr_hex: str) -> None:
        """V2 UICR should have the correct MicroPython version string."""
        info = get_device_info(upy_v2_uicr_hex)
        expected_micropython_versions = (
            "micro:bit v2.0.99+3e09245 on 2020-11-02; "
            "MicroPython 3e09245 on 2020-11-02"
        )
        assert info.micropython_version == expected_micropython_versions


class TestGetDeviceInfoV2FlashRegions:
    """Tests for micro:bit V2 MicroPython hex files with Flash Regions detection."""

    def test_v2_region_page_size(self, upy_v2_region_hex: str) -> None:
        """V2 should have 4096 byte page size."""
        info = get_device_info(upy_v2_region_hex)
        assert info.flash_page_size == 4096

    def test_v2_region_flash_size(self, upy_v2_region_hex: str) -> None:
        """V2 should have 512 KB flash."""
        info = get_device_info(upy_v2_region_hex)
        assert info.flash_size == 512 * 1024

    def test_v2_region_flash_addresses(self, upy_v2_region_hex: str) -> None:
        """V2 flash should start at 0 and end at 512 KB."""
        info = get_device_info(upy_v2_region_hex)
        assert info.flash_start_address == 0
        assert info.flash_end_address == 512 * 1024

    def test_v2_region_runtime_addresses(self, upy_v2_region_hex: str) -> None:
        """V2 runtime should start at 0."""
        info = get_device_info(upy_v2_region_hex)
        assert info.runtime_start_address == 0
        micropython_last_byte_used = 0x61F24
        micropython_end_page = micropython_last_byte_used // info.flash_page_size + 1
        assert info.runtime_end_address == (micropython_end_page * info.flash_page_size)

    def test_v2_region_fs_addresses(self, upy_v2_region_hex: str) -> None:
        """V2 Flash Regions filesystem addresses should be correct."""
        info = get_device_info(upy_v2_region_hex)
        # V2 FS for V2 Flash Regions hex starts at 0x6D000 as defined in linker file
        assert info.fs_start_address == 0x6D000
        # V2 FS ends at 0x73000 as defined in linker file
        assert info.fs_end_address == 0x73000

    def test_v2_region_fs_size(self, upy_v2_region_hex: str) -> None:
        """V2 Flash Regions filesystem size should be 20 KB (24KB available - 1 page)."""
        info = get_device_info(upy_v2_region_hex)
        assert info.fs_size == 20 * 1024

    def test_v2_region_device_version(self, upy_v2_region_hex: str) -> None:
        """V2 should be detected as V2."""
        info = get_device_info(upy_v2_region_hex)
        assert info.device_version == DeviceVersion.V2

    def test_v2_region_micropython_version(self, upy_v2_region_hex: str) -> None:
        """V2 Flash Regions should have the correct MicroPython version string."""
        info = get_device_info(upy_v2_region_hex)
        expected_micropython_versions = (
            "micro:bit v2.0.99+b260810 on 2020-11-17; "
            "MicroPython b260810 on 2020-11-17"
        )
        assert info.micropython_version == expected_micropython_versions


class TestGetDeviceInfoErrors:
    """Tests for error handling in device detection."""

    def test_makecode_hex_raises_not_micropython(self, makecode_hex: str) -> None:
        """MakeCode hex should raise NotMicroPythonError."""
        with pytest.raises(NotMicroPythonError):
            get_device_info(makecode_hex)

    def test_empty_hex_raises_error(self) -> None:
        """Empty hex should raise an error."""
        with pytest.raises((NotMicroPythonError, ValueError)):
            get_device_info("")

    def test_invalid_hex_raises_error(self) -> None:
        """Invalid hex data should raise an error."""
        with pytest.raises((InvalidHexError, NotMicroPythonError, ValueError)):
            get_device_info("not a valid hex file")

    def test_minimal_valid_hex_raises_not_micropython(self) -> None:
        """A minimal valid Intel Hex without MicroPython should raise error."""
        # Minimal valid Intel Hex with just an EOF record
        minimal_hex = ":00000001FF\n"
        with pytest.raises(NotMicroPythonError):
            get_device_info(minimal_hex)
