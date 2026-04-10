from __future__ import annotations

from copy import deepcopy
from importlib.resources import files
from pathlib import Path
import tomllib


PROJECT_CONFIG_NAME = "config.toml"
DEFAULT_CONFIG_RESOURCE = "resources/default_config.toml"


def _read_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def _merge_dicts(base: dict, override: dict) -> dict:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def find_project_config_path(start: str | Path | None = None) -> Path | None:
    current = Path(start).expanduser().resolve() if start is not None else Path.cwd().resolve()
    if current.is_file():
        current = current.parent
    for directory in (current, *current.parents):
        candidate = directory / PROJECT_CONFIG_NAME
        if candidate.exists():
            return candidate
    return None


def _load_default_config() -> dict:
    default_config = files("plot_saver").joinpath(DEFAULT_CONFIG_RESOURCE)
    with default_config.open("rb") as f:
        return tomllib.load(f)


def load_app_config(config_path: str | Path | None = None) -> dict:
    cfg = deepcopy(_load_default_config())
    resolved = Path(config_path).expanduser().resolve() if config_path else find_project_config_path()
    if resolved is not None and resolved.exists():
        cfg = _merge_dicts(cfg, _read_toml(resolved))
    return cfg
