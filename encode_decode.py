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


def encode(raw_value, bitwidth):
    """
    Converts an integer raw value to a sequence of nibbles.

    :param raw_value: integer (must fit in bitwidth)
    :param msn: nibble index
    :param lsn: nibble index
    :param bitwidth: integer
    :return: sequence of 8 integers in the range from 0 through 15; bits not occupied by the eoncoded raw value must be zero.
    """
    nibbles = []
    while bitwidth:
        nibble = raw_value & 0xf
        nibbles.append(nibble)
        raw_value >>= 4
        bitwidth -= 4
    return nibbles  # sequence of length 8; unused bits shall be set to 0


def encode_frame(raw_value, bitwidth=0, msn=0, lsn=0):
    frame = [0] * 8
    if bitwidth % 4 == 2:
        raw_value <<= 2
        nibbles = []
        for n in range(msn,lsn+1):
            nibbles.append(raw_value & 0xF)
            raw_value >>= 4
    else:
        nibbles = encode(raw_value, bitwidth)
    frame[msn:lsn+1] = list(reversed(nibbles))
    return frame


def decode(nibbles, bitwidth=0, msn=0, lsn=0):
    """
    Converts a sequence of nibbles to an integer raw value
    :param nibbles:
    :param msn: nibble index
    :param lsn: nibble index
    :param bitwidth: integer
    :return: integer raw value
    """
    raw_value = 0
    for n in nibbles[msn:lsn+1]:
        raw_value <<= 4
        raw_value += n & 0xF
    if bitwidth % 4 == 2:
        raw_value >>= 2
    return raw_value



if __name__ == '__main__':
    print(encode(291, 16))
    input = bytes([0, 1, 2, 3, 4, 2, 1, 0xF])
    print(decode(input, 10, 1, 3))
    print(encode_frame(raw_value=0x227, bitwidth=10, msn=1, lsn=3))
    print(encode_frame(raw_value=0xEB, bitwidth=10, msn=1, lsn=3))