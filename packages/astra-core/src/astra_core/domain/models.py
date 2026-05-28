"""Data structures shared across chunking, alignment, and reporting."""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class CodeUnit:
    """A source file or submission passed into the analysis pipeline."""

    id: str
    content: str

    def __repr__(self) -> str:
        return f"CodeUnit(id={self.id!r}, chars={len(self.content)})"

    def __str__(self) -> str:
        return f"[CodeUnit] {self.id} ({len(self.content)} chars)"


@dataclass(frozen=True)
class ASTChunk:
    """A normalized AST slice used for pairwise comparison."""

    index: int
    kind: str
    tokens: Tuple[str, ...]

    def __repr__(self) -> str:
        return f"ASTChunk(index={self.index}, kind={self.kind!r}, tokens={len(self.tokens)})"

    def __str__(self) -> str:
        preview = " ".join(self.tokens[:10])
        suffix = "..." if len(self.tokens) > 10 else ""
        return f"[Chunk {self.index}] {self.kind}: {preview}{suffix}"


@dataclass(frozen=True)
class ChunkAlignment:
    """Evidence describing a best match between two AST chunks."""

    left_chunk_index: int
    right_chunk_index: int
    similarity: float
    distance: int
    left_kind: str
    right_kind: str
    left_tokens: Tuple[str, ...]
    right_tokens: Tuple[str, ...]

    def __repr__(self) -> str:
        return (
            f"ChunkAlignment(L{self.left_chunk_index} <=> R{self.right_chunk_index}, "
            f"sim={self.similarity:.3f}, dist={self.distance})"
        )

    def __str__(self) -> str:
        return (
            f"Chunk {self.left_chunk_index} ({self.left_kind}) <=> "
            f"Chunk {self.right_chunk_index} ({self.right_kind}) | "
            f"similarity={self.similarity:.2f}, distance={self.distance}"
        )


@dataclass(frozen=True)
class SimilarityScore:
    """Aggregate similarity result for a pair of code units."""

    unit_a: str
    unit_b: str
    score: float
    alignment_count: int = 0
    chunk_count_a: int = 0
    chunk_count_b: int = 0
    evidence: Tuple[ChunkAlignment, ...] = ()

    def __repr__(self) -> str:
        return (
            f"SimilarityScore({self.unit_a!r}, {self.unit_b!r}, "
            f"score={self.score:.3f}, alignments={self.alignment_count})"
        )

    def __str__(self) -> str:
        return (
            f"{self.unit_a} <=> {self.unit_b}\n"
            f"  score: {self.score:.2%}\n"
            f"  chunks: {self.chunk_count_a} vs {self.chunk_count_b}\n"
            f"  alignments: {self.alignment_count}"
        )


@dataclass(frozen=True)
class AnalysisReport:
    """Summary of all pairwise similarity results for a batch."""

    threshold: float
    total_units: int
    scores: List[SimilarityScore]
    flagged_pairs: List[SimilarityScore]
    metadata: Dict[str, Any]

    def __repr__(self) -> str:
        return (
            f"AnalysisReport(threshold={self.threshold}, "
            f"units={self.total_units}, scores={len(self.scores)}, "
            f"flagged={len(self.flagged_pairs)})"
        )

    def __str__(self) -> str:
        lines = [
            f"Total submissions: {self.total_units}",
            f"Threshold: {self.threshold:.2%}",
            f"Flagged pairs: {len(self.flagged_pairs)}",
            "",
            "Top Similarities:",
        ]

        for s in sorted(self.scores, key=lambda x: x.score, reverse=True)[:10]:
            lines.append(f"  - {s.unit_a} <=> {s.unit_b}: {s.score:.2%}")

        if self.flagged_pairs:
            lines.append("\nFLAGGED:")
            for s in self.flagged_pairs:
                lines.append(f"  - {s.unit_a} <=> {s.unit_b}: {s.score:.2%}")

        return "\n".join(lines)
