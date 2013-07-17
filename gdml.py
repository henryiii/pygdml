#!\usr\bin\env python3


try:
    from lxml import etree
    xfeatures = True
except ImportError:
    import xml.etree.ElementTree as etree
    xfeatures = False

class GDML(object):
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


class GDMLdefine(GDML):
    def __init__(self):
        self._core = etree.Element('define')

    def addConstant(self, name, value):
        return self.addGeneric('constant',**locals())

    def addQuantity(self, name, type, value, unit):
        return self.addGeneric('quanity',**locals())

    def addVariable(self, name, value):
        return self.addGeneric('variable',**locals())

    def addPosition(self, name, x, y, z, unit='m'):
        return self.addGeneric('position',**locals())

    def addRotation(self,x=0,y=0,z=0,unit='deg'):
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

class GDMLmaterials(GDML):
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


class GDMLsolids(GDML):
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


class GDMLstructure(GDML):
    def __init__(self):
        self._core = etree.Element('structure')


class GDMLsetup(GDML):
    def __init__(self):
        self._core = etree.Element('setup')


def makefile(filename, *parsers):
    MY_NAMESPACES={'xsi':'http://www.w3.org/2001/XMLSchema-instance'}
    root = etree.Element('gdml',nsmap=MY_NAMESPACES)
    root.set('{%s}noNamespaceSchemaLocation' % MY_NAMESPACES['xsi'], 'http://service-spi.web.cern.ch/service-spi/app/releases/GDML/GDML_3_0_0/schema/gdml.xsd')
    for parser in parsers:
        root.append(parser._core)
    if xfeatures:
        etree.ElementTree(root).write(filename, xml_declaration=True, encoding='utf-8', pretty_print=True)
    else:
        etree.ElementTree(root).write(filename, xml_declaration=True, encoding='utf-8')
