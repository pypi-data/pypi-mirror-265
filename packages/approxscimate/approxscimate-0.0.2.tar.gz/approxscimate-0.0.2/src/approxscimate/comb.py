import math

import scipy.special as special


def comb(n, k, level=0):
    """
    Calculates the number of ways to choose k items from a set of n distinct items without
    regard to the order of selection. Has different levels of approximation.
    Level=0 is the default SciPy function
    Level=1 indicates an approximated lower bound.
    Level=2 is an approximated higher bound.
    Level=3 is an approximation for large values of n using Stirling's approximation
    :param n: integer
    :param k: integer
    :param level: integer
    :return: integer
    """
    if k > n:
        return 0
    if level == 0:
        return special.comb(n, k)
    if level == 1:
        return (n / k) ** k
    if level == 2:
        return (n ** k) / math.factorial(k)
    if level == 3:
        return (math.sqrt(2 * 3 * n) * (n / 3) ** n) / max(1, ((math.sqrt(2 * 3 * k) * (k / 3) ** k) * (
                math.sqrt(2 * 3 * (n - k)) * ((n - k) / 3) ** (n - k))))
