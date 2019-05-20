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


sig_pressure_12bt_smplx_2 = SignalDefinition(
    name="Pressure 2", minimum='-1', maximum='13', unit='bar',
    physical=spec_conti(minimum=-1, maximum=13, resolution=(1/291.928), bitwidth=12, errorcodes={}, offset=1),
    encoding=SignalEncoding(bitwidth=12, msn=6, lsn=4),
    default=1.671875
)



def test_dataframe_one_signal_16_bit():
    df_obj_test = DataFrame(signal_1=sig_tmp_16bt)

    assert df_obj_test.encode_frame() == [0, 8, 7, 0, 7, 0, 0, 0]


def test_dataframe_one_signal_12_bit():
    df_obj_test = DataFrame(signal_1=sig_pressure_12bt_smplx_1)

    assert df_obj_test.encode_frame() == [0, 9, 2, 11, 0, 0, 0, 0]


def test_dataframe_two_12_12_bit_same_signal():
    df_obj_test = DataFrame(signal_1=sig_pressure_12bt_smplx_1, signal_2=sig_pressure_12bt_smplx_2)

    assert df_obj_test.encode_frame() == [0, 9, 2, 11, 11, 2, 9, 0]
