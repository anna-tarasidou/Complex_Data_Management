def sort_merge_semijoin(r, s):
    """
        Υλοποίηση Semijoin με χρήση Ταξινόμησης (Sort-Merge).
        r: Σχέση αεροδρομίων (airports) - Κλειδί στο index 0
        s: Σχέση πτήσεων (routes) - Κλειδί στο index 5
        """
    # Sort
    # Ταξινομούμε και τις δύο λίστες αλφαβητικά/αριθμητικά με βάση το κλειδί τους.
    sorted_r = sorted([row for row in r if len(row) > 0], key=lambda x: str(x[0]))
    sorted_s = sorted([row for row in s if len(row) > 5], key=lambda x: str(x[5]))

    result = []
    i = 0  # Δείκτης για την ταξινομημένη r
    j = 0  # Δείκτης για την ταξινομημένη s

    # Merge
    while i < len(sorted_r) and j < len(sorted_s):
        r_key = str(sorted_r[i][0])
        s_key = str(sorted_s[j][5])

        if r_key == s_key:
            # Βρήκαμε ταίριασμα! Προσθέτουμε τη γραμμή του r στο αποτέλεσμα.
            result.append(sorted_r[i])
            # Στο semijoin, μόλις βρούμε ΕΣΤΩ ΚΑΙ ΜΙΑ αντιστοιχία,
            # τελειώσαμε με αυτό το αεροδρόμιο και προχωράμε στο επόμενο.
            i += 1
        elif r_key < s_key:
            # Το κλειδί του r είναι "μικρότερο" αλφαβητικά, προχωράμε τον δείκτη του r
            i += 1
        else:
            # Το κλειδί του s είναι "μικρότερο" αλφαβητικά, προχωράμε τον δείκτη του s
            j += 1

    return result


def hash_semijoin(r, s):
    """
        Υλοποίηση Semijoin με χρήση Κατακερματισμού (Hashing).
        r: Σχέση αεροδρομίων (airports) - Κλειδί στο index 0
        s: Σχέση πτήσεων (routes) - Κλειδί στο index 5
        """
    # 1. Φάση Κατασκευής (Build phase):
    # Δημιουργούμε ένα Set με όλους τους μοναδικούς κωδικούς προορισμού (index 5) από το s.
    # Τα Sets στην Python λειτουργούν ως Hash Tables, προσφέροντας ακαριαία αναζήτηση.
    s_keys = set(str(row[5]) for row in s if len(row) > 5)

    # 2. Φάση Ανίχνευσης (Probe phase):
    # Σαρώνουμε το r και κρατάμε μόνο όσες γραμμές έχουν κωδικό (index 0) που υπάρχει στο Set.
    result = []
    for row in r:
        if len(row) > 0 and str(row[0]) in s_keys:
            result.append(row)

    return result
