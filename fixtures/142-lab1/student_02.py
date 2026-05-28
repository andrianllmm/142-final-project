import sys


def next_pal(s):
    if s == "0":
        return "1"
    if s.count("9") == len(s):
        return "1" + ("0" * (len(s) - 1)) + "1"
    arr = list(s)
    i = (len(arr) - 1) // 2
    j = len(arr) // 2
    while i >= 0 and arr[i] == arr[j]:
        i -= 1
        j += 1
    need_bump = i < 0 or arr[i] < arr[j]
    i = (len(arr) - 1) // 2
    j = len(arr) // 2
    if need_bump:
        carry = 1
        while i >= 0:
            digit = ord(arr[i]) - 48 + carry
            arr[i] = chr((digit % 10) + 48)
            arr[j] = arr[i]
            carry = digit // 10
            i -= 1
            j += 1
        if carry:
            return "1" + ("0" * (len(s) - 1)) + "1"
    else:
        while i >= 0:
            arr[j] = arr[i]
            i -= 1
            j += 1
    return "".join(arr)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    p = 0
    t = int(tokens[p])
    p += 1
    ans = []
    while t:
        t -= 1
        ans.append(next_pal(tokens[p].decode()))
        p += 1
    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()
