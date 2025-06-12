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
    # Check for new UI element to confirm new template is used
    assert "Filter nodes (regex):" in content
    # Check for data injection
    assert '"id": "1"' in content
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
    """Test that DiGraphs get arrows enabled by default."""
    output_file = tmp_path / "test_digraph.html"
    nx_to_vis(
        simple_digraph, output_filename=str(output_file), show_browser=False
    )
    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    # Use the robust helper function
    options_object = _extract_json_object(content, "optionsObject")
    assert options_object is not None and isinstance(options_object, dict)

    # Now check the specific option
    edges_options = options_object.get("edges", {})
    arrows_options = edges_options.get("arrows", {})
    to_options = arrows_options.get("to", {})

    assert to_options.get("enabled") is True, (
        f"arrows.to.enabled is not True. Options found: {json.dumps(options_object, indent=2)}"
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


def test_keyboard_options_are_correct_by_default(
    simple_graph: nx.Graph,  # type: ignore[type-arg]
    tmp_path: Path,
) -> None:
    """Test that the default keyboard options are correctly set to not bind to window."""
    output_file = tmp_path / "test_keyboard_default.html"
    nx_to_vis(
        simple_graph, output_filename=str(output_file), show_browser=False
    )

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    options_object = _extract_json_object(content, "optionsObject")
    assert options_object is not None and isinstance(options_object, dict)

    interaction_opts = options_object.get("interaction", {})
    keyboard_opts = interaction_opts.get("keyboard", {})

    expected_keyboard_opts = {"enabled": True, "bindToWindow": False}
    assert keyboard_opts == expected_keyboard_opts, (
        f"Default keyboard options are incorrect. Expected {expected_keyboard_opts}, got {keyboard_opts}"
    )


def test_keyboard_options_can_be_overridden(
    simple_graph: nx.Graph,  # type: ignore[type-arg]
    tmp_path: Path,
) -> None:
    """Test that keyboard options can be fully overridden."""
    output_file = tmp_path / "test_keyboard_override.html"
    # Test overriding with a simple boolean
    custom_opts = {"interaction": {"keyboard": False}}
    nx_to_vis(
        simple_graph,
        output_filename=str(output_file),
        vis_options=custom_opts,
        show_browser=False,
    )

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    options_object = _extract_json_object(content, "optionsObject")
    assert options_object is not None and isinstance(options_object, dict)

    interaction_opts = options_object.get("interaction", {})
    keyboard_opts = interaction_opts.get("keyboard")

    assert keyboard_opts is False, (
        f"Keyboard options not overridden correctly. Expected False, got {keyboard_opts}"
    )


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

    nodes_array_raw = _extract_json_object(content, "allNodesArray")
    assert nodes_array_raw is not None and isinstance(nodes_array_raw, list)
    nodes_array: list[dict[str, Any]] = cast(
        list[dict[str, Any]], nodes_array_raw
    )

    edges_array_raw = _extract_json_object(content, "allEdgesArray")
    assert edges_array_raw is not None and isinstance(edges_array_raw, list)
    edges_array: list[dict[str, Any]] = cast(
        list[dict[str, Any]], edges_array_raw
    )
    # --- END CHANGE ---

    options_object_raw = _extract_json_object(content, "optionsObject")
    assert options_object_raw is not None and isinstance(
        options_object_raw, dict
    )
    options_object: dict[str, Any] = options_object_raw

    # --- Verify Nodes ---
    assert len(nodes_array) == nx_graph.number_of_nodes()

    node1_data = next((n for n in nodes_array if n["id"] == "1"), None)
    node_beta_data = next((n for n in nodes_array if n["id"] == "Beta"), None)
    node3_data = next((n for n in nodes_array if n["id"] == "3"), None)

    assert node1_data is not None
    assert node1_data["label"] == "Alpha"
    assert node1_data["title"] == "Node A"
    assert node1_data["color"] == "red"
    assert node1_data["shape"] == "star"
    assert node1_data["group"] == 0
    assert node1_data["size"] == 25

    assert node_beta_data is not None
    assert node_beta_data["label"] == "Beta Node"
    assert node_beta_data["color"] == "#00FF00"
    assert node_beta_data["group"] == 1
    assert node_beta_data["x"] == 10
    assert node_beta_data["y"] == 20

    assert node3_data is not None
    assert node3_data["label"] == "Gamma"
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
    assert isinstance(nodes_options, dict)
    font_options = nodes_options.get("font")
    assert isinstance(font_options, dict)
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

    groups_option = options_object.get("groups")
    assert isinstance(groups_option, dict)

    group_0_style = groups_option.get("0")
    assert isinstance(group_0_style, dict)
    assert group_0_style.get("shape") == "ellipse"
    group_0_color = group_0_style.get("color", {})
    assert isinstance(group_0_color, dict)
    assert group_0_color.get("border") == "black"

    group_1_style = groups_option.get("1")
    assert isinstance(group_1_style, dict)
    assert group_1_style.get("shape") == "box"
    group_1_font = group_1_style.get("font", {})
    assert isinstance(group_1_font, dict)
    assert group_1_font.get("color") == "white"

    # Check that a default option not overridden is still present
    nodes_options_for_default_check = options_object.get("nodes", {})
    assert isinstance(nodes_options_for_default_check, dict)
    default_nodes_options = DEFAULT_VIS_OPTIONS.get("nodes")
    assert isinstance(default_nodes_options, dict)
    default_border_width = default_nodes_options.get("borderWidth")
    assert default_border_width is not None
    assert (
        nodes_options_for_default_check.get("borderWidth")
        == default_border_width
    )
