# A.M.: 5361
# Anna Tarasidou
import sys
from spatial_queries import *


def load_tree_from_csv(csv_filepath):
    tree = RTree()

    with open(csv_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(' , ', 3)
            if len(parts) < 4:
                continue

            node_id = int(parts[0].strip())
            is_leaf = (int(parts[2].strip()) == 0)

            node = Node(node_id, 0 if is_leaf else 1, is_leaf)
            items = parts[3].strip().split(' , ')

            for item in items:
                if not item.strip():
                    continue

                c = item.replace('(', '').replace(')', '').replace('[', '').replace(']', '')
                vals = [v.strip() for v in c.split(',')]

                if is_leaf and len(vals) >= 3:
                    node.add_entry(LeafEntry(int(vals[0]), Point(float(vals[1]), float(vals[2]))))
                elif not is_leaf and len(vals) >= 5:
                    node.add_entry(IntermediateEntry(int(vals[0]),
                                                     MBR(float(vals[1]), float(vals[2]), float(vals[3]),
                                                         float(vals[4]))))

            node.calculate_mbr()
            tree.nodes.append(node)

    return tree


def main3():
    if len(sys.argv) < 3:
        return

    csv_file = sys.argv[1]
    queries_file = sys.argv[2]

    tree = load_tree_from_csv(csv_file)
    if not tree:
        return

    with open(queries_file, 'r', encoding='utf-8') as f:
        for query_id, line in enumerate(f):
            c = line.strip().replace('[', '').replace(']', '').split()

            if len(c) < 3:
                continue

            center = Point(float(c[0]), float(c[1]))
            radius = float(c[2])

            results = distance_range_query(tree, center, radius)

            ids = [str(r.record_id) for r in results]

            if ids:
                print(f"{query_id} ({len(ids)}): {','.join(ids)}")
            else:
                print(f"{query_id} (0): ")


main3()
