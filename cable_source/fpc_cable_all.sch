<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="yes" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="frames" urn="urn:adsk.eagle:library:229">
<description>&lt;b&gt;Frames for Sheet and Layout&lt;/b&gt;</description>
<packages>
</packages>
<symbols>
<symbol name="DINA4_L" urn="urn:adsk.eagle:symbol:13867/1" library_version="1">
<frame x1="0" y1="0" x2="264.16" y2="180.34" columns="4" rows="4" layer="94" border-left="no" border-top="no" border-right="no" border-bottom="no"/>
</symbol>
<symbol name="DOCFIELD" urn="urn:adsk.eagle:symbol:13864/1" library_version="1">
<wire x1="0" y1="0" x2="71.12" y2="0" width="0.1016" layer="94"/>
<wire x1="101.6" y1="15.24" x2="87.63" y2="15.24" width="0.1016" layer="94"/>
<wire x1="0" y1="0" x2="0" y2="5.08" width="0.1016" layer="94"/>
<wire x1="0" y1="5.08" x2="71.12" y2="5.08" width="0.1016" layer="94"/>
<wire x1="0" y1="5.08" x2="0" y2="15.24" width="0.1016" layer="94"/>
<wire x1="101.6" y1="15.24" x2="101.6" y2="5.08" width="0.1016" layer="94"/>
<wire x1="71.12" y1="5.08" x2="71.12" y2="0" width="0.1016" layer="94"/>
<wire x1="71.12" y1="5.08" x2="87.63" y2="5.08" width="0.1016" layer="94"/>
<wire x1="71.12" y1="0" x2="101.6" y2="0" width="0.1016" layer="94"/>
<wire x1="87.63" y1="15.24" x2="87.63" y2="5.08" width="0.1016" layer="94"/>
<wire x1="87.63" y1="15.24" x2="0" y2="15.24" width="0.1016" layer="94"/>
<wire x1="87.63" y1="5.08" x2="101.6" y2="5.08" width="0.1016" layer="94"/>
<wire x1="101.6" y1="5.08" x2="101.6" y2="0" width="0.1016" layer="94"/>
<wire x1="0" y1="15.24" x2="0" y2="22.86" width="0.1016" layer="94"/>
<wire x1="101.6" y1="35.56" x2="0" y2="35.56" width="0.1016" layer="94"/>
<wire x1="101.6" y1="35.56" x2="101.6" y2="22.86" width="0.1016" layer="94"/>
<wire x1="0" y1="22.86" x2="101.6" y2="22.86" width="0.1016" layer="94"/>
<wire x1="0" y1="22.86" x2="0" y2="35.56" width="0.1016" layer="94"/>
<wire x1="101.6" y1="22.86" x2="101.6" y2="15.24" width="0.1016" layer="94"/>
<text x="1.27" y="1.27" size="2.54" layer="94">Date:</text>
<text x="12.7" y="1.27" size="2.54" layer="94">&gt;LAST_DATE_TIME</text>
<text x="72.39" y="1.27" size="2.54" layer="94">Sheet:</text>
<text x="86.36" y="1.27" size="2.54" layer="94">&gt;SHEET</text>
<text x="88.9" y="11.43" size="2.54" layer="94">REV:</text>
<text x="1.27" y="19.05" size="2.54" layer="94">TITLE:</text>
<text x="1.27" y="11.43" size="2.54" layer="94">Document Number:</text>
<text x="17.78" y="19.05" size="2.54" layer="94">&gt;DRAWING_NAME</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="DINA4_L" urn="urn:adsk.eagle:component:13919/1" prefix="FRAME" uservalue="yes" library_version="1">
<description>&lt;b&gt;FRAME&lt;/b&gt;&lt;p&gt;
DIN A4, landscape with extra doc field</description>
<gates>
<gate name="G$1" symbol="DINA4_L" x="0" y="0"/>
<gate name="G$2" symbol="DOCFIELD" x="162.56" y="0" addlevel="must"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="my_library">
<packages>
<package name="FPC0505">
<smd name="P$1" x="-1" y="0.1" dx="1.7" dy="0.3" layer="1" roundness="3" rot="R90"/>
<smd name="P$2" x="-0.5" y="0.1" dx="1.7" dy="0.3" layer="1" roundness="3" rot="R90"/>
<smd name="P$3" x="0" y="0.1" dx="1.7" dy="0.3" layer="1" roundness="3" rot="R90"/>
<smd name="P$4" x="0.5" y="0.1" dx="1.7" dy="0.3" layer="1" roundness="3" rot="R90"/>
<smd name="P$5" x="1" y="0.1" dx="1.7" dy="0.3" layer="1" roundness="3" rot="R90"/>
<text x="-2.54" y="2.54" size="1.27" layer="25">&gt;NAME</text>
<text x="-2.54" y="-2.54" size="1.27" layer="27">&gt;VALUE</text>
</package>
<package name="FPC0705">
<smd name="P$1" x="-1.5" y="0" dx="1.7" dy="0.3" layer="1" roundness="8" rot="R90"/>
<smd name="P$2" x="-1" y="0" dx="1.7" dy="0.3" layer="1" roundness="8" rot="R90"/>
<smd name="P$3" x="-0.5" y="0" dx="1.7" dy="0.3" layer="1" roundness="8" rot="R90"/>
<smd name="P$4" x="0" y="0" dx="1.7" dy="0.3" layer="1" roundness="8" rot="R90"/>
<smd name="P$5" x="0.5" y="0" dx="1.7" dy="0.3" layer="1" roundness="8" rot="R90"/>
<smd name="P$6" x="1" y="0" dx="1.7" dy="0.3" layer="1" roundness="8" rot="R90"/>
<smd name="P$7" x="1.5" y="0" dx="1.7" dy="0.3" layer="1" roundness="8" rot="R90"/>
</package>
<package name="FPC0905">
<smd name="P$1" x="-2" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<smd name="P$2" x="-1.5" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<smd name="P$3" x="-1" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<smd name="P$4" x="-0.5" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<smd name="P$5" x="0" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<smd name="P$6" x="0.5" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<smd name="P$8" x="1.5" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<smd name="P$7" x="1" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<smd name="P$9" x="2" y="0" dx="1.7" dy="0.3" layer="1" rot="R90"/>
<text x="2.54" y="2.54" size="1.27" layer="25">&gt;NAME</text>
<text x="2.54" y="1.27" size="1.27" layer="27">&gt;VALUE</text>
</package>
</packages>
<symbols>
<symbol name="FPC0505">
<pin name="P$1" x="0" y="5.08" visible="pin" length="short"/>
<pin name="P$2" x="0" y="2.54" visible="pin" length="short"/>
<pin name="P$3" x="0" y="0" visible="pin" length="short"/>
<pin name="P$4" x="0" y="-2.54" visible="pin" length="short"/>
<pin name="P$5" x="0" y="-5.08" visible="pin" length="short"/>
<wire x1="-2.54" y1="7.62" x2="2.54" y2="7.62" width="0.254" layer="94"/>
<wire x1="2.54" y1="7.62" x2="2.54" y2="-7.62" width="0.254" layer="94"/>
<wire x1="2.54" y1="-7.62" x2="-2.54" y2="-7.62" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-7.62" x2="-2.54" y2="7.62" width="0.254" layer="94"/>
<text x="7.62" y="10.16" size="1.778" layer="95">&gt;NAME</text>
<text x="7.62" y="7.62" size="1.778" layer="96">&gt;VALUE</text>
</symbol>
<symbol name="FPC0705">
<pin name="P$1" x="0" y="7.62" visible="pin" length="short"/>
<pin name="P$2" x="0" y="5.08" visible="pin" length="short"/>
<pin name="P$3" x="0" y="2.54" visible="pin" length="short"/>
<pin name="P$4" x="0" y="0" visible="pin" length="short"/>
<pin name="P$5" x="0" y="-2.54" visible="pin" length="short"/>
<pin name="P$6" x="0" y="-5.08" visible="pin" length="short"/>
<pin name="P$7" x="0" y="-7.62" visible="pin" length="short"/>
<wire x1="-2.54" y1="10.16" x2="2.54" y2="10.16" width="0.254" layer="94"/>
<wire x1="2.54" y1="10.16" x2="2.54" y2="-10.16" width="0.254" layer="94"/>
<wire x1="2.54" y1="-10.16" x2="-2.54" y2="-10.16" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-10.16" x2="-2.54" y2="10.16" width="0.254" layer="94"/>
<text x="5.08" y="12.7" size="1.778" layer="95">&gt;NAME</text>
<text x="5.08" y="10.16" size="1.778" layer="96">&gt;VALUE</text>
</symbol>
<symbol name="FPC0905">
<pin name="P$1" x="0" y="10.16" visible="pin" length="short"/>
<pin name="P$2" x="0" y="7.62" visible="pin" length="short"/>
<pin name="P$3" x="0" y="5.08" visible="pin" length="short"/>
<pin name="P$4" x="0" y="2.54" visible="pin" length="short"/>
<pin name="P$5" x="0" y="0" visible="pin" length="short"/>
<pin name="P$6" x="0" y="-2.54" visible="pin" length="short"/>
<pin name="P$7" x="0" y="-5.08" visible="pin" length="short"/>
<pin name="P$8" x="0" y="-7.62" visible="pin" length="short"/>
<pin name="P$9" x="0" y="-10.16" visible="pin" length="short"/>
<wire x1="-2.54" y1="12.7" x2="2.54" y2="12.7" width="0.254" layer="94"/>
<wire x1="2.54" y1="12.7" x2="2.54" y2="-12.7" width="0.254" layer="94"/>
<wire x1="2.54" y1="-12.7" x2="-2.54" y2="-12.7" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-12.7" x2="-2.54" y2="12.7" width="0.254" layer="94"/>
<text x="5.08" y="15.24" size="1.27" layer="95">&gt;NAME</text>
<text x="5.08" y="12.7" size="1.27" layer="96">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="FPC0505">
<gates>
<gate name="G$1" symbol="FPC0505" x="0" y="0"/>
</gates>
<devices>
<device name="05" package="FPC0505">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
<connect gate="G$1" pin="P$3" pad="P$3"/>
<connect gate="G$1" pin="P$4" pad="P$4"/>
<connect gate="G$1" pin="P$5" pad="P$5"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="FPC0705">
<gates>
<gate name="G$1" symbol="FPC0705" x="0" y="0"/>
</gates>
<devices>
<device name="05" package="FPC0705">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
<connect gate="G$1" pin="P$3" pad="P$3"/>
<connect gate="G$1" pin="P$4" pad="P$4"/>
<connect gate="G$1" pin="P$5" pad="P$5"/>
<connect gate="G$1" pin="P$6" pad="P$6"/>
<connect gate="G$1" pin="P$7" pad="P$7"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="FPC0905">
<gates>
<gate name="G$1" symbol="FPC0905" x="0" y="0"/>
</gates>
<devices>
<device name="05" package="FPC0905">
<connects>
<connect gate="G$1" pin="P$1" pad="P$1"/>
<connect gate="G$1" pin="P$2" pad="P$2"/>
<connect gate="G$1" pin="P$3" pad="P$3"/>
<connect gate="G$1" pin="P$4" pad="P$4"/>
<connect gate="G$1" pin="P$5" pad="P$5"/>
<connect gate="G$1" pin="P$6" pad="P$6"/>
<connect gate="G$1" pin="P$7" pad="P$7"/>
<connect gate="G$1" pin="P$8" pad="P$8"/>
<connect gate="G$1" pin="P$9" pad="P$9"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="FRAME1" library="frames" library_urn="urn:adsk.eagle:library:229" deviceset="DINA4_L" device=""/>
<part name="U$1" library="my_library" deviceset="FPC0505" device="05"/>
<part name="U$2" library="my_library" deviceset="FPC0505" device="05"/>
<part name="U$3" library="my_library" deviceset="FPC0705" device="05"/>
<part name="U$4" library="my_library" deviceset="FPC0705" device="05"/>
<part name="U$5" library="my_library" deviceset="FPC0905" device="05"/>
<part name="U$6" library="my_library" deviceset="FPC0905" device="05"/>
<part name="U$7" library="my_library" deviceset="FPC0505" device="05"/>
<part name="U$8" library="my_library" deviceset="FPC0505" device="05"/>
<part name="U$9" library="my_library" deviceset="FPC0705" device="05"/>
<part name="U$10" library="my_library" deviceset="FPC0705" device="05"/>
<part name="U$11" library="my_library" deviceset="FPC0905" device="05"/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="FRAME1" gate="G$1" x="0" y="0" smashed="yes"/>
<instance part="FRAME1" gate="G$2" x="162.56" y="0" smashed="yes">
<attribute name="LAST_DATE_TIME" x="175.26" y="1.27" size="2.54" layer="94"/>
<attribute name="SHEET" x="248.92" y="1.27" size="2.54" layer="94"/>
<attribute name="DRAWING_NAME" x="180.34" y="19.05" size="2.54" layer="94"/>
</instance>
<instance part="U$1" gate="G$1" x="81.28" y="101.6" smashed="yes">
<attribute name="NAME" x="88.9" y="111.76" size="1.778" layer="95"/>
<attribute name="VALUE" x="88.9" y="109.22" size="1.778" layer="96"/>
</instance>
<instance part="U$2" gate="G$1" x="106.68" y="101.6" smashed="yes">
<attribute name="NAME" x="114.3" y="111.76" size="1.778" layer="95"/>
<attribute name="VALUE" x="114.3" y="109.22" size="1.778" layer="96"/>
</instance>
<instance part="U$3" gate="G$1" x="142.24" y="101.6" smashed="yes">
<attribute name="NAME" x="147.32" y="114.3" size="1.778" layer="95"/>
<attribute name="VALUE" x="147.32" y="111.76" size="1.778" layer="96"/>
</instance>
<instance part="U$4" gate="G$1" x="175.26" y="101.6" smashed="yes">
<attribute name="NAME" x="180.34" y="114.3" size="1.778" layer="95"/>
<attribute name="VALUE" x="180.34" y="111.76" size="1.778" layer="96"/>
</instance>
<instance part="U$5" gate="G$1" x="210.82" y="101.6" smashed="yes">
<attribute name="NAME" x="215.9" y="116.84" size="1.27" layer="95"/>
<attribute name="VALUE" x="215.9" y="114.3" size="1.27" layer="96"/>
</instance>
<instance part="U$6" gate="G$1" x="238.76" y="101.6" smashed="yes">
<attribute name="NAME" x="243.84" y="116.84" size="1.27" layer="95"/>
<attribute name="VALUE" x="243.84" y="114.3" size="1.27" layer="96"/>
</instance>
<instance part="U$7" gate="G$1" x="81.28" y="76.2" smashed="yes">
<attribute name="NAME" x="88.9" y="86.36" size="1.778" layer="95"/>
<attribute name="VALUE" x="88.9" y="83.82" size="1.778" layer="96"/>
</instance>
<instance part="U$8" gate="G$1" x="106.68" y="76.2" smashed="yes">
<attribute name="NAME" x="114.3" y="86.36" size="1.778" layer="95"/>
<attribute name="VALUE" x="114.3" y="83.82" size="1.778" layer="96"/>
</instance>
<instance part="U$9" gate="G$1" x="142.24" y="76.2" smashed="yes">
<attribute name="NAME" x="147.32" y="88.9" size="1.778" layer="95"/>
<attribute name="VALUE" x="147.32" y="86.36" size="1.778" layer="96"/>
</instance>
<instance part="U$10" gate="G$1" x="175.26" y="76.2" smashed="yes">
<attribute name="NAME" x="180.34" y="88.9" size="1.778" layer="95"/>
<attribute name="VALUE" x="180.34" y="86.36" size="1.778" layer="96"/>
</instance>
<instance part="U$11" gate="G$1" x="210.82" y="73.66" smashed="yes">
<attribute name="NAME" x="215.9" y="88.9" size="1.27" layer="95"/>
<attribute name="VALUE" x="215.9" y="86.36" size="1.27" layer="96"/>
</instance>
</instances>
<busses>
</busses>
<nets>
<net name="GND" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$1"/>
<pinref part="U$2" gate="G$1" pin="P$1"/>
<wire x1="81.28" y1="106.68" x2="106.68" y2="106.68" width="0.1524" layer="91"/>
<label x="91.44" y="106.68" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="P$2"/>
<wire x1="142.24" y1="106.68" x2="147.32" y2="106.68" width="0.1524" layer="91"/>
<label x="152.4" y="106.68" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="P$2"/>
<wire x1="175.26" y1="106.68" x2="180.34" y2="106.68" width="0.1524" layer="91"/>
<label x="185.42" y="106.68" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$5" gate="G$1" pin="P$3"/>
<wire x1="210.82" y1="106.68" x2="215.9" y2="106.68" width="0.1524" layer="91"/>
<label x="220.98" y="106.68" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$3"/>
<wire x1="238.76" y1="106.68" x2="243.84" y2="106.68" width="0.1524" layer="91"/>
<label x="248.92" y="106.68" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
<net name="SDA3" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$3"/>
<pinref part="U$2" gate="G$1" pin="P$3"/>
<wire x1="81.28" y1="101.6" x2="106.68" y2="101.6" width="0.1524" layer="91"/>
<label x="91.44" y="101.6" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="P$7"/>
<wire x1="142.24" y1="93.98" x2="147.32" y2="93.98" width="0.1524" layer="91"/>
<label x="152.4" y="93.98" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="P$7"/>
<wire x1="175.26" y1="93.98" x2="180.34" y2="93.98" width="0.1524" layer="91"/>
<label x="185.42" y="93.98" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$5" gate="G$1" pin="P$9"/>
<wire x1="210.82" y1="91.44" x2="215.9" y2="91.44" width="0.1524" layer="91"/>
<label x="220.98" y="91.44" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$9"/>
<wire x1="238.76" y1="91.44" x2="243.84" y2="91.44" width="0.1524" layer="91"/>
<label x="248.92" y="91.44" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
<net name="1.8V" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$4"/>
<pinref part="U$2" gate="G$1" pin="P$4"/>
<wire x1="81.28" y1="99.06" x2="106.68" y2="99.06" width="0.1524" layer="91"/>
<label x="91.44" y="99.06" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="P$5"/>
<wire x1="142.24" y1="99.06" x2="147.32" y2="99.06" width="0.1524" layer="91"/>
<label x="152.4" y="99.06" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="P$5"/>
<wire x1="175.26" y1="99.06" x2="180.34" y2="99.06" width="0.1524" layer="91"/>
<label x="185.42" y="99.06" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$5" gate="G$1" pin="P$6"/>
<wire x1="210.82" y1="99.06" x2="215.9" y2="99.06" width="0.1524" layer="91"/>
<label x="220.98" y="99.06" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$6"/>
<wire x1="238.76" y1="99.06" x2="243.84" y2="99.06" width="0.1524" layer="91"/>
<label x="248.92" y="99.06" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
<net name="VIN" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$5"/>
<pinref part="U$2" gate="G$1" pin="P$5"/>
<wire x1="81.28" y1="96.52" x2="106.68" y2="96.52" width="0.1524" layer="91"/>
<label x="91.44" y="96.52" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="P$6"/>
<wire x1="142.24" y1="96.52" x2="147.32" y2="96.52" width="0.1524" layer="91"/>
<label x="152.4" y="96.52" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="P$6"/>
<wire x1="175.26" y1="96.52" x2="180.34" y2="96.52" width="0.1524" layer="91"/>
<label x="185.42" y="96.52" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$5" gate="G$1" pin="P$7"/>
<wire x1="210.82" y1="96.52" x2="215.9" y2="96.52" width="0.1524" layer="91"/>
<label x="220.98" y="96.52" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$7"/>
<wire x1="238.76" y1="96.52" x2="243.84" y2="96.52" width="0.1524" layer="91"/>
<label x="248.92" y="96.52" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
<net name="SCL2" class="0">
<segment>
<pinref part="U$3" gate="G$1" pin="P$3"/>
<wire x1="142.24" y1="104.14" x2="147.32" y2="104.14" width="0.1524" layer="91"/>
<label x="152.4" y="104.14" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="P$3"/>
<wire x1="175.26" y1="104.14" x2="180.34" y2="104.14" width="0.1524" layer="91"/>
<label x="185.42" y="104.14" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$5" gate="G$1" pin="P$2"/>
<wire x1="210.82" y1="109.22" x2="215.9" y2="109.22" width="0.1524" layer="91"/>
<label x="220.98" y="109.22" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$2"/>
<wire x1="238.76" y1="109.22" x2="243.84" y2="109.22" width="0.1524" layer="91"/>
<label x="248.92" y="109.22" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
<net name="SDA2" class="0">
<segment>
<pinref part="U$3" gate="G$1" pin="P$4"/>
<wire x1="142.24" y1="101.6" x2="147.32" y2="101.6" width="0.1524" layer="91"/>
<label x="152.4" y="101.6" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="P$4"/>
<wire x1="175.26" y1="101.6" x2="180.34" y2="101.6" width="0.1524" layer="91"/>
<label x="185.42" y="101.6" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$5" gate="G$1" pin="P$8"/>
<wire x1="210.82" y1="93.98" x2="215.9" y2="93.98" width="0.1524" layer="91"/>
<label x="220.98" y="93.98" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$8"/>
<wire x1="238.76" y1="93.98" x2="243.84" y2="93.98" width="0.1524" layer="91"/>
<label x="248.92" y="93.98" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
<net name="SCL1" class="0">
<segment>
<pinref part="U$5" gate="G$1" pin="P$4"/>
<wire x1="210.82" y1="104.14" x2="215.9" y2="104.14" width="0.1524" layer="91"/>
<label x="220.98" y="104.14" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$4"/>
<wire x1="238.76" y1="104.14" x2="243.84" y2="104.14" width="0.1524" layer="91"/>
<label x="248.92" y="104.14" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
<net name="SDA1" class="0">
<segment>
<pinref part="U$5" gate="G$1" pin="P$5"/>
<wire x1="210.82" y1="101.6" x2="215.9" y2="101.6" width="0.1524" layer="91"/>
<label x="220.98" y="101.6" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$5"/>
<wire x1="238.76" y1="101.6" x2="243.84" y2="101.6" width="0.1524" layer="91"/>
<label x="248.92" y="101.6" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
<net name="SCL3" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="P$2"/>
<pinref part="U$2" gate="G$1" pin="P$2"/>
<wire x1="81.28" y1="104.14" x2="106.68" y2="104.14" width="0.1524" layer="91"/>
<label x="91.44" y="104.14" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="P$1"/>
<wire x1="142.24" y1="109.22" x2="147.32" y2="109.22" width="0.1524" layer="91"/>
<label x="152.4" y="109.22" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="P$1"/>
<wire x1="175.26" y1="109.22" x2="180.34" y2="109.22" width="0.1524" layer="91"/>
<label x="185.42" y="109.22" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$5" gate="G$1" pin="P$1"/>
<wire x1="210.82" y1="111.76" x2="215.9" y2="111.76" width="0.1524" layer="91"/>
<label x="220.98" y="111.76" size="1.016" layer="95" xref="yes"/>
</segment>
<segment>
<pinref part="U$6" gate="G$1" pin="P$1"/>
<wire x1="238.76" y1="111.76" x2="243.84" y2="111.76" width="0.1524" layer="91"/>
<label x="248.92" y="111.76" size="1.016" layer="95" xref="yes"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="8.2" severity="warning">
Since Version 8.2, EAGLE supports online libraries. The ids
of those online libraries will not be understood (or retained)
with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports URNs for individual library
assets (packages, symbols, and devices). The URNs of those assets
will not be understood (or retained) with this version.
</note>
</compatibility>
</eagle>
