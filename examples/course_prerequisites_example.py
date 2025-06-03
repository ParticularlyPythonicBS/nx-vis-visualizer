# examples/course_prerequisites_example.py
import networkx as nx


def create_course_prerequisites_graph_data() -> nx.DiGraph:  # type: ignore[type-arg]
    DG: nx.DiGraph = nx.DiGraph()  # type: ignore[type-arg]
    courses = {
        "CS101": {
            "label": "Intro to CS",
            "level": 1,
            "title": "Fundamentals of Computer Science",
        },
        "CS102": {
            "label": "Data Structures",
            "level": 2,
            "title": "Basic Data Structures and Algorithms",
        },
        "MA101": {
            "label": "Calculus I",
            "level": 1,
            "title": "Differential Calculus",
        },
        "CS201": {
            "label": "Algorithms",
            "level": 3,
            "title": "Advanced Algorithm Design",
        },
        "CS202": {
            "label": "Operating Systems",
            "level": 3,
            "title": "Principles of Operating Systems",
        },
        "CS301": {
            "label": "Compilers",
            "level": 4,
            "title": "Compiler Construction",
        },
    }
    for course_id, attrs in courses.items():
        DG.add_node(course_id, **attrs)

    DG.add_edges_from(
        [
            ("CS101", "CS102"),
            ("MA101", "CS102"),
            ("CS102", "CS201"),
            ("CS102", "CS202"),
            ("CS201", "CS301"),
            ("CS202", "CS301"),
        ]
    )
    return DG


course_prereq_vis_options = {
    "nodes": {
        "shape": "box",
        "font": {"size": 12, "face": "Arial"},
        "margin": 10,
    },
    "edges": {
        "arrows": {
            "to": {"enabled": True, "scaleFactor": 0.8, "type": "arrow"}
        },
        "smooth": {
            "enabled": True,
            "type": "cubicBezier",
            "forceDirection": "vertical",
            "roundness": 0.4,
        },
    },
    "layout": {
        "hierarchical": {
            "enabled": True,
            "direction": "UD",
            "sortMethod": "directed",
            "levelSeparation": 150,
            "nodeSpacing": 120,
        }
    },
    "physics": {"enabled": False},
    "interaction": {
        "hover": True,
        "dragNodes": False,
        "zoomView": True,
        "dragView": True,
    },
}
