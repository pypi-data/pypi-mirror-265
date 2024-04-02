# global
import abc
from typing import Optional, Tuple

# local
import startai


class _ArrayWithSearchingExperimental(abc.ABC):
    def unravel_index(
        self: startai.Array,
        shape: Tuple[int],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> Tuple[startai.Array]:
        """startai.Array instance method variant of startai.unravel_index. This method
        simply wraps the function, and so the docstring for startai.unravel_index
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        shape
            The shape of the array to use for unraveling indices.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Tuple with arrays that have the same shape as the indices array.

        Examples
        --------
        >>> indices = startai.array([22, 41, 37])
        >>> indices.unravel_index((7,6))
        (startai.array([3, 6, 6]), startai.array([4, 5, 1]))
        """
        return startai.unravel_index(self._data, shape, out=out)
