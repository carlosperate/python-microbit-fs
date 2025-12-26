"""Tests for the File class validation and properties."""

import pytest

from microbit_micropython_fs import File, InvalidFileError


class TestFileValidation:
    """Tests for File class validation."""

    def test_empty_filename_raises_error(self) -> None:
        """Empty filename should raise InvalidFileError."""
        with pytest.raises(InvalidFileError, match="cannot be empty"):
            File(name="", content=b"some content")

    def test_empty_content_raises_error(self) -> None:
        """Empty content should raise InvalidFileError."""
        with pytest.raises(InvalidFileError, match="cannot be empty"):
            File(name="empty.py", content=b"")

    def test_filename_too_long_raises_error(self) -> None:
        """Filename longer than 120 bytes should raise InvalidFileError."""
        long_name = "a" * 121
        with pytest.raises(InvalidFileError, match="too long"):
            File(name=long_name, content=b"x")


class TestFilenameBoundaries:
    """Tests for filename length boundary conditions."""

    def test_filename_exactly_120_chars_succeeds(self, upy_v1_hex: str) -> None:
        """Filename of exactly 120 characters should succeed."""
        from microbit_micropython_fs import add_files, get_files

        name_120 = "a" * 116 + ".txt"  # 116 + 4 = 120
        assert len(name_120) == 120

        files = [File.from_text(name_120, "content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == name_120

    def test_filename_119_chars_succeeds(self, upy_v1_hex: str) -> None:
        """Filename of 119 characters should succeed."""
        from microbit_micropython_fs import add_files, get_files

        name_119 = "a" * 115 + ".txt"  # 115 + 4 = 119
        assert len(name_119) == 119

        files = [File.from_text(name_119, "content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == name_119

    def test_filename_121_chars_fails(self) -> None:
        """Filename of 121 characters should fail."""
        name_121 = "a" * 117 + ".txt"  # 117 + 4 = 121
        assert len(name_121) == 121

        with pytest.raises(InvalidFileError, match="too long"):
            File.from_text(name_121, "content")

    def test_filename_single_char_succeeds(self, upy_v1_hex: str) -> None:
        """Single character filename should succeed."""
        from microbit_micropython_fs import add_files, get_files

        files = [File.from_text("x", "content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "x"


class TestFilenameSpecialCases:
    """Tests for special filename patterns."""

    def test_filename_with_dots(self, upy_v1_hex: str) -> None:
        """Filename with multiple dots should work."""
        from microbit_micropython_fs import add_files, get_files

        files = [File.from_text("my.file.name.py", "content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "my.file.name.py"

    def test_filename_starting_with_dot(self, upy_v1_hex: str) -> None:
        """Filename starting with dot (hidden file) should work."""
        from microbit_micropython_fs import add_files, get_files

        files = [File.from_text(".hidden", "secret content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == ".hidden"

    def test_filename_with_numbers(self, upy_v1_hex: str) -> None:
        """Filename with numbers should work."""
        from microbit_micropython_fs import add_files, get_files

        files = [File.from_text("file123.py", "content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "file123.py"

    def test_filename_all_numbers(self, upy_v1_hex: str) -> None:
        """Filename that is all numbers should work."""
        from microbit_micropython_fs import add_files, get_files

        files = [File.from_text("12345", "content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "12345"

    def test_filename_with_spaces(self, upy_v1_hex: str) -> None:
        """Filename with spaces should work."""
        from microbit_micropython_fs import add_files, get_files

        files = [File.from_text("my file.py", "content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "my file.py"

    def test_filename_no_extension(self, upy_v1_hex: str) -> None:
        """Filename without extension should work."""
        from microbit_micropython_fs import add_files, get_files

        files = [File.from_text("README", "content")]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == "README"

    def test_filename_case_sensitive(self, upy_v1_hex: str) -> None:
        """Filenames should be case-sensitive."""
        from microbit_micropython_fs import add_files, get_files

        files = [
            File.from_text("File.py", "upper"),
            File.from_text("file.py", "lower"),
        ]
        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 2
        file_dict = {f.name: f.content for f in read_files}
        assert file_dict["File.py"] == b"upper"
        assert file_dict["file.py"] == b"lower"


class TestFileProperties:
    """Tests for File class properties."""

    def test_file_size_property(self) -> None:
        """File.size should return content length."""
        content = b"hello world"
        f = File(name="test.txt", content=content)
        assert f.size == len(content)

    def test_file_size_fs_property(self) -> None:
        """File.size_fs should return filesystem storage size."""
        # Small file should use one chunk (128 bytes)
        f = File.from_text("small.py", "x=1")
        assert f.size_fs == 128

        # Larger file should use multiple chunks
        f = File.from_text("large.py", "x" * 200)
        assert f.size_fs > 128
        assert f.size_fs % 128 == 0  # Should be multiple of chunk size

    def test_file_get_text(self) -> None:
        """File.get_text should decode content."""
        content = "Hello, 世界!"
        f = File.from_text("test.py", content)
        assert f.get_text() == content

    def test_file_get_text_custom_encoding(self) -> None:
        """File.get_text with custom encoding."""
        content = "Hello"
        f = File(name="test.txt", content=content.encode("latin-1"))
        assert f.get_text(encoding="latin-1") == content
