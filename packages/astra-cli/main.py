import json
from dataclasses import asdict
from pathlib import Path

import typer

from astra_core import (
    AnalysisReport,
    CodeUnit,
    SimilarityScore,
    analyze_code_similarity,
)

app = typer.Typer()


def load_file(path: Path) -> CodeUnit:
    if not path.exists():
        raise typer.BadParameter(f"Path does not exist: {path}")

    if not path.is_file():
        raise typer.BadParameter(f"Path is not a file: {path}")

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise typer.BadParameter(f"Could not read {path}: {exc}") from exc

    return CodeUnit(
        id=str(path),
        content=content,
    )


def validate_threshold(threshold: float) -> None:
    if not 0.0 <= threshold <= 1.0:
        raise typer.BadParameter("Threshold must be between 0.0 and 1.0")


def format_score(score: SimilarityScore) -> str:
    return (
        f"  {score.unit_a} <-> {score.unit_b}  "
        f"score={score.score:.4f}  alignments={score.alignment_count}"
    )


def print_text_report(report: AnalysisReport, top: int) -> None:
    typer.echo("ASTRA Similarity Report")
    typer.echo(f"Threshold: {report.threshold:.2f}")
    typer.echo(f"Files analyzed: {report.total_units}")
    typer.echo(f"Pairs compared: {len(report.scores)}")
    typer.echo(f"Flagged pairs: {len(report.flagged_pairs)}")
    typer.echo()

    typer.echo("Flagged pairs:")
    if report.flagged_pairs:
        for score in report.flagged_pairs:
            typer.echo(f"  {score.unit_a} <-> {score.unit_b}  score={score.score:.4f}")
    else:
        typer.echo("  None")

    typer.echo()
    typer.echo("Top scores:")
    if report.scores and top > 0:
        for score in report.scores[:top]:
            typer.echo(format_score(score))
    else:
        typer.echo("  None")


@app.command()
def analyze(
    paths: list[Path] = typer.Argument(..., help="Paths to code files"),
    threshold: float = 0.8,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Print the full report as JSON.",
    ),
    top: int = typer.Option(
        10,
        "--top",
        min=0,
        help="Number of top pair scores to show in text mode.",
    ),
):
    if len(paths) < 2:
        raise typer.BadParameter("Analyze requires at least two files")

    validate_threshold(threshold)
    units = [load_file(path) for path in paths]

    try:
        result = analyze_code_similarity(units=units, threshold=threshold)
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if json_output:
        typer.echo(json.dumps(asdict(result), indent=2))
    else:
        print_text_report(result, top)


if __name__ == "__main__":
    app()
