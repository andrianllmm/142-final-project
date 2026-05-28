def nextPalindrome(n):
    chars = [char for char in str(n)]
    size = len(chars)

    for position in range(size // 2):
        chars[size - position - 1] = chars[position]

    made = int("".join(chars))
    if made > n:
        return made

    add_at = (size - 1) // 2
    while add_at >= 0 and chars[add_at] == "9":
        chars[add_at] = "0"
        add_at -= 1

    if add_at == -1:
        return int("1" + ("0" * (size - 1)) + "1")

    chars[add_at] = str(int(chars[add_at]) + 1)

    for position in range(size // 2):
        chars[size - position - 1] = chars[position]

    return int("".join(chars))
