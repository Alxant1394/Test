__author__ = 'alxant'
import xml.etree.cElementTree as ET
import re


def main():
    url = []
    input ='/home/alxant/PathonStady/Laba1/Start.xml'
    tree = ET.parse(input)
    print tree  # Look
    root = tree.getroot()
    print root
    for child in root:
        line = child.text
        print(line)
        line = re.sub('[\n\t ]', '', line)
        print line
main()
