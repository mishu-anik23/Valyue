#result[j-2] = input[j] + input[j-1] if (input[j-2]==0)
#result[j-2] = input[j-2]*( input[j] + input[j-1])


def mult_add_sequences(source):
    out_list = []
    j_1 = None
    j_2 = None
    for idx, elm in enumerate(source):
        j = idx
        if idx > 0:
            j_1 = idx - 1
            j_2 = idx - 2

        if j_1:
            if source[j_2] == 0:
                out_list.append(source[j] + source[j_1])
            else:
                out_list.append(source[j_2] * (source[j] + source[j_1]))
    return out_list


def generate_mult_add_sequences(source):
    prev = None
    prev_prev = None
    for elm in source:
        if prev_prev is None:
            if prev is None:
                prev = elm
            prev_prev = prev
        if prev_prev != prev:
            if prev_prev == 0:
                print("elm", elm)
                print("prev", prev)
                print("prev_prev", prev_prev)
                yield elm + prev
            else:
                print("elm", elm)
                print("prev", prev)
                print("prev_prev", prev_prev)
                yield prev_prev * (elm + prev)
            prev_prev = prev

        prev = elm









def consecutive_diffs(in_list):
    out_list = []
    prev_idx = None
    if len(in_list) <= 1:
        raise ValueError("At least need two elements to calculate consecutive diffs.")
    for idx, elm in enumerate(in_list):
        next_idx = idx
        if idx > 0:
            prev_idx = idx - 1

        if prev_idx is not None:
            out_list.append(in_list[next_idx] - in_list[prev_idx])
    return out_list


def consecutive_sums(in_list):
    out_list = []
    prev_idx = None
    for idx, elm in enumerate(in_list):
        next_idx = idx
        if idx > 0:
            prev_idx = idx - 1
        if prev_idx is not None:
            out_list.append(in_list[next_idx] + in_list[prev_idx])
    return out_list


def generate_consecutive_diff(source):
    previous_number = None
    for number in source:
        if previous_number is not None:
            diff = number - previous_number
            yield diff
        previous_number = number


def generate_cumulative_sum_1(number_list):
    previous_number = 0
    for number in number_list:
        sum = previous_number + number
        previous_number = sum
        yield sum


def generate_cumulative_sum(number_list):
    previous_num = None
    for number in number_list:
        if previous_num is None:
            previous_num = number
            sum = previous_num
        else:
            sum = previous_num + number
        previous_num = sum
        yield sum


def cumulative_sums(source):
    out_list = []
    previous_num = None
    for elm in source:
        if previous_num is None:
            previous_num = elm
            sum = previous_num
        else:
            sum = previous_num + elm
        out_list.append(sum)
        previous_num = sum
    return out_list


def current_largest_sequences(source):
    out_list = []
    previous_num = None
    for elm in source:
        if previous_num is None:
            previous_num = elm
        largest = max(elm, previous_num)
        out_list.append((previous_num, largest))
        previous_num = elm
    return out_list


def generate_current_and_largest_sequences(source):
    previous_num = None
    for elm in source:
        if previous_num is None:
            previous_num = elm
        largest = max(elm, previous_num)
        yield (previous_num, largest)
        previous_num = elm


def consecutive_sum_pairs(number_list):
    return [self_elem + next_elem for self_elem, next_elem in zip(number_list[::2], number_list[1::2])]