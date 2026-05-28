import sys


def increment_prefix(chars, left, right):
    carry = 1
    while left >= 0:
        total = (ord(chars[left]) - 48) + carry
        chars[left] = chr((total % 10) + 48)
        chars[right] = chars[left]
        carry = total // 10
        left -= 1
        right += 1
    return carry


def next_palindrome(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    chars = list(text)
    left = (len(chars) - 1) // 2
    right = len(chars) // 2
    while left >= 0 and chars[left] == chars[right]:
        left -= 1
        right += 1
    if left < 0 or chars[left] < chars[right]:
        left = (len(chars) - 1) // 2
        right = len(chars) // 2
        if increment_prefix(chars, left, right):
            return "1" + ("0" * (len(text) - 1)) + "1"
    else:
        while left >= 0:
            chars[right] = chars[left]
            left -= 1
            right += 1
    return "".join(chars)


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return
    idx = 0
    cases = int(raw[idx])
    idx += 1
    out = []
    for _ in range(cases):
        out.append(next_palindrome(raw[idx].decode()))
        idx += 1
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
