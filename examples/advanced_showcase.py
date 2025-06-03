# examples/advanced_showcase.py

import os
import random
from typing import Any

import networkx as nx

from nx_vis_visualizer import nx_to_vis


def create_showcase_graph() -> nx.Graph[Any]:
    """Creates a more complex NetworkX graph for demonstration."""
    G: nx.Graph[Any] = nx.Graph(name="Advanced Showcase Graph")

    # --- Add Nodes with various properties ---
    num_random_nodes = 20
    for i in range(num_random_nodes):
        G.add_node(
            f"R{i}",  # Random node
            label=f"R{i}",
            group=i % 4,  # Assign to one of 4 groups
            value=(i % 5) + 1,  # For size scaling (1 to 5)
            title=f"Random Node R{i}\nGroup: {i % 4}\nValue: {(i % 5) + 1}",
            font={"color": "black", "size": 10} if i % 4 == 0 else {},
        )

    # Special, styled nodes
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
        group=4,  # Special group
        title="This is the main Source node",
        font={
            "size": 16,
            "color": "darkgreen",
            "face": "Arial",
            "strokeWidth": 1,
            "strokeColor": "white",
        },
        fixed={"x": True, "y": True},  # Fix position
        x=-400,
        y=-200,  # Specify coordinates
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
        font={
            "multi": "html",
            "bold": "18px arial darkblue",
        },  # Using multi-font for bold
    )
    G.add_node(
        "Isolated",
        label="I'm Alone",
        shape="text",
        title="An isolated node example",
        color="#FFCCFF",  # Light pink
        font={"size": 12, "color": "purple"},
    )

    # --- Add Edges with various properties ---
    # Connect Source to some random nodes and Hub
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

    # Connect some random nodes to Hub and Sink
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

    # Inter-random node connections
    for i in range(num_random_nodes - 1):
        if random.random() < 0.2:  # Sparsely connect random nodes
            G.add_edge(
                f"R{i}",
                f"R{i + 1}",
                weight=1,
                color="#cccccc",
                title=f"R{i}-R{i + 1}",
            )

    # Add an edge with a complex color object
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


if __name__ == "__main__":
    showcase_graph = create_showcase_graph()

    # --- Define Custom Vis.js Options ---
    # Start with a deep copy of defaults if you want to modify them,
    # or define options from scratch for full control.
    # For this showcase, let's define many options explicitly.
    custom_vis_options: dict[str, Any] = {
        "nodes": {
            "borderWidth": 2,
            "borderWidthSelected": 4,
            "font": {
                "size": 12,
                "face": "Tahoma",
                "color": "#333333",  # Default node font color
            },
            "scaling": {  # Scale node size based on 'value' attribute
                "min": 10,
                "max": 30,
                "label": {"enabled": True, "min": 8, "max": 20},
            },
            "shadow": {"enabled": True, "size": 5, "x": 3, "y": 3},
        },
        "edges": {
            "width": 1,  # Default edge width
            "color": {
                "color": "#848484",
                "highlight": "#000000",
                "hover": "#555555",
                "inherit": "from",  # Inherit color from 'from' node, or 'both', 'to', False
                "opacity": 1.0,
            },
            "arrows": {  # Default arrow settings (can be overridden by individual edges)
                "to": {"enabled": False, "scaleFactor": 0.8, "type": "arrow"},
                # "middle": {"enabled": True, "scaleFactor":0.5, "type":"circle"},
                # "from": {"enabled": False}
            },
            "smooth": {
                "enabled": True,
                "type": "dynamic",  # "dynamic", "continuous", "discrete", "diagonalCross", "straightCross", "horizontal", "vertical", "curvedCW", "curvedCCW", "cubicBezier"
                "roundness": 0.5,
            },
            "font": {
                "size": 10,
                "color": "black",
                "strokeWidth": 0,  # No stroke for edge labels by default
                "align": "horizontal",  # "top", "middle", "bottom"
            },
            "scaling": {  # Scale edge width based on 'weight' attribute
                "min": 1,
                "max": 8,
                "label": {"enabled": False},
            },
            "hoverWidth": 1.5,
            "selectionWidth": 2,
        },
        "groups": {
            0: {
                "color": {"background": "cyan", "border": "blue"},
                "shape": "dot",
            },
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
            4: {
                "borderWidth": 3,
                "shadow": {"enabled": False},
            },  # Special group for Source/Sink
            5: {"shape": "hexagon", "color": "lightgray"},  # Hub group
        },
        "layout": {
            "randomSeed": 42,  # For reproducible layout if physics is re-enabled
            "improvedLayout": True,
            # Example for hierarchical layout (disable physics if using this)
            # "hierarchical": {
            #     "enabled": False,
            #     "direction": "UD",  # UD, DU, LR, RL
            #     "sortMethod": "directed",  # hubsize, directed
            #     "shakeTowards": "roots"
            # }
        },
        "interaction": {
            "hover": True,
            "dragNodes": True,  # Can nodes be dragged?
            "dragView": True,  # Can the view be dragged?
            "zoomView": True,
            "navigationButtons": True,  # Show zoom and fit buttons
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
            "enabled": True,  # Nodes with fixed:true will ignore physics
            "solver": "barnesHut",  # barnesHut, forceAtlas2Based, repulsion, hierarchicalRepulsion
            "barnesHut": {
                "gravitationalConstant": -15000,
                "centralGravity": 0.1,
                "springLength": 120,
                "springConstant": 0.05,
                "damping": 0.15,
                "avoidOverlap": 0.2,
            },
            # "forceAtlas2Based": {
            #     "gravitationalConstant": -50,
            #     "centralGravity": 0.01,
            #     "springLength": 100,
            #     "springConstant": 0.08,
            #     "damping": 0.4,
            #     "avoidOverlap": 0
            # },
            "stabilization": {  # Run stabilization before displaying
                "enabled": True,
                "iterations": 1000,  # More iterations for better layout
                "updateInterval": 50,
                "onlyDynamicEdges": False,
                "fit": True,  # Fit the network to the screen after stabilization
            },
            "adaptiveTimestep": True,
            "minVelocity": 0.75,
        },
        "configure": {  # Show the configuration GUI
            "enabled": True,
            # "filter": "nodes,edges,layout,interaction,physics", # String or array or function
            "showButton": False,  # Show a button to toggle the configurator
        },
    }

    # Define output path relative to this script for cleanliness
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "advanced_showcase_graph.html")

    print(
        f"Generating advanced showcase graph with {showcase_graph.number_of_nodes()} nodes and {showcase_graph.number_of_edges()} edges..."
    )
    file_path = nx_to_vis(
        showcase_graph,
        output_filename=output_file,
        html_title="NX-VIS Visualizer - Advanced Showcase",
        vis_options=custom_vis_options,
        show_browser=True,
        graph_height="90vh",  # Make it take most of the viewport height
        graph_width="100%",
    )

    if file_path:
        print(f"Advanced showcase graph saved to: {file_path}")
        print(
            "Open this HTML file in your browser to see the interactive graph."
        )
        print(
            "Try using the configuration panel (usually a button at the bottom) to tweak settings live!"
        )
    else:
        print("Failed to generate the advanced showcase graph.")
