from utils import load_csv_data
from kg_builder import build_knowledge_graph
from graph_visualizer import visualize_graph
from agents import infer_relationships

def main():
    data = load_csv_data()
    infer_relationships(data)
    G = build_knowledge_graph(data)
    visualize_graph(G)

if __name__ == "__main__":
    main()
