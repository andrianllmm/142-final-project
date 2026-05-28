def nextPalindrome(n):
    word = str(n)
    count = len(word)

    if set(word) == {"9"}:
        return int("1" + ("0" * (count - 1)) + "1")

    middle_count = (count + 1) // 2
    left_part = int(word[:middle_count])

    while True:
        front = str(left_part)
        if len(front) < middle_count:
            front = ("0" * (middle_count - len(front))) + front

        if count % 2:
            possible = int(front + front[:-1][::-1])
        else:
            possible = int(front + front[::-1])

        if possible > n:
            return possible

        left_part += 1
