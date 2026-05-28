def make_candidate(source):
    data = list(source)
    for index in range(len(data) // 2):
        data[len(data) - index - 1] = data[index]
    return "".join(data)


def nextPalindrome(n):
    source = str(n)
    candidate = make_candidate(source)
    if int(candidate) > n:
        return int(candidate)

    middle_end = (len(source) + 1) // 2
    changed_left = str(int(source[:middle_end]) + 1)

    if len(changed_left) > middle_end:
        return int("1" + ("0" * (len(source) - 1)) + "1")

    fixed = changed_left + source[middle_end:]
    return int(make_candidate(fixed))
