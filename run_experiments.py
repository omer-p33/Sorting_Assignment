import argparse
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, stdev


def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left =merge_sort(arr[:mid])
    right =merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def get_algorithm(algo_id):
    algorithms = {
        1: ("Bubble Sort",bubble_sort),
        2: ("Merge Sort",merge_sort),
        3: ("Quick Sort",quick_sort),
    }
    return algorithms[algo_id]


def measure_sort_time(sort_func, arr):
    start = time.perf_counter()
    sorted = sort_func(arr.copy())
    end = time.perf_counter()
    return end - start


def run_experiment_1(algo_ids, sizes, repetitions):
    """Run experiment on random arrays"""
    results = {algo_id: [] for algo_id in algo_ids}

    for size in sizes:
        algo_times = {algo_id: [] for algo_id in algo_ids}

        for rep in range(repetitions):
            arr = [random.randint(0, 100000) for sample in range(size)]

            for algo in algo_ids:
                sort_name, sort_func = get_algorithm(algo)
                measured_time = measure_sort_time(sort_func, arr)
                algo_times[algo].append(measured_time)

        for algo in algo_ids:
            results[algo].append({
                'size': size,
                'avg': mean(algo_times[algo]),
                'stdev': stdev(algo_times[algo])
            })
        print(f"{size}-finished", flush=True)
    return results


def run_experiment_2(algo_ids, sizes, repetitions, noise_percentage):
    """Run experiment on nearly sorted arrays with noise"""
    results = {algo_id: [] for algo_id in algo_ids}

    for size in sizes:
        algo_times = {algo_id: [] for algo_id in algo_ids}

        for rep in range(repetitions):
            arr = list(range(size))
            num_swaps = int(size * noise_percentage / 100)//2
            for swap in range(num_swaps):
                i, j = random.randint(0, size - 1), random.randint(0, size - 1)
                arr[i], arr[j] = arr[j], arr[i]

            for algo in algo_ids:
                sort_name, sort_func = get_algorithm(algo)
                measured_time = measure_sort_time(sort_func, arr)
                algo_times[algo].append(measured_time)

        for algo_id in algo_ids:
            results[algo_id].append({
                'size': size,
                'avg': mean(algo_times[algo_id]),
                'stdev': stdev(algo_times[algo_id]) if len(algo_times[algo_id]) > 1 else 0
            })
        print(f"{size}-finished", flush=True)
    return results


def plot_results(results, sizes, algo_ids, title, filename):
    """Plot experiment results with error bars"""
    plt.figure(figsize=(12, 7))

    for algo in algo_ids:
        algo_name, algo_func = get_algorithm(algo)
        algo_results = results[algo]

        sizes_list = [result['size'] for result in algo_results]
        avgs = [result['avg'] for result in algo_results]
        stdevs = [result['stdev'] for result in algo_results]

        upper = [avg + std for avg, std in zip(avgs, stdevs)]
        lower = [avg - std for avg, std in zip(avgs, stdevs)]

        plt.plot(sizes_list, avgs, marker='o', label=algo_name, linewidth=2)
        plt.fill_between(sizes_list, lower, upper, alpha=0.2)

    plt.xlabel('Array size (n)', fontsize=12)
    plt.ylabel('Runtime (seconds)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

    print(f"Plot saved to {filename}")

"""def export_table_png(results, sizes, algo_ids, title, filename):
    #Export results as a formatted table image (PNG)
    # Prepare data for the table
    cell_text = []
    row_labels = []
    col_labels = [f"N={size}" for size in sizes]

    for algo_id in algo_ids:
        algo_name, _ = get_algorithm(algo_id)
        row_labels.append(algo_name)

        # Map size to average time for easy lookup
        algo_results = {r['size']: r['avg'] for r in results[algo_id]}
        # Format numbers to 6 decimal places
        row_data = [f"{algo_results.get(size, 0):.6f}" for size in sizes]
        cell_text.append(row_data)

    # Create figure and axis (dynamically adjust size based on columns/rows)
    fig, ax = plt.subplots(figsize=(max(8, len(sizes) * 1.5), len(algo_ids) * 0.5 + 1.5))

    ax.axis('off')
    ax.axis('tight')

    # Add title
    plt.title(title, fontsize=14, fontweight='bold', pad=20)

    # Create the table
    table = ax.table(cellText=cell_text,
                     rowLabels=row_labels,
                     colLabels=col_labels,
                     loc='center',
                     cellLoc='center')

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)  # Scale column widths (1x) and row heights (2x)

    # Save the table as an image
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Table image saved to {filename}")"""


def main():
    parser = argparse.ArgumentParser(description='Sorting Algorithm Comparison')
    parser.add_argument('-a', '--algorithms', nargs='+', type=int, default=[1, 2, 3], help='Algorithm IDs (1=Bubble, 2=Merge, 3=Quick)')

    parser.add_argument('-s', '--sizes', nargs='+', type=int, default=[512*i for i in range(16)], help='Array sizes to test')

    parser.add_argument('-e', '--experiment', type=int, default=0, help='Experiment type: 0=random, 1=nearly-sorted 5%%, 2=nearly-sorted 20%%')

    parser.add_argument('-r', '--repetitions', type=int, default=5, help='Number of repetitions per size')

    args = parser.parse_args()

    print(f"Running experiment with algorithms: {args.algorithms}")
    print(f"Array sizes: {args.sizes}")
    print(f"Repetitions: {args.repetitions}")

    if args.experiment == 0:
        print("Experiment type: Random arrays")
        results = run_experiment_1(args.algorithms, args.sizes, args.repetitions)

        plot_results(results, args.sizes, args.algorithms,'Runtime Comparison (Random Arrays)', 'result1.png')

        export_table_png(results, args.sizes, args.algorithms,'Mean Running Time (Random Arrays)', 'result1_table.png')

    elif args.experiment == 1:
        print("Experiment type: Nearly-sorted arrays (5% noise)")
        results = run_experiment_2(args.algorithms, args.sizes, args.repetitions, 5)

        plot_results(results, args.sizes, args.algorithms, 'Runtime Comparison (Nearly Sorted, 5% Noise)', 'result2.png')

        export_table_png(results, args.sizes, args.algorithms, 'Mean Running Time (5% Noise)', 'result2_table.png')

    elif args.experiment == 2:
        print("Experiment type: Nearly-sorted arrays (20% noise)")
        results = run_experiment_2(args.algorithms, args.sizes, args.repetitions, 20)

        plot_results(results, args.sizes, args.algorithms, 'Runtime Comparison (Nearly Sorted, 20% Noise)', 'result3.png')

        export_table_png(results, args.sizes, args.algorithms, 'Mean Running Time (20% Noise)', 'result3_table.png')

    print("Experiment completed!")


if __name__ == '__main__':
    main()
