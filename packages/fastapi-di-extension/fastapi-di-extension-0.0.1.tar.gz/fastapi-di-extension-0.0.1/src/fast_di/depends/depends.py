from typing import TYPE_CHECKING, Annotated

from fastapi import Depends


if TYPE_CHECKING:
    from typing import Union as FastDI

else:

    class FastDI:
        def __class_getitem__(cls, item):
            return Annotated[item, Depends()]
