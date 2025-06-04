# tests/test_core.py
import json
import os
from pathlib import Path
from typing import Any, cast

import networkx as nx
import pytest

from nx_vis_visualizer import DEFAULT_VIS_OPTIONS, nx_to_vis


@pytest.fixture  # type: ignore[misc]
def simple_graph() -> nx.Graph:  # type: ignore[type-arg]
    G: nx.Graph = nx.Graph()  # type: ignore[type-arg]
    G.add_edges_from([(1, 2, {"weight": 3}), (2, 3, {"label": "connects"})])
    G.nodes[1]["label"] = "Node A"
    G.nodes[1]["color"] = "red"
    return G


@pytest.fixture  # type: ignore[misc]
def simple_digraph() -> nx.DiGraph:  # type: ignore[type-arg]
    G: nx.DiGraph = nx.DiGraph()  # type: ignore[type-arg]
    G.add_edges_from([(1, 2), (2, 3)])
    return G


IPythonHTMLOrStrClass = type[Any]
VisOutputType = str | Any | None


def test_nx_to_vis_creates_file(
    simple_graph: nx.Graph,  # type: ignore[type-arg]
    tmp_path: Path,
) -> None:
    """Test that an HTML file is created."""
    output_file = tmp_path / "test_graph.html"
    result_path = nx_to_vis(
        simple_graph, output_filename=str(output_file), show_browser=False
    )
    assert result_path is not None
    assert isinstance(result_path, str)
    assert os.path.exists(result_path)
    assert str(output_file) == result_path


def test_nx_to_vis_html_content(
    simple_graph: nx.Graph,  # type: ignore[type-arg]
    tmp_path: Path,
) -> None:
    """Test that the HTML content contains expected elements."""
    output_file = tmp_path / "test_content.html"
    nx_to_vis(
        simple_graph, output_filename=str(output_file), show_browser=False
    )

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    assert "<!DOCTYPE html>" in content
    assert "vis-network.min.js" in content  # Check for vis.js CDN
    assert (
        '"id": "1"' in content
    )  # Check for node data (assuming node 1 exists)
    assert '"label": "Node A"' in content
    assert '"from": "1", "to": "2"' in content  # Check for edge data


def test_nx_to_vis_notebook_output(simple_graph: nx.Graph) -> None:  # type: ignore[type-arg]
    ipython_concrete_class: IPythonHTMLOrStrClass
    has_ipython: bool
    try:
        from IPython.display import HTML as _IPython_HTML_Actual_Class

        ipython_concrete_class = _IPython_HTML_Actual_Class
        has_ipython = True
    except ImportError:
        has_ipython = False
        ipython_concrete_class = str  # satisfy mypy

    html_output: VisOutputType = nx_to_vis(
        simple_graph, notebook=True, show_browser=False
    )

    if has_ipython:  # if true, we know _IPython_HTML_Actual_Class was imported
        assert isinstance(html_output, ipython_concrete_class)
        assert html_output is not None
        assert "<!DOCTYPE html>" in html_output.data
    else:  # Should be a string instance
        assert isinstance(html_output, str)
        assert "<!DOCTYPE html>" in html_output


def test_digraph_enables_arrows_by_default(
    simple_digraph: nx.DiGraph,  # type: ignore[type-arg]
    tmp_path: Path,
) -> None:
    output_file = tmp_path / "test_digraph.html"
    nx_to_vis(
        simple_digraph, output_filename=str(output_file), show_browser=False
    )
    with open(output_file, encoding="utf-8") as f:
        content = f.read()
    # options_json_str = None
    for line in content.splitlines():
        if line.strip().startswith("var optionsObject ="):
            # Extract the JSON part: from the first '{' to the last '}' on that line, before the ';'
            start_index = line.find("{")
            end_index = line.rfind("}")
            if (
                start_index != -1
                and end_index != -1
                and end_index > start_index
            ):
                options_json_str = line[start_index : end_index + 1]
                break

    assert options_json_str is not None, (
        "Could not find optionsObject JSON in HTML"
    )

    try:
        parsed_options = json.loads(options_json_str)
    except json.JSONDecodeError as e:
        pytest.fail(
            f"Failed to parse optionsObject JSON: {e}\nJSON string was: {options_json_str}"
        )

    assert isinstance(parsed_options, dict), (
        "Parsed optionsObject is not a dictionary"
    )

    # Now check the specific option
    edges_options = parsed_options.get("edges", {})
    arrows_options = edges_options.get("arrows", {})
    to_options = arrows_options.get("to", {})

    assert to_options.get("enabled") is True, (
        f"arrows.to.enabled is not True. Options found: {json.dumps(parsed_options, indent=2)}"
    )


def test_custom_options_are_applied(
    simple_graph: nx.Graph,  # type: ignore[type-arg]
    tmp_path: Path,
) -> None:
    output_file = tmp_path / "test_custom_options.html"
    custom_opts = {
        "nodes": {"shape": "square"},
        "interaction": {"dragNodes": False},
    }
    nx_to_vis(
        simple_graph,
        output_filename=str(output_file),
        vis_options=custom_opts,
        show_browser=False,
    )
    with open(output_file, encoding="utf-8") as f:
        content = f.read()
    options_object = _extract_json_object(content, "optionsObject")
    assert options_object is not None
    assert isinstance(options_object, dict)
    assert options_object.get("nodes", {}).get("shape") == "square"
    assert options_object.get("interaction", {}).get("dragNodes") is False


@pytest.fixture  # type: ignore[misc]
def complex_graph_data() -> tuple[nx.Graph, dict[str, Any]]:  # type: ignore[type-arg]
    """
    Provides a more complex graph and some custom vis_options for it.
    """
    G: nx.Graph = nx.Graph(name="Complex Test Graph")  # type: ignore[type-arg]
    G.add_node(
        1,
        label="Alpha",
        title="Node A",
        color="red",
        shape="star",
        group=0,
        size=25,
    )
    G.add_node(
        "Beta",
        label="Beta Node",
        title="Node B",
        color="#00FF00",
        group=1,
        x=10,
        y=20,
    )
    G.add_node(
        3, label="Gamma", title="Node C", group=0
    )  # Will use default shape/color

    G.add_edge(
        1,
        "Beta",
        weight=5,
        label="Edge 1-B",
        color="blue",
        dashes=True,
        width=3,
    )
    G.add_edge(
        "Beta", 3, weight=2, label="Edge B-3", title="Connection Beta to Gamma"
    )
    G.add_edge(
        1, 3, weight=10, color={"color": "purple", "highlight": "magenta"}
    )

    custom_options: dict[str, Any] = {
        "nodes": {"font": {"size": 10, "color": "darkblue"}},
        "edges": {
            "smooth": {"enabled": False},
            "color": {"inherit": False, "color": "gray"},
        },
        "physics": {"enabled": False},
        "interaction": {"dragNodes": False, "zoomView": False},
        "layout": {"randomSeed": 123},
        "groups": {
            0: {"shape": "ellipse", "color": {"border": "black"}},
            1: {"shape": "box", "font": {"color": "white"}},
        },
    }
    return G, custom_options


ExtractResult = dict[str, Any] | list[Any] | None


def _extract_json_object(content: str, var_name: str) -> ExtractResult:
    """Helper to extract and parse a JSON object/array from HTML script content."""
    for line in content.splitlines():
        line_strip = line.strip()
        if line_strip.startswith(f"var {var_name} ="):
            assignment_part = line_strip[len(f"var {var_name} =") :].strip()
            if assignment_part.endswith(";"):
                json_candidate_str = assignment_part[:-1].strip()
            else:
                json_candidate_str = assignment_part
            if not json_candidate_str:
                pytest.fail(
                    f"Extracted empty JSON string for {var_name} from line: {line_strip}"
                )
            try:
                # json.loads can return various types, not just dict or list
                parsed_json: Any = json.loads(json_candidate_str)
                if not (
                    isinstance(parsed_json, dict)
                    or isinstance(parsed_json, list)
                ):
                    pytest.fail(
                        f"{var_name} JSON is not a dict or list: {type(parsed_json)}"
                    )
                return cast(dict[str, Any] | list[Any], parsed_json)
            except json.JSONDecodeError as e:
                pytest.fail(
                    f"Failed to parse {var_name} JSON: {e}\n"
                    f"Original line: {line_strip}\n"
                    f"Attempted to parse: {json_candidate_str}"
                )
    pytest.fail(
        f"Could not find JavaScript variable '{var_name}' in HTML content."
    )
    return None  # MyPy should not reach here, but just in case


def test_complex_graph_with_options(
    complex_graph_data: tuple[nx.Graph, dict[str, Any]],  # type: ignore[type-arg]
    tmp_path: Path,
) -> None:
    nx_graph, custom_vis_options = complex_graph_data
    output_file = tmp_path / "complex_graph.html"

    nx_to_vis(
        nx_graph,
        output_filename=str(output_file),
        vis_options=custom_vis_options,
        show_browser=False,
        html_title="Complex Graph Test Page",
    )

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    assert "<title>Complex Graph Test Page</title>" in content

    nodes_array_raw = _extract_json_object(content, "nodesArray")
    assert nodes_array_raw is not None and isinstance(nodes_array_raw, list)
    nodes_array: list[dict[str, Any]] = cast(
        list[dict[str, Any]], nodes_array_raw
    )  # Keep cast if needed after isinstance

    edges_array_raw = _extract_json_object(content, "edgesArray")
    assert edges_array_raw is not None and isinstance(edges_array_raw, list)
    edges_array: list[dict[str, Any]] = cast(
        list[dict[str, Any]], edges_array_raw
    )  # Keep cast

    options_object_raw = _extract_json_object(content, "optionsObject")
    assert options_object_raw is not None and isinstance(
        options_object_raw, dict
    )
    # If MyPy said previous cast was redundant, direct assignment is fine:
    options_object: dict[str, Any] = options_object_raw

    # --- Verify Nodes ---
    assert len(nodes_array) == nx_graph.number_of_nodes()

    # Find specific nodes (IDs are strings in vis.js)
    node1_data = next((n for n in nodes_array if n["id"] == "1"), None)
    node_beta_data = next((n for n in nodes_array if n["id"] == "Beta"), None)
    node3_data = next((n for n in nodes_array if n["id"] == "3"), None)

    assert node1_data is not None
    assert node1_data["label"] == "Alpha"
    assert node1_data["title"] == "Node A"
    assert node1_data["color"] == "red"
    assert node1_data["shape"] == "star"  # This comes from node attribute
    assert node1_data["group"] == 0
    assert node1_data["size"] == 25

    assert node_beta_data is not None
    assert node_beta_data["label"] == "Beta Node"
    assert node_beta_data["color"] == "#00FF00"
    assert node_beta_data["group"] == 1
    assert node_beta_data["x"] == 10  # Check for passed through x,y
    assert node_beta_data["y"] == 20

    assert node3_data is not None
    assert (
        node3_data["label"] == "Gamma"
    )  # Default label is node ID if not specified
    assert node3_data["group"] == 0

    # --- Verify Edges ---
    assert len(edges_array) == nx_graph.number_of_edges()
    edge_1_beta = next(
        (e for e in edges_array if e["from"] == "1" and e["to"] == "Beta"), None
    )
    edge_beta_3 = next(
        (e for e in edges_array if e["from"] == "Beta" and e["to"] == "3"), None
    )
    edge_1_3 = next(
        (e for e in edges_array if e["from"] == "1" and e["to"] == "3"), None
    )

    assert edge_1_beta is not None
    assert edge_1_beta["label"] == "Edge 1-B"
    assert edge_1_beta["color"] == "blue"
    assert edge_1_beta["dashes"] is True
    assert edge_1_beta["width"] == 3
    # 'weight' from networkx is often passed as 'value' to vis.js if not explicitly mapped
    # or used directly if vis.js options are configured for it.
    # Here, it should just be passed as 'weight'.
    assert edge_1_beta["weight"] == 5

    assert edge_beta_3 is not None
    assert edge_beta_3["label"] == "Edge B-3"
    assert edge_beta_3["title"] == "Connection Beta to Gamma"
    assert edge_beta_3["weight"] == 2

    assert edge_1_3 is not None
    assert edge_1_3["color"] == {"color": "purple", "highlight": "magenta"}
    assert edge_1_3["weight"] == 10

    # --- Verify Merged Options ---
    nodes_options = options_object.get("nodes")
    assert isinstance(nodes_options, dict), (
        "'nodes' key missing or not a dict in options_object"
    )

    font_options = nodes_options.get("font")
    assert isinstance(font_options, dict), (
        "'font' key missing or not a dict in options_object['nodes']"
    )

    assert font_options.get("size") == 10
    assert font_options.get("color") == "darkblue"

    edges_options = options_object.get("edges")
    assert isinstance(edges_options, dict)
    smooth_options = edges_options.get("smooth")
    assert isinstance(smooth_options, dict)
    assert smooth_options.get("enabled") is False

    edges_color_options = edges_options.get("color")
    assert isinstance(edges_color_options, dict)
    assert edges_color_options.get("color") == "gray"

    physics_options = options_object.get("physics")
    assert isinstance(physics_options, dict)
    assert physics_options.get("enabled") is False

    interaction_options = options_object.get("interaction")
    assert isinstance(interaction_options, dict)
    assert interaction_options.get("dragNodes") is False
    assert interaction_options.get("zoomView") is False

    layout_options = options_object.get("layout")
    assert isinstance(layout_options, dict)
    assert layout_options.get("randomSeed") == 123

    # Check group definitions from custom_vis_options

    groups_option = options_object.get("groups")
    assert isinstance(groups_option, dict), (
        f"Expected 'groups' to be a dict, got {type(groups_option)}"
    )

    group_0_style = groups_option.get("0")  # Key is string "0"
    assert isinstance(group_0_style, dict), (
        f"Expected groups['0'] to be a dict, got {type(group_0_style)}"
    )
    assert (
        group_0_style.get("shape") == "ellipse"
    )  # Use .get() for the final access too

    group_0_color = group_0_style.get(
        "color", {}
    )  # Default to empty dict if 'color' is missing
    assert isinstance(group_0_color, dict), (
        f"Expected groups['0']['color'] to be a dict, got {type(group_0_color)}"
    )
    assert group_0_color.get("border") == "black"

    group_1_style = groups_option.get("1")  # Key is string "1"
    assert isinstance(group_1_style, dict), (
        f"Expected groups['1'] to be a dict, got {type(group_1_style)}"
    )
    assert group_1_style.get("shape") == "box"

    group_1_font = group_1_style.get("font", {})  # Default to empty dict
    assert isinstance(group_1_font, dict), (
        f"Expected groups['1']['font'] to be a dict, got {type(group_1_font)}"
    )
    assert group_1_font.get("color") == "white"

    # Check that a default option not overridden is still present
    nodes_options_for_default_check = options_object.get("nodes", {})
    assert isinstance(nodes_options_for_default_check, dict)

    # Safely access values from DEFAULT_VIS_OPTIONS
    default_nodes_options = DEFAULT_VIS_OPTIONS.get("nodes")
    assert isinstance(default_nodes_options, dict), (
        "DEFAULT_VIS_OPTIONS['nodes'] is not a dict"
    )

    default_border_width = default_nodes_options.get("borderWidth")
    assert default_border_width is not None, (
        "borderWidth missing in DEFAULT_VIS_OPTIONS['nodes']"
    )

    assert (
        nodes_options_for_default_check.get("borderWidth")
        == default_border_width
    )
