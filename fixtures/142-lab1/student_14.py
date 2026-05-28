def nextPalindrome(n):
    digits = list(str(n))
    amount = len(digits)
    left_side = 0
    right_side = amount - 1

    while left_side < right_side:
        digits[right_side] = digits[left_side]
        left_side += 1
        right_side -= 1

    if int("".join(digits)) > n:
        return int("".join(digits))

    middle = amount // 2
    if amount % 2 == 0:
        middle -= 1

    while middle >= 0:
        if digits[middle] == "9":
            digits[middle] = "0"
            middle -= 1
        else:
            digits[middle] = str(int(digits[middle]) + 1)
            break

    if middle < 0:
        return int("1" + ("0" * (amount - 1)) + "1")

    left_side = 0
    right_side = amount - 1
    while left_side < right_side:
        digits[right_side] = digits[left_side]
        left_side += 1
        right_side -= 1

    return int("".join(digits))
