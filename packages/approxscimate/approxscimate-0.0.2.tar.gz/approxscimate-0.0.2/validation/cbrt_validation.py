import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from src.approxscimate.cbrt import cbrt


def compare_cbrt(n, levels):
    results = {}
    for level in levels:
        results[level] = cbrt(n, level)
    return results


def main():
    levels = [0, 1, 2]
    print("n\tLevel 0\tLevel 1\tLevel 2")
    level_data = {level: [] for level in levels}
    r = range(1, 100000)
    for n in r:  # Changed the range to 1001 to include 1000
        results = compare_cbrt(n, levels)
        print(f"{n}\t{results[0]}\t{results[1]}\t{results[2]}")
        for level in levels:
            level_data[level].append(results[level])

    # Plotting
    plt.figure(figsize=(10.0, 6.0))

    plt.plot(r, level_data[0], label=f'Level 0 (SciPy)')
    plt.plot(r, level_data[1], label=f'Level 1 (Halley\'s method)')
    plt.plot(r, level_data[2], label=f'Level 2 (Newton\'s method)')

    plt.xlabel('n')
    plt.ylabel('Result')
    plt.title('Comparison of cbrt() on all levels')
    plt.xscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
