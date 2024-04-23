import networkx as nx
import matplotlib.pyplot as plt
import random
import csv
import logging

__all__ = [
    "create_network_graph",
    "assign_noise_rate",
    "get_random_sd_pairs",
    "find_shortest_paths",
    "calculate_fidelity",
    "generate_sd_pairs",
    "compute_fidelity_for_all_paths",
    "save_to_csv"

]

def create_network_graph(n, top_bottom_connection=True, draw_network=False, destination_mesh=False):

    G = nx.grid_2d_graph(n, n)
    grid_nodes = [f"Node_{i}" for i in range(len(G.nodes))]
    nx.relabel_nodes(G, dict(zip(G.nodes, grid_nodes)), copy=False)

    source_nodes = [f"Node_s{i}" for i in range(n)]
    destination_nodes = [f"Node_d{i}" for i in range(n)]

    # Connect the source nodes to the leftmost column of nodes
    for i in range(n):
        source_node = source_nodes[i]
        G.add_edge(source_node, grid_nodes[i * n])

    # Connect the destination nodes
    if destination_mesh:
        # Connect the destination nodes to the rightmost column of nodes
        for i in range(n):
            destination_node = destination_nodes[i]
            for j in range(n):
                G.add_edge(destination_node, grid_nodes[j * n + n - 1])
    else:
        # Connect the destination nodes to the rightmost column node in their row only
        for i in range(n):
            destination_node = destination_nodes[i]
            G.add_edge(destination_node, grid_nodes[(i + 1) * n - 1])

    # Connect the topmost row to the bottommost row
    if top_bottom_connection:
        for i in range(n):
            top_node = grid_nodes[i]
            bottom_node = grid_nodes[(n - 1) * n + i]
            G.add_edge(top_node, bottom_node)

    pos = nx.spring_layout(G, dim=3, seed=42)  # Arrange nodes in a 3D layout
    
    if draw_network:
        plt.figure(figsize=(12, 8))  # Set the figure size

        # Draw edges
        ax = plt.axes(projection='3d')
        for edge in G.edges():
            ax.plot(
                [pos[edge[0]][0], pos[edge[1]][0]],
                [pos[edge[0]][1], pos[edge[1]][1]],
                [pos[edge[0]][2], pos[edge[1]][2]],
                'blue',
                linewidth=1)

        # Draw nodes with labels
        node_colors = ['red'] * len(G.nodes)
        ax.scatter3D(
            [pos[node][0] for node in G.nodes],
            [pos[node][1] for node in G.nodes],
            [pos[node][2] for node in G.nodes],
            c=node_colors,
            s=50)
        for node, (x, y, z) in pos.items():
            ax.text(x, y, z, node, fontsize=8, ha='center', va='center')

        ax.set_title("Network")
        plt.show()
        plt.axis('auto')  # Enable zooming functionality

    return G, grid_nodes, source_nodes, destination_nodes


HQ_eta = 0.999
LQ_eta = 0.8
def assign_noise_rate(grid_nodes, source_nodes, destination_nodes, HQ_percent, HQ_seed):
    random.seed(HQ_seed)
    noise_rates = {}

    # Assign noise rate to source nodes and destination nodes
    for node in source_nodes + destination_nodes:
        noise_rates[node] = HQ_eta

    # Calculate the number of high-quality nodes based on the HQ_percent
    num_hq_nodes = int(len(grid_nodes) * (HQ_percent / 100))

    # Assign noise rate to grid nodes randomly
    hq_nodes = random.sample(grid_nodes, num_hq_nodes)
    for node in grid_nodes:
        if node in hq_nodes:
            noise_rates[node] = HQ_eta  # High quality node
        else:
            noise_rates[node] = LQ_eta  # Low quality node
    
    return noise_rates


def get_random_sd_pairs(source_nodes, destination_nodes, sd_pair_seed):
    sd_pairs = []

    # Create copies of the source and destination node lists
    available_source_nodes = source_nodes.copy()
    available_destination_nodes = destination_nodes.copy()

    # Shuffle the available source and destination node lists in unison with the provided seed
    random.seed(sd_pair_seed)
    random.shuffle(available_source_nodes)
    random.shuffle(available_destination_nodes)

    # Generate pairs by pairing up the shuffled nodes
    for i in range(len(source_nodes)):
        source_node = available_source_nodes[i]
        destination_node = available_destination_nodes[i]
        sd_pairs.append((source_node, destination_node))

    return sd_pairs


def find_shortest_paths(sd_pairs):
    G, grid_nodes, source_nodes, destination_nodes = create_network_graph(len(sd_pairs))
    
    shortest_paths = []
    path_order = []  # Store the order of shortest paths

    # Create a set to keep track of used edges
    used_edges = set()

    # Iterate over each pair and find the shortest path using Dijkstra's algorithm
    for pair in sd_pairs:
        source_node, destination_node = pair

        try:
            # Find the shortest path
            shortest_path = nx.dijkstra_path(G, source_node, destination_node)

            # Append the shortest path to the list
            shortest_paths.append(shortest_path)

            # Mark the edges in the shortest path as used
            for i in range(len(shortest_path) - 1):
                edge = (shortest_path[i], shortest_path[i + 1])
                used_edges.add(edge)

            # Remove used edges from the graph
            G.remove_edges_from(used_edges)

            # Add the path order
            path_order.append(len(path_order) + 1)

        except nx.NetworkXNoPath:
            # Append an empty list if shortest path cannot be found
            shortest_paths.append([])
            path_order.append(len(path_order) + 1)

    return shortest_paths, path_order


def calculate_fidelity(noise_rates, path):
    # Initialize variables to track the number of HQ and LQ nodes in the path
    num_hq_nodes = 0
    num_lq_nodes = 0

    # Count the number of HQ and LQ nodes in the path
    if path:
        for node in path:
            if node in noise_rates:
                if noise_rates[node] == HQ_eta:
                    num_hq_nodes += 1
                elif noise_rates[node] == LQ_eta:
                    num_lq_nodes += 1

        # Set the initial fidelity constant
        F = 0.975

        # Calculate the fidelity
        fidelity = ((1/4) * (1 + 3 * (((4 * (HQ_eta ** 2) - 1) / 3) ** (num_hq_nodes)) *
                            (((4 * (LQ_eta ** 2) - 1) / 3) ** (num_lq_nodes)) *
                            (((4 * F - 1) / 3) ** (num_hq_nodes + num_lq_nodes + 1))))
    
    else:
        fidelity = 'NA'

    return fidelity, num_hq_nodes, num_lq_nodes


def generate_sd_pairs(source_nodes, destination_nodes, num_combinations):
    sd_pairs_combinations = []
    for i in range(num_combinations):
        sd_pairs = get_random_sd_pairs(source_nodes, destination_nodes, i)
        sd_pairs_combinations.append(sd_pairs)
    return sd_pairs_combinations


def compute_fidelity_for_all_paths(sd_pairs_combinations, noise_rates):
    all_paths_fidelity = []
    for sd_pairs in sd_pairs_combinations:
        shortest_paths, path_order = find_shortest_paths(sd_pairs)
        for order, path in zip(path_order, shortest_paths):  # Use zip to iterate through both path_order and shortest_paths simultaneously
            logging.info(
                f"Fidelity calculation configuration: SD Pairs = {sd_pairs}, Path = {path}, Order = {order}, \n"
            )
            fidelity, num_hq_nodes, num_lq_nodes = calculate_fidelity(noise_rates, path)
            all_paths_fidelity.append((sd_pairs, path, len(path), order, fidelity))
    return all_paths_fidelity


def save_to_csv(all_paths_fidelity, HQ_seed, HQ_percent):
    with open('2_edge_network_app2.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for sd_pairs, path, path_length, path_order, fidelity in all_paths_fidelity:
            writer.writerow([HQ_percent, HQ_seed, path, sd_pairs, path_length, path_order, fidelity])



def main():
    n = 5  # grid size
    num_combinations = 5  # number of sd_pairs combinations

    # Create the network graph
    _ , grid_nodes, source_nodes, destination_nodes = create_network_graph(n)

    with open('2_edge_network_app2.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["HQ_percent", "HQ_seed", "path", "sd_pairs", "path_length", "path_order", "fidelity"])

    for HQ_percent in range(0, 101, 4):
        for HQ_seed in range(1, 101, 1):
            logging.info(
                    f"Main configuration: HQ_percent = {HQ_percent}, HQ_seed = {HQ_seed} \n"
                    )
            # Assign noise rate to nodes
            noise_rates = assign_noise_rate(grid_nodes, source_nodes, destination_nodes, HQ_percent, HQ_seed)

            # Generate sd_pairs combinations
            sd_pairs_combinations = generate_sd_pairs(source_nodes, destination_nodes, num_combinations)

            # Compute fidelity for all paths
            all_paths_fidelity = compute_fidelity_for_all_paths(sd_pairs_combinations, noise_rates)

            # Save the data to a CSV file
            save_to_csv(all_paths_fidelity, HQ_seed, HQ_percent)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()