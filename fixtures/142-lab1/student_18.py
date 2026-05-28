import sys


def grow(text):
    if text == "0":
        return "1"
    if text.count("9") == len(text):
        return "1" + ("0" * (len(text) - 1)) + "1"
    arr = list(text)
    l = (len(arr) - 1) // 2
    r = len(arr) // 2
    while l >= 0 and arr[l] == arr[r]:
        l -= 1
        r += 1
    if l < 0 or arr[l] < arr[r]:
        carry = 1
        l = (len(arr) - 1) // 2
        r = len(arr) // 2
        while l >= 0:
            value = (ord(arr[l]) - 48) + carry
            arr[l] = chr((value % 10) + 48)
            arr[r] = arr[l]
            carry = value // 10
            l -= 1
            r += 1
        if carry:
            return "1" + ("0" * (len(text) - 1)) + "1"
    else:
        while l >= 0:
            arr[r] = arr[l]
            l -= 1
            r += 1
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
        out.append(grow(raw[pos].decode()))
        pos += 1
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
