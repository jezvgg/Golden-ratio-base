import unittest

from irrational_num import IrrationalNum


class TestPhibase(unittest.TestCase):

    def test_addition(self):
        num1 = IrrationalNum(1,1)
        num2 = IrrationalNum(2,2)

        assert (num1+2).rational == 3

        num3 = num1 + num2 + 3

        print(num3)
        assert num3.rational == 6
        assert num3.irrational == 3


    def test_multiplication(self):
        num1 = IrrationalNum(1,1)
        num2 = IrrationalNum(2,2)

        num1 *= 2

        assert num1.rational == 2
        assert num1.irrational == 2

        num3 = num1 * num2

        assert num3.rational == 24
        assert num3.irrational == 8


    def test_diffirance(self):
        num1 = IrrationalNum(1,1)
        num2 = IrrationalNum(2,2)

        assert (num1-2).rational == -1

        num3 = num2 - num1

        assert num3.rational == 1
        assert num3.irrational == 1