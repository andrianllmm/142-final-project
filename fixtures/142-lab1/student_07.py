def build_palindrome(prefix, odd_length):
    text = str(prefix)
    if odd_length:
        return int(text + text[-2::-1])
    return int(text + text[::-1])


def nextPalindrome(n):
    digits = str(n)
    prefix_size = (len(digits) + 1) // 2
    prefix = int(digits[:prefix_size])
    odd_length = len(digits) % 2 == 1

    answer = build_palindrome(prefix, odd_length)
    if answer > n:
        return answer

    answer = build_palindrome(prefix + 1, odd_length)
    if len(str(answer)) == len(digits):
        return answer

    return int("1" + ("0" * (len(digits) - 1)) + "1")
