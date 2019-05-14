"""
Outline for functions for decoding nibbles to raw values
and encoding raw values to nibbles

Nibbles are always represented by a sequence of 8 bytes (i.e. the upper four bits must be ignored).
Nibbles are always counted from 0 to 7, and LSN and MSN always shall use this numbering. (That means, normally
MSN and LSN are in the interval from 1 through 6, because nibbles 0 and 7 are not used for signal data.)

The standard ordering of bits is to have the least significant bit in the last place (rightmost); the same
principle applies to nibbles, i.e. 0x123 is represented by the sequence [1, 2, 3] in the standard nibble order.
Hence, if LSN < MSN, the nibble order is reversed, and 0x123 would become [3, 2, 1].

If half-nibbles are used, e.g. bitwidth == 10, then it is always the LSN where only 2 bits are used. Therefore,
0x123 as a 10-bit number will become the sequence [ 4, 8, 0xC] in standard nibble order and [ 3, 8, 4] in reversed
nibble order.

According to SAE J-2716, signals have at least 8 bits and at most 24 bits, hence our tests must cover all even
bitwidths in that range.  Also the signals may start at any nibble >= 1, so all possible positions in the 6 data
nibbles must be covered.

SAE-J2716 specifies that the second signal (if present) will be in reversed order, so that half-nibbles
"""
from collections import namedtuple


def encode(raw_value, bitwidth, nibblewidth=4):
    mask = (1 << nibblewidth) - 1
    nibbles = []
    if raw_value >= (1 << bitwidth):
        raise ValueError("Given value doesn't fit the bitwidth")
    if bitwidth % 4 == 2:
        raw_value <<= 2
        # shifting left by 2 bits means 2 more bits to encode :
        bitwidth += 2
    for n in range(bitwidth // nibblewidth):
        nibbles.append(raw_value & mask)
        raw_value >>= nibblewidth
    return list(reversed(nibbles))



NibbleData = namedtuple('NibbleData', ['nibbles', 'bitwidth', 'msn', 'lsn'])


def encode_frame(nibble_data_1, nibble_data_2=None):
    frame = [0] * 8
    df_1 = nibble_data_1.nibbles
    frame[nibble_data_1.msn:nibble_data_1.lsn+1] = df_1
    if nibble_data_2 is not None:
        if nibble_data_2.lsn > nibble_data_2.msn:
            df_2 = nibble_data_2.nibbles
        else:
            df_2 = list(reversed(nibble_data_2.nibbles))
        frame[nibble_data_2.lsn:nibble_data_2.msn+1] = df_2
        if nibble_data_1.lsn == nibble_data_2.lsn:
            shared_nibble = construct_shared_nibble(nibble_data_1.nibbles[-1], nibble_data_2.nibbles[-1])
            frame[nibble_data_1.lsn] = shared_nibble
    return frame


def construct_shared_nibble(n1, n2):
    return n1 & 0xC | (n2 >> 2) & 0x3


def decode(nibbles, bitwidth=0, msn=0, lsn=0, nibblewidth=4):
    """
    Converts a sequence of nibbles to an integer raw value
    :param nibbles:
    :param msn: nibble index
    :param lsn: nibble index
    :param bitwidth: integer
    :return: integer raw value
    """
    mask = (1 << nibblewidth) - 1
    raw_value = 0
    for n in nibbles[msn:lsn+1]:
        raw_value <<= nibblewidth
        raw_value += n & mask
    if bitwidth % 4 == 2:
        raw_value >>= 2
    return raw_value


if __name__ == '__main__':
    nibbles1 = encode(0x123, 10)  # 0x000
    print(nibbles1)
    nibbles2 = encode(0x123, 10)  # 0x48C
    print(nibbles2)
    nd1 = NibbleData(nibbles1, bitwidth=10, msn=1, lsn=3)
    nd2 = NibbleData(nibbles2, bitwidth=10, msn=5, lsn=3)
    f = encode_frame(nd1, nd2)
    print(f)


