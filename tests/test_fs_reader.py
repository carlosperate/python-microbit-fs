"""Tests for reading files from the MicroPython filesystem."""

from io import StringIO

from intelhex import IntelHex

from micropython_microbit_fs import get_device_info, get_files
from micropython_microbit_fs.filesystem import get_fs_start_address


class TestGetFilesEmpty:
    """Test get_files with filesystems that have no files."""

    def test_v1_empty_filesystem(self, upy_v1_hex: str) -> None:
        """V1 hex with no files should return empty list."""
        files = get_files(upy_v1_hex)
        assert files == []

    def test_v2_uicr_empty_filesystem(self, upy_v2_uicr_hex: str) -> None:
        """V2 UICR hex with no files should return empty list."""
        files = get_files(upy_v2_uicr_hex)
        assert files == []

    def test_v2_region_empty_filesystem(self, upy_v2_region_hex: str) -> None:
        """V2 Region hex with no files should return empty list."""
        files = get_files(upy_v2_region_hex)
        assert files == []


class TestGetFilesWithData:
    """Test get_files with filesystems that have files embedded."""

    def test_read_single_small_file(self, upy_v1_hex: str) -> None:
        """Test reading a single small file that fits in one chunk."""
        # This hex fragment represents a file "afirst.py" with content "firstname = 'Carlos'"
        # at address 0x3DF00 (which is in V1 filesystem region)
        # The chunk format:
        # Byte 0: 0xFE (FILE_START)
        # Byte 1: 0x1F (end offset = 31 = 2 + 9 + 20)
        # Byte 2: 0x09 (filename length = 9)
        # Bytes 3-11: "afirst.py"
        # Bytes 12-31: "firstname = 'Carlos'"
        # Byte 127: 0xFF (no next chunk)
        afirst_hex_fragment = (
            ":020000040003F7\n"
            ":10DF0000FE1F096166697273742E70796669727397\n"
            ":10DF1000746E616D65203D20274361726C6F7327BD\n"
            ":00000001FF\n"
        )

        ih_base = IntelHex()
        ih_base.loadhex(StringIO(upy_v1_hex))

        ih_fragment = IntelHex()
        ih_fragment.loadhex(StringIO(afirst_hex_fragment))

        # Merge the file data into the base hex
        ih_base.merge(ih_fragment, overlap="replace")

        # Convert back to string
        output = StringIO()
        ih_base.write_hex_file(output)
        merged_hex = output.getvalue()

        files = get_files(merged_hex)

        assert len(files) == 1
        assert files[0].name == "afirst.py"
        assert files[0].content == b"firstname = 'Carlos'"

    def test_read_multi_chunk_file(self, upy_v1_hex: str) -> None:
        """Test reading a file that spans multiple chunks."""
        # Create a file that uses 2 chunks
        # Chunk 1 at address 0x3DF00, chunk 2 at 0x3DF80
        # This uses chunks at indices that would be valid for V1 FS
        # For simplicity, let's create the data directly
        ih_base = IntelHex()
        ih_base.loadhex(StringIO(upy_v1_hex))

        # Calculate filesystem start for V1 (around 0x38C00 based on device info)
        # We'll use chunk 1 at fs_start + 0 and chunk 2 at fs_start + 128
        device_info = get_device_info(upy_v1_hex)

        # Use effective start (accounting for max chunks limit)
        fs_start = get_fs_start_address(device_info)
        chunk1_addr = fs_start
        chunk2_addr = fs_start + 128

        # Create a file "test.txt" with content that spans 2 chunks
        filename = "test.txt"
        # In first chunk: byte 0 = marker, bytes 1-126 = data area (126 bytes), byte 127 = tail
        # Header in data area: byte 1 = end_offset, byte 2 = name_len, bytes 3-10 = name (8 bytes)
        # Content starts at byte 11, can use bytes 11-126 = 116 bytes
        # For second chunk: byte 0 = back pointer, bytes 1-126 = 126 bytes of data, byte 127 = tail
        # Total content space: 116 + 126 = 242 bytes (but we just need to span 2 chunks)
        # We'll use 116 + 14 = 130 bytes to test
        first_chunk_content_space = 126 - (2 + len(filename))  # 116 bytes
        content = b"A" * first_chunk_content_space + b"B" * 14  # 130 bytes

        # Build chunk 1 (FILE_START)
        chunk1 = bytearray(128)
        chunk1[0] = 0xFE  # FILE_START
        # end_offset is where data ends in the last chunk (1-based within data area)
        # In chunk2: back pointer at 0, then 14 bytes of 'B', so end_offset = 14
        end_offset = 14
        chunk1[1] = end_offset
        chunk1[2] = len(filename)
        chunk1[3 : 3 + len(filename)] = filename.encode("utf-8")
        data_start = 3 + len(filename)  # = 11
        first_chunk_data = content[:first_chunk_content_space]
        chunk1[data_start : data_start + len(first_chunk_data)] = first_chunk_data
        # No need to fill rest - chunk is initialized with zeros, but we want 0xFF
        for i in range(data_start + len(first_chunk_data), 127):
            chunk1[i] = 0xFF
        chunk1[127] = 2  # Point to chunk index 2

        # Build chunk 2 (continuation)
        chunk2 = bytearray(128)
        chunk2[0] = 1  # Previous chunk index (back pointer)
        remaining_content = content[len(first_chunk_data) :]
        chunk2[1 : 1 + len(remaining_content)] = remaining_content
        # Fill rest with 0xFF
        for i in range(1 + len(remaining_content), 128):
            chunk2[i] = 0xFF

        # Write chunks to hex
        for i, byte in enumerate(chunk1):
            ih_base[chunk1_addr + i] = byte
        for i, byte in enumerate(chunk2):
            ih_base[chunk2_addr + i] = byte

        # Convert back to string
        output = StringIO()
        ih_base.write_hex_file(output)
        merged_hex = output.getvalue()

        files = get_files(merged_hex)

        assert len(files) == 1
        assert files[0].name == "test.txt"
        assert files[0].content == content

    def test_read_multiple_files(self, upy_v1_hex: str) -> None:
        """Test reading multiple files from the filesystem."""
        ih_base = IntelHex()
        ih_base.loadhex(StringIO(upy_v1_hex))

        device_info = get_device_info(upy_v1_hex)
        fs_start = get_fs_start_address(device_info)

        # Create two small files
        files_to_create = [
            ("file1.py", b"# File 1 content"),
            ("file2.py", b"# File 2 content"),
        ]

        chunk_addr = fs_start
        for filename, content in files_to_create:
            chunk = bytearray(128)
            chunk[0] = 0xFE  # FILE_START
            header_size = 2 + len(filename)
            end_offset = (header_size + len(content)) % 126
            if end_offset == 0:
                end_offset = 126
            chunk[1] = end_offset
            chunk[2] = len(filename)
            chunk[3 : 3 + len(filename)] = filename.encode("utf-8")
            data_start = 3 + len(filename)
            chunk[data_start : data_start + len(content)] = content
            # Fill rest with 0xFF
            for i in range(data_start + len(content), 128):
                chunk[i] = 0xFF

            for i, byte in enumerate(chunk):
                ih_base[chunk_addr + i] = byte
            chunk_addr += 128

        # Convert back to string
        output = StringIO()
        ih_base.write_hex_file(output)
        merged_hex = output.getvalue()

        files = get_files(merged_hex)

        assert len(files) == 2
        filenames = {f.name for f in files}
        assert filenames == {"file1.py", "file2.py"}

        for f in files:
            if f.name == "file1.py":
                assert f.content == b"# File 1 content"
            else:
                assert f.content == b"# File 2 content"
