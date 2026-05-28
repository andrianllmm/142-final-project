def average_grade(values):
    running_sum = 0

    for value in values:
        running_sum += value

    return running_sum / len(values)


def has_passing_mark(values):
    grade_average = average_grade(values)
    return grade_average >= 75
