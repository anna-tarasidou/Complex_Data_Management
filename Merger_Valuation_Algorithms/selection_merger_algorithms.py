def selection_sort_merge_semijoin(airports, routes, aircraft_type):
    # Selection
    filtered_routes = []
    for r in routes:
        if len(r) > 5 and aircraft_type in r[-1]:
            if r[5].strip().isdigit():
                filtered_routes.append(r)

    sorted_routes = sorted(filtered_routes, key=lambda x: int(x[5].strip()))

    result = []
    i = 0
    j = 0

    while i < len(airports) and j < len(sorted_routes):
        if not airports[i][0].strip().isdigit():
            i += 1
            continue

        r_key = int(airports[i][0].strip())
        s_key = int(sorted_routes[j][5].strip())

        if r_key == s_key:
            result.append(airports[i])
            i += 1
        elif r_key < s_key:
            i += 1
        else:
            j += 1

    return result
