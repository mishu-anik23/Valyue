import io
import csv
from signaldef import *


def csv_read_from_file(filepath):
    with open(filepath) as csvfile:
        csv_it = csv.DictReader(csvfile, delimiter=';')
        for row in csv_it:
            yield row


def discard_rows(source, criterion):
    for row in source:
        if criterion(row):
            continue
        yield row


def discard_columns(source, to_remove):
    for row in source:
        yield {k: v for k, v in row.items() if k not in to_remove}


def convert2int(source):
    for row in source:
        yield {k: int(v) for k, v in row.items() if k != 'Time'}


def type_is_512(row):
    if row['Typ'] == '512':
        return True
    return False


def extract_nibbles(row):
    nibbles = ['N0', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'CRC']
    return [int(row[nibble]) for nibble in nibbles]


def make_data(row, conversion):
    timestamp = int(row[0])
    phy_value = float(row[1])
    nibbles = conversion(phy_value)
    return timestamp, nibbles


def create_conversion(signal):
    def conversion(phy_value):
        raw_value = signal.physical.phy2raw(phy_value)
        nibbles = signal.encoding.encode(raw_value)
        return nibbles
    return conversion


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

    def get_time_and_data(self, row):
        rx_time = row['Rx Time']
        data = extract_nibbles(row)
        return rx_time, data






if __name__ == '__main__':
    in_file_pth = os.path.join(os.getcwd(), 'data/SENT_Trace_MUX_2016-11-14.csv')
    to_remove = ['Stat/Err', 'Skipped']
    csv_it = csv_read_from_file(in_file_pth)
    rows_d = discard_rows(source=csv_read_from_file(in_file_pth), criterion=type_is_512)
    rows_dc = discard_columns(rows_d, to_remove)
    #print(next(rows_dc))
    # print(next(rows_dc))
    file_content = io.StringIO("""\
Time;Bus;Typ;N0;N1;N2;N3;N4;N5;N6;CRC;Rx Time;Sync Time
2,47e-6;1;0;8;10;7;5;10;1;1;1;122770661;31495
0,01456917;1;0;8;11;7;4;15;4;15;9;122777518;31496
0,02996182;1;0;0;12;7;4;15;5;0;12;12;31496
""")
    csv_dct = csv.DictReader(file_content, delimiter=';')
    mock_src = convert2int(csv_dct)

    hw_obj = MockHw(source=mock_src)
    # vals = hw_obj.get_value_from_row()
    # vals1 = hw_obj.get_value_from_row()
    # print(vals)
    # print(vals1[3:5])
    for row in mock_src:
        print(hw_obj.get_time_and_data(row))









