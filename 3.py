import math
import sympy
from sympy import sqrt_mod, Mod, mod_inverse
import numpy as np

def L(n):
    log_n = math.log(n)
    loglog_n = math.log(log_n)
    power = math.sqrt(log_n * loglog_n)
    return math.exp(power)


def sieve(n):
    prime = [True] * (n + 1)
    result = []
    for p in range(2, n + 1):
        if prime[p]:
            result.append(p)
            for i in range(p * p, n + 1, p):
                prime[i] = False
    return result


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def rotate(matrix):
    ans = []
    for j in range(len(matrix[0])):
        res = []
        for i in range(len(matrix)):
            res.append(matrix[i][j])
        ans.append(res)
    return ans


def diff_lines(a, b):
    return [(a[i] - b[i]) % 2 for i in range(len(a))]



def solve_mod2(matrix):
    matrix = rotate(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = matrix[i][j] % 2
    i = 0
    solved = set()
    solved_list = []
    for i1 in range(len(matrix[0])):
        found = False
        for j in range(i, len(matrix)):
            if matrix[j][i1] != 0:
                matrix[i], matrix[j] = matrix[j], matrix[i]
                found = True
                break
        if not found:
            continue
        for j in range(i + 1, len(matrix)):
            if matrix[j][i1] == 1:
                matrix[j] = diff_lines(matrix[j], matrix[i])
        for j in range(i):
            if matrix[j][i1] == 1:
                matrix[j] = diff_lines(matrix[j], matrix[i])
        solved_list.append(i1)
        solved.add(i1)
        i += 1
    answer = []
    for i in range(len(matrix[0])):
        if i in solved:
            continue
        new_result = [0] * len(matrix[0])
        new_result[i] = 1
        for j in range(len(solved_list)):
            if matrix[j][i] == 1:
                new_result[solved_list[j]] = 1
        answer.append(new_result)
    return answer


def quadratic_sieve_factor(n):
    a = 1000000
    sqrt_n = round(math.sqrt(n))
    t = [(sqrt_n + i) ** 2 - n for i in range(0, a + 1)]
    tmp_primes = sieve(3000)
    primes = [i for i in tmp_primes if pow(n, i // 2, i) == 1]
    divisors = [[0] * len(primes) for i in range(len(t))]
    for j in range(len(primes)):
        prime = primes[j]
        num = prime
        while num < t[-1]:
            roots = sqrt_mod(n, num, True)
            if len(roots) == 0:
                break
            for root in roots:
                root = (root - sqrt_n) % num
                for i in range(root, len(t), num):
                    t[i] //= prime
                    divisors[i][j] += 1
            num *= prime
    smooth = []
    matrix = []
    for i in range(len(t)):
        if t[i] != 1:
            continue
        smooth.append(i + sqrt_n)
        matrix.append(divisors[i])
    print(smooth)
    for i in solve_mod2(matrix):
        num1 = 1
        num2 = [0] * len(primes)
        for j in range(len(i)):
            if i[j] == 1:
                num1 *= smooth[j]
                for k in range(len(matrix[0])):
                    num2[k] += matrix[j][k]
        num2final = 1
        for j in range(len(num2)):
            num2final *= primes[j] ** (num2[j // 2])
        div = gcd(n, (num1 - num2final) % n)
        if div != 1 and div != n:
            return div
    return -1

if __name__ == "__main__":
    #код работает где-то до 20 значных чисел, занимает некоторое время, но работает
    print(quadratic_sieve_factor(152319825198351672856))
