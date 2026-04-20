from r_tree import *


def main():
    leaf_entries = load_data("Beijing_restaurants.txt")
    if leaf_entries:
        print(f"Successfully loaded.")
    else:
        print("No data loaded.")


main()
