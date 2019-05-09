import pytest
from encode_decode import *


def test_encode_16bit_no_zero_padding():
    expected_nibble = [8, 7, 0, 7]
    assert encode(raw_value=0x8707, bitwidth=16) == expected_nibble


def test_encode_frame_16bit_1():
    assert encode_frame(raw_value=0x8707, bitwidth=16, msn=1, lsn=4) == [0, 8, 7, 0, 7, 0, 0, 0]


def test_encode_frame_16bit_2():
    assert encode_frame(raw_value=0x8707, bitwidth=16, msn=2, lsn=5) == [0, 0, 8, 7, 0, 7, 0, 0]


def test_encode_frame_16bit_3():
    assert encode_frame(raw_value=0x8707, bitwidth=16, msn=3, lsn=6) == [0, 0, 0, 8, 7, 0, 7, 0]


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


def test_encode_bitwidth_exceed():
    with pytest.raises(ValueError) as exc:
        encode(raw_value=0x15F4, bitwidth=8)   # 5620
        assert "doesn't fit bitwidth" in str(exc)


def test_decode_16bit_1():
    nibble_in = bytes([0, 8, 7, 0, 7, 0, 0, 0])
    assert decode(nibble_in, bitwidth=16, msn=1, lsn=4) == 0x8707


def test_decode_16bit_two_zero_padding():
    nibble_in = bytes([0, 0, 0, 4, 12, 0, 0, 0])
    assert decode(nibble_in, bitwidth=16, msn=1, lsn=4) == 76


def test_decode16bit_two_zeroes_1():
    assert decode([0, 0, 1, 2, 3, 0, 0, 0], bitwidth=16, msn=1, lsn=4) == 0x123


def test_decode16bit_two_zeroes_2():
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


def test_decode_16bit_5():
    nibble_in = bytes([0, 1, 2, 3, 4, 5, 6, 0])
    assert decode(nibble_in, bitwidth=16, msn=3, lsn=6) == 0x3456


def test_decode16bit_1():
    nibbles_in = bytes([0, 3, 0xA, 0xE, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, msn=1, lsn=4) == 0x3AE4


def test_decode12bit_1():
    nibbles_in = bytes([0, 3, 0xA, 0xE, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, msn=2, lsn=4) == 0xAE4

def test_decode8bit_1():
    nibbles_in = bytes([0, 3, 0xA, 0xE, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, msn=2, lsn=3) == 0xAE


def test_decode_10bit_1():
    nibbles_in = bytes([0, 1, 2, 3, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, bitwidth=10, msn=1, lsn=3) == 0x048


def test_encode_10bit_1():
    assert encode_frame(nibble_data_1=NibbleData(nibbles=[0, 1, 2, 0],
                                                 bitwidth=10, msn=1, lsn=3) == [0, 1, 2, 0, 0, 0, 0, 0 ])


def test_decode_10bit_2():
    nibbles_in = bytes([0, 1, 2, 3, 4, 2, 1, 0xF ])
    assert decode(nibbles_in, bitwidth=10, msn=2, lsn=4) == 0x08D


def test_encode_10bit_2():
    assert encode_frame(raw_value=0x08D, bitwidth=10, msn=2, lsn=4) == [0, 2, 3, 4, 0, 0, 0, 0]


def test_decode_10bit_3():
    assert decode(nibbles=[0, 3, 0xA, 0xE, 0, 0, 0, 0], bitwidth=10, msn=1, lsn=3) == 0xEB


def test_encode_10bit_3():
    assert encode_frame(raw_value=0xEB, bitwidth=10, msn=1, lsn=3) == [0, 3, 0xA, 0xC, 0, 0, 0, 0]


def test_decode_10bit_4():
    assert decode(nibbles=[0, 8, 9, 0xD, 0, 0, 0, 0], bitwidth=10, msn=1, lsn=3) == 0x227


def test_encode_10bit_4():
    assert encode_frame(raw_value=0x227, bitwidth=10, msn=1, lsn=3) == [0, 8, 9, 0xC, 0, 0, 0, 0]


def test_decode_10bit_5():
    nibble_in = bytes([0, 0xF, 3, 0, 4, 5, 6, 0])
    assert decode(nibble_in, bitwidth=10, msn=1, lsn=3) == 0x3CC


def test_encode_10bit_5():
    assert encode_frame(raw_value=0x3CC, bitwidth=10, msn=1, lsn=3) == [0, 0xF, 3, 0, 0, 0, 0, 0]


def test_decode_10bit_6():
    nibble_in = bytes([0, 3, 13, 8, 4, 5, 6, 0])
    assert decode(nibble_in, bitwidth=10, msn=1, lsn=3) == 0x0F6


def test_encode_10bit_6():
    assert encode_frame(raw_value=0x0F6, bitwidth=10, msn=1, lsn=3) == [0, 3, 13, 8, 0, 0, 0, 0]


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


def test_encode_14bit_1():
    assert encode_frame(raw_value=0x48D, bitwidth=14, msn=1, lsn=4) == [0, 1, 2, 3, 4, 0, 0, 0]


def test_encode_14bit_2():
    assert encode_frame(raw_value=0x3697, bitwidth=14, msn=1, lsn=4) == [0, 0xD, 0xA, 5, 0xC, 0, 0, 0]


def test_encode_14bit_3():
    assert encode_frame(raw_value=0x21FE, bitwidth=14, msn=1, lsn=4) == [0, 8, 7, 15, 8, 0, 0, 0]


def test_encode_14bit_4():
    assert encode_frame(raw_value=0x1ECF, bitwidth=14, msn=1, lsn=4) == [0, 7, 0xB, 3, 0xC, 0, 0, 0]


def test_encode_14bit_5():
    assert encode_frame(raw_value=0x0609, bitwidth=14, msn=1, lsn=4) == [0, 1, 8, 2, 4, 0, 0, 0]


def test_encode_14bit_6():
    assert encode_frame(raw_value=0x313A, bitwidth=14, msn=1, lsn=4) == [0, 0xC, 4, 0xE, 8, 0, 0, 0]


def test_encode_frame_12bit_1():
    assert encode_frame(raw_value=0x3AE, bitwidth=12, msn=1, lsn=3) == [0, 3, 0xA, 0xE, 0, 0, 0, 0]




