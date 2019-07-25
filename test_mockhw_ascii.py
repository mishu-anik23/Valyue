import io
import pytest

from mockhw_ascii import *
from unique_row import drop_duplicates, isequal

sig_in_1st = SignalDefinition(name="Concentration", minimum='-10', maximum='100', unit='%',
                              physical=spec_conti(minimum=-10, maximum=100,
                                                  resolution=0.01, bitwidth=16, errorcodes={}, offset=-10),
                              encoding=SignalEncoding(bitwidth=16, msn=1, lsn=4),
                              default=25.46)

sig_in_1st_as_2nd_signal = SignalDefinition(name="Concentration", minimum='-10', maximum='100', unit='%',
                                            physical=spec_conti(minimum=-10, maximum=100,
                                                                resolution=0.01, bitwidth=16, errorcodes={}, offset=-10),
                                            encoding=SignalEncoding(bitwidth=16, msn=6, lsn=3),
                                            default=25.46)

sig_in_2nd = SignalDefinition(name="Supply Voltage", minimum='0', maximum='40.75', unit='V',
                              physical=spec_conti(minimum=0, maximum=40.75,
                                                  resolution=0.16, bitwidth=8, errorcodes={}, offset=0),
                              encoding=SignalEncoding(bitwidth=8, msn=1, lsn=2),
                              default=5.671875)

sig_in_3rd = SignalDefinition(name="Runtime 1", minimum='0', maximum='1023', unit='V',
                              physical=spec_conti(minimum=0, maximum=1023,
                                                  resolution=0.015625, bitwidth=16, errorcodes={}, offset=0),
                              encoding=SignalEncoding(bitwidth=16, msn=1, lsn=4),
                              default=15.671875)

sig_in_3rd_as_2nd_signal = SignalDefinition(name="Runtime 1", minimum='0', maximum='1023', unit='V',
                                            physical=spec_conti(minimum=0, maximum=1023,
                                                                resolution=0.015625, bitwidth=16, errorcodes={}, offset=0),
                                            encoding=SignalEncoding(bitwidth=16, msn=6, lsn=3),
                                            default=15.671875)


@pytest.fixture()
def processed_ascii():
    ascii2csv_file_content =io.StringIO("""\
time,Concentration,Supply Voltage,Runtime 1,
0.0998410,55.0,12.0,8.0
0.1085597,55.0,12.0,8.0
0.1182596,75.0,12.0,13.0
0.1292343,65.0,15.0,23.0
0.1383462,65.0,15.0,8.0
0.1493690,65.0,12.0,5.0
0.1592528,85.0,14.0,8.0
0.1685217,85.0,12.0,8.0""")

    csv_row = csv.DictReader(ascii2csv_file_content)
    return csv_row


def test_translate_headers_ascii_to_sent():
    headers_in = ['A', 'B', 'X', 'W', 'C']
    conversion_dct = {'A': 'Apple', 'B': 'Ball', 'C': 'Cat'}

    assert translate_headers(headers=headers_in, mapping=conversion_dct) == ['Apple', 'Ball', 'X', 'W', 'Cat']


def test_signal_row_generator_with_time_and_one_signal_1(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_1st)

    assert next(signal_rows) == {'time': '0.0998410', 'Concentration': '55.0'}
    assert next(signal_rows) == {'time': '0.1085597', 'Concentration': '55.0'}
    assert next(signal_rows) == {'time': '0.1182596', 'Concentration': '75.0'}
    assert next(signal_rows) == {'time': '0.1292343', 'Concentration': '65.0'}


def test_drop_duplicates_drops_same_prev_val_one_signal_1(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_1st)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)

    assert list(unique_rows) == [{'time': '0.0998410', 'Concentration': '55.0'},
                                 {'time': '0.1182596', 'Concentration': '75.0'},
                                 {'time': '0.1292343', 'Concentration': '65.0'},
                                 {'time': '0.1592528', 'Concentration': '85.0'}]



def test_signal_row_generator_with_time_and_one_signal_2(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd)

    assert next(signal_rows) == {'time': '0.0998410', 'Supply Voltage': '12.0'}
    assert next(signal_rows) == {'time': '0.1085597', 'Supply Voltage': '12.0'}
    assert next(signal_rows) == {'time': '0.1182596', 'Supply Voltage': '12.0'}
    assert next(signal_rows) == {'time': '0.1292343', 'Supply Voltage': '15.0'}


def test_drop_duplicates_drops_same_prev_val_one_signal_2(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)

    assert list(unique_rows) == [{'time': '0.0998410', 'Supply Voltage': '12.0'},
                                 {'time': '0.1292343', 'Supply Voltage': '15.0'},
                                 {'time': '0.1493690', 'Supply Voltage': '12.0'},
                                 {'time': '0.1592528', 'Supply Voltage': '14.0'},
                                 {'time': '0.1685217', 'Supply Voltage': '12.0'}]


def test_signal_row_generator_with_time_and_one_signal_3(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_3rd)

    assert next(signal_rows) == {'time': '0.0998410', 'Runtime 1': '8.0'}
    assert next(signal_rows) == {'time': '0.1085597', 'Runtime 1': '8.0'}
    assert next(signal_rows) == {'time': '0.1182596', 'Runtime 1': '13.0'}
    assert next(signal_rows) == {'time': '0.1292343', 'Runtime 1': '23.0'}


def test_drop_duplicates_drops_same_prev_val_one_signal_3(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_3rd)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)

    assert list(unique_rows) == [{'time': '0.0998410', 'Runtime 1': '8.0'},
                                 {'time': '0.1182596', 'Runtime 1': '13.0'},
                                 {'time': '0.1292343', 'Runtime 1': '23.0'},
                                 {'time': '0.1383462', 'Runtime 1': '8.0'},
                                 {'time': '0.1493690', 'Runtime 1': '5.0'},
                                 {'time': '0.1592528', 'Runtime 1': '8.0'}]


def test_signal_row_generator_with_time_and_two_signal_1(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd, signal2=sig_in_3rd)

    assert next(signal_rows) == {'time': '0.0998410', 'Supply Voltage': '12.0', 'Runtime 1': '8.0'}
    assert next(signal_rows) == {'time': '0.1085597', 'Supply Voltage': '12.0', 'Runtime 1': '8.0'}
    assert next(signal_rows) == {'time': '0.1182596', 'Supply Voltage': '12.0', 'Runtime 1': '13.0'}
    assert next(signal_rows) == {'time': '0.1292343', 'Supply Voltage': '15.0', 'Runtime 1': '23.0'}


def test_drop_duplicates_drops_same_prev_val_two_signal_1(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd, signal2=sig_in_3rd)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)

    assert list(unique_rows) == [{'time': '0.0998410', 'Supply Voltage': '12.0', 'Runtime 1': '8.0'},
                                 {'time': '0.1182596', 'Supply Voltage': '12.0', 'Runtime 1': '13.0'},
                                 {'time': '0.1292343', 'Supply Voltage': '15.0', 'Runtime 1': '23.0'},
                                 {'time': '0.1383462', 'Supply Voltage': '15.0', 'Runtime 1': '8.0'},
                                 {'time': '0.1493690', 'Supply Voltage': '12.0', 'Runtime 1': '5.0'},
                                 {'time': '0.1592528', 'Supply Voltage': '14.0', 'Runtime 1': '8.0'},
                                 {'time': '0.1685217', 'Supply Voltage': '12.0', 'Runtime 1': '8.0'}]


def test_signal_row_generator_with_time_and_two_signal_2(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd, signal2=sig_in_1st)

    assert next(signal_rows) == {'time': '0.0998410', 'Supply Voltage': '12.0', 'Concentration': '55.0'}
    assert next(signal_rows) == {'time': '0.1085597', 'Supply Voltage': '12.0', 'Concentration': '55.0'}
    assert next(signal_rows) == {'time': '0.1182596', 'Supply Voltage': '12.0', 'Concentration': '75.0'}
    assert next(signal_rows) == {'time': '0.1292343', 'Supply Voltage': '15.0', 'Concentration': '65.0'}


def test_drop_duplicates_drops_same_prev_val_two_signal_2(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd, signal2=sig_in_1st)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)

    assert list(unique_rows) == [{'time': '0.0998410', 'Supply Voltage': '12.0', 'Concentration': '55.0'},
                                 {'time': '0.1182596', 'Supply Voltage': '12.0', 'Concentration': '75.0'},
                                 {'time': '0.1292343', 'Supply Voltage': '15.0', 'Concentration': '65.0'},
                                 {'time': '0.1493690', 'Supply Voltage': '12.0', 'Concentration': '65.0'},
                                 {'time': '0.1592528', 'Supply Voltage': '14.0', 'Concentration': '85.0'},
                                 {'time': '0.1685217', 'Supply Voltage': '12.0', 'Concentration': '85.0'}]


def test_signal_frame_generator_generates_timestamps_in_integer(processed_ascii):
    signal_frames = signal_frame_generator(source=processed_ascii, signal1=sig_in_1st)

    assert next(signal_frames)[0] == 39000
    assert next(signal_frames)[0] == 42406
    assert next(signal_frames)[0] == 46195
    assert next(signal_frames)[0] == 50482
    assert next(signal_frames)[0] == 54041
    assert next(signal_frames)[0] == 58347


def test_signal_frame_generator_generates_unique_frame_one_signal_1(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_1st)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)
    signal_frames = signal_frame_generator(source=unique_rows, signal1=sig_in_1st)

    assert next(signal_frames)[1] == [0, 1, 9, 6, 4, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 2, 1, 3, 4, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 1, 13, 4, 12, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 2, 5, 1, 12, 0, 0, 0]


def test_signal_frame_generator_generates_unique_frame_one_signal_2(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)
    signal_frames = signal_frame_generator(source=unique_rows, signal1=sig_in_2nd)

    assert next(signal_frames)[1] == [0, 4, 11, 0, 0, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 5, 14, 0, 0, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 4, 11, 0, 0, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 5, 8, 0, 0, 0, 0, 0]


def test_signal_frame_generator_generates_unique_frame_one_signal_3(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_3rd)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)
    signal_frames = signal_frame_generator(source=unique_rows, signal1=sig_in_3rd)

    assert next(signal_frames)[1] == [0, 0, 2, 0, 0, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 0, 3, 4, 0, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 0, 5, 12, 0, 0, 0, 0]
    assert next(signal_frames)[1] == [0, 0, 2, 0, 0, 0, 0, 0]


def test_signal_frame_generator_generates_unique_frame_with_time_and_two_signal_1(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd, signal2=sig_in_1st_as_2nd_signal)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)
    signal_frames = signal_frame_generator(source=unique_rows, signal1=sig_in_2nd, signal2=sig_in_1st_as_2nd_signal)

    assert next(signal_frames) == (39000, [0, 4, 11, 4, 6, 9, 1, 0])
    assert next(signal_frames) == (46195, [0, 4, 11, 4, 3, 1, 2, 0])
    assert next(signal_frames) == (50482, [0, 5, 14, 12, 4, 13, 1, 0])
    assert next(signal_frames) == (58347, [0, 4, 11, 12, 4, 13, 1, 0])
    assert next(signal_frames) == (62208, [0, 5, 8, 12, 1, 5, 2, 0])


def test_signal_frame_generator_generates_unique_frame_with_time_and_two_signal_2(processed_ascii):
    signal_rows = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd, signal2=sig_in_3rd_as_2nd_signal)
    unique_rows = drop_duplicates(source=signal_rows, predicate=isequal)
    signal_frames = signal_frame_generator(source=unique_rows, signal1=sig_in_2nd, signal2=sig_in_3rd_as_2nd_signal)

    assert next(signal_frames) == (39000, [0, 4, 11, 0, 0, 2, 0, 0])
    assert next(signal_frames) == (46195, [0, 4, 11, 0, 4, 3, 0, 0])
    assert next(signal_frames) == (50482, [0, 5, 14, 0, 12, 5, 0, 0])
    assert next(signal_frames) == (54041, [0, 5, 14, 0, 0, 2, 0, 0])
    assert next(signal_frames) == (58347, [0, 4, 11, 0, 4, 1, 0, 0])
