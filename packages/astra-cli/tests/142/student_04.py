def copy_left_to_right(items):
    for index in range(len(items) // 2):
        items[-index - 1] = items[index]


def nextPalindrome(n):
    value = list(str(n))
    old_number = int("".join(value))

    copy_left_to_right(value)
    possible = int("".join(value))
    if possible > old_number:
        return possible

    center = (len(value) - 1) // 2
    while center >= 0:
        if value[center] != "9":
            value[center] = str(int(value[center]) + 1)
            break
        value[center] = "0"
        center -= 1

    if center < 0:
        return int("1" + ("0" * (len(value) - 1)) + "1")

    copy_left_to_right(value)
    return int("".join(value))
