# global
from typing import Union, Optional, Sequence

# local
import startai
from startai.func_wrapper import (
    handle_array_function,
    to_native_arrays_and_back,
    handle_out_argument,
    handle_nestable,
    handle_array_like_without_promotion,
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
def all(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Test whether all input array elements evaluate to ``True`` along a
    specified axis.

    .. note::
       Positive infinity, negative infinity, and NaN must evaluate to ``True``.

    .. note::
       If ``x`` is an empty array or the size of the axis (dimension) along which to
       evaluate elements is zero, the test result must be ``True``.

    Parameters
    ----------
    x
        input array.
    axis
        axis or axes along which to perform a logical AND reduction. By default, a
        logical AND reduction must be performed over the entire array. If a tuple of
        integers, logical AND reductions must be performed over multiple axes. A valid
        ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank
        (number of dimensions) of ``x``. If an ``axis`` is specified as a negative
        integer, the function must determine the axis along which to perform a reduction
        by counting backward from the last dimension (where ``-1`` refers to the last
        dimension). If provided an invalid ``axis``, the function must raise an
        exception. Default ``None``.
    keepdims
        If ``True``, the reduced axes (dimensions) must be included in the result as
        singleton dimensions, and, accordingly, the result must be compatible with the
        input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes
        (dimensions) must not be included in the result. Default: ``False``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        if a logical AND reduction was performed over the entire array, the returned
        array must be a zero-dimensional array containing the test result; otherwise,
        the returned array must be a non-zero-dimensional array containing the test
        results. The returned array must have a data type of ``bool``.


    This method conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.all.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicit
    y,but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1, 2, 3])
    >>> y = startai.all(x)
    >>> print(y)
    startai.array(True)

    >>> x = startai.array([[0],[1]])
    >>> y = startai.zeros((1,1), dtype='bool')
    >>> a = startai.all(x, axis=0, out = y, keepdims=True)
    >>> print(a)
    startai.array([[False]])

    >>> x = startai.array(False)
    >>> y = startai.all(startai.array([[0, 4],[1, 5]]), axis=(0,1), out=x, keepdims=False)
    >>> print(y)
    startai.array(False)

    >>> x = startai.array(False)
    >>> y = startai.all(startai.array([[[0], [1]], [[1], [1]]]), axis=(0,1,2), out=x,
    ...             keepdims=False)
    >>> print(y)
    startai.array(False)

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0, 1, 2]), b=startai.array([3, 4, 5]))
    >>> y = startai.all(x)
    >>> print(y)
    {
        a: startai.array(False),
        b: startai.array(True)
    }

    >>> x = startai.Container(a=startai.native_array([0, 1, 2]),b=startai.array([3, 4, 5]))
    >>> y = startai.all(x)
    >>> print(y)
    {
        a: startai.array(False),
        b: startai.array(True)
    }
    """
    return startai.current_backend(x).all(x, axis=axis, keepdims=keepdims, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
def any(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Test whether any input array element evaluates to ``True`` along a
    specified axis.

    .. note::
       Positive infinity, negative infinity, and NaN must evaluate to ``True``.

    .. note::
       If ``x`` is an empty array or the size of the axis (dimension) along which to
       evaluate elements is zero, the test result must be ``False``.

    Parameters
    ----------
    x
        input array.
    axis
        axis or axes along which to perform a logical OR reduction. By default, a
        logical OR reduction must be performed over the entire array. If a tuple of
        integers, logical OR reductions must be performed over multiple axes. A valid
        ``axis`` must be an integer on the interval ``[-N, N)``, where ``N`` is the rank
        (number of dimensions) of ``x``. If an ``axis`` is specified as a negative
        integer, the function must determine the axis along which to perform a reduction
        by counting backward from the last dimension (where ``-1`` refers to the last
        dimension). If provided an invalid ``axis``, the function must raise an
        exception. Default: ``None``.
    keepdims
        If ``True``, the reduced axes (dimensions) must be included in the result as
        singleton dimensions, and, accordingly, the result must be compatible with the
        input array (see :ref:`broadcasting`). Otherwise, if ``False``, the reduced axes
        (dimensions) must not be included in the result. Default: ``False``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        if a logical OR reduction was performed over the entire array, the returned
        array must be a zero-dimensional array containing the test result; otherwise,
        the returned array must be a non-zero-dimensional array containing the test
        results. The returned array must have a data type of ``bool``.


    This method conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.any.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicit
    y,but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([2, 3, 4])
    >>> y = startai.any(x)
    >>> print(y)
    startai.array(True)

    >>> x = startai.array([[0],[1]])
    >>> y = startai.zeros((1,1), dtype='bool')
    >>> a = startai.any(x, axis=0, out = y, keepdims=True)
    >>> print(a)
    startai.array([[True]])

    >>> x=startai.array(False)
    >>> y=startai.any(startai.array([[0, 3],[1, 4]]), axis=(0,1), out=x, keepdims=False)
    >>> print(y)
    startai.array(True)

    >>> x=startai.array(False)
    >>> y=startai.any(startai.array([[[0],[1]],[[1],[1]]]),axis=(0,1,2), out=x, keepdims=False)
    >>> print(y)
    startai.array(True)

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0, 1, 2]), b=startai.array([3, 4, 5]))
    >>> y = startai.any(x)
    >>> print(y)
    {
        a: startai.array(True),
        b: startai.array(True)
    }
    """
    return startai.current_backend(x).any(x, axis=axis, keepdims=keepdims, out=out)


# Extra #
# ----- #


def save(item, filepath, format=None):
    if isinstance(item, startai.Container):
        if format is not None:
            item.cont_save(filepath, format=format)
        else:
            item.cont_save(filepath)
    elif isinstance(item, startai.Module):
        item.save(filepath)
    else:
        raise startai.utils.exceptions.StartaiException("Unsupported item type for saving.")


@staticmethod
def load(filepath, format=None, type="module"):
    if type == "module":
        return startai.Module.load(filepath)
    elif type == "container":
        if format is not None:
            return startai.Container.cont_load(filepath, format=format)
        else:
            return startai.Container.cont_load(filepath)
    else:
        raise startai.utils.exceptions.StartaiException("Unsupported item type for loading.")
