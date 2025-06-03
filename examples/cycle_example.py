# examples/cycle_example.py
import networkx as nx


def create_cycle_graph_data() -> nx.Graph:  # type: ignore[type-arg]
    G: nx.Graph = nx.cycle_graph(5)  # type: ignore[type-arg]
    for i, node_id in enumerate(G.nodes()):
        G.nodes[node_id]["label"] = f"N{i + 1}"
        G.nodes[node_id]["title"] = f"Tooltip for Node N{i + 1}"
        G.nodes[node_id]["group"] = i % 2
        if i == 0:
            G.nodes[node_id]["color"] = "skyblue"
            G.nodes[node_id]["size"] = 25
    G.edges[0, 1]["label"] = "Link 0-1"
    G.edges[0, 1]["color"] = "green"
    G.edges[0, 1]["width"] = 3
    return G


cycle_graph_vis_options = {  # Renamed for clarity
    "nodes": {"font": {"size": 14}},
    "edges": {"smooth": {"enabled": True, "type": "dynamic"}},
    "groups": {
        "0": {
            "shape": "dot",
            "color": {"background": "lightcoral", "border": "red"},
        },
        "1": {
            "shape": "square",
            "color": {"background": "lightgreen", "border": "green"},
        },
    },
    "interaction": {"hover": True, "navigationButtons": True},
    "physics": {"enabled": True, "solver": "barnesHut"},
    "layout": {"randomSeed": 12345},
}
