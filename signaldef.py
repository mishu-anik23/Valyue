"""
Functions and classes to define the SENT signal according to SAE J2716 specification.
"""

import numbers
import xml.etree.ElementTree as ET
from math import floor
from collections import namedtuple
from xml.etree import cElementTree as ET

from signalrow_valid import *


SignalDetails = namedtuple('SignalDetails', ['name', 'minimum', 'maximum', 'unit', 'validate','indicate',
                                             'default', 'format', 'frame_number', 'bitwidth', 'isbitfield'])


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


def spec_conti(minimum, maximum, resolution, bitwidth, errorcodes, offset=None):

    if errorcodes:
        min_raw_value = min(errorcodes)
        if min_raw_value == 0:
            offset_y_low = 1
        else:
            offset_y_low = 0
    else:
        offset_y_low = 0

    if offset is not None:
        offset = offset_y_low
    range_diff = intorfloat(maximum) - intorfloat(minimum)
    offset_y_high = floor(range_diff / resolution + offset + 0.5)

    phy_obj = Physical(x1=minimum, x2=maximum, y1=offset_y_low, y2=offset_y_high, bitwidth=bitwidth,
                       errorcodes=errorcodes)
    return phy_obj


def boundaries_reserve_values(errdict):
    if not errdict:
        return None, None

    if 0 in errdict:
        if len(errdict) == 1:
            return 0, None
        else:
            return 0, sorted(errdict)[1]
    else:
        return None, min(errdict)


def clamps(errorcodes, max_raw):
    lower_minima, higher_minima = boundaries_reserve_values(errorcodes)
    if lower_minima is None:
        low = 0
    else:
        low = 1

    if higher_minima is None:
        high = max_raw
    else:
        high = higher_minima - 1
    return low, high


def create_signal(xml_signaldefinition, context=None):
    """
    Create a SignalDefinition object with frame control value for the XML signal definition
    :param context:
    :param xml_signaldefinition: XML fragment or ElementTree node for <signaldefinition>
    :return: SignalDefinition object
    """
    """Return a SignalDefinition object for the XML signal definition with frame control set
    """
    signal = SignalDefinition.from_xml(xml_signaldefinition, context=context)
    # print("***", signal)
    return signal


def get_default(xml_signaldefinition):
    """
    Get the value from the xml <default> tag
    :return signal default value (as a number), or None if the tag does not exist
    """
    default = xml_signaldefinition.find('default')
    try:
        return intorfloat(default.text)
    except AttributeError:
        return None


class SignalEncoding:

    def __init__(self, bitwidth=None, nibblewidth=4, msn=None, lsn=None):
        self.bitwidth = int(bitwidth)
        self.msn = int(msn)
        self.lsn = int(lsn)
        self.nibblewidth = nibblewidth

    def __repr__(self):
        template = "SignalEncoding(bitwidth={0.bitwidth}, 'nibblewidth={0.nibblewidth}, msn={0.msn}, lsn={0.lsn})"
        return template.format(self)

    def __eq__(self, other):
        attrs = ['bitwidth', 'nibblewidth', 'msn', 'lsn']
        return all(getattr(self, attr) == getattr(other, attr) for attr in attrs)

    @classmethod
    def from_xml(cls, xml_fragment):
        """Create Encoding object from an XML fragment
        :param context:
        """
        if isinstance(xml_fragment, str):
            xml_fragment = ET.fromstring(xml_fragment)
        encoding = xml_fragment.find('encoding')
        if encoding is None:
            raise ValueError("XML fragment does not contain an <encoding> tag")
        return cls(bitwidth=encoding.attrib['bitwidth'],
                   msn=encoding.attrib['msn'],
                   lsn=encoding.attrib['lsn'])

    def encode(self, raw_value):
        """Encode returns only the nibbles required for bitwidth."""
        bitwidth = self.bitwidth
        mask = (1 << self.nibblewidth) - 1
        nibbles = []
        if raw_value >= (1 << bitwidth):
            raise ValueError("Given value doesn't fit the bitwidth")
        if bitwidth % 4:
            raw_value <<= 2
            # shifting left by 2 bits means 2 more bits to encode :
            bitwidth += 2
        for n in range(bitwidth // self.nibblewidth):
            nibbles.append(raw_value & mask)
            raw_value >>= self.nibblewidth
        if self.lsn <= self.msn:
            if self.bitwidth % 4:
                nibbles[0] >>= 2
            return nibbles
        else:
            return list(reversed(nibbles))

    def decode(self, dataframe):
        """
        Convert a dataframe (8 nibbles) to a raw value.
        :param dataframe:
        :return: raw value
        """
        mask = (1 << self.nibblewidth) - 1
        raw_value = 0
        if self.lsn <= self.msn:
            lower_end = self.lsn
            higher_end = self.msn+1
            nibbles = dataframe[lower_end:higher_end]
            if self.bitwidth % 4:
                nibbles[0] <<= 2
            nibbles = list(reversed(nibbles))
        else:
            lower_end = self.msn
            higher_end = self.lsn+1
            nibbles = dataframe[lower_end:higher_end]

        for n in nibbles:
            raw_value <<= self.nibblewidth
            raw_value |= n & mask
        if self.bitwidth % 4:
            raw_value >>= 2
        return raw_value


class BitField:
    def __init__(self, bitwidth):
        self.bitwidth = int(bitwidth)
        self.max_raw = (1 << self.bitwidth) - 1
        self.x1 = 0
        self.x2 = self.max_raw
        self.y1 = 0
        self.y2 = self.max_raw
        self.unit = ""
        self.format = "d"
        self.errorcodes = {}

    def __repr__(self):
        template = "BitField(bitwidth={0.bitwidth!r})"
        return template.format(self)

    def __eq__(self, other):
        return self.bitwidth == other.bitwidth

    @classmethod
    def from_xml(cls, xml_fragment):
        if isinstance(xml_fragment, str):
            xml_fragment = ET.fromstring(xml_fragment)
        encoding = xml_fragment.find('encoding')
        bitsize = encoding.attrib['bitsize']
        return cls(bitsize)

    def raw2phys(self, raw_value):
        return raw_value

    def phy2raw(self, phys_value):
        return phys_value

    def validate_raw_value(self, raw_val):
        if raw_val > self.max_raw:
            ret_val, status = 0, Status.ERROR
        else:
            ret_val, status = raw_val, Status.OK
        return ret_val, status

    def validate_phy_value(self, phy_value):
        return phy_value, Status.OK


class Physical:
    """
    Physical represents the translation between raw signal values measured in sensor domain and
    physical units given in the Tkinter Entry widget by user.
    """
    def __init__(self, x1, x2, y1, y2, bitwidth, unit=None, format=None, errorcodes=None):
        try:
            self.x1 = intorfloat(x1)
            self.x2 = intorfloat(x2)
        except TypeError:
            raise ValueError("Missing or non-numeric input for x1 or x2")
        self.y1 = int(y1)
        self.y2 = int(y2)
        self.bitwidth = bitwidth
        self.unit = unit
        self.format = format
        self.errorcodes = errorcodes
        self.max_raw = (1 << self.bitwidth) - 1
        self._low_clamp, self._high_clamp = clamps(self.errorcodes, self.max_raw)

    def __repr__(self):
        template = "Physical(x1={0.x1}, x2={0.x2}, y1={0.y1}, y2={0.y2}, bitwidth={0.bitwidth!r}," \
                   "errorcodes={0.errorcodes!r})"
        return template.format(self)

    def __eq__(self, other):
        attrs = ['x1', 'x2', 'y1', 'y2', 'bitwidth', 'unit', 'format', 'errorcodes']
        return all(getattr(self, attr) == getattr(other, attr) for attr in attrs)

    @classmethod
    def from_xml(cls, xml_fragment, bitwidth):
        if isinstance(xml_fragment, str):
            xml_fragment = ET.fromstring(xml_fragment)
        physical_sae = xml_fragment.find('physical_sae')
        physical = xml_fragment.find('physical')

        if physical_sae is None and physical is None:
            raise ValueError("XML fragment does not contain a <physical_sae> or <physical> tag")
        elif physical_sae is not None and physical is not None:
            raise ValueError("XML fragment contains both <physical_sae> and <physical> tag")
        else:
            if physical_sae is not None:
                errorcodes_xml = physical_sae.find('errorcodes')
                errorcodes = read_errorcodes(errorcodes_xml)
                phy_obj = Physical(**physical_sae.attrib, bitwidth=bitwidth, errorcodes=errorcodes)
            else:
                errorcodes_xml = physical.find('errorcodes')
                errorcodes = read_errorcodes(errorcodes_xml)
                minimum = intorfloat(physical.attrib['minimum'])
                maximum = intorfloat(physical.attrib['maximum'])
                resolution = 1 / (intorfloat(physical.attrib['factor']))
                offset = intorfloat(physical.attrib['offset'])
                phy_obj = spec_conti(minimum, maximum, resolution, bitwidth, errorcodes, offset)
                phy_obj.format = physical.attrib['format']
                phy_obj.unit = physical.attrib['unit']
        return phy_obj

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
        if raw_val <= self._low_clamp:
            raw_val = self._low_clamp
        elif raw_val >= self._high_clamp:
            raw_val = self._high_clamp
        return raw_val

    def validate_raw_value(self, raw_val):
        if raw_val > self.max_raw:
            ret_val, status = 0, Status.ERROR
        else:
            ret_val, status = raw_val, Status.WARNING
        return ret_val, status

    def validate_phy_value(self, phy_value):
        start_lower_range = self._low_clamp + 1
        end_lower_range = self.y1 - 1
        start_upper_range = self.y2 + 1
        end_upper_range = self._high_clamp - 1

        converted_raw_value = self.phy2raw(phy_value)

        if self.x1 <= phy_value <= self.x2:
            signal_quality = Status.OK
        elif (start_lower_range <= converted_raw_value <= end_lower_range or
              start_upper_range <= converted_raw_value <= end_upper_range):
            signal_quality = Status.WARNING
        elif converted_raw_value == self.y2 and converted_raw_value != self._high_clamp:
            signal_quality = Status.WARNING
        elif converted_raw_value == self.y1 and converted_raw_value != self._low_clamp:
            signal_quality = Status.WARNING
        else:
            signal_quality = Status.ERROR
        return converted_raw_value, signal_quality


class SignalDefinition:
    """
    The SignalDefinition class stores all the information contained in a <signaldefinition> tag
    """

    def __init__(self, name, minimum, maximum, unit, physical, alt_name=None, encoding=None,
                 default=None, frame_number=None, isbitfield=False, context=None):

        context = context or {}

        self.name = name
        self.alt_name = alt_name
        self.minimum = minimum
        self.maximum = maximum
        self.unit = unit
        self.physical = physical
        self.encoding = encoding
        self.default = default
        self.frame_number = frame_number
        self.frame_number = context.get('fc', frame_number)
        if self.frame_number is not None:
            self.frame_number = int(self.frame_number)
        self.isbitfield = isbitfield

    def __repr__(self):
        return ('SignalDefinition(name={!r}, alt_name={!r}, minimum={!r}, maximum={!r}, unit={!r},'
                ' encoding={}), physical={}, default={!r}, frame_number={!r})'.
                format(self.name, self.alt_name, self.minimum, self.maximum, self.unit,
                       self.encoding, self.physical, self.default, self.frame_number))

    def __eq__(self, other):
        attrs = ['name', 'alt_name', 'minimum', 'maximum', 'unit', 'encoding', 'physical', 'default', 'frame_number']
        return all(getattr(self, a) == getattr(other, a) for a in attrs)

    @property
    def display_format(self):
        return self.physical.format

    @classmethod
    def from_xml(cls, xml_fragment, context=None):
        """
        Create a SignalDefinition from an XML fragment
        :param context:
        :param xml_fragment: an ElementTree element or a XML string beginning with <signaldefinition>
        :return: SignalDefinition object including encoding and physical range information
        """
        context = context or {}
        if isinstance(xml_fragment, str):
            xml_fragment = ET.fromstring(xml_fragment)
        if xml_fragment.tag != 'signaldefinition':
            raise ValueError("XML fragment is not a <signaldefinition>")

        encoding = SignalEncoding.from_xml(xml_fragment)
        if xml_fragment.find('isbitfield') is not None:
            bitfield = True
            physical = BitField.from_xml(xml_fragment)
        else:
            bitfield = False
            physical = Physical.from_xml(xml_fragment, encoding.bitwidth)

        return cls(
            name=xml_fragment.attrib['name'],
            alt_name=xml_fragment.attrib['alt_name'],
            minimum=str(physical.x1),
            maximum=str(physical.x2),
            unit=str(physical.unit),
            encoding=encoding,
            physical=physical,
            default=get_default(xml_fragment),
            isbitfield=bitfield,
            context=context,
        )

    def str2number(self, entry_input):
        try:
            if entry_input[:2] == '0x':
                base = 16
                entry_type = EntryType.RAW
            elif entry_input[:2] == '0b':
                base = 2
                entry_type = EntryType.RAW
            else:
                base = 10
                entry_type = EntryType.PHYSICAL
            converted_value = int(entry_input, base)
        except ValueError:
            try:
                converted_value = float(entry_input)
                entry_type = EntryType.PHYSICAL
            except ValueError:
                return 0, EntryType.INVALID
        return converted_value, entry_type

    def validate_str_entry(self, str_entry):
        value, entrytyp = self.str2number(str_entry)
        if entrytyp == EntryType.RAW:
            raw_val, stat = self.physical.validate_raw_value(value)
        elif entrytyp == EntryType.PHYSICAL:
            raw_val, stat = self.physical.validate_phy_value(value)
        else:
            raw_val, stat = 0, Status.ERROR
        return raw_val, stat

    def get_signal_details(self):
        obj_sig_detail = SignalDetails(self.name,
                                       self.minimum,
                                       self.maximum,
                                       self.unit,
                                       self.validate_str_entry,
                                       bg_color_indicator,
                                       self.default,
                                       self.display_format,
                                       self.frame_number,
                                       self.physical.bitwidth,
                                       self.isbitfield)
        return obj_sig_detail


def read_errorcodes(errorcodes_xml):
    if not errorcodes_xml:
        return {}
    if isinstance(errorcodes_xml, str):
        errorcodes_xml = ET.fromstring(errorcodes_xml)
    reserved_values = {}
    for errcode in errorcodes_xml:
        raw_value = int(errcode.attrib['hexvalue'], 16)
        reserved_values[raw_value] = errcode.attrib['desc']
    return reserved_values