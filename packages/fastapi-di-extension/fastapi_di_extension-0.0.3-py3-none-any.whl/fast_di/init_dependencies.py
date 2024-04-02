from typing import TYPE_CHECKING
from fastapi import FastAPI


if TYPE_CHECKING:
    from fast_di import DependencyCollector


def init_dependencies(app: FastAPI, *collectors: "DependencyCollector") -> None:
    if not collectors:
        raise RuntimeError("No collectors provided")

    for collector in collectors:
        for dependency, factory in collector.dependencies.items():
            app.dependency_overrides.update({dependency: factory})
