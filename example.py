import numpy as np
from heapq import heappush, heappop
from collections import defaultdict
import random

# Function to find k shortest paths with waveform assignment
def find_k_shortest_paths_with_waveforms(graph, start_path, end_path, k, traffic_matrix, wavelengths):
    queue = [(0, [start_path])]  # priority queue
    paths = []
    path_count = 0  # counter
    
    while queue and len(paths) < k:
        (cost, path) = heappop(queue)
        current = path[-1]
        
        if current == end_path:
            paths.append((cost, path))
            path_count += 1
            continue
        
        for next_node in range(len(graph)):
            if graph[current][next_node] > 0 and next_node not in path:
                new_cost = cost + graph[current][next_node]
                new_path = path + [next_node]
                heappush(queue, (new_cost, new_path))
                path_count += 1
    
    return paths

# Function to assign waveforms to paths
def assign_waveforms(path, traffic_matrix, wavelengths):
    traffic_demand = sum(traffic_matrix[i, j] for i, j in zip(path[:-1], path[1:]))
    return random.sample(range(wavelengths), traffic_demand)

# Function to find the least used waveform
def least_used_waveform(paths, traffic_matrix, wavelengths):
    used_waveforms = defaultdict(int)
    for path in paths:
        waveforms = assign_waveforms(path, traffic_matrix, wavelengths)
        for wf in waveforms:
            used_waveforms[wf] += 1
    
    least_used_wf = min(used_waveforms, key=used_waveforms.get)
    for i in range(len(path) - 1):
        link_usage[(path[i], path[i + 1])] += 1
        link_usage[(path[i + 1], path[i])] += 1  # account for both directions
    return least_used_wf

def main():
    network_topology = np.array([
        [0, 0, 5, 0, 0],
        [0, 0, 0, 3, 7],
        [5, 0, 0, 1, 0],
        [0, 3, 1, 0, 1],
        [0, 7, 0, 1, 0]
    ])

    traffic_matrix = np.array([
        [0, 0, 2, 0, 0],
        [0, 0, 0, 1, 2],
        [1, 0, 0, 1, 0],
        [0, 2, 0, 1, 0]
    ])

    wavelengths = 5
    k = 3

    print("Network topology:")
    print(network_topology)
    print("\nK shortest paths per pair of nodes:")

    number_nodes = len(network_topology)
    selected_final_paths = []
    link_usage = defaultdict(int)  # Initialize link_usage

    for i in range(number_nodes):
        for j in range(i + 1, number_nodes):
            print(f"\nFrom node {i} to node {j}:")

            paths = find_k_shortest_paths_with_waveforms(network_topology, i, j, k, traffic_matrix, wavelengths)
            
            if paths:
                for idx, (cost, path) in enumerate(paths, 1):
                    print(f"Path {idx}: {path} with cost {cost}")

                best_path = least_used_waveform(paths, traffic_matrix, wavelengths)
                selected_final_paths.append((i, j, best_path))
            else:
                print("No paths found")

    print("\nFinal selected paths with waveforms:")
    for start, end, path in selected_final_paths:
        print(f"From node {start} to node {end}: {path}")

    print("\nLink usage statistics:")
    for link, usage in link_usage.items():
        print(f"Link {link}: {usage}")

if __name__ == "__main__":
    main()
