import csv
from signaldef import *


def csv_read_from_file(filepath):
    with open(filepath) as csvfile:
        for row in get_csv_dict_reader(csvfile):
            yield row


def get_csv_dict_reader(csvfile):
    csv_it = csv.DictReader(csvfile, delimiter=';')
    return csv_it


def discard_rows(source, criterion):
    for row in source:
        if criterion(row):
            continue
        yield row


def discard_columns(source, to_remove):
    for row in source:
        yield {k: v for k, v in row.items() if k not in to_remove}


def type_is_512(row):
    if row['Typ'] == '512':
        return True
    return False


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


if __name__ == '__main__':
    in_file_pth = os.path.join(os.getcwd(), 'data/SENT_Trace_MUX_2016-11-14.csv')
    to_remove = ['Typ', 'Stat/Err', 'Skipped']
    csv_it = csv_read_from_file(in_file_pth)
    print(next(csv_it))
    print(next(csv_it))
    print(next(csv_it))
    print(next(csv_it))
    rows_d = discard_rows(source=csv_read_from_file(in_file_pth), criterion=type_is_512)
    rows_dc = discard_columns(rows_d, to_remove)
    # print(next(rows_dc))
    # print(next(rows_dc))












