from __future__ import annotations

import ast
from typing import List

from ..domain.models import ASTChunk, CodeUnit


def chunk_source_code(unit: CodeUnit) -> List[ASTChunk]:
    tree = parse_source(unit)
    chunks: List[ASTChunk] = []

    if not isinstance(tree, ast.Module):
        return [
            ASTChunk(
                index=0, kind=type(tree).__name__, tokens=tuple(tokenize_node(tree))
            )
        ]

    statements = [
        statement for statement in tree.body if not _is_noop_string_expr(statement)
    ]

    for index, statement in enumerate(statements):
        chunks.append(
            ASTChunk(
                index=index,
                kind=type(statement).__name__,
                tokens=tuple(tokenize_node(statement)),
                start_line=getattr(statement, "lineno", 1),
                end_line=getattr(statement, "end_lineno", getattr(statement, "lineno", 1)),
            )
        )

    return chunks


def parse_source(unit: CodeUnit) -> ast.AST:
    try:
        return ast.parse(unit.content, filename=unit.id)
    except SyntaxError as exc:
        raise ValueError(
            f"Failed to parse Python source for {unit.id}: {exc.msg}"
        ) from exc


def tokenize_node(node: ast.AST) -> List[str]:
    tokens: List[str] = []

    def visit(current: ast.AST) -> None:
        tokens.append(type(current).__name__)

        if isinstance(current, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            tokens.append("IDENT")
        elif isinstance(current, ast.Name):
            tokens.append("IDENT")
        elif isinstance(current, ast.arg):
            tokens.append("ARG")
        elif isinstance(current, ast.Attribute):
            tokens.append("ATTR")
        elif isinstance(current, ast.alias):
            tokens.append("ALIAS")
        elif isinstance(current, ast.Constant):
            tokens.append(_normalize_constant(current.value))

        for field_name, value in ast.iter_fields(current):
            if isinstance(value, ast.AST):
                visit(value)
                continue

            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST) and not _is_noop_string_expr(item):
                        visit(item)
                continue

            normalized = _normalize_primitive(field_name, value)
            if normalized is not None:
                tokens.append(normalized)

    visit(node)
    return tokens


def _normalize_primitive(field_name: str, value: object) -> str | None:
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


def _is_noop_string_expr(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )
