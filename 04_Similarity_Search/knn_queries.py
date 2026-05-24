# A.M.: 5361
# Anna Tarasidou
import heapq
import bisect


# Evaluates a k-NN query using the naive linear scan method with a Priority Queue
def knn_query_naive(q, k, D, dist_func):
    dist_comps = 0
    heap = []

    # Calculate the distance from q to all objects
    for i in range(len(D)):
        dist = dist_func(q, D[i])
        dist_comps += 1

        if len(heap) < k:
            heapq.heappush(heap, (-dist, i))
        else:
            if dist < -heap[0][0]:
                heapq.heapreplace(heap, (-dist, i))

    # Sort the closest first
    best_k = sorted([(-d, obj_id) for d, obj_id in heap])

    # Return objects and distances
    result = [(obj_id, d) for d, obj_id in best_k]

    return result, dist_comps


# Evaluates a k-NN query using the pivot-based pruning method with a Max-Heap
def knn_query_pivot(q, k, D, pivots, distances_2d, dist_func):
    dist_comps = 0
    heap = []

    # Pre-calculate the distance from the query q to all pivots
    dist_q_to_pivots = []
    for p_id in pivots:
        dist_q_to_pivots.append(dist_func(q, D[p_id]))
        dist_comps += 1

    for i in range(len(D)):
        # If the size of the heap is less than k, calculate distance and add to the heap
        if len(heap) < k:
            dist = dist_func(q, D[i])
            dist_comps += 1
            heapq.heappush(heap, (-dist, i))

        else:
            # If the heap size is k, use the top element as epsilon
            epsilon = -heap[0][0]
            pruned = False

            # For each pivot pi, if |dist(pi,o) - dist(pi,q)| > epsilon, prune object o
            for j in range(len(pivots)):
                if abs(distances_2d[i][j] - dist_q_to_pivots[j]) > epsilon:
                    pruned = True
                    break

            # If object o is not pruned, calculate its actual distance dist(q,o)
            if not pruned:
                dist = dist_func(q, D[i])
                dist_comps += 1

                # If dist(q,o) <= epsilon, replace the element at the top of the heap
                if dist <= epsilon:
                    heapq.heapreplace(heap, (-dist, i))

    # Sort the results and return objects and distances
    best_k = sorted([(-d, obj_id) for d, obj_id in heap])
    result = [(obj_id, d) for d, obj_id in best_k]

    return result, dist_comps


# Evaluates a k-NN query following the partition-based iDistance
def knn_query_idistance(q, k, D, pivots, idistance_array, idist_keys, maxd_p, maxd, dist_func):
    dist_comps = 0
    heap = []

    # Find the closest pivot to the query object q
    dist_q_to_pivots = []
    for p_id in pivots:
        dist_q_to_pivots.append(dist_func(q, D[p_id]))
        dist_comps += 1

    closest_pivot_idx = 0
    min_dist = dist_q_to_pivots[0]
    for i in range(1, len(pivots)):
        if dist_q_to_pivots[i] < min_dist:
            min_dist = dist_q_to_pivots[i]
            closest_pivot_idx = i

    # Group objects into their partitions
    partitions = {i: [] for i in range(len(pivots))}
    for item in idistance_array:
        idist_val, obj_id, p_idx = item
        partitions[p_idx].append(obj_id)

    # For objects in the partition of the closest pivot, scan of the closest partition
    for obj_id in partitions[closest_pivot_idx]:
        dist = dist_func(q, D[obj_id])
        dist_comps += 1
        if len(heap) < k:
            heapq.heappush(heap, (-dist, obj_id))
        else:
            if dist < -heap[0][0]:
                heapq.heapreplace(heap, (-dist, obj_id))

    # For the remaining pivots
    for i in range(len(pivots)):
        if i == closest_pivot_idx:
            continue

        # use the current k-th NN distance as the epsilon
        epsilon = -heap[0][0] if len(heap) == k else float('inf')

        # prune them along with their partitions
        if dist_q_to_pivots[i] - epsilon > maxd_p[i]:
            continue

        # Scan using binary search
        lower_bound = i * maxd + dist_q_to_pivots[i] - epsilon
        upper_bound = i * maxd + dist_q_to_pivots[i] + epsilon

        start_idx = bisect.bisect_left(idist_keys, lower_bound)

        for j in range(start_idx, len(idistance_array)):
            idist_val, obj_id, p_idx = idistance_array[j]

            if idist_val > upper_bound:
                break

            if p_idx != i:
                continue

            dist = dist_func(q, D[obj_id])
            dist_comps += 1
            if len(heap) < k:
                heapq.heappush(heap, (-dist, obj_id))
            else:
                if dist < -heap[0][0]:
                    heapq.heapreplace(heap, (-dist, obj_id))

    # Return the k nearest objects to q and their distances
    best_k = sorted([(-d, obj_id) for d, obj_id in heap])
    result = [(obj_id, d) for d, obj_id in best_k]

    return result, dist_comps
