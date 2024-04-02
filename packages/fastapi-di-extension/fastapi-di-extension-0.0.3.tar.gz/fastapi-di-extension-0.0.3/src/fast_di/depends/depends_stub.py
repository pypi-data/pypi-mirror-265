from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from typing import Callable


class Stub:  # noqa: F811
    def __init__(self, dependency: Callable, **kwargs):
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self):
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        if isinstance(other, Stub):
            return (
                self._dependency == other._dependency and self._kwargs == other._kwargs
            )
        else:
            if not self._kwargs:
                return self._dependency == other
            return False

    def __hash__(self):
        if not self._kwargs:
            return hash(self._dependency)
        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)


if TYPE_CHECKING:
    from typing import Union as FastDIStub

else:

    class FastDIStub:
        def __class_getitem__(cls, item):
            return Annotated[item, Depends(Stub(item))]
