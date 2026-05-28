def nextPalindrome(n):
    digits = list(map(int, str(n)))
    length = len(digits)

    for left in range(length // 2):
        right = length - left - 1
        digits[right] = digits[left]

    candidate = int("".join(str(digit) for digit in digits))
    if candidate > n:
        return candidate

    index = (length - 1) // 2
    carry = 1
    while index >= 0:
        total = digits[index] + carry
        digits[index] = total % 10
        carry = total // 10
        if carry == 0:
            break
        index -= 1

    if carry:
        return int("1" + ("0" * (length - 1)) + "1")

    for left in range(length // 2):
        right = length - left - 1
        digits[right] = digits[left]

    return int("".join(str(digit) for digit in digits))
