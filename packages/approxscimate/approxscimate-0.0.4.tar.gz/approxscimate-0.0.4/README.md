# ApproxSciMate

A python library for approximating SciPy functions with different levels of
accuracy. The library is intended to bring awareness to the energy usage of
computer systems, and to give users a choice in how much they consume.

Read the descriptions of the functions and their levels of approximation below,
pick what is best for your use case.

## Functions

### `cbrt(n, level=0)`

Calculates the cube root of the provided number **n** with the accuracy
specified at the **level**.

* `level = 0` : The default SciPy `cbrt` function providing maximum accuracy.
* `level = 1` : Halley's method for approximating cube roots, for moderate accuracy.
* `level = 2` : Newton's method for approximating cube roots, for low accuracy.

### `comb(n, k, level=0)`

Calculates the amount of possible selections of **k** items from a set of size **n**
where the order of selection **does not** matter. Approximates the value based on the
defined **level** of accuracy.

* `level = 0` : The default SciPy `comb` function providing maximum accuracy.
* `level = 1` : The approximated **lower** bound of the calculation.
* `level = 2` : The approximated **upper** bound of the calculation.
* `level = 3` : Uses Stirling's method of approximating factorials which
  converges to the real value when **n** is very large.

### `perm(n, k, level=0)`

Calculates the amount of possible selections of **k** items from a set of size **n**
where the order of selection **does** matter. Approximates the value based on the
defined **level** of accuracy.

* `level = 0` : The default SciPy `perm` function providing maximum accuracy.
* `level = 1` : The approximated **lower** bound of the calculation.
* `level = 2` : The approximated **upper** bound of the calculation.
* `level = 3` : Uses Stirling's method of approximating factorials which
  converges to the real value when **n** is very large.
