#result[j-2] = input[j] + input[j-1] if (input[j-2]==0)
#result[j-2] = input[j-2]*( input[j] + input[j-1])

def generate_sequence(source):
    list = []
    j_1 = None
    j_2 = None
    for idx, elm in enumerate(source):
        j = idx
        if idx > 0:
            j_1 = idx - 1
            j_2 = idx - 2

        if j_1:
            if source[j_2] == 0:
                list.append(source[j] + source[j_1])
            else:
                list.append(source[j_2] * (source[j] + source[j_1]))
    print(list)
    return list


def consecutive_diffs(in_list):
    out_list = []
    prev_idx = None
    for idx, elm in enumerate(in_list):
        next_idx = idx
        if idx > 0:
            prev_idx = idx - 1

        if prev_idx is not None:
            out_list.append(in_list[next_idx] - in_list[prev_idx])
        #else:
         #   out_list.append(in_list[next_idx] - in_list[0])
    print(out_list)
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
        if previous_number is None:
            previous_number = number

        diff = number - previous_number
        previous_number = number
        yield diff


def generate_consecutive_sum(number_list):
    previous_number = 0
    for number in number_list:
        sum = previous_number + number
        previous_number = sum
        yield sum


def consecutive_sum_pairs(number_list):
    return [self_elem + next_elem for self_elem, next_elem in zip(number_list[::2], number_list[1::2])]