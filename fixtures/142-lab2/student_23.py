import sys


def gap(a, b):
    d = a - b
    if d < 0:
        return -d
    return d


def selection_sort(rows):
    for i in range(len(rows)):
        best = i
        best_key = rows[i][:3]
        for j in range(i + 1, len(rows)):
            current_key = rows[j][:3]
            if current_key < best_key:
                best = j
                best_key = current_key
        if best != i:
            rows[i], rows[best] = rows[best], rows[i]
    return rows


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    tests = int(data[idx])
    idx += 1
    output = []
    while tests > 0:
        tests -= 1
        sh = int(data[idx])
        sw = int(data[idx + 1])
        idx += 2
        count = int(data[idx])
        idx += 1
        people = []
        audition = 0
        while audition < count:
            name = data[idx].decode()
            h = int(data[idx + 1])
            w = int(data[idx + 2])
            idx += 3
            people.append((gap(sh, h), gap(sw, w), audition, name))
            audition += 1
        selection_sort(people)
        names = []
        for person in people:
            names.append(person[3])
        output.append(" ".join(names))
    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
