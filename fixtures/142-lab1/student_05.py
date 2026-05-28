import sys


def next_palindrome(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    arr = list(text)
    left = (len(arr) - 1) // 2
    right = len(arr) // 2
    while left >= 0 and arr[left] == arr[right]:
        left -= 1
        right += 1
    if left < 0 or arr[left] < arr[right]:
        carry = 1
        left = (len(arr) - 1) // 2
        right = len(arr) // 2
        while left >= 0:
            current = ord(arr[left]) - 48 + carry
            arr[left] = chr((current % 10) + 48)
            arr[right] = arr[left]
            carry = current // 10
            left -= 1
            right += 1
        if carry:
            return "1" + ("0" * (len(text) - 1)) + "1"
    else:
        while left >= 0:
            arr[right] = arr[left]
            left -= 1
            right += 1
    return "".join(arr)


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return
    pos = 0
    cases = int(raw[pos])
    pos += 1
    out = []
    while cases:
        cases -= 1
        out.append(next_palindrome(raw[pos].decode()))
        pos += 1
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
