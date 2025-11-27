from importlib import import_module

__all__ = ["cli"]


def __getattr__(name):
    if name == "cli":
        from .main import cli  # imported lazily to avoid heavy dependencies at import time
        return cli

    if name in {
        "ask_cmd",
        "process_cmd",
        "project_cmd",
        "sources_cmd",
        "config_cmd",
        "debug_cmd",
        "utils",
    }:
        return import_module(f"{__name__}.{name}")

    raise AttributeError(name)