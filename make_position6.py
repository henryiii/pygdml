#!/usr/bin/env python3

from gdml import GDML

mygdml = GDML('Bricks_Position_6')

mygdml.define.addQuantity('det_length', 1.3720, 'length', 'm')
mygdml.define.addPosition('det_location', 0, 0, 0)
mygdml.define.addRotationMatrix('det_rotation', 1,0,0,0,0,1,0,-1,0)

mygdml.define.addPosition('target_location',0,0,.6)
mygdml.define.addRotation('target_rotation',z=45)

mygdml.solids.addBox('world',1.5,1.5,3)
mygdml.structure.addWorld()

mygdml.solids.addBox('Target',.3048,.3048,.2032)
mygdml.structure.addVolume('Target','G4_Pb','target_location','target_rotation')

mygdml.solids.addTube('Shell', .290, .294, 'det_length')
mygdml.structure.addVolume('Shell','G4_Al','det_location','det_rotation')

mygdml.solids.addTube('Strips', .2470 - .005, .2684 + .005, 'det_length')
mygdml.structure.addVolume('Strips','G4_PLASTIC_SC_VINYLTOLUENE','det_position','det_rotation')

mygdml.solids.addTube('Core', 0.220, .220-.006, 'det_length')
mygdml.structure.addVolume('Core','G4_Al','det_position','det_rotation')

mygdml.tofile()


