# global
import abc
import numpy as np
from numbers import Number
from typing import Any, Iterable, Union, Optional, Dict, Callable, List, Tuple

# ToDo: implement all methods here as public instance methods

# local
import startai


class _ArrayWithGeneral(abc.ABC):
    def is_native_array(
        self: startai.Array,
        /,
        *,
        exclusive: bool = False,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.is_native_array. This
        method simply wraps the function, and so the docstring for
        startai.is_native_array also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input to check
        exclusive
            Whether to check if the data type is exclusively an array, rather than a
            variable or traced array.

        Returns
        -------
        ret
            Boolean, whether or not x is a native array.

        Examples
        --------
        >>> x = startai.array([0, 1, 2])
        >>> ret = x.is_native_array()
        >>> print(ret)
        False
        """
        return startai.is_native_array(self, exclusive=exclusive)

    def is_startai_array(self: startai.Array, /, *, exclusive: bool = False) -> bool:
        """startai.Array instance method variant of startai.is_startai_array. This method
        simply wraps the function, and so the docstring for startai.is_startai_array
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        exclusive
            Whether to check if the data type is exclusively an array, rather than a
            variable or traced array.

        Returns
        -------
        ret
            Boolean, whether or not x is an startai array.

        Examples
        --------
        >>> x = startai.array([0, 1, 2])
        >>> ret = x.is_startai_array()
        >>> print(ret)
        True
        """
        return startai.is_startai_array(self, exclusive=exclusive)

    def is_array(self: startai.Array, /, *, exclusive: bool = False) -> bool:
        """startai.Array instance method variant of startai.is_array. This method
        simply wraps the function, and so the docstring for startai.is_array also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input to check
        exclusive
            Whether to check if the data type is exclusively an array, rather than a
            variable or traced array.

        Returns
        -------
        ret
            Boolean, whether or not x is an array.

        Examples
        --------
        >>> x = startai.array([0, 1, 2])
        >>> print(x.is_array())
        True
        """
        return startai.is_array(self, exclusive=exclusive)

    def is_startai_container(self: startai.Array) -> bool:
        """startai.Array instance method variant of startai.is_startai_container. This
        method simply wraps the function, and so the docstring for
        startai.is_startai_container also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input to check

        Returns
        -------
        ret
            Boolean, whether or not x is an startai container.

        Examples
        --------
        >>> x = startai.array([0, 1, 2])
        >>> print(x.is_startai_container())
        False
        """
        return startai.is_startai_container(self)

    def all_equal(
        self: startai.Array, *x2: Iterable[Any], equality_matrix: bool = False
    ) -> Union[bool, startai.Array, startai.NativeArray]:
        """startai.Array instance method variant of startai.all_equal. This method
        simply wraps the function, and so the docstring for startai.all_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        x2
            input iterable to compare to ``self``
        equality_matrix
            Whether to return a matrix of equalities comparing each input with every
            other. Default is ``False``.

        Returns
        -------
        ret
            Boolean, whether or not the inputs are equal, or matrix array of booleans if
            equality_matrix=True is set.

        Examples
        --------
        >>> x1 = startai.array([1, 1, 0, 0, 1, -1])
        >>> x2 = startai.array([1, 1, 0, 0, 1, -1])
        >>> y = x1.all_equal(x2)
        >>> print(y)
        True

        >>> x1 = startai.array([0, 0])
        >>> x2 = startai.array([0, 0])
        >>> x3 = startai.array([1, 0])
        >>> y = x1.all_equal(x2, x3, equality_matrix=True)
        >>> print(y)
        startai.array([[ True,  True, False],
           [ True,  True, False],
           [False, False,  True]])
        """
        arrays = [self] + [x for x in x2]
        return startai.all_equal(*arrays, equality_matrix=equality_matrix)

    def has_nans(self: startai.Array, /, *, include_infs: bool = True):
        """startai.Array instance method variant of startai.has_nans. This method
        simply wraps the function, and so the docstring for startai.has_nans also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        include_infs
            Whether to include ``+infinity`` and ``-infinity`` in the check.
            Default is ``True``.

        Returns
        -------
        ret
            Boolean as to whether the array contains nans.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = x.has_nans()
        >>> print(y)
        False
        """
        return startai.has_nans(self, include_infs=include_infs)

    def gather(
        self: startai.Array,
        indices: Union[startai.Array, startai.NativeArray],
        /,
        *,
        axis: int = -1,
        batch_dims: int = 0,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.gather. This method simply
        wraps the function, and so the docstring for startai.gather also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            The array from which to gather values.
        indices
            The array which indicates the indices that will be gathered along
            the specified axis.
        axis
            The axis from which the indices will be gathered. Default is ``-1``.
        batch_dims
            Optional int, lets you gather different items from each element of a batch.
            Default is ``0``.
        out
            Optional array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            New array with the values gathered at the specified indices along
            the specified axis.

        Examples
        --------
        >>> x = startai.array([0., 1., 2.])
        >>> y = startai.array([0, 1])
        >>> gather = x.gather(y)
        >>> print(gather)
        startai.array([0., 1.])

        >>> x = startai.array([[0., 1., 2.],[3., 4., 5.]])
        >>> y = startai.array([[0, 1],[1, 2]])
        >>> z = startai.zeros((2, 2, 2))
        >>> gather = x.gather(y, out=z)
        >>> print(z)
        startai.array([[[0., 1.],[1., 2.]],[[3., 4.],[4., 5.]]])

        >>> x = startai.array([[[0., 1.], [2., 3.]],
        ...                [[8., 9.], [10., 11.]]])
        >>> y = startai.array([[0, 1]])
        >>> z = startai.zeros((1, 2, 2, 2))
        >>> gather = x.gather(y, axis=0, out=z)
        >>> print(z)
        startai.array(
            [[[[ 0.,  1.],
            [ 2.,  3.]],
            [[ 8.,  9.],
            [10., 11.]]]])

        >>> x = startai.array([[0, 10, 20, 0, 0],
        ...                [0, 0, 0, 30, 40],
        ...                [0, 10, 0, 0, 40]])
        >>> y = startai.array([[1, 2],[3, 4],[1, 4]])
        >>> gather = x.gather(y, batch_dims=1)
        >>> print(gather)
        startai.array([[10, 20], [30, 40],[10, 40]])
        """
        return startai.gather(self, indices, axis=axis, batch_dims=batch_dims, out=out)

    def scatter_nd(
        self: startai.Array,
        updates: Union[startai.Array, startai.NativeArray],
        /,
        shape: Optional[startai.Array] = None,
        *,
        reduction: str = "sum",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """Scatter updates into an array according to indices.

        Parameters
        ----------
        self
            array of indices
        updates
            values to update input tensor with
        shape
            The shape of the result. Default is ``None``, in which case tensor
            argument must be provided.
        reduction
            The reduction method for the scatter, one of 'sum', 'min', 'max'
            or 'replace'
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            New array of given shape, with the values scattered at the indices.

        Examples
        --------
        With scatter values into an array

        >>> arr = startai.array([1,2,3,4,5,6,7,8, 9, 10])
        >>> indices = startai.array([[4], [3], [1], [7]])
        >>> updates = startai.array([9, 10, 11, 12])
        >>> scatter = indices.scatter_nd(updates, reduction='replace', out=arr)
        >>> print(scatter)
        startai.array([ 1, 11,  3, 10,  9,  6,  7, 12,  9, 10])

        With scatter values into an empty array

        >>> shape = startai.array([2, 5])
        >>> indices = startai.array([[1,4], [0,3], [1,1], [0,2]])
        >>> updates = startai.array([25, 40, 21, 22])
        >>> scatter = indices.scatter_nd(updates, shape=shape)
        >>> print(scatter)
        startai.array([[ 0,  0, 22, 40,  0],
                    [ 0, 21,  0,  0, 25]])
        """
        return startai.scatter_nd(self, updates, shape, reduction=reduction, out=out)

    def gather_nd(
        self: startai.Array,
        indices: Union[startai.Array, startai.NativeArray],
        /,
        *,
        batch_dims: int = 0,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.gather_nd. This method
        simply wraps the function, and so the docstring for startai.gather_nd also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The array from which to gather values.
        indices
            Index array.
        batch_dims
            optional int, lets you gather different items from each element of a batch.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            New array of given shape, with the values gathered at the indices.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([1])
        >>> z = x.gather_nd(y)
        >>> print(z)
        startai.array(2)
        """
        return startai.gather_nd(self, indices, batch_dims=batch_dims, out=out)

    def einops_rearrange(
        self: startai.Array,
        pattern: str,
        /,
        *,
        out: Optional[startai.Array] = None,
        **axes_lengths: Dict[str, int],
    ) -> startai.Array:
        """startai.Array instance method variant of startai.einops_rearrange. This
        method simply wraps the function, and so the docstring for
        startai.einops_rearrange also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array to be re-arranged.
        pattern
            Rearrangement pattern.
        axes_lengths
            Any additional specifications for dimensions.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            New array with einops.rearrange having been applied.

        Examples
        --------
        With :class:`startai.Array` instance method:

        >>> x = startai.array([[1, 2, 3],
        ...               [-4, -5, -6]])
        >>> y = x.einops_rearrange("height width -> width height")
        >>> print(y)
        startai.array([[ 1, -4],
            [ 2, -5],
            [ 3, -6]])

        >>> x = startai.array([[[ 1,  2,  3],
        ...                  [ 4,  5,  6]],
        ...               [[ 7,  8,  9],
        ...                  [10, 11, 12]]])
        >>> y = x.einops_rearrange("c h w -> c (h w)")
        >>> print(y)
        startai.array([[ 1,  2,  3,  4,  5,  6],
            [ 7,  8,  9, 10, 11, 12]])

        >>> x = startai.array([[1, 2, 3, 4, 5, 6]
        ...               [7, 8, 9, 10, 11, 12]])
        >>> y = x.einops_rearrange("c (h w) -> (c h) w", h=2, w=3)
        startai.array([[ 1,  2,  3],
            [ 4,  5,  6],
            [ 7,  8,  9],
            [10, 11, 12]])
        """
        return startai.einops_rearrange(self._data, pattern, out=out, **axes_lengths)

    def einops_reduce(
        self: startai.Array,
        pattern: str,
        reduction: Union[str, Callable],
        /,
        *,
        out: Optional[startai.Array] = None,
        **axes_lengths: Dict[str, int],
    ) -> startai.Array:
        """startai.Array instance method variant of startai.einops_reduce. This method
        simply wraps the function, and so the docstring for startai.einops_reduce
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array to be reduced.
        pattern
            Reduction pattern.
        reduction
            One of available reductions ('min', 'max', 'sum', 'mean', 'prod'), or
            callable.
        axes_lengths
            Any additional specifications for dimensions.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            New array with einops.reduce having been applied.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x = startai.array([[[5, 4],
        ...                 [11, 2]],
        ...                [[3, 5],
        ...                 [9, 7]]])

        >>> reduced = x.einops_reduce('a b c -> b c', 'max')
        >>> print(reduced)
        startai.array([[ 5,  5],
                   [11,  7]])

        With :class:`startai.Array` inputs:

        >>> x = startai.array([[[5, 4, 3],
        ...                 [11, 2, 9]],
        ...                [[3, 5, 7],
        ...                 [9, 7, 1]]])
        >>> reduced = x.einops_reduce('a b c -> a () c', 'min')
        >>> print(reduced)
        startai.array([[[5, 2, 3]],
                   [[3, 5, 1]]])
        """
        return startai.einops_reduce(
            self._data, pattern, reduction, out=out, **axes_lengths
        )

    def einops_repeat(
        self: startai.Array,
        pattern: str,
        /,
        *,
        out: Optional[startai.Array] = None,
        **axes_lengths: Dict[str, int],
    ) -> startai.Array:
        """startai.Array instance method variant of startai.einops_repeat. This method
        simply wraps the function, and so the docstring for startai.einops_repeat
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array to be repeated.
        pattern
            Rearrangement pattern.
        axes_lengths
            Any additional specifications for dimensions.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            New array with einops.repeat having been applied.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x = startai.array([5,4])
        >>> y = x.einops_repeat('a -> a c', c=3)
        >>> print(y)
        startai.array([[5, 5, 5],
                   [4, 4, 4]])

        With :class:`startai.Array` inputs:

        >>> x = startai.array([[5,4],
        ...                [2, 3]])
        >>> y = x.einops_repeat('a b ->  a b c', c=3)
        >>> print(y)
        startai.array([[[5, 5, 5], [4, 4, 4]], [[2, 2, 2], [3, 3, 3]]])
        >>> print(y.shape)
        (2, 2, 3)
        """
        return startai.einops_repeat(self._data, pattern, out=out, **axes_lengths)

    def to_numpy(self: startai.Array, /, *, copy: bool = True) -> np.ndarray:
        """startai.Array instance method variant of startai.to_numpy. This method
        simply wraps the function, and so the docstring for startai.to_numpy also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        copy
            whether to copy the array to a new address or not. Default is ``True``.

        Returns
        -------
        ret
            a numpy array copying all the element of the array ``self``.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x = startai.array([-1, 0, 1])
        >>> y = x.to_numpy()
        >>> print(y)
        [-1  0  1]

        >>> x = startai.array([[-1, 0, 1],[-1, 0, 1], [1,0,-1]])
        >>> y = x.to_numpy()
        >>> print(y)
        [[-1  0  1]
        [-1  0  1]
        [ 1  0 -1]]
        """
        return startai.to_numpy(self, copy=copy)

    def to_list(self: startai.Array, /) -> List:
        """startai.Array instance method variant of startai.to_list. This method simply
        wraps the function, and so the docstring for startai.to_list also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array.

        Returns
        -------
        ret
            A list representation of the input array ``x``.

        Examples
        --------
        With :class:`startai.Array` instance method:

        >>> x = startai.array([0, 1, 2])
        >>> y = x.to_list()
        >>> print(y)
        [0, 1, 2]
        """
        return startai.to_list(self)

    def to_file(
        self: startai.Array, fid: Union[str, bytes, int], sep: str = "", format_: str = "%s"
    ) -> None:
        """startai.Array instance method variant of to_file. Write array to a file
        as text or binary. The data is always written in 'C' order.

        Parameters
        ----------
        self : startai.Array
            Input array.
        fid : str, bytes, int
            An open file object, or a string containing a filename.
        sep : str, optional
            Separator between array items for text output.
            If '', a binary file is written.
        format_ : str, optional
            Format string for text file output.

        Returns
        -------
        None

        Examples
        --------
        With startai.Array instance method:

        >>> x = startai.array([1, 2, 3])
        >>> x.to_file('data.txt', sep=',', format_='%d')

        Notes
        -----
        The data produced by this method can be recovered using
        appropriate methods or functions depending on the data type.
        """
        return startai.to_file(self, fid, sep, format_)

    def supports_inplace_updates(self: startai.Array, /) -> bool:
        """startai.Array instance method variant of startai.supports_inplace_updates.
        This method simply wraps the function, and so the docstring for
        startai.supports_inplace_updates also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            The input array whose elements' data type is to be checked.

        Returns
        -------
        ret
            Bool value depends on whether the currently active backend
            framework supports in-place operations with argument's data type.

        Examples
        --------
        With :class:`startai.Array` input and default backend set as `numpy`:

        >>> x = startai.array([0, 1, 2])
        >>> ret = x.supports_inplace_updates()
        >>> print(ret)
        True

        With `startai.Array` input and backend set as "tensorflow":

        >>> x = startai.array([1., 4.2, 2.2])
        >>> ret = x.supports_inplace_updates()
        >>> print(ret)
        False
        """
        return startai.supports_inplace_updates(self)

    def inplace_decrement(
        self: Union[startai.Array, startai.NativeArray], val: Union[startai.Array, startai.NativeArray]
    ) -> startai.Array:
        """startai.Array instance method variant of startai.inplace_decrement. This
        method simply wraps the function, and so the docstring for
        startai.inplace_decrement also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input array to be decremented by the defined value.
        val
            The value of decrement.

        Returns
        -------
        ret
            The array following an in-place decrement.

        Examples
        --------
        With :class:`startai.Array` instance methods:

        >>> x = startai.array([5.7, 4.3, 2.5, 1.9])
        >>> y = x.inplace_decrement(1)
        >>> print(y)
        startai.array([4.7, 3.3, 1.5, 0.9])

        >>> x = startai.asarray([4., 5., 6.])
        >>> y = x.inplace_decrement(2.5)
        >>> print(y)
        startai.array([1.5, 2.5, 3.5])
        """
        return startai.inplace_decrement(self, val)

    def stable_divide(
        self,
        denominator: Union[Number, startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        min_denominator: Optional[
            Union[Number, startai.Array, startai.NativeArray, startai.Container]
        ] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.stable_divide. This method
        simply wraps the function, and so the docstring for startai.stable_divide
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array, used as the numerator for division.
        denominator
            denominator for division.
        min_denominator
            the minimum denominator to use, use global startai._MIN_DENOMINATOR by default.

        Returns
        -------
        ret
            a numpy array containing the elements of numerator divided by
            the corresponding element of denominator

        Examples
        --------
        With :class:`startai.Array` instance method:

        >>> x = startai.asarray([4., 5., 6.])
        >>> y = x.stable_divide(2)
        >>> print(y)
        startai.array([2., 2.5, 3.])

        >>> x = startai.asarray([4, 5, 6])
        >>> y = x.stable_divide(4, min_denominator=1)
        >>> print(y)
        startai.array([0.8, 1. , 1.2])

        >>> x = startai.asarray([[4., 5., 6.], [7., 8., 9.]])
        >>> y = startai.asarray([[1., 2., 3.], [2., 3., 4.]])
        >>> z = x.stable_divide(y)
        >>> print(z)
        startai.array([[4.  , 2.5 , 2.  ],
                [3.5 , 2.67, 2.25]])
        """
        return startai.stable_divide(self, denominator, min_denominator=min_denominator)

    def clip_vector_norm(
        self: startai.Array,
        max_norm: float,
        /,
        *,
        p: float = 2.0,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.clip_vector_norm. This
        method simply wraps the function, and so the docstring for
        startai.clip_vector_norm also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        max_norm
            float, the maximum value of the array norm.
        p
            optional float, the p-value for computing the p-norm.
            Default is 2.
        out
            optional output array, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            An array with the vector norm downscaled to the max norm if needed.

        Examples
        --------
        With :class:`startai.Array` instance method:

        >>> x = startai.array([0., 1., 2.])
        >>> y = x.clip_vector_norm(2.0)
        >>> print(y)
        startai.array([0., 0.894, 1.79])
        """
        return startai.clip_vector_norm(self, max_norm, p=p, out=out)

    def array_equal(self: startai.Array, x: Union[startai.Array, startai.NativeArray], /) -> bool:
        """startai.Array instance method variant of startai.array_equal. This method
        simply wraps the function, and so the docstring for startai.array_equal
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        x
            input array to compare to ``self``

        Returns
        -------
        ret
            Boolean, whether or not the input arrays are equal

        Examples
        --------
        >>> x = startai.array([-1,0])
        >>> y = startai.array([1,0])
        >>> z = x.array_equal(y)
        >>> print(z)
        False

        >>> a = startai.array([1, 2])
        >>> b = startai.array([1, 2])
        >>> c = a.array_equal(b)
        >>> print(c)
        True

        >>> i = startai.array([1, 2])
        >>> j = startai.array([1, 2, 3])
        >>> k = i.array_equal(j)
        >>> print(k)
        False
        """
        return startai.array_equal(self, x)

    def assert_supports_inplace(self: startai.Array, /) -> bool:
        """startai.Array instance method variant of startai.assert_supports_inplace.
        This method simply wraps the function, and so the docstring for
        startai.assert_supports_inplace also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            input array

        Returns
        -------
        ret
            True if supports, raises StartaiBackendException otherwise

        Examples
        --------
        With :class:`startai.Array` input and default backend set as `torch`:

        >>> startai.set_backend("torch")
        >>> x = startai.array([1, 2, 3])
        >>> print(x.assert_supports_inplace())
        True

        With :class:`startai.Array` input and default backend set as `numpy`:

        >>> startai.set_backend("numpy")
        >>> x = startai.array([1, 2, 3])
        >>> print(x.assert_supports_inplace())
        True
        """
        return startai.assert_supports_inplace(self)

    def to_scalar(self: startai.Array) -> Number:
        """startai.Array instance method variant of startai.to_scalar. This method
        simply wraps the function, and so the docstring for startai.to_scalar also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.

        Returns
        -------
        ret
            a scalar copying the element of the array ``x``.

        Examples
        --------
        With :class:`startai.Array` instance method:

        >>> x = startai.array([3])
        >>> y = x.to_scalar()
        >>> print(y)
        3
        """
        return startai.to_scalar(self)

    def fourier_encode(
        self: startai.Array,
        max_freq: Union[float, startai.Array, startai.NativeArray],
        /,
        *,
        num_bands: int = 4,
        linear: bool = False,
        concat: bool = True,
        flatten: bool = False,
    ) -> Union[startai.Array, startai.NativeArray, Tuple]:
        """startai.Array instance method variant of startai.fourier_encode. This method
        simply wraps the function, and so the docstring for startai.fourier_encode
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array to encode
        max_freq
            The maximum frequency of the encoding.
        num_bands
            The number of frequency bands for the encoding. Default is 4.
        linear
            Whether to space the frequency bands linearly as opposed to geometrically.
            Default is ``False``.
        concat
            Whether to concatenate the position, sin and cos values, or return
            separately. Default is ``True``.
        flatten
            Whether to flatten the position dimension into the batch dimension.
            Default is ``False``.

        Returns
        -------
        ret
            New array with the final dimension expanded, and the encodings stored in
            this channel.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = 1.5
        >>> z = x.fourier_encode(y)
        >>> print(z)
        startai.array([[ 1.0000000e+00, 1.2246468e-16, 0.0000000e+00, 0.0000000e+00,
                     0.0000000e+00, -1.0000000e+00, 1.0000000e+00, 1.0000000e+00,
                     1.0000000e+00],
                   [ 2.0000000e+00, -2.4492936e-16, 0.0000000e+00, 0.0000000e+00,
                     0.0000000e+00, 1.0000000e+00, 1.0000000e+00, 1.0000000e+00,
                     1.0000000e+00],
                   [ 3.0000000e+00, 3.6739404e-16, 0.0000000e+00, 0.0000000e+00,
                     0.0000000e+00, -1.0000000e+00, 1.0000000e+00, 1.0000000e+00,
                     1.0000000e+00]])

        >>> x = startai.array([3, 10])
        >>> y = 2.5
        >>> z = x.fourier_encode(y, num_bands=3)
        >>> print(z)
        startai.array([[ 3.0000000e+00,  3.6739404e-16,  3.6739404e-16,  3.6739404e-16,
                    -1.0000000e+00, -1.0000000e+00, -1.0000000e+00],
                   [ 1.0000000e+01, -1.2246468e-15, -1.2246468e-15, -1.2246468e-15,
                     1.0000000e+00,  1.0000000e+00,  1.0000000e+00]])
        """
        return startai.fourier_encode(
            self,
            max_freq,
            num_bands=num_bands,
            linear=linear,
            concat=concat,
            flatten=flatten,
        )

    def value_is_nan(self: startai.Array, /, *, include_infs: bool = True) -> bool:
        """startai.Array instance method variant of startai.value_is_nan. This method
        simply wraps the function, and so the docstring for startai.value_is_nan
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        include_infs
            Whether to include infs and -infs in the check. Default is ``True``.

        Returns
        -------
        ret
            Boolean as to whether the input value is a nan or not.

        Examples
        --------
        With one :class:`startai.Array` instance method:

        >>> x = startai.array([92])
        >>> y = x.value_is_nan()
        >>> print(y)
        False

        >>> x = startai.array([float('inf')])
        >>> y = x.value_is_nan()
        >>> print(y)
        True

        >>> x = startai.array([float('nan')])
        >>> y = x.value_is_nan()
        >>> print(y)
        True

        >>> x = startai.array([float('inf')])
        >>> y = x.value_is_nan(include_infs=False)
        >>> print(y)
        False
        """
        return startai.value_is_nan(self, include_infs=include_infs)

    def exists(self: startai.Array, /) -> bool:
        """startai.Array instance method variant of startai.exists. This method simply
        wraps the function, and so the docstring for startai.exists also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array.

        Returns
        -------
        ret
            True if input is not None, else False.

        Examples
        --------
        >>> x = startai.array([1, 2, 3, 1.2])
        >>> y = x.exists()
        >>> print(y)
        True

        >>> x = startai.array([])
        >>> y = x.exists()
        >>> print(y)
        True
        """
        return startai.exists(self)

    def default(
        self: startai.Array,
        /,
        default_val: Any,
        *,
        catch_exceptions: bool = False,
        rev: bool = False,
        with_callable: bool = False,
    ) -> Any:
        """startai.Array instance method variant of startai.default. This method simply
        wraps the function, and so the docstring for startai.default also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        default_val
            The default value.
        catch_exceptions
            Whether to catch exceptions from callable x. Default is ``False``.
        rev
            Whether to reverse the input x and default_val. Default is ``False``.
        with_callable
            Whether either of the arguments might be callable functions.
            Default is ``False``.

        Returns
        -------
        ret
            x if x exists (is not None), else default.

        Examples
        --------
        >>> x = startai.array([1, 2, 3, 1.2])
        >>> y = x.default(0)
        >>> print(y)
        startai.array([1. , 2. , 3. , 1.2])
        """
        return startai.default(
            self,
            default_val,
            catch_exceptions=catch_exceptions,
            rev=rev,
            with_callable=with_callable,
        )

    def stable_pow(
        self: startai.Array,
        exponent: Union[Number, startai.Array, startai.NativeArray],
        /,
        *,
        min_base: Optional[float] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.stable_pow. This method
        simply wraps the function, and so the docstring for startai.stable_pow also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array, used as the base.
        exponent
            The exponent number.
        min_base
            The minimum base to use, use global startai.min_base by default.

        Returns
        -------
        ret
            The new item following the numerically stable power.

        Examples
        --------
        With :class:`startai.Array` instance method:

        >>> x = startai.asarray([2, 4])
        >>> y = x.stable_pow(2)
        >>> print(y)
        startai.array([ 4.00004, 16.00008])

        >>> x = startai.asarray([[2., 4.], [6., 8.]])
        >>> y = startai.asarray([2., 4.])
        >>> z = x.stable_pow(y)
        >>> print(z)
        startai.array([[4.00004000e+00, 2.56002560e+02],
                [3.60001200e+01, 4.09602048e+03]])
        """
        return startai.stable_pow(self, exponent, min_base=min_base)

    def inplace_update(
        self: startai.Array,
        val: Union[startai.Array, startai.NativeArray],
        /,
        *,
        ensure_in_backend: bool = False,
        keep_input_dtype: bool = False,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.inplace_update. This method
        simply wraps the function, and so the docstring for startai.inplace_update
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array to update
        val
            The array to update the variable with.
        ensure_in_backend
            Whether to ensure that the `startai.NativeArray` is also inplace updated.
            In cases where it should be, backends which do not natively support inplace
            updates will raise an exception.
        keep_input_dtype
            Whether or not to preserve `x` data type after the update, otherwise `val`
            data type will be applied. Defaults to False.

        Returns
        -------
        ret
            The array following the in-place update.

        Examples
        --------
        With :class:`startai.Array` input and default backend set as `numpy`:

        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([0])
        >>> x.inplace_update(y)
        >>> print(x)
        startai.array([0])

        With :class:`startai.Array` input and default backend set as `numpy`:

        >>> x = startai.array([1, 2, 3], dtype=startai.float32)
        >>> y = startai.array([0, 0, 0], dtype=startai.int32)
        >>> x.inplace_update(y, keep_input_dtype=True)
        >>> print(x)
        startai.array([0., 0., 0.])

        With :class:`startai.Array` input and default backend set as `torch`:

        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([0])
        >>> x.inplace_update(y)
        >>> print(x)
        startai.array([0])

        With :class:`startai.Array` input and default backend set as `jax`:

        >>> x = startai.array([4, 5, 6])
        >>> y = startai.array([1])
        >>> x.inplace_update(y)
        StartaiBackendException: jax: inplace_update: JAX does not natively
        support inplace updates
        """
        return startai.inplace_update(
            self,
            val,
            ensure_in_backend=ensure_in_backend,
            keep_input_dtype=keep_input_dtype,
        )

    def inplace_increment(
        self: startai.Array, val: Union[startai.Array, startai.NativeArray]
    ) -> startai.Array:
        """startai.Array instance method variant of startai.inplace_increment. This
        method wraps the function, and so the docstring for
        startai.inplace_increment also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input array to be incremented by the defined value.
        val
            The value of increment.

        Returns
        -------
        ret
            The array following an in-place increment.

        Examples
        --------
        With :class:`startai.Array` instance methods:

        >>> x = startai.array([5.7, 4.3, 2.5, 1.9])
        >>> y = x.inplace_increment(1)
        >>> print(y)
        startai.array([6.7, 5.3, 3.5, 2.9])

        >>> x = startai.asarray([4., 5., 6.])
        >>> y = x.inplace_increment(2.5)
        >>> print(y)
        startai.array([6.5, 7.5, 8.5])
        """
        return startai.inplace_increment(self, val)

    def clip_matrix_norm(
        self: startai.Array,
        max_norm: float,
        /,
        *,
        p: float = 2.0,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.clip_matrix_norm. This
        method simply wraps the function, and so the docstring for
        startai.clip_matrix_norm also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        max_norm
            The maximum value of the array norm.
        p
            The p-value for computing the p-norm. Default is 2.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            An array with the matrix norm downscaled to the max norm if needed.

        Examples
        --------
        With :class:`startai.Array` instance method:

        >>> x = startai.array([[0., 1., 2.]])
        >>> y = x.clip_matrix_norm(2.0)
        >>> print(y)
        startai.array([[0.   , 0.894, 1.79 ]])
        """
        return startai.clip_matrix_norm(self, max_norm, p=p, out=out)

    def scatter_flat(
        self: startai.Array,
        updates: Union[startai.Array, startai.NativeArray],
        /,
        *,
        size: Optional[int] = None,
        reduction: str = "sum",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.scatter_flat. This method
        simply wraps the function, and so the docstring for startai.scatter_flat
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array containing the indices where the new values will occupy
        updates
            Values for the new array to hold.
        size
            The size of the result. Default is `None`, in which case tensor
            argument out must be provided.
        reduction
            The reduction method for the scatter, one of 'sum', 'min', 'max' or
            'replace'
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            New array of given shape, with the values scattered at the indices.

        Examples
        --------
        With :class:`startai.Array` input:
        >>> indices = startai.array([0, 0, 1, 0, 2, 2, 3, 3])
        >>> updates = startai.array([5, 1, 7, 2, 3, 2, 1, 3])
        >>> size = 8
        >>> out = indices.scatter_flat(updates, size=size)
        >>> print(out)
        startai.array([2, 7, 2, 3, 0, 0, 0, 0])


        With :class:`startai.Array` input:
        >>> indices = startai.array([0, 0, 1, 0, 2, 2, 3, 3])
        >>> updates = startai.array([5, 1, 7, 2, 3, 2, 1, 3])
        >>> out = startai.array([0, 0, 0, 0, 0, 0, 0, 0])
        >>> indices.scatter_flat(updates, out=out)
        >>> print(out)
        startai.array([8, 7, 5, 4, 0, 0, 0, 0])
        """
        return startai.scatter_flat(self, updates, size=size, reduction=reduction, out=out)

    def get_num_dims(self: startai.Array, /, *, as_array: bool = False) -> int:
        """startai.Array instance method variant of startai.shape. This method simply
        wraps the function, and so the docstring for startai.shape also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array to infer the number of dimensions  for
        as_array
            Whether to return the shape as a array, default False.

        Returns
        -------
        ret
            Shape of the array

        Examples
        --------
        >>> x = startai.array([[0.,1.,1.],[1.,0.,0.],[8.,2.,3.]])
        >>> b = x.get_num_dims()
        >>> print(b)
        2

        >>> x = startai.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],\
                            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],\
                            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]])
        >>> b = x.get_num_dims(as_array=False)
        >>> print(b)
        3

        >>> b = x.get_num_dims(as_array=True)
        >>> print(b)
        startai.array(3)
        """
        return startai.get_num_dims(self, as_array=as_array)

    def isin(
        self: startai.Array,
        test_elements: startai.Array,
        /,
        *,
        assume_unique: bool = False,
        invert: bool = False,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.isin. This method simply
        wraps the function, and so the docstring for startai.isin also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array
        test_elements
            values against which to test for each input element
        assume_unique
            If True, assumes both elements and test_elements contain unique elements,
            which can speed up the calculation. Default value is False.
        invert
            If True, inverts the boolean return array, resulting in True values for
            elements not in test_elements. Default value is False.

        Returns
        -------
        ret
            output a boolean array of the same shape as elements that is True for
            elements in test_elements and False otherwise.

        Examples
        --------
        >>> x = startai.array([[10, 7, 4], [3, 2, 1]])
        >>> y = startai.array([1, 2, 3])
        >>> x.isin(y)
        startai.array([[False, False, False], [ True,  True,  True]])

        >>> x = startai.array([3, 2, 1, 0])
        >>> y = startai.array([1, 2, 3])
        >>> x.isin(y, invert=True)
        startai.array([False, False, False,  True])
        """
        return startai.isin(
            self._data, test_elements, assume_unique=assume_unique, invert=invert
        )
