# plot-saver

`plot-saver` is a small reusable package for adding save buttons to Matplotlib figures in marimo notebooks.

It saves plots under a project results directory and can be configured with a project-level `config.toml`.

## Installation

```bash
pip install plot-saver
```

or with `uv`:

```bash
uv add plot-saver
```

## Config

`plot-saver` looks for a `config.toml` by searching upward from the current working directory.

All configuration keys are optional. If you do not provide a `config.toml`, or if you only provide some keys, `plot-saver` falls back to its built-in defaults.

The default output format is `png`.

You can override the defaults with a section like this:

```toml
[plot-saver]
format = "png"
default_label = "Save"
save_all_label = "Save all model plots"
empty_title = "No plots available"
empty_detail = "Render the notebook plots first."
saved_title = "Saved"
saved_many_title = "Saved {count} plots"
saved_error_title = "Saved with errors"
failed_title = "Could not save plots"
toast_detail_color = "#6b7280"

[plot-saver.theme]
radius = "8px"
padding_y = "0.45rem"
padding_x = "0.9rem"
font_size = "0.9rem"
light_border = "rgba(107, 114, 128, 0.35)"
light_background = "rgba(249, 250, 251, 0.95)"
light_text = "#111827"
light_hover_background = "rgba(243, 244, 246, 1)"
light_hover_border = "rgba(107, 114, 128, 0.55)"
light_disabled_background = "rgba(229, 231, 235, 0.9)"
light_disabled_border = "rgba(156, 163, 175, 0.35)"
dark_border = "rgba(156, 163, 175, 0.35)"
dark_background = "rgba(31, 41, 55, 0.95)"
dark_text = "#f3f4f6"
dark_hover_background = "rgba(55, 65, 81, 1)"
dark_hover_border = "rgba(209, 213, 219, 0.45)"
dark_disabled_background = "rgba(55, 65, 81, 0.8)"
dark_disabled_border = "rgba(107, 114, 128, 0.35)"
```

## Usage

```python
from pathlib import Path

import marimo as mo
import matplotlib.pyplot as plt
from plot_saver import make_plot_saver

fig, ax = plt.subplots()
ax.plot([0, 1, 2], [1, 3, 2])

save_plot = make_plot_saver(
    mo,
    results_dir=Path("results"),
    config_path=None,
    task_name="2AFC",
    model_id="example-model",
)

button = save_plot(fig, "Example figure")
save_all = save_plot.save_all_widget()
```

Saved plots go to:

```text
results/plots/<task_name>/<model_id>/
```

`save_plot(fig, "Example figure")` registers that figure and returns an individual save button for it.

`save_plot.save_all_widget()` returns a single button that saves every figure previously registered with that `PlotSaver` instance. This is useful in notebooks where you render several figures for the same task and model and want one action to export all of them together.

## API

Main entry points:

- `make_plot_saver(...)`
- `save_button(...)`
- `save_figure(...)`
- `get_plot_save_format(...)`
- `find_project_config_path(...)`
