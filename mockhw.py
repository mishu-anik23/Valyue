import csv
from signaldef import *


def csv_iterator(filename):
    filepath = os.path.join(os.getcwd(), 'data')
    with open(os.path.join(filepath, filename)) as csvfile:
        csv_it = csv.DictReader(csvfile, delimiter=';')
        #next(csv_it)
        for value in csv_it:
            #yield value
            yield process_row(value)


def process_row(columns):
    to_remove = ['Typ', 'Stat/Err', 'Skipped']
    for i in to_remove:
        del columns[i]
    return columns


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
    it_obj = csv_iterator('SENT_Trace_MUX_2016-11-14.csv')
    print(next(it_obj))
    print(next(it_obj))



