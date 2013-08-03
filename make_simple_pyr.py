#!/usr/bin/env python3

from gdml import GDML

mygdml = GDML('Simple_Pyr')

mygdml.define.addQuantity('det_length', 1.3720, 'length', 'm')
mygdml.define.addQuantity('det_radius', .2734, 'length', 'm')
mygdml.define.addPosition('det_location', -8, -38.5, -10)
mygdml.define.addRotationMatrix('det_rotation',0,1,0,0,0,1,1,0,0)

mygdml.define.addPosition('target_location',0,0,.6)
mygdml.define.addRotation('target_rotation',z=45)

mygdml.solids.addBox('world',64,84,28)
mygdml.structure.addWorld()

mygdml.solids.addTrapeziod('Target',
                           x1 = 60.10, x2 = 5.32,
                           y1 = 77.24, y2 = 26.02,
                           z = 23.129)
mygdml.structure.addVolume('Target','G4_CONCRETE')

mygdml.solids.addTube('Shell', .290, .294, 'det_length/m')
mygdml.structure.addVolume('Shell','G4_Al','det_location','det_rotation')

mygdml.solids.addTube('Strips', .2420 , 'det_radius/m', 'det_length/m')
mygdml.structure.addVolume('Strips','G4_PLASTIC_SC_VINYLTOLUENE','det_location','det_rotation')

mygdml.solids.addTube('Core', 0.220-.006, 0.220, 'det_length/m')
mygdml.structure.addVolume('Core','G4_Al','det_location','det_rotation')

mygdml.validate_detector()

mygdml.tofile()


