import networkx as nx

def build_knowledge_graph(data_dict):
    G = nx.DiGraph()

    # Add nodes and edges
    for _, row in data_dict["customers"].iterrows():
        G.add_node(row["customer_id"], label="Customer", name=row["customer_name"])

    for _, row in data_dict["agreements"].iterrows():
        G.add_node(row["agreement_id"], label="Agreement", loan=row["loan_amount"])
        G.add_edge(row["customer_id"], row["agreement_id"], relation="HAS_AGREEMENT")

    for _, row in data_dict["payments"].iterrows():
        G.add_node(row["payment_id"], label="Payment", amount=row["amount"])
        G.add_edge(row["agreement_id"], row["payment_id"], relation="HAS_PAYMENT")

    for _, row in data_dict["collateral"].iterrows():
        G.add_node(row["collateral_id"], label="Collateral", value=row["value"])
        G.add_edge(row["agreement_id"], row["collateral_id"], relation="HAS_COLLATERAL")

    return G
