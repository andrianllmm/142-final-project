import sys


def cmp_digits(a, b):
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


def next_palindrome(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    digits = list(text)
    left = (len(digits) - 1) // 2
    right = len(digits) // 2
    while left >= 0 and digits[left] == digits[right]:
        left -= 1
        right += 1
    if left < 0 or cmp_digits(digits[left], digits[right]) < 0:
        carry = 1
        left = (len(digits) - 1) // 2
        right = len(digits) // 2
        while left >= 0:
            current = ord(digits[left]) - 48 + carry
            digits[left] = chr((current % 10) + 48)
            digits[right] = digits[left]
            carry = current // 10
            left -= 1
            right += 1
        if carry:
            return "1" + ("0" * (len(text) - 1)) + "1"
        return "".join(digits)
    while left >= 0:
        digits[right] = digits[left]
        left -= 1
        right += 1
    return "".join(digits)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    n = 0
    cases = int(tokens[n])
    n += 1
    lines = []
    while cases > 0:
        cases -= 1
        lines.append(next_palindrome(tokens[n].decode()))
        n += 1
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
