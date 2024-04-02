# global
import abc
from typing import Optional, Union, Literal, List

# local

import startai


class _ArrayWithSorting(abc.ABC):
    def argsort(
        self: startai.Array,
        /,
        *,
        axis: int = -1,
        descending: bool = False,
        stable: bool = True,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.argsort. This method simply
        wraps the function, and so the docstring for startai.argsort also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        axis
            axis along which to sort. If set to ``-1``, the function
            must sort along the last axis. Default: ``-1``.
        descending
            sort order. If ``True``, the returned indices sort ``x`` in descending order
            (by value). If ``False``, the returned indices sort ``x`` in ascending order
            (by value). Default: ``False``.
        stable
            sort stability. If ``True``, the returned indices
            must maintain the relative order of ``x`` values
            which compare as equal. If ``False``, the returned
            indices may or may not maintain the relative order
            of ``x`` values which compare as equal (i.e., the
            relative order of ``x`` values which compare as
            equal is implementation-dependent). Default: ``True``.
        out
            optional output array, for writing the result to. It must have the same
            shape as input.

        Returns
        -------
        ret
            an array of indices. The returned array must have the same shape as ``x``.
            The returned array must have the default array index data type.

        Examples
        --------
        >>> x = startai.array([1, 5, 2])
        >>> y = x.argsort(axis=-1, descending=True, stable=False)
        >>> print(y)
        startai.array([1, 2, 0])

        >>> x = startai.array([9.6, 2.7, 5.2])
        >>> y = x.argsort(axis=-1, descending=True, stable=False)
        >>> print(y)
        startai.array([0, 2, 1])
        """
        return startai.argsort(
            self._data, axis=axis, descending=descending, stable=stable, out=out
        )

    def sort(
        self: startai.Array,
        /,
        *,
        axis: int = -1,
        descending: bool = False,
        stable: bool = True,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.sort. This method simply
        wraps the function, and so the docstring for startai.sort also applies to
        this method with minimal changes.

        Examples
        --------
        >>> x = startai.array([7, 8, 6])
        >>> y = x.sort(axis=-1, descending=True, stable=False)
        >>> print(y)
        startai.array([8, 7, 6])

        >>> x = startai.array([8.5, 8.2, 7.6])
        >>> y = x.sort(axis=-1, descending=True, stable=False)
        >>> print(y)
        startai.array([8.5, 8.2, 7.6])
        """
        return startai.sort(
            self._data, axis=axis, descending=descending, stable=stable, out=out
        )

    def msort(
        self: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.msort. This method simply
        wraps the function, and so the docstring for startai.msort also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            sorted array of the same type and shape as a

        Examples
        --------
        >>> a = startai.asarray([[8, 9, 6],[6, 2, 6]])
        >>> a.msort()
        startai.array(
            [[6, 2, 6],
            [8, 9, 6]]
            )
        """
        return startai.msort(self._data, out=out)

    def searchsorted(
        self: startai.Array,
        v: Union[startai.Array, startai.NativeArray],
        /,
        *,
        side: Literal["left", "right"] = "left",
        sorter: Optional[Union[startai.Array, startai.NativeArray, List[int]]] = None,
        ret_dtype: Union[startai.Dtype, startai.NativeDtype] = startai.int64,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.searchsorted.

        This method simply wraps the function, and so the docstring for
        startai.searchsorted also applies to this method with minimal
        changes.
        """
        return startai.searchsorted(
            self.data, v, side=side, sorter=sorter, ret_dtype=ret_dtype, out=out
        )
