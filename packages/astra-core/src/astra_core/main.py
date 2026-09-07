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
    "ASTChunk",
    "AnalysisReport",
    "ChunkAlignment",
    "CodeUnit",
    "SimilarityScore",
    "analyze_code_similarity",
]
