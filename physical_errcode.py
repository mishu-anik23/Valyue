import xml.etree.ElementTree as ET
from math import floor
from signaldef import intorfloat, read_errorcodes
from signalrow_valid import Status


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
    print(offset_y_high)

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
        # if unit is None:
        #     raise ValueError("Parameter unit must be given")
        self.y1 = int(y1)
        self.y2 = int(y2)
        self.bitwidth = bitwidth
        self.unit = unit
        self.format = format
        self.errorcodes = errorcodes
        self.max_raw = (1 << self.bitwidth) - 1
        self.low_clamp, self.high_clamp = clamps(self.errorcodes, self.max_raw)

    def __repr__(self):
        template = "Physical(x1={0.x1}, x2={0.x2}, y1={0.y1}, y2={0.y2}, bitwidth={0.bitwidth!r}," \
                   "errorcodes={0.errorcodes!r})"
        return template.format(self)

    def __eq__(self, other):
        attrs = ['x1', 'x2', 'y1', 'y2', 'bitwidth', 'unit', 'format']
        return all(getattr(self, attr) == getattr(other, attr) for attr in attrs)

    @classmethod
    def from_xml(cls, xml_fragment, bitwidth):
        if isinstance(xml_fragment, str):
            xml_fragment = ET.fromstring(xml_fragment)
        physical_sae = xml_fragment.find('physical_sae')
        physical = xml_fragment.find('physical')
        bitfield = xml_fragment.find('isbitfield')

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
                #print(errorcodes)
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
        if raw_val <= self.low_clamp:
            raw_val = self.low_clamp
        elif raw_val >= self.high_clamp:
            raw_val = self.high_clamp
        return raw_val

    def validate_raw_value(self, raw_val):
        if raw_val >= self.max_raw:
            ret_val, status = 0, Status.ERROR.name
        else:
            ret_val, status = raw_val, Status.WARNING.name
        return ret_val, status

    def validate_phy_value(self, phy_value):
        # start_lower_range = 2
        # end_lower_range = self.y1 - 1
        # start_upper_range = self.y2 + 1
        # end_upper_range = (1 << self.bitwidth) - 9

        start_lower_range = self.low_clamp + 1
        end_lower_range = self.y1 - 1
        start_upper_range = self.y2 + 1
        end_upper_range = self.high_clamp - 1

        converted_raw_value = self.phy2raw(phy_value)

        if self.x1 <= phy_value <= self.x2:
            signal_quality = Status.OK.name
        elif (start_lower_range <= converted_raw_value <= end_lower_range or
              start_upper_range <= converted_raw_value <= end_upper_range):
            signal_quality = Status.WARNING.name
        elif converted_raw_value == self.y2 and converted_raw_value != self.high_clamp:
            signal_quality = Status.WARNING.name
        elif converted_raw_value == self.y1 and converted_raw_value != self.low_clamp:
            signal_quality = Status.WARNING.name
        else:
            signal_quality = Status.ERROR.name
        return converted_raw_value, signal_quality


if __name__ == '__main__':
    input_args_amplitude = """
    <signaldefinition alt_name="Amplitude 1st ref" name="Amplitude 1">
        <encoding bitsize="8" lsn="0" msn="1" reversed="0"/>
        <physical minimum="0" maximum="24.7" offset="0" factor="10" unit="" format=".1f">
            <errorcodes>
                <errorcode hexvalue="0xF8" desc="IM_1"/>
            </errorcodes>
        </physical>
        <default>0</default>
    </signaldefinition>
    """
    obj = Physical.from_xml(input_args_amplitude, 8)
    print(obj.y2)
    input_args_temp = """
    <signaldefinition alt_name="Temperature" name="Temperature">
        <encoding bitsize="16" lsn="0" msn="3" reversed="0"/>
        <physical minimum="-40" maximum="165" offset="40" factor="128" unit="°C" format=".3f">
            <errorcodes>
                <errorcode hexvalue="0xFFF8" desc="IM_1"/>
            </errorcodes>
        </physical>
        <default>0</default>
    </signaldefinition>
    """
    obj_temp = Physical.from_xml(input_args_temp, 16)
    print(obj_temp.y2)