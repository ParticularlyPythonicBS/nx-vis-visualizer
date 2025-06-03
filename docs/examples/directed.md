# Directed Graph Examples

This page demonstrates examples of generating interactive directed graphs.

## Example 1: A Simple Directed Graph with Arrows

This example shows a basic directed graph where edge directions are indicated by arrows.

<div class="interactive-graph-wrapper" style="margin-bottom: 1.5em; padding: 1em; border: 1px solid #e0e0e0; border-radius: 4px; background-color: #f9f9f9;">
    <h4 style="margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em;">Simple Directed Graph</h4>
    <iframe src="/nx-vis-visualizer/assets/generated_graphs/simple_directed_example.html"
            width="100%"
            height="500px"
            style="border: 1px solid #ccc; max-width: 100%; display: block;"
            sandbox="allow-scripts allow-same-origin allow-popups allow-forms">
        Your browser does not support iframes. Please update your browser.
    </iframe>
</div>

The Python code to generate the graph data:
```python
import networkx as nx

DG = nx.DiGraph()
DG.add_edges_from([
    (1, 2, {'label': 'Rel A'}),
    (1, 3, {'label': 'Rel B'}),
    (2, 4, {'label': 'Rel C'}),
    (3, 4, {'label': 'Rel D'}),
    (4, 1, {'label': 'Rel E (Cycle)'}) # Creates a cycle
])

# Add some node properties
for i in DG.nodes():
    DG.nodes[i]['label'] = f'DNode {i}'
    DG.nodes[i]['title'] = f'This is directed node {i}'
    if i == 1:
        DG.nodes[i]['color'] = 'lightcoral'
        DG.nodes[i]['shape'] = 'star'
    if i == 4:
        DG.nodes[i]['color'] = 'lightgreen'
```

The `vis_options` used (as a Python dictionary in the generation script):
```json
{
    "edges": {
        "arrows": {
            "to": {"enabled": True, "scaleFactor": 1, "type": "arrow"}
        },
        "font": {"align": "middle", "size": 10},
        "smooth": {"enabled": True, "type": "curvedCW", "roundness": 0.2}
    },
    "nodes": {
        "font": {"size": 14}
    },
    "physics": {"enabled": True},
    "layout": {
        "hierarchical": False,
        "randomSeed": 789
    },
    "interaction": {"navigationButtons": True, "hover": True}
}
```

---

## Example 2: Course Prerequisites (Hierarchical Layout)

This example demonstrates a directed graph representing course prerequisites, using a hierarchical layout to show dependencies.

<div class="interactive-graph-wrapper" style="margin-bottom: 1.5em; padding: 1em; border: 1px solid #e0e0e0; border-radius: 4px; background-color: #f9f9f9;">
    <h4 style="margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em;">Course Prerequisites</h4>
    <iframe src="/nx-vis-visualizer/assets/generated_graphs/course_prerequisites_example.html"
            width="100%"
            height="600px"
            style="border: 1px solid #ccc; max-width: 100%; display: block;"
            sandbox="allow-scripts allow-same-origin allow-popups allow-forms">
        Your browser does not support iframes. Please update your browser.
    </iframe>
</div>

The Python code to generate the graph data:
```python
import networkx as nx

DG = nx.DiGraph()
courses = {
    "CS101": {"label": "Intro to CS", "level": 1, "title": "Fundamentals of Computer Science"},
    "CS102": {"label": "Data Structures", "level": 2, "title": "Basic Data Structures and Algorithms"},
    "MA101": {"label": "Calculus I", "level": 1, "title": "Differential Calculus"},
    "CS201": {"label": "Algorithms", "level": 3, "title": "Advanced Algorithm Design"},
    "CS202": {"label": "Operating Systems", "level": 3, "title": "Principles of Operating Systems"},
    "CS301": {"label": "Compilers", "level": 4, "title": "Compiler Construction"}
}
for course_id, attrs in courses.items():
    DG.add_node(course_id, **attrs)

# Edges: (prerequisite, course)
DG.add_edges_from([
    ("CS101", "CS102"),
    ("MA101", "CS102"),
    ("CS102", "CS201"),
    ("CS102", "CS202"),
    ("CS201", "CS301"),
    ("CS202", "CS301")
])
```

The `vis_options` used (as a Python dictionary in the generation script):
```json
{
    "nodes": {
        "shape": "box",
        "font": {"size": 12, "face": "Arial"},
        "margin": 10
    },
    "edges": {
        "arrows": {"to": {"enabled": True, "scaleFactor": 0.8, "type": "arrow"}},
        "smooth": {"enabled": True, "type": "cubicBezier", "forceDirection": "vertical", "roundness": 0.4}
    },
    "layout": {
        "hierarchical": {
            "enabled": True,
            "direction": "UD",
            "sortMethod": "directed",
            "levelSeparation": 150,
            "nodeSpacing": 120
        }
    },
    "physics": {"enabled": False},
    "interaction": {"hover": True, "dragNodes": False, "zoomView": True, "dragView": True}
}
```
