from mockhw import *


def test_create_conversion_1st_signal_1():
    sig_in = SignalDefinition(name="Temp_bosch", minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                              default=-21.671875)
    conv_function = create_conversion(sig_in)

    assert conv_function(sig_in.default) == [1, 9, 0xC]
    assert conv_function(23) == [3, 0, 1]
    assert conv_function(143.56) == [6, 0xC, 6]


def test_create_conversion_2nd_signal_1():
    sig_in = SignalDefinition(name="Temp_bosch", minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=5, lsn=3),
                              default=-21.671875)
    conv_function = create_conversion(sig_in)

    assert conv_function(sig_in.default) == [0xC, 9, 1]
    assert conv_function(23) == [1, 0, 3]
    assert conv_function(143.56) == [6, 0xC, 6]


def test_make_data_from_sigobj_1st_signal():
    sig_in = SignalDefinition(name="Temp_bosch", minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                              default=-21.671875)
    row_in = (100, sig_in.default)

    assert make_data(row=row_in, conversion=sig_in.encode_frame) == (100, [0, 1, 9, 0xC, 0, 0, 0, 0])


