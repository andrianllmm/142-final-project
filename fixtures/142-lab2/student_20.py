import sys


def distance(a, b):
    result = a - b
    if result < 0:
        return -result
    return result


def selection_sort(data):
    i = 0
    n = len(data)
    while i < n:
        best = i
        best_key = data[i][:3]
        j = i + 1
        while j < n:
            if data[j][:3] < best_key:
                best = j
                best_key = data[j][:3]
            j += 1
        if best != i:
            data[i], data[best] = data[best], data[i]
        i += 1
    return data


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    idx = 0
    cases = int(tokens[idx])
    idx += 1
    lines = []
    while cases > 0:
        cases -= 1
        sh = int(tokens[idx])
        sw = int(tokens[idx + 1])
        idx += 2
        total = int(tokens[idx])
        idx += 1
        rows = []
        order = 0
        while order < total:
            nm = tokens[idx].decode()
            h = int(tokens[idx + 1])
            w = int(tokens[idx + 2])
            idx += 3
            rows.append((distance(sh, h), distance(sw, w), order, nm))
            order += 1
        selection_sort(rows)
        names = []
        pos = 0
        while pos < len(rows):
            names.append(rows[pos][3])
            pos += 1
        lines.append(" ".join(names))
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
