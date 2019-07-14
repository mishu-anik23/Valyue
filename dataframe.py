class DataFrame:
    """
    Constructs Nibble data of 1 or 2 signal (if present) in a SENT data frame.
    """
    def __init__(self, encoding1, encoding2=None):
        self.encoding1 = encoding1
        self.encoding2 = encoding2

    def encode_frame(self, raw1, raw2=None):
        frame = [0] * 8
        nibble1 = self.encoding1.encode(raw1)
        frame[self.encoding1.msn : self.encoding1.lsn+1] = nibble1

        if self.encoding2:
            nibble2 = self.encoding2.encode(raw2)
            frame[self.encoding2.lsn : self.encoding2.msn+1] = nibble2
            if self.encoding1.lsn == self.encoding2.lsn:
                shared_nibble = nibble1[-1] | nibble2[0]
                frame[self.encoding1.lsn] = shared_nibble
        return frame

    def decode_frame(self, dataframe):
        raw_1 = self.encoding1.decode(dataframe)
        raw_2 = self.encoding2.decode(dataframe) if self.encoding2 else None
        return raw_1, raw_2


def construct_shared_nibble(n1, n2):
    return n1 & 0xC | (n2 >> 2) & 0x3
