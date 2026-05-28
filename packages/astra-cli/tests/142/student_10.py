def nextPalindrome(n):
    if n < 9:
        return n + 1

    text = str(n)
    half = len(text) // 2
    middle = "" if len(text) % 2 == 0 else text[half]
    left = text[:half]
    trial = int(left + middle + left[::-1])

    if trial > n:
        return trial

    front = str(int(text[: half + len(middle)]) + 1)
    if len(front) > half + len(middle):
        return int("1" + ("0" * (len(text) - 1)) + "1")

    if middle:
        return int(front + front[:-1][::-1])

    return int(front + front[::-1])
