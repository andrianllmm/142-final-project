def calculate_average(scores):
    total = 0

    for score in scores:
        total += score

    return total / len(scores)


def passed_course(scores):
    average = calculate_average(scores)
    return average >= 75
