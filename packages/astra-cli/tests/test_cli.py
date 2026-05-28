import importlib.util
import json
from pathlib import Path

from typer.testing import CliRunner


CLI_PATH = Path(__file__).resolve().parents[1] / "main.py"
SPEC = importlib.util.spec_from_file_location("astra_cli_main", CLI_PATH)
assert SPEC is not None
assert SPEC.loader is not None
astra_cli_main = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(astra_cli_main)

runner = CliRunner()


def write_python_file(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def test_cli_prints_text_report_for_valid_files(tmp_path: Path) -> None:
    left = write_python_file(tmp_path, "a.py", "def add(x, y): return x + y")
    right = write_python_file(tmp_path, "b.py", "def add(a, b): return a + b")

    result = runner.invoke(astra_cli_main.app, [str(left), str(right)])

    assert result.exit_code == 0
    assert "ASTRA Similarity Report" in result.output
    assert "Threshold" in result.output
    assert "0.80" in result.output
    assert "Files analyzed" in result.output
    assert "Pairs compared" in result.output
    assert "Flagged pairs" in result.output
    assert "Top scores" in result.output


def test_cli_flags_identical_logic(tmp_path: Path) -> None:
    left = write_python_file(tmp_path, "a.py", "def add(x, y): return x + y")
    right = write_python_file(tmp_path, "b.py", "def add(a, b): return a + b")

    result = runner.invoke(astra_cli_main.app, [str(left), str(right)])

    assert result.exit_code == 0
    assert str(left) in result.output
    assert str(right) in result.output
    assert "<->" in result.output
    assert "1.0000" in result.output


def test_cli_json_output_is_parseable(tmp_path: Path) -> None:
    left = write_python_file(tmp_path, "a.py", "x = 1")
    right = write_python_file(tmp_path, "b.py", "x = 2")

    result = runner.invoke(astra_cli_main.app, [str(left), str(right), "--json"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["threshold"] == 0.8
    assert data["total_units"] == 2
    assert "scores" in data
    assert "flagged_pairs" in data


def test_cli_requires_at_least_two_files(tmp_path: Path) -> None:
    path = write_python_file(tmp_path, "a.py", "x = 1")

    result = runner.invoke(astra_cli_main.app, [str(path)])

    assert result.exit_code != 0
    assert "at least two files" in result.output


def test_cli_reports_missing_path(tmp_path: Path) -> None:
    left = write_python_file(tmp_path, "a.py", "x = 1")
    missing = tmp_path / "missing.py"

    result = runner.invoke(astra_cli_main.app, [str(left), str(missing)])

    assert result.exit_code != 0
    assert str(missing) in result.output


def test_cli_reports_invalid_python(tmp_path: Path) -> None:
    left = write_python_file(tmp_path, "a.py", "x = 1")
    invalid = write_python_file(tmp_path, "broken.py", "def broken(:")

    result = runner.invoke(astra_cli_main.app, [str(left), str(invalid)])

    assert result.exit_code != 0
    assert "Failed to parse Python source" in result.output
    assert "broken.py" in result.output


def test_cli_rejects_threshold_below_zero(tmp_path: Path) -> None:
    left = write_python_file(tmp_path, "a.py", "x = 1")
    right = write_python_file(tmp_path, "b.py", "x = 2")

    result = runner.invoke(
        astra_cli_main.app,
        [str(left), str(right), "--threshold", "-1"],
    )

    assert result.exit_code != 0
    assert "Threshold must be between 0.0 and 1.0" in result.output


def test_cli_rejects_threshold_above_one(tmp_path: Path) -> None:
    left = write_python_file(tmp_path, "a.py", "x = 1")
    right = write_python_file(tmp_path, "b.py", "x = 2")

    result = runner.invoke(
        astra_cli_main.app,
        [str(left), str(right), "--threshold", "2"],
    )

    assert result.exit_code != 0
    assert "Threshold must be between 0.0 and 1.0" in result.output
