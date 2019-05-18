import pytest
from encode_decode import *


def test_encode_16bit_no_zero_padding():
    expected_nibble = [8, 7, 0, 7]
    assert encode(raw_value=0x8707, bitwidth=16) == expected_nibble


def test_encode_16bit_one_zero_padding():
    raw_value_in = 0x123    # 291
    bitwidth_in = 16
    expected_nibble = [0, 1, 2, 3]
    assert encode(raw_value_in, bitwidth_in) == expected_nibble


def test_encode_16bit_two_zero_padding():
    raw_value_in = 0x4C    # 76
    bitwidth_in = 16
    expected_nibble = [0, 0, 4, 12]
    assert encode(raw_value_in, bitwidth_in) == expected_nibble


def test_encode_16bit_three_zero_padding():
    raw_value_in = 0xC    # 12
    bitwidth_in = 16
    expected_nibble = [0, 0, 0, 12]
    assert encode(raw_value_in, bitwidth_in) == expected_nibble


def test_encode_12bit_no_zero_padding():
    assert encode(raw_value=0x92B, bitwidth=12) == [9, 2, 11]    # 2347


def test_encode_12bit_one_zero_padding():
    assert encode(raw_value=0x79, bitwidth=12) == [0, 7, 9]    # 121


def test_encode_12bit_two_zero_padding():
    assert encode(raw_value=0x7, bitwidth=12) == [0, 0, 7]    # 7


# Testing Encoding for shared Nibbles start here :

def test_encode_10bit_1():
    assert encode(raw_value=0x048, bitwidth=10) == [1, 2, 0]


def test_encode_10bit_2():
    assert encode(raw_value=0x08D, bitwidth=10) == [2, 3, 4]


def test_encode_10bit_3():
    assert encode(raw_value=0xEB, bitwidth=10) == [3, 0xA, 0xC]


def test_encode_10bit_4():
    assert encode(raw_value=0x227, bitwidth=10) == [8, 9, 0xC]


def test_encode_10bit_5():
    assert encode(raw_value=0x3CC, bitwidth=10) == [0xF, 3, 0]


def test_encode_10bit_6():
    assert encode(raw_value=0x0F6, bitwidth=10) == [3, 13, 8]


def test_encode_14bit_1():
    assert encode(raw_value=0x48D, bitwidth=14) == [1, 2, 3, 4]


def test_encode_14bit_2():
    assert encode(raw_value=0x3697, bitwidth=14) == [0xD, 0xA, 5, 0xC]


def test_encode_14bit_3():
    assert encode(raw_value=0x21FE, bitwidth=14) == [8, 7, 15, 8]


def test_encode_14bit_4():
    assert encode(raw_value=0x1ECF, bitwidth=14) == [7, 0xB, 3, 0xC]


def test_encode_14bit_5():
    assert encode(raw_value=0x0609, bitwidth=14) == [1, 8, 2, 4]


def test_encode_14bit_6():
    assert encode(raw_value=0x313A, bitwidth=14) == [0xC, 4, 0xE, 8]


# Test for High Speed Encoding start here :


def test_high_speed_enocde_1():
    assert encode(raw_value=0xFFF, bitwidth=12, nibblewidth=3) == [7, 7, 7, 7]


def test_high_speed_enocde_2():
    assert encode(raw_value=0x123, bitwidth=12, nibblewidth=3) == [0, 4, 4, 3]


def test_high_speed_enocde_3():
    assert encode(raw_value=0x777, bitwidth=12, nibblewidth=3) == [3, 5, 6, 7]


# Test ValueError of normal High Speed Encoding in case of unfit Bitwidth :


def test_high_speed_encode_bitwidth_exceed():
    with pytest.raises(ValueError) as exc:
        encode(raw_value=0xA5F4, bitwidth=12, nibblewidth=3)     # 42484
        assert "doesn't fit bitwidth" in str(exc)



# Test ValueError of normal Encoding in case of unfit Bitwidth :

def test_encode_bitwidth_exceed():
    with pytest.raises(ValueError) as exc:
        encode(raw_value=0x15F4, bitwidth=8)   # 5620
        assert "doesn't fit bitwidth" in str(exc)


# Test for encoding Nibble Data Frames start here :

    # Test encode_frame for 1 Signal :

def test_encode_frame_10bit_lonely_signal_1():
    data_1_in = NibbleData(nibbles=[1, 2, 0], bitwidth=10, msn=1, lsn=3)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 1, 2, 0, 0, 0, 0, 0]


def test_encode_frame_10bit_lonely_signal_2():
    data_1_in = NibbleData(nibbles=[2, 3, 4], bitwidth=10, msn=1, lsn=3)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 2, 3, 4, 0, 0, 0, 0]


def test_encode_frame_10bit_lonely_signal_3():
    data_1_in = NibbleData(nibbles=[3, 0xA, 0xC], bitwidth=10, msn=1, lsn=3)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 3, 0xA, 0xC, 0, 0, 0, 0]


def test_encode_frame_10bit_lonely_signal_4():
    data_1_in = NibbleData(nibbles=[8, 9, 0xC], bitwidth=10, msn=1, lsn=3)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 8, 9, 0xC, 0, 0, 0, 0]


def test_encode_frame_10bit_lonely_signal_5():
    data_1_in = NibbleData(nibbles=[0xF, 3, 0], bitwidth=10, msn=1, lsn=3)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 0xF, 3, 0, 0, 0, 0, 0]


def test_encode_frame_10bit_lonely_signal_6():
    data_1_in = NibbleData(nibbles=[3, 13, 8], bitwidth=10, msn=1, lsn=3)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 3, 13, 8, 0, 0, 0, 0]


def test_encode_frame_14bit_lonely_signal_1():
    data_1_in = NibbleData(nibbles=[1, 2, 3, 4], bitwidth=14, msn=1, lsn=4)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 1, 2, 3, 4, 0, 0, 0]


def test_encode_frame_14bit_lonely_signal_2():
    data_1_in = NibbleData(nibbles=[0xD, 0xA, 5, 0xC], bitwidth=14, msn=1, lsn=4)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 0xD, 0xA, 5, 0xC, 0, 0, 0]


def test_encode_frame_14bit_lonely_signal_3():
    data_1_in = NibbleData(nibbles=[8, 7, 15, 8], bitwidth=14, msn=1, lsn=4)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 8, 7, 15, 8, 0, 0, 0]


def test_encode_frame_14bit_lonely_signal_4():
    data_1_in = NibbleData(nibbles=[7, 0xB, 3, 0xC], bitwidth=14, msn=1, lsn=4)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 7, 0xB, 3, 0xC, 0, 0, 0]


def test_encode_frame_14bit_lonely_signal_5():
    data_1_in = NibbleData(nibbles=[1, 8, 2, 4], bitwidth=14, msn=1, lsn=4)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 1, 8, 2, 4, 0, 0, 0]


def test_encode_frame_14bit_lonely_signal_6():
    data_1_in = NibbleData(nibbles=[0xC, 4, 0xE, 8], bitwidth=14, msn=1, lsn=4)
    assert encode_frame(nibble_data_1=data_1_in) == [0, 0xC, 4, 0xE, 8, 0, 0, 0]


    # Test encode_frame for 2 Signal :


def test_encode_frame_10_10_bit_couple_signal_1_3():
    data_1_in = NibbleData(nibbles=[1, 2, 0], bitwidth=10, msn=1, lsn=3)
    data_2_in = NibbleData(nibbles=[3, 0xA, 0xC], bitwidth=10, msn=6, lsn=4)

    assert encode_frame(nibble_data_1=data_1_in, nibble_data_2=data_2_in) == [0, 1, 2, 0, 0xC, 0xA, 3, 0]


def test_encode_frame_10_10_bit_couple_signal_2_5():
    data_1_in = NibbleData(nibbles=[2, 3, 4], bitwidth=10, msn=1, lsn=3)
    data_2_in = NibbleData(nibbles=[0xF, 3, 0], bitwidth=10, msn=6, lsn=4)

    assert encode_frame(nibble_data_1=data_1_in, nibble_data_2=data_2_in) == [0, 2, 3, 4, 0, 3, 0xF, 0]


def test_encode_frame_10_10_bit_couple_signal_4_6():
    data_1_in = NibbleData(nibbles=[8, 9, 0xC], bitwidth=10, msn=1, lsn=3)
    data_2_in = NibbleData(nibbles=[3, 13, 8], bitwidth=10, msn=6, lsn=4)

    assert encode_frame(nibble_data_1=data_1_in, nibble_data_2=data_2_in) == [0, 8, 9, 0xC, 8, 13, 3, 0]


def test_encode_frame_10_14_bit_couple_signal_1_3():
    data_1_in = NibbleData(nibbles=[1, 2, 0], bitwidth=10, msn=1, lsn=3)
    data_2_in = NibbleData(nibbles=[9, 7, 15, 8], bitwidth=14, msn=6, lsn=3)

    assert encode_frame(nibble_data_1=data_1_in, nibble_data_2=data_2_in) == [0, 1, 2, 2, 15, 7, 9, 0]


def test_encode_frame_10_14_bit_couple_signal_2_5():
    data_1_in = NibbleData(nibbles=[2, 3, 4], bitwidth=10, msn=1, lsn=3)
    data_2_in = NibbleData(nibbles=[1, 8, 2, 4], bitwidth=14, msn=6, lsn=3)

    assert encode_frame(nibble_data_1=data_1_in, nibble_data_2=data_2_in) == [0, 2, 3, 5, 2, 8, 1, 0]


def test_encode_frame_10_14_bit_couple_signal_4_6():
    data_1_in = NibbleData(nibbles=[8, 9, 0xC], bitwidth=10, msn=1, lsn=3)
    data_2_in = NibbleData(nibbles=[0xC, 4, 0xD, 8], bitwidth=14, msn=6, lsn=3)

    assert encode_frame(nibble_data_1=data_1_in, nibble_data_2=data_2_in) == [0, 8, 9, 0xE, 0xD, 4, 0xC, 0]


def test_encode_frame_two_signals_1():
    nibbles1 = encode(0x0, 10)  # 0x000
    nibbles2 = encode(0x123, 10)  # 0x48C
    nd1 = NibbleData(nibbles1, bitwidth=10, msn=1, lsn=3)
    nd2 = NibbleData(nibbles2, bitwidth=10, msn=5, lsn=3)
    assert encode_frame(nd1, nd2) == [0, 0, 0, 3, 8, 4, 0, 0]


def test_encode_frame_two_signals_2():
    nibbles1 = encode(0x123, 10)  # 0x48C
    nibbles2 = encode(0x123, 10)  # 0x48C
    nd1 = NibbleData(nibbles1, bitwidth=10, msn=1, lsn=3)
    nd2 = NibbleData(nibbles2, bitwidth=10, msn=5, lsn=3)
    assert encode_frame(nd1, nd2) == [0, 4, 8, 0xF, 8, 4, 0, 0]


# Testing Decode starts here :


def test_decode_16bit_1():
    nibble_in = bytes([0, 8, 7, 0, 7, 0, 0, 0])
    assert decode(nibble_in, bitwidth=16, msn=1, lsn=4) == 0x8707


def test_decode_16bit_2():
    nibbles_in = bytes([0, 3, 0xA, 0xE, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, msn=1, lsn=4) == 0x3AE4


def test_decode_16bit_3():
    nibble_in = bytes([0, 1, 2, 3, 4, 5, 6, 0])
    assert decode(nibble_in, bitwidth=16, msn=3, lsn=6) == 0x3456


def test_decode_16bit_two_zero_padding():
    nibble_in = bytes([0, 0, 0, 4, 12, 0, 0, 0])
    assert decode(nibble_in, bitwidth=16, msn=1, lsn=4) == 76


def test_decode_16bit_two_zeroes_1():
    assert decode([0, 0, 1, 2, 3, 0, 0, 0], bitwidth=16, msn=1, lsn=4) == 0x123


def test_decode_16bit_two_zeroes_2():
    assert decode([0, 0, 0, 2, 3, 0, 0, 0], bitwidth=16, msn=1, lsn=4) == 0x23


def test_decode_ignores_upper_4_bits():
    assert decode([0, 0, 0x10, 2, 3, 0, 0, 0], bitwidth=16, msn=1, lsn=4) == 0x23


def test_decode_12bit_1():
    nibble_in = bytes([0, 1, 0, 0, 0, 0, 0, 0])
    assert decode(nibble_in, bitwidth=12, msn=1, lsn=3) == 0x100


def test_decode_12bit_2():
    nibble_in = bytes([0, 8, 7, 0, 7, 0, 0, 0])
    assert decode(nibble_in, bitwidth=12, msn=1, lsn=3) == 0x870


def test_decode_12bit_3():
    nibble_in = bytes([0, 4, 5, 6, 7, 0, 0, 0])
    assert decode(nibble_in, bitwidth=12, msn=2, lsn=4) == 0x567


def test_decode_12bit_4():
    nibble_in = bytes([0, 4, 5, 6, 7, 0, 0, 0])
    assert decode(nibble_in, bitwidth=12, msn=3, lsn=5) == 0x670


def test_decode_12bit_5():
    nibbles_in = bytes([0, 3, 0xA, 0xE, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, msn=2, lsn=4) == 0xAE4


def test_decode_8bit_1():
    nibbles_in = bytes([0, 3, 0xA, 0xE, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, msn=2, lsn=3) == 0xAE


# Test Cases for Decoding shared Nibbles start here :


def test_decode_10bit_1():
    nibbles_in = bytes([0, 1, 2, 3, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, bitwidth=10, msn=1, lsn=3) == 0x048


def test_decode_10bit_2():
    nibbles_in = bytes([0, 1, 2, 3, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, bitwidth=10, msn=2, lsn=4) == 0x08D


def test_decode_10bit_3():
    assert decode(nibbles=[0, 3, 0xA, 0xE, 0, 0, 0, 0], bitwidth=10, msn=1, lsn=3) == 0xEB


def test_decode_10bit_4():
    assert decode(nibbles=[0, 8, 9, 0xD, 0, 0, 0, 0], bitwidth=10, msn=1, lsn=3) == 0x227


def test_decode_10bit_5():
    nibble_in = bytes([0, 0xF, 3, 0, 4, 5, 6, 0])
    assert decode(nibble_in, bitwidth=10, msn=1, lsn=3) == 0x3CC


def test_decode_10bit_6():
    nibble_in = bytes([0, 3, 13, 8, 4, 5, 6, 0])
    assert decode(nibble_in, bitwidth=10, msn=1, lsn=3) == 0x0F6


def test_decode_14bit_1():
    assert decode(nibbles=[0, 1, 2, 3, 4, 0, 0, 0], bitwidth=14, msn=1, lsn=4) == 0x048D


def test_decode_14bit_2():
    assert decode(nibbles=[0, 0xD, 0xA, 5, 0xC, 0, 0, 0], bitwidth=14, msn=1, lsn=4) == 0x3697


def test_decode_14bit_3():
    assert decode(nibbles=[0, 0x8, 0x7, 0xF, 0xB, 0, 0, 0], bitwidth=14, msn=1, lsn=4) == 0x21FE


def test_decode_14bit_4():
    assert decode(nibbles=[0, 7, 0xB, 3, 0xE, 0, 0, 0], bitwidth=14, msn=1, lsn=4) == 0x1ECF


def test_decode_14bit_5():
    assert decode(nibbles=[0, 1, 8, 2, 4, 0, 0, 0], bitwidth=14, msn=1, lsn=4) == 0x0609


def test_decode_14bit_6():
    assert decode(nibbles=[0, 0xC, 4, 0xE, 9, 0, 0, 0], bitwidth=14, msn=1, lsn=4) == 0x313A


# Test Cases for Decoding High Speed Nibbles start here:

def test_high_speed_decode_12bit_1():
    assert decode(nibbles=[0, 7, 7, 7, 7, 0, 0, ], bitwidth=12, msn=1, lsn=4, nibblewidth=3) == 0xFFF


def test_high_speed_decode_12bit_2():
    assert decode(nibbles=[0, 4, 4, 3], bitwidth=12, msn=0, lsn=3, nibblewidth=3) == 0x123


def test_high_speed_decode_12bit_3():
    assert decode(nibbles=[0, 3, 5, 6, 7, 0, 0, ], bitwidth=12, msn=1, lsn=4, nibblewidth=3) == 0x777




