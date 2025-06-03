# Basic Graph Examples

This page demonstrates some basic examples of generating interactive graphs.

## Example 1: A Simple Cycle Graph

Let's create a 5-node cycle graph and add some basic styling through node attributes and `vis_options`.

<div class="interactive-graph-wrapper" style="margin-bottom: 1.5em; padding: 1em; border: 1px solid #e0e0e0; border-radius: 4px; background-color: #f9f9f9;">
    <h4 style="margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em;">Interactive 5-Cycle Graph</h4>
    <iframe src="/nx-vis-visualizer/assets/generated_graphs/cycle_graph_example.html"
            width="100%"
            height="450px"
            style="border: 1px solid #ccc; max-width: 100%; display: block;"
            sandbox="allow-scripts allow-same-origin allow-popups allow-forms">
        Your browser does not support iframes. Please update your browser.
    </iframe>
</div>

The Python code to generate the graph data:
```python
import networkx as nx

G = nx.cycle_graph(5)
for i, node_id in enumerate(G.nodes()):
    G.nodes[node_id]['label'] = f'N{i+1}'
    G.nodes[node_id]['title'] = f'Tooltip for Node N{i+1}'
    G.nodes[node_id]['group'] = i % 2
    if i == 0:
        G.nodes[node_id]['color'] = 'skyblue'
        G.nodes[node_id]['size'] = 25
G.edges[0,1]['label'] = "Link 0-1"
G.edges[0,1]['color'] = "green"
G.edges[0,1]['width'] = 3
```

The `vis_options` used (as a Python dictionary in the generation script):
```json
{
    "nodes": {"font": {"size": 14}},
    "edges": {"smooth": {"enabled": True, "type": "dynamic"}},
    "groups": {
        "0": {"shape": "dot", "color": {"background": "lightcoral", "border": "red"}},
        "1": {"shape": "square", "color": {"background": "lightgreen", "border": "green"}}
    },
    "interaction": {"hover": True, "navigationButtons": True},
    "physics": {"enabled": True, "solver": "barnesHut"},
    "layout": {
        "randomSeed": 12345
    }
}
```

---

## Example 2: Karate Club Graph

<div class="interactive-graph-wrapper" style="margin-bottom: 1.5em; padding: 1em; border: 1px solid #e0e0e0; border-radius: 4px; background-color: #f9f9f9;">
    <h4 style="margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em;">Zachary's Karate Club</h4>
    <iframe src="/nx-vis-visualizer/assets/generated_graphs/karate_club_example.html"
            width="100%"
            height="550px"
            style="border: 1px solid #ccc; max-width: 100%; display: block;"
            sandbox="allow-scripts allow-same-origin allow-popups allow-forms">
        Your browser does not support iframes. Please update your browser.
    </iframe>
</div>

The Python code to generate the graph data:
```python
import networkx as nx

G = nx.karate_club_graph()
for node_id, data in G.nodes(data=True):
    data['label'] = str(node_id)
    data['title'] = f"Member {node_id}\nClub: {data['club']}"
    data['group'] = data['club']
    data['value'] = G.degree(node_id)
```

The `vis_options` used (as a Python dictionary in the generation script):
```json
{
    "nodes": {
        "scaling": {
            "min": 10,
            "max": 30,
            "label": {"enabled": False}
        },
        "font": {"size": 12}
    },
    "edges": {"width": 0.5, "color": "silver", "smooth": False},
    "groups": {
        "Mr. Hi": {"color": {"background":"orange", "border":"darkorange"}, "shape": "dot"},
        "Officer": {"color": {"background":"purple", "border":"indigo"}, "shape": "ellipse"}
    },
    "physics": {
        "stabilization": {"iterations": 1200},
        "barnesHut": {"gravitationalConstant": -10000, "springLength": 120, "avoidOverlap": 0.1}
    },
    "layout": {"randomSeed": 42},
    "interaction": {"tooltipDelay": 200, "hover": True}
}
```
