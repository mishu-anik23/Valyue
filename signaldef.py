"""
Functions and classes to define the SENT signal according to SAE J2716 specification.
"""

import numbers
from math import floor


def intorfloat(x):
    """Convert string input to int if possible, otherwise try converting to float

    Numeric input (instances of numbers.Real) will be returned unchanged.
    Other input that cannot be converted to int or float will raise a ValueError.
    """
    if isinstance(x, numbers.Real):
        return x
    try:
        return int(x)
    except ValueError:
        return float(x)


def high_clamp(bitwidth):
    return (1 << bitwidth) - 8


def calc_y2(x1, x2, resolution):
    y1 = 1
    phy_range_diff = x2 - x1
    y2 = (phy_range_diff / resolution) + y1
    return y1, y2


def spec_conti(minimum, maximum, resolution, bitwidth, offset=None):
    offsetY_low = 1
    if offset is not None:
        offset = offsetY_low
    range_diff = intorfloat(maximum) - intorfloat(minimum)
    offsetY_high = (range_diff / float(resolution)) + offset

    phy_obj = Physical(x1=minimum, x2=maximum, y1=offsetY_low, y2=offsetY_high, bitwidth=bitwidth)
    return phy_obj




class SignalEncoding:

    def __init__(self, bitsize=None):
        self.bitsize = int(bitsize)

    def __repr__(self):
        template = "SignalEncoding(bitsize={0.bitsize})"
        return template.format(self)


class Physical:
    """
    Physical represents the translation between raw signal values measured in sensor domain and
    physical units given in the Tkinter Entry widget by user.
    """
    def __init__(self, x1, x2, y1, y2, bitwidth, unit=None):
        try:
            self.x1 = intorfloat(x1)
            self.x2 = intorfloat(x2)
        except TypeError:
            raise ValueError("Missing or non-numeric input for x1 or x2")
        # if unit is None:
        #     raise ValueError("Parameter unit must be given")
        self.y1 = y1
        self.y2 = y2
        self.bitwidth = bitwidth
        self.unit = unit
        self.low_clamp = 1
        self.high_clamp = high_clamp(bitwidth)
        self.max_raw = (1 << self.bitwidth) - 1

    def __repr__(self):
        template = "Physical(x1={0.x1}, x2={0.x2}, y1={0.y1}, y2={0.y2}, bitwidth={0.bitwidth!r})"
        return template.format(self)

    def raw2phys(self, raw_value):
        """
        Convert a raw value to a physical value according to SAE J2716 specification.
        :param raw_value: raw value (int)
        :return: physical value as a number (float or int)
        """
        slope = (self.y2 - self.y1) / (self.x2 - self.x1)
        physical_value = self.x1 + (raw_value - self.y1) / slope
        return physical_value

    def phy2raw(self, phys_value):
        """
        Convert a physical value to a raw value according to SAE J2716 specification.
        :param phys_value: physical value as a number (float or int)
        :return: raw value (int)
        """
        slope = (self.y2 - self.y1) / (self.x2 - self.x1)
        raw_val = floor((self.y1 + slope * (phys_value - self.x1)) + 0.5)
        # print(raw_val)
        if raw_val <= self.low_clamp:
            raw_val = self.low_clamp
        elif raw_val >= self.high_clamp:
            raw_val = self.high_clamp
        return raw_val

    def reserved_value(self, raw_value):
        upper_limit = self.max_raw + 1
        index = upper_limit - raw_value
        indicator_message_list = ["IM_0", "IM_1", "IM_2", "IM_3", "IM_4", "IM_5", "IM_6", "IM_7"]
        if raw_value == 0:
            indicator_message = indicator_message_list[0]
        elif 1 <= index <= 7:
            indicator_message = indicator_message_list[index]
        else:
            indicator_message = ""
        return indicator_message

    def validate_raw_value(self, raw_val):
        if raw_val >= self.max_raw:
            ret_val, status = 0, "ERROR"
        else:
            ret_val, status = raw_val, "WARNING"
        return ret_val, status

    def validate_phy_value(self, phy_value):
        start_lower_range = 2
        end_lower_range = self.y1 - 1
        start_upper_range = self.y2 + 1
        end_upper_range = (1 << self.bitwidth) - 9
        converted_raw_value = self.phy2raw(phy_value)

        if self.x1 <= phy_value <= self.x2:
            signal_quality = "OK"
        elif converted_raw_value == self.y1 or converted_raw_value == self.y2:
            signal_quality = "WARNING"
        elif (start_lower_range <= converted_raw_value <= end_lower_range or
              start_upper_range <= converted_raw_value <= end_upper_range):
            signal_quality = "WARNING"
        else:
            signal_quality = "ERROR"
        return converted_raw_value, signal_quality


class SignalDefinition:
    """
    The SignalDefinition class stores all the information contained in a <signaldefinition> tag
    """

    def __init__(self, name, minimum, maximum, unit, physical, encoding=None):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.unit = unit
        self.encoding = encoding
        self.physical = physical

    def __repr__(self):
        return 'SignalDefinition(name={!r}, encoding={}, physical={})'.format(self.name, self.encoding, self.physical)

    def str2number(self, entry_input):
        try:
            if entry_input[:2] == '0x':
                base = 16
                entry_type = "RAW"
            elif entry_input[:2] == '0b':
                base = 2
                entry_type = "RAW"
            else:
                base = 10
                entry_type = "PHYSICAL"
            converted_value = int(entry_input, base)
        except ValueError:
            try:
                converted_value = float(entry_input)
                entry_type = "PHYSICAL"
            except ValueError:
                return 0, "INVALID"
        return converted_value, entry_type

    def validate_str_entry(self, str_entry):
        value, typ = self.str2number(str_entry)
        if typ == "RAW":
            raw_val, status = self.physical.validate_raw_value(value)
        elif typ == "PHYSICAL":
            raw_val, status = self.physical.validate_phy_value(value)
        else:
            raw_val, status = 0, "ERROR"
        return raw_val, status



