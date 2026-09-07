from collections.abc import Sequence


def damerau_levenshtein_distance(a: Sequence[str], b: Sequence[str]) -> int:
    """
    Compute the Damerau-Levenshtein distance between two sequences.

    This dynamic programming formulation supports:
    - insertion
    - deletion
    - substitution
    - adjacent transposition (swap of neighboring elements)

    Interpretation:
    dp[i][j] represents the minimum number of edits required to transform
    the prefix a[:i] into the prefix b[:j].
    """
    # If both sequences are identical, no edits are needed.
    if a == b:
        return 0

    n, m = len(a), len(b)

    # dp table where each entry stores optimal edit distance for prefixes
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Base case initialization

    # If a[:0] (empty string) -> b[:j],
    # the only option is inserting all j elements from b.
    # So cost grows linearly with j.
    for j in range(m + 1):
        dp[0][j] = j

    # If a[:i] -> empty string b[:0],
    # the only option is deleting all i elements from a.
    # So cost grows linearly with i.
    for i in range(n + 1):
        dp[i][0] = i

    # Fill DP table bottom-up
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # COST: do current tokens match?
            # If they match, no substitution is needed (cost = 0).
            # If they differ, we must account for 1 substitution cost.
            cost = 0 if a[i - 1] == b[j - 1] else 1

            # DELETION
            #
            # We assume the optimal solution ends by deleting a[i-1].
            #
            # Meaning:
            # - We already optimally transformed a[:i-1] -> b[:j]
            # - Then we delete a[i-1] to reach a[:i]
            #
            # Why dp[i-1][j]?
            # Because we remove one character from A without consuming B.
            delete = dp[i - 1][j] + 1

            # INSERTION
            #
            # We assume the optimal solution ends by inserting b[j-1].
            #
            # Meaning:
            # - We already transformed a[:i] -> b[:j-1]
            # - Then we insert b[j-1] at the end
            #
            # Why dp[i][j-1]?
            # Because we consume one extra character from B.
            insert = dp[i][j - 1] + 1

            # SUBSTITUTION (or MATCH)
            #
            # We align last characters a[i-1] and b[j-1].
            #
            # Meaning:
            # - We already solved a[:i-1] -> b[:j-1]
            # - Then we fix the last character:
            #   - cost = 0 if equal (no edit needed)
            #   - cost = 1 if different (substitution)
            #
            # Why dp[i-1][j-1]?
            # Because both prefixes shrink by one character.
            substitute = dp[i - 1][j - 1] + cost

            # Start with best of the three classical edit operations
            dp[i][j] = min(delete, insert, substitute)

            # TRANSPOSITION (adjacent swap)
            #
            # This handles cases where two neighboring elements are swapped:
            # Example: "ab" -> "ba"
            #
            # Condition:
            # a[i-1] must match b[j-2]
            # a[i-2] must match b[j-1]
            #
            # Why?
            # We are checking if the last two characters are reversed.
            #
            # If true:
            # - We assume we came from dp[i-2][j-2]
            # - Because both swapped elements are consumed at once
            # - Cost is 1 (single swap operation)
            #
            # Why dp[i-2][j-2]?
            # Because a transposition consumes TWO characters from each string.
            # -------------------------------------------------------
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                transpose = dp[i - 2][j - 2] + 1

                # Compare against existing best solution:
                # transposition may be cheaper than insertion/deletion/substitution
                dp[i][j] = min(dp[i][j], transpose)

    # Final answer: full transformation from a[:n] -> b[:m]
    return dp[n][m]
