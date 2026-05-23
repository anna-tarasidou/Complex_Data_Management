# A.M.: 5361
# Anna Tarasidou
from similarity_search import load_data, calculate_pivots_and_distances


def main1(data_file, num_pivots):
    print("--- Part 1 ---")
    D = load_data(data_file)
    print(f"Loaded {len(D)} objects from {data_file}")

    pivots, distances = calculate_pivots_and_distances(D, num_pivots)
    print(f"pivots: {pivots}")


main1("data10K10.txt", 5)
