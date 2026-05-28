import sys


def make_next(number):
    if number == "0":
        return "1"
    if number.count("9") == len(number):
        return "1" + ("0" * (len(number) - 1)) + "1"
    digits = list(number)
    a = (len(digits) - 1) // 2
    b = len(digits) // 2
    while a >= 0 and digits[a] == digits[b]:
        a -= 1
        b += 1
    if a < 0 or digits[a] < digits[b]:
        carry = 1
        a = (len(digits) - 1) // 2
        b = len(digits) // 2
        while a >= 0:
            total = (ord(digits[a]) - 48) + carry
            digits[a] = chr((total % 10) + 48)
            digits[b] = digits[a]
            carry = total // 10
            a -= 1
            b += 1
        if carry:
            return "1" + ("0" * (len(number) - 1)) + "1"
    else:
        while a >= 0:
            digits[b] = digits[a]
            a -= 1
            b += 1
    return "".join(digits)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    i = 0
    t = int(tokens[i])
    i += 1
    result = []
    while t > 0:
        t -= 1
        result.append(make_next(tokens[i].decode()))
        i += 1
    sys.stdout.write("\n".join(result))


if __name__ == "__main__":
    main()
