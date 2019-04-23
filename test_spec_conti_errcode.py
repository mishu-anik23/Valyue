import pytest
from physical_errcode import spec_conti, Physical


input_args_temperature = {'minimum': '-40', 'maximum': '165',
                          'resolution': 0.0078125, 'bitwidth': 16, 'offset': '-40',
                          'errorcodes': {0: 'IM_0', 65529: 'IM_1', 65530: 'IM_2', 65531: 'IM_3', 65532: 'IM_4',
                                         65533: 'IM_5', 65534: 'IM_6', 65535: 'IM_7'}}

input_args_temperature_no_errcode = {'minimum': '-40', 'maximum': '165',
                          'resolution': 0.0078125, 'bitwidth': 16, 'offset': '-40',
                          'errorcodes': {}}

# input_args_voltage = {'minimum': '0', 'maximum': '40.75',
#                       'resolution': '0.16', 'bitwidth': 8, 'offset': '0'}

input_args_voltage = """
                <signaldefinition alt_name="Supply Voltage" name="Supply Voltage">
                    <encoding bitsize="8" lsn="0" msn="1" reversed="0"/>
                    <physical minimum="0" maximum="40.75" offset="0" factor="6.25" unit="V" format=".2f">
                    </physical>
                    <default>0</default>
                </signaldefinition>
"""

input_args_level = {'minimum': '0', 'maximum': '600',
                    'resolution': 0.01, 'bitwidth': 16, 'offset': '0',
                    'errorcodes': {0: 'IM_0', 65531: 'IM_3', 65532: 'IM_4',
                                   65533: 'IM_5'}}

input_amplitude_no_xml = {'minimum': '0', 'maximum': '24.7',
                        'resolution': 0.1, 'bitwidth': 8, 'offset': '0',
                        'errorcodes':{248: 'IM_1'}}

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


def test_spec_conti_temperature_init():
    """Test the initialized object attributes."""
    obj_temperature = spec_conti(**input_args_temperature)

    assert obj_temperature.x1 == -40
    assert obj_temperature.x2 == 165
    assert obj_temperature.y1 == 1
    assert obj_temperature.y2 == 26241
    assert obj_temperature.low_clamp == 1
    assert obj_temperature.high_clamp == 65528
    assert obj_temperature.max_raw == 65535


def test_spec_conti_temperature_init_no_errorcode():
    """Test the initialized object attributes."""
    obj_temperature = spec_conti(**input_args_temperature_no_errcode)

    assert obj_temperature.x1 == -40
    assert obj_temperature.x2 == 165
    assert obj_temperature.y1 == 0
    assert obj_temperature.y2 == 26240
    assert obj_temperature.low_clamp == 0
    assert obj_temperature.high_clamp == 65535
    assert obj_temperature.max_raw == 65535


def test_spec_conti_temperature_validate_raw():
    """validate_raw_value() considers hexadecimal and binary value as RAW and status as WARN / ERR."""
    obj_temperature = spec_conti(**input_args_temperature)

    assert obj_temperature.validate_raw_value(0xABC) == (2748, 'WARNING')
    assert obj_temperature.validate_raw_value(0xFFFF) == (0, 'ERROR')
    assert obj_temperature.validate_raw_value(0b101010111100) == (2748, 'WARNING')
    assert obj_temperature.validate_raw_value(0b1111111111111111) == (0, 'ERROR')


def test_spec_conti_temperature_validate_phy():
    """
    validate_phy_value() considers Integer or Float value as physical input and returns RAW value and status
    according to JAE2716 specification.
    """
    obj_temperature = spec_conti(**input_args_temperature)

    assert obj_temperature.validate_phy_value(-40) == (1, 'OK')
    assert obj_temperature.validate_phy_value(165) == (26241, 'OK')
    assert obj_temperature.validate_phy_value(165.001) == (26241, 'WARNING')
    assert obj_temperature.validate_phy_value(265) == (39041, 'WARNING')
    assert obj_temperature.validate_phy_value(-40.001) == (1, 'ERROR')
    assert obj_temperature.validate_phy_value(-50) == (1, 'ERROR')

    assert obj_temperature.validate_phy_value(470.75) == (65377, 'WARNING')
    assert obj_temperature.validate_phy_value(770.75) == (65528, 'ERROR')


def test_spec_conti_level_init():
    """Test the initialized object attributes."""
    obj_level = spec_conti(**input_args_level)

    assert obj_level.x1 == 0
    assert obj_level.x2 == 600
    assert obj_level.y1 == 1
    assert obj_level.y2 == 60001
    assert obj_level.low_clamp == 1
    assert obj_level.high_clamp == 65530
    assert obj_level.max_raw == 65535


def test_spec_conti_level_validate_raw():
    """validate_raw_value() considers hexadecimal and binary value as RAW and status as WARN / ERR."""
    obj_level = spec_conti(**input_args_level)

    assert obj_level.validate_raw_value(0xFEC) == (4076, 'WARNING')
    assert obj_level.validate_raw_value(0xFFFF) == (0, 'ERROR')
    assert obj_level.validate_raw_value(0b11011) == (27, 'WARNING')
    assert obj_level.validate_raw_value(0b1111111111111111) == (0, 'ERROR')


def test_spec_conti_level_validate_phy():
    """
    validate_phy_value() considers Integer or Float value as physical input and returns RAW value and status
    according to JAE2716 specification.
    """
    obj_level = spec_conti(**input_args_level)

    assert obj_level.validate_phy_value(0) == (1, 'OK')
    assert obj_level.validate_phy_value(-0.1) == (1, 'ERROR')
    assert obj_level.validate_phy_value(-10) == (1, 'ERROR')
    assert obj_level.validate_phy_value(165.96) == (16597, 'OK')
    assert obj_level.validate_phy_value(600) == (60001, 'OK')
    assert obj_level.validate_phy_value(648.76) == (64877, 'WARNING')
    assert obj_level.validate_phy_value(655.26) == (65527, 'WARNING')
    assert obj_level.validate_phy_value(655.28) == (65529, 'WARNING')
    #assert obj_level.validate_phy_value(770.75) == (65528, 'ERROR')
    assert obj_level.validate_phy_value(770.75) == (65530, 'ERROR')


# @pytest.mark.skip("Conti specification deviates too much from the J2716 Specification")
def test_spec_conti_voltage_init():
    """Test the initialized object attributes."""
    obj_voltage = Physical.from_xml(input_args_voltage, 8)

    assert obj_voltage.x1 == 0
    assert obj_voltage.x2 == 40.75
    assert obj_voltage.y1 == 0
    assert obj_voltage.y2 == 255
    assert obj_voltage.low_clamp == 0
    assert obj_voltage.high_clamp == 255
    assert obj_voltage.max_raw == 255


# @pytest.mark.skip("Conti specification deviates too much from the J2716 Specification")
def test_spec_conti_voltage_validate_raw():
    """validate_raw_value() considers hexadecimal and binary value as RAW and status as WARN / ERR."""
    obj_voltage = Physical.from_xml(input_args_voltage, 8)

    assert obj_voltage.validate_raw_value(0xA) == (10, 'WARNING')
    assert obj_voltage.validate_raw_value(0xAB) == (171, 'WARNING')
    assert obj_voltage.validate_raw_value(0x115) == (0, 'ERROR') # 277
    assert obj_voltage.validate_raw_value(0b10001) == (17, 'WARNING')
    assert obj_voltage.validate_raw_value(0b10000111) == (135, 'WARNING')
    assert obj_voltage.validate_raw_value(0b100000010) == (0, 'ERROR') # 258


#@pytest.mark.skip("Conti specification deviates too much from the J2716 Specification")
def test_spec_conti_voltage_validate_phy():
    """
    validate_phy_value() considers Integer or Float value as physical input and returns RAW value and status
    according to JAE2716 specification.
    """
    obj_voltage = Physical.from_xml(input_args_voltage, 8)

    assert obj_voltage.validate_phy_value(0) == (0, 'OK')
    assert obj_voltage.validate_phy_value(-0.01) == (0, 'ERROR')
    assert obj_voltage.validate_phy_value(5.96) == (37, 'OK')
    assert obj_voltage.validate_phy_value(35.96) == (218, 'OK')
    assert obj_voltage.validate_phy_value(40.75) == (247, 'OK')
    assert obj_voltage.validate_phy_value(40.76) == (248, 'ERROR')
    assert obj_voltage.validate_phy_value(50.76) == (248, 'ERROR')


def test_spec_conti_amplitude_init_no_xml():
    """Test the initialized object attributes."""
    obj_amplitude = spec_conti(**input_amplitude_no_xml)

    assert obj_amplitude.x1 == 0
    assert obj_amplitude.x2 == 24.7
    assert obj_amplitude.y1 == 0
    assert obj_amplitude.y2 == 247
    assert obj_amplitude.low_clamp == 0
    assert obj_amplitude.high_clamp == 247
    assert obj_amplitude.max_raw == 255


def test_spec_conti_amplitude_init():
    """Test the initialized object attributes."""
    obj_amplitude = Physical.from_xml(input_args_amplitude, 8)

    assert obj_amplitude.x1 == 0
    assert obj_amplitude.x2 == 24.7
    assert obj_amplitude.y1 == 0
    assert obj_amplitude.y2 == 247
    assert obj_amplitude.low_clamp == 0
    assert obj_amplitude.high_clamp == 247
    assert obj_amplitude.max_raw == 255


def test_spec_conti_amplitude_validate_raw():
    """validate_raw_value() considers hexadecimal and binary value as RAW and status as WARN / ERR."""
    obj_amplitude = Physical.from_xml(input_args_amplitude, 8)

    assert obj_amplitude.validate_raw_value(0xA) == (10, 'WARNING')
    assert obj_amplitude.validate_raw_value(0xAB) == (171, 'WARNING')
    assert obj_amplitude.validate_raw_value(0x115) == (0, 'ERROR') # 277
    assert obj_amplitude.validate_raw_value(0b10001) == (17, 'WARNING')
    assert obj_amplitude.validate_raw_value(0b10000111) == (135, 'WARNING')
    assert obj_amplitude.validate_raw_value(0b100000010) == (0, 'ERROR') # 258


def test_spec_conti_amplitude_validate_phy():
    """
    validate_phy_value() considers Integer or Float value as physical input and returns RAW value and status
    according to JAE2716 specification.
    """
    obj_amplitude = Physical.from_xml(input_args_amplitude, 8)

    assert obj_amplitude.validate_phy_value(0) == (0, 'OK')
    assert obj_amplitude.validate_phy_value(-2) == (0, 'ERROR')
    assert obj_amplitude.validate_phy_value(24.7) == (247, 'OK')
    assert obj_amplitude.validate_phy_value(25.1) == (247, 'ERROR')
    assert obj_amplitude.validate_phy_value(45.75) == (247, 'ERROR')

