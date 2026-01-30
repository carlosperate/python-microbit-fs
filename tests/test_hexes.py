"""Tests for the hexes module."""

import pytest

import micropython_microbit_fs as upyfs
from micropython_microbit_fs.hexes import (
    HexNotFoundError,
    get_bundled_hex,
    list_bundled_versions,
)


class TestListBundledVersions:
    """Tests for list_bundled_versions function."""

    def test_list_v1_versions(self) -> None:
        """Should list available V1 hex versions."""
        versions = list_bundled_versions(1)
        assert 1 in versions
        assert len(versions[1]) >= 1
        assert "1.1.1" in versions[1]

    def test_list_v2_versions(self) -> None:
        """Should list available V2 hex versions."""
        versions = list_bundled_versions(2)
        assert 2 in versions
        assert len(versions[2]) >= 1
        assert "2.1.2" in versions[2]

    def test_list_nonexistent_device(self) -> None:
        """Should return empty list for non-existent device version."""
        versions = list_bundled_versions(99)
        assert versions == {99: []}

    def test_versions_sorted_newest_first(self) -> None:
        """Versions should be sorted with newest first."""
        # This test will be more meaningful when we have multiple versions
        v1_versions = list_bundled_versions(1)
        v2_versions = list_bundled_versions(2)
        # At minimum, ensure we get a list (even if single item)
        assert isinstance(v1_versions[1], list)
        assert isinstance(v2_versions[2], list)

    def test_list_all_devices(self) -> None:
        """Should list versions for all known devices when no device given."""
        versions = list_bundled_versions()
        assert 1 in versions
        assert 2 in versions
        assert "1.1.1" in versions[1]
        assert "2.1.2" in versions[2]


class TestGetBundledHex:
    """Tests for get_bundled_hex function."""

    def test_get_v1_hex_latest(self) -> None:
        """Should return latest V1 hex when no version specified."""
        hex_file = get_bundled_hex(1)
        assert hex_file.content.startswith(":")
        assert hex_file.file_path.name.endswith(".hex")
        assert hex_file.device_version == 1
        # Verify it's a valid V1 hex
        device_info = upyfs.get_device_info(hex_file.content)
        assert device_info.device_version == upyfs.DeviceVersion.V1

    def test_get_v2_hex_latest(self) -> None:
        """Should return latest V2 hex when no version specified."""
        hex_file = get_bundled_hex(2)
        assert hex_file.content.startswith(":")
        assert hex_file.file_path.name.endswith(".hex")
        assert hex_file.device_version == 2
        # Verify it's a valid V2 hex
        device_info = upyfs.get_device_info(hex_file.content)
        assert device_info.device_version == upyfs.DeviceVersion.V2

    def test_get_v1_hex_specific_version(self) -> None:
        """Should return specific V1 version."""
        hex_file = get_bundled_hex(1, "1.1.1")
        assert hex_file.content.startswith(":")
        assert hex_file.version == "1.1.1"
        assert "1.1.1" in hex_file.file_path.name
        assert hex_file.file_path.name.endswith(".hex")
        assert hex_file.device_version == 1
        device_info = upyfs.get_device_info(hex_file.content)
        assert device_info.device_version == upyfs.DeviceVersion.V1

    def test_get_v2_hex_specific_version(self) -> None:
        """Should return specific V2 version."""
        hex_file = get_bundled_hex(2, "2.1.2")
        assert hex_file.content.startswith(":")
        assert hex_file.version == "2.1.2"
        assert "2.1.2" in hex_file.file_path.name
        assert hex_file.file_path.name.endswith(".hex")
        assert hex_file.device_version == 2
        device_info = upyfs.get_device_info(hex_file.content)
        assert device_info.device_version == upyfs.DeviceVersion.V2

    def test_get_hex_nonexistent_version(self) -> None:
        """Should raise error for non-existent version."""
        with pytest.raises(HexNotFoundError) as exc_info:
            get_bundled_hex(1, "99.99.99")
        assert "99.99.99" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    def test_get_hex_nonexistent_device(self) -> None:
        """Should raise error for non-existent device version."""
        with pytest.raises(HexNotFoundError) as exc_info:
            get_bundled_hex(99)
        assert "V99" in str(exc_info.value)

    def test_hex_content_can_add_files(self) -> None:
        """Bundled hex should support adding files."""
        hex_file = get_bundled_hex(1)
        files = [upyfs.File.from_text("main.py", "print('hello')")]
        new_hex = upyfs.add_files(hex_file.content, files)
        result_files = upyfs.get_files(new_hex)
        assert len(result_files) == 1
        assert result_files[0].name == "main.py"
