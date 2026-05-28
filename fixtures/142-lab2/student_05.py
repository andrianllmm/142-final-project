import sys


def absolute_gap(x, y):
    gap = x - y
    if gap < 0:
        gap = -gap
    return gap


def merge(left, right):
    result = []
    left_index = 0
    right_index = 0
    left_len = len(left)
    right_len = len(right)
    while left_index < left_len and right_index < right_len:
        if left[left_index][0] < right[right_index][0]:
            result.append(left[left_index])
            left_index += 1
        elif left[left_index][0] > right[right_index][0]:
            result.append(right[right_index])
            right_index += 1
        elif left[left_index][1] < right[right_index][1]:
            result.append(left[left_index])
            left_index += 1
        elif left[left_index][1] > right[right_index][1]:
            result.append(right[right_index])
            right_index += 1
        else:
            if left[left_index][2] < right[right_index][2]:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1
    while left_index < left_len:
        result.append(left[left_index])
        left_index += 1
    while right_index < right_len:
        result.append(right[right_index])
        right_index += 1
    return result


def sort_items(items):
    if len(items) <= 1:
        return items
    middle = len(items) // 2
    first_half = sort_items(items[:middle])
    second_half = sort_items(items[middle:])
    return merge(first_half, second_half)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    test_count = int(data[idx])
    idx += 1
    lines = []
    while test_count > 0:
        test_count -= 1
        sol_h = int(data[idx])
        sol_w = int(data[idx + 1])
        idx += 2
        actor_total = int(data[idx])
        idx += 1
        payload = []
        rank = 0
        while rank < actor_total:
            person = data[idx].decode()
            height = int(data[idx + 1])
            weight = int(data[idx + 2])
            idx += 3
            payload.append(
                (absolute_gap(sol_h, height), absolute_gap(sol_w, weight), rank, person)
            )
            rank += 1
        sorted_payload = sort_items(payload)
        names = []
        pos = 0
        while pos < len(sorted_payload):
            names.append(sorted_payload[pos][3])
            pos += 1
        lines.append(" ".join(names))
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
