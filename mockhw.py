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

    def calc_rx_time_diff(self):
        rx_time1 = next(self.source)['Rx Time']
        rx_time2 = next(self.source)['Rx Time']
        return rx_time2 - rx_time1






if __name__ == '__main__':
    in_file_pth = os.path.join(os.getcwd(), 'data/SENT_Trace_MUX_2016-11-14.csv')
    to_remove = ['Stat/Err', 'Skipped']
    csv_it = csv_read_from_file(in_file_pth)
    rows_d = discard_rows(source=csv_read_from_file(in_file_pth), criterion=type_is_512)
    rows_dc = discard_columns(rows_d, to_remove)
    print(next(rows_dc))
    # print(next(rows_dc))
    file_content = io.StringIO("""\
Bus;Typ;Rx Time;Sync Time;N0;N1;N2;N3;N4;N5;N6;CRC
1;2;3;44;0;1;2;3;14;2;4;1
4;5;6;66;1;11;3;14;2;4;3;0
""")
    csv_dct = csv.DictReader(file_content, delimiter=';')
    hw_obj = MockHw(source=convert2int(rows_dc))
    vals = hw_obj.get_value_from_row()
    vals1 = hw_obj.get_value_from_row()
    tdiff = hw_obj.calc_rx_time_diff()
    #print(tdiff)
    print(vals)
    print(vals1)
    print(tdiff)
    print(hw_obj.calc_rx_time_diff())
    print(hw_obj.calc_rx_time_diff())
    print(hw_obj.calc_rx_time_diff())
    print(hw_obj.calc_rx_time_diff())
    print(hw_obj.calc_rx_time_diff())
    print(hw_obj.calc_rx_time_diff())











