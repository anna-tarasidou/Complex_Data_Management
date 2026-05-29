# A.M.: 5361
# Anna Tarasidou
import time
import matplotlib.pyplot as plt
from similarity_search import *
from range_queries import *
from knn_queries import *


def main():
    print("Loading data...")
    # Data
    data_path = 'data10K10.txt'
    queries_path = 'queries10.txt'
    num_pivots = 10

    D = load_data(data_path)
    queries = load_data(queries_path)
    num_queries = len(queries)

    pivots, distances_2d = calculate_pivots_and_distances(D, num_pivots)
    idistance_array, maxd_p, maxd = calculate_idistance_index(pivots, distances_2d)

    # Extract keys for binary search in iDistance
    idist_keys = [item[0] for item in idistance_array]

    # EXPERIMENT 1: Range Queries
    epsilons = [0.1, 0.2, 0.4, 0.8]

    # Dictionaries to store results
    range_times = {'Naive': [], 'Pivot': [], 'iDistance': []}
    range_comps = {'Naive': [], 'Pivot': [], 'iDistance': []}

    print("\n--- Evaluating Range Queries ---")
    for eps in epsilons:
        # Naive
        t_start = time.time()
        total_comps = 0
        for q in queries:
            _, comps = range_query_naive(q, eps, D, euclidean_distance)
            total_comps += comps
        range_times['Naive'].append(time.time() - t_start)
        range_comps['Naive'].append(total_comps / num_queries)

        # Pivot-based
        t_start = time.time()
        total_comps = 0
        for q in queries:
            _, comps = range_query_pivot(q, eps, D, pivots, distances_2d, euclidean_distance)
            total_comps += comps
        range_times['Pivot'].append(time.time() - t_start)
        range_comps['Pivot'].append(total_comps / num_queries)

        # iDistance
        t_start = time.time()
        total_comps = 0
        for q in queries:
            _, comps = range_query_idistance(q, eps, D, pivots, idistance_array, idist_keys, maxd, euclidean_distance)
            total_comps += comps
        range_times['iDistance'].append(time.time() - t_start)
        range_comps['iDistance'].append(total_comps / num_queries)

    # EXPERIMENT 2: kNN Queries
    k_values = [1, 5, 10, 50, 100]

    knn_times = {'Naive': [], 'Pivot': [], 'iDistance': []}
    knn_comps = {'Naive': [], 'Pivot': [], 'iDistance': []}

    print("\n--- Evaluating kNN Queries ---")
    for k in k_values:
        # Naive
        t_start = time.time()
        total_comps = 0
        for q in queries:
            _, comps = knn_query_naive(q, k, D, euclidean_distance)
            total_comps += comps
        knn_times['Naive'].append(time.time() - t_start)
        knn_comps['Naive'].append(total_comps / num_queries)

        # Pivot-based
        t_start = time.time()
        total_comps = 0
        for q in queries:
            _, comps = knn_query_pivot(q, k, D, pivots, distances_2d, euclidean_distance)
            total_comps += comps
        knn_times['Pivot'].append(time.time() - t_start)
        knn_comps['Pivot'].append(total_comps / num_queries)

        # iDistance
        t_start = time.time()
        total_comps = 0
        for q in queries:
            _, comps = knn_query_idistance(q, k, D, pivots, idistance_array, idist_keys, maxd_p, maxd,
                                           euclidean_distance)
            total_comps += comps
        knn_times['iDistance'].append(time.time() - t_start)
        knn_comps['iDistance'].append(total_comps / num_queries)

    # Plots
    print("\nGenerating plots...")

    # Range Queries: Epsilon vs Total Time
    plt.figure(figsize=(10, 5))
    plt.plot(epsilons, range_times['Naive'], label='Naive', marker='o')
    plt.plot(epsilons, range_times['Pivot'], label='Pivot-based', marker='s')
    plt.plot(epsilons, range_times['iDistance'], label='iDistance', marker='^')
    plt.xlabel('Epsilon (\u03B5)')
    plt.ylabel('Total Time (seconds)')
    plt.title('Range Queries: Total Time vs Epsilon')
    plt.legend()
    plt.grid(True)
    plt.savefig('diagrams/range_time_plot.png')
    plt.show()

    # Range Queries: Epsilon vs Average Distance Computations
    plt.figure(figsize=(10, 5))
    plt.plot(epsilons, range_comps['Naive'], label='Naive', marker='o')
    plt.plot(epsilons, range_comps['Pivot'], label='Pivot-based', marker='s')
    plt.plot(epsilons, range_comps['iDistance'], label='iDistance', marker='^')
    plt.xlabel('Epsilon (\u03B5)')
    plt.ylabel('Average Distance Computations')
    plt.title('Range Queries: Distance Computations vs Epsilon')
    plt.legend()
    plt.grid(True)
    plt.savefig('diagrams/range_comps_plot.png')
    plt.show()

    # kNN Queries: k vs Total Time
    plt.figure(figsize=(10, 5))
    plt.plot(k_values, knn_times['Naive'], label='Naive', marker='o')
    plt.plot(k_values, knn_times['Pivot'], label='Pivot-based', marker='s')
    plt.plot(k_values, knn_times['iDistance'], label='iDistance', marker='^')
    plt.xlabel('k (Nearest Neighbors)')
    plt.ylabel('Total Time (seconds)')
    plt.title('kNN Queries: Total Time vs k')
    plt.legend()
    plt.grid(True)
    plt.savefig('diagrams/knn_time_plot.png')
    plt.show()

    # kNN Queries: k vs Average Distance Computations
    plt.figure(figsize=(10, 5))
    plt.plot(k_values, knn_comps['Naive'], label='Naive', marker='o')
    plt.plot(k_values, knn_comps['Pivot'], label='Pivot-based', marker='s')
    plt.plot(k_values, knn_comps['iDistance'], label='iDistance', marker='^')
    plt.xlabel('k (Nearest Neighbors)')
    plt.ylabel('Average Distance Computations')
    plt.title('kNN Queries: Distance Computations vs k')
    plt.legend()
    plt.grid(True)
    plt.savefig('diagrams/knn_comps_plot.png')
    plt.show()


main()
