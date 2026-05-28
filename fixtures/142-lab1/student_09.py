import sys


def grow(text):
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
            value = (ord(digits[left]) - 48) + carry
            digits[left] = chr((value % 10) + 48)
            digits[right] = digits[left]
            carry = value // 10
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
    buf = sys.stdin.buffer.read().split()
    if not buf:
        return
    idx = 0
    cases = int(buf[idx])
    idx += 1
    ans = []
    for _ in range(cases):
        ans.append(grow(buf[idx].decode()))
        idx += 1
    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()
