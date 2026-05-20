# A.M.: 5361
# Anna Tarasidou
import time
from similarity_search import *
from range_queries import *


def main():

    # --- MEROS 1 ---
    print(f"\n--- Part 1 ---")

    DATA_FILE = "data10K10.txt"
    NUM_PIVOTS = 5

    D1 = load_data(DATA_FILE)
    print(f"Loaded {len(D1)} objects with {len(D1[0]) if D1 else 0} dimensions.")

    pivots, distances = calculate_pivots_and_distances(D1, NUM_PIVOTS)

    print(f"pivots: {pivots}\n")

    # Distance of Object 0 to the 5 pivots
    # print(f"Distances of Object 0 to pivots: {distances[0]}")

    # --- MEROS 2 ---
    print(f"\n--- Part 2 ---")

    # Calculate the iDistance index
    idistance_array, maxd_p, maxd = calculate_idistance_index(pivots, distances)

    print(f"Global maxd: {maxd}")
    print(f"maxd per pivot: {maxd_p}")
    print(f"iDistance array created and sorted. First 5 entries (iDist, Object_ID):")
    for i in range(5):
        print(f"  {idistance_array[i]}")

    # --- MEROS 3 ---
    print(f"\n--- Part 3 ---")

    DATA_FILE = "data10K10.txt"
    QUERIES_FILE = "queries10.txt"
    NUM_PIVOTS = 10
    EPSILON = 0.2

    D2 = load_data(DATA_FILE)
    queries = load_data(QUERIES_FILE)

    pivots, distances_2d = calculate_pivots_and_distances(D2, NUM_PIVOTS)
    idistance_array, maxd_p, maxd = calculate_idistance_index(pivots, distances_2d)

    idist_keys = [item[0] for item in idistance_array]

    total_comps_naive, total_comps_pivot, total_comps_idist = 0, 0, 0

    # Naive
    start_time = time.time()
    for q in queries:
        _, comps = range_query_naive(q, EPSILON, D2, euclidean_distance)
        total_comps_naive += comps
    time_naive = time.time() - start_time

    # Pivot-based
    start_time = time.time()
    for q in queries:
        _, comps = range_query_pivot(q, EPSILON, D2, pivots, distances_2d, euclidean_distance)
        total_comps_pivot += comps
    time_pivot = time.time() - start_time

    # iDistance
    start_time = time.time()
    for q in queries:
        _, comps = range_query_idistance(q, EPSILON, D2, pivots, idistance_array, idist_keys, maxd, euclidean_distance)
        total_comps_idist += comps
    time_idist = time.time() - start_time

    # Calculate averages
    num_queries = len(queries)
    avg_comps_naive = total_comps_naive / num_queries
    avg_comps_pivot = total_comps_pivot / num_queries
    avg_comps_idist = total_comps_idist / num_queries

    # Output the results
    print(f"average distance comp per query (Naive) = {avg_comps_naive}")
    print(f"average distance comp per query (Pivot-based) = {avg_comps_pivot}")
    print(f"average distance comp per query (iDistance) = {avg_comps_idist}")
    print(f"total time Naive = {time_naive}")
    print(f"total time Pivot-based = {time_pivot}")
    print(f"total time iDistance = {time_idist}")


main()
