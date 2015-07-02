#!/usr/bin/env python3
# Run from inside Blender

import bpy
import bpy_types
from pathlib import Path

from .gdml import GDML, breakup_quads_if_needed


def export_gdml(filepath, only_sel, global_coor, world=(5, 5, 5), pretty=True):
    filepath = Path(filepath)
    print('Writing', filepath)

    mygdml = GDML(filepath.stem)
    mygdml.solids.addBox('world', *world)
    mygdml.structure.addWorld()

    for ob in (bpy.context.selected_objects if only_sel else bpy.data.objects):
        if isinstance(ob.data, bpy_types.Mesh):
            name = ob.name.replace('.', '_')
            ob.data.calc_tessface()

            vertlocs = [ob.matrix_world * vert.co if global_coor else vert.co for vert in ob.data.vertices]
            mygdml.define.addVerts(name, vertlocs)

            solidfaces = [face.vertices for face in ob.data.tessfaces]
            mygdml.solids.addTessallated(name, breakup_quads_if_needed(solidfaces, vertlocs))

            mygdml.structure.addVolume(name, ob.data.materials[0].name)

    mygdml.to_file(filepath, pretty)
