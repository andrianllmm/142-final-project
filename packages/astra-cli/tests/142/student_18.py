def nextPalindrome(n):
    numbers = [int(item) for item in str(n)]
    old = int("".join(str(item) for item in numbers))

    low = 0
    high = len(numbers) - 1
    while low < high:
        numbers[high] = numbers[low]
        low += 1
        high -= 1

    trial = int("".join(str(item) for item in numbers))
    if trial > old:
        return trial

    mid = (len(numbers) - 1) // 2
    done = False
    while mid >= 0 and not done:
        numbers[mid] += 1
        if numbers[mid] == 10:
            numbers[mid] = 0
            mid -= 1
        else:
            done = True

    if not done:
        return int("1" + ("0" * (len(numbers) - 1)) + "1")

    low = 0
    high = len(numbers) - 1
    while low < high:
        numbers[high] = numbers[low]
        low += 1
        high -= 1

    return int("".join(str(item) for item in numbers))
