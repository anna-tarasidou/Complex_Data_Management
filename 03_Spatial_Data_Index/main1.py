# A.M.: 5361
# Anna Tarasidou

import sys
from spatial_queries import *


def main1():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "Beijing_restaurants.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "rtree.csv"

    leaf_entries = load_data(input_file)

    if leaf_entries:
        print(f"Successfully loaded {len(leaf_entries)} points.")
    else:
        print("No data loaded. Exiting.")
        return

    tree = RTree()
    tree.build_tree(leaf_entries)
    print("Tree built successfully.")

    tree.print_statistics()

    tree.export_csv(output_file)
    print(f"Export complete: {output_file}")


main1()
