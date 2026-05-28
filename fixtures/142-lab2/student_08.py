import sys


def score(item):
    return item[0], item[1], item[2]


def partition(values, start, end):
    pivot = score(values[start + (end - start) // 2])
    i = start
    j = end
    while True:
        while score(values[i]) < pivot:
            i += 1
        while score(values[j]) > pivot:
            j -= 1
        if i > j:
            return i, j
        values[i], values[j] = values[j], values[i]
        i += 1
        j -= 1


def quicksort(values, start, end):
    if start >= end:
        return
    i, j = partition(values, start, end)
    if start < j:
        quicksort(values, start, j)
    if i < end:
        quicksort(values, i, end)


def delta(a, b):
    n = a - b
    if n < 0:
        return -n
    return n


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    index = 0
    cases = int(data[index])
    index += 1
    result = []
    while cases > 0:
        cases -= 1
        sol_h = int(data[index])
        sol_w = int(data[index + 1])
        index += 2
        total = int(data[index])
        index += 1
        people = []
        audition = 0
        while audition < total:
            nm = data[index].decode()
            h = int(data[index + 1])
            w = int(data[index + 2])
            index += 3
            people.append((delta(sol_h, h), delta(sol_w, w), audition, nm))
            audition += 1
        quicksort(people, 0, len(people) - 1)
        names = []
        for row in people:
            names.append(row[3])
        result.append(" ".join(names))
    sys.stdout.write("\n".join(result))


if __name__ == "__main__":
    main()
