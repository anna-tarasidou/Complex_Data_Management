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
    """
    Υπολογίζει το join(r, s) και κάνει pipe τα αποτελέσματα στο join με το t.
    """

    # Εσωτερική συνάρτηση-γεννήτρια που κάνει το join(r,s) on the fly
    def generate_rs_join(r, s):
        i, j = 0, 0
        while i < len(r) and j < len(s):
            if r[i][0] == s[j][0]:
                key = r[i][0]
                # Ελέγχουμε αν υπάρχουν διπλότυπα στο s (όπως στο παράδειγμα για το κλειδί 1)
                temp_j = j
                while temp_j < len(s) and s[temp_j][0] == key:
                    # ΑΝΤΙ για append, κάνουμε yield (pipelining)
                    yield (key, r[i][1], s[temp_j][1])
                    temp_j += 1
                i += 1
            elif r[i][0] < s[j][0]:
                i += 1
            else:
                j += 1

    result = []
    # Ενεργοποιούμε το pipeline
    rs_stream = generate_rs_join(r, s)

    try:
        # Τραβάμε το πρώτο ενδιάμεσο αποτέλεσμα (χωρίς να έχει υπολογιστεί όλο το join!)
        current_rs = next(rs_stream)
        k = 0

        while k < len(t):
            rs_key = current_rs[0]
            t_key = t[k][0]

            if rs_key == t_key:
                # Βρέθηκε ταίριασμα και με τον 3ο πίνακα (t)
                temp_k = k
                while temp_k < len(t) and t[temp_k][0] == rs_key:
                    # Συνθέτουμε την τελική πλειάδα: (A, B, C, D)
                    result.append((rs_key, current_rs[1], current_rs[2], t[temp_k][1]))
                    temp_k += 1

                # Ζητάμε το επόμενο στοιχείο από το pipeline
                current_rs = next(rs_stream)

            elif rs_key < t_key:
                current_rs = next(rs_stream)
            else:
                k += 1

    except StopIteration:
        # Το pipeline άδειασε (δεν υπάρχουν άλλα στοιχεία στο join(r,s))
        pass

    return result


def three_way_sort_merge_join(r, s, t):
    """
    Εφαρμόζει sort-merge ταυτόχρονα και στις 3 εισόδους χωρίς ενδιάμεσα αποτελέσματα.
    """
    result = []
    i, j, k = 0, 0, 0

    while i < len(r) and j < len(s) and k < len(t):
        key_r, key_s, key_t = r[i][0], s[j][0], t[k][0]

        if key_r == key_s == key_t:
            # Και τα τρία κλειδιά ταυτίζονται!
            match_key = key_r

            # Μαζεύουμε όλα τα στοιχεία από το r που έχουν αυτό το κλειδί
            r_matches = []
            while i < len(r) and r[i][0] == match_key:
                r_matches.append(r[i])
                i += 1

            # Μαζεύουμε όλα τα στοιχεία από το s
            s_matches = []
            while j < len(s) and s[j][0] == match_key:
                s_matches.append(s[j])
                j += 1

            # Μαζεύουμε όλα τα στοιχεία από το t
            t_matches = []
            while k < len(t) and t[k][0] == match_key:
                t_matches.append(t[k])
                k += 1

            # Κάνουμε τον συνδυασμό (Καρτεσιανό Γινόμενο) των ταιριαστών εγγραφών
            for rm in r_matches:
                for sm in s_matches:
                    for tm in t_matches:
                        result.append((match_key, rm[1], sm[1], tm[1]))
        else:
            # Δεν ταυτίζονται όλα. Βρίσκουμε τον μεγαλύτερο αριθμό κλειδιού.
            max_key = max(key_r, key_s, key_t)

            # Όποιος δείκτης έχει μείνει πίσω, τον προχωράμε
            if key_r < max_key:
                i += 1
            if key_s < max_key:
                j += 1
            if key_t < max_key:
                k += 1

    return result
