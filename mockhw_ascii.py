import csv

from signaldef import *
from dataframe import DataFrame


ascii2sent_headers = {
    'temp_rag_tank_sens': 'Temperature',
    'rtl_mes_sens[0]': 'Level signal 2 - Combi-sensor',
    'conc_rag_sens': 'Concentration',
    'vel_rag_ucls_sent': 'Speed',
    'vcc_rag_ucls': 'Supply Voltage',
    'rt_rag_ucls[0]': 'Runtime 1',
    'rt_rag_ucls[1]': 'Runtime 2',
    'rt_rag_ucls[2]': 'Runtime 3',
    'rt_rag_ucls[3]': 'Runtime 4',
    'ampl_rag_ucls_sent[0]': 'Amplitude 1',
    'ampl_rag_ucls_sent[1]': 'Amplitude 2',
    'ampl_rag_ucls_sent[2]': 'Amplitude 3',
    'ampl_rag_ucls_sent[3]': 'Amplitude 4',
    'qly_rag_ucls[0]': 'Quality 1',
    'qly_rag_ucls[1]': 'Quality 2',
    'qly_rag_ucls[2]': 'Quality 3',
    'qly_rag_ucls[3]': 'Quality 4',
    'rtl_mes_sens[1]': 'Level signal 1 - Direct-sensor',
}


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


def translate_headers(headers, mapping):
    lst = []
    for header in headers:
        if header in mapping:
            replc_str = mapping[header]
        else:
            replc_str = header
        lst.append(replc_str)
    return lst


def row_generator(source, headers):
    # discard the first 5 lines
    for _ in range(5):
        next(source)
    # now the actual data rows:
    for row in source:
        yield dict(zip(headers, row))


def signal_row_generator_1(source, signal1, signal2=None):
    headings = ['time', signal1.name]
    if signal2:
        headings = ['time', signal1.name, signal2.name]
    for row in source:
        yield {k: v for k, v in row.items() if k in headings}


def signal_row_generator(source, signal1, signal2=None):
    headings = ['time', signal1.name]
    if signal2:
        headings = ['time', signal1.name, signal2.name]
    for row in source:
        yield {heading: row[heading] for heading in headings}


def signal_frame_generator(source, signal1, signal2=None):
    for row in source:
        ts = scale_sent_timestamp(row['time'])
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
        yield make_sent_row(ts, frame)


def scale_sent_timestamp(time):
    return int(float(time) / 2.56e-6)


def make_sent_row(ts, frame):
    rowdct_sent = insert_nibbles(frame)
    rowdct_sent['Bus'] = 0
    rowdct_sent['Typ'] = 0
    rowdct_sent['Sync Time'] = 0
    rowdct_sent['Rx Time'] = ts

    return rowdct_sent


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

    sig_in_1st = SignalDefinition(name="Supply Voltage", minimum='0', maximum='40.75', unit='V',
                                  physical=spec_conti(minimum=0, maximum=40.75,
                                                      resolution=0.16, bitwidth=8, errorcodes={}, offset=0),
                                  encoding=SignalEncoding(bitwidth=8, msn=1, lsn=2),
                                  default=5.671875)

    sig_in_2nd = SignalDefinition(name="Concentration", minimum='-10', maximum='100', unit='%',
                                  physical=spec_conti(minimum=-10, maximum=100,
                                                      resolution=0.01, bitwidth=16, errorcodes={}, offset=-10),
                                  encoding=SignalEncoding(bitwidth=16, msn=6, lsn=3),
                                  default=25.46)

    print(headers)

    sent_headers = translate_headers(headers, mapping=ascii2sent_headers)
    print(sent_headers)
    #print(len(headers))

    rows = row_generator(source=csv_read_from_file(infilepath), headers=sent_headers)
    #print(len(next(rows)))
    sigrows = signal_row_generator(source=comma2decimal(rows), signal1=sig_in_2nd)#, signal2=sig_in_2nd)
    #print(next(sigrows))

    sigframe = signal_frame_generator(source=sigrows, signal1=sig_in_1st, signal2=sig_in_2nd)
    #print(next(sigframe))

    sent_rows = sent_csv_adapter(source=sigframe)
    #print(next(sent_rows))

    mhw = MockHw(source=sent_rows)
    #print(mhw.get_value_from_row())
    #csv_writer(output_path, headers, source=comma2decimal(rows))