from signaldef import *


class DataFrame:
    """
    Constructs Nibble data of 1 or 2 signal (if present) in a SENT data frame.
    """
    def __init__(self, signal_1, signal_2=None):
        self.signal_1 = signal_1
        self.signal_2 = signal_2
        self.data_1 = self.get_nibbles()[0]
        if signal_2 is not None:
            self.data_2 = self.get_nibbles()[1]

        self.dataframe = self.encode_frame()

    def convert_raw(self):
        if self.signal_2 is not None:
            return (self.signal_1.physical.phy2raw(self.signal_1.default),
                    self.signal_2.physical.phy2raw(self.signal_2.default))
        else:
            return self.signal_1.physical.phy2raw(self.signal_1.default), None

    def get_nibbles(self):
        raw_value_1, raw_value_2 = self.convert_raw()
        if raw_value_2 is not None:
            return self.signal_1.encoding.encode(raw_value_1), self.signal_2.encoding.encode(raw_value_2)
        else:
            return self.signal_1.encoding.encode(raw_value_1), None

    def encode_frame(self):
        frame = [0] * 8
        frame[self.signal_1.encoding.msn : self.signal_1.encoding.lsn+1] = self.data_1
        if self.signal_2 is not None :
            if self.signal_2.encoding.lsn > self.signal_2.encoding.msn:
                df_2 = self.data_2
            else:
                df_2 = list(reversed(self.data_2))
            frame[self.signal_2.encoding.lsn : self.signal_2.encoding.msn + 1] = df_2
            if self.signal_1.encoding.lsn == self.signal_2.encoding.lsn:
                shared_nibble = construct_shared_nibble(self.data_1[-1], df_2[-1])
                frame[self.signal_1.encoding.lsn] = shared_nibble
        return frame

    def decode_frame(self):
        nibble_data_1 = self.dataframe[self.signal_1.encoding.msn:self.signal_1.encoding.lsn+1]
        if self.signal_2 is not None:
            nibble_data_2 = self.dataframe[self.signal_2.encoding.lsn:self.signal_2.encoding.msn+1]
            return self.signal_1.encoding.decode(nibble_data_1), self.signal_2.encoding.decode(list(reversed(nibble_data_2)))
        return self.signal_1.encoding.decode(nibble_data_1), None


def construct_shared_nibble(n1, n2):
    return n1 & 0xC | (n2 >> 2) & 0x3


if __name__ == '__main__':
    df = DataFrame(signal_1=SignalDefinition(name="Temp", minimum='-40', maximum='165', unit='C',
                                             physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16),
                                             encoding=SignalEncoding(bitwidth=16, msn=1, lsn=4),
                                             default=230.046875))
    df_2 = DataFrame(
        signal_1=SignalDefinition(name="Temp_bosch_1", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                                  default=-21.671875),
        signal_2=SignalDefinition(name="Temp", minimum='-40.15', maximum='130.10', unit='C',
                                  physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                                  encoding=SignalEncoding(bitwidth=12, msn=6, lsn=4),
                                  default=-21.671875)
                     )

    df_conti = DataFrame(
        signal_1=SignalDefinition(name="Pressure 1", minimum='-1', maximum='13', unit='C',
                                  physical=spec_conti(minimum=-1, maximum=13, resolution=(1/291.928), bitwidth=12, errorcodes={}, offset=1),
                                  encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                                  default=1.671875),
        signal_2=SignalDefinition(name="Temp", minimum='-40', maximum='165', unit='C',
                                  physical=spec_conti(minimum=-1, maximum=13, resolution=(1 / 291.928), bitwidth=12,
                                                      errorcodes={}, offset=1),
                                  encoding=SignalEncoding(bitwidth=12, msn=6, lsn=4),
                                  default=11.671875)
                     )
    print(df.encode_frame())
    print(df_2.encode_frame())
    print(df_conti.encode_frame())