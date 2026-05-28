def reverse_text(text):
    result = []
    for index in range(len(text) - 1, -1, -1):
        result.append(text[index])
    return "".join(result)


def nextPalindrome(n):
    target = n + 1

    while True:
        label = str(target)
        if label == reverse_text(label):
            return target
        target += 1
