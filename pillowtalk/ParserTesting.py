import unittest
from TextParser import *

TP = TextParser()
class ParserTesting(unittest.TestCase):
    def test_allstop(self):
        '''Verify that all motors stop upon hearing the command "exit."'''
        string = "ksjbdvksjdv exit ksbksbd skjdskjd skjdhs"
        string = string.lower().split()
        self.assertEqual(TP.returnMotor(string), 0)

    def test_allstop2(self):
        '''Verify that all motors stop upon hearing the command "stop."'''
        string = "ks sjsbisbk svdjvd svdsbsvdvd ssdjv stop sdkjbsdv sdkkv sdkvjbdv svbsk"
        string = string.lower().split()
        self.assertEqual(TP.returnMotor(string), 0)

    def test_leftrun(self):
        '''Verify that the left pillow inflates for 1 second.'''
        string = "kjdskdjn jksdkjhsd inflate ksjdns left 1 ldsld seconds"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (1, None, 1))

    def test_rightrun(self):
        '''Verify that the right pillow inflates for 30 seconds.'''
        string = "kjdskdjn jksdkjhsd inflate ksjdns right ldsld 30 seconds"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (3, None, 30))

    def test_bothinflate(self):
        '''Verify that both pillows inflate for 20 seconds.'''
        string = "kjddjn inflate ksjdns right both ldsld 20 seconds"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (1, 3, 20))

    def test_bothdeflate(self):
        '''Verify that both pillows deflate for 30 seconds.'''
        string = "kkdjn deflate ksjdns left both ldsld 30 seconds"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (2, 4, 30))

    def test_timeconversion(self):
        '''Verify that the time interval of 2 minutes correctly converts to 120 seconds.'''
        string = "kjdskdjn deflate ksjdns right both ldsld 2 minutes"
        string = string.lower().split()
        self.assertTupleEqual(TP.returnMotor(string), (2, 4, 120))

    def test_actionexists(self):
        '''Verify that the program throws an InvalidActionError upon not finding an action in the command string.'''
        string = "kjdskn ksjs right both ldsld 2 minutes"
        string = string.lower().split()
        with self.assertRaises(InvalidActionError):
            TP.returnMotor(string)

    def test_pillowexists(self):
        '''Verify that the program throws an NonexistentPillowError upon not finding a pillow in the command string.'''
        string = "kjdskdjn inflate ldsld 2 minutes"
        string = string.lower().split()
        with self.assertRaises(NonexistentPillowError):
            TP.returnMotor(string)

    def test_timeexists(self):
        '''Verify that the program throws an InvalidActionError upon not finding a time amount in the command string.'''
        string = "kjdskdjn inflate left ldsld minutes"
        string = string.lower().split()
        with self.assertRaises(InvalidActionError):
            TP.returnMotor(string)

    def test_unitexists(self):
        '''Verify that the program throws an InvalidActionError upon not finding a time unit in the command string.'''
        string = "kjdskdjn inflate ldsld 2"
        string = string.lower().split()
        with self.assertRaises(InvalidActionError):
            TP.returnMotor(string)

if __name__ == '__main__':
    unittest.main()