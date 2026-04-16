from plot_saver.save_widget import SaveFigureAnyWidget


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
