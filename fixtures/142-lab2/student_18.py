import sys


def gap(a, b):
    value = a - b
    if value < 0:
        return -value
    return value


def insert_sorted(items):
    for i in range(1, len(items)):
        current = items[i]
        key = current[:3]
        j = i - 1
        while j >= 0 and key < items[j][:3]:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current
    return items


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return
    p = 0
    cases = int(raw[p])
    p += 1
    lines = []
    while cases > 0:
        cases -= 1
        sh = int(raw[p])
        sw = int(raw[p + 1])
        p += 2
        total = int(raw[p])
        p += 1
        rows = []
        order = 0
        while order < total:
            name = raw[p].decode()
            h = int(raw[p + 1])
            w = int(raw[p + 2])
            p += 3
            rows.append((gap(sh, h), gap(sw, w), order, name))
            order += 1
        insert_sorted(rows)
        names = []
        index = 0
        while index < len(rows):
            names.append(rows[index][3])
            index += 1
        lines.append(" ".join(names))
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
