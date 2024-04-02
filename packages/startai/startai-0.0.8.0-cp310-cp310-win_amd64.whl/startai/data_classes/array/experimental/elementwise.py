# global
import abc
from typing import Optional, Union, Tuple, List, Sequence
from numbers import Number

# local
import startai


class _ArrayWithElementWiseExperimental(abc.ABC):
    def amax(
        self: startai.Array,
        /,
        *,
        axis: Optional[Union[int, Sequence[int]]] = None,
        keepdims: bool = False,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.amax. This method simply
        wraps the function, and so the docstring for startai.amax also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        axis
            axis or axes along which maximum values must be computed. By default, the
            maximum value must be computed over the entire array. If a tuple of
            integers, maximum values must be computed over multiple axes.
            Default: ``None``.
        keepdims
            optional boolean, if ``True``, the reduced axes (dimensions) must be
            included in the result as singleton dimensions, and, accordingly, the
            result must be compatible with the input array
            (see `broadcasting<https://data-apis.org/array-api/latest/
            API_specification/broadcasting.html#broadcasting>`_).
            Otherwise, if ``False``, the reduced axes (dimensions)
            must not be included in the result.
            Default: ``False``.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            if the maximum value was computed over the entire array, a zero-dimensional
            array containing the maximum value; otherwise, a non-zero-dimensional array
            containing the maximum values. The returned array must have the same
            data type as ``x``.

        Examples
        --------
        >>> x = startai.array([3., 4., 5.])
        >>> y = x.amax()
        >>> print(y)
        startai.array(5.)

        >>> x = startai.array([[-1, 0, 1], [2, 3, 4]])
        >>> y = x.amax(axis=1)
        >>> print(y)
        startai.array([1,  4])

        >>> x = startai.array([0.1, 1.1, 2.1])
        >>> y = startai.array(0.)
        >>> x.amax(out=y)
        >>> print(y)
        startai.array(2.1)
        """
        return startai.amax(self._data, axis=axis, keepdims=keepdims, out=out)

    def amin(
        self: startai.Array,
        /,
        *,
        axis: Optional[Union[int, Sequence[int]]] = None,
        keepdims: bool = False,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.amin. This method simply
        wraps the function, and so the docstring for startai.amin also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        axis
            axis or axes along which minimum values must be computed. By default, the
            minimum value must be computed over the entire array. If a tuple of
            integers, minimum values must be computed over multiple axes.
            Default: ``None``.
        keepdims
            optional boolean, if ``True``, the reduced axes (dimensions) must be
            included in the result as singleton dimensions, and, accordingly, the
            result must be compatible with the input array
            (see `broadcasting<https://data-apis.org/array-api/latest/
            API_specification/broadcasting.html#broadcasting>`_). Otherwise,
            if ``False``, the reduced axes (dimensions)
            must not be included in the result.
            Default: ``False``.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            if the minimum value was computed over the entire array, a zero-dimensional
            array containing the minimum value; otherwise, a non-zero-dimensional array
            containing the minimum values. The returned array must have the same
            data type as ``x``.

        Examples
        --------
        >>> x = startai.array([3., 4., 5.])
        >>> y = x.amin()
        >>> print(y)
        startai.array(3.)

        >>> x = startai.array([[-1, 0, 1], [2, 3, 4]])
        >>> y = x.amin(axis=1)
        >>> print(y)
        startai.array([-1,  2])

        >>> x = startai.array([0.1, 1.1, 2.1])
        >>> y = startai.array(0.)
        >>> x.amin(out=y)
        >>> print(y)
        startai.array(0.1)
        """
        return startai.amin(self._data, axis=axis, keepdims=keepdims, out=out)

    def lgamma(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.lgamma. This method simply
        wraps the function, and so the docstring for startai.lgamma also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1., 2., 3.])
        >>> y = x.lgamma()
        >>> print(y)
        startai.array([0., 0., 0.69314718])

        >>> x = startai.array([4.5, -4, -5.6])
        >>> x.lgamma(out = x)
        >>> print(x)
        startai.array([2.45373654, inf, -4.6477685 ])
        """
        return startai.lgamma(self._data, out=out)

    def sinc(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.sinc. This method simply
        wraps the function, and so the docstring for startai.sinc also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements are each expressed in radians. Should have a
            floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the sinc of each element in ``self``. The returned
            array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([0.5, 1.5, 2.5, 3.5])
        >>> y = x.sinc()
        >>> print(y)
        startai.array([0.637,-0.212,0.127,-0.0909])
        """
        return startai.sinc(self._data, out=out)

    def fmod(
        self: startai.Array,
        x2: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.fmod. This method simply
        wraps the function, and so the docstring for startai.fmod also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            First input array.
        x2
            Second input array
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Array with element-wise remainder of divisions.

        Examples
        --------
        >>> x1 = startai.array([2, 3, 4])
        >>> x2 = startai.array([1, 5, 2])
        >>> x1.fmod(x2)
        startai.array([ 0,  3,  0])

        >>> x1 = startai.array([startai.nan, 0, startai.nan])
        >>> x2 = startai.array([0, startai.nan, startai.nan])
        >>> x1.fmod(x2)
        startai.array([ nan,  nan,  nan])
        """
        return startai.fmod(self._data, x2, out=out)

    def fmax(
        self: startai.Array,
        x2: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.fmax. This method simply
        wraps the function, and so the docstring for startai.fmax also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            First input array.
        x2
            Second input array
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Array with element-wise maximums.

        Examples
        --------
        >>> x1 = startai.array([2, 3, 4])
        >>> x2 = startai.array([1, 5, 2])
        >>> startai.fmax(x1, x2)
        startai.array([ 2.,  5.,  4.])

        >>> x1 = startai.array([startai.nan, 0, startai.nan])
        >>> x2 = startai.array([0, startai.nan, startai.nan])
        >>> x1.fmax(x2)
        startai.array([ 0,  0,  nan])
        """
        return startai.fmax(self._data, x2, out=out)

    def float_power(
        self: Union[startai.Array, float, list, tuple],
        x2: Union[startai.Array, float, list, tuple],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.float_power. This method
        simply wraps the function, and so the docstring for startai.float_power
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Array-like with elements to raise in power.
        x2
            Array-like of exponents. If x1.shape != x2.shape,
            they must be broadcastable to a common shape
            (which becomes the shape of the output).
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The bases in x1 raised to the exponents in x2.
            This is a scalar if both x1 and x2 are scalars

        Examples
        --------
        >>> x1 = startai.array([1, 2, 3, 4, 5])
        >>> x1.float_power(3)
        startai.array([1.,    8.,   27.,   64.,  125.])
        >>> x1 = startai.array([1, 2, 3, 4, 5])
        >>> x2 = startai.array([2, 3, 3, 2, 1])
        >>> x1.float_power(x2)
        startai.array([1.,   8.,  27.,  16.,   5.])
        """
        return startai.float_power(self._data, x2, out=out)

    def copysign(
        self: Union[startai.Array, startai.NativeArray, Number],
        x2: Union[startai.Array, startai.NativeArray, Number],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.copysign. This method
        simply wraps the function, and so the docstring for startai.copysign also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            Array or scalar to change the sign of
        x2
            Array or scalar from which the new signs are applied
            Unsigned zeroes are considered positive.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            x1 with the signs of x2.
            This is a scalar if both x1 and x2 are scalars.

        Examples
        --------
        >>> x1 = startai.array([0, 1, 2, 3])
        >>> x2 = startai.array([-1, 1, -2, 2])
        >>> x1.copysign(x2)
        startai.array([-0.,  1., -2.,  3.])
        >>> x2.copysign(-1)
        startai.array([-1., -1., -2., -2.])
        """
        return startai.copysign(self._data, x2, out=out)

    def count_nonzero(
        self: startai.Array,
        /,
        *,
        axis: Optional[Union[int, Tuple[int, ...]]] = None,
        keepdims: bool = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.count_nonzero. This method
        simply wraps the function, and so the docstring for startai.count_nonzero
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array for which to count non-zeros.
        axis
            optional axis or tuple of axes along which to count non-zeros. Default is
            None, meaning that non-zeros will be counted along a flattened
            version of the input array.
        keepdims
            optional, if this is set to True, the axes that are counted are left in the
            result as dimensions with size one. With this option, the result
            will broadcast correctly against the input array.
        dtype
            optional output dtype. Default is of type integer.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
           Number of non-zero values in the array along a given axis. Otherwise,
           the total number of non-zero values in the array is returned.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> x.count_nonzero()
        startai.array(3)
        >>> x = startai.array([[[0,1],[2,3]],[[4,5],[6,7]]])
        >>> x.count_nonzero(axis=0)
        startai.array([[1, 2],
               [2, 2]])
        >>> x = startai.array([[[0,1],[2,3]],[[4,5],[6,7]]])
        >>> x.count_nonzero(axis=(0,1), keepdims=True)
        startai.array([[[3, 4]]])
        """
        return startai.count_nonzero(
            self._data, axis=axis, keepdims=keepdims, dtype=dtype, out=out
        )

    def nansum(
        self: startai.Array,
        /,
        *,
        axis: Optional[Union[tuple, int]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
        keepdims: bool = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.nansum. This method simply
        wraps the function, and so the docstring for startai.nansum also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        axis
            Axis or axes along which the sum is computed.
            The default is to compute the sum of the flattened array.
        dtype
            The type of the returned array and of the accumulator in
            which the elements are summed. By default, the dtype of input is used.
        keepdims
            If this is set to True, the axes which are reduced are left
            in the result as dimensions with size one.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            A new array holding the result is returned unless out is specified,
            in which it is returned.

        Examples
        --------
        >>> a = startai.array([[ 2.1,  3.4,  startai.nan], [startai.nan, 2.4, 2.1]])
        >>> startai.nansum(a)
        10.0
        >>> startai.nansum(a, axis=0)
        startai.array([2.1, 5.8, 2.1])
        >>> startai.nansum(a, axis=1)
        startai.array([5.5, 4.5])
        """
        return startai.nansum(
            self._data, axis=axis, dtype=dtype, keepdims=keepdims, out=out
        )

    def isclose(
        self: startai.Array,
        b: startai.Array,
        /,
        *,
        rtol: float = 1e-05,
        atol: float = 1e-08,
        equal_nan: bool = False,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.isclose. This method simply
        wraps the function, and so the docstring for startai.isclose also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            First input array.
        b
            Second input array.
        rtol
            The relative tolerance parameter.
        atol
            The absolute tolerance parameter.
        equal_nan
            Whether to compare NaN's as equal. If True, NaN's in a will be
            considered equal to NaN's in b in the output array.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            A new array holding the result is returned unless out is specified,
            in which it is returned.

        Examples
        --------
        >>> a = startai.array([[ 2.1,  3.4,  startai.nan], [startai.nan, 2.4, 2.1]])
        >>> b = startai.array([[ 2.1,  3.4,  startai.nan], [startai.nan, 2.4, 2.1]])
        >>> a.isclose(b)
        startai.array([[True, True, False],
               [False, True, True]])
        >>> a.isclose(b, equal_nan=True)
        startai.array([[True, True, True],
               [True, True, True]])
        >>> a=startai.array([1.0, 2.0])
        >>> b=startai.array([1.0, 2.001])
        >>> a.isclose(b, atol=0.0)
        startai.array([True, False])
        >>> a.isclose(b, rtol=0.01, atol=0.0)
        startai.array([True, True])
        """
        return startai.isclose(
            self._data, b, rtol=rtol, atol=atol, equal_nan=equal_nan, out=out
        )

    def signbit(
        self: Union[startai.Array, float, int, list, tuple],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.signbit. This method simply
        wraps the function, and so the docstring for startai.signbit also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            Array-like input.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Element-wise signbit of x.

        Examples
        --------
        >>> x = startai.array([1, -2, 3])
        >>> x.signbit()
        startai.array([False, True, False])
        """
        return startai.signbit(self._data, out=out)

    def hypot(
        self: startai.Array,
        x2: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.hypot. This method simply
        wraps the function, and so the docstring for startai.hypot also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            First input array
        x2
            Second input array
        out
            Optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            An array containing the hypotenuse computed from each element of the
            input arrays.

        Examples
        --------
        >>> x = startai.array([3.0, 4.0, 5.0])
        >>> y = startai.array([4.0, 5.0, 6.0])
        >>> x.hypot(y)
        startai.array([5.0, 6.4031, 7.8102])
        """
        return startai.hypot(self._data, x2, out=out)

    def allclose(
        self: startai.Array,
        x2: startai.Array,
        /,
        *,
        rtol: float = 1e-05,
        atol: float = 1e-08,
        equal_nan: bool = False,
        out: Optional[startai.Container] = None,
    ) -> bool:
        """startai.Array instance method variant of startai.allclose. This method
        simply wraps the function, and so the docstring for startai.allclose also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            First input array.
        x2
            Second input array.
        rtol
            The relative tolerance parameter.
        atol
            The absolute tolerance parameter.
        equal_nan
            Whether to compare NaN's as equal. If True, NaN's in a will be
            considered equal to NaN's in b in the output array.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            Returns True if the two arrays are equal within the given tolerance;
            False otherwise.

        Examples
        --------
        >>> x1 = startai.array([1e10, 1e-7])
        >>> x2 = startai.array([1.00001e10, 1e-8])
        >>> y = x1.allclose(x2)
        >>> print(y)
        startai.array(False)

        >>> x1 = startai.array([1.0, startai.nan])
        >>> x2 = startai.array([1.0, startai.nan])
        >>> y = x1.allclose(x2, equal_nan=True)
        >>> print(y)
        startai.array(True)

        >>> x1 = startai.array([1e-10, 1e-10])
        >>> x2 = startai.array([1.00001e-10, 1e-10])
        >>> y = x1.allclose(x2, rtol=0.005, atol=0.0)
        >>> print(y)
        startai.array(True)
        """
        return startai.allclose(
            self._data, x2, rtol=rtol, atol=atol, equal_nan=equal_nan, out=out
        )

    def diff(
        self: startai.Array,
        /,
        *,
        n: int = 1,
        axis: int = -1,
        prepend: Optional[Union[startai.Array, startai.NativeArray, int, list, tuple]] = None,
        append: Optional[Union[startai.Array, startai.NativeArray, int, list, tuple]] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.diff. This method simply
        wraps the function, and so the docstring for startai.diff also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            array-like input.
        n
            The number of times values are differenced. If zero, the input is returned
            as-is.
        axis
            The axis along which the difference is taken, default is the last axis.
        prepend,append
            Values to prepend/append to x along given axis prior to performing the
            difference. Scalar values are expanded to arrays with length 1 in the
            direction of axis and the shape of the input array in along all other
            axes. Otherwise the dimension and shape must match x except along axis.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Returns the n-th discrete difference along the given axis.

        Examples
        --------
        >>> x = startai.array([1, 2, 4, 7, 0])
        >>> x.diff()
        startai.array([ 1,  2,  3, -7])
        """
        return startai.diff(
            self._data, n=n, axis=axis, prepend=prepend, append=append, out=out
        )

    def fix(
        self: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.fix. This method simply
        wraps the function, and so the docstring for startai.fix also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Array input.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Array of floats with elements corresponding to input elements
            rounded to nearest integer towards zero, element-wise.

        Examples
        --------
        >>> x = startai.array([2.1, 2.9, -2.1])
        >>> x.fix()
        startai.array([ 2.,  2., -2.])
        """
        return startai.fix(self._data, out=out)

    def nextafter(
        self: startai.Array,
        x2: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.nextafter. This method
        simply wraps the function, and so the docstring for startai.nextafter also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            First input array.
        x2
            Second input array.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            The next representable values of x1 in the direction of x2.

        Examples
        --------
        >>> x1 = startai.array([1.0e-50, 2.0e+50])
        >>> x2 = startai.array([2.0, 1.0])
        >>> x1.nextafter(x2)
        startai.array([1.4013e-45., 3.4028e+38])
        """
        return startai.nextafter(self._data, x2, out=out)

    def zeta(
        self: startai.Array,
        q: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.zeta. This method simply
        wraps the function, and so the docstring for startai.zeta also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            First input array.
        q
            Second input array.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            Array with values computed from zeta function from
            input arrays' values.

        Examples
        --------
        >>> x = startai.array([5.0, 3.0])
        >>> q = startai.array([2.0])
        >>> x.zeta(q)
        startai.array([0.0369, 0.2021])
        """
        return startai.zeta(self._data, q, out=out)

    def gradient(
        self: Union[startai.Array, startai.NativeArray],
        /,
        *,
        spacing: Union[int, list, tuple] = 1,
        edge_order: int = 1,
        axis: Optional[Union[int, list, tuple]] = None,
    ) -> Union[startai.Array, List[startai.Array]]:
        """Calculate gradient of x with respect to (w.r.t.) spacing.

        Parameters
        ----------
        self
            input array representing outcomes of the function
        spacing
            if not given, indices of x will be used
            if scalar indices of x will be scaled with this value
            if array gradient of x w.r.t. spacing
        edge_order
            1 or 2, for 'first order' and 'second order' estimation
            of boundary values of gradient respectively.
            Note: jax supports edge_order=1 case only
        axis
            dimension(s) to approximate the gradient over
            by default partial gradient is computed in every dimension


        Returns
        -------
        ret
            Array with values computed from gradient function from
            inputs

        Examples
        --------
        >>> spacing = (startai.array([-2., -1., 1., 4.]),)
        >>> x = startai.array([4., 1., 1., 16.], )
        >>> startai.gradient(x, spacing=spacing)
        startai.array([-3., -2.,  2.,  5.])

        >>> x = startai.array([[1, 2, 4, 8], [10, 20, 40, 80]])
        >>> startai.gradient(x)
        [startai.array([[ 9., 18., 36., 72.],
           [ 9., 18., 36., 72.]]), startai.array([[ 1. ,  1.5,  3. ,  4. ],
           [10. , 15. , 30. , 40. ]])]

        >>> x = startai.array([[1, 2, 4, 8], [10, 20, 40, 80]])
        >>> startai.gradient(x, spacing=2.0)
        [startai.array([[ 4.5,  9. , 18. , 36. ],
           [ 4.5,  9. , 18. , 36. ]]), startai.array([[ 0.5 ,  0.75,  1.5 ,  2.  ],
           [ 5.  ,  7.5 , 15.  , 20.  ]])]

        >>> x = startai.array([[1, 2, 4, 8], [10, 20, 40, 80]])
        >>> startai.gradient(x, axis=1)
        startai.array([[ 1. ,  1.5,  3. ,  4. ],
           [10. , 15. , 30. , 40. ]])

        >>> x = startai.array([[1, 2, 4, 8], [10, 20, 40, 80]])
        >>> startai.gradient(x, spacing=[3., 2.])
        [startai.array([[ 3.,  6., 12., 24.],
           [ 3.,  6., 12., 24.]]), startai.array([[ 0.5 ,  0.75,  1.5 ,  2.  ],
           [ 5.  ,  7.5 , 15.  , 20.  ]])]

        >>> spacing = (startai.array([0, 2]), startai.array([0, 3, 6, 9]))
        >>> startai.gradient(x, spacing=spacing)
        [startai.array([[ 4.5,  9. , 18. , 36. ],
           [ 4.5,  9. , 18. , 36. ]]), startai.array([[ 0.33333333,  0.5,  1., 1.33333333],
           [ 3.33333333,  5.        , 10.        , 13.33333333]])]
        """
        return startai.gradient(
            self._data, spacing=spacing, axis=axis, edge_order=edge_order
        )

    def xlogy(
        self: startai.Array,
        y: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.xlogy. This method simply
        wraps the function, and so the docstring for startai.xlogy also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            First input array.
        y
            Second input array.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            The next representable values of x1 in the direction of x2.

        Examples
        --------
        >>> x = startai.zeros(3)
        >>> y = startai.array([-1.0, 0.0, 1.0])
        >>> x.xlogy(y)
        startai.array([0.0, 0.0, 0.0])

        >>> x = startai.array([1.0, 2.0, 3.0])
        >>> y = startai.array([3.0, 2.0, 1.0])
        >>> x.xlogy(y)
        startai.array([1.0986, 1.3863, 0.0000])
        """
        return startai.xlogy(self._data, y, out=out)

    def binarizer(
        self: startai.Array, /, *, threshold: float = 0, out: Optional[startai.Array] = None
    ) -> startai.Array:
        """Map the values of the input tensor to either 0 or 1, element-wise,
        based on the outcome of a comparison against a threshold value.

        Parameters
        ----------
        self
             Data to be binarized
        threshold
             Values greater than this are
             mapped to 1, others to 0.
        out
            optional output array, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            Binarized output data
        """
        return startai.binarizer(self._data, threshold=threshold, out=out)

    def conj(self: startai.Array, /, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.conj. This method simply
        wraps the function, and so the docstring for startai.conj also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        out
            optional output array, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the complex conjugates of values in the input array,
            with the same dtype as the input array.

        Examples
        --------
        >>> x = startai.array([4+3j, 6+2j, 1-6j])
        >>> x.conj()
        startai.array([4-3j, 6-2j, 1+6j])
        """
        return startai.conj(self._data, out=out)

    def lerp(
        self: startai.Array,
        end: startai.Array,
        weight: Union[startai.Array, float],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.lerp. This method simply
        wraps the function, and so the docstring for startai.lerp also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Array of starting points
        end
            Array of ending points
        weight
            Weight for the interpolation formula  , array or scalar.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            The linear interpolation between array self and array end based on
            scalar or array weight
            self + ((end - self) * weight)

        Examples
        --------
        >>> x = startai.array([1.0, 2.0, 3.0, 4.0])
        >>> end = startai.array([10.0, 10.0, 10.0, 10.0])
        >>> weight = 0.5
        >>> x.lerp(end, weight)
        startai.array([5.5, 6. , 6.5, 7. ])
        """
        return startai.lerp(self, end, weight, out=out)

    def ldexp(
        self: startai.Array,
        x2: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.ldexp. This method simply
        wraps the function, and so the docstring for startai.ldexp also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        x2
            The array of exponents.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            The next representable values of x1 in the direction of x2.

        Examples
        --------
        >>> x = startai.array([1.0, 2.0, 3.0])
        >>> y = startai.array([3.0, 2.0, 1.0])
        >>> x.ldexp(y)
        startai.array([8.0, 8.0, 6.0])
        """
        return startai.ldexp(self._data, x2, out=out)

    def frexp(
        self: startai.Array, /, *, out: Optional[Tuple[startai.Array, startai.Array]] = None
    ) -> startai.Array:
        """startai.Array instance method variant of startai.frexp. This method simply
        wraps the function, and so the docstring for startai.frexp also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            The next representable values of x1 in the direction of x2.

        Examples
        --------
        >>> x = startai.array([1.0, 2.0, 3.0])
        >>> x.frexp()
        startai.array([[0.5, 0.5, 0.75], [1, 2, 2]])
        """
        return startai.frexp(self._data, out=out)

    def modf(
        self: startai.Array, /, *, out: Optional[Tuple[startai.Array, startai.Array]] = None
    ) -> Tuple[startai.Array, startai.Array]:
        """startai.Array instance method variant of startai.modf. This method simply
        wraps the function, and so the docstring for startai.modf also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        out
            Alternate output arrays in which to place the result.
            The default is None.

        Returns
        -------
        ret
            The fractional and integral parts of the input array.

        Examples
        --------
        >>> x = startai.array([1.5, 2.7, 3.9])
        >>> x.modf()
        (startai.array([0.5, 0.7, 0.9]), startai.array([1, 2, 3]))
        """
        return startai.modf(self._data, out=out)

    def digamma(
        self: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.digamma. This method simply
        wraps the function, and so the docstring for startai.digamma also applies
        to this method with minimal changes.

        Note
        ----
        The Startai version only accepts real-valued inputs.

        Parameters
        ----------
        self
            Input array.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            Array with values computed from digamma function from
            input arrays' values, element-wise.

        Examples
        --------
        >>> x = startai.array([.9, 3, 3.2])
        >>> y = startai.digamma(x)
        startai.array([-0.7549271   0.92278427  0.9988394])
        """
        return startai.digamma(self._data, out=out)

    def sparsify_tensor(
        self: startai.Array,
        card: int,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array class method variant of startai.sparsify_tensor. This method
        simply wraps the function, and so the docstring for startai.sparsify_tensor
        also applies to this method with minimal changes.

        Parameters
        ----------
        self : array
            The tensor to sparsify.
        card : int
            The number of values to keep.
        out : array, optional
            Optional output array, for writing the result to.

        Returns
        -------
        ret : array
            The sparsified tensor.

        Examples
        --------
        >>> x = startai.arange(100)
        >>> x = startai.reshape(x, (10, 10))
        >>> x.sparsify_tensor(10)
        startai.array([[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]])
        """
        return startai.sparsify_tensor(self._data, card, out=out)

    def erfc(
        self: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.erfc. This method simply
        wraps the function, and so the docstring for startai.erfc also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array with real or complex valued argument.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            Values of the complementary error function.

        Examples
        --------
        >>> x = startai.array([0, -1., 10.])
        >>> x.erfc()
        startai.array([1.00000000e+00, 1.84270084e+00, 2.80259693e-45])
        """
        return startai.erfc(self._data, out=out)

    def erfinv(
        self: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.erfinv. This method simply
        wraps the function, and so the docstring for startai.erfinv also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array with real or complex valued argument.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            Values of the inverse error function.

        Examples
        --------
        >>> x = startai.array([0, -1., 10.])
        >>> x.erfinv()
        startai.array([1.00000000e+00, 1.84270084e+00, 2.80259693e-45])
        """
        return startai.erfinv(self._data, out=out)
