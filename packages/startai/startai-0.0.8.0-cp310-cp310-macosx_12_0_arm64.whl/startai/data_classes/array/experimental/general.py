# global
import abc
from typing import Union, Callable, Sequence

# local
import startai


class _ArrayWithGeneralExperimental(abc.ABC):
    def reduce(
        self: startai.Array,
        init_value: Union[int, float],
        computation: Callable,
        /,
        *,
        axes: Union[int, Sequence[int]] = 0,
        keepdims: bool = False,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.reduce. This method simply
        wraps the function, and so the docstring for startai.reduce also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            The array to act on.
        init_value
            The value with which to start the reduction.
        computation
            The reduction function.
        axes
            The dimensions along which the reduction is performed.
        keepdims
            If this is set to True, the axes which are reduced are left in the result as
            dimensions with size one.

        Returns
        -------
        ret
            The reduced array.

        Examples
        --------
        >>> x = startai.array([[1, 2, 3], [4, 5, 6]])
        >>> x.reduce(0, startai.add, 0)
        startai.array([6, 15])
        """
        return startai.reduce(self, init_value, computation, axes=axes, keepdims=keepdims)
