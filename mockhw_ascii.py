def get_headers(source):
    for index, line in enumerate(source):
        if index == 2:
            return line


def row_generator(source, headers):
    # discard the first 5 lines
    for _ in range(5):
        next(source)
    # now the actual data rows:
    for row in source:
        yield dict(zip(headers, row))


def comma2decimal(source):
    for data in source:
        data = {key: val.replace(',', '.') for key, val in data.items()}
        yield data


def extract_nibbles(row, signal):
    phy_val = row['Channel 1']
    nibbles = signal.encode_frame(phy_val)
    return nibbles


class MockHw:
    def __init__(self, source, signal):
        self.source = source
        self.signal = signal

    def get_value_from_row(self):
        rowdict = next(self.source)
        data = extract_nibbles(rowdict, self.signal)
        ts = rowdict['time']
        return ts, data