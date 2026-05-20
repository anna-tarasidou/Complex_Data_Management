# A.M.: 5361
# Anna Tarasidou
import bisect


# Evaluates a range query using the naive linear scan method
def range_query_naive(q, epsilon, D, dist_func):
    result = []
    dist_comps = 0

    for i in range(len(D)):
        dist = dist_func(q, D[i])
        dist_comps += 1

        if dist <= epsilon:
            result.append(i)

    return result, dist_comps


# Evaluates a range query using the pivot-based pruning method
def range_query_pivot(q, epsilon, D, pivots, distances_2d, dist_func):
    result = []
    dist_comps = 0

    # Pre-calculate the distance from the query q to all pivots
    dist_q_to_pivots = []
    for p_id in pivots:
        dist_q_to_pivots.append(dist_func(q, D[p_id]))
        dist_comps += 1

    for i in range(len(D)):
        pruned = False

        # Apply the triangle inequality pruning rule for each pivot
        for j in range(len(pivots)):
            # If |dist(p_i, o) - dist(p_i, q)| > epsilon, prune o
            if abs(distances_2d[i][j] - dist_q_to_pivots[j]) > epsilon:
                pruned = True
                break

        # If the object is not pruned by any pivot, compute the actual distance
        if not pruned:
            dist = dist_func(q, D[i])
            dist_comps += 1
            if dist <= epsilon:
                result.append(i)

    return result, dist_comps


# Evaluates a range query using the iDistance sorted array and binary search
def range_query_idistance(q, epsilon, D, pivots, idistance_array, idist_keys, maxd, dist_func):
    result = []
    dist_comps = 0

    dist_q_to_pivots = []
    for p_id in pivots:
        dist_q_to_pivots.append(dist_func(q, D[p_id]))
        dist_comps += 1

    for i in range(len(pivots)):
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
            if dist <= epsilon:
                result.append(obj_id)

    return result, dist_comps
