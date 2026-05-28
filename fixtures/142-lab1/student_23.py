import sys


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
    if left < 0 or digits[left] < digits[right]:
        carry = 1
        left = (len(digits) - 1) // 2
        right = len(digits) // 2
        while left >= 0:
            current = (ord(digits[left]) - 48) + carry
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
    idx = 0
    total = int(tokens[idx])
    idx += 1
    out = []
    while total > 0:
        total -= 1
        out.append(next_palindrome(tokens[idx].decode()))
        idx += 1
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
