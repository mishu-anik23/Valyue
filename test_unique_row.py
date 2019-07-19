from signaldef import *
from unique_row import *


sig_in_1st = SignalDefinition(name="Concentration", minimum='-10', maximum='100', unit='%',
                              physical=spec_conti(minimum=-10, maximum=100,
                                                  resolution=0.01, bitwidth=16, errorcodes={}, offset=-10),
                              encoding=SignalEncoding(bitwidth=16, msn=6, lsn=3),
                              default=25.46)

sig_in_2nd = SignalDefinition(name="Supply Voltage", minimum='0', maximum='40.75', unit='V',
                              physical=spec_conti(minimum=0, maximum=40.75,
                                                  resolution=0.16, bitwidth=8, errorcodes={}, offset=0),
                              encoding=SignalEncoding(bitwidth=8, msn=1, lsn=2),
                              default=5.671875)


fake_src_in_1_signal = [{'time': 0.123, 'Concentration': 80.0},
                        {'time': 0.153, 'Concentration': 80.0},
                        {'time': 0.223, 'Concentration': 70.0},
                        {'time': 0.363, 'Concentration': 80.0},
                        {'time': 0.523, 'Concentration': 90.0},
                        {'time': 0.703, 'Concentration': 90.0},
                        {'time': 0.823, 'Concentration': 60.0}]

fake_src_in_2_signal = [{'time': 0.123, 'Concentration': 80.0, 'Supply Voltage': 15.0},
                        {'time': 0.153, 'Concentration': 80.0, 'Supply Voltage': 12.0},
                        {'time': 0.223, 'Concentration': 70.0, 'Supply Voltage': 12.0},
                        {'time': 0.363, 'Concentration': 80.0, 'Supply Voltage': 15.0},
                        {'time': 0.523, 'Concentration': 90.0, 'Supply Voltage': 18.0},
                        {'time': 0.703, 'Concentration': 90.0, 'Supply Voltage': 18.0},
                        {'time': 0.823, 'Concentration': 60.0, 'Supply Voltage': 12.0}]


def fake_source_generator(source):
    for row in source:
        yield row


def test_unique_rows_with_one_signal_return_unique_elements():
    fake_gens = fake_source_generator(source=fake_src_in_1_signal)
    urows = unique_rows(source=fake_gens, signal1=sig_in_1st)

    assert urows[0] == {'time': 0.123, 'Concentration': 80.0}
    assert urows[1] == {'time': 0.223, 'Concentration': 70.0}
    assert urows[2] == {'time': 0.363, 'Concentration': 80.0}
    assert urows[3] == {'time': 0.523, 'Concentration': 90.0}
    assert urows[4] == {'time': 0.823, 'Concentration': 60.0}


def test_unique_rows_with_two_signal_return_unique_elements():
    fake_gens = fake_source_generator(source=fake_src_in_2_signal)
    urows = unique_rows(source=fake_gens, signal1=sig_in_1st, signal2=sig_in_2nd)

    assert urows[0] == {'time': 0.123, 'Concentration': 80.0, 'Supply Voltage': 15.0}
    assert urows[1] == {'time': 0.153, 'Concentration': 80.0, 'Supply Voltage': 12.0}
    assert urows[2] == {'time': 0.223, 'Concentration': 70.0, 'Supply Voltage': 12.0}
    assert urows[2] == {'time': 0.363, 'Concentration': 80.0}
    assert urows[3] == {'time': 0.523, 'Concentration': 90.0}
    assert urows[4] == {'time': 0.823, 'Concentration': 60.0}