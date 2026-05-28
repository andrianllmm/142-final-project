"""Top-level orchestration for pairwise code similarity analysis."""

from typing import List

from ..domain.models import AnalysisReport, CodeUnit, SimilarityScore
from .alignment import compare_chunk_sequences
from .ast_processing import chunk_source_code


def analyze_code_similarity(
    units: List[CodeUnit],
    threshold: float = 0.8,
) -> AnalysisReport:
    """Analyze code units and return a ranked similarity report.

    Each unit is chunked into top-level AST statements before pairwise
    comparison, and the report keeps both the full ranking and the flagged
    pairs above the threshold.
    """
    chunked_units = [(unit, chunk_source_code(unit)) for unit in units]
    scores: List[SimilarityScore] = []

    for left_index in range(len(chunked_units)):
        left_unit, left_chunks = chunked_units[left_index]
        for right_index in range(left_index + 1, len(chunked_units)):
            right_unit, right_chunks = chunked_units[right_index]
            score, evidence = compare_chunk_sequences(left_chunks, right_chunks)
            scores.append(
                SimilarityScore(
                    unit_a=left_unit.id,
                    unit_b=right_unit.id,
                    score=score,
                    alignment_count=len(evidence),
                    chunk_count_a=len(left_chunks),
                    chunk_count_b=len(right_chunks),
                    evidence=evidence,
                )
            )

    scores.sort(key=lambda item: (-item.score, item.unit_a, item.unit_b))
    flagged = [score for score in scores if score.score >= threshold]

    return AnalysisReport(
        threshold=threshold,
        total_units=len(units),
        scores=scores,
        flagged_pairs=flagged,
        metadata={
            "algorithm": "ast-normalized-damerau-levenshtein",
            "chunking": "top-level-ast-statements",
            "tokenization": "preorder-normalized-ast",
            "unit_chunk_counts": {
                unit.id: len(chunks) for unit, chunks in chunked_units
            },
        },
    )
