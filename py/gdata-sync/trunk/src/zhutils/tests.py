# -*- encoding=utf8 -*-
import unittest
from pinyin import hanzi2pinyin

# 1. encoding
# 2. output

class PinYinTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testChinese(self):
        assert hanzi2pinyin(u'公共的模') == u'gonggongdemo'

    def testEnglish(self): 
        assert hanzi2pinyin(u'this is a english') == u'this is a english'

    def testMixedText(self):
        assert hanzi2pinyin(u'公共的  模 asdf!') == u'gonggongde  mo asdf!'

def suite():
    return unittest.makeSuite(PinYinTestCase, 'test')

if __name__ == '__main__':
   runner = unittest.TextTestRunner()
   runner.run(suite())
