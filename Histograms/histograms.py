import matplotlib.pyplot as plt


def load_age_data(filename):
    # reads the data file and extracts 2nd column (age)
    ages = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()

                if len(parts) > 1:
                    age_str = parts[1]

                    try:
                        age = int(age_str)
                        ages.append(age)
                    except ValueError:
                        pass
        print(f"Data successfully loaded! Found {len(ages)} valid ages.")

        return ages

    except FileNotFoundError:
        print(f"File {filename} not found!")
        return []


def build_equi_width_histogram(ages, num_bins=10):
    if not ages:
        return []

    min_age = min(ages)
    max_age = max(ages)

    bin_width = (max_age - min_age) / num_bins

    histogram = [0] * num_bins

    for age in ages:
        bin_index = int((age - min_age) / bin_width)

        if bin_index == num_bins:
            bin_index -= 1

        histogram[bin_index] += 1

    return histogram


def build_equi_depth_histogram(ages, num_bins=10):
    if not ages:
        return []

    # sorting the data
    sorted_ages = sorted(ages)
    total_elements = len(sorted_ages)

    elements_per_bin = total_elements / num_bins

    boundaries = []

    for i in range(1, num_bins):
        split_index = int(i * elements_per_bin)
        boundaries.append(sorted_ages[split_index])

    boundaries.append(sorted_ages[-1])

    return boundaries


def save_histograms_to_file(equi_width, equi_depth, filename="histograms_output.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Equi-Width Histogram\n")
        f.write(f"Counts per bin (10 bins):\n{equi_width}\n\n")

        f.write("Equi-Depth Histogram\n")
        f.write(f"Boundaries (10 bins):\n{equi_depth}\n")

    print(f"\nHistograms written in file: {filename}")


def plot_histograms(ages, eq_width_counts, eq_depth_boundaries,  num_bins=10):
    min_age = min(ages)
    max_age = max(ages)
    total_elements = len(ages)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Equal Width Histogram
    bin_width = (max_age - min_age) / num_bins
    width_labels = [f"{int(min_age + i * bin_width)}-{int(min_age + (i + 1) * bin_width)}" for i in range(num_bins)]

    ax1.bar(width_labels, eq_width_counts, color='blue', edgecolor='black', width=0.5)
    ax1.set_title("Equal width")

    # Equal Depth Histogram
    frequency = total_elements // num_bins
    depth_counts = [frequency] * num_bins

    depth_labels = []
    prev_boundary = min_age
    for b in eq_depth_boundaries:
        depth_labels.append(f"{prev_boundary}-{b}")
        prev_boundary = b

    ax2.bar(depth_labels, depth_counts, color='blue', edgecolor='black', width=0.5)
    ax2.set_title("Equal frequency")

    # Show window
    plt.tight_layout()

    plt.savefig("histograms_plot.png")
    print("Saved successfully as: 'histograms_plot.png'!")


def estimate_equi_width(a, b, eq_width_counts, min_age, max_age):
    num_bins = len(eq_width_counts)
    bin_width = (max_age - min_age) / num_bins
    estimated_count = 0.0

    for i in range(num_bins):
        bin_start = min_age + i * bin_width
        bin_end = min_age + (i + 1) * bin_width

        # Find the overlap
        overlap_start = max(a, bin_start)
        overlap_end = min(b, bin_end)

        # If there is overlap
        if overlap_start < overlap_end:
            fraction = (overlap_end - overlap_start) / bin_width
            estimated_count += fraction * eq_width_counts[i]

    return estimated_count


def estimate_equi_depth(a, b, eq_depth_boundaries, min_age, total_elements):
    num_bins = len(eq_depth_boundaries)
    frequency = total_elements / num_bins
    estimated_count = 0.0

    prev_boundary = min_age
    for boundary in eq_depth_boundaries:
        bin_start = prev_boundary
        bin_end = boundary
        bin_width = bin_end - bin_start

        if bin_width > 0:
            overlap_start = max(a, bin_start)
            overlap_end = min(b, bin_end)

            if overlap_start < overlap_end:
                fraction = (overlap_end - overlap_start) / bin_width
                estimated_count += fraction * frequency

        prev_boundary = boundary

    return estimated_count


def get_actual_count(a, b, ages):
    # Find the actual count
    count = 0
    for age in ages:
        if a <= age <= b:
            count += 1
    return count
