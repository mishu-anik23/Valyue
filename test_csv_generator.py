import io
from mockhw import *


def test_get_csv_dict_reader_from_file_obj():
    file_content = io.StringIO("""\
A;B;C
1;2;3
4;5;6
""")
    csv_it = csv.DictReader(file_content, delimiter=';')

    assert next(csv_it) == {'A': '1', 'B': '2', 'C': '3'}
    assert next(csv_it) == {'A': '4', 'B': '5', 'C': '6'}


def test_discard_rows_for_typ_512():
    file_content = io.StringIO("""\
Typ
0
512
23
""")
    csv_it = csv.DictReader(file_content, delimiter=';')
    csv_it_discarded_row = discard_rows(source=csv_it, criterion=type_is_512)

    assert next(csv_it_discarded_row) == {'Typ': '0'}
    assert next(csv_it_discarded_row) == {'Typ': '23'}


def test_discard_columns_simple_case():
    file_content = io.StringIO("""\
A;B
1;2
4;5
""")
    remove_list = ['B']
    csv_it = csv.DictReader(file_content, delimiter=';')
    csv_it_discarded_cols = discard_columns(source=csv_it, to_remove=remove_list)

    assert next(csv_it_discarded_cols) == {'A': '1'}
    assert next(csv_it_discarded_cols) == {'A': '4'}


def test_discard_columns_all():
    """Removing all cols return the empty mapping."""
    file_content = io.StringIO("""\
A;B
1;2
4;5
""")
    remove_list = ['A', 'B']
    csv_it = csv.DictReader(file_content, delimiter=';')
    csv_it_discarded_cols = discard_columns(source=csv_it, to_remove=remove_list)

    assert next(csv_it_discarded_cols) == {}
    assert next(csv_it_discarded_cols) == {}


def test_discard_columns_empty_remove_list():
    """For empty remove list func returns the existing cols and relavent row mapping."""
    file_content = io.StringIO("""\
A
1
4
""")
    remove_list = []
    csv_it = csv.DictReader(file_content, delimiter=';')
    csv_it_discarded_cols = discard_columns(source=csv_it, to_remove=remove_list)

    assert next(csv_it_discarded_cols) == {'A': '1'}
    assert next(csv_it_discarded_cols) == {'A': '4'}


def test_discard_columns_invalid_remove_list():
    """For invalid remove list func also returns the existing cols and relavent row mapping."""
    file_content = io.StringIO("""\
A
1
4
""")
    remove_list = ['C']
    csv_it = csv.DictReader(file_content, delimiter=';')
    csv_it_discarded_cols = discard_columns(source=csv_it, to_remove=remove_list)

    assert next(csv_it_discarded_cols) == {'A': '1'}
    assert next(csv_it_discarded_cols) == {'A': '4'}


def test_extract_nibbles():
    row_in = {'N0': '8', 'N1': '10', 'N2': '7', 'N3': '5', 'N4': '10', 'N5': '1',
              'N6': '1', 'CRC': '1', 'Rx Time': '122770661', 'Res': '0',  'Bus': '1',
              'Sync Time': '31495'}

    assert extract_nibbles(row_in) == [8, 10, 7, 5, 10, 1, 1, 1]


def test_convert2int():
    file_content = io.StringIO("""\
A;B;C;Time
1;2;3;0,234
4;5;6;0,1e-6
""")
    csv_it = csv.DictReader(file_content, delimiter=';')
    row_converted = convert2int(source=csv_it)

    assert next(row_converted) == {'A': 1, 'B': 2, 'C': 3}
    assert next(row_converted) == {'A': 4, 'B': 5, 'C': 6}

