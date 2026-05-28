def mirror(chars):
    start = 0
    end = len(chars) - 1
    while start < end:
        chars[end] = chars[start]
        start += 1
        end -= 1


def increase_middle(chars):
    point = (len(chars) - 1) // 2
    while point >= 0:
        if chars[point] == "9":
            chars[point] = "0"
            point -= 1
            continue
        chars[point] = str(int(chars[point]) + 1)
        return chars
    return ["1"] + ["0"] * (len(chars) - 1) + ["1"]


def nextPalindrome(n):
    chars = list(str(n))
    mirror(chars)
    if int("".join(chars)) > n:
        return int("".join(chars))

    chars = increase_middle(chars)
    mirror(chars)
    return int("".join(chars))
