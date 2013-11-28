#!/usr/bin/env python3
# Run from inside Blender
# Outputs the active object only

from textwrap import dedent
import bpy
from io import StringIO

class G4TessellatedSolid:
    def __init__(self, name):
        name = name.replace('.','_')
        self._name = name
        self._facelist = []
        self._vertlist = []

    def add_face(self,face):
        'Triangulates face if not flat, follows geant ordering convention'
        face = list(reversed(face))
        if len(face) != 4:
            self._facelist.append(face)
        else:
            v1 = self._vertlist[face[1]] - self._vertlist[face[0]]
            v2 = self._vertlist[face[2]] - self._vertlist[face[1]]
            v3 = self._vertlist[face[3]] - self._vertlist[face[2]]
            v12 = v1.cross(v2)
            plane_factor = v12.dot(v3)
            if plane_factor == 0:
                self._facelist.append(face)
            else:
                face1 = [face[0], face[1], face[2]]
                face2 = [face[0], face[2], face[3]]
                self._facelist.append(face1)
                self._facelist.append(face2)

    def add_vert(self,vert):
        self._vertlist.append(vert)

    @property
    def info(self):
        return dict(name = self._name,
                    nfaces = len(self._facelist),
                    nverts = len(self._vertlist),
                    solid = 'solid' + self._name,
                    verts = self._name + '_v',
                    faces = self._name + '_f'
                    )

    def str_init(self):
        with StringIO() as output:
            print('// Solid from blendertoG4.py', file=output)
            print('G4TessellatedSolid* {solid} = new G4TessellatedSolid("{name}");'.format(**self.info), file=output)

            print('G4VFacet* {faces}[{nfaces}];'.format(**self.info), file=output)
            return output.getvalue()

    def str_vertlist(self):
        with StringIO() as output:
            print('G4ThreeVector {verts}[] = {{'.format(**self.info), file=output)
            for vert in self._vertlist:
                print('    G4ThreeVector({0[0]:.4f},{0[1]:.4f},{0[2]:.4f})*m,'.format(vert), file=output)
            print('};', file=output)
            return output.getvalue()

    def str_facelist(self):
        with StringIO() as output:
            for n,face in enumerate(self._facelist):
                name = 'Triangular' if len(face) == 3 else 'Quadrangular'
                print('{faces}[{n}] = (G4VFacet*) new G4{type}Facet ('
                      .format(n=n,type=name,**self.info), end=' ', file=output)
                str_verts = ', '.join('{verts}[{v}]'.format(v=vertex,**self.info) for vertex in face)
                print(str_verts + ', ABSOLUTE);', file=output)
            return output.getvalue()

    def str_finalize(self):
        with StringIO() as output:
            print('for(int i=0; i<{nfaces}; i++)'.format(**self.info), file=output)
            print('    {solid}->AddFacet({faces}[i]);'.format(**self.info), file=output)
            print('{solid}->SetSolidClosed(true);'.format(**self.info), file=output)
            return output.getvalue()


    def __str__(self):
        return '\n'.join([self.str_init(), self.str_vertlist(), self.str_facelist(), self.str_finalize()])

export_cpp(filepath):

    ob = bpy.context.object
    me = ob.data
    solid = G4TessellatedSolid(ob.name)
    wmatrix = ob.matrix_world

    me.calc_tessface()

    # Fix for different object's local coords
    lmatrix = bpy.data.objects['Cube'].matrix_local

    for vert in me.vertices:
        solid.add_vert(lmatrix.inverted() * wmatrix * vert.co)

    for face in me.tessfaces:
        solid.add_face(face.vertices)

    with open(filepath, 'w') as out:
    out.write(str(solid))
