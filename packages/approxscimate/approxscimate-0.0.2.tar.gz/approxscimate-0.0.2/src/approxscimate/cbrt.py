import scipy.special as sp


def cbrt(n, level=0):
    """
    Approximates the cube root of each element in the input array x with different levels of accuracy.
    Level=0 uses scipy's cbrt function for the highest accuracy.
    Level=1 uses Halleys's method of simple approximation of cube root for moderate accuracy.
    Level=2 uses Newton's method of simple approximation of cube root for low accuracy.
    :param n: integer
    :param level: integer (0, 1, or 2)
    :return: integer
    """
    if level == 0:
        return sp.cbrt(n)
    elif level == 1:
        return halleys_method(n)
    elif level == 2:
        return newtons_method(n)


def newtons_method(x, max_iterations=7):
    """
    Simple approximation of cube root using Newton's method.
    """
    guess = x / 3
    iterations = 0
    while abs(guess ** 3 - x) > 3 and iterations < max_iterations:
        guess = guess - (guess ** 3 - x) / (3 * guess ** 2)  # Newton's method formula
        iterations += 1

    return guess


def halleys_method(x, max_iterations=7):
    """
    Simple approximation of cube root using Halley's method.
    """
    guess = x / 3
    iterations = 0
    while abs(guess ** 3 - x) > 3 and iterations < max_iterations:
        numerator = guess * (guess ** 3 + 2 * x)
        denominator = 2 * (guess ** 3) + x
        guess = numerator / denominator
        iterations += 1

    return guess
