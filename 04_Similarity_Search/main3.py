# A.M.: 5361
# Anna Tarasidou
import time
from similarity_search import *
from range_queries import *


def main3(data_file, query_file, num_pivots, epsilon):
    print("--- Part 3 ---")
    D = load_data(data_file)
    queries = load_data(query_file)

    pivots, distances_2d = calculate_pivots_and_distances(D, num_pivots)
    idistance_array, maxd_p, maxd = calculate_idistance_index(pivots, distances_2d)

    idist_keys = [item[0] for item in idistance_array]

    total_comps_naive, total_comps_pivot, total_comps_idist = 0, 0, 0

    # 1. Naive
    start_time = time.time()
    for q in queries:
        _, comps = range_query_naive(q, epsilon, D, euclidean_distance)
        total_comps_naive += comps
    time_naive = time.time() - start_time

    # 2. Pivot-based
    start_time = time.time()
    for q in queries:
        _, comps = range_query_pivot(q, epsilon, D, pivots, distances_2d, euclidean_distance)
        total_comps_pivot += comps
    time_pivot = time.time() - start_time

    # 3. iDistance
    start_time = time.time()
    for q in queries:
        _, comps = range_query_idistance(q, epsilon, D, pivots, idistance_array, idist_keys, maxd, euclidean_distance)
        total_comps_idist += comps
    time_idist = time.time() - start_time

    num_queries = len(queries)
    print(f"average distance comp per query (Naive) = {total_comps_naive / num_queries}")
    print(f"average distance comp per query (Pivot-based) = {total_comps_pivot / num_queries}")
    print(f"average distance comp per query (iDistance) = {total_comps_idist / num_queries}")
    print(f"total time Naive = {time_naive}")
    print(f"total time Pivot-based = {time_pivot}")
    print(f"total time iDistance = {time_idist}")


main3("data10K10.txt", "queries10.txt", 10, 0.2)
