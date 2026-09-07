from astra_core.pipeline.distance import damerau_levenshtein_distance

# BASIC CORRECTNESS


def test_exact_match_returns_zero() -> None:
    assert damerau_levenshtein_distance(("A", "B", "C"), ("A", "B", "C")) == 0


def test_single_insertion() -> None:
    assert damerau_levenshtein_distance(("A", "B"), ("A", "B", "C")) == 1


def test_single_deletion() -> None:
    assert damerau_levenshtein_distance(("A", "B", "C"), ("A", "C")) == 1


def test_single_substitution() -> None:
    assert damerau_levenshtein_distance(("A", "B", "C"), ("A", "X", "C")) == 1


# TRANSPOSITION BEHAVIOR


def test_adjacent_transposition_costs_one() -> None:
    assert damerau_levenshtein_distance(("A", "B"), ("B", "A")) == 1


def test_larger_transposition_case() -> None:
    assert damerau_levenshtein_distance(("A", "B", "C", "D"), ("A", "C", "B", "D")) == 1


def test_multiple_transpositions() -> None:
    assert damerau_levenshtein_distance(("A", "B", "C", "D"), ("B", "A", "D", "C")) == 2


# EMPTY / BOUNDARY CASES


def test_both_empty_sequences() -> None:
    assert damerau_levenshtein_distance((), ()) == 0


def test_first_empty_sequence() -> None:
    assert damerau_levenshtein_distance((), ("A", "B", "C")) == 3


def test_second_empty_sequence() -> None:
    assert damerau_levenshtein_distance(("A", "B", "C"), ()) == 3


# SINGLE ELEMENT CASES


def test_single_element_equal() -> None:
    assert damerau_levenshtein_distance(("A",), ("A",)) == 0


def test_single_element_different() -> None:
    assert damerau_levenshtein_distance(("A",), ("B",)) == 1


# MIXED COMPLEX CASES


def test_complex_mix_operations() -> None:
    # ABCD -> AXBD requires substitution + transposition
    assert damerau_levenshtein_distance(("A", "B", "C", "D"), ("A", "X", "B", "D")) == 2


def test_repeated_tokens() -> None:
    assert damerau_levenshtein_distance(("A", "A", "B"), ("A", "B", "B")) >= 1


def test_longer_sequence_structure_shift() -> None:
    assert (
        damerau_levenshtein_distance(
            ("A", "B", "C", "D", "E"), ("A", "C", "B", "E", "D")
        )
        == 2
    )


# IDENTITY AND SYMMETRY PROPERTIES


def test_symmetry_property() -> None:
    a = ("A", "B", "C")
    b = ("A", "C", "B")
    assert damerau_levenshtein_distance(a, b) == damerau_levenshtein_distance(b, a)


def test_identity_property() -> None:
    a = ("X", "Y", "Z")
    assert damerau_levenshtein_distance(a, a) == 0
