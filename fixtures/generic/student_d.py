def summarize_scores(scores):
    highest = scores[0]
    lowest = scores[0]
    total = 0

    for score in scores:
        if score > highest:
            highest = score
        if score < lowest:
            lowest = score
        total += score

    average = total / len(scores)
    return {
        "highest": highest,
        "lowest": lowest,
        "average": average,
        "passed": average >= 75,
    }
