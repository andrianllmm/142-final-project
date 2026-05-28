import sys


def diff(a, b):
    value = a - b
    if value < 0:
        return -value
    return value


def merge_sort(values):
    n = len(values)
    if n < 2:
        return values
    mid = n // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])
    merged = []
    li = 0
    ri = 0
    while li < len(left) and ri < len(right):
        l_key = left[li][:3]
        r_key = right[ri][:3]
        if l_key <= r_key:
            merged.append(left[li])
            li += 1
        else:
            merged.append(right[ri])
            ri += 1
    while li < len(left):
        merged.append(left[li])
        li += 1
    while ri < len(right):
        merged.append(right[ri])
        ri += 1
    return merged


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    p = 0
    cases = int(tokens[p])
    p += 1
    output = []
    for _ in range(cases):
        sol_h = int(tokens[p])
        sol_w = int(tokens[p + 1])
        p += 2
        count = int(tokens[p])
        p += 1
        records = []
        order = 0
        while order < count:
            name = tokens[p].decode()
            h = int(tokens[p + 1])
            w = int(tokens[p + 2])
            p += 3
            records.append((diff(sol_h, h), diff(sol_w, w), order, name))
            order += 1
        records = merge_sort(records)
        line = []
        index = 0
        while index < len(records):
            line.append(records[index][3])
            index += 1
        output.append(" ".join(line))
    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
