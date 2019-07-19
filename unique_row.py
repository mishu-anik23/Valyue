import operator


def unique_rows(source, signal1, signal2=None):
    lst = []
    prev_row = next(source)
    prev_val = (prev_row[signal1.name], None)

    if signal2:
        prev_val = (prev_row[signal1.name], prev_row[signal2.name])

    lst.append(prev_row)

    for r in source:
        if r[signal1.name] != prev_val[0]:
            prev_val = (r[signal1.name], None)
            if signal2:
                if ((r[signal1.name] != prev_val[0] and r[signal2.name] != prev_val[1]) or
                        (r[signal1.name] == prev_val[0] and r[signal2.name] != prev_val[1]) or
                        (r[signal1.name] != prev_val[0] and r[signal2.name] == prev_val[1])):
                    prev_val = (r[signal1.name], r[signal2.name])
            lst.append(r)

    return lst


def drop_duplicates_1(source):
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


def compare_rows(row1, row2):
    for k1, v1 in row1.items():
        for k2, v2 in row2.items():
            if k1 or k2 == 'time':
                continue
        return True
    else:
        return False


def compare_x_values(value1, value2):
    if value1[0] == value2[0]:
        return True
    else:
        return False



class UniqueRows:
    def __init__(self, source, signal1):
        self.source = source
        self.signal1 = signal1
        self.prev_value = None
        self.storage = []
        self.store_unique_rows()

    def store_unique_rows(self):
        if self.prev_value is None:
            try:
                start_row = next(self.source)
                self.prev_value = start_row[self.signal1.name]
                self.storage.append(start_row)
            except StopIteration:
                return

        for row in self.source:
            if row[self.signal1.name]!= self.prev_value:
                self.prev_value = row[self.signal1.name]
                self.storage.append(row)

    def generate_unique_rows(self):
        for elem in self.storage:
            yield elem

