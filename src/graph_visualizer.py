import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(G):
    plt.figure(figsize=(10,7))
    pos = nx.spring_layout(G, seed=42)
    labels = {node: f"{node}\n{data['label']}" for node, data in G.nodes(data=True)}
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color="lightblue", font_size=8, font_weight="bold", arrows=True)
    edge_labels = {(u, v): d['relation'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title("Agentic Knowledge Graph (CSV-based)")
    plt.show()
