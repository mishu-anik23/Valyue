import pytest
from signaldef import SignalEncoding


def test_encode_decode_16_bit():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=0, lsn=3)

    assert enc_obj_test.encode(raw_value=0x8707) == [8, 7, 0, 7]
    assert enc_obj_test.decode(nibbles=[8, 7, 0, 7]) == 0x8707


def test_encode_decode_12_bit():
    enc_obj_test = SignalEncoding(bitwidth=12, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0x870) == [8, 7, 0]
    assert enc_obj_test.decode(nibbles=[0, 8, 7, 0, 0, 0, 0, 0]) == 0x870


def test_encode_decode_10_bit_1():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)
    dec_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0xEB) == [3, 0xA, 0xC]
    assert dec_obj_test.decode(nibbles=[0, 3, 0xA, 0xE, 0, 0, 0, 0]) == 0xEB


def test_encode_decode_10_bit_2():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0x227) == [8, 9, 0xC]
    assert enc_obj_test.decode(nibbles=[0, 8, 9, 0xD, 0, 0, 0, 0]) == 0x227