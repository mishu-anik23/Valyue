from dataframe import *


def test_encode_dataframe_one_signal_16_bit():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=16, msn=1, lsn=4))

    assert df_obj_test.encode_frame(raw_value_1=0x8707) == [0, 8, 7, 0, 7, 0, 0, 0]


def test_encode_dataframe_one_signal_12_bit():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=12, msn=1, lsn=3))
    assert df_obj_test.encode_frame(raw_value_1=0x19C) == [0, 1, 9, 0xC, 0, 0, 0, 0]


def test_encode_dataframe_one_signal_12_bit_smplx_conti_spec():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=12, msn=1, lsn=3))

    assert df_obj_test.encode_frame(raw_value_1=0xD4F) == [0, 0xD, 4, 0xF, 0, 0, 0, 0]


def test_encode_dataframe_one_12_bit_smplx_conti_one_12_bit_bosch_temp():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                            encoding_2=SignalEncoding(bitwidth=12, msn=6, lsn=4)
                            )

    assert df_obj_test.encode_frame(raw_value_1=0xD4F, raw_value_2=0x19C) == [0, 0xD, 4, 0xF, 0xC, 9, 1, 0]


def test_encode_dataframe_two_12_12_bit_same_signal():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                            encoding_2=SignalEncoding(bitwidth=12, msn=6, lsn=4)
                            )
    assert df_obj_test.encode_frame(raw_value_1=0x19C, raw_value_2=0x19C) == [0, 1, 9, 0xC, 0xC, 9, 1, 0]


def test_encode_dataframe_two_10_14_bit_shared_nibble():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=10, msn=1, lsn=3),
                            encoding_2=SignalEncoding(bitwidth=14, msn=6, lsn=3)
                            )

    assert df_obj_test.encode_frame(raw_value_1=0x08D, raw_value_2=0x0609) == [0, 2, 3, 5, 2, 8, 1, 0]


def test_decode_dataframe_one_signal_16_bit():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=16, msn=1, lsn=4))

    assert df_obj_test.decode_frame(nibbles=[0, 8, 7, 0, 7, 0, 0, 0]) == (0x8707, None)


def test_decode_dataframe_one_signal_12_bit():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=12, msn=1, lsn=3))

    assert df_obj_test.decode_frame(nibbles=[0, 1, 9, 0xC, 0, 0, 0, 0]) == (0x19C, None)


def test_decode_dataframe_two_12_12_bit_same_signal():
    df_obj_test = DataFrame(encoding_1=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                            encoding_2=SignalEncoding(bitwidth=12, msn=6, lsn=4)
                            )

    assert df_obj_test.decode_frame(nibbles=[0, 1, 9, 0xC, 0xC, 9, 1, 0]) == (0x19C, 0x19C)
