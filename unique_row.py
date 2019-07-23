import operator


def basic_stream_signature(source):
    for elem in source:
        yield elem


def drop_duplicates(source, predicate=operator.__eq__):
    prev = None
    for elem in source:
        if prev is not None:
            if predicate(elem, prev):
                continue
        prev = elem
        yield elem


def isequal_1(row1, row2):
    row_no_time1 = {k: v for k, v in row1.items() if k != 'time'}
    row_no_time2 = {k: v for k, v in row2.items() if k != 'time'}
    return row_no_time1 == row_no_time2


def isequal(row1, row2):
    # if row1:
    #     return False
    # if row2:
    #     return False
    for k in row1:
        print(k)
        if row1[k] == row2[k]:
            return True
    return True

def compare_values(value1, value2):
    return value1[0] == value2[0]
