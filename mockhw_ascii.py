import csv

from signaldef import *
from dataframe import DataFrame

def csv_read_from_file(filepath):
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            yield row


def get_headers(source):
    for index, line in enumerate(source):
        if index == 2:
            #return line
            return [elem.rstrip('\\XCP:1') for elem in line]


def row_generator(source, headers):
    # discard the first 5 lines
    for _ in range(5):
        next(source)
    # now the actual data rows:
    for row in source:
        yield dict(zip(headers, row))


def signal_row_generator(source, signal1, signal2=None):
    headings = ['time', signal1.name]
    if signal2:
        headings = ['time', signal1.name, signal2.name]
    for row in source:
        yield {k: v for k, v in row.items() if k in headings}


def signal_frame_generator(source, signal1, signal2=None):
    for row in source:
        ts = row['time']
        phy1 = intorfloat(row[signal1.name])
        raw1 = signal1.physical.phy2raw(phy1)
        df = DataFrame(encoding1=signal1.encoding)
        nibbles = df.encode_frame(raw1)

        if signal2:
            phy2 = intorfloat(row[signal2.name])
            raw2 = signal2.physical.phy2raw(phy2)
            df = DataFrame(encoding1=signal1.encoding, encoding2=signal2.encoding)
            nibbles = df.encode_frame(raw1, raw2)

        yield ts, nibbles


def sent_csv_adapter(source):
    for ts, frame in source:
        rowdct_sent = {}
        rowdct_sent['Bus'] = 0.0
        rowdct_sent['Typ'] = 0.0
        rowdct_sent['Sync Time'] = 0.0
        rowdct_sent['Rx Time'] = float(ts)
        rowdct_sent.update(insert_nibbles(frame))

        yield rowdct_sent


def comma2decimal(source):
    for data in source:
        data = {key: val.replace(',', '.') for key, val in data.items()}
        yield data


def insert_nibbles(frame):
    nibbles = ['N0', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'CRC']
    return dict(zip(nibbles, frame))



def extract_nibbles(row):
    nibbles = ['N0', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'CRC']
    return [int(row[nibble]) for nibble in nibbles]



class MockHw:
    def __init__(self, source):
        self.source = source

    def get_value_from_row(self):
        rowdict = next(self.source)
        rx_bus_id = rowdict['Bus']
        typ = rowdict['Typ']
        data = extract_nibbles(rowdict)
        rx_time = rowdict['Rx Time']
        sync = rowdict['Sync Time']
        return rx_bus_id, typ, 0, data, rx_time, sync


if __name__ == '__main__':
    infilepath = os.path.join(os.getcwd(), 'data', '20161017_Test_Tool_MS0660X3i_02_10.ascii')
    output_path = os.path.join(os.getcwd(), 'out_short.csv')
    headers = get_headers(source=csv_read_from_file(infilepath))

    sig_in_1st = SignalDefinition(name="prs_rag", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                                  default=-21.671875)

    sig_in_2nd = SignalDefinition(name="prs_ctl_dif_rag_fil", minimum='-40', maximum='165', unit='C',
                                  physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16),
                                  encoding=SignalEncoding(bitwidth=16, msn=6, lsn=3),
                                  default=25.46)

    print(headers)
    print(len(headers))

    rows = row_generator(source=csv_read_from_file(infilepath), headers=headers)
    print(len(next(rows)))
    sigrows = signal_row_generator(source=comma2decimal(rows), signal1=sig_in_1st, signal2=sig_in_2nd)
    print(next(sigrows))

    sigframe = signal_frame_generator(source=sigrows, signal1=sig_in_1st, signal2=sig_in_2nd)
    print(next(sigframe))

    sent_rows = sent_csv_adapter(source=sigframe)
    print(next(sent_rows))

    mhw = MockHw(source=sent_rows)
    print(mhw.get_value_from_row())
    #csv_writer(output_path, headers, source=comma2decimal(rows))