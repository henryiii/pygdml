#!/usr/bin/env python3
# Run from inside Blender
# Outputs the active object only
# Result is in seperate text block and console

from textwrap import dedent
import bpy

class G4TessellatedSolid:
    def __init__(self, name):
        self._name = name
        self._facelist = []

    def __str__(self):
        out = '// Solid from blendertoG4.py\n'
        out += 'G4TessellatedSolid* solidTarget = new G4TessellatedSolid("{name}");\n\n'.format(name=self._name)
        for n,facet in enumerate(self._facelist):
            name = 'Triangular' if len(facet) == 3 else 'Quadrangular'
            out += 'G4{type}Facet *facet{n} = new G4{type}Facet (\n'.format(n=n,type=name)
            for item in facet[::-1]:
                out += '    G4ThreeVector({0[0]:.4f},{0[1]:.4f},{0[2]:.4f})*m,\n'.format(item)

            out += '    ABSOLUTE);\n'
        out += '\n'
        for n in range(len(self._facelist)):
            out += 'solidTarget->AddFacet((G4VFacet*) facet{n});\n'.format(n=n)
        out += 'solidTarget->SetSolidClosed(true);'
        return out


ob = bpy.context.object
me = ob.data
solid = G4TessellatedSolid(ob.name)
wmatrix = ob.matrix_world

me.calc_tessface()

# Fix for different object's local coords
lmatrix = bpy.data.objects['Cube'].matrix_local

for face in me.tessfaces:
    solid._facelist.append([lmatrix.inverted() * wmatrix * me.vertices[vertex].co  for vertex in face.vertices])

out = bpy.data.texts.new('output.cpp')
out.write(str(solid))

print(solid)
