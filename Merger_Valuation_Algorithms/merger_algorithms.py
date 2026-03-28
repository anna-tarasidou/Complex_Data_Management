def sort_merge_semijoin(r, s, r_key_index=0, s_key_index=0):
    # Sort-Merge
    # r: airports : index 0
    # s: routes : index 5

    # Sort
    sorted_r = sorted([row for row in r if len(row) > r_key_index], key=lambda x: str(x[r_key_index]))
    sorted_s = sorted([row for row in s if len(row) > s_key_index], key=lambda x: str(x[s_key_index]))

    result = []
    i = 0  # pointer for r
    j = 0  # pointer for s

    # Merge
    while i < len(sorted_r) and j < len(sorted_s):
        r_key = str(sorted_r[i][r_key_index])
        s_key = str(sorted_s[j][s_key_index])

        if r_key == s_key:
            result.append(sorted_r[i])
            i += 1
        elif r_key < s_key:
            i += 1
        else:
            j += 1

    return result


def hash_semijoin(r, s, r_key_index=0, s_key_index=0):
    # r: airports : index 0
    # s: routes : index 5

    # Build hash set
    s_keys = set(str(row[s_key_index]) for row in s if len(row) > s_key_index)

    result = []
    for row in r:
        if len(row) > r_key_index and str(row[r_key_index]) in s_keys:
            result.append(row)

    return result


def hash_antisemijoin(r, s, r_key_index=0, s_key_index=0):
    s_keys = set(str(row[s_key_index]) for row in s if len(row) > s_key_index)

    result = []
    for row in r:
        if len(row) > r_key_index and str(row[r_key_index]) not in s_keys:
            result.append(row)

    return result


def sort_merge_antisemijoin(r, s, r_key_index=0, s_key_index=0):
    # Sort
    sorted_r = sorted([row for row in r if len(row) > r_key_index], key=lambda x: str(x[r_key_index]))
    sorted_s = sorted([row for row in s if len(row) > s_key_index], key=lambda x: str(x[s_key_index]))

    result = []
    i = 0
    j = 0

    # Merge
    while i < len(sorted_r) and j < len(sorted_s):
        r_key = str(sorted_r[i][r_key_index])
        s_key = str(sorted_s[j][s_key_index])

        if r_key == s_key:
            i += 1
        elif r_key < s_key:
            result.append(sorted_r[i])
            i += 1
        else:
            j += 1

    while i < len(sorted_r):
        result.append(sorted_r[i])
        i += 1

    return result


def load_dat_file(filename):
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                row = line.strip().split(',')
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
        return []
