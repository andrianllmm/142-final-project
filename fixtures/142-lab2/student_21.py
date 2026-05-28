import sys


def gap(a, b):
    x = a - b
    if x < 0:
        return -x
    return x


def better(left, right):
    if left[0] != right[0]:
        return left[0] < right[0]
    if left[1] != right[1]:
        return left[1] < right[1]
    return left[2] < right[2]


def selection_sort(items):
    n = len(items)
    for i in range(n):
        best = i
        for j in range(i + 1, n):
            if better(items[j], items[best]):
                best = j
        if best != i:
            items[i], items[best] = items[best], items[i]
    return items


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    p = 0
    tests = int(tokens[p])
    p += 1
    out = []
    for _ in range(tests):
        sh = int(tokens[p])
        sw = int(tokens[p + 1])
        p += 2
        count = int(tokens[p])
        p += 1
        people = []
        rank = 0
        while rank < count:
            name = tokens[p].decode()
            h = int(tokens[p + 1])
            w = int(tokens[p + 2])
            p += 3
            people.append((gap(sh, h), gap(sw, w), rank, name))
            rank += 1
        selection_sort(people)
        names = []
        for person in people:
            names.append(person[3])
        out.append(" ".join(names))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
