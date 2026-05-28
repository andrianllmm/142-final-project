import sys


def distance(a, b):
    diff = a - b
    return -diff if diff < 0 else diff


def merge_runs(source, left_start, left_end, right_end, target):
    i = left_start
    j = left_end
    k = left_start
    while i < left_end and j < right_end:
        left_item = source[i]
        right_item = source[j]
        if left_item[:3] <= right_item[:3]:
            target[k] = left_item
            i += 1
        else:
            target[k] = right_item
            j += 1
        k += 1
    while i < left_end:
        target[k] = source[i]
        i += 1
        k += 1
    while j < right_end:
        target[k] = source[j]
        j += 1
        k += 1


def bottom_up_merge_sort(items):
    size = len(items)
    if size < 2:
        return items
    temp = [None] * size
    width = 1
    src = items[:]
    dst = temp
    while width < size:
        start = 0
        while start < size:
            mid = start + width
            end = start + (width * 2)
            if mid > size:
                mid = size
            if end > size:
                end = size
            merge_runs(src, start, mid, end, dst)
            start += width * 2
        src, dst = dst, src
        width *= 2
    return src


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    p = 0
    t = int(tokens[p])
    p += 1
    answers = []
    for _ in range(t):
        sh = int(tokens[p])
        sw = int(tokens[p + 1])
        p += 2
        count = int(tokens[p])
        p += 1
        records = [None] * count
        i = 0
        while i < count:
            nm = tokens[p].decode()
            h = int(tokens[p + 1])
            w = int(tokens[p + 2])
            p += 3
            records[i] = (distance(sh, h), distance(sw, w), i, nm)
            i += 1
        ordered = bottom_up_merge_sort(records)
        names = [None] * count
        i = 0
        while i < count:
            names[i] = ordered[i][3]
            i += 1
        answers.append(" ".join(names))
    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()
