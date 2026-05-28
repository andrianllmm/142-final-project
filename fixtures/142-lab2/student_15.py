import sys


def diff(a, b):
    value = a - b
    if value < 0:
        return -value
    return value


def before(left, right):
    if left[0] != right[0]:
        return left[0] < right[0]
    if left[1] != right[1]:
        return left[1] < right[1]
    return left[2] < right[2]


def insertion_sort(items):
    index = 1
    while index < len(items):
        item = items[index]
        spot = index - 1
        while spot >= 0 and before(item, items[spot]):
            items[spot + 1] = items[spot]
            spot -= 1
        items[spot + 1] = item
        index += 1
    return items


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    cur = 0
    t = int(data[cur])
    cur += 1
    result = []
    while t > 0:
        t -= 1
        sh = int(data[cur])
        sw = int(data[cur + 1])
        cur += 2
        total = int(data[cur])
        cur += 1
        people = []
        order = 0
        while order < total:
            name = data[cur].decode()
            h = int(data[cur + 1])
            w = int(data[cur + 2])
            cur += 3
            people.append((diff(sh, h), diff(sw, w), order, name))
            order += 1
        insertion_sort(people)
        names = []
        for person in people:
            names.append(person[3])
        result.append(" ".join(names))
    sys.stdout.write("\n".join(result))


if __name__ == "__main__":
    main()
