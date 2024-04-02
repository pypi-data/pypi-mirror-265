# global
from typing import Union, Optional, Literal, List

# local
import startai
from startai.func_wrapper import (
    handle_array_function,
    to_native_arrays_and_back,
    handle_out_argument,
    handle_nestable,
    handle_array_like_without_promotion,
    handle_device,
    handle_backend_invalid,
)
from startai.utils.exceptions import handle_exceptions


# Array API Standard #
# -------------------#


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def argsort(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return the indices that sort an array ``x`` along a specified axis.

    Parameters
    ----------
    x
        input array.
    axis
        axis along which to sort. If set to ``-1``, the function must sort along the
        last axis. Default: ``-1``.
    descending
        sort order. If ``True``, the returned indices sort ``x`` in descending order
        (by value). If ``False``, the returned indices sort ``x`` in ascending order
        (by value). Default: ``False``.
    stable
        sort stability. If ``True``, the returned indices must maintain the relative
        order of ``x`` values which compare as equal. If ``False``, the returned indices
        may or may not maintain the relative order of ``x`` values which compare as
        equal (i.e., the relative order of ``x`` values which compare as equal is
        implementation-dependent). Default: ``True``.
    out
        optional output array, for writing the result to. It must have the same shape
        as ``x``.

    Returns
    -------
    ret
        an array of indices. The returned array must have the same shape as ``x``. The
        returned array must have the default array index data type.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.argsort.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([3,1,2])
    >>> y = startai.argsort(x)
    >>> print(y)
    startai.array([1,2,0])

    >>> x = startai.array([4,3,8])
    >>> y = startai.argsort(x, descending=True)
    >>> print(y)
    startai.array([2,0,1])

    >>> x = startai.array([[1.5, 3.2], [2.3, 2.3]])
    >>> startai.argsort(x, axis=0, descending=True, stable=False, out=x)
    >>> print(x)
    startai.array([[1, 0], [0, 1]])

    >>> x = startai.array([[[1,3], [3,2]], [[2,4], [2,0]]])
    >>> y = startai.argsort(x, axis=1, descending=False, stable=True)
    >>> print(y)
    startai.array([[[0, 1], [1, 0]], [[0, 1], [1, 0]]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([5,1,3]), b=startai.array([[0, 3], [3, 2]]))
    >>> y = startai.argsort(x)
    >>> print(y)
    {
        a: startai.array([1, 2, 0]),
        b: startai.array([[0, 1], [1, 0]])
    }

    >>> x = startai.Container(a=startai.array([[3.5, 5],[2.4, 1]]))
    >>> y = startai.argsort(x)
    >>> print(y)
    {
        a: startai.array([[0,1],[1,0]])
    }

    >>> x = startai.Container(a=startai.array([4,3,6]), b=startai.array([[4, 5], [2, 4]]))
    >>> y = startai.argsort(x, descending=True)
    >>> print(y)
    {
        a: startai.array([2, 0, 1]),
        b: startai.array([[1, 0], [1, 0]])
    }

    >>> x = startai.Container(a=startai.array([[1.5, 3.2],[2.3, 4]]),
    ...                   b=startai.array([[[1,3],[3,2],[2,0]]]))
    >>> y = x.argsort(axis=-1, descending=True, stable=False)
    >>> print(y)
    {
        a: startai.array([[1,0],[1,0]]),
        b: startai.array([[[1,0],[0, 1],[0, 1]]])
    }
    """
    return startai.current_backend(x).argsort(
        x, axis=axis, descending=descending, stable=stable, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def sort(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return a sorted copy of an array.

    Parameters
    ----------
    x
        input array
    axis
        axis along which to sort. If set to ``-1``, the function must sort along the
        last axis. Default: ``-1``.
    descending
        direction  The direction in which to sort the values
    stable
        sort stability. If ``True``,
        the returned indices must maintain the relative order of ``x`` values which
        compare as equal. If ``False``, the returned indices may or may not maintain the
        relative order of ``x`` values which compare as equal (i.e., the relative order
        of ``x`` values which compare as equal is implementation-dependent).
        Default: ``True``.
    out
        optional output array, for writing the result to. It must have the same shape
        as ``x``.

    Returns
    -------
    ret
        An array with the same dtype and shape as ``x``, with the elements sorted
        along the given `axis`.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.sort.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments


    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([7, 8, 6])
    >>> y = startai.sort(x)
    >>> print(y)
    startai.array([6, 7, 8])

    >>> x = startai.array([[[8.9,0], [19,5]],[[6,0.3], [19,0.5]]])
    >>> y = startai.sort(x, axis=1, descending=True, stable=False)
    >>> print(y)
    startai.array([[[19. ,  5. ],[ 8.9,  0. ]],[[19. ,  0.5],[ 6. ,  0.3]]])

    >>> x = startai.array([1.5, 3.2, 0.7, 2.5])
    >>> y = startai.zeros(5)
    >>> startai.sort(x, descending=True, stable=False, out=y)
    >>> print(y)
    startai.array([3.2, 2.5, 1.5, 0.7])

    >>> x = startai.array([[1.1, 2.2, 3.3],[-4.4, -5.5, -6.6]])
    >>> startai.sort(x, out=x)
    >>> print(x)
    startai.array([[ 1.1,  2.2,  3.3],
        [-6.6, -5.5, -4.4]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([8, 6, 6]),b=startai.array([[9, 0.7], [0.4, 0]]))
    >>> y = startai.sort(x, descending=True)
    >>> print(y)
    {
        a: startai.array([8, 6, 6]),
        b: startai.array([[9., 0.7], [0.4, 0.]])
    }

    >>> x = startai.Container(a=startai.array([3, 0.7, 1]),b=startai.array([[4, 0.9], [0.6, 0.2]]))
    >>> y = startai.sort(x, descending=False, stable=False)
    >>> print(y)
    {
        a: startai.array([0.7, 1., 3.]),
        b: startai.array([[0.9, 4.], [0.2, 0.6]])
    }
    """
    return startai.current_backend(x).sort(
        x, axis=axis, descending=descending, stable=stable, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def msort(
    a: Union[startai.Array, startai.NativeArray, list, tuple],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return a copy of an array sorted along the first axis.

    Parameters
    ----------
    a
        array-like input.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        sorted array of the same type and shape as a

    Examples
    --------
    >>> a = startai.asarray([[8, 9, 6],[6, 2, 6]])
    >>> startai.msort(a)
    startai.array(
        [[6, 2, 6],
         [8, 9, 6]]
        )
    """
    return startai.current_backend(a).msort(a, out=out)


# Extra #
# ------#


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def searchsorted(
    x: Union[startai.Array, startai.NativeArray],
    v: Union[startai.Array, startai.NativeArray],
    /,
    *,
    side: Literal["left", "right"] = "left",
    sorter: Optional[Union[startai.Array, startai.NativeArray, List[int]]] = None,
    ret_dtype: Union[startai.Dtype, startai.NativeDtype] = startai.int64,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return the indices of the inserted elements in a sorted array.

    Parameters
    ----------
    x
        Input array. If `sorter` is None, then it must be sorted in ascending order,
        otherwise `sorter` must be an array of indices that sort it.
    v
        specific elements to insert in array x1
    side
        The specific elements' index is at the 'left' side or
        'right' side in the sorted array x1. If the side is 'left', the
        index of the first suitable location located is given. If
        'right', return the last such index.
    ret_dtype
        the data type for the return value, Default: startai.int64,
        only integer data types is allowed.
    sorter
        optional array of integer indices that sort array x into ascending order,
        typically the result of argsort.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
         An array of insertion points.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1, 2, 3])
    >>> v = startai.array([2])
    >>> y  = startai.searchsorted(x, v)
    >>> print(y)
    startai.array([1])

    >>> x = startai.array([0, 1, 2, 3])
    >>> v = startai.array([3])
    >>> y  = startai.searchsorted(x, v, side='right')
    >>> print(y)
    startai.array([4])

    >>> x = startai.array([0, 1, 2, 3, 4, 5])
    >>> v = startai.array([[3, 1], [10, 3], [-2, -1]])
    >>> y  = startai.searchsorted(x, v)
    >>> print(y)
    startai.array([[3, 1],
       [6, 3],
       [0, 0]])
    """
    return startai.current_backend(x, v).searchsorted(
        x,
        v,
        side=side,
        sorter=sorter,
        out=out,
        ret_dtype=ret_dtype,
    )
