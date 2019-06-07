import csv
from signaldef import *


def csv_reader(filename):
    filepath = os.path.join(os.getcwd(), 'data')
    with open(os.path.join(filepath, filename)) as csvfile:
        csv_it = csv.DictReader(csvfile, delimiter=';')
        to_remove = ['Typ', 'Stat/Err', 'Skipped']
        for value in csv_it:
            discard_row = discard_type_512(value)
            if discard_row:
                continue
            yield discard_columns(value, to_remove)


def csv_read(filepath):
    with open(filepath) as csvfile:
        csv_it = csv.DictReader(csvfile, delimiter=';')
        for value in csv_it:
            yield value


def discard_columns(row, to_remove):
    return {k: v for k, v in row.items() if k not in to_remove}




def generate_rows(source, to_remove):
    for row in source:
        if discard_type_512(row):
            continue
        yield discard_columns(row, to_remove)


def discard_type_512(source):
    if source['Typ'] == '512':
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
    # it_obj = csv_reader('SENT_Trace_MUX_2016-11-14.csv')
    # print(next(it_obj))
     #print(next(it_obj))
    #print(next(it_obj))
    #print(next(it_obj))
    #print(next(it_obj))
    #print(next(it_obj))
    in_file_pth = os.path.join(os.getcwd(), 'data/SENT_Trace_MUX_2016-11-14.csv')
    src_gens = csv_read(in_file_pth)
    to_remove = ['Typ', 'Stat/Err', 'Skipped']
    rows = generate_rows(src_gens, to_remove)
    print(next(rows))
    print(next(rows))
    print(next(rows))
    print(next(rows))
    print(next(rows))
    print(next(rows))







