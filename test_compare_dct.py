from unique_row import isequal


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


def test_1():
    row1 = {'a': 1}
    row2 = {'b': 1}
    assert not isequal(row1, row2)


def test_2():
    row1 = {'b': 1}
    row2 = {'b': 1}
    assert isequal(row1, row2)


def test_3():
    row1 = {'c': 3, 'd': 4}
    row2 = {'c': 3, 'd': 44}
    assert not isequal(row1, row2)


def test_4():
    row1 = {'c': 3, 'd': 4}
    row2 = {'d': 3, 'c': 4}
    assert not isequal(row1, row2)


def test_5():
    row1 = {'a': 1}
    row2 = {'a': 1, 'b': 2}
    assert not isequal(row1, row2)
