def nextPalindrome(n):
    current = str(n + 1)

    while True:
        reverse = ""
        for char in current:
            reverse = char + reverse

        if current == reverse:
            return int(current)

        current = str(int(current) + 1)
