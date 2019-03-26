from signalrow_valid import *
from signaldef import *

sig_obj1 = SignalDefinition(name="Temperature_D", minimum="-40", maximum="165", unit="°C",
                                          physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16))
sig_obj2 = SignalDefinition(name="Temperature_K", minimum="233.98", maximum="438.35",
                                          unit="Kelvin",
                                          physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16))



if __name__ == '__main__':
    # sd1 = get_signal_details(sig_obj1)
    # print(sd1.name)
    # sd2 = get_signal_details(sig_obj2)
    # #print(sd1.name)
    # print(sd2.name)
    sd1 = sig_obj1.get_signal_details()
    #print(sd1.name)
    sd2 = sig_obj2.get_signal_details()
    print(sd1.name)
    print(sd2.name)