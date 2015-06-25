from xml import etree

__author__ = 'alxant'
import xml.etree.cElementTree as ET
import re
from xml.dom import minidom
from lxml import html
from urllib2 import urlopen, URLError, HTTPError, Request


def main():
    playlist = ET.Element("playlist")
    output_list = '/home/alxant/PathonStady/Laba1/out.xml'
    for list_entry in output_list:
        product = ET.SubElement(playlist, "entry")
        print product
        ET.SubElement(product, "artist").text = list_entry[0]
        ET.SubElement(product, "title").text = list_entry[1]
        ET.SubElement(product, "genre").text = list_entry[2]
    tree = ET.ElementTree(playlist)
    print tree
    tree.write(output_list)
    parser = etree.MLParser(resolve_entities=False, strip_cdata=False)
    print parser
    document = etree.parse(output_list, parser)
    print document
    document.write(output_list, pretty_print=True, encoding='utf-8')


main()
