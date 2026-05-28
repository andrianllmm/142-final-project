import sys


def key_of(item):
    return item[0], item[1], item[2]


def partition(data, lo, hi):
    pivot = key_of(data[(lo + hi) // 2])
    left = lo
    right = hi
    while left <= right:
        while key_of(data[left]) < pivot:
            left += 1
        while key_of(data[right]) > pivot:
            right -= 1
        if left <= right:
            data[left], data[right] = data[right], data[left]
            left += 1
            right -= 1
    return left, right


def quick_sort(data, lo, hi):
    if lo >= hi:
        return
    left, right = partition(data, lo, hi)
    if lo < right:
        quick_sort(data, lo, right)
    if left < hi:
        quick_sort(data, left, hi)


def abs_gap(a, b):
    d = a - b
    if d < 0:
        return -d
    return d


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return
    pos = 0
    t = int(raw[pos])
    pos += 1
    lines = []
    for _ in range(t):
        sh = int(raw[pos])
        sw = int(raw[pos + 1])
        pos += 2
        count = int(raw[pos])
        pos += 1
        people = []
        order = 0
        while order < count:
            name = raw[pos].decode()
            h = int(raw[pos + 1])
            w = int(raw[pos + 2])
            pos += 3
            people.append((abs_gap(sh, h), abs_gap(sw, w), order, name))
            order += 1
        quick_sort(people, 0, len(people) - 1)
        names = []
        i = 0
        while i < len(people):
            names.append(people[i][3])
            i += 1
        lines.append(" ".join(names))
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
