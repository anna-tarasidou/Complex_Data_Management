from histograms import *

# Load dataset
dataset_file = "final_general.dat"
age_list = load_age_data(dataset_file)

if age_list:
    # print(f"Youngest: {min(age_list)}, Oldest: {max(age_list)}")

    # Meros 1.1
    eq_width_hist = build_equi_width_histogram(age_list, 10)
    eq_depth_hist = build_equi_depth_histogram(age_list, 10)

    # Save histogram to file
    save_histograms_to_file(eq_width_hist, eq_depth_hist)
    plot_histograms(age_list, eq_width_hist, eq_depth_hist, 10)

    # Meros 1.2
    min_a = min(age_list)
    max_a = max(age_list)
    total = len(age_list)

    query_start = 28
    query_end = 30

    print(f"\nExperiment for ages: [{query_start}, {query_end}]")

    est_width = estimate_equi_width(query_start, query_end, eq_width_hist, min_a, max_a)
    est_depth = estimate_equi_depth(query_start, query_end, eq_depth_hist, min_a, total)

    actual = get_actual_count(query_start, query_end, age_list)

    print(f"1. Estimate Equi-Width : {est_width:.2f}")
    print(f"2. Estimate Equi-Depth : {est_depth:.2f}")
    print(f"3. Actual result : {actual}")

    # Calculation error
    print("\nCalculation error")
    print(f"Error Equi-Width: {abs(actual - est_width):.2f}")
    print(f"Error Equi-Depth: {abs(actual - est_depth):.2f}")
