import io
from ascii2csv import *


def test_get_headers_from_file_obj_1():
    """Takes 3rd line as headers."""
    file_content = io.StringIO("""\
A\tB
C\tD
E\tF
G\tH
""")
    csv_reader = csv.reader(file_content, delimiter='\t')

    assert get_headers(source=csv_reader) == ['E', 'F']


def test_get_headers_from_file_obj_2():
    """Takes 3rd line as headers."""
    file_content = io.StringIO("""\
A\tB
C\tD
time\tChannel
E\tF
""")
    csv_reader = csv.reader(file_content, delimiter='\t')

    assert get_headers(source=csv_reader) == ['time', 'Channel']


def test_row_generator_file_obj():
    file_content = io.StringIO("""\
blah\tblah
Whatever\tis
will be\tskipped
until\tline 5
Data start\tfrom line 6
1\t2
0,01\t5,09
anything\tanything
""")
    headers_in = ['A', 'B']
    csv_reader = csv.reader(file_content, delimiter='\t')
    csv_rows = row_generator(source=csv_reader, headers=headers_in)

    assert next(csv_rows) == {'A': '1', 'B': '2'}
    assert next(csv_rows) == {'A': '0,01', 'B': '5,09'}
    assert next(csv_rows) == {'A': 'anything', 'B': 'anything'}


def test_comma2decimal():
    rows_in = [{'A': '0,01', 'B': '5,09'}, {'A': '0,004', 'B': '9,098'}]
    modified_row = comma2decimal(rows_in)

    assert next(modified_row) == {'A': '0.01', 'B': '5.09'}
    assert next(modified_row) == {'A': '0.004', 'B': '9.098'}