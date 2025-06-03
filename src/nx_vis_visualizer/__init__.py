# src/nx_vis_visualizer/__init__.py

from .core import DEFAULT_VIS_OPTIONS, nx_to_vis

# Read version from a single source of truth, e.g., a _version.py file
# or dynamically using importlib.metadata (for installed packages)
# For simplicity now, we can hardcode or use a simple text file.
# A common pattern is to have a _version.py:
# __version__ = "0.1.0"
# And then: from ._version import __version__

# For now, let's keep it simple for the initial setup:
__version__ = "0.1.0"  # Should match pyproject.toml

__all__ = [
    "DEFAULT_VIS_OPTIONS",
    "__version__",
    "nx_to_vis",
]
