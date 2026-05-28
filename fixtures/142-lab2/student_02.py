import sys


def abs_gap(left, right):
    value = left - right
    if value < 0:
        value = -value
    return value


def take(left, right):
    merged = []
    a = 0
    b = 0
    while a < len(left) and b < len(right):
        current_left = left[a]
        current_right = right[b]
        if current_left[0] != current_right[0]:
            choose_left = current_left[0] < current_right[0]
        elif current_left[1] != current_right[1]:
            choose_left = current_left[1] < current_right[1]
        else:
            choose_left = current_left[2] <= current_right[2]
        if choose_left:
            merged.append(current_left)
            a += 1
        else:
            merged.append(current_right)
            b += 1
    while a < len(left):
        merged.append(left[a])
        a += 1
    while b < len(right):
        merged.append(right[b])
        b += 1
    return merged


def sort_block(items):
    if len(items) <= 1:
        return items
    middle = len(items) // 2
    left = sort_block(items[:middle])
    right = sort_block(items[middle:])
    return take(left, right)


def main():
    data = sys.stdin.buffer.read().split()
    if len(data) == 0:
        return
    place = 0
    case_count = int(data[place])
    place += 1
    result = []
    while case_count > 0:
        case_count -= 1
        sol_h = int(data[place])
        sol_w = int(data[place + 1])
        place += 2
        amount = int(data[place])
        place += 1
        rows = []
        order = 0
        while order < amount:
            name = data[place].decode()
            h = int(data[place + 1])
            w = int(data[place + 2])
            place += 3
            rows.append((abs_gap(sol_h, h), abs_gap(sol_w, w), order, name))
            order += 1
        rows = sort_block(rows)
        names = []
        index = 0
        while index < len(rows):
            names.append(rows[index][3])
            index += 1
        result.append(" ".join(names))
    sys.stdout.write("\n".join(result))


if __name__ == "__main__":
    main()
