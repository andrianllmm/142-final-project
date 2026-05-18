from astra_core import AnalysisReport, CodeUnit, analyze_code_similarity


def test_analyze_code_similarity_returns_valid_report_structure() -> None:
    units = [
        CodeUnit(id="a.py", content="x = 1"),
        CodeUnit(id="b.py", content="x = 2"),
        CodeUnit(id="c.py", content="x = 3"),
    ]

    report = analyze_code_similarity(units)

    assert isinstance(report, AnalysisReport)
    assert report.total_units == 3
    assert isinstance(report.scores, list)
    assert isinstance(report.flagged_pairs, list)


def test_analyze_code_similarity_metadata_is_present() -> None:
    units = [CodeUnit(id="a.py", content="x = 1")]

    report = analyze_code_similarity(units)

    assert report.metadata["algorithm"] == "ast-normalized-damerau-levenshtein"
    assert "unit_chunk_counts" in report.metadata


def test_analyze_code_similarity_ranks_most_similar_pair_first() -> None:
    units = [
        CodeUnit(id="a.py", content="def add(x, y): return x + y"),
        CodeUnit(id="b.py", content="def add(a, b): return a + b"),
        CodeUnit(id="c.py", content="def subtract(x, y): return x - y"),
    ]

    report = analyze_code_similarity(units)

    top = report.scores[0]

    assert {top.unit_a, top.unit_b} == {"a.py", "b.py"}


def test_analyze_code_similarity_top_score_is_high_for_identical_logic() -> None:
    units = [
        CodeUnit(id="a.py", content="def add(x, y): return x + y"),
        CodeUnit(id="b.py", content="def add(a, b): return a + b"),
    ]

    report = analyze_code_similarity(units)

    assert report.scores[0].score >= 0.9


def test_analyze_code_similarity_applies_threshold_correctly() -> None:
    units = [
        CodeUnit(id="a.py", content="def add(x, y): return x + y"),
        CodeUnit(id="b.py", content="def add(a, b): return a + b"),
        CodeUnit(id="c.py", content="def subtract(x, y): return x - y"),
    ]

    report = analyze_code_similarity(units, threshold=0.99)

    assert len(report.flagged_pairs) >= 1
    assert all(p.score >= 0.99 for p in report.flagged_pairs)


def test_analyze_code_similarity_handles_empty_input() -> None:
    report = analyze_code_similarity([])

    assert report.total_units == 0
    assert report.scores == []
    assert report.flagged_pairs == []


def test_analyze_code_similarity_single_input_has_no_pairs() -> None:
    report = analyze_code_similarity([CodeUnit(id="a.py", content="x = 1")])

    assert report.total_units == 1
    assert report.scores == []
    assert report.flagged_pairs == []


def test_analyze_code_similarity_unit_chunk_counts_match_inputs() -> None:
    units = [
        CodeUnit(id="a.py", content="x = 1"),
        CodeUnit(id="b.py", content="x = 2"),
    ]

    report = analyze_code_similarity(units)

    assert set(report.metadata["unit_chunk_counts"].keys()) == {"a.py", "b.py"}
