from signaldef import SignalEncoding


def test_encode_decode_16_bit_as_1st_signal():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=1, lsn=4)

    assert enc_obj_test.encode(raw_value=0x8707) == [8, 7, 0, 7]
    assert enc_obj_test.decode(dataframe=[0, 8, 7, 0, 7, 0, 0, 0]) == 0x8707


def test_encode_frame_16_bit_as_1st_signal():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=1, lsn=4)

    assert enc_obj_test.encode_frame(raw=0x8706) == [0, 8, 7, 0, 6, 0, 0, 0]


def test_encode_decode_16_bit_as_2nd_signal():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=6, lsn=3)

    assert enc_obj_test.encode(raw_value=0x8706) == [6, 0, 7, 8]
    assert enc_obj_test.decode(dataframe=[0xF, 0xF, 0xF, 6, 0, 7, 8, 0xF]) == 0x8706


def test_encode_frame_16_bit_as_2nd_signal():
    enc_obj_test = SignalEncoding(bitwidth=16, msn=6, lsn=3)

    assert enc_obj_test.encode_frame(raw=0x8706) == [0, 0, 0, 6, 0, 7, 8, 0]


def test_encode_decode_12_bit_as_1st_signal():
    enc_obj_test = SignalEncoding(bitwidth=12, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0x872) == [8, 7, 2]
    assert enc_obj_test.decode(dataframe=[0xF, 8, 7, 2, 0xC, 8, 0, 0xF]) == 0x872


def test_encode_frame_12_bit_as_1st_signal():
    enc_obj_test = SignalEncoding(bitwidth=12, msn=1, lsn=3)

    assert enc_obj_test.encode_frame(raw=0x872) == [0, 8, 7, 2, 0, 0, 0, 0]


def test_encode_decode_12_bit_as_2nd_signal():
    enc_obj_test = SignalEncoding(bitwidth=12, msn=5, lsn=3)

    assert enc_obj_test.encode(raw_value=0x871) == [1, 7, 8]
    assert enc_obj_test.decode(dataframe=[0, 0xF, 0, 1, 7, 8, 0xC, 0xD]) == 0x871


def test_encode_frame_12_bit_as_2nd_signal():
    enc_obj_test = SignalEncoding(bitwidth=12, msn=5, lsn=3)

    assert enc_obj_test.encode_frame(raw=0x871) == [0, 0, 0, 1, 7, 8, 0, 0]


def test_encode_decode_10_bit_1st_signal_1():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0xEB) == [3, 0xA, 0xC]
    assert enc_obj_test.encode(raw_value=0x97E) == [2, 0x5, 0xF]
    assert enc_obj_test.decode(dataframe=[0, 3, 0xA, 0xC, 0, 0, 0, 0]) == 0xEB


def test_encode_frame_10_bit_as_1st_signal_1():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test.encode_frame(raw=0xEB) == [0, 3, 0xA, 0xC, 0, 0, 0, 0]


def test_encode_decode_10_bit_2nd_signal_1():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=6, lsn=4)
    assert enc_obj_test.encode(raw_value=0x2EB) == [3, 0xA, 0xB]
    assert enc_obj_test.decode(dataframe=[0xF, 0xF, 0xF, 0xB, 0xF, 0xA, 0xB, 0xF]) == 0x2EB


def test_encode_frame_10_bit_as_2nd_signal_1():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=6, lsn=4)
    assert enc_obj_test.encode_frame(raw=0xEB) == [0, 0, 0, 0, 0x3, 0xA, 0x3, 0]


def test_encode_decode_10_bit_1st_signal_2():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test.encode(raw_value=0x227) == [8, 9, 0xC]
    assert enc_obj_test.decode(dataframe=[0, 8, 9, 0xC, 0, 0, 0, 0]) == 0x227


def test_encode_frame_10_bit_as_1st_signal_2():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=1, lsn=3)

    assert enc_obj_test.encode_frame(raw=0x227) == [0, 8, 9, 0xC, 0, 0, 0, 0]


def test_encode_decode_10_bit_2nd_signal_2():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=4, lsn=2)

    assert enc_obj_test.encode(raw_value=0x227) == [3, 9, 8]
    assert enc_obj_test.decode(dataframe=[0, 2, 3, 9, 8, 6, 9, 5]) == 0x227


def test_encode_frame_10_bit_as_2nd_signal_2():
    enc_obj_test = SignalEncoding(bitwidth=10, msn=4, lsn=2)

    assert enc_obj_test.encode_frame(raw=0x227) == [0, 0, 3, 9, 8, 0, 0, 0]


