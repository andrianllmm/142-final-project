# Astra CLI

Command-line wrapper for ASTRA's code similarity engine.

The CLI compares two or more Python source files and reports how structurally
similar they are after AST normalization.

## Run From The Workspace

From the repository root, install dependencies:

```bash
uv sync
```

Then run:

```bash
uv run --package astra-cli astra path/to/file_a.py path/to/file_b.py
```

Example:

```bash
uv run --package astra-cli astra packages/astra-core/tests/test_distance.py packages/astra-core/tests/test_alignment.py
```

## Output

Text output is rendered with Rich tables. It shows the summary first, followed
by flagged pairs and top scores. Rich adjusts borders and wrapping to the
terminal width, but the report content follows this shape:

```text
ASTRA Similarity Report
Threshold        0.80
Files analyzed   2
Pairs compared   1
Flagged pairs    1

Flagged pairs
Pair                           Score
a.py <-> b.py                  1.0000

Top scores
Pair                           Score   Alignments
a.py <-> b.py                  1.0000  1
```

If no pair reaches the threshold, `Flagged pairs` will show `None`.

## Options

Set the similarity threshold:

```bash
uv run --package astra-cli astra file_a.py file_b.py --threshold 0.9
```

Show fewer or more top scores in text mode:

```bash
uv run --package astra-cli astra file_a.py file_b.py --top 5
```

Print the full report as JSON:

```bash
uv run --package astra-cli astra file_a.py file_b.py --json
```

Show help:

```bash
uv run --package astra-cli astra --help
```

## Notes

- Pass at least two files. ASTRA compares files in pairs.
- `--threshold` must be between `0.0` and `1.0`.
- The CLI expects valid Python source files.
- Text output hides token evidence to keep the report readable.
- JSON output includes the full report, including alignment evidence.
