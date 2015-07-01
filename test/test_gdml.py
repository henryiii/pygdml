#!/usr/bin/env python3

import unittest
import sys
from pathlib import Path

# Add main directory to path
masterpath = str(Path().absolute().parent)
if masterpath not in sys.path:
    sys.path.append(masterpath)
import pygdml.gdml as gdml


WORLD_ONLY_OUTPUT = r'''<?xml version="1.0" ?>
<gdml nsmap="{'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/GDML_3_0_0/schema/gdml.xsd">
  <define>
    <position name="center" unit="m" x="0" y="0" z="0"/>
    <rotation name="identity" unit="deg"/>
    <scale name="unity" x="1" y="1" z="1"/>
  </define>
  <materials/>
  <solids>
    <box lunit="m" name="world" x="1" y="2" z="3"/>
  </solids>
  <structure>
    <volume name="World">
      <materialref ref="G4_AIR"/>
      <solidref ref="world"/>
    </volume>
  </structure>
  <setup name="simple" version="1.0">
    <world ref="World"/>
  </setup>
</gdml>
'''

SIMPLE_OBJECTS_OUTPUT = r'''<?xml version="1.0" ?>
<gdml nsmap="{'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/GDML_3_0_0/schema/gdml.xsd">
  <define>
    <position name="center" unit="m" x="0" y="0" z="0"/>
    <rotation name="identity" unit="deg"/>
    <scale name="unity" x="1" y="1" z="1"/>
  </define>
  <materials/>
  <solids>
    <box lunit="m" name="world" x="4" y="5" z="6"/>
    <box lunit="m" name="bigbox" x="1" y="2" z="3"/>
    <box lunit="m" name="smallbox" x="1" y="2" z="3"/>
  </solids>
  <structure>
    <volume name="smallbox">
      <materialref ref="nicematerial"/>
      <solidref ref="smallbox"/>
    </volume>
    <volume name="bigbox">
      <materialref ref="awefulmaterial"/>
      <solidref ref="bigbox"/>
    </volume>
    <volume name="World">
      <materialref ref="G4_AIR"/>
      <solidref ref="world"/>
      <physvol>
        <volumeref ref="bigbox"/>
        <positionref ref="center"/>
        <rotationref ref="identity"/>
      </physvol>
      <physvol>
        <volumeref ref="smallbox"/>
        <positionref ref="center"/>
        <rotationref ref="identity"/>
      </physvol>
    </volume>
  </structure>
  <setup name="simple" version="1.0">
    <world ref="World"/>
  </setup>
</gdml>
'''

ONLY_STRUCTURE_OUTPUT = r'''<?xml version="1.0" ?>
<structure>
  <volume name="smallbox">
    <materialref ref="nicematerial"/>
    <solidref ref="smallbox"/>
  </volume>
  <volume name="bigbox">
    <materialref ref="awefulmaterial"/>
    <solidref ref="bigbox"/>
  </volume>
  <volume name="World">
    <materialref ref="G4_AIR"/>
    <solidref ref="world"/>
    <physvol>
      <volumeref ref="bigbox"/>
      <positionref ref="center"/>
      <rotationref ref="identity"/>
    </physvol>
    <physvol>
      <volumeref ref="smallbox"/>
      <positionref ref="center"/>
      <rotationref ref="identity"/>
    </physvol>
  </volume>
</structure>
'''

class TestGDMLOutput(unittest.TestCase):
    
    def test_world_only(self):
        mygdml = gdml.GDML('simple')
        mygdml.solids.addBox('world',1,2,3)
        mygdml.structure.addWorld()
        self.assertEqual(str(mygdml),WORLD_ONLY_OUTPUT)
            
    def test_simple_objects(self):
        mygdml = gdml.GDML('simple')
        mygdml.solids.addBox('world',4,5,6)
        mygdml.structure.addWorld()
        
        mygdml.solids.addBox('bigbox',1,2,3)
        mygdml.structure.addVolume('bigbox', 'awefulmaterial')

        smallbox = mygdml.solids.addBox('smallbox',1,2,3)
        mygdml.structure.addVolume(smallbox, 'nicematerial')
        self.assertEqual(str(mygdml), SIMPLE_OBJECTS_OUTPUT)
        
    def test_only_objects(self):
        mygdml = gdml.GDML('simple')
        mygdml.solids.addBox('world',4,5,6)
        mygdml.structure.addWorld()
        
        mygdml.solids.addBox('bigbox',1,2,3)
        mygdml.structure.addVolume('bigbox', 'awefulmaterial')

        smallbox = mygdml.solids.addBox('smallbox',1,2,3)
        mygdml.structure.addVolume(smallbox, 'nicematerial')
        self.assertEqual(str(mygdml.structure),ONLY_STRUCTURE_OUTPUT)

if __name__ == '__main__':
    unittest.main()