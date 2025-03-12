from math import gcd

# возведение в степень чисел ввида (a+b√5)

def multiplyPhi(system, koef=1, debug: bool = False):

    if debug: print(system, koef, 'multiply start')

    while len(system)!=1: # (A+Bq)*(C+Dq) = ((A*C+5*B*D)+(B*C+A*D)*q)
        if debug: print(system, koef, 'process')
        if system[0].isdigit() and system[1].isdigit():
            system[1] = int(system[0])*int(system[1])
        elif system[1].isdigit():
            A, B = system[0][:-2].split('+')[0], system[0][:-2].split('+')[1]
            system[1] = f'{int(A)*int(system[1])}+{int(B)*int(system[1])}*Q'
        elif system[0].isdigit():
            A, B = system[1][:-2].split('+')[0], system[1][:-2].split('+')[1]
            system[1] = f'{int(A)*int(system[0])}+{int(B)*int(system[0])}*Q'
        else:
            A, B, C, D = system[0][:-2].split('+')[0], system[0][:-2].split('+')[1], system[1][:-2].split('+')[0], system[1][:-2].split('+')[1]
            system[1] = f"{eval(f'({A}*{C}+5*{B}*{D})')}+{eval(f'({B}*{C}+{A}*{D})')}*Q"

        system.pop(0)

    if len(system)==1 and not str(system[0]).isdigit():
        A, B = system[0][:-2].split('+')[0], system[0][:-2].split('+')[1]
        system[0] = f'{int(A)*int(koef)}+{int(B)*int(koef)}*Q'

    if debug: print(system, 'end')
    return str(system[0])


# сумма чисел ввида (a+b√5)

def sumPhi(numbers: list):
    while len(numbers)!=1: # (A+Bq)+(C+Dq) = ((A+C) + (B+D)q)
        if numbers[1].isdigit():
            A,B = numbers[0][:-2].split('+')
            numbers[1] = f"{eval(f'{A}+{numbers[1]}')}+{B}*Q"
        else:
            A, B, C, D = numbers[0][:-2].split('+')[0], numbers[0][:-2].split('+')[1], numbers[1][:-2].split('+')[0], numbers[1][:-2].split('+')[1]
            numbers[1] = f"{eval(f'{A}+{C}')}+{eval(f'{B}+{D}')}*Q"

        numbers.pop(0)
        
    return str(numbers[0])


def sumPhibase(numbers: list, debug: bool = False):
    if debug: print(numbers)
    while len(numbers)!=1:
        pNumber1, nNumber1 = normalizePhi(numbers[0]).split('.')
        pNumber2, nNumber2 = normalizePhi(numbers[1]).split('.')
        pNumber1, pNumber2 = sorted([pNumber1, pNumber2], key=len , reverse=True)
        nNumber1, nNumber2 = sorted([nNumber1, nNumber2], key=len , reverse=True)
        if debug: print('positive numbers', pNumber1, pNumber2)

        pNumber2 = '0'*(len(pNumber1)-len(pNumber2))+pNumber2
        result_pNumber = ''.join([str(int(n1)+int(n2)) for n1, n2 in zip(pNumber1, pNumber2)])
        if debug: print('positive', pNumber1, pNumber2)

        nNumber2 = nNumber2+'0'*(len(nNumber1)-len(nNumber2))
        result_nNumber = ''.join([str(int(n1)+int(n2)) for n1, n2 in zip(nNumber1, nNumber2)])
        if debug: print('negative', nNumber1, nNumber2)

        numbers[1] = normalizePhi(f'{result_pNumber}.{result_nNumber}')
        numbers.pop(0)

    return numbers[0]


# перевод в строчку-математическую форму

def calcPositivePhiToDec(positive_part: str, debug: bool = False):
    zero = positive_part[-1]
    positive_part = positive_part[:-1]
    if debug: print('zero: ', zero)
    positive_result = []
    max_number = 2**len(positive_part)
    for i, number in enumerate(positive_part[::-1]):
        if number=='1':
            # приведение к общему знаменателю
            koef = int(max_number/2**int(i+1))

            system = ['1+1*Q']*(i+1)
            if debug: print('positive result')
            positive_result.append(multiplyPhi(system, koef))

    if zero=='1': return f"{sumPhi([*positive_result, str(max_number)])}/{max_number}"
    return f"{sumPhi(positive_result)}/{max_number}"


def calcNegativePhiToDec(negative_part: str, debug: bool = False):
    negative_result = []
    negative_index = []
    max_index = 2**len(negative_part)
    for i, number in enumerate(negative_part):
        if number=='1':

            koef = int(max_index/2**(i+1))
            if debug: print('koef', koef)

            system = ['1+1*Q']*(i+1)
            if debug: print('negative index')
            negative_index.append(multiplyPhi(system, koef))
            if koef!=1:
                if debug: print('negative result')
                system = ['1+1*Q']*(len(negative_part)-i-1)
                negative_result.append(multiplyPhi(system, 2**(i+1)))
            else:
                negative_result.append(str(2**(i+1)))

    return f"{sumPhi(negative_result)}/{negative_index[-1]}"

    
def fromPhibase(n, debug: bool = False):
    n = n.split('.')
    positive_part = n[0]
    negative_part = n[1]
    positive_result, positive_index = calcPositivePhiToDec(positive_part, debug=debug).split('/')
    negative_result, negative_index = calcNegativePhiToDec(negative_part, debug=debug).split('/')

    if debug:
        print(f'positive number: {positive_result}, / {positive_index}')
        print(f'negative number: {negative_result}, / {negative_index}')

    result = sumPhi([multiplyPhi([positive_result, negative_index], debug=debug), multiplyPhi([positive_index, negative_result], debug=debug)])
    index = multiplyPhi([negative_index,positive_index], debug=debug)

    if debug: print(result, index, '!'*20)

    A,B = result[:-2].split('+')
    nod_result = gcd(int(A),int(B))
    A1=int(A)//nod_result
    B1=int(B)//nod_result

    C,D = index[:-2].split('+')
    nod_index = gcd(int(C),int(D))
    C1=int(C)//nod_index
    D1=int(D)//nod_index

    if int(A1)+int(B1)==int(C1)+int(D1) and nod_result%nod_index==0: # Если получилось целое число
        return nod_result//nod_index
    elif int(A1)+int(B1)==int(C1)+int(D1):
        return f"({nod_result})/{nod_index}"
    else:
        index = eval(f"{int(C)**2}-{int(D)**2*5}") # Если иррациональное
        result = multiplyPhi([f'{A}+{B}*Q', f'{C}+-{D}*Q'], debug=debug)
        if debug: print(result, index)
        A,B = result[:-2].split('+')
        gcd_A = gcd(int(A),index)
        gcd_B = gcd(int(B), index)
        A = int(A) // gcd_A
        index_A = index//gcd_A
        B = int(B) // gcd_B
        index_B = index//gcd_B
        return f'{A}/{index_A}+({B}*√5)/{index_B}'


def normalizePhi(phibase: str, debug: bool = False):
    while '11' in phibase or '1.1' in phibase or '2' in phibase:
        if debug: print(phibase)
        phibase = phibase.replace('011', '100').replace('01.1', '10.0').replace('0.11', '1.00')
        phibase = phibase.replace('0200', '1001').replace('02.21', '10.22').replace('0.220', '1.021').replace('1200','2001').replace('0210', '1011').replace('1220', '2021').replace('0201', '1002').replace('1210', '2011').replace('1201', '2002').replace('1211', '2012').replace('0211', '1012').replace('0.200', '1.001').replace('1.200','2.001').replace('0.210', '1.011').replace('0.201', '1.002').replace('1.210', '2.011').replace('1.201', '2.002').replace('1.211', '2.012').replace('02.00', '10.01').replace('12.00','20.01').replace('02.10', '10.11').replace('02.01', '10.02').replace('12.10', '20.11').replace('12.01', '20.02').replace('12.11', '20.12').replace('020.0', '100.1').replace('120.0','200.1').replace('021.0', '101.1').replace('020.1', '100.2').replace('121.0', '201.0').replace('120.1', '200.2').replace('121.1', '201.2')
        
        if phibase[:2]=='11':
            phibase = '100' + phibase[2:]
        elif phibase[0] == '2':
            phibase = '0' + phibase
        elif phibase[-1]=='2':
            phibase = phibase + '00'
        elif phibase[-2]=='2':
            phibase += '0'
            
    return phibase


def denormalizePhi(phibase: str, debug: bool = False):
    positive_part = phibase.split('.')[0]
    negative_phibase = phibase.split('.')[1][::-1]
    if debug: print(negative_phibase[-2:])
    while negative_phibase[-2:]!='00':
        if debug: print(negative_phibase)
        if negative_phibase[0]=='1':
            negative_phibase = '110'+negative_phibase[1:]
        negative_phibase = negative_phibase.replace('001', '110')
        if debug: print(negative_phibase)
    if positive_part[-1]=='1':
        negative_phibase = negative_phibase[::-1]
        negative_phibase = '11'+negative_phibase[2:]
        return f'{positive_part[:-1]}0.{negative_phibase}'
    else: return f'{positive_part}.{negative_phibase[::-1]}'


def toPhibase(number: int, phibase='10.01', debug: bool = False):
    if debug: print(phibase, 'phibase_normal', number)
    for i in range(number-2):
        positive_part = phibase.split('.')[0]
        negative_part = phibase.split('.')[1]
        if positive_part[-1]=='0':
            phibase = normalizePhi(f'{positive_part[:-1]}1.{negative_part}', debug=debug)
        else:
            phibase = denormalizePhi(phibase, debug=debug)
            phibase = normalizePhi(f"{phibase.split('.')[0][:-1]}1.{phibase.split('.')[1]}", debug=debug)
    

    for i,n in enumerate(phibase[::-1]):
        if n=='1' and i==0: break
        if n=='1':
            phibase = phibase[:-i]
            break
    
    return phibase


def toPhibaseV2(number: int, debug: bool = False):
    res = []
    i=2
    while number-i>4:
        result = '10.01'
        while i*2<number:
            if debug: print(i)
            result = sumPhibase([result,result], debug=debug)
            i*=2
        if debug: print(i, 'number')
        number-=i
        res.append(result)
        i = 2
    result = sumPhibase(res)
    
    return toPhibase(number-i+4, result, debug)


def toPhibaseIrr(number: str):
    print(number)
    A,s,D = number.split('/')
    B,C = s.split('+')
    print(B,D, type(max(B,D)))
    C = C[1:-3]
    A = int(eval(f'{A}*({B}/(max({B},{D})))'))
    C = int(eval(f'{C}*({D}/(max({B},{D})))'))
    D = int(D)
    B = int(B)

    if C>A or max(B,D)>2:
        return 'Не может быть переведенно'
    
    

    if max(B,D) == 1:
        return f'({A*2}+{C*2}*Q)/{max(B,D*2)}'
    return f'({A}+{C}*Q)/{max(B,D)}'