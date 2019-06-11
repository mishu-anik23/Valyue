import io
from mockhw import *


def test_get_csv_dict_reader_from_file_obj():
    csv_in = io.StringIO("""\
A;B;C
1;2;3
4;5;6
""")
    csv_it = get_csv_dict_reader(csv_in)

    assert next(csv_it) == {'A': '1', 'B': '2', 'C': '3'}
    assert next(csv_it) == {'A': '4', 'B': '5', 'C': '6'}


def test_discard_rows_for_typ_512():
    csv_in = io.StringIO("""\
Typ
0
512
23
""")
    csv_it_discarded_row = discard_rows(source=get_csv_dict_reader(csv_in), criterion=type_is_512)

    assert next(csv_it_discarded_row) == {'Typ': '0'}
    assert next(csv_it_discarded_row) == {'Typ': '23'}


def test_discard_columns_simple_case():
        csv_in = io.StringIO("""\
A;B
1;2
4;5
""")
        remove_list = ['B']
        csv_it_discarded_cols = discard_columns(source=get_csv_dict_reader(csv_in), to_remove=remove_list)

        assert next(csv_it_discarded_cols) == {'A': '1'}
        assert next(csv_it_discarded_cols) == {'A': '4'}


def test_discard_columns_all():
    csv_in = io.StringIO("""\
A;B
1;2
4;5
""")
    remove_list = ['A', 'B']
    csv_it_discarded_cols = discard_columns(source=get_csv_dict_reader(csv_in), to_remove=remove_list)

    assert next(csv_it_discarded_cols) == {}
    assert next(csv_it_discarded_cols) == {}


def test_discard_columns_empty_remove_list():
    csv_in = io.StringIO("""\
A
1
4
""")
    remove_list = []
    csv_it_discarded_cols = discard_columns(source=get_csv_dict_reader(csv_in), to_remove=remove_list)

    assert next(csv_it_discarded_cols) == {'A': '1'}
    assert next(csv_it_discarded_cols) == {'A': '4'}


def test_discard_columns_invalid_remove_list():
    """"""
    csv_in = io.StringIO("""\
A
1
4
""")
    remove_list = ['C']
    csv_it_discarded_cols = discard_columns(source=get_csv_dict_reader(csv_in), to_remove=remove_list)

    assert next(csv_it_discarded_cols) == {'A': '1'}
    assert next(csv_it_discarded_cols) == {'A': '4'}
