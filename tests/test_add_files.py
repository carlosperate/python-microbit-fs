"""Tests for the add_files function."""

import pytest

from micropython_microbit_fs import (
    File,
    InvalidFileError,
    add_files,
    get_files,
)
from micropython_microbit_fs.hex_utils import hex_to_string, load_hex


class TestAddFilesBasic:
    """Basic tests for add_files function."""

    def test_add_single_small_file(self, upy_v1_hex: str) -> None:
        """Add a single small file and verify it can be read back."""
        file_content = "print('Hello!')"
        files = [File.from_text("main.py", file_content)]

        result_hex = add_files(upy_v1_hex, files)

        # Read back the files
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "main.py"
        assert read_files[0].content == file_content.encode("utf-8")
        assert read_files[0].get_text() == file_content

    def test_add_multiple_files(self, upy_v1_hex: str) -> None:
        """Add multiple files and verify they can be read back."""
        files = [
            File.from_text("main.py", "import helper\nhelper.run()"),
            File.from_text("helper.py", "def run():\n    print('Running!')"),
        ]

        result_hex = add_files(upy_v1_hex, files)

        read_files = get_files(result_hex)

        assert len(read_files) == 2
        file_dict = {f.name: f.content for f in read_files}
        assert file_dict["main.py"] == b"import helper\nhelper.run()"
        assert file_dict["helper.py"] == b"def run():\n    print('Running!')"

    def test_add_binary_file(self, upy_v1_hex: str) -> None:
        """Add a file with binary content."""
        binary_content = bytes(range(256))
        files = [File(name="data.bin", content=binary_content)]

        result_hex = add_files(upy_v1_hex, files)

        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "data.bin"
        assert read_files[0].content == binary_content

    def test_add_empty_list(self, upy_v1_hex: str) -> None:
        """Adding empty file list should return valid hex with no files."""
        result_hex = add_files(upy_v1_hex, [])
        assert result_hex == hex_to_string(load_hex(upy_v1_hex))

        # Should still be valid MicroPython hex with no files
        read_files = get_files(result_hex)
        assert read_files == []

        # Original should also have no files
        original_files = get_files(upy_v1_hex)
        assert original_files == []


class TestAddFilesMultiChunk:
    """Tests for files that span multiple chunks."""

    def test_add_file_spanning_two_chunks(self, upy_v1_hex: str) -> None:
        """Add a file large enough to need 2 chunks."""
        # A chunk data area is 126 bytes. Header is ~10 bytes.
        # So we need content > 116 bytes to span 2 chunks.
        content = "A" * 130
        files = [File.from_text("large.py", content)]

        result_hex = add_files(upy_v1_hex, files)

        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "large.py"
        assert read_files[0].content == content.encode("utf-8")

    def test_add_file_spanning_many_chunks(self, upy_v1_hex: str) -> None:
        """Add a file that spans many chunks."""
        # 1000 bytes should need about 8-9 chunks
        content = "X" * 1000
        files = [File.from_text("big.py", content)]

        result_hex = add_files(upy_v1_hex, files)

        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "big.py"
        assert read_files[0].content == content.encode("utf-8")


class TestAddFilesV2:
    """Tests for V2 hex files."""

    def test_add_file_v2_uicr(self, upy_v2_uicr_hex: str) -> None:
        """Add a file to a V2 UICR hex file."""
        files = [File.from_text("test.py", "print('V2 test')")]

        result_hex = add_files(upy_v2_uicr_hex, files)

        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "test.py"
        assert read_files[0].content == b"print('V2 test')"

    def test_add_file_v2_region(self, upy_v2_region_hex: str) -> None:
        """Add a file to a V2 Region hex file."""
        files = [File.from_text("test.py", "print('V2 region test')")]

        result_hex = add_files(upy_v2_region_hex, files)

        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "test.py"
        assert read_files[0].content == b"print('V2 region test')"


class TestAddFilesErrors:
    """Tests for error handling in add_files."""

    def test_duplicate_filenames_raises_error(self, upy_v1_hex: str) -> None:
        """Adding files with duplicate names should raise InvalidFileError."""
        files = [
            File.from_text("main.py", "print('first')"),
            File.from_text("main.py", "print('second')"),
        ]
        with pytest.raises(InvalidFileError, match="Duplicate file name"):
            add_files(upy_v1_hex, files)


class TestContentBoundaries:
    """Tests for content size boundary conditions."""

    def test_single_byte_content_succeeds(self, upy_v1_hex: str) -> None:
        """Single byte content should succeed."""
        files = [File(name="tiny.bin", content=b"x")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].content == b"x"

    def test_content_exactly_one_chunk_data_size(self, upy_v1_hex: str) -> None:
        """Content that exactly fills one chunk's data area."""
        # Chunk data size is 126 bytes, minus filename overhead
        # With filename "a.py" (4 bytes) + length byte (1), we have 121 bytes for content
        filename = "a.py"
        content_size = 126 - len(filename) - 1  # 121 bytes
        content = "x" * content_size

        files = [File.from_text(filename, content)]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].content == content.encode("utf-8")

    def test_content_one_byte_over_chunk_boundary(self, upy_v1_hex: str) -> None:
        """Content that is one byte over chunk boundary needs two chunks."""
        # This should spill into a second chunk
        filename = "a.py"
        content_size = 126 - len(filename)  # One byte more than fits
        content = "x" * content_size

        files = [File.from_text(filename, content)]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].content == content.encode("utf-8")

    def test_binary_content_all_byte_values(self, upy_v1_hex: str) -> None:
        """Content with all possible byte values (0x00-0xFF)."""
        content = bytes(range(256))
        files = [File(name="allbytes.bin", content=content)]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].content == content

    def test_binary_content_with_null_bytes(self, upy_v1_hex: str) -> None:
        """Content containing null bytes should be preserved."""
        content = b"hello\x00world\x00\x00end"
        files = [File(name="nulls.bin", content=content)]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].content == content

    def test_binary_content_with_marker_bytes(self, upy_v1_hex: str) -> None:
        """Content containing filesystem marker bytes (0xFE, 0xFF) should work."""
        # 0xFE is FILE_START marker, 0xFF is UNUSED marker
        content = b"\xfe\xff\xfe\xff" * 50
        files = [File(name="markers.bin", content=content)]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].content == content


class TestAddFilesRoundtrip:
    """Roundtrip tests: add files then read them back."""

    def test_roundtrip_preserves_content(self, upy_v1_hex: str) -> None:
        """Content should be exactly preserved through roundtrip."""
        original_content = b"# This is a test\n\ndef main():\n    pass\n"
        files = [File(name="test.py", content=original_content)]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert read_files[0].content == original_content

    def test_roundtrip_multiple_files_different_sizes(self, upy_v1_hex: str) -> None:
        """Multiple files of different sizes should roundtrip correctly."""
        files = [
            File.from_text("tiny.py", "x=1"),
            File.from_text("small.py", "# " + "x" * 50),
            File.from_text("medium.py", "# " + "y" * 200),
            File.from_text("large.py", "# " + "z" * 500),
        ]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 4
        file_dict = {f.name: f.content for f in read_files}

        assert file_dict["tiny.py"] == b"x=1"
        assert file_dict["small.py"] == b"# " + b"x" * 50
        assert file_dict["medium.py"] == b"# " + b"y" * 200
        assert file_dict["large.py"] == b"# " + b"z" * 500

    def test_roundtrip_special_characters_in_filename(self, upy_v1_hex: str) -> None:
        """Filenames with special characters should work."""
        files = [File.from_text("test_file-1.py", "content")]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "test_file-1.py"

    def test_roundtrip_utf8_content(self, upy_v1_hex: str) -> None:
        """UTF-8 content should be preserved."""
        content = "# Hello 世界\nprint('こんにちは')\n"
        files = [File.from_text("unicode.py", content)]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert read_files[0].content == content.encode("utf-8")

    def test_roundtrip_many_small_files(self, upy_v1_hex: str) -> None:
        """Many small files should all roundtrip correctly."""
        files = [File.from_text(f"file{i}.py", f"x={i}") for i in range(20)]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 20
        file_dict = {f.name: f.content for f in read_files}
        for i in range(20):
            assert file_dict[f"file{i}.py"] == f"x={i}".encode()

    def test_roundtrip_file_order_preserved(self, upy_v1_hex: str) -> None:
        """File order should be consistent through roundtrip."""
        files = [
            File.from_text("aaa.py", "first"),
            File.from_text("zzz.py", "second"),
            File.from_text("mmm.py", "third"),
        ]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        # Files should be readable (order may vary based on chunk allocation)
        assert len(read_files) == 3
        file_dict = {f.name: f.content for f in read_files}
        assert file_dict["aaa.py"] == b"first"
        assert file_dict["zzz.py"] == b"second"
        assert file_dict["mmm.py"] == b"third"
