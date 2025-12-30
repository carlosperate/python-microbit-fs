"""Tests for the CLI module."""

from pathlib import Path

import pytest

from microbit_micropython_fs.cli import app


class TestInfoCommand:
    """Tests for the info command."""

    def test_info_displays_device_information(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Info command should display device information."""
        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        app(["info", str(hex_file)])

        captured = capsys.readouterr()
        assert "Device: micro:bit V1" in captured.out
        assert "MicroPython version:" in captured.out
        assert "Flash page size:" in captured.out
        assert "Filesystem size:" in captured.out
        assert "Filesystem start:" in captured.out
        assert "Filesystem end:" in captured.out

    def test_info_v2_hex(
        self, upy_v2_region_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Info command should work with V2 hex files."""
        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v2_region_hex)

        app(["info", str(hex_file)])

        captured = capsys.readouterr()
        assert "Device: micro:bit V2" in captured.out


class TestListCommand:
    """Tests for the list command."""

    def test_list_empty_filesystem(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """List command should report no files for empty filesystem."""
        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        app(["list", str(hex_file)])

        captured = capsys.readouterr()
        assert "No files found" in captured.out

    def test_list_with_files(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """List command should show files in the filesystem."""
        import microbit_micropython_fs as upyfs

        # Add files to hex
        files = [
            upyfs.File.from_text("main.py", "print('hello')"),
            upyfs.File.from_text("helper.py", "def foo(): pass"),
        ]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)

        app(["list", str(hex_file)])

        captured = capsys.readouterr()
        assert "main.py" in captured.out
        assert "helper.py" in captured.out
        assert "2 files" in captured.out


class TestExtractCommand:
    """Tests for the get command."""

    def test_extract_empty_filesystem(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Extract command should report no files for empty filesystem."""
        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        app(["get", str(hex_file)])

        captured = capsys.readouterr()
        assert "No files found" in captured.out

    def test_extract_all_files(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Get command should extract all files to output directory."""
        import microbit_micropython_fs as upyfs

        # Add files to hex
        files = [
            upyfs.File.from_text("main.py", "print('hello')"),
            upyfs.File.from_text("data.txt", "some data"),
        ]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)
        output_dir = tmp_path / "output"

        app(["get", str(hex_file), "--output-dir", str(output_dir)])

        captured = capsys.readouterr()
        assert "Extracted: main.py" in captured.out
        assert "Extracted: data.txt" in captured.out
        assert (output_dir / "main.py").read_text() == "print('hello')"
        assert (output_dir / "data.txt").read_text() == "some data"

    def test_extract_specific_file(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Get command should extract only the specified file."""
        import microbit_micropython_fs as upyfs

        # Add files to hex
        files = [
            upyfs.File.from_text("main.py", "print('hello')"),
            upyfs.File.from_text("other.py", "print('other')"),
        ]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)
        output_dir = tmp_path / "output"

        app(
            [
                "get",
                str(hex_file),
                "--output-dir",
                str(output_dir),
                "--filename",
                "main.py",
            ]
        )

        captured = capsys.readouterr()
        assert "Extracted: main.py" in captured.out
        assert "Extracted: other.py" not in captured.out
        assert (output_dir / "main.py").exists()
        assert not (output_dir / "other.py").exists()

    def test_extract_nonexistent_file(self, upy_v1_hex: str, tmp_path: Path) -> None:
        """Get command should error when specific file is not found."""
        import microbit_micropython_fs as upyfs

        # Add files to hex
        files = [upyfs.File.from_text("main.py", "print('hello')")]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)

        with pytest.raises(SystemExit) as exc_info:
            app(["get", str(hex_file), "--filename", "nonexistent.py"])

        assert "File not found" in str(exc_info.value)

    def test_extract_fails_if_file_exists(
        self, upy_v1_hex: str, tmp_path: Path
    ) -> None:
        """Get command should fail if output file already exists."""
        import microbit_micropython_fs as upyfs

        # Add files to hex
        files = [upyfs.File.from_text("main.py", "print('hello')")]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)

        # Create existing file
        existing_file = tmp_path / "main.py"
        existing_file.write_text("existing content")

        with pytest.raises(SystemExit) as exc_info:
            app(["get", str(hex_file), "--output-dir", str(tmp_path)])

        assert "Files already exist" in str(exc_info.value)
        assert "main.py" in str(exc_info.value)
        # Original file should not be overwritten
        assert existing_file.read_text() == "existing content"

    def test_extract_with_force_overwrites_existing(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Get command with --force should overwrite existing files."""
        import microbit_micropython_fs as upyfs

        # Add files to hex
        files = [upyfs.File.from_text("main.py", "print('new content')")]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)

        # Create existing file
        existing_file = tmp_path / "main.py"
        existing_file.write_text("existing content")

        app(["get", str(hex_file), "--output-dir", str(tmp_path), "--force"])

        captured = capsys.readouterr()
        assert "Extracted: main.py" in captured.out
        # File should be overwritten
        assert existing_file.read_text() == "print('new content')"


class TestAddCommand:
    """Tests for the add command."""

    def test_add_single_file(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Add command should add a single file to the hex."""
        import microbit_micropython_fs as upyfs

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        output_file = tmp_path / "output.hex"

        app(["add", str(hex_file), str(source_file), "--output", str(output_file)])

        captured = capsys.readouterr()
        assert "Adding: main.py" in captured.out
        assert f"Written to: {output_file}" in captured.out

        # Verify the file was added
        result_hex = output_file.read_text()
        files = upyfs.get_files(result_hex)
        assert len(files) == 1
        assert files[0].name == "main.py"
        assert files[0].get_text() == "print('hello')"

    def test_add_multiple_files(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Add command should add multiple files to the hex."""
        import microbit_micropython_fs as upyfs

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        file1 = tmp_path / "main.py"
        file1.write_text("print('main')")
        file2 = tmp_path / "helper.py"
        file2.write_text("def helper(): pass")

        output_file = tmp_path / "output.hex"

        app(
            ["add", str(hex_file), str(file1), str(file2), "--output", str(output_file)]
        )

        captured = capsys.readouterr()
        assert "Adding: main.py" in captured.out
        assert "Adding: helper.py" in captured.out

        # Verify files were added
        result_hex = output_file.read_text()
        files = upyfs.get_files(result_hex)
        assert len(files) == 2
        file_names = {f.name for f in files}
        assert file_names == {"main.py", "helper.py"}

    def test_add_creates_output_file_by_default(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Add command should create <name>_output.hex when no output specified."""
        import microbit_micropython_fs as upyfs

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        app(["add", str(hex_file), str(source_file)])

        expected_output = tmp_path / "test_output.hex"
        captured = capsys.readouterr()
        assert f"Written to: {expected_output}" in captured.out

        # Verify the file was created with the added file
        assert expected_output.exists()
        result_hex = expected_output.read_text()
        files = upyfs.get_files(result_hex)
        assert len(files) == 1
        assert files[0].name == "main.py"

        # Original file should be unchanged (no files)
        original_hex = hex_file.read_text()
        original_files = upyfs.get_files(original_hex)
        assert len(original_files) == 0


class TestVersionAndHelp:
    """Tests for --version and --help flags."""

    def test_version_flag(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--version should display the version."""
        import microbit_micropython_fs as upyfs

        app(["--version"])

        captured = capsys.readouterr()
        assert upyfs.__version__ in captured.out

    def test_help_flag(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--help should display help information."""
        app(["--help"])

        captured = capsys.readouterr()
        assert "info" in captured.out
        assert "list" in captured.out
        assert "get" in captured.out
        assert "add" in captured.out
