def count_words(sentence):
    counts = {}

    for word in sentence.lower().split():
        if word not in counts:
            counts[word] = 0
        counts[word] += 1

    return counts


def most_common_word(sentence):
    counts = count_words(sentence)
    best_word = ""
    best_count = 0

    for word, count in counts.items():
        if count > best_count:
            best_word = word
            best_count = count

    return best_word
