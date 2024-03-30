from typing import Callable

from fast_di.collector.base import BaseDependencyCollector, DependencyT, FactoryT


class DependencyCollector(BaseDependencyCollector):
    def __init__(self) -> None:
        super().__init__()

    def factory(self, dependency: DependencyT) -> Callable[[FactoryT], None]:
        def decorator(factory: FactoryT) -> None:
            self.add_factory(dependency, factory)

        return decorator

    def singleton(
        self, dependency: DependencyT, is_async: bool = False
    ) -> Callable[[FactoryT], None]:
        def decorator(factory: FactoryT) -> None:
            self.add_singleton(dependency, factory, is_async)

        return decorator
