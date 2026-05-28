import json
from dataclasses import asdict
from pathlib import Path

import typer
from rich import box
from rich.console import Console
from rich.markup import escape
from rich.table import Table
from rich.text import Text

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


def build_summary_table(report: AnalysisReport) -> Table:
    table = Table(
        title="ASTRA Similarity Report",
        box=box.ROUNDED,
        show_header=False,
        border_style="cyan",
        title_style="bold cyan",
    )
    table.add_column("Metric", style="bold", no_wrap=True)
    table.add_column("Value", justify="right")
    table.add_row("Threshold", f"{report.threshold:.2f}")
    table.add_row("Files analyzed", str(report.total_units))
    table.add_row("Pairs compared", str(len(report.scores)))
    table.add_row("Flagged pairs", str(len(report.flagged_pairs)))
    return table


def build_pair_text(score: SimilarityScore) -> Text:
    return Text.assemble(
        (score.unit_a, "cyan"),
        " <-> ",
        (score.unit_b, "cyan"),
    )


def build_flagged_table(report: AnalysisReport) -> Table:
    table = Table(
        title="Flagged pairs",
        box=box.SIMPLE_HEAVY,
        border_style="red",
        header_style="bold red",
    )
    table.add_column("Pair", overflow="fold")
    table.add_column("Score", justify="right", no_wrap=True)

    if report.flagged_pairs:
        for score in report.flagged_pairs:
            table.add_row(build_pair_text(score), f"{score.score:.4f}")
    else:
        table.add_row(Text("None", style="dim"), "")

    return table


def build_top_scores_table(report: AnalysisReport, top: int) -> Table:
    table = Table(
        title="Top scores",
        box=box.SIMPLE_HEAVY,
        border_style="green",
        header_style="bold green",
    )
    table.add_column("Pair", overflow="fold")
    table.add_column("Score", justify="right", no_wrap=True)
    table.add_column("Alignments", justify="right", no_wrap=True)

    if report.scores and top > 0:
        for score in report.scores[:top]:
            table.add_row(
                build_pair_text(score),
                f"{score.score:.4f}",
                str(score.alignment_count),
            )
    else:
        table.add_row(Text("None", style="dim"), "", "")

    return table


def print_text_report(report: AnalysisReport, top: int) -> None:
    console = Console()
    console.print(build_summary_table(report))
    console.print()
    console.print(build_flagged_table(report))
    console.print()
    console.print(build_top_scores_table(report, top))


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
        Console(stderr=True).print(f"[bold red]Error:[/] {escape(str(exc))}")
        raise typer.Exit(code=1) from exc

    if json_output:
        typer.echo(json.dumps(asdict(result), indent=2))
    else:
        print_text_report(result, top)


if __name__ == "__main__":
    app()
