def nextPalindrome(n):
    number = int(n)
    candidate = number + 1

    while str(candidate) != str(candidate)[::-1]:
        candidate += 1

    return candidate
