import sys


def delta(a, b):
    n = a - b
    if n < 0:
        return -n
    return n


def merge(left, right):
    combined = []
    i = 0
    j = 0
    while True:
        if i >= len(left) or j >= len(right):
            break
        l_item = left[i]
        r_item = right[j]
        if l_item[:3] <= r_item[:3]:
            combined.append(l_item)
            i += 1
        else:
            combined.append(r_item)
            j += 1
    while i < len(left):
        combined.append(left[i])
        i += 1
    while j < len(right):
        combined.append(right[j])
        j += 1
    return combined


def merge_sort(values):
    count = len(values)
    if count < 2:
        return values
    half = count // 2
    first = merge_sort(values[:half])
    second = merge_sort(values[half:])
    return merge(first, second)


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return
    cursor = 0
    cases = int(tokens[cursor])
    cursor += 1
    output = []
    while cases:
        cases -= 1
        sol_h = int(tokens[cursor])
        sol_w = int(tokens[cursor + 1])
        cursor += 2
        actors_count = int(tokens[cursor])
        cursor += 1
        people = []
        order = 0
        while order < actors_count:
            label = tokens[cursor].decode()
            height = int(tokens[cursor + 1])
            weight = int(tokens[cursor + 2])
            cursor += 3
            people.append((delta(sol_h, height), delta(sol_w, weight), order, label))
            order += 1
        ranked = merge_sort(people)
        names = []
        for item in ranked:
            names.append(item[3])
        output.append(" ".join(names))
    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
