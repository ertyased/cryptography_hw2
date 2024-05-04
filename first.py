import math

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def all_divisors(a):
    ans = []
    for i in range(1, int(math.sqrt(a)) + 1):
        if i * i == a:
            ans.append(i)
            break
        if a % i == 0:
            ans.append(i)
            ans.append(a // i)
    return ans


def pow(x, p, m):
    if p == 0:
        return 1
    if p % 2 == 1:
        return (pow((x * x) % m, p // 2, m) * x) % m
    return pow((x * x) % m, p // 2, m)


def is_primitive0(p, g):
    divs = sorted(all_divisors(p - 1))
    prev = 0
    s = 1
    for i in divs:
        diff = pow(g, i - prev, p)
        s = (s * diff) % p
        if s == 1:
            return i
        prev = i
    return p - 1


def is_primitive(p, g):
    return is_primitive0(p, g) == p - 1


def brute_force(p, g, a, prime=False):
    pow_ = 1
    for i in range(p):
        pow_ = (pow_ * g) % p
        if pow_ == a:
            return i + 1
    return -1

if __name__ == "__main__":
    pass