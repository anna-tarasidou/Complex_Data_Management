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


def pipelined_merge_join(r, s, t):
    # Function that generates join
    def generate_rs_join(r, s):
        i, j = 0, 0
        while i < len(r) and j < len(s):
            if r[i][0] == s[j][0]:
                key = r[i][0]
                temp_j = j
                while temp_j < len(s) and s[temp_j][0] == key:
                    yield key, r[i][1], s[temp_j][1]
                    temp_j += 1
                i += 1
            elif r[i][0] < s[j][0]:
                i += 1
            else:
                j += 1

    result = []
    # Pipeline
    rs_stream = generate_rs_join(r, s)

    try:
        current_rs = next(rs_stream)
        k = 0

        while k < len(t):
            rs_key = current_rs[0]
            t_key = t[k][0]

            if rs_key == t_key:
                temp_k = k
                while temp_k < len(t) and t[temp_k][0] == rs_key:
                    result.append((rs_key, current_rs[1], current_rs[2], t[temp_k][1]))
                    temp_k += 1

                current_rs = next(rs_stream)

            elif rs_key < t_key:
                current_rs = next(rs_stream)
            else:
                k += 1

    except StopIteration:
        pass

    return result


def three_way_sort_merge_join(r, s, t):
    result = []
    i, j, k = 0, 0, 0

    while i < len(r) and j < len(s) and k < len(t):
        key_r, key_s, key_t = r[i][0], s[j][0], t[k][0]

        if key_r == key_s == key_t:
            match_key = key_r

            r_matches = []
            while i < len(r) and r[i][0] == match_key:
                r_matches.append(r[i])
                i += 1

            s_matches = []
            while j < len(s) and s[j][0] == match_key:
                s_matches.append(s[j])
                j += 1

            t_matches = []
            while k < len(t) and t[k][0] == match_key:
                t_matches.append(t[k])
                k += 1

            for rm in r_matches:
                for sm in s_matches:
                    for tm in t_matches:
                        result.append((match_key, rm[1], sm[1], tm[1]))
        else:
            max_key = max(key_r, key_s, key_t)

            if key_r < max_key:
                i += 1
            if key_s < max_key:
                j += 1
            if key_t < max_key:
                k += 1

    return result
