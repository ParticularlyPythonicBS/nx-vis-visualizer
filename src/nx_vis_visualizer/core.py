# src/nx_vis_visualizer/core.py

import json
import os
import uuid
import webbrowser
from html import escape  # For safely embedding JSON into script tags
from typing import Any, TypeVar, cast

import networkx as nx

# Runtime compatible TypeVar for NetworkX graphs
GraphType = TypeVar("GraphType", nx.Graph, nx.DiGraph)  # type: ignore[type-arg]

# For JSON serializable data (Python 3.9+ syntax for Union with built-ins)
JSONSerializable = dict[str, Any] | list[Any] | str | int | float | bool | None

# --- Corrected IPython HTML Typing using built-in `type` ---
# This will store the *type* of IPython.display.HTML if available, otherwise None.
IPythonHTMLClass = (
    type[Any] | None
)  # Alias for the class type (type[SomeClass]) or None
IPythonHTMLInstance = (
    Any  # Alias for an instance of HTML (or str if not available)
)

iPythonHtmlClassGlobal: IPythonHTMLClass  # Declare with the alias

try:
    # Import the actual class
    from IPython.display import HTML as _IPython_HTML_Concrete_Class

    # Store the class itself in our typed variable
    iPythonHtmlClassGlobal = _IPython_HTML_Concrete_Class
except ImportError:
    iPythonHtmlClassGlobal = None


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_page_title}</title>
    <script type="text/javascript" src="{cdn_js_url}"></script>
    <link href="{cdn_css_url}" rel="stylesheet" type="text/css" />
    <style type="text/css">
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            background-color: #f4f6f8; /* Light background for the page */
            display: flex;
            flex-direction: column;
            overflow: hidden; /* Prevent body scrollbars */
        }}

        .config-panel-wrapper {{
            width: 100%;
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            z-index: 10; /* Ensure it's above the graph if any overlap issues */
            flex-shrink: 0; /* Prevent panel from shrinking */
        }}

        .config-panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 15px;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;
            background-color: #f9f9f9;
        }}

        .config-panel-header h3 {{
            margin: 0;
            font-size: 16px;
            font-weight: 600;
            color: #333;
        }}

        .config-toggle-btn {{
            background: none;
            border: none;
            font-size: 18px;
            cursor: pointer;
            padding: 5px;
            color: #555;
        }}
        .config-toggle-btn::after {{
            content: '\\25BC'; /* Down arrow ▼ */
            display: inline-block;
            transition: transform 0.2s ease-in-out;
        }}
        .collapsed .config-toggle-btn::after {{
            transform: rotate(-90deg); /* Right arrow for collapsed state */
        }}

        #config-container-content-{div_id_suffix} {{
            max-height: 40vh; /* Default expanded max height */
            overflow-y: auto;
            padding: 15px;
            box-sizing: border-box;
            background-color: #ffffff;
            transition: max-height 0.3s ease-in-out, padding 0.3s ease-in-out;
        }}

        .collapsed #config-container-content-{div_id_suffix} {{
            max-height: 0;
            padding-top: 0;
            padding-bottom: 0;
            overflow: hidden;
            border-bottom: none; /* Hide border when collapsed */
        }}

        #mynetwork-{div_id_suffix} {{
            width: 100%;
            flex-grow: 1; /* Graph takes remaining vertical space */
            min-height: 0; /* Important for flex children to shrink */
            /* border-top: 1px solid #e0e0e0; */ /* Optional: if config panel is directly above */
            background-color: #ffffff; /* Graph background */
        }}

        /* Basic styling for vis.js config elements to blend better */
        div.vis-configuration-wrapper {{
            padding: 0; /* Remove default padding if vis.js adds it */
        }}
        div.vis-configuration-wrapper table {{
            width: 100%;
        }}
        div.vis-configuration-wrapper table tr td:first-child {{
            width: 30%; /* Adjust label width */
            font-size: 13px;
        }}
        div.vis-configuration-wrapper input[type=text],
        div.vis-configuration-wrapper select {{
            width: 95%;
            padding: 6px;
            margin: 2px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 13px;
        }}
        div.vis-configuration-wrapper input[type=range] {{
            width: 60%; /* Adjust slider width */
        }}
        div.vis-configuration-wrapper .vis-label {{
             font-size: 13px;
             color: #333;
        }}

    </style>
</head>
<body>
    <div class="config-panel-wrapper" id="config-panel-wrapper-{div_id_suffix}">
        <div class="config-panel-header" id="config-panel-header-{div_id_suffix}" role="button" tabindex="0" aria-expanded="true" aria-controls="config-container-content-{div_id_suffix}">
            <h3>Configuration</h3>
            <button class="config-toggle-btn" id="config-toggle-btn-{div_id_suffix}" aria-label="Toggle configuration panel"></button>
        </div>
        <div id="config-container-content-{div_id_suffix}">
            <!-- Vis.js configuration UI will be injected here -->
        </div>
    </div>

    <div id="mynetwork-{div_id_suffix}"></div>

    <script type="text/javascript">
        (function() {{
            var nodesArray = {nodes_json_str};
            var edgesArray = {edges_json_str};
            var optionsObject = {options_json_str};

            var configWrapper = document.getElementById('config-panel-wrapper-{div_id_suffix}');
            var configHeader = document.getElementById('config-panel-header-{div_id_suffix}');
            var configContent = document.getElementById('config-container-content-{div_id_suffix}');
            var toggleButton = document.getElementById('config-toggle-btn-{div_id_suffix}'); // Also target button for ARIA

            if (optionsObject.configure && optionsObject.configure.enabled) {{
                if (!optionsObject.configure.container) {{ // Only set if user hasn't provided one
                    optionsObject.configure.container = configContent;
                }}
                // optionsObject.configure.showButton = false; // User should set this in Python options

                configHeader.addEventListener('click', function() {{
                    configWrapper.classList.toggle('collapsed');
                    var isExpanded = !configWrapper.classList.contains('collapsed');
                    configHeader.setAttribute('aria-expanded', isExpanded);
                    toggleButton.setAttribute('aria-expanded', isExpanded); // Keep button ARIA in sync
                }});
                configHeader.addEventListener('keydown', function(event) {{
                    if (event.key === 'Enter' || event.key === ' ') {{
                        configWrapper.classList.toggle('collapsed');
                        var isExpanded = !configWrapper.classList.contains('collapsed');
                        configHeader.setAttribute('aria-expanded', isExpanded);
                        toggleButton.setAttribute('aria-expanded', isExpanded);
                        event.preventDefault();
                    }}
                }});

                // Optional: Start collapsed by default
                // configWrapper.classList.add('collapsed');
                // configHeader.setAttribute('aria-expanded', 'false');
                // toggleButton.setAttribute('aria-expanded', 'false');

            }} else {{
                // If configure is not enabled, hide the whole panel wrapper
                if (configWrapper) {{
                    configWrapper.style.display = 'none';
                }}
            }}

            var nodes = new vis.DataSet(nodesArray);
            var edges = new vis.DataSet(edgesArray);
            var graphContainer = document.getElementById('mynetwork-{div_id_suffix}');
            var data = {{ nodes: nodes, edges: edges }};
            var network = new vis.Network(graphContainer, data, optionsObject);

            network.on("click", function (params) {{
                console.log('Click event:', params);
            }});
        }})();
    </script>
</body>
</html>
"""

DEFAULT_VIS_OPTIONS = {
    "autoResize": True,
    # height and width will be set by parameters or default to 100% in template
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
        "navigationButtons": False,  # Often better to control via custom UI
        "keyboard": True,
    },
    "layout": {"randomSeed": None, "improvedLayout": True},
    # Example of how to define groups (can be overridden by node attributes)
    # "groups": {
    #     "myGroup1": {"color": {"background": "red"}, "shape": "star"},
    #     "myGroup2": {"color": {"background": "blue"}, "borderWidth": 3}
    # }
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

        # print(f"MERGE CALL {call_id}: key='{key}', type(source_value)={type(source_value)}, type(dest_value)={type(dest_value)}")

        if isinstance(source_value, dict) and isinstance(dest_value, dict):
            # print(f"MERGE CALL {call_id}: Recursing for key='{key}'")
            _deep_merge_dicts(source_value, dest_value)
        else:
            # print(f"MERGE CALL {call_id}: Assigning for key='{key}'. Destination type before assignment: {type(destination)}")
            try:
                destination[key] = source_value
            except TypeError as e:
                print(
                    f"MERGE CALL {call_id}: TypeError during assignment for key='{key}'"
                )
                print(f"  destination type: {type(destination)}")
                print(
                    f"  destination value: {destination!r}"
                )  # repr for more detail
                print(f"  key: {key!r}")
                print(f"  source_value type: {type(source_value)}")
                print(f"  source_value: {source_value!r}")
                raise e  # Re-raise the original error
    return destination


def nx_to_vis(
    nx_graph: GraphType,
    output_filename: str = "vis_network.html",
    html_title: str = "NetworkX to vis.js Graph",  # This is for the <title> tag
    vis_options: dict[str, Any] | None = None,
    show_browser: bool = True,
    notebook: bool = False,
    override_node_properties: dict[str, Any] | None = None,
    override_edge_properties: dict[str, Any] | None = None,
    graph_width: str = "100%",
    graph_height: str = "95vh",
    cdn_js: str = "https://unpkg.com/vis-network/standalone/umd/vis-network.min.js",
    cdn_css: str = "https://unpkg.com/vis-network/styles/vis-network.min.css",
) -> str | IPythonHTMLInstance | None:
    nodes_data: list[dict[str, Any]] = []
    node_ids_map: dict[Any, str] = {}

    for _, (node_obj, attrs) in enumerate(nx_graph.nodes(data=True)):
        node_id_str = str(node_obj)
        node_ids_map[node_obj] = node_id_str
        node_entry: dict[str, Any] = {"id": node_id_str}
        if "label" not in attrs:
            node_entry["label"] = node_id_str
        for key, value in attrs.items():
            if isinstance(value, list | dict):
                try:
                    json.dumps(value)
                    node_entry[key] = value
                except (TypeError, OverflowError):
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
        for key, value in attrs.items():
            if isinstance(value, list | dict):
                try:
                    json.dumps(value)
                    edge_entry[key] = value
                except (TypeError, OverflowError):
                    edge_entry[key] = str(value)
            else:
                edge_entry[key] = value
        if override_edge_properties:
            edge_entry.update(override_edge_properties)
        edges_data.append(edge_entry)

    current_options: dict[str, Any] = json.loads(
        json.dumps(DEFAULT_VIS_OPTIONS)
    )

    # --- START DEBUG PRINTS ---
    if isinstance(nx_graph, nx.DiGraph):
        print(
            f"DEBUG DiGraph: Initial arrows.to.enabled from DEFAULT: {current_options.get('edges', {}).get('arrows', {}).get('to', {}).get('enabled')}"
        )
    # --- END DEBUG PRINTS ---

    if isinstance(nx_graph, nx.DiGraph):
        current_options.setdefault("edges", {}).setdefault(
            "arrows", {}
        ).setdefault("to", {})["enabled"] = True
        # --- START DEBUG PRINTS ---
        print(
            f"DEBUG DiGraph: arrows.to.enabled AFTER DiGraph specific set: {current_options.get('edges', {}).get('arrows', {}).get('to', {}).get('enabled')}"
        )
        # --- END DEBUG PRINTS ---

    if vis_options:
        _deep_merge_dicts(vis_options, current_options)
        # --- START DEBUG PRINTS ---
        if isinstance(nx_graph, nx.DiGraph):
            print(
                f"DEBUG DiGraph: arrows.to.enabled AFTER vis_options merge: {current_options.get('edges', {}).get('arrows', {}).get('to', {}).get('enabled')}"
            )
        # --- END DEBUG PRINTS ---

    hierarchical_options = current_options.get("layout", {}).get("hierarchical")
    hierarchical_enabled = False
    if isinstance(hierarchical_options, dict):
        hierarchical_enabled = hierarchical_options.get("enabled", False)
    elif isinstance(
        hierarchical_options, bool
    ):  # Handle if 'hierarchical' itself is a boolean
        hierarchical_enabled = hierarchical_options

    if hierarchical_enabled:
        current_options.setdefault("physics", {})["enabled"] = False
        # --- START DEBUG PRINTS ---
        if isinstance(nx_graph, nx.DiGraph):
            print(
                f"DEBUG DiGraph: arrows.to.enabled AFTER hierarchical check: {current_options.get('edges', {}).get('arrows', {}).get('to', {}).get('enabled')}"
            )
        # --- END DEBUG PRINTS ---

    # --- START DEBUG PRINTS ---
    # Final check right before serialization for DiGraphs
    if isinstance(nx_graph, nx.DiGraph):
        final_arrow_to_enabled = (
            current_options.get("edges", {})
            .get("arrows", {})
            .get("to", {})
            .get("enabled")
        )
        print(
            f"DEBUG DiGraph: FINAL arrows.to.enabled before JSON dump: {final_arrow_to_enabled}"
        )
    # --- END DEBUG PRINTS ---

    if isinstance(current_options.get("physics"), dict):
        print(
            f"DEBUG: current_options['physics']['enabled'] is {current_options['physics'].get('enabled')}"
        )
    else:
        print(
            f"DEBUG: current_options['physics'] is NOT a dict. It is: {current_options.get('physics')}"
        )
        print(
            f"DEBUG: Full current_options['physics']: {current_options.get('physics')}"
        )

    div_id_suffix: str = uuid.uuid4().hex[:8]

    # Generate JSON strings *without* HTML escaping for direct JS embedding
    nodes_json_str: str = json.dumps(nodes_data)
    edges_json_str: str = json.dumps(edges_data)
    options_json_str: str = json.dumps(current_options)

    # The HTML page title *should* be escaped
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
            # iPythonHtmlClassGlobal is the actual IPython.display.HTML class
            # We are calling the constructor of the class.
            # If types-ipython stubs are good, MyPy should understand this.
            # If it still complains about "Call to untyped function",
            # it means the stubs aren't perfect for the constructor.
            html_instance = iPythonHtmlClassGlobal(html_content)
            return cast(
                IPythonHTMLInstance, html_instance
            )  # Cast to expected instance type
        else:
            print("IPython is not available. Returning raw HTML string.")
            return html_content

    abs_path: str | None = None
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        abs_path = os.path.abspath(output_filename)
        print(f"Generated graph HTML at: {abs_path}")
    except OSError as e:
        print(f"Error writing file {output_filename}: {e}")
        return None

    if show_browser and abs_path:
        try:
            webbrowser.open("file://" + abs_path)
        except Exception as e:
            print(f"Could not open browser: {e}")

    return abs_path
