# A.M.: 5361
# Anna Tarasidou

from r_tree import Point, MBR, Node, RTree


def is_point_inside_mbr(point: Point, mbr: MBR) -> bool:
    return (mbr.x_low <= point.x <= mbr.x_high) and (mbr.y_low <= point.y <= mbr.y_high)


def do_mbrs_intersect(mbr1: MBR, mbr2: MBR) -> bool:
    if (mbr1.x_high < mbr2.x_low or mbr1.x_low > mbr2.x_high or
            mbr1.y_high < mbr2.y_low or mbr1.y_low > mbr2.y_high):
        return False
    return True


def window_range_query(tree: RTree, query_mbr: MBR) -> list:

    results = []

    if not tree.nodes:
        return results

    # The root is always the last node added to our bottom-up array
    root_node = tree.nodes[-1]

    # Start the recursive top-down traversal
    _range_query_recursive(tree, root_node, query_mbr, results)

    return results


def _range_query_recursive(tree: RTree, node: Node, query_mbr: MBR, results: list):

    # Base Case: If the current node is a leaf (Level 0)
    if node.is_leaf:
        for entry in node.entries:
            # Check if the actual restaurant point falls inside the query window
            if is_point_inside_mbr(entry.point, query_mbr):
                results.append(entry)

    # Recursive Step: If the current node is an intermediate node (Level 1+)
    else:
        for entry in node.entries:
            # Check if the child's MBR intersects with the query window
            if do_mbrs_intersect(entry.mbr, query_mbr):
                # Retrieve the child node from the tree's array using its node_id
                child_node = tree.nodes[entry.node_id]

                # Recursively search inside the child node
                _range_query_recursive(tree, child_node, query_mbr, results)
