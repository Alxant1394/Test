_author__ = 'alxant'

from unittest import TestCase
from PlayListCreate import PlayListCreator

class Testing(TestCase):
    def test_get_urls_from_xml(self):
        s = PlayListCreator('test.xml', 'out.xml', 0, 'Test')
        self.assertEqual(s.get_url_from_xml(), ['http://itc.ua'])

    def test_get_tags_from_xml(self):
        s = PlayListCreator('test.xml', 'out.xml', 0, 'Test')
        self.assertEqual(s.get_tags_from_xml(), [[u'div', u'class', u'sad']])

    def test_scrapper(self):
        s = PlayListCreator('test.xml', 'out.xml', 0, 'Test')
        self.assertEqual(s.scrapper('file:///home/alxant/PathonStady/Laba1/testing/test.html'), None)
