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
    "ASTChunk",
    "AnalysisReport",
    "ChunkAlignment",
    "CodeUnit",
    "SimilarityScore",
    "analyze_code_similarity",
]
