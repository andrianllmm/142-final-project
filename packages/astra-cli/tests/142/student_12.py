def nextPalindrome(n):
    number = n + 1

    while True:
        digits = []
        temporary = number

        while temporary > 0:
            digits.append(temporary % 10)
            temporary //= 10

        if digits == digits[::-1]:
            return number

        number += 1
