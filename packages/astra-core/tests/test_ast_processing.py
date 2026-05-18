import pytest

from astra_core.domain.models import CodeUnit
from astra_core.pipeline.ast_processing import (
    chunk_source_code,
    parse_source,
    tokenize_node,
)


def test_chunk_source_code_returns_single_function_chunk() -> None:
    unit = CodeUnit(
        id="sample.py",
        content="""
def add(left, right):
    return left + right
""".strip(),
    )

    chunks = chunk_source_code(unit)

    assert len(chunks) == 1


def test_chunk_source_code_chunk_kind_is_functiondef() -> None:
    unit = CodeUnit(
        id="sample.py",
        content="""
def add(left, right):
    return left + right
""".strip(),
    )

    chunks = chunk_source_code(unit)

    assert chunks[0].kind == "FunctionDef"


def test_chunk_source_code_assigns_sequential_index() -> None:
    unit = CodeUnit(
        id="sample.py",
        content="""
def add(left, right):
    return left + right
""".strip(),
    )

    chunks = chunk_source_code(unit)

    assert chunks[0].index == 0


def test_chunk_source_code_tokens_include_identifier_placeholder() -> None:
    unit = CodeUnit(
        id="sample.py",
        content="""
def add(left, right):
    return left + right
""".strip(),
    )

    chunks = chunk_source_code(unit)

    assert "IDENT" in chunks[0].tokens


def test_chunk_source_code_tokens_include_argument_placeholder() -> None:
    unit = CodeUnit(
        id="sample.py",
        content="""
def add(left, right):
    return left + right
""".strip(),
    )

    chunks = chunk_source_code(unit)

    assert "ARG" in chunks[0].tokens


def test_tokenize_node_replaces_identifiers_with_ident() -> None:
    unit = CodeUnit(id="sample.py", content="value = answer")
    tree = parse_source(unit)

    tokens = tokenize_node(tree)

    assert "IDENT" in tokens


def test_tokenize_node_replaces_numeric_literals() -> None:
    unit = CodeUnit(id="sample.py", content="x = 3")
    tree = parse_source(unit)

    tokens = tokenize_node(tree)

    assert "NUM" in tokens


def test_parse_source_returns_ast_for_valid_code() -> None:
    unit = CodeUnit(id="sample.py", content="x = 1")

    tree = parse_source(unit)

    assert tree is not None


def test_parse_source_raises_value_error_on_syntax_error() -> None:
    unit = CodeUnit(id="broken.py", content="def broken(:\n    pass")

    with pytest.raises(ValueError):
        parse_source(unit)


def test_parse_source_error_message_includes_file_id() -> None:
    unit = CodeUnit(id="broken.py", content="def broken(:\n    pass")

    with pytest.raises(ValueError, match="broken.py"):
        parse_source(unit)
