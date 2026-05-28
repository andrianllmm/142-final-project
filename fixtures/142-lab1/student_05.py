def is_palindrome(number):
    word = str(number)
    return word == word[::-1]


def nextPalindrome(n):
    answer = n + 1
    while not is_palindrome(answer):
        answer += 1
    return answer
