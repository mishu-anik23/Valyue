from signaldef import *
from unique_row import *


sig_in_1st = SignalDefinition(name="Concentration", minimum='-10', maximum='100', unit='%',
                              physical=spec_conti(minimum=-10, maximum=100,
                                                  resolution=0.01, bitwidth=16, errorcodes={}, offset=-10),
                              encoding=SignalEncoding(bitwidth=16, msn=6, lsn=3),
                              default=25.46)

sig_in_2nd = SignalDefinition(name="Supply Voltage", minimum='0', maximum='40.75', unit='V',
                              physical=spec_conti(minimum=0, maximum=40.75,
                                                  resolution=0.16, bitwidth=8, errorcodes={}, offset=0),
                              encoding=SignalEncoding(bitwidth=8, msn=1, lsn=2),
                              default=5.671875)

input_src_1_signal = [{'time': 0.123, 'Concentration': 80.0},
                      {'time': 0.153, 'Concentration': 80.0},
                      {'time': 0.223, 'Concentration': 70.0},
                      {'time': 0.363, 'Concentration': 80.0},
                      {'time': 0.523, 'Concentration': 90.0},
                      {'time': 0.703, 'Concentration': 90.0},
                      {'time': 0.823, 'Concentration': 60.0}]

input_src_2_signal = [{'time': 0.123, 'Concentration': 80.0, 'Supply Voltage': 15.0},
                      {'time': 0.153, 'Concentration': 80.0, 'Supply Voltage': 12.0},
                      {'time': 0.223, 'Concentration': 70.0, 'Supply Voltage': 12.0},
                      {'time': 0.363, 'Concentration': 80.0, 'Supply Voltage': 15.0},
                      {'time': 0.523, 'Concentration': 90.0, 'Supply Voltage': 18.0},
                      {'time': 0.703, 'Concentration': 90.0, 'Supply Voltage': 18.0},
                      {'time': 0.823, 'Concentration': 60.0, 'Supply Voltage': 12.0}]


def make_generator(source):
    for row in source:
        yield row


def test_drop_duplicates_is_a_generator():
    input_list = [1, 2, 3, 4, 5]
    fake_gen = make_generator(source=input_list)
    urows = drop_duplicates(source=fake_gen)
    assert list(urows) == [1, 2, 3, 4, 5]


def test_drop_duplicates_returns_a_unique_list():
    input_list = [1, 1, 2, 2, 2, 3]
    urows = drop_duplicates(source=input_list)
    assert list(urows)[:2] == [1, 2]


def test_drop_duplicates_generates_unique_elements():
    input_list = [5, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5]
    generator = make_generator(source=input_list)
    urows = drop_duplicates(source=generator)
    assert list(urows) == [5, 2, 3, 4, 5]


def test_drop_duplicates_does_not_like_none():
    input_list = [None, None]
    urows = drop_duplicates(source=input_list)
    assert list(urows) == [None, None]


def test_drop_duplicates_with_compare_rows_ignores_time_and_return_unique_elements_1():
    generator = make_generator(source=input_src_1_signal)
    urows = drop_duplicates(source=generator, predicate=isequal)

    assert next(urows) == {'time': 0.123, 'Concentration': 80.0}
    assert next(urows) == {'time': 0.223, 'Concentration': 70.0}
    assert next(urows) == {'time': 0.363, 'Concentration': 80.0}
    assert next(urows) == {'time': 0.523, 'Concentration': 90.0}
    assert next(urows) == {'time': 0.823, 'Concentration': 60.0}


def test_drop_duplicates_with_compare_rows_ignores_time_and_return_unique_elements_2():
    generator = make_generator(source=input_src_2_signal)
    urows = drop_duplicates(source=generator, predicate=isequal)

    assert next(urows) == {'time': 0.123, 'Concentration': 80.0, 'Supply Voltage': 15.0}
    assert next(urows) == {'time': 0.153, 'Concentration': 80.0, 'Supply Voltage': 12.0}
    assert next(urows) == {'time': 0.223, 'Concentration': 70.0, 'Supply Voltage': 12.0}
    assert next(urows) == {'time': 0.363, 'Concentration': 80.0, 'Supply Voltage': 15.0}
    assert next(urows) == {'time': 0.523, 'Concentration': 90.0, 'Supply Voltage': 18.0}
    assert next(urows) == {'time': 0.823, 'Concentration': 60.0, 'Supply Voltage': 12.0}


def test_compare_rows_are_different():
    row1 = {'time': 0.123, 'Concentration': 80.0, 'Supply Voltage': 15.0}
    row2 = {'time': 0.153, 'Concentration': 80.0, 'Supply Voltage': 12.0}
    assert not isequal(row1, row2)


def test_compare_rows_are_equal():
    row1 = {'time': 0.153, 'Concentration': 80.0, 'Supply Voltage': 12.0}
    row2 = {'time': 0.183, 'Concentration': 80.0, 'Supply Voltage': 12.0}
    assert isequal(row1, row2)


def test_compare_rows_are_equal_2():
    row1 = {'time': 0.153, 'Percentage': 80.0, 'Supply Voltage': 12.0}
    row2 = {'time': 0.183, 'Percentage': 80.0, 'Supply Voltage': 12.0}
    assert isequal(row1, row2)


def test_compare_rows_are_equal_empty_dict():
    row1 = {}
    row2 = {}
    assert isequal(row1, row2)


def test_compare_rows_are_equal_with_equal_time():
    row1 = {'time': 0.153, 'Percentage': 80.0, 'Supply Voltage': 12.0}
    row2 = {'time': 0.153, 'Percentage': 80.0, 'Supply Voltage': 12.0}
    assert isequal(row1, row2)


def test_compare_rows_are_equal_with_no_time():
    row1 = {'Percentage': 80.0, 'Supply Voltage': 12.0}
    row2 = {'Percentage': 80.0, 'Supply Voltage': 12.0}
    assert isequal(row1, row2)


def test_compare_values_are_different():
    value1 = (2, 3)
    value2 = (4, 4)
    assert not compare_values(value1, value2)


def test_compare_values_are_equal():
    value1 = (2, 3)
    value2 = (2, 4)
    assert compare_values(value1, value2)

def test_empty_dicts_are_equal():
    row1 = {}
    row2 = {}
    assert isequal(row1, row2)


def test_non_empty_dict_unequal_to_empty_dict():
    row1 = {'a': 1}
    row2 = {}
    assert not isequal(row1, row2)


def test_non_empty_dict_unequal_to_empty_dict_1():
    row1 = {}
    row2 = {'a': 1}
    assert not isequal(row1, row2)


def test_non_empty_dict_unequal_to_empty_dict_2():
    row1 = {'a': 1}
    row2 = {'a': 1}
    assert isequal(row1, row2)
