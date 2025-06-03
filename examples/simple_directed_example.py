# examples/simple_directed_example.py
import networkx as nx


def create_simple_directed_graph_data() -> nx.DiGraph:  # type: ignore[type-arg]
    DG: nx.DiGraph = nx.DiGraph()  # type: ignore[type-arg]
    DG.add_edges_from(
        [
            (1, 2, {"label": "Rel A"}),
            (1, 3, {"label": "Rel B"}),
            (2, 4, {"label": "Rel C"}),
            (3, 4, {"label": "Rel D"}),
            (4, 1, {"label": "Rel E (Cycle)"}),
        ]
    )
    for i in DG.nodes():
        DG.nodes[i]["label"] = f"DNode {i}"
        DG.nodes[i]["title"] = f"This is directed node {i}"
        if i == 1:
            DG.nodes[i]["color"] = "lightcoral"
            DG.nodes[i]["shape"] = "star"
        if i == 4:
            DG.nodes[i]["color"] = "lightgreen"
    return DG


simple_directed_vis_options = {
    "edges": {
        "arrows": {"to": {"enabled": True, "scaleFactor": 1, "type": "arrow"}},
        "font": {"align": "middle", "size": 10},
        "smooth": {"enabled": True, "type": "curvedCW", "roundness": 0.2},
    },
    "nodes": {"font": {"size": 14}},
    "physics": {"enabled": True},
    "layout": {
        "hierarchical": False,  # This was the key for the previous bug fix
        "randomSeed": 789,
    },
    "interaction": {"navigationButtons": True, "hover": True},
}
