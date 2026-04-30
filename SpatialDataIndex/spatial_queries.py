# A.M.: 5361
# Anna Tarasidou
import heapq

from r_tree import *


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

    # Start the recursive top-down
    _range_query_recursive(tree, root_node, query_mbr, results)

    return results


def _range_query_recursive(tree: RTree, node: Node, query_mbr: MBR, results: list):
    # If the current node is a leaf (Level 0)
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


def euclidean_distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def min_dist_point_to_mbr(p: Point, mbr: MBR) -> float:
    # Find the closest X coordinate of the MBR to the point
    closest_x = max(mbr.x_low, min(p.x, mbr.x_high))

    # Find the closest Y coordinate of the MBR to the point
    closest_y = max(mbr.y_low, min(p.y, mbr.y_high))

    # Return the Euclidean distance from P to this closest point
    return math.sqrt((p.x - closest_x) ** 2 + (p.y - closest_y) ** 2)


def distance_range_query(tree: RTree, center: Point, radius: float) -> list:
    results = []

    if not tree.nodes:
        return results

    # The root is the last node added to the tree
    root_node = tree.nodes[-1]
    _distance_query_recursive(tree, root_node, center, radius, results)

    return results


def _distance_query_recursive(tree: RTree, node: Node, center: Point, radius: float, results: list):
    # If the current node is a leaf (Level 0)
    if node.is_leaf:
        for entry in node.entries:
            # Check if the actual point is within the search circle
            if euclidean_distance(entry.point, center) <= radius:
                results.append(entry)

    # Recursive Step: If the current node is an intermediate node (Level 1+)
    else:
        for entry in node.entries:
            # Pruning step: Check if the MBR intersects with the search circle
            if min_dist_point_to_mbr(center, entry.mbr) <= radius:
                # Retrieve the child node and search recursively
                child_node = tree.nodes[entry.node_id]
                _distance_query_recursive(tree, child_node, center, radius, results)


def knn_query(tree: RTree, query_point: Point, k: int) -> list:
    results = []

    if not tree.nodes or k <= 0:
        return results

    # Priority queue. Elements will be tuples (distance, priority_type, id_tie_breaker, item)
    # priority_type: 0 for points, 1 for nodes
    pq = []

    # Push the root node into the priority queue (distance 0 to force it to pop first)
    root = tree.nodes[-1]
    heapq.heappush(pq, (0.0, 1, root.node_id, root))

    while pq:
        dist, priority_type, _, item = heapq.heappop(pq)

        if priority_type == 0:
            # LeafEntry (data point)
            results.append(item)

            # Stop if we have exactly 'k' neighbors
            if len(results) == k:
                break

        else:
            # Node
            if item.is_leaf:
                for entry in item.entries:
                    d = euclidean_distance(query_point, entry.point)
                    # Push point to heap (priority_type = 0, tie_breaker = record_id)
                    heapq.heappush(pq, (d, 0, entry.record_id, entry))
            else:
                for entry in item.entries:
                    d = min_dist_point_to_mbr(query_point, entry.mbr)
                    child_node = tree.nodes[entry.node_id]
                    # Push node to heap (priority_type = 1, tie_breaker = node_id)
                    heapq.heappush(pq, (d, 1, child_node.node_id, child_node))

    return results
