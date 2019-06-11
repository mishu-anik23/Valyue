import os
import csv


def stream_processor_template(source):
    for data in source:
        # do something here
        yield data


def csv_read_from_file(filepath):
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            yield row


def get_headers(source):
    for index, line in enumerate(source):
        if index == 2:
            return line


def row_generator(source, headers):
    # discard the first 5 lines
    for _ in range(5):
        next(source)
    # now the actual data rows:
    for row in source:
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
    infilepath = os.path.join(os.getcwd(), 'out_short.ascii')
    output_path = os.path.join(os.getcwd(), 'out_short.csv')
    headers = get_headers(source=csv_read_from_file(infilepath))
    rows = row_generator(source=csv_read_from_file(infilepath), headers=headers)
    csv_writer(output_path, headers, source=comma2decimal(rows))
