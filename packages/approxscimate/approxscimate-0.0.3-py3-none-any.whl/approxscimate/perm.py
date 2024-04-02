import math

import scipy.special as special


def perm(n, k, level=0):
    """
    Calculates the number of ways to arrange k items out of a set of n distinct items,
    where the order of selection matters. Has different levels of accuracy based on the value of level.
    Level=0 is the scipy perm function
    Level=1 is the lower bound approximation
    Level=2 is the upper bound approximation
    Level=3 is the approximation for large values of n using Sterling's method with constants rounded to 0 decimal places
    :param n: integer, total number of items
    :param k: integer, number of items to arrange
    :param level: integer, approximation level
    :return: integer or float, number of arrangements
    """
    if k > n:
        return 0
    if level == 0:
        return special.perm(n, k)
    elif level == 1:
        return math.factorial(k)
    elif level == 2:
        return n ** k
    elif level == 3:
        return (math.sqrt(2 * 3 * n) * (n / 3) ** n) / max(1, (
                math.sqrt(2 * 3 * (n - k)) * ((n - k) / 3) ** (n - k)))
