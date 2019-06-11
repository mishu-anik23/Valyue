import io
from ascii2csv import *


def test_get_csv_reader_from_file_obj():
    file_content = io.StringIO("""\
A\tB
C\tD
""")
    assert next(get_csv_reader(file_content)) == ['A', 'B']
    assert next(get_csv_reader(file_content)) == ['C', 'D']


def test_get_headers_from_file_obj_1():
    file_content = io.StringIO("""\
A\tB
C\tD
E\tF
G\tH
""")
    assert get_headers(source=get_csv_reader(file_content)) == ['E', 'F']


def test_get_headers_from_file_obj_2():
    file_content = io.StringIO("""\
A\tB
C\tD
time\tChannel
E\tF
""")
    src = get_csv_reader(file_content)
    assert get_headers(source=src) == ['time', 'Channel']


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
    src = get_csv_reader(file_content)

    assert next(row_generator(source=src, headers=headers_in)) == {'A': '1', 'B': '2'}
    assert next(row_generator(source=src, headers=headers_in)) == {'A': '0,01', 'B': '5,09'}
    assert next(row_generator(source=src, headers=headers_in)) == {'A': 'anything', 'B': 'anything'}