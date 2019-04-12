from signaldef import *

sigdef_with_errcode = """
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
            <errorcode hexvalue="0xFFF9" desc="IM_2"/>
         </errorcodes>   
    </physical>
    <default>0</default>
</signaldefinition>
"""

if __name__ == '__main__':
    phy = Physical.from_xml(sigdef_with_errcode, 16)
    print("+++", phy.reserved_values)