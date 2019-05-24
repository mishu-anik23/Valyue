import pytest
from signaldef import SignalEncoding
from dataframe import DataFrame


def test_encode_decode_16_bit_1st_signal():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=1, lsn=4)

    assert enc_obj_test.encode(raw_value=0x8707) == [8, 7, 0, 7]
    assert enc_obj_test.decode(dataframe=[0, 8, 7, 0, 7, 0, 0, 0]) == 0x8707


def test_encode_frame_16_bit_1st_signal_no_zero_padded():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=1, lsn=4)

    assert enc_obj_test.encode_frame(raw=0x8706) == [0xF, 8, 7, 0, 6, 0xF, 0xF, 0xF]


def test_encode_decode_16_bit_2nd_signal():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=6, lsn=3)

    assert enc_obj_test.encode(raw_value=0x8707) == [7, 0, 7, 8]
    assert enc_obj_test.decode(dataframe=[0, 0, 0, 7, 0, 7, 8, 0]) == 0x8707


def test_encode_frame_16_bit_2nd_signal_no_zero_padded():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=6, lsn=3)

    assert enc_obj_test.encode_frame(raw=0x8706) == [0xF, 0xF, 0xF, 6, 0, 7, 8, 0xF]


def test_encode_decode_12_bit_1st_signal():
    enc_obj_test = SignalEncoding(bitwidth=12, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0x870) == [8, 7, 0]
    assert enc_obj_test.decode(dataframe=[0, 8, 7, 0, 0, 0, 0, 0]) == 0x870


def test_encode_decode_12_bit_2nd_signal():
    enc_obj_test = SignalEncoding(bitwidth=12, msn=5, lsn=3)

    assert enc_obj_test.encode(raw_value=0x871) == [1, 7, 8]
    assert enc_obj_test.decode(dataframe=[0, 0, 0, 1, 7, 8, 0, 0]) == 0x871


def test_encode_decode_10_bit_1st_signal_1():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0xEB) == [3, 0xA, 0xC]
    assert enc_obj_test.decode(dataframe=[0, 3, 0xA, 0xC, 0, 0, 0, 0]) == 0xEB


def test_encode_decode_10_bit_2nd_signal_1():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=6, lsn=4)

    assert enc_obj_test.encode(raw_value=0xEB) == [0x3, 0xA, 3]
    assert enc_obj_test.decode(dataframe=[0, 0, 0, 0, 0x3, 0xA, 0x3, 0]) == 0xEB


def test_encode_decode_10_bit_1st_signal_2():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0x227) == [8, 9, 0xC]
    assert enc_obj_test.decode(dataframe=[0, 8, 9, 0xC, 0, 0, 0, 0]) == 0x227


def test_encode_decode_10_bit_2nd_signal_2():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=4, lsn=2)

    assert enc_obj_test.encode(raw_value=0x227) == [3, 9, 8]
    assert enc_obj_test.decode(dataframe=[0, 0, 3, 9, 8, 0, 0, 0]) == 0x227


def test_encode_decode_with_dataframe_12_12_bit_1():
    raw1_in, raw2_in = 0xD4F, 0x19C
    df_in = [0, 0xD, 4, 0xF, 0xC, 9, 1, 0]

    enc_obj_test_1 = SignalEncoding(bitwidth=12, msn=1, lsn=3)

    assert enc_obj_test_1.encode(raw_value=raw1_in) == [0xD, 4, 0xF]
    assert enc_obj_test_1.decode(dataframe=[0, 0xD, 4, 0xF, 0, 0, 0, 0]) == 0xD4F

    enc_obj_test_2 = SignalEncoding(bitwidth=12, msn=6, lsn=4)

    assert enc_obj_test_2.encode(raw_value=raw2_in) == [0xC, 9, 1]
    assert enc_obj_test_2.decode(dataframe=[0, 0, 0, 0, 0xC, 9, 1, 0]) == 0x19C

    df_obj_test = DataFrame(encoding1=enc_obj_test_1, encoding2=enc_obj_test_2)

    assert df_obj_test.encode_frame(raw1=raw1_in, raw2=raw2_in) == df_in
    assert df_obj_test.decode_frame(dataframe=df_in) == (raw1_in, raw2_in)


def test_encode_decode_with_dataframe_shared_nibble_10_14_bit_1():
    raw1_in, raw2_in = 0x227, 0xBA9C
    df_in = [0, 8, 9, 0xE, 0xD, 4, 0xC, 0]

    enc_obj_test_1 = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test_1.encode(raw_value=raw1_in) == [8, 9, 0xC]
    assert enc_obj_test_1.decode(dataframe=[0, 8, 9, 0xC, 0, 0, 0, 0]) == 0x227

    enc_obj_test_2 = SignalEncoding(bitwidth=14, msn=6, lsn=3)

    assert enc_obj_test_2.encode(raw_value=raw2_in) == [7, 0xA, 0xD, 2]
    assert enc_obj_test_2.decode(dataframe=[0, 0, 0, 7, 0xA, 0xD, 2, 0]) == 0xBA9C

    df_obj_test = DataFrame(encoding1=enc_obj_test_1, encoding2=enc_obj_test_2)

    assert df_obj_test.encode_frame(raw1=raw1_in, raw2=raw2_in) == df_in
    assert df_obj_test.decode_frame(dataframe=df_in) == (raw1_in, raw2_in)

