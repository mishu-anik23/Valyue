from signaldef import *

sig_in_1st = SignalDefinition(name="Temp_bosch", minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                              default=-21.671875)

sig_in_2nd = SignalDefinition(name="Temp_conti", minimum='-40', maximum='165', unit='C',
                              physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16),
                              encoding=SignalEncoding(bitwidth=16, msn=6, lsn=3),
                              default=25.46)


def test_encode_frame_from_phy_as_1st_signal():
    assert sig_in_1st.encode_frame(phy_value=sig_in_1st.default) == [0, 1, 9, 0xC, 0, 0, 0, 0]

    assert sig_in_1st.encode_frame(phy_value=230.56789) == [0, 9, 7, 0xE, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=230.56) == [0, 9, 7, 0xE, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=230.5) == [0, 9, 7, 0xD, 0, 0, 0, 0]

    assert sig_in_1st.encode_frame(phy_value=130.10) == [0, 6, 5, 0xA, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=431.10) == [0, 0xF, 0xC, 2, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=438.61) == [0, 0xF, 0xF, 0xE, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=438.66) == [0, 0xF, 0xF, 0xE, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=438.67) == [0, 0xF, 0xF, 0xF, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=1436.69) == [0, 0xF, 0xF, 0xF, 0, 0, 0, 0]

    assert sig_in_1st.encode_frame(phy_value=-40.15) == [0, 1, 0, 8, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=-66.15) == [0, 0, 3, 8, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=-73.05) == [0, 0, 0, 1, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=-73.08) == [0, 0, 0, 1, 0, 0, 0, 0]
    assert sig_in_1st.encode_frame(phy_value=-73.09) == [0, 0, 0, 0, 0, 0, 0, 0]


def test_encode_frame_from_raw_as_1st_signal():
    assert sig_in_1st.encoding.encode_frame(raw=0x97E) == [0, 9, 7, 0xE, 0, 0, 0, 0]
    assert sig_in_1st.encoding.encode_frame(raw=0x65A) == [0, 6, 5, 0xA, 0, 0, 0, 0]
    assert sig_in_1st.encoding.encode_frame(raw=0xFEF) == [0, 0xF, 0xE, 0xF, 0, 0, 0, 0]
    assert sig_in_1st.encoding.encode_frame(raw=0xFFF) == [0, 0xF, 0xF, 0xF, 0, 0, 0, 0]

    assert sig_in_1st.encoding.encode_frame(raw=0x108) == [0, 1, 0, 8, 0, 0, 0, 0]
    assert sig_in_1st.encoding.encode_frame(raw=0x038) == [0, 0, 3, 8, 0, 0, 0, 0]
    assert sig_in_1st.encoding.encode_frame(raw=0x001) == [0, 0, 0, 1, 0, 0, 0, 0]


def test_encode_frame_from_phy_shared_nibble_as_1st_signal():
    sig_in_shared = SignalDefinition(name="Temp_bosch", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=10),
                                  encoding=SignalEncoding(bitwidth=10, msn=1, lsn=3),
                                  default=-21.671875)

    assert sig_in_shared.encode_frame(phy_value=sig_in_shared.default) == [0, 6, 7, 0, 0, 0, 0, 0]

    assert sig_in_shared.encode_frame(phy_value=230.56789) == [0, 0xF, 0xF, 0xC, 0, 0, 0, 0]

    assert sig_in_shared.encode_frame(phy_value=52.10) == [0, 0xF, 0xA, 8, 0, 0, 0, 0]
    assert sig_in_shared.encode_frame(phy_value=54.55) == [0, 0xF, 0xF, 8, 0, 0, 0, 0]
    assert sig_in_shared.encode_frame(phy_value=54.66) == [0, 0xF, 0xF, 8, 0, 0, 0, 0]
    assert sig_in_shared.encode_frame(phy_value=54.67) == [0, 0xF, 0xF, 0xC, 0, 0, 0, 0]
    assert sig_in_shared.encode_frame(phy_value=130.10) == [0, 0xF, 0xF, 0xC, 0, 0, 0, 0]

    assert sig_in_shared.encode_frame(phy_value=-40.15) == [0, 4, 2, 0, 0, 0, 0, 0]
    assert sig_in_shared.encode_frame(phy_value=-66.15) == [0, 0, 0xE, 0, 0, 0, 0, 0]
    assert sig_in_shared.encode_frame(phy_value=-73.05) == [0, 0, 0, 4, 0, 0, 0, 0]
    assert sig_in_shared.encode_frame(phy_value=-73.08) == [0, 0, 0, 4, 0, 0, 0, 0]
    assert sig_in_shared.encode_frame(phy_value=-73.09) == [0, 0, 0, 0, 0, 0, 0, 0]


def test_encode_frame_from_phy_value_as_2nd_signal():
    assert sig_in_2nd.encode_frame(phy_value=sig_in_2nd.default) == [0, 0, 0, 0xC, 0xB, 0, 2, 0]

    assert sig_in_2nd.encode_frame(phy_value=137.56789) == [0, 0, 0, 0xA, 0xC, 8, 5, 0]
    assert sig_in_2nd.encode_frame(phy_value=137.56) == [0, 0, 0, 9, 0xC, 8, 5, 0]
    assert sig_in_2nd.encode_frame(phy_value=137.5) == [0, 0, 0, 1, 0xC, 8, 5, 0]

    assert sig_in_2nd.encode_frame(phy_value=165) == [0, 0, 0, 1, 8, 6, 6, 0]
    assert sig_in_2nd.encode_frame(phy_value=165.15) == [0, 0, 0, 4, 9, 6, 6, 0]
    assert sig_in_2nd.encode_frame(phy_value=457.15) == [0, 0, 0, 4, 9, 8, 0xF, 0]
    assert sig_in_2nd.encode_frame(phy_value=471.55) == [0, 0, 0, 7, 0xC, 0xF, 0xF, 0]
    assert sig_in_2nd.encode_frame(phy_value=471.85) == [0, 0, 0, 0xE, 0xE, 0xF, 0xF, 0]
    assert sig_in_2nd.encode_frame(phy_value=471.98) == [0, 0, 0, 0xE, 0xF, 0xF, 0xF, 0]
    assert sig_in_2nd.encode_frame(phy_value=471.99) == [0, 0, 0, 0xF, 0xF, 0xF, 0xF, 0]
    assert sig_in_2nd.encode_frame(phy_value=1171.98) == [0, 0, 0, 0xF, 0xF, 0xF, 0xF, 0]

    assert sig_in_2nd.encode_frame(phy_value=-40) == [0, 0, 0, 1, 0, 0, 0, 0]
    assert sig_in_2nd.encode_frame(phy_value=-40.15) == [0, 0, 0, 0, 0, 0, 0, 0]


def test_encode_frame_from_raw_value_as_2nd_signal():
    assert sig_in_2nd.encoding.encode_frame(raw=0x20BC) == [0, 0, 0, 0xC, 0xB, 0, 2, 0]
    assert sig_in_2nd.encoding.encode_frame(raw=0x58CA) == [0, 0, 0, 0xA, 0xC, 8, 5, 0]
    assert sig_in_2nd.encoding.encode_frame(raw=0x6681) == [0, 0, 0, 1, 8, 6, 6, 0]
    assert sig_in_2nd.encoding.encode_frame(raw=0xF894) == [0, 0, 0, 4, 9, 8, 0xF, 0]
    assert sig_in_2nd.encoding.encode_frame(raw=0x0001) == [0, 0, 0, 1, 0, 0, 0, 0]


def test_encode_frame_from_phy_value_shared_nibble_as_2nd_signal():
    sig_in = SignalDefinition(name="Temp_conti", minimum='-40', maximum='165', unit='C',
                                  physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=14),
                                  encoding=SignalEncoding(bitwidth=14, msn=6, lsn=3),
                                  default=25.46)

    assert sig_in.encode_frame(phy_value=sig_in.default) == [0, 0, 0, 0xC, 0xB, 0, 2, 0]

    assert sig_in.encode_frame(phy_value=137.56789) == [0, 0, 0, 0xA, 0xC, 8, 5, 0]
    assert sig_in.encode_frame(phy_value=137.56) == [0, 0, 0, 9, 0xC, 8, 5, 0]
    assert sig_in.encode_frame(phy_value=137.5) == [0, 0, 0, 1, 0xC, 8, 5, 0]

    assert sig_in.encode_frame(phy_value=165) == [0, 0, 0, 1, 8, 6, 6, 0]
    assert sig_in.encode_frame(phy_value=165.15) == [0, 0, 0, 4, 9, 6, 6, 0]
    assert sig_in.encode_frame(phy_value=457.15) == [0, 0, 0, 4, 9, 8, 0xF, 0]
    assert sig_in.encode_frame(phy_value=471.55) == [0, 0, 0, 7, 0xC, 0xF, 0xF, 0]
    assert sig_in.encode_frame(phy_value=471.85) == [0, 0, 0, 0xE, 0xE, 0xF, 0xF, 0]
    assert sig_in.encode_frame(phy_value=471.98) == [0, 0, 0, 0xE, 0xF, 0xF, 0xF, 0]
    assert sig_in.encode_frame(phy_value=471.99) == [0, 0, 0, 0xF, 0xF, 0xF, 0xF, 0]
    assert sig_in.encode_frame(phy_value=1171.98) == [0, 0, 0, 0xF, 0xF, 0xF, 0xF, 0]

    assert sig_in.encode_frame(phy_value=-40) == [0, 0, 0, 1, 0, 0, 0, 0]
    assert sig_in.encode_frame(phy_value=-40.15) == [0, 0, 0, 0, 0, 0, 0, 0]


def test_decode_frame_to_phy_value_for_signal_1():

    assert sig_in_1st.decode_frame(dataframe=[0, 1, 9, 0xC, 0, 0, 0, 0]) == -21.65
    assert sig_in_1st.decode_frame(dataframe=[0, 9, 7, 0xE, 0, 0, 0, 0]) == 230.6
    assert sig_in_1st.decode_frame(dataframe=[0xF, 9, 7, 0xD, 0xF, 0xF, 0xF, 0xF]) == 230.475
    assert sig_in_1st.decode_frame(dataframe=[0, 6, 5, 0xA, 0, 0, 0, 0]) == 130.10
    assert sig_in_1st.decode_frame(dataframe=[0xF, 1, 0, 8, 0xF, 0xF, 0xF, 0xF]) == -40.15
