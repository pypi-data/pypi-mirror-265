# global
from typing import Optional
import abc

# local
import startai


class _ArrayWithUtilityExperimental(abc.ABC):
    def optional_get_element(
        self: Optional[startai.Array] = None,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """If the input is a tensor or sequence type, it returns the input. If
        the input is an optional type, it outputs the element in the input. It
        is an error if the input is an empty optional-type (i.e. does not have
        an element) and the behavior is undefined in this case.

        Parameters
        ----------
        self
            Input array
        out
            Optional output array, for writing the result to.

        Returns
        -------
        ret
            Input array if it is not None
        """
        return startai.optional_get_element(self._data, out=out)
