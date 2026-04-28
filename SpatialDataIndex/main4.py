# A.M.: 5361
# Anna Tarasidou

import sys
from r_tree import *
from spatial_queries import knn_query


def load_tree_from_csv(csv_filepath: str) -> RTree:
    tree = RTree()

    try:
        with open(csv_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue

                # Split the line into the 4 main components: node_id, n, f, entries
                parts = line.split(' , ', 3)
                if len(parts) < 4: continue

                node_id = int(parts[0].strip())
                is_leaf = (int(parts[2].strip()) == 0)

                node = Node(node_id, 0 if is_leaf else 1, is_leaf)

                # Split the entries segment
                items = parts[3].strip().split(' , ')

                for item in items:
                    if not item.strip(): continue

                    # Remove brackets and parentheses
                    c = item.replace('(', '').replace(')', '').replace('[', '').replace(']', '')
                    vals = [v.strip() for v in c.split(',')]

                    # Populate Leaf Nodes
                    if is_leaf and len(vals) >= 3:
                        node.add_entry(LeafEntry(int(vals[0]), Point(float(vals[1]), float(vals[2]))))

                    # Populate Intermediate Nodes
                    elif not is_leaf and len(vals) >= 5:
                        node.add_entry(IntermediateEntry(int(vals[0]),
                                                         MBR(float(vals[1]), float(vals[2]), float(vals[3]),
                                                             float(vals[4]))))

                node.calculate_mbr()

                # Append node directly to the tree array
                tree.nodes.append(node)

    except Exception as e:
        print(f"Error loading tree: {e}")
        return None

    return tree


def main():
    # Expecting: python main4.py rtree.csv NNQueries.txt 10
    if len(sys.argv) < 4:
        print("Usage: python main4.py <rtree.csv> <NNQueries.txt> <k>")
        return

    csv_file = sys.argv[1]
    queries_file = sys.argv[2]

    # Read the 'k' parameter from the command line arguments
    k_param = int(sys.argv[3])

    # 1. Load the R-Tree from the CSV
    tree = load_tree_from_csv(csv_file)
    if not tree: return

    # 2. Execute k-Nearest Neighbors Queries
    try:
        with open(queries_file, 'r', encoding='utf-8') as f:
            for query_id, line in enumerate(f):
                # Clean the line from brackets and split by whitespace
                c = line.strip().replace('[', '').replace(']', '').split()

                # We only need x and y from the file now
                if len(c) < 2: continue

                # Create the query center point
                query_point = Point(float(c[0]), float(c[1]))

                # Execute the Best-First Search kNN algorithm
                results = knn_query(tree, query_point, k_param)

                # Extract the record IDs exactly as they were found (ordered by distance)
                ids = [str(r.record_id) for r in results]

                # Print strictly according to the requested format (no spaces after commas)
                if ids:
                    print(f"{query_id}: {','.join(ids)}")
                else:
                    print(f"{query_id} (0): ")

    except Exception as e:
        pass


main()
