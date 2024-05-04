from first import *
from random import randint
from sympy import mod_inverse
import time

def extended_gcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1

    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0


def inverse(x, p):
    return pow(x, p - 2, p)


def Babystep_giantstep(p, g, a, prime=False):
    N = 0
    if prime:
        N = p - 1
    else:
        N = is_primitive0(p, g)
    n = int(N ** (1 / 2)) + 1
    dict1 = dict()
    dict1[1] = 0
    num = 1
    for i in range(1, n + 1):
        num = (num * g) % p
        dict1[num] = i
    inv = inverse(pow(g, n, p), p)
    num = a
    for i in range(n + 1):
        if num in dict1:
            return i * n + dict1[num]
        num = (num * inv) % p
    return -1


def probabilistic_collision_method(p, g, a, prime=False):
    N = 0
    if prime:
        N = p - 1
    else:
        N = is_primitive0(p, g)
    dict1 = dict()
    dict2 = dict()
    id = 0
    while True:
        num = randint(1, N)
        num1 = pow(g, num, p)
        num2 = (a * num1) % p

        def answer(c, d):
            return (c - d) % N

        if num1 in dict2:
            return answer(num, dict2[num1])
        if num2 in dict1:
            return answer(dict1[num2], num)
        dict1[num1] = num
        dict2[num2] = num
        id += 1




def pollard_rho(p, g, h, prime=False):
    order = 0
    if prime:
        order = p - 1
    else:
        order1 = is_primitive0(p, g)
        order2 = is_primitive0(p, h)
        order = order1 * order2 // gcd(order1, order2)
    first = [0, 0, 1]
    second = [0, 0, 1]

    def update_uv(u, v, z):
        if z < p // 3:
            return (u + 1) % (p - 1), v
        elif z < 2 * p // 3:
            return (2 * u) % (p - 1), (2 * v) % (p - 1)
        else:
            return u % (p - 1), (v + 1) % (p - 1)

    def update(a):
        u, v = update_uv(a[0], a[1], a[2])
        return [u, v, (pow(g, u, p) * pow(h, v, p)) % p]

    while True:
        first = update(first)
        second = update(update(second))
        if first[2] == second[2]:
            a = first[0]
            b = first[1]
            c = second[0]
            d = second[1]
            fp = (a - c) % order
            sp = (d - b) % order
            gc, x, y = extended_gcd(sp, p - 1)
            if gc == 1:
                return sp * inverse(fp, p - 1)
            x = x % order
            fp = (x * fp) % order
            sp = gc
            new_gc = gcd(sp, gcd(order, fp))
            new_p = order // new_gc
            fp = fp // new_gc
            sp = sp // new_gc
            fp = (fp * mod_inverse(sp, new_p)) % new_p
            for i in range(gc):
                if pow(g, fp + i * new_p, p) == h:
                    return fp + i * new_p
            return -1

def test_all(am, p, g):
    funcs = {"brute": brute_force, "babystep": Babystep_giantstep, "probability": probabilistic_collision_method, "pollard": pollard_rho}
    testing = [randint(1, p) for i in range(am)]
    for i in funcs:
        print(f"Testing {i}:")
        start = time.time()
        for id, h in enumerate(testing):
            if (id + 1) % 10 == 0:
                print("tested:", id + 1)
            res = funcs[i](p, g, h, True)
            if (g**res) % p != h:
                print("ERROR while testing", g, h, res)
        all = (time.time() - start)
        print(f"{am} runs completed in: {all} seconds. Avg time for run: {all / am}")




if __name__ == "__main__":
    print(is_primitive(9999991, 22))
    test_data = [[100, 1000003, 7], [10, 9999991, 22], [1, 1000000007, 13]]
    for amount, mod, root in test_data:
        print(f"testing for amount: {amount} with mod: {mod} and root: {root}")
        test_all(amount, mod, root)
