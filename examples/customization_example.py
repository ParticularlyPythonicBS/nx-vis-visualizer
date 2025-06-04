# examples/advanced_showcase.py

import random
from typing import Any

import networkx as nx


def create_showcase_graph() -> nx.Graph:  # type: ignore[type-arg]
    """Creates a more complex NetworkX graph for demonstration."""
    G: nx.Graph = nx.Graph(name="Advanced Showcase Graph")  # type: ignore[type-arg]

    # --- Add Nodes with various properties ---
    num_random_nodes = 20
    for i in range(num_random_nodes):
        G.add_node(
            f"R{i}",  # Random node
            label=f"R{i}",
            group=i % 4,
            value=(i % 5) + 1,
            title=f"Random Node R{i}\nGroup: {i % 4}\nValue: {(i % 5) + 1}",
            font={"color": "black", "size": 10} if i % 4 == 0 else {},
        )
    G.add_node(
        "Source",
        label="START",
        shape="diamond",
        color={
            "background": "lightgreen",
            "border": "darkgreen",
            "highlight": {"background": "green", "border": "darkgreen"},
        },
        size=30,
        group=4,
        title="This is the main Source node",
        font={
            "size": 16,
            "color": "darkgreen",
            "face": "Arial",
            "strokeWidth": 1,
            "strokeColor": "white",
        },
        fixed={"x": True, "y": True},
        x=-400,
        y=-200,
    )
    G.add_node(
        "Sink",
        label="END",
        shape="star",
        color="gold",
        size=30,
        group=4,
        title="This is the main Sink node",
        font={"size": 16, "color": "black", "face": "Georgia"},
        fixed={"x": True, "y": True},
        x=400,
        y=200,
    )
    G.add_node(
        "Hub",
        label="Central Hub",
        shape="ellipse",
        color="lightblue",
        size=25,
        group=5,
        title="A central connecting hub",
        font={"multi": "html", "bold": "18px arial darkblue"},
    )
    G.add_node(
        "Isolated",
        label="I'm Alone",
        shape="text",
        title="An isolated node example",
        color="#FFCCFF",
        font={"size": 12, "color": "purple"},
    )

    # --- Add Edges with various properties ---
    for i in range(0, num_random_nodes, 5):
        G.add_edge(
            "Source",
            f"R{i}",
            weight=(i % 3) + 1,
            color="darkgreen",
            label=f"S->R{i}",
        )
    G.add_edge(
        "Source",
        "Hub",
        weight=5,
        color="darkgreen",
        width=4,
        title="Main link to Hub",
    )
    for i in range(1, num_random_nodes, 4):
        G.add_edge(
            f"R{i}",
            "Hub",
            weight=(i % 2) + 1,
            dashes=[5, 5],
            color="gray",
            title=f"R{i} to Hub",
        )
        if i + 2 < num_random_nodes:
            G.add_edge(
                f"R{i + 2}",
                "Sink",
                weight=3,
                color="orange",
                label=f"R{i + 2}->E",
                arrows="to",
            )
    G.add_edge(
        "Hub",
        "Sink",
        weight=5,
        color="blue",
        width=4,
        title="Main link from Hub to Sink",
        arrows="to",
        smooth={"type": "curvedCW", "roundness": 0.2},
    )
    for i in range(num_random_nodes - 1):
        if random.random() < 0.2:
            G.add_edge(
                f"R{i}",
                f"R{i + 1}",
                weight=1,
                color="#cccccc",
                title=f"R{i}-R{i + 1}",
            )
    if num_random_nodes > 5:
        G.add_edge(
            "R0",
            "R5",
            color={
                "color": "red",
                "highlight": "darkred",
                "hover": "pink",
                "opacity": 0.7,
            },
            label="Opacity Edge",
            weight=2,
        )
    return G


# --- Define Custom Vis.js Options at the module level ---
custom_vis_options: dict[str, Any] = {
    "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "font": {"size": 12, "face": "Tahoma", "color": "#333333"},
        "scaling": {
            "min": 10,
            "max": 30,
            "label": {"enabled": True, "min": 8, "max": 20},
        },
        "shadow": {"enabled": True, "size": 5, "x": 3, "y": 3},
    },
    "edges": {
        "width": 1,
        "color": {
            "color": "#848484",
            "highlight": "#000000",
            "hover": "#555555",
            "inherit": "from",
            "opacity": 1.0,
        },
        "arrows": {
            "to": {"enabled": False, "scaleFactor": 0.8, "type": "arrow"}
        },
        "smooth": {"enabled": True, "type": "dynamic", "roundness": 0.5},
        "font": {
            "size": 10,
            "color": "black",
            "strokeWidth": 0,
            "align": "horizontal",
        },
        "scaling": {"min": 1, "max": 8, "label": {"enabled": False}},
        "hoverWidth": 1.5,
        "selectionWidth": 2,
    },
    "groups": {
        0: {"color": {"background": "cyan", "border": "blue"}, "shape": "dot"},
        1: {
            "color": {"background": "pink", "border": "purple"},
            "shape": "square",
            "font": {"color": "purple"},
        },
        2: {
            "color": {"background": "yellow", "border": "orange"},
            "shape": "triangle",
        },
        3: {
            "color": {"background": "lime", "border": "green"},
            "shape": "triangleDown",
        },
        4: {"borderWidth": 3, "shadow": {"enabled": False}},
        5: {"shape": "hexagon", "color": "lightgray"},
    },
    "layout": {"randomSeed": 42, "improvedLayout": True},
    "interaction": {
        "hover": True,
        "dragNodes": True,
        "dragView": True,
        "zoomView": True,
        "navigationButtons": True,
        "tooltipDelay": 200,
        "keyboard": {
            "enabled": True,
            "speed": {"x": 10, "y": 10, "zoom": 0.05},
            "bindToWindow": True,
        },
        "multiselect": True,
        "selectable": True,
        "selectConnectedEdges": True,
    },
    "physics": {
        "enabled": True,
        "solver": "barnesHut",
        "barnesHut": {
            "gravitationalConstant": -15000,
            "centralGravity": 0.1,
            "springLength": 120,
            "springConstant": 0.05,
            "damping": 0.15,
            "avoidOverlap": 0.2,
        },
        "stabilization": {
            "enabled": True,
            "iterations": 1000,
            "updateInterval": 50,
            "onlyDynamicEdges": False,
            "fit": True,
        },
        "adaptiveTimestep": True,
        "minVelocity": 0.75,
    },
    "configure": {"enabled": True, "showButton": False},
}
