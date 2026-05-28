import sys


def build_candidate(chars):
    left = (len(chars) - 1) // 2
    right = len(chars) // 2
    while left >= 0 and chars[left] == chars[right]:
        left -= 1
        right += 1
    if left < 0 or chars[left] < chars[right]:
        carry = 1
        left = (len(chars) - 1) // 2
        right = len(chars) // 2
        while left >= 0:
            total = (ord(chars[left]) - 48) + carry
            chars[left] = chr((total % 10) + 48)
            chars[right] = chars[left]
            carry = total // 10
            left -= 1
            right += 1
        if carry:
            return None
    else:
        while left >= 0:
            chars[right] = chars[left]
            left -= 1
            right += 1
    return "".join(chars)


def next_palindrome(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    chars = list(text)
    result = build_candidate(chars)
    if result is None:
        return "1" + ("0" * (len(text) - 1)) + "1"
    return result


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    pos = 0
    count = int(tokens[pos])
    pos += 1
    lines = []
    while count > 0:
        count -= 1
        lines.append(next_palindrome(tokens[pos].decode()))
        pos += 1
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
