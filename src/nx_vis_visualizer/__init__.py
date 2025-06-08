# src/nx_vis_visualizer/__init__.py

from importlib.metadata import version

from .core import DEFAULT_VIS_OPTIONS, nx_to_vis

__version__ = version("nx-vis-visualizer")  # Get version from pyproject.toml

__all__ = [
    "DEFAULT_VIS_OPTIONS",
    "__version__",
    "nx_to_vis",
]
