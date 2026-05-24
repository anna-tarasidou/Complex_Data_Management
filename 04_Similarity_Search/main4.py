# A.M.: 5361
# Anna Tarasidou
import time
from similarity_search import *
from knn_queries import *


def main4(data_file, queries_file, num_pivots, k):
    print(f"--- Part 4 (K-NN Queries with K = {k}) ---")

    # Load the datasets
    D = load_data(data_file)
    queries = load_data(queries_file)

    # Calculate indices (Pivots & iDistance)
    pivots, distances_2d = calculate_pivots_and_distances(D, num_pivots)
    idistance_array, maxd_p, maxd = calculate_idistance_index(pivots, distances_2d)

    # Extract keys for faster binary search
    idist_keys = [item[0] for item in idistance_array]

    total_comps_naive, total_comps_pivot, total_comps_idist = 0, 0, 0

    # Naive k-NN
    start_time = time.time()
    for q in queries:
        _, comps = knn_query_naive(q, k, D, euclidean_distance)
        total_comps_naive += comps
    time_naive = time.time() - start_time

    # Pivot-based k-NN
    start_time = time.time()
    for q in queries:
        _, comps = knn_query_pivot(q, k, D, pivots, distances_2d, euclidean_distance)
        total_comps_pivot += comps
    time_pivot = time.time() - start_time

    # 3. iDistance k-NN
    start_time = time.time()
    for q in queries:
        _, comps = knn_query_idistance(q, k, D, pivots, idistance_array, idist_keys, maxd_p, maxd, euclidean_distance)
        total_comps_idist += comps
    time_idist = time.time() - start_time

    # Calculate averages and print the evaluation results
    num_queries = len(queries)
    print(f"average distance comp per query (Naive k-NN) = {total_comps_naive / num_queries}")
    print(f"average distance comp per query (Pivot-based k-NN) = {total_comps_pivot / num_queries}")
    print(f"average distance comp per query (iDistance k-NN) = {total_comps_idist / num_queries}")
    print(f"total time Naive k-NN = {time_naive}")
    print(f"total time Pivot-based k-NN = {time_pivot}")
    print(f"total time iDistance k-NN = {time_idist}")


main4("data10K10.txt", "queries10.txt", 10, 5)
