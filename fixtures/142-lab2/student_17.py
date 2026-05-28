import sys


def abs_gap(a, b):
    diff = a - b
    if diff < 0:
        return -diff
    return diff


def insertion_sort(values):
    i = 1
    while i < len(values):
        current = values[i]
        j = i - 1
        while j >= 0:
            if current[:3] >= values[j][:3]:
                break
            values[j + 1] = values[j]
            j -= 1
        values[j + 1] = current
        i += 1
    return values


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    tests = int(data[idx])
    idx += 1
    outputs = []
    for _ in range(tests):
        sh = int(data[idx])
        sw = int(data[idx + 1])
        idx += 2
        count = int(data[idx])
        idx += 1
        actors = []
        order = 0
        while order < count:
            name = data[idx].decode()
            h = int(data[idx + 1])
            w = int(data[idx + 2])
            idx += 3
            actors.append((abs_gap(sh, h), abs_gap(sw, w), order, name))
            order += 1
        insertion_sort(actors)
        names = []
        for actor in actors:
            names.append(actor[3])
        outputs.append(" ".join(names))
    sys.stdout.write("\n".join(outputs))


if __name__ == "__main__":
    main()
