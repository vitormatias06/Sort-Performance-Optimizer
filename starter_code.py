"""
Sorting Assignment Starter Code
Implement four sorting algorithms and benchmark their performance.
"""

import json
import time
import tracemalloc


# ============================================================================
# PART 1: SORTING IMPLEMENTATIONS
# ============================================================================

def bubble_sort(arr):
    """Sort a list in ascending order using Bubble Sort."""
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


def selection_sort(arr):
    """Sort a list in ascending order using Selection Sort."""
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def insertion_sort(arr):
    """Sort a list in ascending order using Insertion Sort."""
    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def merge_sort(arr):
    """Sort a list in ascending order using Merge Sort."""
    if len(arr) <= 1:
        return arr.copy()

    middle = len(arr) // 2

    left = merge_sort(arr[:middle])
    right = merge_sort(arr[middle:])

    return merge(left, right)


def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = 0
    j = 0

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


# ============================================================================
# PART 2: STABILITY DEMONSTRATION
# ============================================================================

def demonstrate_stability():
    """
    Demonstrate whether sorting algorithms preserve the original order
    of products with equal prices.
    """

    products = [
        {"name": "Widget A", "price": 1999, "original_position": 0},
        {"name": "Gadget B", "price": 999, "original_position": 1},
        {"name": "Widget C", "price": 1999, "original_position": 2},
        {"name": "Tool D", "price": 999, "original_position": 3},
        {"name": "Widget E", "price": 1999, "original_position": 4},
    ]

    def bubble_products(items):
        items = items.copy()

        for i in range(len(items)):
            for j in range(len(items) - i - 1):
                if items[j]["price"] > items[j + 1]["price"]:
                    items[j], items[j + 1] = items[j + 1], items[j]

        return items

    def selection_products(items):
        items = items.copy()

        for i in range(len(items)):
            min_index = i

            for j in range(i + 1, len(items)):
                if items[j]["price"] < items[min_index]["price"]:
                    min_index = j

            items[i], items[min_index] = items[min_index], items[i]

        return items

    def insertion_products(items):
        items = items.copy()

        for i in range(1, len(items)):
            key = items[i]
            j = i - 1

            while j >= 0 and items[j]["price"] > key["price"]:
                items[j + 1] = items[j]
                j -= 1

            items[j + 1] = key

        return items

    def merge_product_sort(items):
        if len(items) <= 1:
            return items.copy()

        middle = len(items) // 2
        left = merge_product_sort(items[:middle])
        right = merge_product_sort(items[middle:])

        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if left[i]["price"] <= right[j]["price"]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    algorithms = {
        "bubble_sort": bubble_products,
        "selection_sort": selection_products,
        "insertion_sort": insertion_products,
        "merge_sort": merge_product_sort,
    }

    results = {}

    for name, algorithm in algorithms.items():
        sorted_products = algorithm(products)

        # Check whether equal-price products retain their original order.
        stable = True
        prices = set(product["price"] for product in products)

        for price in prices:
            original_positions = [
                product["original_position"]
                for product in products
                if product["price"] == price
            ]

            sorted_positions = [
                product["original_position"]
                for product in sorted_products
                if product["price"] == price
            ]

            if original_positions != sorted_positions:
                stable = False
                break

        results[name] = "Stable" if stable else "Unstable"

    return results


# ============================================================================
# PART 3: PERFORMANCE BENCHMARKING
# ============================================================================

def load_dataset(filename):
    """Load a dataset from a JSON file."""
    with open(f"datasets/{filename}", "r") as file:
        return json.load(file)


def load_test_cases():
    """Load test cases for validation."""
    with open("datasets/test_cases.json", "r") as file:
        return json.load(file)


def test_sorting_correctness():
    """Test that all sorting functions work correctly."""

    print("=" * 70)
    print("TESTING SORTING CORRECTNESS")
    print("=" * 70)

    test_cases = load_test_cases()

    test_names = [
        "small_random",
        "small_sorted",
        "small_reverse",
        "small_duplicates",
    ]

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
    }

    all_passed = True

    for test_name in test_names:
        print(f"\nTest: {test_name}")
        print(f"Input:    {test_cases[test_name]}")
        print(f"Expected: {test_cases['expected_sorted'][test_name]}")

        for algo_name, algo_func in algorithms.items():
            try:
                result = algo_func(test_cases[test_name].copy())
                expected = test_cases["expected_sorted"][test_name]
                passed = result == expected

                status = "PASS" if passed else "FAIL"

                if not passed:
                    all_passed = False

                print(f"  {algo_name:20s}: {status}")

            except Exception as error:
                all_passed = False
                print(f"  {algo_name:20s}: ERROR - {error}")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")

    return all_passed


def benchmark_algorithm(sort_func, data):
    """
    Benchmark a sorting algorithm.

    Returns:
        tuple: (execution_time_ms, peak_memory_kb)
    """

    # Exclude the input copy from the measured sorting operation.
    data_copy = data.copy()

    tracemalloc.start()

    try:
        start_time = time.perf_counter()
        result = sort_func(data_copy)
        end_time = time.perf_counter()

        current, peak = tracemalloc.get_traced_memory()

    finally:
        tracemalloc.stop()

    # Keep the result alive until after memory measurement.
    del result

    execution_time_ms = (end_time - start_time) * 1000
    peak_memory_kb = peak / 1024

    return execution_time_ms, peak_memory_kb


def benchmark_all_datasets():
    """Benchmark the four sorting algorithms on all four datasets."""

    print("\n" + "=" * 90)
    print("BENCHMARKING SORTING ALGORITHMS")
    print("=" * 90)

    datasets = {
        "orders.json": ("Order Processing Queue", 50000, 5000),
        "products.json": ("Product Search Results", 100000, 5000),
        "inventory.json": ("Inventory Reconciliation", 25000, 5000),
        "activity_log.json": ("Customer Activity Log", 75000, 5000),
    }

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
    }

    for filename, (description, full_size, sample_size) in datasets.items():
        print(f"\nDataset: {description}")
        print(f"File: {filename}")
        print(f"Sample size: {sample_size:,} elements")
        print("-" * 70)

        data = load_dataset(filename)
        data_sample = data[:sample_size]

        for algo_name, algo_func in algorithms.items():
            try:
                exec_time, memory = benchmark_algorithm(
                    algo_func,
                    data_sample
                )

                print(
                    f"{algo_name:20s}: "
                    f"{exec_time:10.2f} ms | "
                    f"{memory:10.2f} KB"
                )

            except Exception as error:
                print(f"{algo_name:20s}: ERROR - {error}")

    print("\nBenchmarking complete.")


def analyze_stability():
    """Display the stability results."""

    print("\n" + "=" * 70)
    print("STABILITY ANALYSIS")
    print("=" * 70)

    results = demonstrate_stability()

    for algo_name, stability in results.items():
        print(f"{algo_name:20s}: {stability}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("SORTING ASSIGNMENT")
    print("Four sorting algorithms, stability, and performance analysis.")

    # Run correctness tests first.
    tests_passed = test_sorting_correctness()

    if tests_passed:
        analyze_stability()

        # Enable benchmarking after confirming the dataset files exist.
        benchmark_all_datasets()
    else:
        print("\nFix the sorting errors before running benchmarks.")

