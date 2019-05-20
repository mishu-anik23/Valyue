from signaldef import *


class DataFrame:
    """
    Constructs Nibble data of 1 or 2 signal (if present) in a SENT data frame.
    """
    def __init__(self, encoding_1, encoding_2=None):
        self.encoding_1 = encoding_1
        self.encoding_2 = encoding_2

    def encode_frame(self, raw_value_1, raw_value_2=None):
        frame = [0] * 8
        nibble_data_1 = self.encoding_1.encode(raw_value_1)
        frame[self.encoding_1.msn : self.encoding_1.lsn+1] = nibble_data_1
        if self.encoding_2 is not None :
            if self.encoding_2.lsn > self.encoding_2.msn:
                nibble_data_2 = self.encoding_2.encode(raw_value_2)
            else:
                nibble_data_2 = list(reversed(self.encoding_2.encode(raw_value_2)))
            frame[self.encoding_2.lsn : self.encoding_2.msn + 1] = nibble_data_2
            if self.encoding_1.lsn == self.encoding_2.lsn:
                shared_nibble = construct_shared_nibble(nibble_data_1[-1], list(reversed(nibble_data_2))[-1])
                frame[self.encoding_1.lsn] = shared_nibble
        return frame

    def decode_frame(self, nibbles):
        if self.encoding_2 is not None:
            return self.encoding_1.decode(nibbles), self.encoding_2.decode(nibbles)
        return self.encoding_1.decode(nibbles), None


def construct_shared_nibble(n1, n2):
    return n1 & 0xC | (n2 >> 2) & 0x3
