from exercise_sequence import *

def test_sequence_generator_1():
    input = [1, 2, 3, 0, 5, 6]
    assert generate_sequence(input) == [1*(2+3), 2*(3+0), 3*(0+5), (5+6)]


def test_sequence_generator_2():
    input = [1, 2, 3, 5, 8, 13, 21]
    assert generate_sequence(input) == [1*(2+3), 2*(3+5), 3*(5+8), 5*(8+13), 8*(13+21)]


def test_sequence_generator_3():
    input = [-2, -1, 0, -1, 0, 1, 0]
    assert generate_sequence(input) == [-2*(-1+0), -1*(0-1), (-1+0), -1*(0+1), (1+0)]


def test_consecutive_diffs_1():
    input = [1, 1, 2, 3, 5, 8, 13]
    assert consecutive_diffs(input) == [0, 1, 1, 2, 3, 5]


def test_consecutive_diffs_2():
    input = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    assert consecutive_diffs(input) == [1, 2, 4, 8, 16, 32, 64, 128]


def test_consecutive_diffs_3():
    input = [-1, 2, -4, 8, -16, 32, -64, 128]
    assert consecutive_diffs(input) == [3, -6, 12, -24, 48, -96, 192]



def test_consecutive_sums_1():
    input = [1, 1, 2, 3, 5, 8, 13]
    assert consecutive_sums(input) == [2, 3, 5, 8, 13, 21]


def test_consecutive_sums_2():
    input = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    assert consecutive_sums(input) == [3, 6, 12, 24, 48, 96, 192, 384]


def test_consecutive_sums_3():
    input = [-1, 2, -4, 8, -16, 32, -64, 128]
    assert consecutive_sums(input) == [3, -6, 12, -24, 48, -96, 192]



def test_generate_consecutive_diff_between_numbers():
    generate_diffs = generate_consecutive_diff([1, 1, 2, 3, 5, 8, 13])

    assert list(generate_diffs) == [0, 0, 1, 1, 2, 3, 5]


def test_generate_consecutive_sum_between_numbers():
    generate_sum = generate_consecutive_sum([1,2,3,4])

    assert list(generate_sum) == [1, 3, 6, 10]


def test_generate_sums_of_consecutive_pairs():
     generate_sum_pair = consecutive_sum_pairs([1, 2, 3, 4, 5, 6])

     assert list(generate_sum_pair) ==  [(1+2), (3+4), (5+6)]