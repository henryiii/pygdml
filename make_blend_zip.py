#!/usr/bin/env python3

import zipfile
from pathlib import Path

blender_scripts = Path('blender_scripts')
pygdml = Path('pygdml')
curdir = Path()
internal_dir = Path('blender_gdml')

with zipfile.ZipFile('blender_gdml.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:

    write = lambda pre, name: myzip.write(str(pre / name), str(internal_dir / name))

    write(blender_scripts, '__init__.py')
    write(blender_scripts, 'blendertoGDML.py')
    write(blender_scripts, 'blendertoCPP.py')
    write(pygdml, 'cpp.py')
    write(pygdml, 'gdml.py')
    write(blender_scripts, 'pygdml.wiki')
    write(curdir, 'LICENSE.txt')


