# Astra

A system for detecting structural similarity between programming assignments using AST normalization and Damerau–Levenshtein sequence alignment.

Astra is designed for academic use in programming courses to identify potential plagiarism cases where students modify code superficially (renaming variables, reformatting, or minor structural edits) while preserving underlying logic.

## Project Information

- Subject: CMSC 142
- Project title: Astra
- Type: Web / CLI hybrid tool
- Group members: Andrian Lloyd Maagma, Dejel Cyrus De Asis, John Romyr Lopez

Full title:

Internal Code Similarity Detection System for Student Programming Submissions Using Abstract Syntax Tree (AST) Normalization and Damerau–Levenshtein Sequence Alignment

## Problem Definition

In programming classes, instructors manually review student submissions to detect copying or near-duplicate solutions. This does not scale across multiple lab sections and many files. Text-based comparison tools are also easy to bypass through identifier renaming, formatting edits, or small structural changes.

Astra addresses this by comparing normalized Python program structure rather than raw text similarity.

## Features

- AST-based normalization using Python built-in `ast` module
- Python comment and docstring noise ignored during structural comparison
- Structural chunking of code
- Deterministic AST-to-token conversion (preorder traversal)
- Damerau–Levenshtein dynamic programming similarity engine
- Chunk-level alignment with best-match pairing
- File-level similarity aggregation
- Ranked similarity reports with threshold-based flagging
- Optional detailed alignment evidence for interpretation

## Algorithm

Each Python submission is parsed into an AST. The AST is normalized by replacing identifiers with generic placeholders, standardizing literals, ignoring comments, and removing docstrings. Structural chunks are converted into deterministic token sequences using preorder traversal.

Chunk token sequences are compared using Damerau–Levenshtein distance, a dynamic programming algorithm that computes the minimum edit cost between sequences using insertion, deletion, substitution, and transposition. Chunk-level scores are aggregated into file-level similarity scores.

Optimality is guaranteed at the sequence-alignment level because the dynamic programming matrix computes the exact minimum edit distance under the defined operation costs. File-level detection remains heuristic because it depends on chunking, best-match selection, and score aggregation.

## Scope and Limitations

- Designed exclusively for Python `.py` submissions.
- Intended for single-file programming lab assignments.
- Optimized for small to medium class batches, approximately 15 to 30 students.
- Focused on syntactic and structural similarity, not semantic equivalence or intent.
- Pairwise comparison has O(n²) scaling over the number of submissions.

## References

- https://doi.org/10.3390/app132011358
- https://doi.org/10.1145/3313290
- https://doi.org/10.15294/sji.v11i1.48064
- https://ceur-ws.org/Vol-2259/aics_33.pdf
- https://yangdanny97.github.io/blog/2019/05/03/MOSS
- https://glotta.ntua.gr/IS-Social/CopyRight/Plagiarism%20Detection.htm
- https://jplag.github.io/Demo/overview

## Usage

### CLI

Install the workspace dependencies first:

```bash
uv sync
```

Run ASTRA against two or more Python files:

```bash
uv run --package astra-cli astra path/to/file_a.py path/to/file_b.py
```

Example using files already in this repository:

```bash
uv run --package astra-cli astra packages/astra-core/tests/test_distance.py packages/astra-core/tests/test_alignment.py
```

The CLI prints a similarity report with the configured threshold, number of files,
compared pairs, flagged pairs, and top scores.

Common options:

```bash
uv run --package astra-cli astra file_a.py file_b.py --threshold 0.9
uv run --package astra-cli astra file_a.py file_b.py --top 5
uv run --package astra-cli astra file_a.py file_b.py --json
```

- `--threshold` sets the minimum score for a pair to be flagged. It must be
  between `0.0` and `1.0`.
- `--top` controls how many top pair scores are shown in text output.
- `--json` prints the full report, including detailed evidence, as JSON.

### Core API

```python
from astra_core import analyze_code_similarity, CodeUnit

result = analyze_code_similarity([
    CodeUnit(id="a.py", content="def add(x, y): return x + y"),
    CodeUnit(id="b.py", content="def add(a, b): return a + b"),
])
```

## Development

### Requirements

- Python 3.11+
- uv
- Node.js and npm for the web UI

### Install dependencies

```bash
uv sync
```

### Run tests

```bash
uv run pytest
```

### Run CLI

```bash
uv run astra
```

### Run web

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
npm run dev
```

## Project Structure

```
packages/
  astra-core/      # core similarity engine (main logic)
  astra-cli/       # CLI wrapper
  astra-web/       # web service
```
