import sys


def to_digits(text):
    digits = []
    i = 0
    while i < len(text):
        digits.append(ord(text[i]) - 48)
        i += 1
    return digits


def from_digits(digits):
    chars = []
    for value in digits:
        chars.append(chr(value + 48))
    return "".join(chars)


def next_palindrome(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    digits = to_digits(text)
    left = (len(digits) - 1) // 2
    right = len(digits) // 2
    while left >= 0 and digits[left] == digits[right]:
        left -= 1
        right += 1
    if left < 0 or digits[left] < digits[right]:
        carry = 1
        left = (len(digits) - 1) // 2
        right = len(digits) // 2
        while left >= 0:
            total = digits[left] + carry
            digits[left] = total % 10
            digits[right] = digits[left]
            carry = total // 10
            left -= 1
            right += 1
        if carry:
            return "1" + ("0" * (len(text) - 1)) + "1"
        return from_digits(digits)
    while left >= 0:
        digits[right] = digits[left]
        left -= 1
        right += 1
    return from_digits(digits)


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return
    pos = 0
    cases = int(raw[pos])
    pos += 1
    res = []
    while cases > 0:
        cases -= 1
        res.append(next_palindrome(raw[pos].decode()))
        pos += 1
    sys.stdout.write("\n".join(res))


if __name__ == "__main__":
    main()
