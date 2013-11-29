#!/usr/bin/env python3
# Run from inside Blender

import bpy
import bpy_types
import os

from .gdml import GDML, breakup_quads_if_needed

def export_gdml(filepath, only_sel, global_coor, standalone=False, world=(5,5,5)):
    print('Writing',filepath)
    fname = os.path.splitext(os.path.basename(filepath))[0]
    mygdml = GDML(fname)
    mygdml.solids.addBox('world',*world)
    mygdml.structure.addWorld()

    for ob in (bpy.context.selected_objects if only_sel else bpy.data.objects):
        if isinstance(ob.data,bpy_types.Mesh):

            name = ob.name.replace('.','_')
            ob.data.calc_tessface()

            vertlocs = [ob.matrix_world * vert.co if global_coor else vert.co for vert in ob.data.vertices]
            mygdml.define.addVerts(name,vertlocs)

            solidfaces = [face.vertices for face in ob.data.tessfaces]
            mygdml.solids.addTessallated(name,breakup_quads_if_needed(solidfaces,vertlocs))

            mygdml.structure.addVolume(name,ob.data.materials[0].name)

    mygdml.tofile(filepath)

