# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 19:48:18 2017

@author: Wizard
"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

OSM_PATH = "sample.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':
        # create dictionary for parent
        for attrib in element.attrib:
            if attrib in NODE_FIELDS:
                node_attribs[attrib] = element.attrib[attrib]
        # create list of dictionaries for sub tags
        tagDict = {}
        for sub in element.iter("tag"):
            if PROBLEMCHARS.search(sub.attrib['k']):
                continue
            key_split = sub.attrib['k'].split(":")
            if len(key_split) == 2:
                tagDict = {
                    'id': element.attrib['id'],
                    'key': key_split[1],
                    'value': sub.attrib['v'],
                    'type': key_split[0]
                    }
            if len(key_split) != 2:
                tagDict = {
                    'id': element.attrib['id'],
                    'key': sub.attrib['k'],
                    'value': sub.attrib['v'],
                    'type': 'regular'
                    }
            tags.append(tagDict)
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for attrib in element.attrib:
            if attrib in WAY_FIELDS:
                way_attribs[attrib] = element.attrib[attrib]
        wayDict = {}
        count = 0
        for sub in element.iter("nd"):
            wayDict = {
                'id': element.attrib['id'],
                'node_id': sub.attrib['ref'],
                'position': count
                }
            count += 1
            way_nodes.append(wayDict)
        tagDict = {}
        for sub in element.iter("tag"):
            if PROBLEMCHARS.search(sub.attrib['k']):
                continue
            key_split = sub.attrib['k'].split(":")
            if len(key_split) == 1:
                tagDict = {
                    'id': element.attrib['id'],
                    'key': sub.attrib['k'],
                    'value': sub.attrib['v'],
                    'type': 'regular'
                    }
            if len(key_split) == 2:
                tagDict = {
                    'id': element.attrib['id'],
                    'key': key_split[1],
                    'value': sub.attrib['v'],
                    'type': key_split[0]
                    }
            if len(key_split) > 2:
                tagDict = {
                    'id': element.attrib['id'],
                    'key': key_split[1] +":"+ key_split[2],
                    'value': sub.attrib['v'],
                    'type': key_split[0]
                    }
            tags.append(tagDict)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH)
