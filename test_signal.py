from signaldef import *


def test_encode_frame_from_phy_value_as_1st_signal():
    sig_in = SignalDefinition(name="Temp_bosch", minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                              default=-21.671875)

    assert sig_in.encode_frame(phy_value=sig_in.default) == [0, 1, 9, 0xC, 0, 0, 0, 0]

    assert sig_in.encode_frame(phy_value=230.56789) == [0, 9, 7, 0xE, 0, 0, 0, 0]
    assert sig_in.encode_frame(phy_value=230.56) == [0, 9, 7, 0xE, 0, 0, 0, 0]
    assert sig_in.encode_frame(phy_value=230.5) == [0, 9, 7, 0xD, 0, 0, 0, 0]

    assert sig_in.encode_frame(phy_value=130.10) == [0, 6, 5, 0xA, 0, 0, 0, 0]
    assert sig_in.encode_frame(phy_value=-40.15) == [0, 1, 0, 8, 0, 0, 0, 0]


def test_decode_frame_to_phy_value_for_signal_1():
    sig_in = SignalDefinition(name="Temp_bosch", minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                              default=-21.671875)

    assert sig_in.decode_frame(dataframe=[0, 1, 9, 0xC, 0, 0, 0, 0]) == -21.65
    assert sig_in.decode_frame(dataframe=[0, 9, 7, 0xE, 0, 0, 0, 0]) == 230.6
    assert sig_in.decode_frame(dataframe=[0xF, 9, 7, 0xE, 0xF, 0xF, 0xF, 0xF]) == 230.6
    assert sig_in.decode_frame(dataframe=[0xF, 9, 7, 0xD, 0xF, 0xF, 0xF, 0xF]) == 230.475
    assert sig_in.decode_frame(dataframe=[0, 6, 5, 0xA, 0, 0, 0, 0]) == 130.10
    assert sig_in.decode_frame(dataframe=[0xF, 1, 0, 8, 0xF, 0xF, 0xF, 0xF]) == -40.15
