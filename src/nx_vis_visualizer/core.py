import json
import logging
import os
import uuid
import webbrowser
from html import escape
from pathlib import Path  # Import Path
from typing import Any, TypeVar, cast

import networkx as nx

# Using a hardcoded name for clear identification in logs
logger = logging.getLogger("nx_vis_visualizer")

# Runtime compatible TypeVar for NetworkX graphs
GraphType = TypeVar("GraphType", nx.Graph, nx.DiGraph)  # type: ignore[type-arg]

JSONSerializable = dict[str, Any] | list[Any] | str | int | float | bool | None

IPythonHTMLClass = type[Any] | None
IPythonHTMLInstance = Any

iPythonHtmlClassGlobal: IPythonHTMLClass  # Declare with the alias

try:
    # Import the actual class
    from IPython.display import HTML as _IPython_HTML_Concrete_Class

    # Store the class itself in our typed variable
    iPythonHtmlClassGlobal = _IPython_HTML_Concrete_Class
except ImportError:
    iPythonHtmlClassGlobal = None


def _load_template() -> str:
    """Loads the HTML template from the adjacent file."""
    try:
        # Get the path to the template file relative to this script
        template_path = Path(__file__).parent / "template.html"
        with open(template_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(
            "Could not find template.html. It should be in the same directory as core.py."
        )
        return "<html><body>Template file not found.</body></html>"


# Load the template once when the module is imported
HTML_TEMPLATE = _load_template()


DEFAULT_VIS_OPTIONS = {
    "autoResize": True,
    "nodes": {
        "shape": "dot",
        "size": 16,
        "font": {"size": 14, "color": "#333"},
        "borderWidth": 2,
    },
    "edges": {
        "width": 2,
        "smooth": {"type": "continuous", "roundness": 0.5},
        "arrows": {"to": {"enabled": False, "scaleFactor": 1}},
    },
    "physics": {
        "enabled": True,
        "barnesHut": {
            "gravitationalConstant": -8000,
            "springConstant": 0.04,
            "springLength": 150,
            "damping": 0.09,
            "avoidOverlap": 0.1,
        },
        "solver": "barnesHut",
        "stabilization": {"iterations": 1000, "fit": True},
    },
    "interaction": {
        "hover": True,
        "dragNodes": True,
        "dragView": True,
        "zoomView": True,
        "tooltipDelay": 200,
        "navigationButtons": False,
        # CHANGE: Configure keyboard to not bind globally
        "keyboard": {
            "enabled": True,
            "bindToWindow": False,
        },
    },
    "layout": {"randomSeed": None, "improvedLayout": True},
}


_DEBUG_MERGE_CALL_COUNT = 0


def _deep_merge_dicts(
    source: dict[str, Any], destination: dict[str, Any]
) -> dict[str, Any]:
    global _DEBUG_MERGE_CALL_COUNT
    _DEBUG_MERGE_CALL_COUNT += 1
    call_id = _DEBUG_MERGE_CALL_COUNT

    for key, source_value in source.items():
        dest_value = destination.get(key)

        if isinstance(source_value, dict) and isinstance(dest_value, dict):
            _deep_merge_dicts(source_value, dest_value)
        else:
            try:
                destination[key] = source_value
            except TypeError as e:
                print(
                    f"MERGE CALL {call_id}: TypeError during assignment for key='{key}'"
                )
                print(f"  destination type: {type(destination)}")
                print(f"  destination value: {destination!r}")
                print(f"  key: {key!r}")
                print(f"  source_value type: {type(source_value)}")
                print(f"  source_value: {source_value!r}")
                raise e
    return destination


def nx_to_vis(
    nx_graph: GraphType,
    output_filename: str = "vis_network.html",
    html_title: str = "NetworkX to vis.js Graph",
    vis_options: dict[str, Any] | None = None,
    show_browser: bool = True,
    notebook: bool = False,
    override_node_properties: dict[str, Any] | None = None,
    override_edge_properties: dict[str, Any] | None = None,
    graph_width: str = "100%",
    graph_height: str = "95vh",
    cdn_js: str = "https://unpkg.com/vis-network/standalone/umd/vis-network.min.js",
    cdn_css: str = "https://unpkg.com/vis-network/styles/vis-network.min.css",
    verbosity: int = 0,
) -> str | IPythonHTMLInstance | None:
    """
    Converts a NetworkX graph to an interactive HTML file using vis.js.

    Args:
        nx_graph: The NetworkX graph object (Graph or DiGraph).
        output_filename: Name of the HTML file to generate.
        html_title: The title for the HTML page.
        vis_options: A dictionary of vis.js options to customize the visualization.
                     These will be deep-merged with default options.
        show_browser: If True, automatically opens the generated HTML file in a web browser.
        notebook: If True, returns HTML content suitable for embedding in Jupyter Notebooks.
                  `show_browser` is typically False when `notebook` is True.
        override_node_properties: A dictionary of properties to apply to all nodes,
                                  overriding existing attributes.
        override_edge_properties: A dictionary of properties to apply to all edges,
                                  overriding existing attributes.
        graph_width: CSS width for the graph container (default: "100%").
        graph_height: CSS height for the graph container (default: "95vh").
        cdn_js: URL for the vis.js Network JavaScript library.
        cdn_css: URL for the vis.js Network CSS.
        verbosity: Controls the amount of logging output.
                   0: Errors/Warnings only.
                   1: Info messages (e.g., file saved).
                   2: Debug messages (more detailed, for library development).

    Returns:
        If `notebook` is True, returns the HTML string or an IPython.display.HTML object.
        Otherwise, returns the absolute path to the generated HTML file, or None on error.
    """
    nodes_data: list[dict[str, Any]] = []
    node_ids_map: dict[Any, str] = {}

    for _, (node_obj, attrs) in enumerate(nx_graph.nodes(data=True)):
        node_id_str = str(node_obj)
        node_ids_map[node_obj] = node_id_str
        node_entry: dict[str, Any] = {"id": node_id_str}
        if "label" not in attrs:  # Default label to node ID if not specified
            node_entry["label"] = node_id_str
        for key, value in attrs.items():
            if isinstance(value, list | dict):  # Check if list or dict
                try:
                    json.dumps(value)  # Check if JSON serializable
                    node_entry[key] = value
                except (TypeError, OverflowError):
                    if verbosity >= 2:
                        logger.debug(
                            f"Node {node_id_str} attribute '{key}' not JSON serializable, converting to string: {value}"
                        )
                    node_entry[key] = str(value)
            else:
                node_entry[key] = value
        if override_node_properties:
            node_entry.update(override_node_properties)
        nodes_data.append(node_entry)

    edges_data: list[dict[str, Any]] = []
    for u_obj, v_obj, attrs in nx_graph.edges(data=True):
        edge_entry: dict[str, Any] = {
            "from": node_ids_map[u_obj],
            "to": node_ids_map[v_obj],
        }
        if "id" not in attrs and nx_graph.is_multigraph():
            edge_entry["id"] = str(uuid.uuid4())

        for key, value in attrs.items():
            if isinstance(value, list | dict):
                try:
                    json.dumps(value)
                    edge_entry[key] = value
                except (TypeError, OverflowError):
                    if verbosity >= 2:
                        logger.debug(
                            f"Edge ({u_obj}-{v_obj}) attribute '{key}' not JSON serializable, converting to string: {value}"
                        )
                    edge_entry[key] = str(value)
            else:
                edge_entry[key] = value
        if override_edge_properties:
            edge_entry.update(override_edge_properties)
        edges_data.append(edge_entry)

    current_options: dict[str, Any] = json.loads(
        json.dumps(DEFAULT_VIS_OPTIONS)
    )

    if isinstance(nx_graph, nx.DiGraph):
        current_options.setdefault("edges", {}).setdefault(
            "arrows", {}
        ).setdefault("to", {})["enabled"] = True
        if verbosity >= 2:
            logger.debug("DiGraph: Defaulted arrows.to.enabled to True.")

    if vis_options:
        if verbosity >= 2:
            logger.debug(f"Merging user vis_options: {vis_options}")
        _deep_merge_dicts(vis_options, current_options)
        if verbosity >= 2:
            logger.debug(f"Options after user merge: {current_options}")

    hierarchical_options = current_options.get("layout", {}).get("hierarchical")
    hierarchical_enabled = False
    if isinstance(hierarchical_options, dict):
        hierarchical_enabled = hierarchical_options.get("enabled", False)
    elif isinstance(hierarchical_options, bool):
        hierarchical_enabled = hierarchical_options

    if hierarchical_enabled:
        current_options.setdefault("physics", {})["enabled"] = False
        if verbosity >= 2:
            logger.debug("Hierarchical layout enabled, physics disabled.")

    if verbosity >= 2:
        if isinstance(current_options.get("physics"), dict):
            logger.debug(
                f"Final physics.enabled: {current_options['physics'].get('enabled')}"
            )
        else:
            logger.debug(
                f"Final physics options is not a dict: {current_options.get('physics')}"
            )
        if isinstance(nx_graph, nx.DiGraph) and isinstance(
            current_options.get("edges", {}).get("arrows", {}).get("to"), dict
        ):
            logger.debug(
                f"Final arrows.to.enabled for DiGraph: {current_options['edges']['arrows']['to'].get('enabled')}"
            )

    div_id_suffix: str = uuid.uuid4().hex[:8]
    nodes_json_str: str = json.dumps(nodes_data)
    edges_json_str: str = json.dumps(edges_data)
    options_json_str: str = json.dumps(current_options)
    escaped_html_page_title: str = escape(html_title)

    html_content: str = HTML_TEMPLATE.format(
        html_page_title=escaped_html_page_title,
        nodes_json_str=nodes_json_str,
        edges_json_str=edges_json_str,
        options_json_str=options_json_str,
        div_id_suffix=div_id_suffix,
        width=graph_width,
        height=graph_height,
        cdn_js_url=cdn_js,
        cdn_css_url=cdn_css,
    )

    if notebook:
        if iPythonHtmlClassGlobal is not None:
            html_instance = iPythonHtmlClassGlobal(html_content)
            return cast(IPythonHTMLInstance, html_instance)
        else:
            if verbosity >= 1:
                logger.info(
                    "IPython is not available. Returning raw HTML string for notebook mode."
                )
            return html_content

    abs_path: str | None = None
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        abs_path = os.path.abspath(output_filename)
        if verbosity >= 1:
            logger.info(f"Generated graph HTML at: {abs_path}")
    except OSError as e:
        logger.error(f"Error writing file {output_filename}: {e}")
        return None

    if show_browser and abs_path:
        try:
            webbrowser.open("file://" + abs_path)
        except Exception as e:
            logger.warning(f"Could not open browser: {e}")

    return abs_path
