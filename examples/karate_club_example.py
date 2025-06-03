# examples/karate_club_example.py
import networkx as nx


def create_karate_club_graph_data() -> nx.Graph:  # type: ignore[type-arg]
    G: nx.Graph = nx.karate_club_graph()  # type: ignore[type-arg]
    for node_id, data in G.nodes(data=True):
        data["label"] = str(node_id)
        data["title"] = f"Member {node_id}\nClub: {data['club']}"
        data["group"] = data["club"]
        data["value"] = G.degree(node_id)
    return G


karate_club_vis_options = {
    "nodes": {
        "scaling": {"min": 10, "max": 30, "label": {"enabled": False}},
        "font": {"size": 12},
    },
    "edges": {"width": 0.5, "color": "silver", "smooth": False},
    "groups": {
        "Mr. Hi": {
            "color": {"background": "orange", "border": "darkorange"},
            "shape": "dot",
        },
        "Officer": {
            "color": {"background": "purple", "border": "indigo"},
            "shape": "ellipse",
        },
    },
    "physics": {
        "stabilization": {"iterations": 1200},
        "barnesHut": {
            "gravitationalConstant": -10000,
            "springLength": 120,
            "avoidOverlap": 0.1,
        },
    },
    "layout": {"randomSeed": 42},
    "interaction": {"tooltipDelay": 200, "hover": True},
}
