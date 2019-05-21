import csv
from signaldef import *


def csv_iterator(filename):
    filepath = os.path.join(os.getcwd(), 'data')
    with open(os.path.join(filepath, filename)) as csvfile:
        csv_it = csv.reader(csvfile, delimiter=';')
        for ts, value in csv_it:
            yield (ts, value)


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



