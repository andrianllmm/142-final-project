import sys


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
        carry = 1
        left = (len(chars) - 1) // 2
        right = len(chars) // 2
        while left >= 0:
            current = (ord(chars[left]) - 48) + carry
            chars[left] = chr((current % 10) + 48)
            chars[right] = chars[left]
            carry = current // 10
            left -= 1
            right += 1
        if carry:
            return "1" + ("0" * (len(text) - 1)) + "1"
        return "".join(chars)
    while left >= 0:
        chars[right] = chars[left]
        left -= 1
        right += 1
    return "".join(chars)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    index = 0
    count = int(tokens[index])
    index += 1
    output = []
    while count > 0:
        count -= 1
        output.append(next_palindrome(tokens[index].decode()))
        index += 1
    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
