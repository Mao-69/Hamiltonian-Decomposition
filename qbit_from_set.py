import ast
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import numpy as np
import math

def entanglement_strength(distance, alpha):
    return 1 / (alpha * distance + 1)

def von_neumann_entropy(rho):
    eigenvalues = np.linalg.eigvalsh(rho)
    non_zero_eigenvalues = eigenvalues[eigenvalues > 0]
    entropy = -np.sum(non_zero_eigenvalues * np.log2(non_zero_eigenvalues))
    return entropy

def draw_combined_graph(G, central_node, alpha):
    pos = nx.spring_layout(G, dim=3)
    pos_without_central = pos.copy()
    pos_without_central.pop(central_node, None)
    central_pos = np.mean(list(pos_without_central.values()), axis=0)
    distances = {node: abs(node - central_node) for node in G.nodes()}
    entanglement_strengths = [entanglement_strength(distances[node], alpha) for node in G.nodes()]
    average_entanglement = np.mean(entanglement_strengths)
    num_qubits = sum([len(format(node, 'b')) for node in G.nodes()])
    entanglement_entropy = -num_qubits * average_entanglement * math.log2(average_entanglement)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, (node, position) in enumerate(pos.items()):
        if node != central_node:
            color = plt.cm.viridis(entanglement_strengths[i] / max(entanglement_strengths))
            ax.scatter(position[0], position[1], position[2], color=color, s=100)
            ax.text(position[0], position[1], position[2], f"|{node}> ({entanglement_strengths[i]*100:.2f}%)", fontsize=8, color='black')

    for node, position in pos.items():
        if node != central_node:
            ax.plot([position[0], central_pos[0]], [position[1], central_pos[1]], [position[2], central_pos[2]], color='k')

    for i in range(len(G.nodes())):
        for j in range(i + 1, len(G.nodes())):
            node_i = list(G.nodes())[i]
            node_j = list(G.nodes())[j]
            if distances[node_i] <= node_i and distances[node_j] <= node_j:
                ax.plot([pos[node_i][0], pos[node_j][0]], [pos[node_i][1], pos[node_j][1]], [pos[node_i][2], pos[node_j][2]], color='gray', linestyle='--')

    ax.scatter(central_pos[0], central_pos[1], central_pos[2], color='g', s=100)
    ax.text(central_pos[0], central_pos[1], central_pos[2], f"|{central_node}>", fontsize=8, color='black')
    all_node_positions = np.array(list(pos_without_central.values()) + [central_pos])
    min_coord = np.min(all_node_positions, axis=0)
    max_coord = np.max(all_node_positions, axis=0)
    ax.set_xlim([min_coord[0] - 0.1, max_coord[0] + 0.1])
    ax.set_ylim([min_coord[1] - 0.1, max_coord[1] + 0.1])
    ax.set_zlim([min_coord[2] - 0.1, max_coord[2] + 0.1])
    ax.view_init(elev=20, azim=45)
    ax.mouse_init()
    ax.text2D(0.5, 0.95, f"Total Entanglement Entropy: {entanglement_entropy:.2f} bits", transform=ax.transAxes, ha='center')
    plt.show()

numbers_input = input("Enter a list of numbers in the format [x1, x2, x3, ...]: ")

try:
    numbers = ast.literal_eval(numbers_input)
except ValueError:
    print("Invalid input. Please enter numbers in the correct format.")
    exit()

central_node = int(input("Enter the central node: "))
alpha = float(input("Enter the alpha parameter for entanglement strength: "))
G = nx.Graph()
for number in numbers:
    if number != central_node:
        G.add_edge(number, central_node)
draw_combined_graph(G, central_node, alpha)
