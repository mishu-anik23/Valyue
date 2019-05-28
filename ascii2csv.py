import os
import csv


def get_headers(filepath):
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for index, line in enumerate(reader):
            if index == 2:
                return line


def row_generator(filepath, headers):
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        # discard the first 5 lines
        for _ in range(5):
            next(reader)
        # now the actual data rows:
        for row in reader:
            yield dict(zip(headers, row))


def comma2decimal(source):
    for data in source:
        data = {key: val.replace(',', '.') for key, val in data.items()}
        yield data


def csv_writer(filepath, headers, source):
    with open(filepath, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for row in source:
            writer.writerow(row)


if __name__ == '__main__':
    filepath = os.path.join(os.getcwd(), 'out_short.ascii')
    output_path = os.path.join(os.getcwd(), 'out_short.csv')
    headers = get_headers(filepath)
    rows = row_generator('out_short.ascii', headers)
    csv_writer(output_path, headers, source=comma2decimal(rows))
