"""Test comparison between Python and JavaScript implementations.

These tests compares this Python port of microbit-fs with the original
JavaScript library to ensure they produce identical results.
"""

from io import StringIO

import microbitfs_js
import pytest
from intelhex import IntelHex
from py_mini_racer import JSEvalException

import micropython_microbit_fs
from micropython_microbit_fs import File, StorageFullError
from micropython_microbit_fs.device_info import get_device_info_ih
from micropython_microbit_fs.filesystem import (
    CHUNK_DATA_SIZE,
    CHUNK_SIZE,
    MAX_FILENAME_LENGTH,
    get_fs_start_address,
    get_last_page_address,
)
from micropython_microbit_fs.hex_utils import load_hex


# =============================================================================
# Helper Functions
# =============================================================================
def compare_ihexes(hex_str1: str, hex_str2: str, msg: str) -> None:
    """Compare two Intel Hex strings for equality.

    The comparison ignores start_addr metadata and compares only the
    actual memory content (address -> byte mapping).
    """
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


def get_available_chunks(hex_data: str) -> int:
    """Get the number of available chunks in the filesystem."""
    ih = load_hex(hex_data)
    device_info = get_device_info_ih(ih)
    fs_start = get_fs_start_address(device_info)
    fs_end = get_last_page_address(device_info)
    return (fs_end - fs_start) // CHUNK_SIZE


def generate_content(size: int) -> str:
    """Generate content of the specified byte size using printable ASCII characters."""
    # Use printable ASCII characters (letters and digits) to avoid encoding issues
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(chars[i % len(chars)] for i in range(size))


def py_add_files(hex_data: str, files_dict: dict[str, str]) -> str:
    """Add files using the Python library."""
    py_files = [File.from_text(name, content) for name, content in files_dict.items()]
    return micropython_microbit_fs.add_files(hex_data, py_files)


def py_get_files(hex_data: str) -> dict[str, str]:
    """Get files using the Python library, returning as a dict."""
    files = micropython_microbit_fs.get_files(hex_data)
    return {f.name: f.get_text() for f in files}


def js_add_files(hex_data: str, files_dict: dict[str, str]) -> str:
    """Add files using the JavaScript library."""
    return microbitfs_js.add_files(hex_data, files_dict)


def js_get_files(hex_data: str) -> dict[str, str]:
    """Get files using the JavaScript library."""
    return microbitfs_js.get_files(hex_data)


def run_all_checks(
    hex_data: str,
    files_dict: dict[str, str],
) -> None:
    """Run all comparison checks for adding files.

    This runs the following checks:
    1. Add files to Python and JS, compare the generated hex output
    2. Add files to Python, read with JS, compare results
    3. Add files to JS, read with Python, compare results
    """
    # Check 1: Add files to both and compare hex output
    py_hex = py_add_files(hex_data, files_dict)
    js_hex = js_add_files(hex_data, files_dict)
    compare_ihexes(
        py_hex,
        js_hex,
        f"Python and JS hex outputs do not match for files: {list(files_dict.keys())}",
    )

    # Check 2: Add with Python, read with JS
    js_read_from_py = js_get_files(py_hex)
    assert js_read_from_py == files_dict, (
        f"JS reading from Python hex failed. Expected: {files_dict}, Got: {js_read_from_py}"
    )

    # Check 3: Add with JS, read with Python
    py_read_from_js = py_get_files(js_hex)
    assert py_read_from_js == files_dict, (
        f"Python reading from JS hex failed. Expected: {files_dict}, Got: {py_read_from_js}"
    )


def calculate_max_content_for_single_file(filename: str, available_chunks: int) -> int:
    """Calculate the maximum content size for a single file.

    The formula accounts for:
    - Header: 2 bytes (end_offset + name_len) + filename bytes
    - Trailing 0xFF byte
    - Chunk structure: 128 bytes total, 126 bytes usable per chunk
    """
    filename_bytes = len(filename.encode("utf-8"))
    header_size = 2 + filename_bytes  # end_offset + name_len + name
    trailing_byte = 1  # trailing 0xFF

    total_data_capacity = available_chunks * CHUNK_DATA_SIZE
    max_content = total_data_capacity - header_size - trailing_byte
    return max_content


# =============================================================================
# Group 1: Single File Tests
# =============================================================================
class TestSingleFileIncremental:
    """Test adding a single file with incrementally increasing content sizes."""

    CONTENT_SIZES = (
        [
            1,  # Minimum content size
            50,  # Medium content
        ]
        # 1st chunk includes header, so over-test to ensure we cover the boundary
        + list(range(115, 128))
        + [
            200,  # Two chunks
            500,  # Multiple chunks
            10000,  # Larger file
        ]
    )

    @pytest.mark.parametrize("content_size", CONTENT_SIZES)
    def test_single_file_various_sizes(
        self, upy_v1_hex: str, content_size: int
    ) -> None:
        """Test adding a single file with various content sizes."""
        files_dict = {"main.py": generate_content(content_size)}
        run_all_checks(upy_v1_hex, files_dict)

    def test_single_file_fill_filesystem(self, upy_v1_hex: str) -> None:
        """Test filling the filesystem with a single file up to capacity.

        This test finds the maximum content size that fits, then verifies
        that exceeding it raises StorageFullError.
        """
        filename = "main.py"
        available_chunks = get_available_chunks(upy_v1_hex)
        max_content = calculate_max_content_for_single_file(filename, available_chunks)

        # Verify max content fits
        files_dict = {filename: generate_content(max_content)}
        run_all_checks(upy_v1_hex, files_dict)

        # Verify one more byte triggers StorageFullError
        files_dict_overflow = {filename: generate_content(max_content + 1)}

        with pytest.raises(StorageFullError):
            py_add_files(upy_v1_hex, files_dict_overflow)

        with pytest.raises(StorageFullError):
            js_add_files(upy_v1_hex, files_dict_overflow)


# =============================================================================
# Group 2: Multiple Files Tests
# =============================================================================
class TestMultipleFilesIncremental:
    """Test adding multiple files incrementally until filesystem is full."""

    def _generate_small_file(self, index: int) -> tuple[str, str]:
        """Generate a small file that fits in a single chunk.

        Each file takes exactly one chunk (filename + content < 120 bytes).
        """
        filename = f"f{index:03d}.py"  # 8 chars, e.g., "f001.py"
        content = generate_content(50)
        return filename, content

    def test_multiple_files_incremental(self, upy_v1_hex: str) -> None:
        """Test adding files one by one until filesystem is full."""
        # Exponential number of files until we reach the max
        max_files = get_available_chunks(upy_v1_hex)
        number_of_files = []
        f_i = 1
        while f_i <= max_files:
            number_of_files.append(f_i)
            f_i *= 2
        number_of_files.append(max_files)
        assert len(number_of_files) > 0, "Should add at least one file"

        test_files: dict[str, str] = {}
        for file_count in number_of_files:
            for file_index in range(len(test_files), file_count):
                filename, content = self._generate_small_file(file_index)
                test_files[filename] = content
            run_all_checks(upy_v1_hex, test_files)

        # Verify adding one more file raises StorageFullError for both
        file_index += 1
        next_filename, next_content = self._generate_small_file(file_index)
        overflow_files = {**test_files, next_filename: next_content}

        with pytest.raises(StorageFullError):
            py_add_files(upy_v1_hex, overflow_files)

        with pytest.raises(StorageFullError):
            js_add_files(upy_v1_hex, overflow_files)


# =============================================================================
# Group 3: Filename Length Tests
# =============================================================================
class TestFilenameLength:
    """Test filename length limits (max 120 characters)."""

    @pytest.mark.parametrize("filename_length", [1, 10, 119, 120])
    def test_various_filename_lengths(
        self, upy_v1_hex: str, filename_length: int
    ) -> None:
        """Test various valid filename lengths."""
        # Ensure we have a valid extension
        if filename_length <= 3:
            filename = "a" * filename_length
        else:
            filename = "a" * (filename_length - 3) + ".py"
        assert len(filename) == filename_length

        content = "test content"
        files_dict = {filename: content}

        run_all_checks(upy_v1_hex, files_dict)

    def test_filename_121_chars_fails(self, upy_v1_hex: str) -> None:
        """Test that a filename of 121 characters fails in both."""
        filename = "a" * 118 + ".py"  # 118 + 3 = 121 chars
        assert len(filename) == MAX_FILENAME_LENGTH + 1

        content = "test content"

        # Python should raise InvalidFileError during File creation
        with pytest.raises(micropython_microbit_fs.InvalidFileError):
            File.from_text(filename, content)

        # JS should raise an exception
        with pytest.raises(JSEvalException) as exc_info:
            js_add_files(upy_v1_hex, {filename: content})
        assert "too long" in str(exc_info.value).lower()


# =============================================================================
# Group 4: Additional Edge Case Tests
# =============================================================================
class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_multiple_files_with_different_sizes(self, upy_v1_hex: str) -> None:
        """Test adding multiple files with varying content sizes."""
        files_dict = {
            "tiny.py": generate_content(1),
            "small.py": generate_content(50),
            "medium.py": generate_content(200),
            "large.py": generate_content(500),
        }
        run_all_checks(upy_v1_hex, files_dict)

    def test_unicode_content(self, upy_v1_hex: str) -> None:
        """Test files with unicode content."""
        files_dict = {
            "hello.py": "print('Hello, 世界!')",
            "emoji.py": "# 🐍 Python",
            "世界.py": "More content with\nunicode filename.",
        }
        run_all_checks(upy_v1_hex, files_dict)

    def test_empty_filesystem_read(self, upy_v1_hex: str) -> None:
        """Test reading from a hex with no files."""
        # Python should return empty dict
        py_files = py_get_files(upy_v1_hex)
        assert py_files == {}, f"Python should return empty dict, got: {py_files}"

        # JS throws an error for empty filesystem
        with pytest.raises(JSEvalException) as exc_info:
            js_get_files(upy_v1_hex)
        assert "does not have any files" in str(exc_info.value)
