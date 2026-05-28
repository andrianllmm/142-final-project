import sys


def gap(a, b):
    delta = a - b
    if delta < 0:
        return -delta
    return delta


def qs(values, lo, hi):
    if lo >= hi:
        return
    pivot = values[lo][:3]
    i = lo + 1
    j = hi
    while i <= j:
        while i <= j and values[i][:3] <= pivot:
            i += 1
        while i <= j and values[j][:3] >= pivot:
            j -= 1
        if i < j:
            values[i], values[j] = values[j], values[i]
            i += 1
            j -= 1
    values[lo], values[j] = values[j], values[lo]
    qs(values, lo, j - 1)
    qs(values, j + 1, hi)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    pos = 0
    t = int(tokens[pos])
    pos += 1
    out = []
    for _ in range(t):
        sh = int(tokens[pos])
        sw = int(tokens[pos + 1])
        pos += 2
        count = int(tokens[pos])
        pos += 1
        people = []
        order = 0
        while order < count:
            name = tokens[pos].decode()
            h = int(tokens[pos + 1])
            w = int(tokens[pos + 2])
            pos += 3
            people.append((gap(sh, h), gap(sw, w), order, name))
            order += 1
        qs(people, 0, len(people) - 1)
        names = []
        idx = 0
        while idx < len(people):
            names.append(people[idx][3])
            idx += 1
        out.append(" ".join(names))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
