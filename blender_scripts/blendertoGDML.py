#!/usr/bin/env python3
# Run from inside Blender

import bpy
import bpy_types
from pathlib import Path
import numpy as np

from .gdml import GDML, breakup_quads_if_needed


def export_gdml(filepath, only_sel, global_coor, world=(0, 0, 0), pretty=True):
    filepath = Path(filepath)
    print('Writing', filepath)

    mygdml = GDML(filepath.stem)

    objects = bpy.context.selected_objects if only_sel else bpy.data.objects
    objects = [ob for ob in objects if isinstance(ob.data, bpy_types.Mesh)]

    extents = get_extents(objects)
    for i in range(3):
        if world[i] == 0:
            print('Setting extents on', i, 'axis to', extents[i])
            world[i] = extents[i]
    mygdml.solids.addBox('world', *world)
    mygdml.structure.addWorld()

    for ob in objects:
        add_mesh(mygdml, ob, global_coor)

    mygdml.to_file(filepath, pretty)


def add_mesh(mygdml, ob, global_coor):
    name = ob.name.replace('.', '_')
    ob.data.calc_tessface()

    vertlocs = [(ob.matrix_world * vert.co if global_coor else vert.co) for vert in ob.data.vertices]
    mygdml.define.addVerts(name, vertlocs)

    solidfaces = [face.vertices for face in ob.data.tessfaces]
    mygdml.solids.addTessallated(name, breakup_quads_if_needed(solidfaces, vertlocs))

    mygdml.structure.addVolume(name, ob.data.materials[0].name if ob.data.materials else 'NoMaterial')


def get_extent(ob):
    arr = np.array([ob.matrix_world * v.co for v in ob.data.vertices], dtype=np.double)
    return arr.max(axis=0), arr.min(axis=0)


def get_extents(objects):
    extents = np.array([get_extent(ob) for ob in objects], dtype=np.double)
    return abs(extents).max(axis=0).max(axis=0)*2
