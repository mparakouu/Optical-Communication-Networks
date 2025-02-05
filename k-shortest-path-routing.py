#                           GRAPH NETWORK
#               (0)---5---(2)---1---(3)---3---(1)
#                                    |        /
#                                    |       /
#                                    1     7
#                                    |    /
#                                    |   /
#                                     (4)

import heapq
import itertools
from collections import defaultdict
import random, time, collections

A = [
    [0, 0, 5, 0, 0],
    [0, 0, 0, 3, 7],
    [5, 0, 0, 1, 0],
    [0, 3, 1, 0, 1],
    [0, 7, 0, 1, 0]
]


traffic_matrix = [
        [0, 0, 2, 0, 0],
        [0, 0, 0, 1, 2],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 1],
        [0, 2, 0, 1, 0] 
]

# find the first k shortest paths between each pair of nodes.
def find_k_shortest_paths(graph_network, k):
    n = len(graph_network)
    all_paths = {}

    print("Network topology:")
    for row in A:
        print(row)
    print("\n")        
    
    for start, end in itertools.combinations(range(n), 2): # combinations of link nodes
        print(f"From node {start} to node {end}:")
        
        paths = []
        # initialize queue --> [(total cost , [path])]
        queue = [(0, [start])]  
        
        while queue and len(paths) < k: # not empty queue, continue until --> k 
            cost, path = heapq.heappop(queue)
            current_node = path[-1]
            
            if current_node == end: # if end 
                paths.append((cost, path)) # save path
                continue
            
            # add cost to the path
            for next_node in range(n):
                if graph_network[current_node][next_node] > 0 and next_node not in path: 
                    new_cost = cost + graph_network[current_node][next_node] # 
                    new_path = path + [next_node]
                    heapq.heappush(queue, (new_cost, new_path))
        
        all_paths[(start, end)] = paths
        
        # print paths with their cost 
        for i, (cost, path) in enumerate(paths, 1):
            print(f"Path = {path} , Cost = {cost}")
        print()
    
    return all_paths


def usage_link(graph_network, all_paths):
    
    link_usage = defaultdict(int)
    selected_paths = {}

    # choose pairs that appear less
    for (start, end), paths in all_paths.items():
        kept_path = None # initialize the paths that we will keep 
        min_link_usage = float('inf')

        for cost, path in paths:
            # link usage for this path
            current_link_usage = 0
            for i in range(len(path) - 1):
                link = tuple(sorted((path[i], path[i + 1])))
                # the times this link is used from the link_usage dictionary & add
                current_link_usage += link_usage[link] 

            # choose link --> least usage --> keep it
            if min_link_usage > current_link_usage :
                # the new best path (kept_path)
                min_link_usage = current_link_usage
                kept_path = (cost, path)

        # update
        if kept_path:
            selected_paths[(start, end)] = kept_path
            for i in range(len(kept_path[1]) - 1):
                link = tuple(sorted((kept_path[1][i], kept_path[1][i + 1])))
                link_usage[link] += 1


    print("\nThe paths that have been selected are:")
    for (start, end), (cost, path) in selected_paths.items():
        print(f"Path from {start} to {end}: Cost = {cost}, Route = {path}")

    # Calculate usage statistics
    usages = list(link_usage.values())
    min_link_usage = min(usages) if usages else 0
    max_usage = max(usages) if usages else 0
    avg_usage = sum(usages) / len(usages) if usages else 0


    # print 
    print("\nThe Statistics:")
    print(f"Min use of a link node: {min_link_usage}")
    print(f"Max use of a link node: {max_usage}")
    print(f"Average use of a link node: {avg_usage:.2f}")
    print("\n")

    for link, usage in link_usage.items():
        print(f"Link {link}: was used {usage} times")

    print("\n")
    print("Traffic Matrix:")
    for row in traffic_matrix:
        print(row)

    print("\n")    
    for link, usage in link_usage.items():
        # assign wavelengths to each link of nodes that exists
        total_usage = usage * traffic_matrix[link[0]][link[1]]
        print(f"Link {link}: has been assigned with {total_usage} wavelengths")    

    return selected_paths, max_usage, min_link_usage, avg_usage


def assign_wavelengths(selected_paths, traffic_matrix, wavelengths, algorithms):
    links_of_nodes = {}

    for (source, destination), (_, path) in selected_paths.items():
        links = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        links_of_nodes[(source, destination)] = links

    # dictionary that stores the traffic between nodes
    traffic_dict = {
        (source, destination): traffic_matrix[source][destination]
        for source in range(len(traffic_matrix))
        for destination in range(len(traffic_matrix[source]))
        if traffic_matrix[source][destination] > 0
    }

    #dict of total number of required wavelengths for each link
    link_occurrences = {}

    for (source, destination), links in links_of_nodes.items():
        demand = traffic_dict.get((source, destination), 0)
        
        for link in links:
            req_wavelengths = traffic_dict.get(link, 1)
            if link not in link_occurrences:
                link_occurrences[link] = 0
            link_occurrences[link] += demand * req_wavelengths
            
            symmetric_link = link[::-1]
            if symmetric_link in traffic_dict:
                req_wavelengths = traffic_dict[symmetric_link]
                if symmetric_link not in link_occurrences:
                    link_occurrences[symmetric_link] = 0
                link_occurrences[symmetric_link] += demand * req_wavelengths

    wavelength_assignments = {}
    blocked_links = []
    wavelength_usage = collections.defaultdict(int)
    
    if algorithms == "Random":
        for link, required_wavelengths in link_occurrences.items():
            available_wavelengths = list(range(1, wavelengths + 1))
            random.shuffle(available_wavelengths)
            
            if required_wavelengths > len(available_wavelengths):
                blocked_links.append(link)
            else:
                wavelength_assignments[link] = available_wavelengths[:required_wavelengths]

    elif algorithms == "First-Fit":
        wavelength_assignments = {}
        blocked_links = []
        
        for link, required_wavelengths in link_occurrences.items():
            assigned_wavelengths = []
            
            # 1 to wavelength
            for w in range(1, wavelengths + 1):
                if len(assigned_wavelengths) < required_wavelengths:
                    assigned_wavelengths.append(w)

            if len(assigned_wavelengths) == required_wavelengths:
                wavelength_assignments[link] = assigned_wavelengths
            else:
                blocked_links.append(link)


    elif algorithms == "Least-Used":
        # links with the highest demand will be assigned first
        for link, required_wavelengths in sorted(link_occurrences.items(), key=lambda x: x[1], reverse=True): # links are sorted by the number of waveforms they require
            least_used_wavelengths = sorted(range(1, wavelengths + 1), key=lambda w: wavelength_usage[w]) # number of times waveform w has been used
            
            assigned_wavelengths = []
            for w in least_used_wavelengths:
                if len(assigned_wavelengths) < required_wavelengths:
                    assigned_wavelengths.append(w)
                    wavelength_usage[w] += 1
            
            if len(assigned_wavelengths) < required_wavelengths:
                blocked_links.append(link)
            else:
                wavelength_assignments[link] = assigned_wavelengths

    # blocked links
    blocked_percentage = (len(blocked_links) / len(link_occurrences)) * 100 if link_occurrences else 0

    # assign wavelengths labeled
    wavelength_labels = {w: f'λ{w}' for w in range(1, wavelengths + 1)}
    wavelength_assignments_labeled = {}
    for link, wavelengths_list in wavelength_assignments.items():
        wavelength_assignments_labeled[link] = [wavelength_labels[w] for w in wavelengths_list]

    # bidirectional link of nodes
    bidirectional_assignments = {}
    processed_links = set() # to avoid processing the same link in the reverse direction
    
    for link, wavelengths_list in wavelength_assignments_labeled.items():
        if link not in processed_links:
            reverse_link = (link[1], link[0])
            reverse_wavelengths = wavelength_assignments_labeled.get(reverse_link, [])
            
            # key --> for 1 directions 
            sorted_link = tuple(sorted([link[0], link[1]]))
            
            bidirectional_assignments[sorted_link] = {
                'forward': {
                    'direction': f"{link[0]} → {link[1]}",
                    'wavelengths': wavelengths_list
                },
                'reverse': {
                    'direction': f"{link[1]} → {link[0]}",
                    'wavelengths': reverse_wavelengths
                }
            }
            
            processed_links.add(link)
            processed_links.add(reverse_link)

    # print
    print(f"\n{algorithms} Algorithm")
    print("Wavelength Assignments:")
    for link, assignments in bidirectional_assignments.items():
        print(f"\nLink {link}:")
        print(f"  {assignments['forward']['direction']}: {assignments['forward']['wavelengths']}")
        print(f"  {assignments['reverse']['direction']}: {assignments['reverse']['wavelengths']}")

    return {
        'link_wavelength_requirements': link_occurrences,
        'wavelength_assignments': bidirectional_assignments,
        'blocked_links': blocked_links,
        'blocked_percentage': blocked_percentage,
        'wavelength_usage': dict(wavelength_usage) if algorithms == 'least-used' else None,
    }


def main():

    k = 3

    # Run k-shortest path routing
    all_paths = find_k_shortest_paths(A, k)
    selected_paths, max_usage, min_usage, avg_usage = usage_link(A, all_paths)
    print()

    wavelengths = 5
    #wavelengths = 6

    print("Link Wavelength Requirements:")
    for alg in ["Random", "First-Fit", "Least-Used"]:
        
        # algorithm's performance
        start = time.time()
        result = assign_wavelengths(selected_paths, traffic_matrix, wavelengths, alg)
        end = time.time()
        time_needed = end - start

        print("Percentage of Blocked:", result['blocked_percentage'])
        print("Blocked Links:", result['blocked_links'])
        print("Time has taken:", time_needed)
        print("\n")
    
if __name__ == "__main__":

    main()