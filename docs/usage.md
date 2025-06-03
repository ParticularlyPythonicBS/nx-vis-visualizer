# Basic Usage

Using `nx-vis-visualizer` is straightforward. The primary function you'll interact with is `nx_to_vis`.

## Quick Example

Here's a minimal example to get you started:

```python
import networkx as nx
from nx_vis_visualizer import nx_to_vis

# 1. Create a NetworkX graph
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4)])
G.nodes[1]['label'] = 'Node One'
G.nodes[2]['title'] = 'This is node 2, connected to 1 and 3.' # Tooltip
G.nodes[3]['color'] = 'red'
G.edges[2,3]['label'] = 'Link'

# 2. Visualize it!
output_path = nx_to_vis(
    G,
    output_filename="my_first_graph.html",
    html_title="My First Interactive Graph",
    show_browser=True # Automatically open the generated HTML in your browser
)

print(f"Graph saved to: {output_path}")
```

This will generate an HTML file named `my_first_graph.html` in your current directory and open it in your web browser.

## Key Parameters of `nx_to_vis`

The `nx_to_vis` function accepts several parameters to customize its behavior:

* `nx_graph` (required): Your NetworkX `Graph` or `DiGraph` object.
* `output_filename` (str, optional): Name of the HTML file to generate. Defaults to `"vis_network.html"`.
* `html_title` (str, optional): The title for the HTML page. Defaults to `"NetworkX to vis.js Graph"`.
* `vis_options` (dict, optional): A Python dictionary representing [vis.js Network options](https://visjs.github.io/vis-network/docs/network/options.html). This is where you can extensively customize the appearance, layout, physics, interaction, etc.
* `show_browser` (bool, optional): If `True` (default), automatically opens the generated HTML file in the browser.
* `notebook` (bool, optional): If `True`, returns an `IPython.display.HTML` object for rendering directly in Jupyter Notebooks/Lab, instead of writing to a file. Defaults to `False`.
* `override_node_properties` (dict, optional): A dictionary of properties to apply to *all* nodes, overriding any individual node attributes or defaults.
* `override_edge_properties` (dict, optional): A dictionary of properties to apply to *all* edges.
* `graph_width` (str, optional): CSS value for the graph container's width (e.g., `"800px"`, `"100%"`). Defaults to `"100%"`.
* `graph_height` (str, optional): CSS value for the graph container's height (e.g., `"600px"`, `"90vh"`). Defaults to `"95vh"` (or as per the template).

## Customizing with Node/Edge Attributes

You can control many visual aspects by setting attributes directly on your NetworkX nodes and edges. `nx-vis-visualizer` will attempt to map these to corresponding vis.js properties.

**Common Node Attributes:**

* `label` (str): Text displayed on or near the node.
* `title` (str): HTML content for the tooltip on hover.
* `color` (str or dict): Node color (e.g., `"red"`, `"#FF0000"`, or `{"background":"pink", "border":"red"}`).
* `shape` (str): Node shape (e.g., `"dot"`, `"ellipse"`, `"box"`, `"star"`, `"image"`).
* `size` (int): Node size.
* `group` (str or int): Assigns node to a group for collective styling via `vis_options['groups']`.
* `font` (dict): Font properties (e.g., `{"size": 10, "color": "blue"}`).
* `x`, `y` (int): Fixed coordinates (if physics is disabled or for initial positions).
* `fixed` (dict or bool): e.g. `{"x":True, "y":True}` to fix node position.

**Common Edge Attributes:**

* `label` (str): Text displayed on the edge.
* `title` (str): HTML content for the tooltip.
* `color` (str or dict): Edge color.
* `width` (int): Edge thickness.
* `arrows` (str or dict): Arrow configuration (e.g., `"to"`, `{"to": {"enabled": True}}`).
* `dashes` (bool or list): For dashed lines (e.g., `True` or `[5, 5]`).
* `smooth` (dict): Edge smoothing options.
* `value` (int or float): Can be used for scaling edge width or by physics.

## Next Steps

* Dive into the **[Examples](./examples/basic.md)** to see these features in action.
* Consult the **[vis.js Network documentation](https://visjs.github.io/vis-network/docs/network/)** for a complete list of all available customization options you can pass via the `vis_options` parameter.
