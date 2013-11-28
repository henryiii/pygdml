#!/usr/bin/env python3
# Run from inside Blender
# Outputs the active object only

import bpy
import bpy_types
from io import StringIO

from . import cpp
Tess = cpp.G4TessellatedSolid

def export_cpp(filepath, only_sel, global_coor):
    with open(filepath, 'w') as out:
        print('Writing',filepath)
        for ob in (bpy.context.selected_objects if only_sel else bpy.data.objects):
            if isinstance(ob.data,bpy_types.Mesh):

                solid = Tess(ob.name)
                wmatrix = ob.matrix_world

                ob.data.calc_tessface()

                for vert in ob.data.vertices:
                    solid.add_vert(ob.matrix_world * vert.co if global_coor else vert.co)

                for face in ob.data.tessfaces:
                    solid.add_face(face.vertices)

                out.write(str(solid))
