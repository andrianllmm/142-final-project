def nextPalindrome(n):
    text = str(n)
    length = len(text)
    left = text[: length // 2]

    if length % 2 == 0:
        candidate = int(left + left[::-1])
    else:
        candidate = int(left + text[length // 2] + left[::-1])

    if candidate > n:
        return candidate

    prefix_length = (length + 1) // 2
    prefix = int(text[:prefix_length]) + 1
    prefix_text = str(prefix)

    if len(prefix_text) > prefix_length:
        return int("1" + ("0" * (length - 1)) + "1")

    if length % 2 == 0:
        return int(prefix_text + prefix_text[::-1])

    return int(prefix_text + prefix_text[:-1][::-1])
