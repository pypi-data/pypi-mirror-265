from functools import wraps
from typing import Callable, TypeVar

DependencyT = TypeVar("DependencyT")
FactoryT = TypeVar("FactoryT", bound=Callable)


class BaseDependencyCollector:
    def __init__(self) -> None:
        self.dependencies: dict[DependencyT, FactoryT] = {}

    def add_factory(self, dependency: DependencyT, factory: FactoryT) -> None:
        self.dependencies[dependency] = factory

    def add_singleton(
        self, dependency: DependencyT, factory: FactoryT, is_async: bool = False
    ) -> None:
        self.dependencies[dependency] = self.__create_singleton(factory, is_async)

    def __create_singleton(
        self, factory: FactoryT, is_async: bool
    ) -> Callable[..., FactoryT]:
        singleton_instance = None

        @wraps(factory)
        async def async_wrapper(*args, **kwargs) -> FactoryT:
            nonlocal singleton_instance

            if singleton_instance is None:
                singleton_instance = await factory(*args, **kwargs)

            return singleton_instance

        @wraps(factory)
        def sync_wrapper(*args, **kwargs) -> FactoryT:
            nonlocal singleton_instance

            if singleton_instance is None:
                singleton_instance = factory(*args, **kwargs)

            return singleton_instance

        return async_wrapper if is_async else sync_wrapper
