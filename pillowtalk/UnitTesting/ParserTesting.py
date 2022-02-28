import unittest
import sys
sys.path.append('../pillowtalk')
import TextParser

TP = TextParser()
class ParserTesting(unittest.TestCase):

    def test_true(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()