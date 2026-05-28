import sys


def digits_of(text):
    result = []
    for ch in text:
        result.append(ord(ch) - 48)
    return result


def render(digits):
    pieces = []
    for value in digits:
        pieces.append(chr(value + 48))
    return "".join(pieces)


def next_palindrome(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    digits = digits_of(text)
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
        return render(digits)
    while left >= 0:
        digits[right] = digits[left]
        left -= 1
        right += 1
    return render(digits)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    idx = 0
    cases = int(tokens[idx])
    idx += 1
    out = []
    for _ in range(cases):
        out.append(next_palindrome(tokens[idx].decode()))
        idx += 1
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
