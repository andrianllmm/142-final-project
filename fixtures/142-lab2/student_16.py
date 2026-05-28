import sys


def gap(a, b):
    d = a - b
    if d < 0:
        return -d
    return d


def insertion_sort(items):
    keys = [item[:3] for item in items]
    i = 1
    while i < len(items):
        current = items[i]
        current_key = keys[i]
        j = i - 1
        while j >= 0 and current_key < keys[j]:
            items[j + 1] = items[j]
            keys[j + 1] = keys[j]
            j -= 1
        items[j + 1] = current
        keys[j + 1] = current_key
        i += 1
    return items


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    p = 0
    cases = int(tokens[p])
    p += 1
    out = []
    while cases:
        cases -= 1
        sh = int(tokens[p])
        sw = int(tokens[p + 1])
        p += 2
        n = int(tokens[p])
        p += 1
        rows = []
        order = 0
        while order < n:
            nm = tokens[p].decode()
            h = int(tokens[p + 1])
            w = int(tokens[p + 2])
            p += 3
            rows.append((gap(sh, h), gap(sw, w), order, nm))
            order += 1
        insertion_sort(rows)
        names = []
        idx = 0
        while idx < len(rows):
            names.append(rows[idx][3])
            idx += 1
        out.append(" ".join(names))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
