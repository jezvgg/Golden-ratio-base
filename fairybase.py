from math import gcd
from functools import singledispatchmethod
from irrational_num import IrrationalNum


class FairyBase:
    value: str
    __repl: dict

    def __init__(self, fromInt: int = None, fromFyriBase: str = None):
        self.__repl = {
            '011': '100', '01.1': '10.0', '0.11': '1.00', '0200': '1001', '02.21': '10.22',
            '0.220': '1.021', '1200': '2001', '0210': '1011', '1220': '2021', '0201': '1002',
            '1210': '2011', '1201': '2002', '1211': '2012', '0211': '1012', '0.200': '1.001',
            '1.200': '2.001', '0.210': '1.011', '0.201': '1.002', '1.210': '2.011', '1.201': '2.002',
            '1.211': '2.012', '02.00': '10.01', '12.00': '20.01', '02.10': '10.11', '02.01': '10.02',
            '12.10': '20.11', '12.01': '20.02', '12.11': '20.12', '020.0': '100.1', '120.0': '200.1',
            '021.0': '101.1', '020.1': '100.2', '121.0': '201.0', '120.1': '200.2', '121.1': '201.2'
        }

        if fromInt is not None:
            self.value = self.toPhibase(fromInt)
        if fromFyriBase is not None:
            self.value = fromFyriBase

    @singledispatchmethod
    def __iadd__(self, other) -> "FairyBase":
        if not isinstance(other, self.__class__):
            raise SyntaxError(f"FairyBase don't sum with {type(other)}")

        pNumber1, nNumber1 = self.normalizePhi(self.value.split('.'))
        pNumber2, nNumber2 = self.normalizePhi(other.value.split('.'))
        pNumber1, pNumber2 = sorted([pNumber1, pNumber2], key=len, reverse=True)
        nNumber1, nNumber2 = sorted([nNumber1, nNumber2], key=len, reverse=True)

        pNumber2 = '0' * (len(pNumber1) - len(pNumber2)) + pNumber2
        result_pNumber = ''.join([str(int(n1) + int(n2)) for n1, n2 in zip(pNumber1, pNumber2)])

        nNumber2 = nNumber2 + '0' * (len(nNumber1) - len(nNumber2))
        result_nNumber = ''.join([str(int(n1) + int(n2)) for n1, n2 in zip(nNumber1, nNumber2)])

        self.value = self.normalizePhi(f'{result_pNumber}.{result_nNumber}')
        return self

    def __add__(self, other) -> "FairyBase":
        num = FairyBase(fromFyriBase=self.value)
        num += other
        return num

    def toPhibase(self, number: int):
        result = FairyBase(fromFyriBase="10.01")
        i = 2
        while number - i > 4:
            while i * 2 < number:
                result += result
                i *= 2
            number -= i
            i = 2

        phibase = result.value
        for i in range(number - i + 2):
            positive_part = phibase.split('.')[0]
            negative_part = phibase.split('.')[1]
            if positive_part[-1] == '0':
                phibase = self.normalizePhi(f'{positive_part[:-1]}1.{negative_part}')
            else:
                phibase = self.denormalizePhi(phibase)
                phibase = self.normalizePhi(f"{phibase.split('.')[0][:-1]}1.{phibase.split('.')[1]}")

        for i, n in enumerate(phibase[::-1]):
            if n == '1' and i == 0:
                break
            if n == '1':
                phibase = phibase[:-i]
                break

        return phibase

    def normalizePhi(self, phibase: str):
        while '11' in phibase or '1.1' in phibase or '2' in phibase:
            for replaceable, replacement in self.__repl.items():
                phibase = phibase.replace(replaceable, replacement)

            if phibase[:2] == '11':
                phibase = '100' + phibase[2:]
            elif phibase[0] == '2':
                phibase = '0' + phibase
            elif phibase[-1] == '2':
                phibase = phibase + '00'
            elif phibase[-2] == '2':
                phibase += '0'

        return phibase

    def denormalizePhi(self, phibase: str):
        positive_part = phibase.split('.')[0]
        negative_phibase = phibase.split('.')[1][::-1]

        while negative_phibase[-2:] != '00':
            if negative_phibase[0] == '1':
                negative_phibase = '110' + negative_phibase[1:]
            negative_phibase = negative_phibase.replace('001', '110')

        if positive_part[-1] == '1':
            negative_phibase = negative_phibase[::-1]
            negative_phibase = '11' + negative_phibase[2:]
            return f'{positive_part[:-1]}0.{negative_phibase}'
        else:
            return f'{positive_part}.{negative_phibase[::-1]}'

    def calcPositivePhiToDec(self, positive_part: str):
        zero = positive_part[-1]
        positive_part = positive_part[:-1]

        positive_result = IrrationalNum(0, 0)
        max_number = 2 ** len(positive_part)
        for i, number in enumerate(positive_part[::-1]):
            if number == '1':
                koef = int(max_number / 2 ** int(i + 1))
                system = IrrationalNum(1, 1 + 1)
                for _ in range(i):
                    system *= IrrationalNum(1, 1)

                positive_result += (system * koef)

        if zero == '1':
            return positive_result
        return [positive_result, max_number]

    def calcNegativePhiToDec(self, negative_part: str, debug: bool = False):
        negative_result = IrrationalNum(0, 0)
        negative_index = IrrationalNum(0, 0)
        max_index = 2 ** len(negative_part)
        for i, number in enumerate(negative_part):
            if number == '1':
                koef = int(max_index / 2 ** (i + 1))
                if debug:
                    print('koef', koef)
                system = IrrationalNum(1, 1)
                for _ in range(i + 1):
                    system *= IrrationalNum(1, 1)
                if debug:
                    print('negative index')
                negative_index = (system * koef)
                if koef != 1:
                    if debug:
                        print('negative result')
                    for _ in range(len(negative_part) - i - 1):
                        system *= IrrationalNum(1, 1)
                    negative_result += (system * 2 ** (i + 1))
                else:
                    negative_result += (2 ** (i + 1))

        return [negative_result, negative_index]

    def Phibase2Dec(self):
        n = self.value.split(".")
        positive_part = n[0]
        negative_part = n[1]
        positive_result, positive_index = self.calcPositivePhiToDec(positive_part)
        negative_result, negative_index = self.calcNegativePhiToDec(negative_part)

       

        result = (positive_result * negative_index) + (negative_result * positive_index)
        index = negative_index * positive_index

        return result + index
    

if __name__ == '__main__':
    num1 = FairyBase(10)
    num2 = FairyBase(10)
    print(num1.value)
    num3 = num1+num2
    print(num1.Phibase2Dec())