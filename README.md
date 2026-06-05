# Astra

Structural similarity detection system for Python code using AST normalization and Damerau–Levenshtein sequence alignment.

---

## About The Project

Astra is a tool for detecting structural similarity between Python programs by analyzing their Abstract Syntax Trees (ASTs) instead of raw text.

It is designed to identify near-duplicate submissions where code has been superficially modified (e.g., renamed variables, formatting changes, minor restructuring) while preserving the same underlying logic.

The system is suitable for comparing programming assignments and identifying potential plagiarism patterns in small to medium batches of submissions.

---

## Key Features

- AST-based normalization using Python `ast` module
- Identifier and literal normalization
- Comment and docstring removal
- Deterministic AST-to-token conversion via preorder traversal
- Damerau–Levenshtein sequence alignment for structural comparison
- Chunk-level similarity matching
- Aggregated file-level similarity scoring
- Ranked similarity reports with configurable thresholds
- Optional detailed alignment output for inspection

---

## Built With

- Python 3.11+
- AST (standard library)
- uv (package management)
- FastAPI (web service)
- Typer (CLI)
- TypeScript / Node.js (web frontend)

---

## Getting Started

### Prerequisites

- Python 3.11+
- uv
- Node.js + npm (for web UI)

---

### Installation

```sh
git clone https://github.com/andrianllmm/astra.git
cd astra
uv sync
```

---

### Run CLI

```sh
uv run --package astra-cli astra path/to/file_a.py path/to/file_b.py
```

Example:

```sh
uv run --package astra-cli astra packages/astra-core/tests/test_distance.py packages/astra-core/tests/test_alignment.py
```

Options:

```sh
uv run --package astra-cli astra file_a.py file_b.py --threshold 0.9
uv run --package astra-cli astra file_a.py file_b.py --top 5
uv run --package astra-cli astra file_a.py file_b.py --json
```

---

### Run Web Service

```sh
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

```sh
npm run dev
```

---

### Core API Usage

```python
from astra_core import analyze_code_similarity, CodeUnit

result = analyze_code_similarity([
    CodeUnit(id="a.py", content="def add(x, y): return x + y"),
    CodeUnit(id="b.py", content="def add(a, b): return a + b"),
])
```

---

## Project Structure

```
packages/
├── astra-core/   # core AST similarity engine
├── astra-cli/    # command-line interface
└── astra-web/    # web service + UI
```
