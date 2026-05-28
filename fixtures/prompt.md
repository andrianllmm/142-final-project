Generate **20–30 Python (.py) student submission files** in fixtures folder for a single programming lab, plus a **CSV annotation file** for evaluation of a plagiarism detection system.

---

## Lab Instructions

```id="lab_spec"
[INSERT LAB INSTRUCTIONS HERE]
```

---

## Output Requirements

### 1. Python Files

Generate 20–30 `.py` files:

- Each file is a single student submission
- All solve the same problem
- Must be executable Python 3 code

### 2. Directory + Naming

Assume files are saved under a dataset folder, e.g.:

```
fixtures/labX/
  student_01.py
  student_02.py
  ...
```

You must use these relative paths in the CSV.

---

### 3. CSV Annotation File

Generate a CSV named:

```
annotations.csv
```

Each row corresponds to one Python file.

### CSV Schema

```
file_path,student_id,ground_truth_group,source_type
```

### Field Definitions

- `file_path`: relative path to file (e.g., `fixtures/labX//student_01.py`)
- `student_id`: unique identifier (e.g., `student_01`)
- `ground_truth_group`: cluster label (A, B, C, etc.)
- `source_type`:
  - `original` → independently written solution
  - `near_copy` → lightly modified copy (renamed variables, minor edits)
  - `modified_copy` → structurally altered but same logic lineage

---

## Dataset Design Rules

### 1. Solution Diversity

Include multiple independent solution strategies:

- At least 2–4 distinct algorithmic approaches (if applicable)
- Different decomposition styles (single function vs multiple helpers)

---

### 2. Controlled Plagiarism Structure

Create grouped similarity clusters:

- Each `ground_truth_group` contains:
  - 1–2 originals
  - several near_copies
  - several modified_copies

Target:

- 3–6 groups depending on dataset size

---

### 3. Structural Variation Requirements

Ensure realistic AST-level diversity:

- Renamed identifiers across submissions
- Reordered code blocks
- Equivalent logic with different control flow
- Some structurally similar but textually different implementations
- Some visually similar but structurally modified implementations

---

### 4. AST Testing Intent

Dataset must stress-test:

- AST normalization robustness
- chunk-level alignment consistency
- Damerau–Levenshtein edit distance sensitivity
- similarity ranking correctness
- false positive/negative behavior under obfuscation

---

### 5. Constraints

- Python 3 only
- Single-file submissions only
- No external libraries unless explicitly required
- Must run without errors

---

## Purpose

This dataset is for evaluating Astra’s plagiarism detection pipeline using:

- AST normalization
- structural chunking
- edit-distance alignment
- similarity scoring
- ranked pair detection

The CSV provides **ground truth labels for evaluation metrics** (precision, recall, clustering accuracy, threshold tuning).
