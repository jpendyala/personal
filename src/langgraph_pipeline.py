from langgraph.graph import Graph
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from utils import load_csv_data
from kg_builder import build_knowledge_graph
from graph_visualizer import visualize_graph

def build_langgraph_pipeline():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    g = Graph()

    # ---- Step 1: Schema Understanding ----
    @g.node
    def schema_agent(state):
        data = state["data"]
        model_input = f"Given these CSV files: {list(data.keys())}, infer what entities and attributes they represent."
        response = model.invoke(model_input)
        state["schema_description"] = response.content
        return state

    # ---- Step 2: Relationship Builder ----
    @g.node
    def relationship_agent(state):
        schema_info = state["schema_description"]
        response = model.invoke(f"Based on schema:\n{schema_info}\nDescribe likely relationships between entities.")
        state["relationships"] = response.content
        return state

    # ---- Step 3: Graph Creator ----
    @g.node
    def graph_builder(state):
        G = build_knowledge_graph(state["data"])
        visualize_graph(G)
        state["graph"] = G
        return state

    # Chain the workflow
    g.add_edge("schema_agent", "relationship_agent")
    g.add_edge("relationship_agent", "graph_builder")
    g.set_entry_point("schema_agent")

    return g

def run_pipeline():
    data = load_csv_data("../data")
    pipeline = build_langgraph_pipeline()
    result = pipeline.invoke({"data": data})
    print("\n✅ Schema:\n", result["schema_description"])
    print("\n🔗 Relationships:\n", result["relationships"])

if __name__ == "__main__":
    run_pipeline()
