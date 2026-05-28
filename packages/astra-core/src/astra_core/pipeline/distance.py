"""Damerau-Levenshtein distance for token sequence comparison."""

from typing import Sequence


def damerau_levenshtein_distance(left: Sequence[str], right: Sequence[str]) -> int:
    """Return the edit distance with adjacent transpositions counted as one."""
    if left == right:
        return 0

    left_length = len(left)
    right_length = len(right)

    if left_length == 0:
        return right_length

    if right_length == 0:
        return left_length

    max_distance = left_length + right_length
    distance_matrix = [[0] * (right_length + 2) for _ in range(left_length + 2)]
    distance_matrix[0][0] = max_distance

    # The outer border seeds the dynamic-programming table with edit costs.
    for i in range(left_length + 1):
        distance_matrix[i + 1][0] = max_distance
        distance_matrix[i + 1][1] = i

    for j in range(right_length + 1):
        distance_matrix[0][j + 1] = max_distance
        distance_matrix[1][j + 1] = j

    # Track the last row where each token from the left side matched.
    last_seen: dict[str, int] = {}

    for i in range(1, left_length + 1):
        last_match_column = 0

        for j in range(1, right_length + 1):
            left_token = left[i - 1]
            right_token = right[j - 1]
            previous_match_row = last_seen.get(right_token, 0)
            previous_match_column = last_match_column

            cost = 0 if left_token == right_token else 1
            if cost == 0:
                last_match_column = j

            substitution = distance_matrix[i][j] + cost
            insertion = distance_matrix[i + 1][j] + 1
            deletion = distance_matrix[i][j + 1] + 1
            # This is the transposition case that makes Damerau-Levenshtein differ from Levenshtein.
            transposition = (
                distance_matrix[previous_match_row][previous_match_column]
                + (i - previous_match_row - 1)
                + 1
                + (j - previous_match_column - 1)
            )

            distance_matrix[i + 1][j + 1] = min(
                substitution,
                insertion,
                deletion,
                transposition,
            )

        last_seen[left[i - 1]] = i

    return distance_matrix[left_length + 1][right_length + 1]
