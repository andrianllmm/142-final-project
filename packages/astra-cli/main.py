import typer
from pathlib import Path

from astra_core import CodeUnit, analyze_code_similarity

app = typer.Typer()


def load_file(path: Path) -> CodeUnit:
    return CodeUnit(
        id=str(path),
        content=path.read_text(encoding="utf-8"),
    )


@app.command()
def analyze(
    paths: list[Path] = typer.Argument(..., help="Paths to code files"),
    threshold: float = 0.8,
):
    units = [load_file(p) for p in paths]

    result = analyze_code_similarity(
        units=units,
        threshold=threshold,
    )

    typer.echo(result)


if __name__ == "__main__":
    app()
