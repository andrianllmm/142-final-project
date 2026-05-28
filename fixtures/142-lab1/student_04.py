import sys


def build_next(value):
    if value == "0":
        return "1"
    if value.count("9") == len(value):
        return "1" + ("0" * (len(value) - 1)) + "1"
    digits = list(value)
    mid_left = (len(digits) - 1) // 2
    mid_right = len(digits) // 2
    while mid_left >= 0 and digits[mid_left] == digits[mid_right]:
        mid_left -= 1
        mid_right += 1
    if mid_left < 0 or digits[mid_left] < digits[mid_right]:
        carry = 1
        mid_left = (len(digits) - 1) // 2
        mid_right = len(digits) // 2
        while mid_left >= 0:
            num = (ord(digits[mid_left]) - 48) + carry
            digits[mid_left] = chr((num % 10) + 48)
            digits[mid_right] = digits[mid_left]
            carry = num // 10
            mid_left -= 1
            mid_right += 1
        if carry:
            return "1" + ("0" * (len(value) - 1)) + "1"
        return "".join(digits)
    while mid_left >= 0:
        digits[mid_right] = digits[mid_left]
        mid_left -= 1
        mid_right += 1
    return "".join(digits)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    index = 0
    total = int(tokens[index])
    index += 1
    answers = []
    for _ in range(total):
        answers.append(build_next(tokens[index].decode()))
        index += 1
    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()
