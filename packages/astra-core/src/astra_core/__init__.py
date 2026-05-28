"""Public package exports for AST-based code similarity analysis."""

from .main import (
    AnalysisReport,
    ASTChunk,
    ChunkAlignment,
    CodeUnit,
    SimilarityScore,
    analyze_code_similarity,
)

__all__ = [
    "analyze_code_similarity",
    "CodeUnit",
    "ASTChunk",
    "ChunkAlignment",
    "SimilarityScore",
    "AnalysisReport",
]
