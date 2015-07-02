#!/usr/bin/env python3

import unittest
import sys
from pathlib import Path
from tempfile import TemporaryFile

# Add main directory to path, get DIR
DIR = Path(__file__).absolute().parent
if str(DIR.parent) not in sys.path:
    sys.path.append(str(DIR.parent))
import pygdml.gdml as gdml

REQUIRED_DETECTOR = ('det_rotation', 'det_location', 'Shell', 'Strips', 'Core')


class TestGDMLToText(unittest.TestCase):

    def test_world_only(self):
        mygdml = gdml.GDML('simple')
        mygdml.solids.addBox('world', 1, 2, 3)
        mygdml.structure.addWorld()
        with (DIR / 'world_only.gdml').open() as f:
            self.assertEqual(str(mygdml), f.read())

    def test_simple_objects(self):
        mygdml = gdml.GDML('simple')
        mygdml.solids.addBox('world', 4, 5, 6)
        mygdml.structure.addWorld()

        mygdml.solids.addBox('bigbox', 1, 2, 3)
        mygdml.structure.addVolume('bigbox', 'awefulmaterial')

        smallbox = mygdml.solids.addBox('smallbox', 1, 2, 3)
        mygdml.structure.addVolume(smallbox, 'nicematerial')
        with (DIR / 'simple_objects.gdml').open() as f:
            self.assertEqual(str(mygdml), f.read())

    def test_only_objects(self):
        mygdml = gdml.GDML('simple')
        mygdml.solids.addBox('world', 4, 5, 6)
        mygdml.structure.addWorld()

        mygdml.solids.addBox('bigbox', 1, 2, 3)
        mygdml.structure.addVolume('bigbox', 'awefulmaterial')

        smallbox = mygdml.solids.addBox('smallbox', 1, 2, 3)
        mygdml.structure.addVolume(smallbox, 'nicematerial')
        with (DIR / 'only_structure.gdml').open() as f:
            self.assertEqual(str(mygdml.structure), f.read())


class TestGDMLFiles(unittest.TestCase):

    def setUp(self):
        mygdml = gdml.GDML('simple')
        mygdml.solids.addBox('world', 4, 5, 6)
        mygdml.structure.addWorld()

        mygdml.solids.addBox('bigbox', 1, 2, 3)
        mygdml.structure.addVolume('bigbox', 'awefulmaterial')

        smallbox = mygdml.solids.addBox('smallbox', 1, 2, 3)
        mygdml.structure.addVolume(smallbox, 'nicematerial')

        self.mygdml = mygdml
        self.mypath = Path('tmp_will_be_deleted.gdml')
        self.actual = DIR / 'simple_objects.gdml'

    def test_save_string(self):
        self.mygdml.to_file(str(self.mypath), pretty=True)
        with self.actual.open() as f1, self.mypath.open() as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_save_pathlib(self):
        self.mygdml.to_file(self.mypath, pretty=True)
        with self.actual.open() as f1, self.mypath.open() as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_save_tmpfile(self):
        with self.actual.open() as f1, TemporaryFile('w+') as f2:
            self.mygdml.to_file(f2, pretty=True)
            f2.seek(0)
            self.assertEqual(f1.read(), f2.read())


    def tearDown(self):
        if self.mypath.exists():
            self.mypath.unlink()


class TestStandardDetector(unittest.TestCase):

    def test_position_6(self):
        mygdml = gdml.GDML('Bricks_Position_6')

        mygdml.define.addQuantity('det_length', 1.3720, 'length', 'm')
        mygdml.define.addQuantity('det_radius', .2734, 'length', 'm')

        mygdml.define.addPosition('det_location', 0, 0, 0)
        mygdml.define.addRotationMatrix('det_rotation', 1, 0, 0, 0, 0, 1, 0, -1, 0)

        mygdml.define.addPosition('target_location', 0, 0, .6)
        mygdml.define.addRotation('target_rotation', z=45)

        mygdml.solids.addBox('world', 1.0, 1.5, 1.6)
        mygdml.structure.addWorld()

        mygdml.solids.addBox('Target', .3048, .3048, .2032)
        mygdml.structure.addVolume('Target', 'G4_Pb', 'target_location', 'target_rotation')

        mygdml.solids.addTube('Shell', .290, .294, 'det_length/m')
        mygdml.structure.addVolume('Shell', 'G4_Al', 'det_location', 'det_rotation')

        mygdml.solids.addTube('Strips', .2420, 'det_radius/m', 'det_length/m')
        mygdml.structure.addVolume('Strips', 'G4_PLASTIC_SC_VINYLTOLUENE', 'det_location', 'det_rotation')

        mygdml.solids.addTube('Core', 0.220-.006, 0.220, 'det_length/m')
        mygdml.structure.addVolume('Core', 'G4_Al', 'det_location', 'det_rotation')

        mygdml.validate(REQUIRED_DETECTOR)

        mygdml.to_file()

        main_file = Path('Bricks_Position_6.gdml')
        true_file = DIR / 'Bricks_Position_6_actual.gdml'

        self.assertTrue(main_file.exists())
        with main_file.open() as f1, true_file.open() as f2:
            self.assertEqual(f1.read(), f2.read())

        if main_file.exists():
            main_file.unlink()


if __name__ == '__main__':
    unittest.main()
