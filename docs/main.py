# docs/main.py
import copy
import json
import os
import uuid
from html import escape  # For escaping graph_title in the iframe HTML
from typing import Any

import networkx as nx

from nx_vis_visualizer import DEFAULT_VIS_OPTIONS, nx_to_vis
from nx_vis_visualizer.core import (
    _deep_merge_dicts,  # Assuming this is still needed
)

# Ensure the output directory for graphs exists
GENERATED_GRAPHS_DIR_NAME: str = "generated_graphs"
# Path relative to the docs directory
DOCS_ASSETS_GRAPHS_DIR: str = os.path.join("assets", GENERATED_GRAPHS_DIR_NAME)


# The 'env' object is specific to mkdocs-macros-plugin.
def define_env(env: Any) -> None:
    """
    Hook for defining variables, macros, and filters for MkDocs.
    `env.project_dir` is the root of the MkDocs project (where mkdocs.yml is).
    `env.conf['docs_dir']` is the path to the docs directory, relative to project_dir.
    """
    abs_output_dir: str = os.path.join(
        env.project_dir, env.conf["docs_dir"], DOCS_ASSETS_GRAPHS_DIR
    )
    os.makedirs(abs_output_dir, exist_ok=True)

    @env.macro  # type: ignore[misc]
    def embed_interactive_graph(
        nx_graph_code: str,
        vis_options_json_str: str = "{}",
        iframe_height: str = "500px",
        graph_title: str = "Interactive Graph",
    ) -> str:  # Macros typically return HTML strings
        """
        Generates a NetworkX graph from Python code, saves it as an HTML file,
        and returns an iframe to embed it.
        """
        local_scope: dict[str, Any] = {"nx": nx, "G": None}
        graph: nx.Graph | None = (  # type: ignore[type-arg]
            None
        )

        try:
            # Provide globals for exec, including nx
            exec(nx_graph_code, {"nx": nx}, local_scope)
            graph_candidate = local_scope.get("G")
            if isinstance(
                graph_candidate, nx.Graph
            ):  # Check if it's a NetworkX graph instance
                graph = graph_candidate  # Now graph is known to be nx.Graph
            else:
                return (
                    "<p style='color:red; font-weight:bold;'>"
                    "Error: Provided code did not create a NetworkX graph "
                    "in variable 'G'.</p>"
                )
        except Exception as e:
            import traceback

            print(f"Error executing graph code: {traceback.format_exc()}")
            return (
                f"<p style='color:red; font-weight:bold;'>"
                f"Error executing graph generation code: {escape(str(e))}</p>"
            )

        user_vis_options: dict[str, Any]
        try:
            user_vis_options = json.loads(vis_options_json_str)
        except json.JSONDecodeError as e:
            return (
                f"<p style='color:red; font-weight:bold;'>"
                f"Error decoding vis_options_json_str: {escape(str(e))}</p>"
                f"<pre>{escape(vis_options_json_str)}</pre>"
            )

        final_vis_options: dict[str, Any] = copy.deepcopy(DEFAULT_VIS_OPTIONS)
        _deep_merge_dicts(user_vis_options, final_vis_options)

        graph_html_filename: str = f"graph_{uuid.uuid4().hex[:10]}.html"
        graph_html_save_path: str = os.path.join(
            abs_output_dir, graph_html_filename
        )

        nx_to_vis(
            graph,
            output_filename=graph_html_save_path,
            html_title=graph_title,
            vis_options=final_vis_options,
            show_browser=False,
            graph_width="100%",
            graph_height="100%",
        )

        path_to_graph_in_docs: str = os.path.join(
            DOCS_ASSETS_GRAPHS_DIR, graph_html_filename
        )

        # Assuming env.filters['url'] exists and is callable
        iframe_src: str = env.filters["url"](path_to_graph_in_docs)
        escaped_graph_title: str = escape(
            graph_title
        )  # Escape title for HTML context

        return f"""
        <div class="interactive-graph-wrapper" style="margin-bottom: 1.5em; padding: 1em; border: 1px solid #e0e0e0; border-radius: 4px; background-color: #f9f9f9;">
            <h4 style="margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em;">{escaped_graph_title}</h4>
            <iframe src="{iframe_src}"
                    width="100%"
                    height="{iframe_height}"
                    style="border: 1px solid #ccc; max-width: 100%; display: block;"
                    sandbox="allow-scripts allow-same-origin"
                    loading="lazy">
                Your browser does not support iframes. Please update your browser.
            </iframe>
        </div>
        """

    @env.macro  # type: ignore[misc]
    def show_code_block(
        code_string: str, language: str = "python"
    ) -> str:  # Added return type
        """Displays a code block, typically for showing the graph generation code."""
        escaped_code: str = code_string.strip()
        return f"```{language}\n{escaped_code}\n```"
