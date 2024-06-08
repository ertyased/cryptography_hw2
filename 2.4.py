p = 65537


def pow(base, exponent, modulus=p):
    result = 1
    base = base % modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus

    return result

def log(g, b, k, a):
    print(g, b, k, a)
    check = (pow(g, a) * b) % p
    if check == 1:
        return (p - 1) - a # т. к. (g**x * g**a) = 1
    if pow(check, (p - 1) // (2**k)) == 1:
        return log(g, b, k + 1, a)
    else:
        return log(g, b, k + 1, a + 2**(k - 1))


print(log(12, 9, 1, 0))
