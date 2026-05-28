def nextPalindrome(n):
    digits = str(n)
    midpoint = len(digits) // 2

    if len(digits) % 2 == 0:
        first = digits[:midpoint]
        guess = first + first[::-1]
    else:
        first = digits[: midpoint + 1]
        guess = first + first[:-1][::-1]

    if int(guess) > n:
        return int(guess)

    first = str(int(first) + 1)

    if len(first) > midpoint + (len(digits) % 2):
        return int("1" + ("0" * (len(digits) - 1)) + "1")

    if len(digits) % 2 == 0:
        return int(first + first[::-1])

    return int(first + first[:-1][::-1])
