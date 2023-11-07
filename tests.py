import unittest
from fairybase import sumPhi

class TestPhibase(unittest.TestCase):

    def test_sumPhi(self):
        self.assertEqual(sumPhi(['1+1*Q', '1+1*Q']), '2+2*Q', "Shoud be 2+2*Q")
        self.assertEqual(sumPhi(['1+1*Q','8+3*Q','3+2*Q']), '12+6*Q', "Shoud be 12+6*Q")
        self.assertEqual(sumPhi(['23+14*Q', '10+-5*Q']), '33+9*Q')
        self.assertEqual(sumPhi(['23+14*Q', '-10+-5*Q']), '13+9*Q')
        self.assertEqual(sumPhi(['23+14*Q', '12']), '35+14*Q')

if __name__=="__main__":
    unittest.main()