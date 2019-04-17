import xml.etree.ElementTree as ET

errcode_8bit = """                
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

sigdef_with_errcode = """
<signaldefinition alt_name="Temperature" name="Temperature">
    <encoding bitsize="16" lsn="0" msn="3" reversed="0"/>
    <physical minimum="-40" maximum="165" offset="40" factor="128" unit="°C" format=".3f">
        <errorcodes>
        
            <errorcode hexvalue="0xFFFE" desc="IM_6"/>
            <errorcode hexvalue="0xFFFD" desc="IM_5"/>
            <errorcode hexvalue="0xFFFC" desc="IM_4"/>
         </errorcodes>   
    </physical>
    <default>0</default>
</signaldefinition>
"""

if __name__ == '__main__':
    signal_fragment = ET.fromstring(errcode_8bit)
    err_fragment = signal_fragment.find('physical').find('errorcodes')
    reserved_values = read_errorcodes(err_fragment)
    print("+++", reserved_values)
    min_r = min(reserved_values, key=reserved_values.get)
    #min_r = min(reserved_values.keys(), key=lambda x: x[1])
    print(min_r)
    print(sorted(reserved_values)[1])