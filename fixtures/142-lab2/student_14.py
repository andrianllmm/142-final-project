import sys


def distance(a, b):
    n = a - b
    if n < 0:
        return -n
    return n


def insert_sort(rows):
    for i in range(1, len(rows)):
        item = rows[i]
        pos = i - 1
        while pos >= 0 and item[:3] < rows[pos][:3]:
            rows[pos + 1] = rows[pos]
            pos -= 1
        rows[pos + 1] = item
    return rows


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    p = 0
    cases = int(tokens[p])
    p += 1
    lines = []
    while cases:
        cases -= 1
        sh = int(tokens[p])
        sw = int(tokens[p + 1])
        p += 2
        count = int(tokens[p])
        p += 1
        actors = []
        idx = 0
        while idx < count:
            name = tokens[p].decode()
            h = int(tokens[p + 1])
            w = int(tokens[p + 2])
            p += 3
            actors.append((distance(sh, h), distance(sw, w), idx, name))
            idx += 1
        insert_sort(actors)
        names = []
        i = 0
        while i < len(actors):
            names.append(actors[i][3])
            i += 1
        lines.append(" ".join(names))
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
