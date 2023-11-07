from fairybase import fromPhibase, toPhibaseV2, sumPhibase

n = input()
phibase = toPhibaseV2(int(n))
print(phibase)
print('='*30)
print(fromPhibase(phibase))