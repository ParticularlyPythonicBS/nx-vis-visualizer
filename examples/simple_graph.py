# examples/simple_graph.py
import copy
import os
from typing import Any

import networkx as nx

from nx_vis_visualizer import (
    DEFAULT_VIS_OPTIONS,
    nx_to_vis,
)

# Create a sample graph
G = nx.complete_graph(5)
for i in G.nodes():
    G.nodes[i]["label"] = f"Node {i + 1}"
    G.nodes[i]["title"] = f"This is node {i + 1} with degree {G.degree(i)}"
    G.nodes[i]["value"] = G.degree(i)  # Example: size node by degree
    G.nodes[i]["group"] = i % 2  # Assign to one of two groups

# Customize options
my_options: dict[str, Any] = copy.deepcopy(DEFAULT_VIS_OPTIONS)
my_options["nodes"]["shape"] = "box"
my_options["edges"]["color"] = "lightgray"
my_options["physics"]["enabled"] = True
my_options["interaction"]["hover"] = True
my_options["groups"] = {
    0: {"color": "skyblue", "font": {"color": "black"}},
    1: {"color": "lightcoral", "font": {"color": "white"}},
}
# Scale node size based on 'value' attribute if you want
# my_options['nodes']['scaling'] = {
#  "min": 10,
#  "max": 30,
#  "label": {"enabled": True, "min": 8, "max": 20}
# }


# Define output path relative to this script for cleanliness
current_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(current_dir, "complete_graph_example.html")


if __name__ == "__main__":
    print("Generating example graph...")
    file_path = nx_to_vis(
        G,
        output_filename=output_file,
        html_title="Complete Graph (k=5) Example",
        vis_options=my_options,
        show_browser=True,
        graph_height="600px",
        graph_width="800px",
    )
    if file_path:
        print(f"Example graph saved to: {file_path}")
    else:
        print("Failed to generate example graph.")
