import sys


def gap(a, b):
    diff = a - b
    if diff < 0:
        return -diff
    return diff


def selection_sort(items):
    n = len(items)
    i = 0
    while i < n:
        best = i
        j = i + 1
        while j < n:
            if items[j][:3] < items[best][:3]:
                best = j
            j += 1
        if best != i:
            items[i], items[best] = items[best], items[i]
        i += 1
    return items


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    p = 0
    tests = int(data[p])
    p += 1
    out = []
    while tests:
        tests -= 1
        sh = int(data[p])
        sw = int(data[p + 1])
        p += 2
        count = int(data[p])
        p += 1
        actors = []
        order = 0
        while order < count:
            name = data[p].decode()
            h = int(data[p + 1])
            w = int(data[p + 2])
            p += 3
            actors.append((gap(sh, h), gap(sw, w), order, name))
            order += 1
        selection_sort(actors)
        names = []
        for actor in actors:
            names.append(actor[3])
        out.append(" ".join(names))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
