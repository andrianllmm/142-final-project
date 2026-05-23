from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class CodeUnit:
    id: str
    content: str


@dataclass(frozen=True)
class ASTChunk:
    index: int
    kind: str
    tokens: Tuple[str, ...]
    start_line: int = 1
    end_line: int = 1


@dataclass(frozen=True)
class ChunkAlignment:
    left_chunk_index: int
    right_chunk_index: int
    similarity: float
    distance: int
    left_kind: str
    right_kind: str
    left_tokens: Tuple[str, ...]
    right_tokens: Tuple[str, ...]
    left_start_line: int = 1
    left_end_line: int = 1
    right_start_line: int = 1
    right_end_line: int = 1


@dataclass(frozen=True)
class SimilarityScore:
    unit_a: str
    unit_b: str
    score: float
    alignment_count: int = 0
    chunk_count_a: int = 0
    chunk_count_b: int = 0
    evidence: Tuple[ChunkAlignment, ...] = ()


@dataclass(frozen=True)
class AnalysisReport:
    threshold: float
    total_units: int
    scores: List[SimilarityScore]
    flagged_pairs: List[SimilarityScore]
    metadata: Dict[str, Any]
