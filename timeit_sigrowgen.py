import timeit

setup_code = """
from signaldef import SignalDefinition, SignalEncoding, spec_conti
from mockhw_ascii import signal_row_generator_1, signal_row_generator

sig_in_1st = SignalDefinition(name="Supply Voltage", minimum='0', maximum='40.75', unit='V',
                              physical=spec_conti(minimum=0, maximum=40.75,
                                                  resolution=0.16, bitwidth=8, errorcodes={}, offset=0),
                              encoding=SignalEncoding(bitwidth=8, msn=1, lsn=2),
                              default=5.671875)
                              
sig_in_2nd = SignalDefinition(name="Concentration", minimum='-10', maximum='100', unit='%',
                              physical=spec_conti(minimum=-10, maximum=100,
                                                  resolution=0.01, bitwidth=16, errorcodes={}, offset=-10),
                              encoding=SignalEncoding(bitwidth=16, msn=6, lsn=3),
                              default=25.46)

input_src = [{'time': 0.123, 'Concentration': 80.0, 'Supply Voltage': 15.0, 'Runtime 1': '8.0'},
             {'time': 0.153, 'Concentration': 80.0, 'Supply Voltage': 12.0, 'Runtime 1': '13.0'},
             {'time': 0.223, 'Concentration': 70.0, 'Supply Voltage': 12.0, 'Runtime 1': '23.0'},
             {'time': 0.363, 'Concentration': 80.0, 'Supply Voltage': 15.0, 'Runtime 1': '8.0'},
             {'time': 0.523, 'Concentration': 90.0, 'Supply Voltage': 18.0, 'Runtime 1': '5.0'},
             {'time': 0.703, 'Concentration': 90.0, 'Supply Voltage': 18.0,'Runtime 1': '8.0'},
             {'time': 0.823, 'Concentration': 60.0, 'Supply Voltage': 12.0,'Runtime 1': '8.0'}]
"""


def compute_time_with_2signal_func1():
    test_code1 = "list(signal_row_generator_1(input_src, sig_in_1st, sig_in_2nd))"
    exec_time = timeit.timeit(stmt=test_code1, setup=setup_code, number=10000)
    print('Function1 with two siganl -  execution time: {}'.format(exec_time))


def compute_time_with_2signal_func2():
    test_code2 = "list(signal_row_generator(input_src, sig_in_1st, sig_in_2nd))"
    exec_time = timeit.timeit(stmt=test_code2, setup=setup_code, number=10000)
    print('Function2 with two siganl - execution time: {}'.format(exec_time))


if __name__ == '__main__':
    compute_time_with_2signal_func1()
    compute_time_with_2signal_func2()







