import sys


def gap(a, b):
    diff = a - b
    if diff < 0:
        return -diff
    return diff


def merge(left, right):
    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            merged.append(left[i])
            i += 1
        elif left[i][0] > right[j][0]:
            merged.append(right[j])
            j += 1
        elif left[i][1] < right[j][1]:
            merged.append(left[i])
            i += 1
        elif left[i][1] > right[j][1]:
            merged.append(right[j])
            j += 1
        elif left[i][2] <= right[j][2]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged


def merge_sort(items):
    if len(items) < 2:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return merge(left, right)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    pos = 0
    tests = int(tokens[pos])
    pos += 1
    lines = []
    for _ in range(tests):
        sol_h = int(tokens[pos])
        sol_w = int(tokens[pos + 1])
        pos += 2
        total = int(tokens[pos])
        pos += 1
        actors = []
        idx = 0
        while idx < total:
            name = tokens[pos].decode()
            height = int(tokens[pos + 1])
            weight = int(tokens[pos + 2])
            pos += 3
            actors.append((gap(sol_h, height), gap(sol_w, weight), idx, name))
            idx += 1
        ordered = merge_sort(actors)
        out = []
        i = 0
        while i < len(ordered):
            out.append(ordered[i][3])
            i += 1
        lines.append(" ".join(out))
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
