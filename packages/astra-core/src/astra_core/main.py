"""Convenience imports for the core similarity analysis API."""

from .domain.models import (
    AnalysisReport,
    ASTChunk,
    ChunkAlignment,
    CodeUnit,
    SimilarityScore,
)
from .pipeline.analyze import analyze_code_similarity

__all__ = [
    "analyze_code_similarity",
    "CodeUnit",
    "ASTChunk",
    "ChunkAlignment",
    "SimilarityScore",
    "AnalysisReport",
]
