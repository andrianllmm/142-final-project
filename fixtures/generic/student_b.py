def get_mean(grades):
    result = 0

    for grade in grades:
        result += grade

    return result / len(grades)


def is_passing(grades):
    mean = get_mean(grades)
    return mean >= 75
