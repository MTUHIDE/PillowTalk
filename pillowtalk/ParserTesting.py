import unittest
from TextParser import *

TP = TextParser()
class ParserTesting(unittest.TestCase):

    def test_true(self):
        self.assertTrue(True)

    #returnMotors
    def test_allstop(self):
        string = "ksjbdvksjdv exit ksbksbd skjdskjd skjdhs"
        string = string.lower().split()
        self.assertEqual(TP.returnMotor(string), 0)

    def test_allstop2(self):
        string = "ksjbdvksjdv ksbksbd skjdskjd skjdhs afad aasa gdg sjsbisbk svdjsdsvd svdsvdbjsvdvd svdhsdjv stop sdkjbsdv sdkvjbsdkv sdkvjbskdv sjkdvbsk"
        string = string.lower().split()
        self.assertEqual(TP.returnMotor(string), 0)

    def test_leftrun(self):
        string = "kjdskdjn jksdkjhsd inflate ksjdns left 1 ldsld seconds"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (1, None, 1))

    def test_rightrun(self):
        string = "kjdskdjn jksdkjhsd inflate ksjdns right ldsld 30 seconds"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (3, None, 30))

    def test_bothinflate(self):
        string = "kjdskdjn inflate ksjdns right both ldsld 20 seconds"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (1, 3, 20))

    def test_bothdeflate(self):
        string = "kjdskdjn deflate ksjdns left both ldsld 30 seconds"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (2, 4, 30))

    def test_timeconversion(self):
        string = "kjdskdjn deflate ksjdns right both ldsld 2 minutes"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (2, 4, 120))

    #function
    def test_actionexists(self):
        string = "kjdskdjn ksjdns right both ldsld 2 minutes"
        string = string.lower().split()
        with self.assertRaises(InvalidActionError):
            TP.returnMotor(string)

    #pillow
    def test_pillowexists(self):
        string = "kjdskdjn inflate ldsld 2 minutes"
        string = string.lower().split()
        with self.assertRaises(NonexistentPillowError):
            TP.returnMotor(string)
    #time
    def test_pillowexists(self):
        string = "kjdskdjn inflate left ldsld two minutes"
        string = string.lower().split()
        with self.assertRaises(InvalidActionError):
            TP.returnMotor(string)

    #units
    def test_pillowexists(self):
        string = "kjdskdjn inflate ldsld 2"
        string = string.lower().split()
        with self.assertRaises(InvalidActionError):
            TP.returnMotor(string)

if __name__ == '__main__':
    unittest.main()