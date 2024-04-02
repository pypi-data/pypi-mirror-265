# global
from typing import Optional, Union

# local
import startai
from .base import NestedArrayBase


class NestedArrayElementwise(NestedArrayBase):
    @staticmethod
    def static_add(
        x1: Union[NestedArrayBase, startai.Array, startai.NestedArray],
        x2: Union[NestedArrayBase, startai.Array, startai.NestedArray],
        /,
        *,
        alpha: Optional[Union[int, float]] = None,
        out: Optional[startai.Array] = None,
    ) -> NestedArrayBase:
        pass
        # return self._elementwise_op(other, startai.add)
