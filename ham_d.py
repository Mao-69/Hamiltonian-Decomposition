import ast
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import numpy as np

def draw_combined_graph(G, central_node):
    pos = nx.spring_layout(G, dim=3)
    pos_without_central = pos.copy()
    pos_without_central.pop(central_node, None)
    central_pos = np.mean(list(pos_without_central.values()), axis=0)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for node, position in pos.items():
        if node != central_node:
            ax.scatter(position[0], position[1], position[2], color='b')
            ax.text(position[0], position[1], position[2], f"|{node}>", fontsize=8, color='black')

    for node, position in pos.items():
        if node != central_node:
            ax.plot([position[0], central_pos[0]], [position[1], central_pos[1]], [position[2], central_pos[2]], color='k')

    for edge in G.edges():
        start, end = edge
        if start != central_node and end != central_node and start in G.nodes() and end in G.nodes():
            ax.plot([pos[start][0], pos[end][0]], [pos[start][1], pos[end][1]], [pos[start][2], pos[end][2]], color='gray', linestyle='--')

    ax.scatter(central_pos[0], central_pos[1], central_pos[2], color='g', s=100)
    ax.text(central_pos[0], central_pos[1], central_pos[2], f"|{central_node}>", fontsize=8, color='black')
    ax.set_axis_off()
    all_node_positions = np.array(list(pos_without_central.values()) + [central_pos])
    min_coord = np.min(all_node_positions, axis=0)
    max_coord = np.max(all_node_positions, axis=0)
    ax.set_xlim([min_coord[0] - 0.1, max_coord[0] + 0.1])
    ax.set_ylim([min_coord[1] - 0.1, max_coord[1] + 0.1])
    ax.set_zlim([min_coord[2] - 0.1, max_coord[2] + 0.1])
    ax.view_init(elev=20, azim=45)
    ax.mouse_init()
    plt.show()

numbers_input = input("Enter a list of numbers in the format [x1, x2, x3, ...]: ")

try:
    numbers = ast.literal_eval(numbers_input)
except ValueError:
    print("Invalid input. Please enter numbers in the correct format.")
    exit()

central_node = int(input("Enter the central node: "))
G = nx.Graph()
for number in numbers:
    if number != central_node:
        G.add_edge(number, central_node)

for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        if numbers[i] != central_node and numbers[j] != central_node:
            G.add_edge(numbers[i], numbers[j])

draw_combined_graph(G, central_node)
