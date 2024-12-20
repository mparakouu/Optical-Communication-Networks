import random
import networkx as nx
import time

# random wavelength assignment
def random_wavelength(traffic_matrix, paths, num_wavelengths):
    wavelength_usage = {link: [False] * num_wavelengths for path in paths.values() for i in range(len(path) - 1) for link in [(path[i], path[i + 1])]}
    assigned_wavelengths = {}  # wavelengths that have been assigned
    blocked_requests = 0  # blocked

    for source in range(len(traffic_matrix)):
        for dest in range(len(traffic_matrix[0])):
            num_requests = traffic_matrix[source][dest]  # wavelength for node to node
            if num_requests == 0 or (source, dest) not in paths:
                blocked_requests += num_requests  # blocked if now exist or 0
                continue

            path = paths[(source, dest)]
            links = [(path[i], path[i + 1]) for i in range(len(path) - 1)]  # links of this path
            assigned = []  # wavelengths that have been used

            # check if wavelengths for each link in a path
            for _ in range(num_requests):
                available_wavelengths = set(range(num_wavelengths))
                for link in links:
                    if any(wavelength_usage[link][w] for w in available_wavelengths):
                        available_wavelengths -= {w for w in range(num_wavelengths) if wavelength_usage[link][w]}
                    if not available_wavelengths:
                        blocked_requests += 1
                        break
                else:
                    selected_wavelength = random.choice(list(available_wavelengths))
                    for link in links:
                        wavelength_usage[link][selected_wavelength] = True
                    assigned.append(selected_wavelength)

            assigned_wavelengths[(source, dest)] = assigned

    return assigned_wavelengths, blocked_requests

# First-Fit wavelength 
def first_fit_wavelength(traffic_matrix, paths, num_wavelengths):
    wavelength_usage = {link: [False] * num_wavelengths for path in paths.values() for i in range(len(path) - 1) for link in [(path[i], path[i + 1])]}
    assigned_wavelengths = {}
    blocked_requests = 0

    for source in range(len(traffic_matrix)):
        for dest in range(len(traffic_matrix[0])):
            num_requests = traffic_matrix[source][dest]
            if num_requests == 0 or (source, dest) not in paths:
                continue

            path = paths[(source, dest)]
            links = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            assigned = []

            for _ in range(num_requests):
                for w in range(num_wavelengths):
                    if all(not wavelength_usage[link][w] for link in links):
                        for link in links:
                            wavelength_usage[link][w] = True
                        assigned.append(w)
                        break
                else:
                    blocked_requests += 1

            assigned_wavelengths[(source, dest)] = assigned

    return assigned_wavelengths, blocked_requests

# Least-Used wavelength 
def least_used_wavelength(traffic_matrix, paths, num_wavelengths):
    wavelength_usage = {link: [0] * num_wavelengths for path in paths.values() for i in range(len(path) - 1) for link in [(path[i], path[i + 1])]}
    assigned_wavelengths = {}
    blocked_requests = 0

    for source in range(len(traffic_matrix)):
        for dest in range(len(traffic_matrix[0])):
            num_requests = traffic_matrix[source][dest]
            if num_requests == 0 or (source, dest) not in paths:
                continue

            path = paths[(source, dest)]
            links = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            assigned = []

            for _ in range(num_requests):
                available_wavelengths = sorted(range(num_wavelengths), key=lambda w: sum(wavelength_usage[link][w] for link in links))
                for w in available_wavelengths:
                    if all(wavelength_usage[link][w] == 0 for link in links):
                        for link in links:
                            wavelength_usage[link][w] += 1
                        assigned.append(w)
                        break
                else:
                    blocked_requests += 1

            assigned_wavelengths[(source, dest)] = assigned

    return assigned_wavelengths, blocked_requests

# Traffic matrix
traffic_matrix = [
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 2],
    [1, 0, 0, 1, 0],
    [0, 2, 0, 1, 0]
]

# Paths
paths = {
    (0, 1): [0, 2, 3, 1],
    (0, 2): [0, 2],
    (0, 3): [0, 2, 3],
    (0, 4): [0, 2, 3, 4],
    (1, 2): [1, 3, 2],
    (1, 3): [1, 4, 3],
    (1, 4): [1, 4],
    (2, 3): [2, 3],
    (2, 4): [2, 3, 4],
    (3, 4): [3, 4]
}

# Number of wavelengths
num_wavelengths = 5

def print_results(algorithm_name, assigned_wavelengths, blocked_requests, execution_time, traffic_matrix):
    print(f"\n{algorithm_name} Assignment:")
    for (source, dest), wavelengths in assigned_wavelengths.items():
        print(f"({source} -> {dest}): {wavelengths}")
    print(f"Blocked requests: {blocked_requests}")
    total_requests = sum(sum(row) for row in traffic_matrix)
    print(f"Percentage of blocked requests: {blocked_requests / total_requests * 100:.2f}%")
    print(f"Execution time: {execution_time:.6f} seconds")

# Random
start_time = time.time()
random_assigned, random_blocked = random_wavelength(traffic_matrix, paths, num_wavelengths)
random_time = time.time() - start_time
print_results("Random", random_assigned, random_blocked, random_time, traffic_matrix)

# First-Fit
start_time = time.time()
first_fit_assigned, first_fit_blocked = first_fit_wavelength(traffic_matrix, paths, num_wavelengths)
first_fit_time = time.time() - start_time
print_results("First-Fit", first_fit_assigned, first_fit_blocked, first_fit_time, traffic_matrix)

# Least-Used
start_time = time.time()
least_used_assigned, least_used_blocked = least_used_wavelength(traffic_matrix, paths, num_wavelengths)
least_used_time = time.time() - start_time
print_results("Least-Used", least_used_assigned, least_used_blocked, least_used_time, traffic_matrix)

for new_num_wavelengths in range(6, 11):
    start_time = time.time()
    _, new_blocked = random_wavelength(traffic_matrix, paths, new_num_wavelengths)
    new_time = time.time() - start_time
    if new_blocked == 0:
        print(f"\nWith num_wavelengths = {new_num_wavelengths}, blocking is 0.")
        break

if random_blocked <= first_fit_blocked and random_blocked <= least_used_blocked:
    print("\nRandom algorithm is the most efficient.")
elif first_fit_blocked <= random_blocked and first_fit_blocked <= least_used_blocked:
    print("\nFirst-Fit algorithm is the most efficient.")
else:
    print("\nLeast-Used algorithm is the most efficient.")
