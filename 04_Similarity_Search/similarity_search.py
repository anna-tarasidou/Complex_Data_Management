# A.M.: 5361
# Anna Tarasidou
import math


# Calculate euclidean distance
def euclidean_distance(point1, point2):
    distance = 0.0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2
    return math.sqrt(distance)


def load_data(filepath):
    D = []
    with open(filepath, 'r') as file:
        for line in file:
            # Skip empty lines
            if not line.strip():
                continue

            # Convert the space-separated string values into floats
            point = [float(x) for x in line.strip().split()]
            D.append(point)

    return D


# Calculates the pivots base and computes a 2D array of distances from every object to every chosen pivot
def calculate_pivots_and_distances(D, num_pivots):
    n = len(D)
    if n == 0 or num_pivots <= 0:
        return [], []

    pivots = []

    # Seed is the first object ID-0
    seed_id = 0

    # First pivot is the furthest object from the seed
    max_dist = -1
    p0 = -1
    for i in range(n):
        dist = euclidean_distance(D[seed_id], D[i])
        if dist > max_dist:
            max_dist = dist
            p0 = i
    pivots.append(p0)

    # Second pivot is the furthest object from first pivot
    if num_pivots >= 2:
        max_dist = -1
        p1 = -1
        for i in range(n):
            dist = euclidean_distance(D[p0], D[i])
            if dist > max_dist:
                max_dist = dist
                p1 = i
        pivots.append(p1)

    # K-th pivot is the object that maximizes the sum of distances to all previously selected pivots
    for k in range(2, num_pivots):
        max_sum_dist = -1
        next_pivot = -1
        for i in range(n):
            # Skip objects that are already chosen as pivots
            if i in pivots:
                continue

            # Calculate the sum of distances to all previously selected pivots
            current_sum_dist = sum(euclidean_distance(D[i], D[p]) for p in pivots)

            if current_sum_dist > max_sum_dist:
                max_sum_dist = current_sum_dist
                next_pivot = i
        pivots.append(next_pivot)

    # Compute the 2D distances array.
    # distances[i][j] is the distance from object i to pivot j
    distances = []
    for i in range(n):
        obj_distances = []
        for j in range(num_pivots):
            dist = euclidean_distance(D[i], D[pivots[j]])
            obj_distances.append(dist)
        distances.append(obj_distances)

    return pivots, distances


# Calculates the iDistance index for all objects based on their distances to the pivots
def calculate_idistance_index(pivots, distances):
    n = len(distances)  # Total number of objects
    num_pivots = len(pivots)

    # maxd_p[i] will store the maximum distance from pivot i to any object for which pivot i is the closest pivot.
    maxd_p = [0.0] * num_pivots

    # Track the closest pivot index for each object
    closest_pivot_indices = []

    # Find the closest pivot for each object and update maxd(p)
    for i in range(n):
        min_dist = float('inf')
        closest_idx = -1

        # Find the closest pivot for object i
        for j in range(num_pivots):
            if distances[i][j] < min_dist:
                min_dist = distances[i][j]
                closest_idx = j

        closest_pivot_indices.append(closest_idx)

        # Update the max distance for this pivot
        if min_dist > maxd_p[closest_idx]:
            maxd_p[closest_idx] = min_dist

    # Calculate global maximum distance maxd
    maxd = max(maxd_p)

    idistance_array = []

    # Calculate the iDistance value for each object
    for i in range(n):
        c_idx = closest_pivot_indices[i]
        dist_to_pivot = distances[i][c_idx]

        # iDistance formula: i * maxd + dist(o, p_i)
        idist_value = c_idx * maxd + dist_to_pivot

        idistance_array.append((idist_value, i, c_idx))

    # Sort the array based on the iDistance value
    idistance_array.sort(key=lambda x: x[0])

    return idistance_array, maxd_p, maxd
