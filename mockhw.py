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


def process_ascii_file(filename):
    with open(os.path.join(os.getcwd(), filename)) as fd:
        lines = fd.readlines()
        header = lines.pop(2).rstrip('\n').split('\t')
        data = (elm.rstrip('\n').split('\t') for elm in lines[4:])
        return header, data


def csv_row_generator(header, data):
    coldict = {}
    for value in data:
        coldict[header[0]] = value[0]
        coldict[header[1]] = value[1]
        yield coldict


def csv_writer(filename, header, data):
    with open(os.path.join(os.getcwd(), filename), 'w', newline='') as fd:
        writer = csv.DictWriter(fd, fieldnames=header)
        writer.writeheader()
        for row in data:
            rowdict = {}
            rowdict[header[0]] = row[0].replace(',', '.')
            rowdict[header[1]] = row[1].replace(',', '.')
            writer.writerow(rowdict)




if __name__ == '__main__':
    it_obj = csv_iterator('SENT_Trace_MUX_2016-11-14.csv')
    #print(next(it_obj))
    #print(next(it_obj))
    print(process_ascii_file('out_short.ascii'))
    header, data = process_ascii_file('out_short.ascii')
    csv_writer('out_short.csv', header, data)

    #print(next(csv_row_generator(header, data)))




