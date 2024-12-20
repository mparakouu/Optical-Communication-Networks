import numpy as np
from heapq import heappush, heappop
from collections import defaultdict


def find_k_shortest_paths(graph, start_path, end_path, k):
    # initialize queue --> [(total cost , [path])]
    queue = [(0, [start_path])]
    # save k shortest paths 
    paths = []
    path_count = 0 # k = 3
    
    # > cost from queue
    while queue and len(paths) < k:
        (cost, path) = heappop(queue)
        current = path[-1] # last node
        
        # if last node = end path --> add to paths
        if current == end_path:
            paths.append((cost, path))
            path_count += 1
            continue

        # calculate new cost, that is connected with the current  
        for next_node in range(len(graph)):
            if graph[current][next_node] > 0 and next_node not in path:
                new_cost = cost + graph[current][next_node]
                # new path 
                new_path = path + [next_node]
                heappush(queue, (new_cost, new_path)) # add to queue
                path_count += 1
    
    return paths


def min_use_link(paths, link_usage):

    def usage_of_links(path):

        # calculate the num of appears of the link nodes
        return sum(link_usage[(path[i], path[i+1])] for i in range(len(path) - 1))
    
    # lambda calculuce : find the reverse link nodes
    paths.sort(key=lambda x: usage_of_links(x[1]))
    return paths[0][1]  


def main():

    network_topology = np.array([
    [0, 0, 5, 0, 0],  
    [0, 0, 0, 3, 7],  
    [5, 0, 0, 1, 0],  
    [0, 3, 1, 0, 1],  
    [0, 7, 0, 1, 0]   
])

    # symmetric matrix
    topology = np.maximum(network_topology, network_topology.T)

    k = 3 # 0,1,2

    # print topology 
    print("Network topology:")
    print(network_topology)
    print("\nK shortest paths per pair of nodes:")

    number_nodes = len(topology) # len --> length of array -> num of lines
    link_usage = defaultdict(int) # link connections of the graph
    selected_final_paths = []

    for i in range(number_nodes): 
        for j in range(i+1, number_nodes): 
            print(f"\nFrom node {i} to node {j}:")

            paths = find_k_shortest_paths(topology, i, j, k)
            
            if paths:
                for idx, (cost, path) in enumerate(paths, 1): # we count the elements of the array 
                    print(f"Path {idx}: {path} with cost {cost}")

                best_path = min_use_link(paths, link_usage)   
                selected_final_paths.append((i, j, best_path)) 

                for idx in range(len(best_path) - 1):
                    link_usage[(best_path[idx], best_path[idx+1])] += 1
                    link_usage[(best_path[idx+1], best_path[idx])] += 1  
            else:
                print("No paths have been found")

    # 
    print("\nCount the appear of link nodes that has been chosen to the final paths:")
    link_usages = []  # save link node usages
    for (u, v), usage in link_usage.items():
        # print only one link of nodes (not the reverse)
        if u < v:  
            print(f"Link ({u}, {v}) usage: {usage}")
            link_usages.append(usage) # add to array of links

    
    print("\nFinal selected paths:")
    for (start, end, path) in selected_final_paths:
        print(f"From node {start} to node {end}: {path}")
        
    print("\nThe Statistics:")
    max_use_link = max(link_usages)  # max
    print(f"1) Max use of a link node: {max_use_link}")
    mini_use_link = min(link_usages)  # imn
    print(f"2) Min use of a link node: {mini_use_link}")
    avg_use_link = sum(link_usages) / len(link_usages)  # average
    print(f"3) Average use of a link node: {avg_use_link:.2f}") 
    

if __name__ == "__main__":
    main()
