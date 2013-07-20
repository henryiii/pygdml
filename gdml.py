#!\usr\bin\env python3

__all__ = ['Define','Materials','Solids','Structure','Setup','makefile','GDML']

MY_NAMESPACES = {'xsi':'http://www.w3.org/2001/XMLSchema-instance'}
SCHEMA_LOC = 'http://service-spi.web.cern.ch/service-spi/app/releases/GDML/GDML_3_0_0/schema/gdml.xsd'

try:
    from lxml import etree
    xfeatures = True
except ImportError:
    import xml.etree.ElementTree as etree
    xfeatures = False

class GDMLbase(object):
    def getElements(self):
        return self._core

    def __repr__(self):
        return self.__class__.__name__ + '()'

    def __str__(self):
        if xfeatures:
            return etree.tostring(self._core,encoding='utf-8',pretty_print=True).decode("utf-8")
        else:
            return etree.tostring(self._core,encoding='utf-8').decode("utf-8")


    def addGeneric(local_self, type, name, **kargs):
        el = etree.SubElement(local_self._core, type)
        el.set('name',name)
        if 'self' in kargs:
            del kargs['self']
        for name in kargs:
            el.set(name,str(kargs[name]))
        return el


class Define(GDMLbase):
    def __init__(self):
        self._core = etree.Element('define')

    def setDefault(self):
        self.addPosition('center')
        self.addRotation('identity')
        self.addScale('unity')
        return self

    def addConstant(self, name, value):
        return self.addGeneric('constant',**locals())

    def addQuantity(self, name, value, type, unit):
        return self.addGeneric('quanity',**locals())

    def addVariable(self, name, value):
        return self.addGeneric('variable',**locals())

    def addPosition(self, name, x=0, y=0, z=0, unit='m'):
        return self.addGeneric('position',**locals())

    def addRotation(self, name, x=0, y=0, z=0, unit='deg'):
        el = etree.SubElement(self._core, 'rotation')
        el.set('name',name)
        if x:
            el.set('x',str(x))
        if y:
            el.set('y',str(y))
        if z:
            el.set('z',str(z))
        el.set('unit',unit)
        return el

    def addScale(self, name, x=1, y=1, z=1):
        return self.addGeneric('scale',**locals())

    def addMatrix(self, name, coldim, values):
        'Values should be space seperated.'
        return self.addGeneric('matrix',**locals())

    def addVerts(self, name, verts, unit='m'):
        for i,vert in enumerate(verts):
            self.addPosition(name + '_v' + str(i), vert[0], vert[1], vert[2], unit)

class Materials(GDMLbase):
    'Note that G4_... NIST materials work!'
    def __init__(self):
        self._core = etree.Element('materials')

    def addIsotope(self, name, Z, N, atomtype, atomvalue):
        el = etree.SubElement(self._core, 'isotope')
        el.set('name',name)
        el.set('Z',str(Z))
        el.set('N',str(N))
        at = etree.SubElement(el,'atom')
        at.set('type', atomtype)
        at.set('value', atomvalue)
        return el

    def addElement(self, name, Z, formula, atomvalue):
        el = etree.SubElement(self._core, 'element')
        el.set('name',name)
        el.set('Z',str(Z))
        el.set('formula',formula)
        at = etree.SubElement(el,'atom')
        at.set('value', atomvalue)
        return el

    def addElementByFrac(self, name, fracdict):
        'Use a dictionary of the form element:fraction.'
        el = etree.SubElement(self._core, 'element')
        el.set('name',name)
        for frac in fracdict:
            at = etree.SubElement(el,'fraction')
            at.set('ref',frac)
            at.set('n',str(fracdict[frac]))

    def addMaterialSingleElement(self, name, Z, D, atomvalue):
        el = etree.SubElement(self._core, 'material')
        el.set('name',name)
        el.set('Z',str(Z))
        den = etree.SubElement(el, 'D')
        den.set('value',str(D))
        at = etree.SubElement(el,'atom')
        at.set('value', atomvalue)
        return el


    def addMaterialComposite(self, name, formula, D, compdict):
        'Use a dictionary of the form element:n.'
        el = etree.SubElement(self._core, 'material')
        el.set('name',name)
        el.set('formula',formula)
        den = etree.SubElement(el, 'D')
        den.set('value',str(D))
        for comp in compdict:
            at = etree.SubElement(el,'composite')
            at.set('ref',comp)
            at.set('n',str(compdict[comp]))
        return el

    def addMaterialFractions(self, name, formula, D, fracdict):
        'Use a dictionary of the form element:fraction. You can also use previously defined materials.'
        el = etree.SubElement(self._core, 'material')
        el.set('name',name)
        el.set('formula',formula)
        den = etree.SubElement(el, 'D')
        den.set('value',str(D))
        for frac in fracdict:
            at = etree.SubElement(el,'fraction')
            at.set('ref',frac)
            at.set('n',str(fracdict[frac]))
        return el


class Solids(GDMLbase):
    def __init__(self):
        self._core = etree.Element('solids')

    def addBox(self, name, x, y, z, lunit='m'):
        return self.addGeneric('box',**locals())

    def addCone(self, name, rmin1, rmax1, rmin2, rmax2, z, startphi=0, deltaphi=360, aunit='deg', lunit='m'):
        '''\
        rmin1    inner radius at base of cone
        rmax1    outer radius at base of cone
        rmin2    inner radius at top of cone
        rmax2    outer radius at top of cone
        z        height of cone segment
        startphi start angle of the segment
        deltaphi angle of the segment'''
        return self.addGeneric('cone',**locals())

    def addTrapeziod(self, name, x1, x2, y1, y2, z, lunit='m'):
        return self.addGeneric('trd',**locals())

    def addTube(self, name, rmin, rmax, z, startphi=0, deltaphi=360, aunit='deg', lunit='m'):
        return self.addGeneric('tube',**locals())

    def addTessallated(self, name, listoffaces, type='ABSOLUTE'):
        el = etree.SubElement(self._core, 'tessellated')
        el.set('name', name)
        for face in listoffaces:
            fc = etree.SubElement(el, 'triangular' if len(face) == 3 else 'quadrangular')
            for i,vert in enumerate(face):
                fc.set('vertex{0}'.format(i+1), str(vert))
            fc.set('type', type)


class Structure(GDMLbase):
    def __init__(self):
        self._core = etree.Element('structure')

    def addWorld(self, name='World', material='G4_AIR', solid_name='world'):
        'Must be a predefinied box!'
        el = etree.SubElement(self._core, 'volume')
        el.set('name', name)
        mat = etree.SubElement(el, 'materialref')
        mat.set('ref', material)
        sol = etree.SubElement(el, 'solidref')
        sol.set('ref', solid_name)
        self._world = el


    def addVolume(self, name, material, solid_name=None,
                  volume_position='center',
                  volume_rotation='identity', volume_scale='unity'):

        if solid_name is None:
            solid_name = name

        el = etree.SubElement(self._core, 'volume')
        el.set('name',name)
        mat = etree.SubElement(el, 'materialref')
        mat.set('ref', material)
        sol = etree.SubElement(el, 'solidref')
        sol.set('ref', solid_name)

        nel = etree.SubElement(self._world, 'physvol')
        volname = etree.SubElement(nel, 'volumeref')
        volname.set('ref', name)
        volpos = etree.SubElement(nel, 'positionref')
        volpos.set('ref', volume_position)
        volrot = etree.SubElement(nel, 'rotationref')
        volrot.set('ref', volume_rotation)
        volscale = etree.SubElement(nel, 'scaleref')
        volscale.set('ref', volume_scale)



class Setup(GDMLbase):
    def __init__(self, name='Default', world='World', version='1.0'):
        self._core = etree.Element('setup')
        self._core.set('name', name)
        self._core.set('version', str(version))
        el = etree.SubElement(self._core, 'world')
        el.set('ref',world)


class GDML(GDMLbase):
    def __init__(self, name='Default'):

        self._core = etree.Element('gdml',nsmap=MY_NAMESPACES)
        self._core.set('{%s}noNamespaceSchemaLocation' % MY_NAMESPACES['xsi'], SCHEMA_LOC)

        self.define = Define()
        self.materials = Materials()
        self.solids = Solids()
        self.structure = Structure()
        self.setup = Setup(name)

        self._core.append(self.define._core)
        self._core.append(self.materials._core)
        self._core.append(self.solids._core)
        self._core.append(self.structure._core)
        self._core.append(self.setup._core)

        self.define.setDefault()

    def tofile(self, filename):
        if xfeatures:
            etree.ElementTree(self._core).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)
        else:
            etree.ElementTree(self._core).write(filename, xml_declaration=True, encoding='utf-8')


def makefile(filename, *parsers):
    MY_NAMESPACES={'xsi':'http://www.w3.org/2001/XMLSchema-instance'}
    root = etree.Element('gdml',nsmap=MY_NAMESPACES)
    root.set('{%s}noNamespaceSchemaLocation' % MY_NAMESPACES['xsi'], SCHEMA_LOC)
    for parser in parsers:
        root.append(parser._core)
    if xfeatures:
        etree.ElementTree(root).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)
    else:
        etree.ElementTree(root).write(filename, xml_declaration=True, encoding='utf-8')
