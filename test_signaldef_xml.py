import pytest
from signaldef import *

input_sig_level_old = """
    <signaldefinition alt_name="Level signal 1" name="Level signal 2 - Combi-sensor">
        <encoding bitsize="16" lsn="0" msn="3" reversed="0"/>
        <physical minimum="0" maximum="600" offset="0" factor="100" unit="mm" format=".2f">
            <errorcodes>
                <errorcode hexvalue="0x0000" desc="IM_0"/>
                <errorcode hexvalue="0xFFFF" desc="IM_7"/>
                <errorcode hexvalue="0xFFFE" desc="IM_6"/>
                <errorcode hexvalue="0xFFFD" desc="IM_5"/>
                <errorcode hexvalue="0xFFFC" desc="IM_4"/>
                <errorcode hexvalue="0xFFFB" desc="IM_3"/>
                <errorcode hexvalue="0xFFFA" desc="IM_2"/>
                <errorcode hexvalue="0xFFF9" desc="IM_1"/>
            </errorcodes>
        </physical>
        <default>0</default>
    </signaldefinition>
"""

input_sig_temp_old = """
<signaldefinition alt_name="Temperature" name="Temperature">
    <encoding bitsize="16" lsn="0" msn="3" reversed="0"/>
    <physical minimum="-40" maximum="165" offset="40" factor="128" unit="°C" format=".3f">
        <errorcodes>
            <errorcode hexvalue="0x0000" desc="IM_0"/>
            <errorcode hexvalue="0xFFFF" desc="IM_7"/>
            <errorcode hexvalue="0xFFFE" desc="IM_6"/>
            <errorcode hexvalue="0xFFFD" desc="IM_5"/>
            <errorcode hexvalue="0xFFFC" desc="IM_4"/>
            <errorcode hexvalue="0xFFFB" desc="IM_3"/>
            <errorcode hexvalue="0xFFFA" desc="IM_2"/>
            <errorcode hexvalue="0xFFF9" desc="IM_1"/>
        </errorcodes>
    </physical>
    <default>0</default>
</signaldefinition>
"""

input_sig_temp_new = """
<signaldefinition alt_name="Temperature" name="Temperature">
    <encoding bitsize="16" lsn="0" msn="3" reversed="0"/>
    <physical_sae x1="-40" x2="165" y1="1" y2="26241" unit="°C" format=".3f">
        <errorcodes>
            <errorcode hexvalue="0x0000" desc="IM_0"/>
            <errorcode hexvalue="0xFFFF" desc="IM_7"/>
            <errorcode hexvalue="0xFFFE" desc="IM_6"/>
            <errorcode hexvalue="0xFFFD" desc="IM_5"/>
            <errorcode hexvalue="0xFFFC" desc="IM_4"/>
            <errorcode hexvalue="0xFFFB" desc="IM_3"/>
            <errorcode hexvalue="0xFFFA" desc="IM_2"/>
            <errorcode hexvalue="0xFFF9" desc="IM_1"/>
        </errorcodes>
    </physical_sae>
    <default>0</default>
</signaldefinition>
"""

input_sig_temp_both = """
<signaldefinition alt_name="Temperature" name="Temperature">
    <encoding bitsize="16" lsn="0" msn="3" reversed="0"/>
    <physical minimum="-40" maximum="165" offset="40" factor="128" unit="°C" format=".3f"/>
    <physical_sae x1="-40" x2="165" y1="1" y2="26241" bitwidth="16"/>
    <default>0</default>
</signaldefinition>
"""

input_sig_temp_no_phy = """
<signaldefinition alt_name="Temperature" name="Temperature">
    <encoding bitsize="16" lsn="0" msn="3" reversed="0"/>
    <default>0</default>
</signaldefinition>
"""


def test_old_phy_to_new_phy_level():
    bitwidth = 16
    expected = Physical(x1=0, x2=600, y1=1, y2=60001, bitwidth=bitwidth, unit='mm', format='.2f',
                        errorcodes={0: 'IM_0', 65529: 'IM_1', 65530: 'IM_2', 65531: 'IM_3', 65532: 'IM_4',
                                    65533: 'IM_5', 65534: 'IM_6', 65535: 'IM_7'})
    ret_phy = Physical.from_xml(input_sig_level_old, bitwidth=bitwidth)
    assert ret_phy == expected


def test_old_phy_to_new_phy_temp():
    bitwidth = 16
    expected = Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=bitwidth, unit='°C', format='.3f',
                        errorcodes={0: 'IM_0', 65529: 'IM_1', 65530: 'IM_2', 65531: 'IM_3', 65532: 'IM_4',
                                    65533: 'IM_5', 65534: 'IM_6', 65535: 'IM_7'})
    ret_phy = Physical.from_xml(input_sig_temp_old, bitwidth=bitwidth)
    assert ret_phy == expected


def test_new_phy_to_new_phy_temp():
    bitwidth = 16
    expected = Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=bitwidth, unit='°C', format='.3f',
                        errorcodes={0: 'IM_0', 65529: 'IM_1', 65530: 'IM_2', 65531: 'IM_3', 65532: 'IM_4',
                                    65533: 'IM_5', 65534: 'IM_6', 65535: 'IM_7'})
    ret_phy = Physical.from_xml(input_sig_temp_new, bitwidth=bitwidth)

    assert expected.bitwidth == ret_phy.bitwidth
    assert expected.x1 == ret_phy.x1
    assert expected.x2 == ret_phy.x2
    assert expected.y1 == ret_phy.y1
    assert expected.y2 == ret_phy.y2
    assert expected.unit == ret_phy.unit
    assert expected.format == ret_phy.format

    assert ret_phy == expected


def test_both_phy_temp():
    bitwidth = 16
    # Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=bitwidth, unit='°C', format='.3f')
    with pytest.raises(ValueError) as exc:
        Physical.from_xml(input_sig_temp_both, bitwidth=bitwidth)
        assert 'contains both' in str(exc)


def test_no_phy_temp():
    bitwidth = 16
    # expected = Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=bitwidth, unit='°C', format='.3f')
    with pytest.raises(ValueError) as exc:
        Physical.from_xml(input_sig_temp_no_phy, bitwidth=bitwidth)
        assert 'does not contain' in str(exc)


def test_old_phy_attrs_to_new_phy_attrs():
    bitwidth = 16
    ret_phy = Physical.from_xml(input_sig_temp_old, bitwidth=bitwidth)

    assert ret_phy.x1 == -40
    assert ret_phy.x2 == 165
    assert ret_phy.y1 == 1
    assert ret_phy.y2 == 26241
    assert ret_phy.bitwidth == 16
    assert ret_phy.unit == "°C"
    assert ret_phy.format == ".3f"


def test_new_phy_attrs_to_new_phy_attrs():
    bitwidth = 16
    ret_phy = Physical.from_xml(input_sig_temp_new, bitwidth=bitwidth)

    assert ret_phy.x1 == -40
    assert ret_phy.x2 == 165
    assert ret_phy.y1 == 1
    assert ret_phy.y2 == 26241
    assert ret_phy.bitwidth == 16
    assert ret_phy.unit == "°C"
    assert ret_phy.format == ".3f"
