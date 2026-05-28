def nextPalindrome(n):
    digits = list(str(n))
    original = n
    pairs = len(digits) // 2

    for offset in range(pairs):
        digits[-1 - offset] = digits[offset]

    result = int("".join(digits))
    if result > original:
        return result

    cursor = (len(digits) - 1) // 2
    carry = 1

    while cursor >= 0:
        updated = int(digits[cursor]) + carry
        digits[cursor] = str(updated % 10)
        carry = updated // 10
        if carry == 0:
            break
        cursor -= 1

    if carry:
        return int("1" + ("0" * (len(digits) - 1)) + "1")

    for offset in range(pairs):
        digits[-1 - offset] = digits[offset]

    return int("".join(digits))
