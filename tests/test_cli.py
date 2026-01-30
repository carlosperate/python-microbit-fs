"""Tests for the CLI module."""

from pathlib import Path

import pytest

import micropython_microbit_fs as upyfs
from micropython_microbit_fs.cli import app


class TestInfoCommand:
    """Tests for the info command."""

    def test_info_displays_device_information(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Info command should display device information."""
        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        try:
            app(["info", str(hex_file)])
        except SystemExit as e:
            assert e.code == 0

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

        try:
            app(["info", str(hex_file)])
        except SystemExit as e:
            assert e.code == 0

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

        try:
            app(["list", str(hex_file)])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "No files found" in captured.out

    def test_list_with_files(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """List command should show files in the filesystem."""
        files = [
            upyfs.File.from_text("main.py", "print('hello')"),
            upyfs.File.from_text("helper.py", "def foo(): pass"),
        ]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)

        try:
            app(["list", str(hex_file)])
        except SystemExit as e:
            assert e.code == 0

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

        try:
            app(["get", str(hex_file)])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "No files found" in captured.out

    def test_extract_all_files(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Get command should extract all files to output directory."""
        files = [
            upyfs.File.from_text("main.py", "print('hello')"),
            upyfs.File.from_text("data.txt", "some data"),
        ]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)
        output_dir = tmp_path / "output"

        try:
            app(["get", str(hex_file), "--output-dir", str(output_dir)])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Extracted: main.py" in captured.out
        assert "Extracted: data.txt" in captured.out
        assert (output_dir / "main.py").read_text() == "print('hello')"
        assert (output_dir / "data.txt").read_text() == "some data"

    def test_extract_specific_file(
        self, upy_v1_hex: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Get command should extract only the specified file."""
        files = [
            upyfs.File.from_text("main.py", "print('hello')"),
            upyfs.File.from_text("other.py", "print('other')"),
        ]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)
        output_dir = tmp_path / "output"

        try:
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
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Extracted: main.py" in captured.out
        assert "Extracted: other.py" not in captured.out
        assert (output_dir / "main.py").exists()
        assert not (output_dir / "other.py").exists()

    def test_extract_nonexistent_file(self, upy_v1_hex: str, tmp_path: Path) -> None:
        """Get command should error when specific file is not found."""
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
        files = [upyfs.File.from_text("main.py", "print('new content')")]
        new_hex = upyfs.add_files(upy_v1_hex, files)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(new_hex)

        # Create existing file
        existing_file = tmp_path / "main.py"
        existing_file.write_text("existing content")

        try:
            app(["get", str(hex_file), "--output-dir", str(tmp_path), "--force"])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Extracted: main.py" in captured.out
        # File should be overwritten
        assert existing_file.read_text() == "print('new content')"


class TestAddCommand:
    """Tests for the add command."""

    def test_add_single_file(
        self,
        upy_v1_hex: str,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Add command should add a single file to the hex."""
        # Output is now rooted in the current working directory
        monkeypatch.chdir(tmp_path)
        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        output_file = tmp_path / "output.hex"

        try:
            app(
                [
                    "add",
                    str(source_file),
                    "--hex-file",
                    str(hex_file),
                    "--output",
                    str(output_file),
                ]
            )
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Adding: main.py" in captured.out
        assert "Written to: output.hex" in captured.out

        # Verify the file was added
        result_hex = output_file.read_text()
        files = upyfs.get_files(result_hex)
        assert len(files) == 1
        assert files[0].name == "main.py"
        assert files[0].get_text() == "print('hello')"

    def test_add_multiple_files(
        self,
        upy_v1_hex: str,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Add command should add multiple files to the hex."""
        # Ensure output path is relative to cwd
        monkeypatch.chdir(tmp_path)
        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        file1 = tmp_path / "main.py"
        file1.write_text("print('main')")
        file2 = tmp_path / "helper.py"
        file2.write_text("def helper(): pass")

        output_file = tmp_path / "output.hex"

        try:
            app(
                [
                    "add",
                    str(file1),
                    str(file2),
                    "--hex-file",
                    str(hex_file),
                    "--output",
                    str(output_file),
                ]
            )
        except SystemExit as e:
            assert e.code == 0

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
        self,
        upy_v1_hex: str,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Add command should create <name>_output.hex when no output specified."""
        # Output now defaults to the current working directory, so run in tmp_path
        monkeypatch.chdir(tmp_path)

        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        try:
            app(["add", str(source_file), "--hex-file", str(hex_file)])
        except SystemExit as e:
            assert e.code == 0

        expected_output = Path("test_output.hex")
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


class TestAddWithBundledHex:
    """Tests for the add command with bundled hex files."""

    def test_add_with_v1_latest(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Add command with --v1=latest should use bundled V1 hex."""
        monkeypatch.chdir(tmp_path)
        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        output_file = tmp_path / "output.hex"

        try:
            app(["add", str(source_file), "--v1=latest", "--output", str(output_file)])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Using bundled micro:bit V1 MicroPython" in captured.out
        assert "Adding: main.py" in captured.out
        assert "Written to: output.hex" in captured.out

        # Verify the file was added and it's a V1 hex
        result_hex = output_file.read_text()
        files = upyfs.get_files(result_hex)
        assert len(files) == 1
        assert files[0].name == "main.py"

        device_info = upyfs.get_device_info(result_hex)
        assert device_info.device_version == upyfs.DeviceVersion.V1

    def test_add_with_v2_latest(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Add command with --v2=latest should use bundled V2 hex."""
        monkeypatch.chdir(tmp_path)
        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        output_file = tmp_path / "output.hex"

        try:
            app(["add", str(source_file), "--v2=latest", "--output", str(output_file)])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Using bundled micro:bit V2 MicroPython" in captured.out
        assert "Adding: main.py" in captured.out

        # Verify the file was added and it's a V2 hex
        result_hex = output_file.read_text()
        files = upyfs.get_files(result_hex)
        assert len(files) == 1
        assert files[0].name == "main.py"

        device_info = upyfs.get_device_info(result_hex)
        assert device_info.device_version == upyfs.DeviceVersion.V2

    def test_add_with_v1_specific_version(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Add command with --v1=version should use specific V1 version."""
        monkeypatch.chdir(tmp_path)
        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        output_file = tmp_path / "output.hex"

        try:
            app(["add", str(source_file), "--v1=1.1.1", "--output", str(output_file)])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Using bundled micro:bit V1 MicroPython v1.1.1" in captured.out

        # Verify the hex was created
        assert output_file.exists()

    def test_add_with_v2_specific_version(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Add command with --v2=version should use specific V2 version."""
        monkeypatch.chdir(tmp_path)
        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        output_file = tmp_path / "output.hex"

        try:
            app(["add", str(source_file), "--v2=2.1.2", "--output", str(output_file)])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Using bundled micro:bit V2 MicroPython v2.1.2" in captured.out

        # Verify the hex was created
        assert output_file.exists()

    def test_add_with_invalid_version(self, tmp_path: Path) -> None:
        """Add command with invalid version should error."""
        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        with pytest.raises(SystemExit) as exc_info:
            app(["add", str(source_file), "--v1=99.99.99"])

        assert "not found" in str(exc_info.value).lower()

    def test_add_error_both_v1_and_v2(self, tmp_path: Path) -> None:
        """Add command should error if both --v1 and --v2 are provided."""
        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        with pytest.raises(SystemExit) as exc_info:
            app(["add", str(source_file), "--v1=latest", "--v2=latest"])

        assert "Cannot combine" in str(exc_info.value)

    def test_add_error_hex_file_and_v1(self, upy_v1_hex: str, tmp_path: Path) -> None:
        """Add command should error if both hex_file and --v1 are provided."""
        hex_file = tmp_path / "test.hex"
        hex_file.write_text(upy_v1_hex)

        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        with pytest.raises(SystemExit) as exc_info:
            app(["add", str(source_file), "--hex-file", str(hex_file), "--v1=latest"])

        assert "Cannot combine" in str(exc_info.value)

    def test_add_error_no_hex_source(self, tmp_path: Path) -> None:
        """Add command should error if no hex source is provided."""
        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        with pytest.raises(SystemExit) as exc_info:
            app(["add", str(source_file)])

        assert "must provide" in str(exc_info.value).lower()

    def test_add_with_bundled_hex_default_output(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Add with bundled hex and no output should create output.hex."""
        # Change to tmp_path so output.hex is created there
        monkeypatch.chdir(tmp_path)

        source_file = tmp_path / "main.py"
        source_file.write_text("print('hello')")

        try:
            app(["add", str(source_file), "--v1=latest"])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "Written to: micropython-microbit-v1.1.1_output.hex" in captured.out
        assert (tmp_path / "micropython-microbit-v1.1.1_output.hex").exists()


class TestVersionsCommand:
    """Tests for the versions command."""

    def test_versions_lists_bundled_hexes(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Versions command should list available bundled hex versions."""
        try:
            app(["versions"])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "micro:bit V1" in captured.out
        assert "micro:bit V2" in captured.out
        # Check that at least some version is listed
        assert "1." in captured.out  # Versions like 1.1, 1.2, etc.


class TestVersionAndHelp:
    """Tests for --version and --help flags."""

    def test_version_flag(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--version should display the version."""
        try:
            app(["--version"])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert upyfs.__version__ in captured.out

    def test_help_flag(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--help should display help information."""
        try:
            app(["--help"])
        except SystemExit as e:
            assert e.code == 0

        captured = capsys.readouterr()
        assert "info" in captured.out
        assert "list" in captured.out
        assert "get" in captured.out
        assert "add" in captured.out
