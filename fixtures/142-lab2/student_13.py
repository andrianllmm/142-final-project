import sys


def gap(a, b):
    x = a - b
    if x < 0:
        return -x
    return x


def comes_before(first, second):
    return first[:3] < second[:3]


def insertion_sort(items):
    i = 1
    while i < len(items):
        current = items[i]
        j = i - 1
        while j >= 0 and comes_before(current, items[j]):
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current
        i += 1
    return items


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return
    p = 0
    tests = int(raw[p])
    p += 1
    out = []
    for _ in range(tests):
        sh = int(raw[p])
        sw = int(raw[p + 1])
        p += 2
        count = int(raw[p])
        p += 1
        rows = []
        order = 0
        while order < count:
            name = raw[p].decode()
            h = int(raw[p + 1])
            w = int(raw[p + 2])
            p += 3
            rows.append((gap(sh, h), gap(sw, w), order, name))
            order += 1
        rows = insertion_sort(rows)
        names = []
        for row in rows:
            names.append(row[3])
        out.append(" ".join(names))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
