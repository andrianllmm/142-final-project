import sys


def gap(a, b):
    diff = a - b
    if diff < 0:
        return -diff
    return diff


def quicksort(items, left, right):
    if left >= right:
        return
    pivot = items[right][:3]
    i = left
    j = right - 1
    while i <= j:
        while i <= j and items[i][:3] < pivot:
            i += 1
        while i <= j and items[j][:3] > pivot:
            j -= 1
        if i <= j:
            items[i], items[j] = items[j], items[i]
            i += 1
            j -= 1
    items[i], items[right] = items[right], items[i]
    quicksort(items, left, i - 1)
    quicksort(items, i + 1, right)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    p = 0
    tests = int(tokens[p])
    p += 1
    out = []
    for _ in range(tests):
        sol_h = int(tokens[p])
        sol_w = int(tokens[p + 1])
        p += 2
        count = int(tokens[p])
        p += 1
        people = []
        order = 0
        while order < count:
            name = tokens[p].decode()
            h = int(tokens[p + 1])
            w = int(tokens[p + 2])
            p += 3
            people.append((gap(sol_h, h), gap(sol_w, w), order, name))
            order += 1
        quicksort(people, 0, len(people) - 1)
        names = []
        i = 0
        while i < len(people):
            names.append(people[i][3])
            i += 1
        out.append(" ".join(names))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
