import gevent
import os
import xml.etree.cElementTree as ET
import re
from xml.dom import minidom
from urllib2 import urlopen
from urllib2 import URLError
from urllib2 import HTTPError
from urllib2 import Request
from lxml import etree
from lxml import html
from mutagen.easyid3 import EasyID3
import unicodedata
from gevent import monkey

__author__ = 'alxant'


class PlayListCreator(object):
    def __init__(self, input_path, output_path, given_depth, genre):
        """

        Ok This all understand constructor but need method comment
:param input_path:
:param output_path:
:param given_depth:
:param genre:
:return:

        """

        if os.path.exists(input_path):
            if not os.path.isfile(input_path):
                raise IOError("Not a file: %s" % input_path)
        else:
            raise IOError("File not found: %s" % input_path)

        self.input_path = input_path
        self.output_path = output_path
        self.tags = []
        self.output_list = []
        self.depth = 0
        self.given_depth = given_depth
        self.genre = genre

    def get_url_from_xml(self):
        """

        :return: file:///home/alxant/PathonStady/Laba1/test_files/test1.html
        look test.py

        """

        urls = []
        tree = ET.parse(self.input_path)
        root = tree.getroot()
        for child_of_root in root:
            line = child_of_root.text
            line = re.sub('[\n\t ]', '', line)
            print line
            urls.append(line)
        return urls

    def get_tags_from_xml(self):
        """

        :return: [u'div', u'class', u'audio']
        look App01

        """
        xml_doc = minidom.parse(self.input_path)
        item_list = xml_doc.getElementsByTagName('url')
        for s in item_list:
            temp = [s.attributes['maintag'].value,
                    s.attributes['tag'].value,
                    s.attributes['name'].value]
            self.tags.append(temp)
        return self.tags

    def scrapper(self, resource):
        """

        :param resource:
        :return:

        """
        try:
            test_req = urlopen(resource).read()
        except HTTPError as e:
            print '\tThe server couldn\'t fulfill the request.'
            print '\tError code: ', e.code
        except URLError as e:
            print '\tWe failed to reach a server.'
            print '\tReason: ', e.reason
        else:
            tree = html.fromstring(test_req)
            for link in tree.xpath('//a/@href'):
                self.depth += 1
                if self.depth < self.given_depth:
                    print "\tGoing deeper: ", link
                    self.scrapper(link)
                    print "\tWent back from some href."
            for tag in self.tags:
                links = tree.xpath('//%s[@%s="%s"]/text()' %
                                   (tag[0], tag[1], tag[2]))
                for link in links:
                    req = Request(link)
                    req.headers['Range'] = 'bytes=%s-%s' % (0, 30000)
                    f = urlopen(req)
                    v = f.read()
                    nf = open("temp.mp3", "w")
                    nf.write(v)
                    nf.close()
                    audio = EasyID3("temp.mp3")
                    artist = audio["artist"]
                    unicodedata.normalize('NFKD', artist[0]).\
                        encode('ascii', 'ignore')
                    title = audio["title"]
                    unicodedata.normalize('NFKD', title[0]).\
                        encode('ascii', 'ignore')
                    genre = audio["genre"]
                    unicodedata.normalize('NFKD', genre[0]).\
                        encode('ascii', 'ignore')
                    print '\tSong found: ' + artist[0] + ' - ' +\
                          title[0] + '; genre - ' + genre[0]
                    os.system("rm temp.mp3")
                    new_playlist_entry = []
                    if self.genre == genre[0]:
                        new_playlist_entry.append(artist[0])
                        new_playlist_entry.append(title[0])
                        new_playlist_entry.append(genre[0])
                        self.output_list.append(new_playlist_entry)

    def write_xml(self):
        """

        :return:

        """
        playlist = ET.Element("playlist")
        for list_entry in self.output_list:
            product = ET.SubElement(playlist, "entry")
            ET.SubElement(product, "artist").text = list_entry[0]
            ET.SubElement(product, "title").text = list_entry[1]
            ET.SubElement(product, "genre").text = list_entry[2]
        tree = ET.ElementTree(playlist)
        tree.write(self.output_path)
        parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
        document = etree.parse(self.output_path, parser)
        document.write(self.output_path, pretty_print=True, encoding='utf-8')

    def multitask_scrapper(self, resources):
        """

        :param resources:
        :return:

        """
        monkey.patch_all()
        jobs = [gevent.spawn(self.scrapper, url) for url in resources]
        gevent.wait(jobs)
