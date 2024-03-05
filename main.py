import argparse

import matplotlib.pyplot as plt
import networkx as nx
import torch
import torch_geometric
from torch_geometric.data import Data

# Define all relevant system calls
relevant_syscalls = {
    "recvfrom", "write", "ioctl", "read", "sendto", "writev", "close", "socket", "bind", "connect",
    "mkdir", "access", "chmod", "open", "fchown", "rename", "unlink", "umask", "recvmsg", "sendmsg",
    "getdents64", "epoll_wait", "dup", "pread", "pwrit", "fcntl64"
}
file_syscalls = {
    "open", "mkdir", "rmdir", "access", "chmod", "rename", "unlink", "getdents64", "dup", "pread", "pwrit", "fcntl64"
}
network_syscalls = {
    "recvfrom", "write", "read", "sendto", "writev", "close", "socket", "bind", "connect",
    "recvmsg", "sendmsg", "epoll_wait"
}


def read_syscalls(file_path, filter_calls):
    with open(file_path, 'r') as file:
        if filter_calls:
            syscalls = [line.split('(')[0] for line in file if line.split('(')[0] in relevant_syscalls]
        else:
            syscalls = [line.split('(')[0] for line in file]
    return syscalls


def get_syscall_type_encoding(syscall):
    if syscall in file_syscalls:
        return [1, 0, 0]  # File syscall node
    elif syscall in network_syscalls:
        return [0, 1, 0]  # Network syscall node
    else:
        return [0, 0, 1]  # Default (other) syscall node


def create_graph(syscalls):
    unique_syscalls = list(set(syscalls))
    num_nodes = len(unique_syscalls)
    node_mapping = {syscall: i for i, syscall in enumerate(unique_syscalls)}

    G = nx.DiGraph()  # Create a directed graph using NetworkX
    edge_counter = {}
    for i in range(len(syscalls) - 1):
        src = node_mapping[syscalls[i]]
        dst = node_mapping[syscalls[i + 1]]
        edge = (src, dst)
        edge_counter[edge] = edge_counter.get(edge, 0) + 1
        if G.has_edge(src, dst):
            G[src][dst]['weight'] += 1
        else:
            G.add_edge(src, dst, weight=1)

    # Compute centrality measures
    katz_centrality = nx.katz_centrality_numpy(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)

    # Define nodes and their features
    node_features = []
    for syscall in unique_syscalls:
        node_idx = node_mapping[syscall]
        katz = katz_centrality[node_idx]
        betweenness = betweenness_centrality[node_idx]
        closeness = closeness_centrality[node_idx]
        print(syscall, f'katz: {katz}', f'betweeness: {betweenness}', f'closeness: {closeness}')
        syscall_type_encoding = get_syscall_type_encoding(syscall)
        # Append all centralities to the node features
        node_features.append(syscall_type_encoding + [katz, betweenness, closeness])

    x = torch.tensor(node_features, dtype=torch.float)
    edge_index = list(G.edges())
    edge_features = [edge_counter[edge] for edge in edge_index]
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_features = torch.tensor(edge_features, dtype=torch.float)

    graph = Data(x=x, edge_index=edge_index, num_nodes=num_nodes, edge_features=edge_features)

    return graph, node_mapping


def plot_graph(file_path, filter_calls, graph, node_mapping):
    g = torch_geometric.utils.to_networkx(graph, to_undirected=False)
    pos = nx.spring_layout(g)
    reverse_mapping = {i: syscall for syscall, i in node_mapping.items()}

    # Extract node colors based on their features
    node_colors = [graph.x[i].tolist().index(1) for i in range(graph.num_nodes)]

    # Extract edge labels based on the edge_features
    edge_labels = {tuple(graph.edge_index[:, i].tolist()): int(graph.edge_features[i].item()) for i in range(graph.edge_features.size(0))}

    # Define color map for nodes
    color_map = {0: '#3366CC', 1: '#DC3912', 2: '#FF9900'}

    # Set the figure size
    plt.figure(figsize=(10, 6))  # Adjust the size as needed

    # Draw nodes with different colors and labels
    nx.draw_networkx_nodes(g, pos, node_color=[color_map[color] for color in node_colors], node_size=100)
    labels = {node: reverse_mapping[node] for node in g.nodes()}
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=8)

    # Draw edges with labels
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=8)

    # Set the legend for node colors to the top-right
    node_labels = {'File syscall node': '#3366CC', 'Network syscall node': '#DC3912', 'Default (other) syscall node': '#FF9900'}
    patches = [plt.Line2D([], [], marker='o', color=color, markersize=8, linestyle='None', label=label) for label, color in node_labels.items()]
    plt.legend(handles=patches, title='Node Features', loc='upper right')

    plt.axis('off')
    plt.savefig(f'{file_path}.png') if not filter_calls else plt.savefig(f'{file_path}_filtered.png')
    # plt.show()


def main(file_path, filter_calls):
    syscalls = read_syscalls(file_path, filter_calls)
    graph, node_mapping = create_graph(syscalls)

    plot_graph(file_path, filter_calls, graph, node_mapping)


if __name__ == "__main__":
    # python main.py ./strace_generator/strace_output_example1 --filter

    parser = argparse.ArgumentParser(description='Process system call data and visualize as a graph.')
    parser.add_argument('file_path', type=str, help='Path to the file containing system calls')
    parser.add_argument('--filter', action='store_true', help='Filter to include only relevant system calls')

    args = parser.parse_args()

    main(args.file_path, args.filter)
