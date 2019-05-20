from dataframe import *

sig_tmp_16bt = SignalDefinition(name="Temp", minimum='-40', maximum='165', unit='C',
                               physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16),
                               encoding=SignalEncoding(bitwidth=16, msn=1, lsn=4),
                               default=230.046875)

sig_pressure_12bt_smplx_1 = SignalDefinition(
    name="Pressure 1", minimum='-1', maximum='13', unit='bar',
    physical=spec_conti(minimum=-1, maximum=13, resolution=(1/291.928), bitwidth=12, errorcodes={}, offset=1),
    encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
    default=10.671875
)


sig_tmp_bosch_12bt = SignalDefinition(
    name="Temp", minimum='-40.15', maximum='130.10', unit='C',
    physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
    encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
    default=-21.671875)



def test_encode_dataframe_one_signal_16_bit():
    df_obj_test = DataFrame(signal_1=sig_tmp_16bt)
    assert df_obj_test.signal_1.physical.phy2raw(df_obj_test.signal_1.default) == 0x8707

    assert df_obj_test.encode_frame() == [0, 8, 7, 0, 7, 0, 0, 0]


def test_encode_dataframe_one_signal_12_bit():
    df_obj_test = DataFrame(
        signal_1=SignalDefinition(name="Temp", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                                  default=-21.671875)
    )
    assert df_obj_test.encode_frame() == [0, 1, 9, 0xC, 0, 0, 0, 0]


def test_encode_dataframe_one_signal_12_bit_smplx_conti_spec():
    df_obj_test = DataFrame(signal_1=sig_pressure_12bt_smplx_1)

    assert df_obj_test.encode_frame() == [0, 0xD, 4, 0xF, 0, 0, 0, 0]


def test_encode_dataframe_one_12_bit_smplx_conti_one_12_bit_bosch_temp():
    sig_tmp_bosch_12bt.encoding.msn = 6
    sig_tmp_bosch_12bt.encoding.lsn = 4
    df_obj_test = DataFrame(signal_1=sig_pressure_12bt_smplx_1, signal_2=sig_tmp_bosch_12bt)

    assert df_obj_test.encode_frame() == [0, 0xD, 4, 0xF, 0xC, 9, 1, 0]


def test_encode_dataframe_two_12_12_bit_same_signal():
    df_obj_test = DataFrame(
        signal_1=SignalDefinition(name="Temp", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                                  default=-21.671875),
        signal_2=SignalDefinition(name="Temp", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=6, lsn=4),
                                  default=-21.671875)
    )
    assert df_obj_test.encode_frame() == [0, 1, 9, 0xC, 0xC, 9, 1, 0]


def test_encode_dataframe_two_10_10_bit_shared_nibble():
    sig_tmp_bosch_12bt.encoding.msn = 5
    sig_tmp_bosch_12bt.encoding.lsn = 3
    df_obj_test = DataFrame(signal_1=sig_pressure_12bt_smplx_1, signal_2=sig_tmp_bosch_12bt)

    assert df_obj_test.encode_frame() == [0, 0xD, 4, 0xC, 9, 1, 0, 0]


def test_decode_dataframe_one_signal_16_bit():
    df_obj_test = DataFrame(signal_1=sig_tmp_16bt)

    assert df_obj_test.decode_frame() == (0x8707, None)


def test_decode_dataframe_one_signal_12_bit():
    df_obj_test = DataFrame(
        signal_1=SignalDefinition(name="Temp", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                                  default=-21.671875)
    )

    assert df_obj_test.dataframe == [0, 1, 9, 0xC, 0, 0, 0, 0]

    assert df_obj_test.decode_frame() == (0x19C, None)


def test_decode_dataframe_two_12_12_bit_same_signal():
    df_obj_test = DataFrame(
        signal_1=SignalDefinition(name="Temp", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                                  default=-21.671875),
        signal_2=SignalDefinition(name="Temp", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=6, lsn=4),
                                  default=-21.671875)
    )

    assert df_obj_test.dataframe == [0, 1, 9, 0xC, 0xC, 9, 1, 0]

    assert df_obj_test.decode_frame() == (0x19C, 0x19C)
