#!/usr/bin/env python3
# Run from inside Blender
# Outputs the active object only
# Result is in a file nameofobject.gdml

from . import gdml.GDML as gdml
import bpy

def export_gdml(filepath,name,standalone):
    mygdml = GDML(name)

    mygdml.solids.addBox('world',5,5,5)
    mygdml.structure.addWorld()

    for ob in bpy.context.selected_objects:

        me = ob.data
        wmatrix = ob.matrix_world
        name = ob.name.replace('.','_')

        me.calc_tessface()

        # Fix for different object's local coords
        # lmatrix = ob.matrix_local
        # matrix.inverted() *

        vertlocs = [wmatrix * vert.co for vert in me.vertices]
        mygdml.define.addVerts(name,vertlocs)

        solidfaces = (face.vertices for face in me.tessfaces)
        mygdml.solids.addTessallated(name,breakup_quads_if_needed(solidfaces,vertlocs))

        mygdml.structure.addVolume(name,me.materials[0].name)

    mygdml.tofile(filepath)


def breakup_quads_if_needed(facelist,vertlist):
    for face in facelist:
        if len(face) != 4:
            yield face
        else:
            v1 = vertlist[face[1]] - vertlist[face[0]]
            v2 = vertlist[face[2]] - vertlist[face[1]]
            v3 = vertlist[face[3]] - vertlist[face[2]]
            v12 = v1.cross(v2)
            plane_factor = v12.dot(v3)
            if plane_factor == 0:
                yield face
            else:
                face1 = [face[0], face[1], face[2]]
                face2 = [face[0], face[2], face[3]]
                yield face1
                yield face2
