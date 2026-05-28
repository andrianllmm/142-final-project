import sys


def make(text):
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
            return "1" + ("0" * (len(text) - 1)) + "1"
    else:
        while left >= 0:
            chars[right] = chars[left]
            left -= 1
            right += 1
    return "".join(chars)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    cases = int(data[pos])
    pos += 1
    result = []
    while cases > 0:
        cases -= 1
        result.append(make(data[pos].decode()))
        pos += 1
    sys.stdout.write("\n".join(result))


if __name__ == "__main__":
    main()
