# Advanced Customization Showcase

This page demonstrates a graph with a wide variety of node and edge customizations, physics settings, and interaction options available through `vis_options`.

The graph includes:
- Nodes with different shapes, colors, sizes, and groups.
- Fixed position nodes.
- Nodes with multi-font labels.
- Edges with different colors, widths, dashing, and labels.
- Edges with explicit arrowheads.
- Edges with complex color objects (including hover and opacity).
- Node and edge size scaling based on attributes (`value` and `weight`).
- Group-based styling.
- An interactive configuration panel (usually appears at the bottom or can be toggled) to tweak Vis.js settings live.

<div class="interactive-graph-wrapper" style="margin-bottom: 1.5em; padding: 1em; border: 1px solid #e0e0e0; border-radius: 4px; background-color: #f9f9f9;">
    <h4 style="margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em;">Advanced Customization Example</h4>
    <iframe src="/assets/generated_graphs/advanced_showcase_example.html"
            width="100%"
            height="700px"
            style="border: 1px solid #ccc; max-width: 100%; display: block;"
            sandbox="allow-scripts allow-same-origin allow-popups allow-forms">
        Your browser does not support iframes. Please update your browser.
    </iframe>
</div>

The Python code to generate the graph structure can be found in `examples/advanced_showcase.py`. Here's a snippet of how nodes and edges are defined:

```python
# From examples/advanced_showcase.py (snippet)
import networkx as nx
import random

def create_showcase_graph():
    G = nx.Graph(name="Advanced Showcase Graph")

    # Special, styled nodes
    G.add_node(
        "Source",
        label="START",
        shape="diamond",
        color={"background": "lightgreen", "border": "darkgreen"},
        size=30,
        fixed={"x": True, "y": True}, x=-400, y=-200,
        # ... other attributes
    )
    # ... more nodes ...

    G.add_edge(
        "Hub", "Sink", weight=5, color="blue", width=4,
        title="Main link from Hub to Sink", arrows="to",
        smooth={"type": "curvedCW", "roundness": 0.2}
    )
    # ... more edges ...
    return G
```

The extensive `vis_options` used for this graph (defined as `custom_vis_options` in `examples/advanced_showcase.py`):
```json
// From examples/advanced_showcase.py (snippet of custom_vis_options)
{
    "nodes": {
        "borderWidth": 2,
        "scaling": {
            "min": 10,
            "max": 30,
            "label": {"enabled": True, "min": 8, "max": 20}
        },
        "shadow": {"enabled": True, "size": 5, "x": 3, "y": 3}
    },
    "edges": {
        "width": 1,
        "color": {
            "inherit": "from",
            "opacity": 1.0
        },
        "arrows": {
            "to": {"enabled": False, "scaleFactor": 0.8, "type": "arrow"}
        },
        "smooth": {"enabled": True, "type": "dynamic", "roundness": 0.5},
        "scaling": {"min": 1, "max": 8}
    },
    "groups": { /* ... group definitions ... */ },
    "interaction": {
        "navigationButtons": True,
        "keyboard": {"enabled": True}
    },
    "physics": {
        "enabled": True,
        "solver": "barnesHut",
        "stabilization": {"enabled": True, "iterations": 1000, "fit": True}
    },
    "configure": {"enabled": True, "showButton": False }
}
```
*Note: The configuration panel is enabled for this graph, allowing live tweaking of options.*
