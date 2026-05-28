import sys


def absdiff(a, b):
    value = a - b
    if value < 0:
        return -value
    return value


def partition(items, lo, hi):
    pivot = items[(lo + hi) // 2][:3]
    i = lo
    j = hi
    while i <= j:
        while items[i][:3] < pivot:
            i += 1
        while items[j][:3] > pivot:
            j -= 1
        if i <= j:
            items[i], items[j] = items[j], items[i]
            i += 1
            j -= 1
    return i, j


def quick_sort(items):
    if len(items) < 2:
        return items
    stack = [(0, len(items) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        left, right = partition(items, lo, hi)
        if lo < right:
            stack.append((lo, right))
        if left < hi:
            stack.append((left, hi))
    return items


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    p = 0
    tests = int(data[p])
    p += 1
    answer = []
    while tests > 0:
        tests -= 1
        sh = int(data[p])
        sw = int(data[p + 1])
        p += 2
        amount = int(data[p])
        p += 1
        actors = []
        rank = 0
        while rank < amount:
            name = data[p].decode()
            h = int(data[p + 1])
            w = int(data[p + 2])
            p += 3
            actors.append((absdiff(sh, h), absdiff(sw, w), rank, name))
            rank += 1
        quick_sort(actors)
        names = []
        for actor in actors:
            names.append(actor[3])
        answer.append(" ".join(names))
    sys.stdout.write("\n".join(answer))


if __name__ == "__main__":
    main()
