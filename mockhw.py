import csv
from signaldef import *
from encode_decode import *


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


def convert_nibble(physical):
    def conversion(phy_value):
        raw_value = physical.phy2raw(phy_value)
        nibbles = encode(raw_value, physical.bitwidth)
        return nibbles
    return conversion

# Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16)

if __name__ == '__main__':
    csv_it = csv_iterator('mockhw_data.csv')

    conv_func = convert_nibble(Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16))
    print(make_data(next(csv_it), conversion=conv_func))
    print(make_data(next(csv_it), conversion=conv_func))
    print(make_data(next(csv_it), conversion=conv_func))
    print(make_data(next(csv_it), conversion=conv_func))
    print(make_data(next(csv_it), conversion=conv_func))
    print(next(csv_it)[0])

    print(next(csv_it)[1])
    print(next(csv_it))
    print(next(csv_it))


