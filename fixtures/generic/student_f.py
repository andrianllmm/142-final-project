def is_prime(number):
    if number < 2:
        return False

    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1

    return True


def list_primes(limit):
    primes = []

    for number in range(2, limit + 1):
        if is_prime(number):
            primes.append(number)

    return primes
