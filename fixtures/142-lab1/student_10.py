import sys


def next_palindrome(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    numbers = list(text)
    left = (len(numbers) - 1) // 2
    right = len(numbers) // 2
    while left >= 0 and numbers[left] == numbers[right]:
        left -= 1
        right += 1
    if left < 0 or numbers[left] < numbers[right]:
        carry = 1
        left = (len(numbers) - 1) // 2
        right = len(numbers) // 2
        while left >= 0:
            total = (ord(numbers[left]) - 48) + carry
            numbers[left] = chr((total % 10) + 48)
            numbers[right] = numbers[left]
            carry = total // 10
            left -= 1
            right += 1
        if carry:
            return "1" + ("0" * (len(text) - 1)) + "1"
    else:
        while left >= 0:
            numbers[right] = numbers[left]
            left -= 1
            right += 1
    return "".join(numbers)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    p = 0
    total = int(data[p])
    p += 1
    out = []
    while total > 0:
        total -= 1
        out.append(next_palindrome(data[p].decode()))
        p += 1
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
