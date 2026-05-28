"""Parse Python source and normalize AST nodes into comparison chunks."""

from __future__ import annotations

import ast
from typing import List

from ..domain.models import ASTChunk, CodeUnit


def chunk_source_code(unit: CodeUnit) -> List[ASTChunk]:
    """Split a parsed module into comparable top-level AST chunks."""
    tree = parse_source(unit)
    chunks: List[ASTChunk] = []

    if not isinstance(tree, ast.Module):
        # Non-module parses are still represented as a single chunk for scoring.
        return [
            ASTChunk(
                index=0, kind=type(tree).__name__, tokens=tuple(tokenize_node(tree))
            )
        ]

    for index, statement in enumerate(tree.body):
        # Each top-level statement becomes one comparison unit.
        chunks.append(
            ASTChunk(
                index=index,
                kind=type(statement).__name__,
                tokens=tuple(tokenize_node(statement)),
            )
        )

    return chunks


def parse_source(unit: CodeUnit) -> ast.AST:
    """Parse a code unit and raise a readable error when parsing fails."""
    try:
        return ast.parse(unit.content, filename=unit.id)
    except SyntaxError as exc:
        raise ValueError(
            f"Failed to parse Python source for {unit.id}: {exc.msg}"
        ) from exc


def tokenize_node(node: ast.AST) -> List[str]:
    """Walk an AST node and emit a normalized token stream."""
    tokens: List[str] = []

    def visit(current: ast.AST) -> None:
        # Preserve structure while normalizing identifiers and literals.
        tokens.append(type(current).__name__)

        if isinstance(current, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            # Names of declarations should not dominate the similarity result.
            tokens.append("IDENT")
        elif isinstance(current, ast.Name):
            tokens.append("IDENT")
        elif isinstance(current, ast.arg):
            # Function arguments are treated as placeholders, not exact names.
            tokens.append("ARG")
        elif isinstance(current, ast.Attribute):
            # Attribute access is normalized to preserve the shape of the expression.
            tokens.append("ATTR")
        elif isinstance(current, ast.alias):
            # Imports are compared by structure rather than exact alias text.
            tokens.append("ALIAS")
        elif isinstance(current, ast.Constant):
            # Literal values are collapsed to broad kinds so tiny value changes matter less.
            tokens.append(_normalize_constant(current.value))

        for field_name, value in ast.iter_fields(current):
            if isinstance(value, ast.AST):
                visit(value)
                continue

            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        visit(item)
                continue

            normalized = _normalize_primitive(field_name, value)
            if normalized is not None:
                tokens.append(normalized)

    visit(node)
    return tokens


def _normalize_primitive(field_name: str, value: object) -> str | None:
    """Map primitive field values to coarse comparison tokens."""
    if value is None:
        return None

    if isinstance(value, bool):
        return "BOOL"

    if isinstance(value, (int, float, complex)):
        return "NUM"

    if isinstance(value, str):
        if field_name in {"id", "name", "attr", "arg", "asname", "module"}:
            return "IDENT"

        if field_name == "kind":
            return "CONST_KIND"

        if field_name in {"type_comment", "annotation"}:
            return None

        return "STR"

    return type(value).__name__.upper()


def _normalize_constant(value: object) -> str:
    """Normalize constant literals so only their broad type matters."""
    if value is None:
        return "CONST_NONE"

    if isinstance(value, bool):
        return "CONST_BOOL"

    if isinstance(value, (int, float, complex)):
        return "CONST_NUM"

    if isinstance(value, str):
        return "CONST_STR"

    if isinstance(value, bytes):
        return "CONST_BYTES"

    return "CONST_OTHER"
