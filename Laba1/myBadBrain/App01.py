__author__ = 'alxant'
import xml.etree.cElementTree as ET
import re
from xml.dom import minidom



def main():
    tags = []
    input_file = '/home/alxant/PathonStady/Laba1/Start.xml'
    xml_doc = minidom.parse(input_file)
    print xml_doc
    item_list = xml_doc.getElementsByTagName('url')
    print item_list
    for s in item_list:
        tmp = []
        print s
        tmp.append(s.attributes['maintag'].value)
        tmp.append(s.attributes['tag'].value)
        tmp.append(s.attributes['name'].value)
        print tmp


main()
