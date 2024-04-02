# local
from typing import Optional, Union, Tuple, List, Sequence
from numbers import Number
import startai
from startai.func_wrapper import (
    handle_out_argument,
    to_native_arrays_and_back,
    handle_nestable,
    handle_partial_mixed_function,
    handle_array_like_without_promotion,
    inputs_to_startai_arrays,
    handle_array_function,
    infer_dtype,
    handle_device,
    handle_backend_invalid,
)
from startai.utils.exceptions import handle_exceptions


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def amax(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Calculate the maximum value of the input array ``x``.

    .. note::
       ``amax`` is an alias of ``max`` and both function
       behaves similarly in every backend except PyTorch and PaddlePaddle
       (see `PyTorch's amax function
       documentation<https://pytorch.org/docs/stable/generated/torch.amax.html>`_`)
       (see `PaddlePaddle's amax function documentation<https://www.paddlepaddle.org.cn/
       documentation/docs/zh/api/paddle/amax_cn.html>`_`)

    .. note::
       When the number of elements over which to compute the maximum value is zero, the
       maximum value is implementation-defined. Specification-compliant libraries may
       choose to raise an error, return a sentinel value (e.g., if ``x`` is a
       floating-point input array, return ``NaN``), or return the minimum possible
       value for the input array ``x`` data type (e.g., if ``x`` is a floating-point
       array, return ``-infinity``).

    **Special Cases**

    For floating-point operands,

    -   If ``x_i`` is ``NaN``, the maximum value is ``NaN``
        (i.e., ``NaN`` values propagate).

    Parameters
    ----------
    x
        input array. Should have a real-valued data type.
    axis
        axis or axes along which maximum values must be computed. By default, the
        maximum value must be computed over the entire array. If a tuple of integers,
        maximum values must be computed over multiple axes. Default: ``None``.
    keepdims
        optional boolean, if ``True``, the reduced axes (dimensions) must be included
        in the result as singleton dimensions, and, accordingly, the result must be
        compatible with the input array (see `broadcasting<https://data-apis.org/
        array-api/latest/API_specification/broadcasting.html#broadcasting>`_).
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
        containing the maximum values. The returned array must have the same data type
        as ``x``.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.max.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1, 2, 3])
    >>> y = startai.amax(x)
    >>> print(y)
    startai.array(3)

    >>> x = startai.array([0, 1, 2])
    >>> z = startai.array([0, 0, 0])
    >>> y = startai.amax(x, out=z)
    >>> print(z)
    startai.array(2)

    >>> x = startai.array([[0, 1, 2], [4, 6, 10]])
    >>> y = startai.amax(x, axis=0, keepdims=True)
    >>> print(y)
    startai.array([[4, 6, 10]])

    >>> x = startai.native_array([[0, 1, 2], [4, 6, 10]])
    >>> y = startai.amax(x)
    >>> print(y)
    startai.array(10)

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([2, 3, 4]))
    >>> y = startai.amax(x)
    >>> print(y)
    {
        a: startai.array(3),
        b: startai.array(4)
    }
    """
    return startai.current_backend(x).amax(x, axis=axis, keepdims=keepdims, out=out)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def amin(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Calculate the minimum value of the input array ``x``.

    .. note::
       ``amin`` is an alias of ``min`` and both function
       behaves similarly in every backend except PyTorch and PaddlePaddle
       (see `PyTorch's amin function
       documentation<https://pytorch.org/docs/stable/generated/torch.amin.html>`_`)
       (see `PaddlePaddle's amin function documentation<https://www.paddlepaddle.org.cn/
       documentation/docs/zh/api/paddle/amin_cn.html>`_`)

    .. note::
       When the number of elements over which to compute the minimum value is zero, the
       minimum value is implementation-defined. Specification-compliant libraries may
       choose to raise an error, return a sentinel value (e.g., if ``x`` is a
       floating-point input array, return ``NaN``), or return the maximum possible value
       for the input array ``x`` data type (e.g., if ``x`` is a floating-point array,
       return ``+infinity``).

    **Special Cases**

    For floating-point operands,

    -   If ``x_i`` is ``NaN``, the minimum value is ``NaN``
        (i.e., ``NaN`` values propagate).

    Parameters
    ----------
    x
        input array. Should have a real-valued data type.
    axis
        axis or axes along which minimum values must be computed. By default, the
        minimum value must be computed over the entire array. If a tuple of integers,
        minimum values must be computed over multiple axes. Default: ``None``.

    keepdims
        optional boolean, if ``True``, the reduced axes (dimensions) must be included
        in the result as singleton dimensions, and, accordingly, the result must be
        compatible with the input array (see `broadcasting<https://data-apis.org/
        array-api/latest/API_specification/broadcasting.html#broadcasting>`_).
        Otherwise, if ``False``, the reduced axes (dimensions)
        must not be included in the result.
        Default: ``False``.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        if the minimum value was computed over the entire array, a zero-dimensional
        array containing the minimum value; otherwise, a non-zero-dimensional array
        containing the minimum values. The returned array must have the same data type
        as ``x``.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.min.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1, 2, 3])
    >>> y = startai.amin(x)
    >>> print(y)
    startai.array(1)

    >>> x = startai.array([0, 1, 2])
    >>> z = startai.array([0, 0, 0])
    >>> y = startai.amin(x, out=z)
    >>> print(z)
    startai.array(0)

    >>> x = startai.array([[0, 1, 2], [4, 6, 10]])
    >>> y = startai.amin(x, axis=0, keepdims=True)
    >>> print(y)
    startai.array([[0, 1, 2]])

    >>> x = startai.native_array([[0, 1, 2], [4, 6, 10]])
    >>> y = startai.amin(x)
    >>> print(y)
    startai.array(0)

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([2, 3, 4]))
    >>> y = startai.amin(x)
    >>> print(y)
    {
        a: startai.array(1),
        b: startai.array(2)
    }
    """
    return startai.current_backend(x).amin(x, axis=axis, keepdims=keepdims, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
def lgamma(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute the natural logarithm of the absolute value of the gamma
    function on x.

    Parameters
    ----------
    x
        input array. Should have a floating-point data type.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the natural log of Gamma(x) of each element in x.
        The returned array must have a floating-point data type determined
        by :ref:`type-promotion`.

    Examples
    --------
    >>> x = startai.array([1.6, 2.6, 3.5])
    >>> y = x.lgamma()
    >>> print(y)
    startai.array([-0.11259177,  0.3574118 ,  1.20097363])

    >>> x = startai.array([1., 2., 3. ])
    >>> y = x.lgamma()
    >>> print(y)
    startai.array([0. ,0. ,0.69314718])

    >>> x = startai.array([4.5, -4, -5.6])
    >>> x.lgamma(out = x)
    >>> print(x)
    startai.array([2.45373654, inf, -4.6477685 ])
    """
    return startai.current_backend(x).lgamma(x, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def sinc(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Calculate an implementation-dependent approximation of the principal
    value of the normalized sinc function, having domain ``(-infinity,
    +infinity)`` and codomain ``[-0.217234, 1]``, for each element ``x_i`` of
    the input array ``x``. Each element ``x_i`` is assumed to be expressed in
    radians.

    **Special cases**

    For floating-point operands,

    - If x_i is NaN, the result is NaN.
    - If ``x_i`` is ``0``, the result is ``1``.
    - If ``x_i`` is either ``+infinity`` or ``-infinity``, the result is ``NaN``.

    Parameters
    ----------
    x
        input array. Should have a floating-point data type.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the normalized sinc function of each element in x.
        The returned array must have a floating-point data type determined
        by :ref:`type-promotion`.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0.5, 1.5, 2.5, 3.5])
    >>> y = x.sinc()
    >>> print(y)
    startai.array([0.637,-0.212,0.127,-0.0909])

    >>> x = startai.array([1.5, 0.5, -1.5])
    >>> y = startai.zeros(3)
    >>> startai.sinc(x, out=y)
    >>> print(y)
    startai.array([-0.212,0.637,-0.212])

    With :class:`startai.NativeArray` input:

    >>> x = startai.array([0.5, 1.5, 2.5, 3.5])
    >>> y = startai.sinc(x)
    >>> print(y)
    startai.array([0.637,-0.212,0.127,-0.0909])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0.5, 1.5, 2.5]),
    ...                   b=startai.array([3.5, 4.5, 5.5]))
    >>> y = x.sinc()
    >>> print(y)
    {
        a: startai.array([0.637,-0.212,0.127]),
        b: startai.array([-0.0909,0.0707,-0.0579])
    }
    """
    return startai.current_backend(x).sinc(x, out=out)


@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def fmax(
    x1: Union[startai.Array, startai.NativeArray],
    x2: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> Union[startai.Array, startai.NativeArray]:
    """Compute the element-wise maximums of two arrays. Differs from
    startai.maximum in the case where one of the elements is NaN. startai.maximum
    returns the NaN element while startai.fmax returns the non-NaN element.

    Parameters
    ----------
    x1
        First input array.
    x2
        Second input array.
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
    >>> startai.fmax(x1, x2)
    startai.array([ 0.,  0.,  nan])
    """
    return startai.current_backend().fmax(x1, x2, out=out)


@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def float_power(
    x1: Union[startai.Array, float, list, tuple],
    x2: Union[startai.Array, float, list, tuple],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Raise each base in x1 to the positionally-corresponding power in x2. x1
    and x2 must be broadcastable to the same shape. This differs from the power
    function in that integers, float16, and float32 are promoted to floats with
    a minimum precision of float64 so that the result is always inexact.

    Parameters
    ----------
    x1
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
    >>> startai.float_power(x1, 3)
    startai.array([1.,    8.,   27.,   64.,  125.])
    >>> x1 = startai.array([1, 2, 3, 4, 5])
    >>> x2 = startai.array([2, 3, 3, 2, 1])
    >>> startai.float_power(x1, x2)
    startai.array([1.,   8.,  27.,  16.,   5.])
    """
    return startai.current_backend().float_power(x1, x2, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def copysign(
    x1: Union[startai.Array, startai.NativeArray, Number],
    x2: Union[startai.Array, startai.NativeArray, Number],
    /,
    *,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> startai.Array:
    """Change the signs of x1 to match x2 x1 and x2 must be broadcastable to a
    common shape.

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
    >>> x1 = startai.array([-1, 0, 23, 2])
    >>> x2 = startai.array([1, -1, -10, 44])
    >>> startai.copysign(x1, x2)
    startai.array([  1.,  -0., -23.,   2.])
    >>> startai.copysign(x1, -1)
    startai.array([ -1.,  -0., -23.,  -2.])
    >>> startai.copysign(-10, 1)
    startai.array(10.)
    """
    return startai.current_backend().copysign(x1, x2, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@to_native_arrays_and_back
@infer_dtype
@handle_device
def count_nonzero(
    a: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[Union[int, Tuple[int, ...]]] = None,
    keepdims: bool = False,
    dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> startai.Array:
    """Count the number of non-zero values in the array a.

    Parameters
    ----------
    a
        array for which to count non-zeros.
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
    >>> a = startai.array([[0, 1, 2, 3],[4, 5, 6, 7]])
    >>> startai.count_nonzero(a)
    startai.array(7)
    >>> a = startai.array([[0, 1, 2, 3],[4, 5, 6, 7]])
    >>> startai.count_nonzero(a, axis=0)
    startai.array([1, 2, 2, 2])
    >>> a = startai.array([[[0,1],[2,3]],[[4,5],[6,7]]])
    >>> startai.count_nonzero(a, axis=(0,1), keepdims=True)
    startai.array([[[3, 4]]])
    """
    return startai.current_backend().count_nonzero(
        a, axis=axis, keepdims=keepdims, dtype=dtype, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@infer_dtype
@handle_device
def nansum(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[Union[Tuple[int, ...], int]] = None,
    dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
    keepdims: bool = False,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return the sum of array elements over a given axis treating Not a
    Numbers (NaNs) as zero.

    Parameters
    ----------
    x
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
    return startai.current_backend().nansum(
        x, axis=axis, dtype=dtype, keepdims=keepdims, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def isclose(
    a: Union[startai.Array, startai.NativeArray],
    b: Union[startai.Array, startai.NativeArray],
    /,
    *,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return a boolean array where two arrays are element-wise equal within a
    tolerance.

    The tolerance values are positive, typically very small numbers.
    The relative difference (rtol * abs(b)) and the absolute difference
    atol are added together to compare against the absolute difference
    between a and b.
    The default atol is not appropriate for comparing numbers that are
    much smaller than one

    Parameters
    ----------
    a
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
        Returns a boolean array of where a and b are equal within the given
        tolerance. If both a and b are scalars, returns a single boolean value.

    Examples
    --------
    >>> startai.isclose([1e10,1e-7], [1.00001e10,1e-8])
    startai.array([True, False])
    >>> startai.isclose([1.0, startai.nan], [1.0, startai.nan], equal_nan=True)
    startai.array([True, True])
    >>> startai.isclose([1e-100, 1e-7], [0.0, 0.0], atol=0.0)
    startai.array([False, False])
    >>> startai.isclose([1e-10, 1e-10], [1e-20, 0.999999e-10], rtol=0.005, atol=0.0)
    startai.array([False, True])
    """
    return startai.current_backend().isclose(
        a, b, rtol=rtol, atol=atol, equal_nan=equal_nan, out=out
    )


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def signbit(
    x: Union[startai.Array, startai.NativeArray, float, int, list, tuple],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return element-wise True where signbit is set (less than zero).

    Parameters
    ----------
    x
        Array-like input.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Output array, or reference to out if that was supplied.
        This is a scalar if x is a scalar.

    Examples
    --------
    >>> x = startai.array([1, -2, 3])
    >>> startai.signbit(x)
    startai.array([False, True, False])
    """
    return startai.current_backend(x).signbit(x, out=out)


@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def hypot(
    x1: Union[startai.Array, startai.NativeArray],
    x2: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> Union[startai.Array, startai.NativeArray]:
    """Return the hypotenuse given the two sides of a right angle triangle.

    Parameters
    ----------
    x1
        The first input array
    x2
        The second input array

    Returns
    -------
    ret
        An array with the hypotenuse

    Examples
    --------
    >>> a = startai.array([3.0, 4.0, 5.0])
    >>> b = startai.array([4.0, 5.0, 6.0])
    >>> startai.hypot(a, b)
    startai.array([5.0, 6.4031, 7.8102])
    """
    return startai.current_backend(x1, x2).hypot(x1, x2, out=out)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def diff(
    x: Union[startai.Array, startai.NativeArray, list, tuple],
    /,
    *,
    n: int = 1,
    axis: int = -1,
    prepend: Optional[Union[startai.Array, startai.NativeArray, int, list, tuple]] = None,
    append: Optional[Union[startai.Array, startai.NativeArray, int, list, tuple]] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return the n-th discrete difference along the given axis.

    Parameters
    ----------
    x
        Array-like input.
    n
        The number of times values are differenced. If zero, the input is returned
        as-is.
    axis
        The axis along which the difference is taken, default is the last axis.
    prepend,append
        Values to prepend/append to x along given axis prior to performing the
        difference. Scalar values are expanded to arrays with length 1 in the direction
        of axis and the shape of the input array in along all other axes. Otherwise the
        dimension and shape must match x except along axis.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Returns the n-th discrete difference along the given axis.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    >>> x = startai.array([1, 2, 4, 7, 0])
    >>> startai.diff(x)
    startai.array([ 1,  2,  3, -7])
    """
    return startai.current_backend().diff(
        x, n=n, axis=axis, prepend=prepend, append=append, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@to_native_arrays_and_back
@handle_device
def allclose(
    a: Union[startai.Array, startai.NativeArray],
    b: Union[startai.Array, startai.NativeArray],
    /,
    *,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
    out: Optional[startai.Array] = None,
) -> bool:
    """Return a True if the two arrays are element-wise equal within given
    tolerance; otherwise False.

    The tolerance values are positive, typically very small numbers.
    The relative difference (rtol * abs(x2)) and the absolute difference
    atol are added together to compare against the absolute difference
    between x1 and x2.
    The default atol is not appropriate for comparing numbers that are
    much smaller than one

    Parameters
    ----------
    x1
        First input array.
    x2
        Second input array.
    rtol
        The relative tolerance parameter.
    atol
        The absolute tolerance parameter.
    equal_nan
        Whether to compare NaN's as equal. If True, NaN's in x1 will be
        considered equal to NaN's in x2 in the output array.
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
    >>> y = startai.allclose(x1, x2)
    >>> print(y)
    startai.array(False)

    >>> x1 = startai.array([1.0, startai.nan])
    >>> x2 = startai.array([1.0, startai.nan])
    >>> y = startai.allclose(x1, x2, equal_nan=True)
    >>> print(y)
    startai.array(True)

    >>> x1 = startai.array([1e-10, 1e-10])
    >>> x2 = startai.array([1.00001e-10, 1e-10])
    >>> y = startai.allclose(x1, x2, rtol=0.005, atol=0.0)
    >>> print(y)
    startai.array(True)
    """
    return startai.current_backend().allclose(
        a, b, rtol=rtol, atol=atol, equal_nan=equal_nan, out=out
    )


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def fix(
    x: Union[startai.Array, startai.NativeArray, float, int, list, tuple],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Round an array of floats element-wise to nearest integer towards zero.
    The rounded values are returned as floats.

    Parameters
    ----------
    x
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
    >>> startai.fix(x)
    startai.array([ 2.,  2., -2.])
    """
    return startai.current_backend(x).fix(x, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def nextafter(
    x1: Union[startai.Array, startai.NativeArray],
    x2: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> bool:
    """Return the next floating-point value after x1 towards x2, element-wise.

    Parameters
    ----------
    x1
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
    >>> startai.nextafter(x1, x2)
    startai.array([1.4013e-45., 3.4028e+38])
    """
    return startai.current_backend(x1, x2).nextafter(x1, x2, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def zeta(
    x: Union[startai.Array, startai.NativeArray],
    q: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> bool:
    """Compute the Hurwitz zeta function elementwisely with each pair of floats
    in two arrays.

    Parameters
    ----------
    x
        First input array.
    q
        Second input array, must have the same shape as the first input array
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
    >>> q = startai.array([2.0, 2.0])
    >>> startai.zeta(x, q)
    startai.array([0.0369, 0.2021])
    """
    return startai.current_backend(x, q).zeta(x, q, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@to_native_arrays_and_back
@handle_device
def gradient(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    spacing: Union[int, list, tuple] = 1,
    edge_order: int = 1,
    axis: Optional[Union[int, list, tuple]] = None,
) -> Union[startai.Array, List[startai.Array]]:
    """Calculate gradient of x with respect to (w.r.t.) spacing.

    Parameters
    ----------
    x
        input array representing outcomes of the function
    spacing
        if not given, indices of x will be used
        if scalar indices of x will be scaled with this value
        if array gradient of x w.r.t. spacing
    edge_order
        1 or 2, for 'frist order' and 'second order' estimation
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
       [ 4.5,  9. , 18. , 36. ]]), startai.array([[ 0.33333333, 0.5,  1., 1.33333333],
       [ 3.33333333,  5.        , 10.        , 13.33333333]])]
    """
    return startai.current_backend(x).gradient(
        x, spacing=spacing, edge_order=edge_order, axis=axis
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def xlogy(
    x: Union[startai.Array, startai.NativeArray],
    y: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> bool:
    """Compute x*log(y) element-wise so that the result is 0 if x = 0.

    Parameters
    ----------
    x
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
    >>> startai.xlogy(x, y)
    startai.array([0.0, 0.0, 0.0])

    >>> x = startai.array([1.0, 2.0, 3.0])
    >>> y = startai.array([3.0, 2.0, 1.0])
    >>> startai.xlogy(x, y)
    startai.array([1.0986, 1.3863, 0.0000])
    """
    return startai.current_backend(x, y).xlogy(x, y, out=out)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@inputs_to_startai_arrays
def binarizer(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    threshold: float = 0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Map the values of the input tensor to either 0 or 1, element-wise, based
    on the outcome of a comparison against a threshold value.

    Parameters
    ----------
    x
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
    xc = startai.copy_array(x, out=out)
    if startai.is_bool_dtype(xc) and startai.current_backend_str() == "torch":
        xc = startai.astype(xc, startai.default_float_dtype())
    if startai.is_complex_dtype(xc):
        xc = startai.abs(xc)
    ret = startai.where(xc > threshold, 1, 0)
    return ret


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def conj(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return the complex conjugate for each element ``x_i`` of the input array
    ``x``.

    For complex number of the form

    .. math::
        a + bj

    the complex conjugate is defined as

    .. math::
        a - bj

    Hence, the returned conjugates must be computed by negating
    the imaginary component of each element ``x_i``

    This method conforms to the
    `Array API Standard <https://data-apis.org/array-api/latest/>`_.
    This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.conj.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Parameters
    ----------
    x
        input array.
    out
        optional output array, for writing the result to.
        It must have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        an array of the same dtype as the input array with
        the complex conjugates of the complex values present
        in the input array. If x is a scalar then a scalar
        will be returned.

    The descriptions above assume an array input for simplicity, but
    the method also accepts :class:`startai.Container` instances
    in place of: class:`startai.Array` or :class:`startai.NativeArray`
    instances, as shown in the type hints and also the examples below.


    Examples
    --------
    With :class:`startai.Array` inputs:
    >>> x = startai.array([4.2-0j, 3j, 7+5j])
    >>> z = startai.conj(x)
    >>> print(z)
    startai.array([4.2-0.j, 0. -3.j, 7. -5.j])

    With :class:`startai.Container` input:
    >>> x = startai.Container(a=startai.array([-6.7-7j, 0.314+0.355j, 1.23]),
    ...                   b=startai.array([5j, 5.32-6.55j, 3.001]))
    >>> z = startai.conj(x)
    >>> print(z)
    {
        a: startai.array([-6.7+7.j, 0.314-0.355j, 1.23-0.j]),
        b: startai.array([0.-5.j, 5.32+6.55j, 3.001-0.j])
    }
    """
    return startai.current_backend(x).conj(x, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def ldexp(
    x1: Union[startai.Array, startai.NativeArray],
    x2: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return x1 * (2**x2), element-wise.

    Parameters
    ----------
    x1
        Input array.
    x2
        Input array.
    out
        optional output array, for writing the result to.
        It must have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        The next representable values of x1 in the direction of x2.

    Examples
    --------
    >>> x1 = startai.array([1, 2, 3])
    >>> x2 = startai.array([0, 1, 2])
    >>> startai.ldexp(x1, x2)
    startai.array([1, 4, 12])
    """
    return startai.current_backend(x1, x2).ldexp(x1, x2, out=out)


@handle_exceptions
@handle_nestable
@handle_partial_mixed_function
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def lerp(
    input: Union[startai.Array, startai.NativeArray],
    end: Union[startai.Array, startai.NativeArray],
    weight: Union[startai.Array, startai.NativeArray, float],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return a linear interpolation of two arrays start (given by input) and
    end.

    based on a scalar or array weight.
        input + weight * (end - input),  element-wise.

    Parameters
    ----------
    input
        array of starting points
    end
        array of ending points
    weight
        the weight for the interpolation formula. Scalar or Array.
    out
        optional output array, for writing the result to.
        It must have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        The result of  input + ((end - input) * weight)

    Examples
    --------
    With :class:`startai.Array` inputs:
    >>> input = startai.array([1, 2, 3])
    >>> end = startai.array([10, 10, 10])
    >>> weight = 0.5
    >>> y = startai.lerp(input, end, weight)
    >>> print(y)
    startai.array([5.5, 6. , 6.5])

    >>> input = startai.array([1.1, 1.2, 1.3])
    >>> end = startai.array([20])
    >>> weight = startai.array([0.4, 0.5, 0.6])
    >>> y = startai.zeros(3)
    >>> startai.lerp(input, end, weight, out=y)
    >>> print(y)
    startai.array([ 8.65999985, 10.60000038, 12.52000046])

    >>> input = startai.array([[4, 5, 6],[4.1, 4.2, 4.3]])
    >>> end = startai.array([10])
    >>> weight = startai.array([0.5])
    >>> startai.lerp(input, end, weight, out=input)
    >>> print(input)
    startai.array([[7.        , 7.5       , 8.        ],
           [7.05000019, 7.0999999 , 7.1500001 ]])

    With :class:`startai.Container` input:
    >>> input = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.]))
    >>> end = startai.array([10.])
    >>> weight = 1.1
    >>> y = input.lerp(end, weight)
    >>> print(y)
    {
        a: startai.array([11., 10.90000057, 10.80000019]),
        b: startai.array([10.70000076, 10.60000038, 10.5])
    }

    >>> input = startai.Container(a=startai.array([10.1, 11.1]), b=startai.array([10, 11]))
    >>> end = startai.Container(a=startai.array([5]), b=startai.array([0]))
    >>> weight = 0.5
    >>> y = input.lerp(end, weight)
    >>> print(y)
    {
        a: startai.array([7.55000019, 8.05000019]),
        b: startai.array([5., 5.5])
    }
    """
    input_end_allowed_types = [
        "int8",
        "int16",
        "int32",
        "int64",
        "float16",
        "bfloat16",
        "float32",
        "float64",
        "complex",
    ]
    weight_allowed_types = ["float16", "bfloat16", "float32", "float64"]

    if not startai.is_array(input):
        input = startai.array([input])
    if not startai.is_array(end):
        end = startai.array([end])
    if (
        startai.dtype(input) not in input_end_allowed_types
        or startai.dtype(end) not in input_end_allowed_types
    ):
        input = startai.astype(input, "float64")
        end = startai.astype(end, "float64")

    if startai.is_array(weight):
        if startai.dtype(weight) not in weight_allowed_types:
            weight = startai.astype(weight, "float64")
    elif not isinstance(weight, float):
        weight = startai.astype(startai.array([weight]), "float64")

    return startai.add(input, startai.multiply(weight, startai.subtract(end, input)), out=out)


lerp.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays", "handle_partial_mixed_function"),
}


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def frexp(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[Tuple[startai.Array, startai.Array]] = None,
) -> Tuple[startai.Array, startai.Array]:
    """Decompose the elements of x into mantissa and twos exponent.

    Parameters
    ----------
    x
        Input array.
    out
        optional output array, for writing the result to.
        It must have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        A tuple of two arrays, the mantissa and the twos exponent.

    Examples
    --------
    >>> x = startai.array([1, 2, 3])
    >>> startai.frexp(x)
    (startai.array([0.5, 0.5, 0.75]), startai.array([1, 2, 2]))
    """
    return startai.current_backend(x).frexp(x, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
def modf(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[Tuple[startai.Array, startai.Array]] = None,
) -> Tuple[startai.Array, startai.Array]:
    """Decompose the elements of x into fractional and integral parts.

    Parameters
    ----------
    x
        Input array.
    out
        Optional output array for writing the result to.
        It must have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        A tuple of two arrays, the fractional and integral parts.

    Examples
    --------
    >>> x = startai.array([1.5, 2.7, 3.9])
    >>> startai.modf(x)
    (startai.array([0.5, 0.7, 0.9]), startai.array([1, 2, 3]))
    """
    return startai.current_backend(x).modf(x, out=out)


@handle_exceptions
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
def digamma(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute the logarithmic derivative of the gamma function at x.

    Note
    ----
    The Startai version only accepts real-valued inputs.

    Parameters
    ----------
    x
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
    return startai.current_backend(x).digamma(x, out=out)


@handle_exceptions
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
def sparsify_tensor(
    x: Union[startai.Array, startai.NativeArray],
    card: int,
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Zeros out all elements in the tensor except `card` elements with maximum
    absolute values.

    Parameters
    ----------
    x
        Tensor to be sparsified
    card
        Desired number of non-zero elements in the tensor
    out
        Optional output array for writing the result to.

    Returns
    -------
    startai.array of shape tensor.shape

    Examples
    --------
    >>> x = startai.arange(100)
    >>> x = startai.reshape(x, (10, 10))
    >>> sparsify_tensor(x, 10)
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
    if card >= startai.prod(startai.array(x.shape)):
        return startai.inplace_update(out, x) if startai.exists(out) else x
    _shape = startai.shape(x)
    x = startai.reshape(startai.sort(startai.abs(x)), (-1,))
    tensor = startai.concat([startai.zeros(len(x) - card, dtype=x.dtype), x[-card:]], axis=0)

    return startai.reshape(tensor, _shape, out=out)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def erfc(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """
    Complementary error function, 1 - erf(x)

    Parameters
    ----------
    x
        Input array of real or complex valued argument.
    out
        optional output array, for writing the result to.
        It must have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        Values of the complementary error function.

    Examples
    --------
    >>> x = startai.array([2, -1., 0])
    >>> startai.erfc(x)
    startai.array([0.00467773, 1.84270084, 1.        ])
    """
    return startai.current_backend(x).erfc(x, out=out)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def erfinv(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
):
    """Compute the inverse error function.

    Parameters
    ----------
    x
        Input array of real or complex valued argument.
    out
        optional output array, for writing the result to.
        It must have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        Values of the inverse error function.

    Examples
    --------
    >>> x = startai.array([0, 0.5, -1.])
    >>> startai.erfinv(x)
    startai.array([0.0000, 0.4769,   -inf])
    """
    return startai.current_backend(x).erfinv(x, out=out)
