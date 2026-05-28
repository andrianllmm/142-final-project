def nextPalindrome(n):
    def okay(value):
        letters = str(value)
        for index in range(len(letters) // 2):
            if letters[index] != letters[-index - 1]:
                return False
        return True

    next_number = n + 1
    while not okay(next_number):
        next_number += 1

    return next_number
