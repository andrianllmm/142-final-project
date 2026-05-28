import sys


def rank_key(record):
    return record[0], record[1], record[2]


def quicksort_stack(items):
    if len(items) < 2:
        return items
    stack = [(0, len(items) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        pivot = rank_key(items[(lo + hi) // 2])
        i = lo
        j = hi
        while i <= j:
            while rank_key(items[i]) < pivot:
                i += 1
            while rank_key(items[j]) > pivot:
                j -= 1
            if i <= j:
                items[i], items[j] = items[j], items[i]
                i += 1
                j -= 1
        if lo < j:
            stack.append((lo, j))
        if i < hi:
            stack.append((i, hi))
    return items


def dist(a, b):
    value = a - b
    if value < 0:
        return -value
    return value


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    cur = 0
    cases = int(data[cur])
    cur += 1
    lines = []
    while cases:
        cases -= 1
        sh = int(data[cur])
        sw = int(data[cur + 1])
        cur += 2
        n = int(data[cur])
        cur += 1
        rows = []
        idx = 0
        while idx < n:
            name = data[cur].decode()
            h = int(data[cur + 1])
            w = int(data[cur + 2])
            cur += 3
            rows.append((dist(sh, h), dist(sw, w), idx, name))
            idx += 1
        rows = quicksort_stack(rows)
        names = []
        for row in rows:
            names.append(row[3])
        lines.append(" ".join(names))
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
