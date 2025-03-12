from functools import singledispatchmethod



class IrrationalNum:
    rational: int
    irrational: int

    
    def __init__(self, A: int, B: int):
        self.rational = A
        self.irrational = B


    @singledispatchmethod
    def __iadd__(self, other) -> "IrrationalNum":
        if not isinstance(other, self.__class__):
            raise SyntaxError(f"IrrationalNum don't sum with {type(other)}")
        
        self.rational += other.rational
        self.irrational += other.irrational
        return self
    

    @__iadd__.register
    def add_int(self, other: int):
        self.rational += other
        return self


    def __add__(self, other) -> "IrrationalNum":
        num = IrrationalNum(self.rational,self.irrational)
        num += other
        return num
    

    @singledispatchmethod
    def __imul__(self, other) -> "IrrationalNum":
        if not isinstance(other, self.__class__):
            raise SyntaxError(f"IrrationalNum don't multiplicate with {type(other)}")
        
        # (A+Bq)*(C+Dq) = ((A*C+5*B*D)+(B*C+A*D)*q)
        self.rational, self.irrational = self.rational*other.rational + 5*self.irrational*other.irrational, \
                                         self.irrational*other.rational + self.rational*other.irrational
        return self
    

    @__imul__.register
    def mul_int(self, other: int):
        self.rational *= other
        self.irrational *= other
        return self
    

    def __mul__(self, other) -> "IrrationalNum":
        num = IrrationalNum(self.rational, self.irrational)
        num *= other
        return num
    

    def __isub__(self, other) -> "IrrationalNum":
        self += other*-1
        return self
    

    def __sub__(self, other) -> "IrrationalNum":
        num = IrrationalNum(self.rational, self.irrational)
        num -= other
        return num


    def __str__(self):
        return f"{self.rational}{'+' if self.irrational>=0 else ''}{self.irrational}√5"


if __name__ == '__main__':
    num1 = IrrationalNum(1, 1)
    num2 = IrrationalNum(1, 1)
    print(num1*num2)
    print(num1)
    print(num1 + 1)
    print(num1 + num1)
    print(IrrationalNum(0, -5))
    print(num1 * 2)
    print(num1*-1)
    print(num1*IrrationalNum(2,2))
    print(num1 - 1)
    print(num1-num1)