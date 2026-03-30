import sys
from merger_algorithms import *
from selection_merger_algorithms import *

r_test = [(1, 2), (1, 4), (2, 5)]
s_test = [(1, 'a'), (1, 'c'), (3, 'a')]

print("--- Test ---")
print("Semijoin Sort Result:", sort_merge_semijoin(r_test, s_test))
print("Semijoin Hash Result:", hash_semijoin(r_test, s_test))

print("Anti-Semijoin Sort Result:", sort_merge_antisemijoin(r_test, s_test))
print("Anti-Semijoin Hash Result:", hash_antisemijoin(r_test, s_test))

airports = load_dat_file("airports.dat")
routes = load_dat_file("routes.dat")

if airports and routes:
    print(f"\nFound {len(airports)} airports and {len(routes)} flights.\n")

    semi_sort = sort_merge_semijoin(airports, routes, 0, 5)
    semi_hash = hash_semijoin(airports, routes, 0, 5)

    print(f"Sort Result: Found {len(semi_sort)} airports with flights.")
    print(f"Hash Result: Found {len(semi_hash)} airports with flights.")

    antisemi_sort = sort_merge_antisemijoin(airports, routes, 0, 5)
    antisemi_hash = hash_antisemijoin(airports, routes, 0, 5)

    print(f"Sort Result: Found {len(antisemi_sort)} airports with NO flights.")
    print(f"Hash Result: Found {len(antisemi_hash)} airports with NO flights.")

if len(sys.argv) != 2:
    print("Error give type of aircraft!")
    sys.exit(1)

target_aircraft = sys.argv[1]

airports_data = load_dat_file("airports.dat")
routes_data = load_dat_file("routes.dat")

if airports_data and routes_data:
    result_airports = selection_sort_merge_semijoin(airports_data, routes_data, target_aircraft)

    print(f"\n--- Result ---")
    print(f"Found {len(result_airports)} airports with aircrafts {target_aircraft}.")

r_test = [(1, 'b1'), (2, 'b2'), (3, 'b3'), (4, 'b4')]
s_test = [(1, 'c1'), (1, 'c2'), (2, 'c3'), (3, 'c4')]
t_test = [(1, 'd1'), (2, 'd2'), (3, 'd3'), (5, 'd4')]

expected_output = [(1, 'b1', 'c1', 'd1'), (1, 'b1', 'c2', 'd1'), (2, 'b2', 'c3', 'd2'), (3, 'b3', 'c4', 'd3')]

print("--- Pipelined Merge Join ---")
pipe_result = pipelined_merge_join(r_test, s_test, t_test)
print("Result:", pipe_result)
print(pipe_result == expected_output)

print("\n--- Three-Way Sort-Merge Join ---")
three_way_result = three_way_sort_merge_join(r_test, s_test, t_test)
print("Result:", three_way_result)
print(three_way_result == expected_output)