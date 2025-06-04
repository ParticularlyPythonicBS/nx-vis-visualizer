# generate_graph_examples.py

import importlib
import os
import sys

import networkx as nx  # Keep for type hinting if G is passed around

# --- Configuration ---
DOCS_DIR = "docs"
GENERATED_GRAPHS_ASSET_SUBDIR = os.path.join("assets", "generated_graphs")
OUTPUT_DIR = os.path.join(DOCS_DIR, GENERATED_GRAPHS_ASSET_SUBDIR)
EXAMPLES_DIR = "examples"

project_root = os.path.dirname(os.path.abspath(__file__))
examples_abs_path = os.path.join(project_root, EXAMPLES_DIR)
if examples_abs_path not in sys.path:
    sys.path.insert(0, examples_abs_path)

os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Ensured output directory exists: {os.path.abspath(OUTPUT_DIR)}")


# --- Helper Function ---
def generate_graph_from_example(
    example_module_name: str,
    graph_creation_func_name: str,
    vis_options_var_name: str,
    output_graph_filename: str,
    html_page_title: str,
):
    print(f"\n--- Generating: {html_page_title} ({output_graph_filename}) ---")
    try:
        from nx_vis_visualizer import nx_to_vis  # Import here

        example_module = importlib.import_module(example_module_name)
        graph_creation_func = getattr(example_module, graph_creation_func_name)
        vis_options_dict = getattr(example_module, vis_options_var_name)

        G = graph_creation_func()
        if not isinstance(G, nx.Graph):  # nx.DiGraph is a subclass of nx.Graph
            print(
                f"Error: {graph_creation_func_name} from {example_module_name} did not produce a valid NetworkX graph."
            )
            return

        output_filepath = os.path.join(OUTPUT_DIR, output_graph_filename)

        nx_to_vis(
            G,
            output_filename=output_filepath,
            html_title=html_page_title,
            vis_options=vis_options_dict,
            show_browser=False,
            graph_width="100%",
            graph_height="100%",
        )
        print(f"Successfully saved: {output_filepath}")

    except ImportError as e:
        print(
            f"ImportError for module {example_module_name} or nx_vis_visualizer: {e}"
        )
    except AttributeError as e:
        print(
            f"AttributeError accessing function/variable in {example_module_name}: {e}"
        )
    except Exception as e:
        print(f"An unexpected error occurred for {html_page_title}: {e}")
        import traceback

        traceback.print_exc()


# --- Main execution ---
if __name__ == "__main__":
    print("Starting generation of graph examples from 'examples' directory...")

    generate_graph_from_example(
        example_module_name="cycle_example",
        graph_creation_func_name="create_cycle_graph_data",
        vis_options_var_name="cycle_graph_vis_options",
        output_graph_filename="cycle_graph_example.html",
        html_page_title="Interactive 5-Cycle Graph",
    )

    generate_graph_from_example(
        example_module_name="karate_club_example",
        graph_creation_func_name="create_karate_club_graph_data",
        vis_options_var_name="karate_club_vis_options",
        output_graph_filename="karate_club_example.html",
        html_page_title="Zachary's Karate Club",
    )

    generate_graph_from_example(
        example_module_name="simple_directed_example",
        graph_creation_func_name="create_simple_directed_graph_data",
        vis_options_var_name="simple_directed_vis_options",
        output_graph_filename="simple_directed_example.html",
        html_page_title="Simple Directed Graph",
    )

    generate_graph_from_example(
        example_module_name="course_prerequisites_example",
        graph_creation_func_name="create_course_prerequisites_graph_data",
        vis_options_var_name="course_prereq_vis_options",
        output_graph_filename="course_prerequisites_example.html",
        html_page_title="Course Prerequisites",
    )

    generate_graph_from_example(
        example_module_name="customization_example",
        graph_creation_func_name="create_showcase_graph",
        vis_options_var_name="custom_vis_options",
        output_graph_filename="advanced_showcase_example.html",
        html_page_title="Advanced Graph Showcase",
    )

    print("\nFinished generating graph examples.")
    print(f"Check the output in: {os.path.abspath(OUTPUT_DIR)}")
