# global
import abc
from numbers import Number
from typing import Optional, Union, Tuple

# local
import startai


class _ArrayWithSearching(abc.ABC):
    def argmax(
        self: startai.Array,
        /,
        *,
        axis: Optional[int] = None,
        keepdims: bool = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
        select_last_index: bool = False,
        out: Optional[startai.Array] = None,
    ) -> Union[startai.Array, int]:
        """startai.Array instance method variant of startai.argmax. This method simply
        wraps the function, and so the docstring for startai.argmax also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        axis
            axis along which to search. If None, the function must return the index of
            the maximum value of the flattened array. Default: ``None``.
        keepdims
            If this is set to True, the axes which are reduced are left in the result as
            dimensions with size one. With this option, the result will broadcast
            correctly against the array.
        dtype
            Optional data type of the output array.
        select_last_index
            If this is set to True, the index corresponding to the
            last occurrence of the maximum value will be returned.
        out
            If provided, the result will be inserted into this array. It should be of
            the appropriate shape and dtype.

        Returns
        -------
        ret
            if axis is None, a zero-dimensional array containing the index of the first
            occurrence of the maximum value; otherwise, a non-zero-dimensional array
            containing the indices of the maximum values. The returned array must have
            the default array index data type.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([0., 1., 2.])
        >>> y = x.argmax()
        >>> print(y)
        startai.array(2)

        >>> x = startai.array([[1., -0., -1.], [-2., 3., 2.]])
        >>> y = x.argmax(axis=1)
        >>> print(y)
        startai.array([0, 1])

        >>> x = startai.array([[4., 0., -1.], [2., -3., 6]])
        >>> y = x.argmax(axis=1, keepdims=True)
        >>> print(y)
        startai.array([[0], [2]])

        >>> x = startai.array([[4., 0., -1.], [2., -3., 6]])
        >>> y = x.argmax(axis=1, dtype=startai.int64)
        >>> print(y, y.dtype)
        startai.array([0, 2]) int64
        """
        return startai.argmax(
            self._data,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            select_last_index=select_last_index,
            out=out,
        )

    def argmin(
        self: startai.Array,
        /,
        *,
        axis: Optional[int] = None,
        keepdims: bool = False,
        dtype: Optional[Union[startai.int32, startai.int64]] = None,
        select_last_index: bool = False,
        out: Optional[startai.Array] = None,
    ) -> Union[startai.Array, int]:
        """startai.Array instance method variant of startai.argmin. This method simply
        wraps the function, and so the docstring for startai.argmin also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        axis
            axis along which to search. If None, the function must return the index of
            the minimum value of the flattened array. Default = None.
        keepdims
            if True, the reduced axes (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the result must be compatible with
            the input array (see Broadcasting). Otherwise, if False, the reduced axes
            (dimensions) must not be included in the result. Default = False.
        dtype
            An optional output_dtype from: int32, int64. Defaults to int64.
        select_last_index
            If this is set to True, the index corresponding to the
            last occurrence of the minimum value will be returned.
        out
            if axis is None, a zero-dimensional array containing the index of the first
            occurrence of the minimum value; otherwise, a non-zero-dimensional array
            containing the indices of the minimum values. The returned array must have
            the default array index data type.

        Returns
        -------
        ret
            Array containing the indices of the minimum values across the specified
            axis.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([0., 1., -1.])
        >>> y = x.argmin()
        >>> print(y)
        startai.array(2)

        >>> x = startai.array([[0., 1., -1.],[-2., 1., 2.],[1., -2., 0.]])
        >>> y= startai.zeros((3,1), dtype=startai.int64)
        >>> x.argmin(axis=1, keepdims=True, out=y)
        >>> print(y)
        startai.array([[2],
               [0],
               [1]])
        """
        return startai.argmin(
            self._data,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            select_last_index=select_last_index,
            out=out,
        )

    def nonzero(
        self: startai.Array,
        /,
        *,
        as_tuple: bool = True,
        size: Optional[int] = None,
        fill_value: Number = 0,
    ) -> Union[Tuple[startai.Array], startai.Array]:
        """startai.Array instance method variant of startai.nonzero. This method simply
        wraps the function, and so the docstring for startai.nonzero also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        as_tuple
            if True, the output is returned as a tuple of indices, one for each
            dimension of the input, containing the indices of the true elements in that
            dimension. If False, the coordinates are returned in a (N, ndim) array,
            where N is the number of true elements. Default = True.
        size
            if specified, the function will return an array of shape (size, ndim).
            If the number of non-zero elements is fewer than size, the remaining
            elements will be filled with fill_value. Default = None.
        fill_value
            when size is specified and there are fewer than size number of elements,
            the remaining elements in the output array will be filled with fill_value.
            Default = 0.

        Returns
        -------
        ret
            Array containing the indices of the non-zero values.
        """
        return startai.nonzero(
            self._data, as_tuple=as_tuple, size=size, fill_value=fill_value
        )

    def where(
        self: startai.Array,
        x1: startai.Array,
        x2: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.where. This method simply
        wraps the function, and so the docstring for startai.where also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Where True, yield x1, otherwise yield x2.
        x1
            input array. Should have a numeric data type.
        x2
            values from which to choose when condition is False.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            An array with elements from self where condition is True, and elements from
            x2 otherwise.

        Examples
        --------
        >>> condition = startai.array([[True, False], [True, True]])
        >>> x1 = startai.array([[1, 2], [3, 4]])
        >>> x2 = startai.array([[5, 6], [7, 8]])
        >>> res = x1.where(condition,x2)
        >>> print(res)
        startai.array([[1, 0],
               [1, 1]])
        """
        return startai.where(self._data, x1._data, x2._data, out=out)

    def argwhere(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.argwhere. This method
        simply wraps the function, and so the docstring for startai.argwhere also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array for which indices are desired
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Indices for where the boolean array is True.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([[1, 2], [3, 4]])
        >>> res = x.argwhere()
        >>> print(res)
        startai.array([[0, 0], [0, 1], [1, 0], [1, 1]])

        >>> x = startai.array([[0, 2], [3, 4]])
        >>> res = x.argwhere()
        >>> print(res)
        startai.array([[0, 1], [1, 0], [1, 1]])
        """
        return startai.argwhere(self._data, out=out)
