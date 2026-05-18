from pathlib import Path
import tempfile

from plot_saver.save_widget import PlotSaver, SaveFigureAnyWidget


class _Status:
    def __init__(self):
        self.toasts = []

    def toast(self, *args, **kwargs):
        self.toasts.append((args, kwargs))


class _Mo:
    def __init__(self):
        self.status = _Status()


class _Figure:
    def __init__(self):
        self.saved = []

    def savefig(self, path, **kwargs):
        self.saved.append((path, kwargs))


def test_save_widget_assets_are_file_backed():
    assert SaveFigureAnyWidget._esm._path.name == "figure_save_widget.js"
    assert SaveFigureAnyWidget._css._path.name == "figure_save_widget.css"
    assert SaveFigureAnyWidget._esm._path.is_file()
    assert SaveFigureAnyWidget._css._path.is_file()


def test_click_command_increments_clicks_and_clears_command():
    widget = SaveFigureAnyWidget()

    widget.command = "click"
    widget.command_payload = {"source": "button"}
    widget.command_nonce = 1

    assert widget.clicks == 1
    assert widget.command == ""
    assert widget.command_payload == {}


def test_unknown_command_is_ignored_and_cleared():
    widget = SaveFigureAnyWidget()

    widget.command = "unknown"
    widget.command_payload = {"source": "button"}
    widget.command_nonce = 1

    assert widget.clicks == 0
    assert widget.command == ""
    assert widget.command_payload == {}


def test_plot_saver_individual_button_uses_current_registry_item():
    mo = _Mo()
    plot_saver = PlotSaver(
        mo,
        results_dir=Path(tempfile.mkdtemp()),
        config_path=None,
        task_name="task",
        model_id="model",
    )

    fig_initial = _Figure()
    button_initial = plot_saver(fig_initial, "Example", stem="example")

    assert isinstance(button_initial, SaveFigureAnyWidget)

    button_initial.clicks = 1

    assert len(fig_initial.saved) == 1
    assert mo.status.toasts[-1][0][0] == "Saved"

    fig_current = _Figure()
    button_current = plot_saver(fig_current, "Example", stem="example")

    assert button_current is not button_initial

    button_current.clicks = 2

    assert len(fig_initial.saved) == 1
    assert len(fig_current.saved) == 1
    assert fig_current.saved[0][0].name == f"example.{plot_saver.fmt}"


def test_plot_saver_old_individual_button_uses_current_registry_item():
    mo = _Mo()
    plot_saver = PlotSaver(
        mo,
        results_dir=Path(tempfile.mkdtemp()),
        config_path=None,
        task_name="task",
        model_id="model",
    )

    fig_initial = _Figure()
    button_initial = plot_saver(fig_initial, "Example", stem="example")
    fig_current = _Figure()
    plot_saver(fig_current, "Example", stem="example")

    button_initial.clicks = 1

    assert len(fig_initial.saved) == 0
    assert len(fig_current.saved) == 1
    assert fig_current.saved[0][0].name == f"example.{plot_saver.fmt}"


def test_save_all_widget_instances_are_fresh_and_enable_after_registration():
    mo = _Mo()
    plot_saver = PlotSaver(
        mo,
        results_dir=Path(tempfile.mkdtemp()),
        config_path=None,
        task_name="task",
        model_id="model",
    )

    save_all_initial = plot_saver.save_all_widget()
    save_all_current = plot_saver.save_all_widget()

    assert save_all_current is not save_all_initial
    assert save_all_initial.disabled
    assert save_all_current.disabled

    plot_saver(_Figure(), "Example", stem="example")

    assert not save_all_initial.disabled
    assert not save_all_current.disabled
