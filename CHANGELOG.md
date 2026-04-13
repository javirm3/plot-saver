# Changelog

## 0.1.2

- Dropped wrapper-level anywidget UIElement caching so marimo rebuilds the plot saver widget with a fresh virtual-file JavaScript module on each rerun.
- Kept the widget comm initialization path so the underlying anywidget model id remains stable across marimo renders.

## 0.1.1

- Fixed the marimo anywidget compatibility layer to serve widget JavaScript through marimo-managed virtual files instead of embedding untrusted `data:` URLs.
- Raised the `anywidget` dependency floor to `0.10.0` for compatibility with the latest marimo release.
