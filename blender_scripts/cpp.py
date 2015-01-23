#!/usr/bin/env python3

from io import StringIO
from . import gdml

class G4TessellatedSolid:
    def __init__(self, name):
        name = name.replace('.','_')
        self._name = name
        self._facelist = []
        self._vertlist = []

    def add_face(self,face):
        'Triangulates face if not flat, follows geant ordering convention'
        face = list(reversed(face))
        for realface in gdml.breakup_quads_if_needed([face],self._vertlist):
            self._facelist.append(realface)

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
            print('// Solid {name} exported from Blender'.format(**self.info), file=output)
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
            print('for(int i_{name}=0; i_{name}<{nfaces}; i_{name}++)'.format(**self.info), file=output)
            print('    {solid}->AddFacet({faces}[i_{name}]);'.format(**self.info), file=output)
            print('{solid}->SetSolidClosed(true);'.format(**self.info), file=output)
            return output.getvalue()


    def __str__(self):
        return '\n'.join([self.str_init(), self.str_vertlist(), self.str_facelist(), self.str_finalize()])
