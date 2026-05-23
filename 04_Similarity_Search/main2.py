# A.M.: 5361
# Anna Tarasidou
from similarity_search import *


def main2(data_file, num_pivots):
    print("--- Part 2 ---")

    D = load_data(data_file)
    pivots, distances = calculate_pivots_and_distances(D, num_pivots)
    calculate_idistance_index(pivots, distances)


main2("data10K10.txt", 5)
