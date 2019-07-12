from signaldef import *
from mockhw_ascii import *


def dict_generator(dicts):
    for dct in dicts:
        yield dct


def test_get_value_from_fake_source():
    dicts_in = [{'time': '0.00006', 'Channel 1': 5.01062},
                {'time': '0.00008', 'Channel 1': 5.01062},
                {'time': '0.00010', 'Channel 1': 5.01414},
                {'time': '0.00012', 'Channel 1': 5.00710}]

    sig_in = SignalDefinition(name="Voltage", minimum='0', maximum='40.75', unit='v',
                                           physical=Physical(x1=0, x2=40.75, y1=0, y2=255, bitwidth=8),
                                           encoding=SignalEncoding(bitwidth=8, msn=1, lsn=2), default=-0)

    mockhw = MockHw(source=dict_generator(dicts_in), signal=sig_in)

    assert mockhw.get_value_from_row() == ('0.00006', [0, 1, 0xF, 0, 0, 0, 0, 0])
    assert mockhw.get_value_from_row() == ('0.00008', [0, 1, 0xF, 0, 0, 0, 0, 0])

    assert mockhw.get_value_from_row() == ('0.00012', [0, 1, 0xF, 0, 0, 0, 0, 0])



