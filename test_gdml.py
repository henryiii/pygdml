#!/usr/bin/env python3

from lxml import etree

def test_parsable():
    filename = 'Bricks_Position_6.gdml'

    doc = etree.parse(filename)

    schema_doc = etree.parse(find_schema_link(doc))
    schema = etree.XMLSchema(schema_doc)

    schema.assertValid(doc)

def find_schema_link(doc):
    XMLSchemaNamespace = '{http://www.w3.org/2001/XMLSchema-instance}'
    root = doc.getroot()
    schemaLink = root.get(XMLSchemaNamespace + 'schemaLocation')
    if schemaLink is None:
        schemaLink = root.get(XMLSchemaNamespace + 'noNamespaceSchemaLocation')

    return schemaLink

