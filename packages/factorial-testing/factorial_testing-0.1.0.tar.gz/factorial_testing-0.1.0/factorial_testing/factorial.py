def fact(n):
    if n < 0:
        raise ValueError('Factorial is not defined for negative numbers')
    elif n <= 1:
        return 1
    return n * fact(n-1)