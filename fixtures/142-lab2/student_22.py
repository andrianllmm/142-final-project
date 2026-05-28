import sys


def diff(a, b):
    value = a - b
    if value < 0:
        return -value
    return value


def selection_sort(data):
    n = len(data)
    i = 0
    while i < n:
        best = i
        j = i + 1
        while j < n:
            if data[j][:3] < data[best][:3]:
                best = j
            j += 1
        if best != i:
            picked = data[best]
            k = best
            while k > i:
                data[k] = data[k - 1]
                k -= 1
            data[i] = picked
        i += 1
    return data


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return
    p = 0
    cases = int(raw[p])
    p += 1
    lines = []
    while cases:
        cases -= 1
        sh = int(raw[p])
        sw = int(raw[p + 1])
        p += 2
        count = int(raw[p])
        p += 1
        actors = []
        order = 0
        while order < count:
            name = raw[p].decode()
            h = int(raw[p + 1])
            w = int(raw[p + 2])
            p += 3
            actors.append((diff(sh, h), diff(sw, w), order, name))
            order += 1
        selection_sort(actors)
        names = []
        idx = 0
        while idx < len(actors):
            names.append(actors[idx][3])
            idx += 1
        lines.append(" ".join(names))
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
