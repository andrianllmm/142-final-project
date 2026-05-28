"""Chunk matching and scoring helpers for AST sequence comparison."""

from __future__ import annotations

from typing import Sequence

from ..domain.models import ASTChunk, ChunkAlignment
from .distance import damerau_levenshtein_distance


def compare_chunk_sequences(
    left_chunks: Sequence[ASTChunk],
    right_chunks: Sequence[ASTChunk],
) -> tuple[float, tuple[ChunkAlignment, ...]]:
    """Compare two AST chunk sequences and return a normalized score.

    The score is built from best matches in both directions so the result stays
    symmetric even when one side has extra or reordered chunks.
    """
    if not left_chunks and not right_chunks:
        return 1.0, ()

    if not left_chunks or not right_chunks:
        return 0.0, ()

    # Compare both directions so a chunk only being "best" from one side does not skew the score.
    left_to_right = _best_chunk_matches(left_chunks, right_chunks)
    right_to_left = _best_chunk_matches(right_chunks, left_chunks, reverse=True)

    left_score = _weighted_average(left_to_right)
    right_score = _weighted_average(right_to_left)
    combined_score = (left_score + right_score) / 2.0

    evidence = _rank_alignments(left_to_right + right_to_left)
    return combined_score, tuple(evidence[: min(5, len(evidence))])


def _best_chunk_matches(
    primary_chunks: Sequence[ASTChunk],
    secondary_chunks: Sequence[ASTChunk],
    *,
    reverse: bool = False,
) -> list[tuple[float, ChunkAlignment]]:
    """Find the best match for each chunk in one direction."""
    matches: list[tuple[float, ChunkAlignment]] = []

    for primary in primary_chunks:
        best_alignment: ChunkAlignment | None = None
        best_score = -1.0

        for secondary in secondary_chunks:
            # Token distance is the cheapest way to compare two normalized AST chunks.
            distance = damerau_levenshtein_distance(primary.tokens, secondary.tokens)
            token_length = max(len(primary.tokens), len(secondary.tokens))
            similarity = 1.0 if token_length == 0 else 1.0 - (distance / token_length)

            if similarity > best_score:
                if reverse:
                    best_alignment = ChunkAlignment(
                        left_chunk_index=secondary.index,
                        right_chunk_index=primary.index,
                        similarity=similarity,
                        distance=distance,
                        left_kind=secondary.kind,
                        right_kind=primary.kind,
                        left_tokens=secondary.tokens,
                        right_tokens=primary.tokens,
                    )
                else:
                    best_alignment = ChunkAlignment(
                        left_chunk_index=primary.index,
                        right_chunk_index=secondary.index,
                        similarity=similarity,
                        distance=distance,
                        left_kind=primary.kind,
                        right_kind=secondary.kind,
                        left_tokens=primary.tokens,
                        right_tokens=secondary.tokens,
                    )
                best_score = similarity

        if best_alignment is not None:
            matches.append((best_score, best_alignment))

    return matches


def _weighted_average(matches: Sequence[tuple[float, ChunkAlignment]]) -> float:
    """Weight matches by chunk size so longer chunks contribute more."""
    if not matches:
        return 0.0

    total_weight = 0.0
    weighted_sum = 0.0

    for similarity, alignment in matches:
        # Longer chunks carry more structural information, so they count more.
        weight = float(max(len(alignment.left_tokens), len(alignment.right_tokens)))
        total_weight += weight
        weighted_sum += similarity * weight

    if total_weight == 0.0:
        return 0.0

    return weighted_sum / total_weight


def _rank_alignments(
    matches: Sequence[tuple[float, ChunkAlignment]],
) -> list[ChunkAlignment]:
    """Deduplicate and sort alignments so the strongest evidence comes first."""
    unique: dict[tuple[int, int, tuple[str, ...], tuple[str, ...]], ChunkAlignment] = {}

    for _, alignment in matches:
        # Keep only the strongest evidence for each chunk pairing.
        key = (
            alignment.left_chunk_index,
            alignment.right_chunk_index,
            alignment.left_tokens,
            alignment.right_tokens,
        )
        existing = unique.get(key)
        if existing is None or alignment.similarity > existing.similarity:
            unique[key] = alignment

    return sorted(
        unique.values(),
        key=lambda item: (
            -item.similarity,
            item.left_chunk_index,
            item.right_chunk_index,
        ),
    )
