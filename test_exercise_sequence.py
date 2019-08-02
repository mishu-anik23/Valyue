import pytest
from exercise_sequence import *


def test_mult_add_sequences_1():
    list_in = [1, 2, 3, 0, 5, 6]
    assert mult_add_sequences(list_in) == [1 * (2 + 3), 2 * (3 + 0), 3 * (0 + 5), (5 + 6)]


def test_mult_add_sequences_2():
    list_in = [1, 2, 3, 5, 8, 13, 21]
    assert mult_add_sequences(list_in) == [1 * (2 + 3), 2 * (3 + 5), 3 * (5 + 8), 5 * (8 + 13), 8 * (13 + 21)]


def test_mult_add_sequences_3():
    list_in = [-2, -1, 0, -1, 0, 1, 0]
    assert mult_add_sequences(list_in) == [-2 * (-1 + 0), -1 * (0 - 1), (-1 + 0), -1 * (0 + 1), (1 + 0)]


def test_mult_add_sequences_with_empty_list():
    list_in = []
    assert mult_add_sequences(list_in) == []


def test_mult_add_sequences_with_one_element():
    list_in = [1]
    assert mult_add_sequences(list_in) == []


def test_mult_add_sequences_with_two_element():
    list_in = [1, 2]
    assert mult_add_sequences(list_in) == []


def test_mult_add_sequences_same_element():
    list_in = [1, 1, 1, 1]
    assert mult_add_sequences(list_in) == [1 * (1 + 1), 1 * (1 + 1)]


def test_generate_mult_add_sequences_1():
    list_in = [1, 2, 0, 5]
    generator = generate_mult_add_sequences(list_in)
    assert list(generator) == [1 * (2 + 0), 2 * (0 + 5)]


def test_generate_mult_add_sequences_2():
    list_in = [1, 2, 3, 5]
    generator = generate_mult_add_sequences(list_in)
    assert list(generator) == [1 * (2 + 3), 2 * (3 + 5)]


def test_generate_mult_add_sequences_3():
    list_in = [-2, -1, 0, -1, 0, 1, 0]
    generator = generate_mult_add_sequences(list_in)
    assert list(generator) == [-2 * (-1 + 0), -1 * (0 - 1), (-1 + 0), -1 * (0 + 1), (1 + 0)]


def test_generate_mult_add_sequences_with_empty_list():
    list_in = []
    generator = generate_mult_add_sequences(list_in)
    assert list(generator) == []


def test_generate_mult_add_sequences_with_one_element():
    list_in = [1]
    generator = generate_mult_add_sequences(list_in)
    assert list(generator) == []


def test_generate_mult_add_sequences_with_two_element():
    list_in = [1, 2]
    generator = generate_mult_add_sequences(list_in)
    assert list(generator) == []


def test_generate_mult_add_sequences_same_element():
    list_in = [1, 1, 1, 1]
    generator = generate_mult_add_sequences(list_in)
    assert list(generator) == [1 * (1 + 1), 1 * (1 + 1)]


def test_get_consecutive_diffs_1():
    list_in = [1, 1, 2, 3, 5, 8, 13]
    assert consecutive_diffs(list_in) == [0, 1, 1, 2, 3, 5]


def test_get_consecutive_diffs_2():
    list_in = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    assert consecutive_diffs(list_in) == [1, 2, 4, 8, 16, 32, 64, 128]


def test_get_consecutive_diffs_3():
    list_in = [-1, 2, -4, 8, -16, 32, -64, 128]
    assert consecutive_diffs(list_in) == [3, -6, 12, -24, 48, -96, 192]


def test_get_consecutive_diffs_with_empty_list():
    list_in = []
    with pytest.raises(ValueError) as exc:
        consecutive_diffs(list_in)
        assert 'need two elements' in str(exc)


def test_get_consecutive_diffs_with_one_element():
    list_in = [1]
    with pytest.raises(ValueError) as exc:
        consecutive_diffs(list_in)
        assert 'need two elements' in str(exc)


def test_get_consecutive_diffs_with_two_element():
    list_in = [1, 2]
    assert consecutive_diffs(list_in) == [1]


def test_generate_consecutive_diffs_1():
    list_in = [1, 1, 2, 3, 5, 8, 13]
    diffs_generator = generate_consecutive_diff(list_in)
    assert list(diffs_generator) == [0, 1, 1, 2, 3, 5]


def test_generate_consecutive_diffs_2():
    list_in = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    diffs_generator = generate_consecutive_diff(list_in)
    assert list(diffs_generator) == [1, 2, 4, 8, 16, 32, 64, 128]


def test_generate_consecutive_diffs_3():
    list_in = [-1, 2, -4, 8, -16, 32, -64, 128]
    diffs_generator = generate_consecutive_diff(list_in)
    assert list(diffs_generator) == [3, -6, 12, -24, 48, -96, 192]


def test_generate_consecutive_diffs_with_same_element():
    list_in = [1, 1, 1, 1, 1, 1]
    diffs_generator = generate_consecutive_diff(list_in)
    assert list(diffs_generator) == [0, 0, 0, 0, 0]


def test_generate_consecutive_diffs_with_empty_list():
    list_in = []
    diffs_generator = generate_consecutive_diff(list_in)
    assert list(diffs_generator) == []
    # with pytest.raises(ValueError) as exc:
    #     list(diffs_generator)
    #     assert 'need two elements' in str(exc)


def test_generate_consecutive_diffs_with_one_element():
    list_in = [1]
    diffs_generator = generate_consecutive_diff(list_in)
    #assert list(diffs_generator) == []
    with pytest.raises(ValueError) as exc:
        list(diffs_generator)
        assert 'need two elements' in str(exc)


def test_consecutive_diffs_with_a_zero():
    input = [0, 2, 1]
    assert consecutive_diffs(input) == [2, -1]


def test_consecutive_sums_1():
    input = [1, 1, 2, 3, 5, 8, 13]
    assert consecutive_sums(input) == [2, 3, 5, 8, 13, 21]


def test_consecutive_sums_2():
    input = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    assert consecutive_sums(input) == [3, 6, 12, 24, 48, 96, 192, 384]


def test_consecutive_sums_3():
    input = [-1, 2, -4, 8, -16, 32, -64, 128]
    assert consecutive_sums(input) == [1, -2, 4, -8, 16, -32, 64]


def test_cumulative_sums_1():
    list_in = [1, 2, 3, 4]
    assert cumulative_sums(list_in) == [1, 3, 6, 10]


def test_generate_cumulative_sums_1():
    generate_sum = generate_cumulative_sum([1, 2, 3, 4])

    assert list(generate_sum) == [1, 3, 6, 10]


def test_generate_sums_of_consecutive_pairs():
     generate_sum_pair = consecutive_sum_pairs([1, 2, 3, 4, 5, 6])

     assert list(generate_sum_pair) == [(1+2), (3+4), (5+6)]


def test_current_and_largest_sequences_1():
    list_in = [1, 1, 2, 3, 5]
    print(current_largest_sequences(list_in))
    assert current_largest_sequences(list_in) == [(1, 1), (1, 1), (1, 2), (2, 3), (3, 5)]


def test_current_and_largest_sequences_2():
    list_in = [-1, 2, -4, 8, -16, 32]
    print(current_largest_sequences(list_in))
    assert current_largest_sequences(list_in) == [(-1, -1), (-1, 2), (2, 2), (-4, 8), (8, 8), (-16, 32)]


def test_current_and_largest_sequences_with_empty_list():
    list_in = []
    assert current_largest_sequences(list_in) == []


def test_current_and_largest_sequences_with_one_element():
    list_in = [1]
    assert current_largest_sequences(list_in) == [(1, 1)]


def test_generate_current_and_largest_sequences_1():
    list_in = [1, 1, 2, 3, 5]
    generator = generate_current_and_largest_sequences(list_in)
    assert list(generator) == [(1, 1), (1, 1), (1, 2), (2, 3), (3, 5)]


def test_generate_current_and_largest_sequences_2():
    list_in = [-1, 2, -4, 8]
    generator = generate_current_and_largest_sequences(list_in)
    assert list(generator) == [(-1, -1), (-1, 2), (2, 2), (-4, 8)]


def test_generate_current_and_largest_sequences_with_empty_list():
    list_in = []
    generator = generate_current_and_largest_sequences(list_in)
    assert list(generator) == []


def test_generate_current_and_largest_sequences_with_one_element():
    list_in = [1]
    generator = generate_current_and_largest_sequences(list_in)
    assert list(generator) == [(1, 1)]

