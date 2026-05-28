import sys


def absolute_gap(a, b):
    value = a - b
    if value < 0:
        return -value
    return value


def selection_sort(items):
    n = len(items)
    index = 0
    while index < n:
        best_key = items[index][:3]
        best_index = index
        probe = index + 1
        while probe < n:
            probe_key = items[probe][:3]
            if probe_key < best_key:
                best_key = probe_key
                best_index = probe
            probe += 1
        if best_index != index:
            swap = items[best_index]
            while best_index > index:
                items[best_index] = items[best_index - 1]
                best_index -= 1
            items[index] = swap
        index += 1
    return items


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    pos = 0
    tests = int(tokens[pos])
    pos += 1
    answer = []
    while tests:
        tests -= 1
        sh = int(tokens[pos])
        sw = int(tokens[pos + 1])
        pos += 2
        total = int(tokens[pos])
        pos += 1
        records = []
        rank = 0
        while rank < total:
            name = tokens[pos].decode()
            h = int(tokens[pos + 1])
            w = int(tokens[pos + 2])
            pos += 3
            records.append((absolute_gap(sh, h), absolute_gap(sw, w), rank, name))
            rank += 1
        selection_sort(records)
        names = []
        i = 0
        while i < len(records):
            names.append(records[i][3])
            i += 1
        answer.append(" ".join(names))
    sys.stdout.write("\n".join(answer))


if __name__ == "__main__":
    main()
