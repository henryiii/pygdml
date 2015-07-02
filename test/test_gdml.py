#!/usr/bin/env python3

import unittest
import sys
from pathlib import Path

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

        self.mygdml = mygdml

    def test_save_string(self):
        self.mygdml.to_file('tmp.gdml')

    def test_save_pathlib(self):
        self.mygdml.to_file(Path('tmp.gdml'))

    def tearDown(self):
        if Path('tmp.gdml').exists():
            Path('tmp.gdml').unlink()

if __name__ == '__main__':
    unittest.main()
