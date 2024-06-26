def eulersFunction(n: int or str) -> int:
    n = int(n)
    res = n
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            while n % d == 0:
                n //= d
            res -= res // d
    if n > 1:
        res -= res // n
    return res


def eulersFunctionFull(n: int or str) -> dict:
    n = int(n)
    ret = {}
    ret['all'] = []
    res = n
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            while n % d == 0:
                n //= d
            ret['all'].append(d)
            res -= res // d
    if n > 1:
        res -= res // n
    ret['res'] = res
    return ret


def numberIntoPrimeFactors(n: int or str) -> list:
    n = int(n)
    i = 2
    primfacs = []
    while i * i <= n:
        while n % i == 0:
            primfacs.append(i)
            n = n // i
        i = i + 1
    if n > 1:
        primfacs.append(n)
    return primfacs


def cononicalNumber(n: int or str) -> str:
    n = int(n)
    primfacs = numberIntoPrimeFactors(n)
    ret = ''
    for i in primfacs:
        ret += str(i)
        if primfacs.count(i) > 1:
            ret += '^' + str(primfacs.count(i))
        ret += '*'
        primfacs.remove(i)
    return ret[:-1]


if __name__ == '__main__':
    print(cononicalNumber(441))
