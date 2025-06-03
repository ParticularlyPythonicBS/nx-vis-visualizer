# Installation

You can install `nx-vis-visualizer` using `pip`. It's recommended to use a virtual environment.

## Using `pip`

Once the package is available on PyPI:

```bash
pip install nx-vis-visualizer
```

If you have cloned the repository locally and want to install it in editable mode (recommended for development):

```bash
# Navigate to the root of the cloned repository
pip install -e .
```

## Using `uv` (for development)

If you are contributing to the project or prefer `uv` for environment management:

1. **Clone the repository (if you haven't already):**

    ```bash
    git clone https://github.com/yourusername/nx-vis-visualizer.git
    cd nx-vis-visualizer
    ```

2. **Create and activate a virtual environment:**

    ```bash
    uv venv
    source .venv/bin/activate  # On Linux/macOS
    # .venv\Scripts\activate    # On Windows (Command Prompt)
    # .venv\Scripts\Activate.ps1 # On Windows (PowerShell)
    ```

3. **Install the package in editable mode with development dependencies:**
    This will also install tools for testing, linting, and documentation.

    ```bash
    uv pip install -e .[dev,docs,notebook]
    ```

## Dependencies

`nx-vis-visualizer` primarily depends on:

* [NetworkX](https://networkx.org/): For graph creation and manipulation.

The generated HTML files rely on the [vis.js Network](https://visjs.github.io/vis-network/docs/network/) library, which is loaded from a CDN by default, so you don't need to install it separately.
