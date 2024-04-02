# global
import abc
from typing import Optional

# local

import startai


class _ArrayWithSortingExperimental(abc.ABC):
    def lexsort(
        self: startai.Array,
        /,
        *,
        axis: int = -1,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.lexsort. This method simply
        wraps the function, and so the docstring for startai.lexsort also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        axis
            axis of each key to be indirectly sorted.
            By default, sort over the last axis of each key.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            array of integer indices with shape N, that sort the input array as keys.

        Examples
        --------
        >>> a = [1,5,1,4,3,4,4] # First column
        >>> b = [9,4,0,4,0,2,1] # Second column
        >>> keys = startai.asarray([b,a])
        >>> keys.lexsort() # Sort by a, then by b
        array([2, 0, 4, 6, 5, 3, 1])
        """
        return startai.lexsort(self._data, axis=axis, out=out)
