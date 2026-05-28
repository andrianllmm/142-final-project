def nextPalindrome(n):
    digits = list(str(n))
    original = int("".join(digits))

    def mirror_left():
        left = 0
        right = len(digits) - 1
        while left < right:
            digits[right] = digits[left]
            left += 1
            right -= 1

    mirror_left()
    if int("".join(digits)) > original:
        return int("".join(digits))

    middle = (len(digits) - 1) // 2
    carry = 1
    while middle >= 0 and carry:
        value = int(digits[middle]) + carry
        digits[middle] = str(value % 10)
        carry = value // 10
        middle -= 1

    if carry:
        digits = ["1"] + ["0"] * (len(digits) - 1) + ["1"]
    else:
        mirror_left()

    return int("".join(digits))
