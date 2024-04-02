import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('TkAgg')
from src.approxscimate.comb import comb


def compare_combinatorial(n, k, levels):
    results = {}
    for level in levels:
        results[level] = comb(n, k, level)
    return results


def main():
    levels = [0, 1, 2, 3]
    print("n\tk\tLevel 0\tLevel 1\tLevel 2\tLevel 3")
    for n in range(1, 10):
        for k in range(1, n + 1):
            results = compare_combinatorial(n, k, levels)
            print(f"{n}\t{k}\t{results[0]}\t{results[1]}\t{results[2]}\t{results[3]}")

    # Plotting
    level_data = {level: [] for level in levels}
    r = range(1, 30)
    plt.figure(figsize=(10.0, 6.0))
    for k in r:
        for level in levels:
            level_data[level].append(comb(30, k, level))

    plt.plot(r, level_data[0], label=f'Level 0 (SciPy)')
    plt.plot(r, level_data[1], label=f'Level 1 (lower bound)')
    plt.plot(r, level_data[2], label=f'Level 2 (upper bound)')
    plt.plot(r, level_data[3], label=f'Level 3 (Sterling\'s method)')

    plt.xlabel('k')
    plt.ylabel('Result')
    plt.yscale('log')
    plt.title('Comparison of comb() with n = 30 on all levels')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
