#!/usr/bin/env python3
# Run from inside Blender

import bpy
import bpy_types

from .cpp import G4TessellatedSolid as Tess

def export_cpp(filepath, only_sel, global_coor):
    with open(filepath, 'w') as out:
        print('Writing',filepath)
        for ob in (bpy.context.selected_objects if only_sel else bpy.data.objects):
            if isinstance(ob.data,bpy_types.Mesh):
                name = ob.name.replace('.','_')
                solid = Tess(name)
                wmatrix = ob.matrix_world

                ob.data.calc_tessface()

                for vert in ob.data.vertices:
                    solid.add_vert(ob.matrix_world * vert.co if global_coor else vert.co)

                for face in ob.data.tessfaces:
                    solid.add_face(face.vertices)

                out.write(str(solid))
