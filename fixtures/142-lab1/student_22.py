import sys


def next_palindrome(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    chars = list(text)
    l = (len(chars) - 1) // 2
    r = len(chars) // 2
    while l >= 0 and chars[l] == chars[r]:
        l -= 1
        r += 1
    if l < 0 or chars[l] < chars[r]:
        carry = 1
        l = (len(chars) - 1) // 2
        r = len(chars) // 2
        while l >= 0:
            total = (ord(chars[l]) - 48) + carry
            chars[l] = chr((total % 10) + 48)
            chars[r] = chars[l]
            carry = total // 10
            l -= 1
            r += 1
        if carry:
            return "1" + ("0" * (len(text) - 1)) + "1"
    else:
        while l >= 0:
            chars[r] = chars[l]
            l -= 1
            r += 1
    return "".join(chars)


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return
    idx = 0
    cases = int(raw[idx])
    idx += 1
    lines = []
    while cases > 0:
        cases -= 1
        lines.append(next_palindrome(raw[idx].decode()))
        idx += 1
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
