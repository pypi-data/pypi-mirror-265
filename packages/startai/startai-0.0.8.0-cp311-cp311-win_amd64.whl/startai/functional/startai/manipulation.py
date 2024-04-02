# For Review
# global
from typing import Union, Optional, Tuple, List, Iterable, Sequence
from numbers import Number
from numpy.core.numeric import normalize_axis_tuple

# local
import startai
from startai.utils.backend import current_backend
from startai.func_wrapper import (
    handle_array_function,
    to_native_arrays_and_back,
    handle_out_argument,
    handle_nestable,
    handle_array_like_without_promotion,
    handle_view,
    handle_device,
    handle_backend_invalid,
)
from startai.utils.exceptions import handle_exceptions


def _calculate_out_shape(axis, array_shape):
    if type(axis) not in (tuple, list):
        axis = (axis,)
    out_dims = len(axis) + len(array_shape)
    norm_axis = normalize_axis_tuple(axis, out_dims)
    shape_iter = iter(array_shape)
    out_shape = [
        1 if current_ax in norm_axis else next(shape_iter)
        for current_ax in range(out_dims)
    ]
    return out_shape


# Array API Standard #
# -------------------#


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def concat(
    xs: Union[
        Tuple[Union[startai.Array, startai.NativeArray], ...],
        List[Union[startai.Array, startai.NativeArray]],
    ],
    /,
    *,
    axis: int = 0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Join a sequence of arrays along an existing axis.

    Parameters
    ----------
    xs
        input arrays to join. The arrays must have the same shape, except in the
        dimension specified by axis.
    axis
        axis along which the arrays will be joined. If axis is None, arrays are
        flattened before concatenation. If axis is negative, the axis is along which
        to join is determined by counting from the last dimension. Default: ``0``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an output array containing the concatenated values. If the input arrays have
        different data types, normal Type Promotion Rules apply.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.concat.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    >>> x = startai.array([[1, 2], [3, 4]])
    >>> y = startai.array([[5, 6]])
    >>> startai.concat((x, y))
    startai.array([[1, 2],[3, 4],[5, 6]])
    """
    return current_backend(xs[0]).concat(xs, axis=axis, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def expand_dims(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
    axis: Union[int, Sequence[int]] = 0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Expand the shape of an array by inserting a new axis (dimension) of size
    one at the position specified by axis.

    Parameters
    ----------
    x
        input array.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    axis
        axis position (zero-based). If x has rank (i.e, number of dimensions) N, a
        valid axis must reside on the closed-interval [-N-1, N]. If provided a negative
        axis, the axis position at which to insert a singleton dimension is
        computed as N + axis + 1. Hence, if provided -1, the resolved axis position
        is N (i.e., a singleton dimension is appended to the input array x).
        If provided -N-1, the resolved axis position is 0 (i.e., a singleton
        dimension is prepended to the input array x). An IndexError exception
        is raised if provided an invalid axis position.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array with its dimension added by one in a given axis.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an
    extension of the `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.expand_dims.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0, 1, 2])
    >>> y = startai.expand_dims(x)
    >>> print(y)
    startai.array([[0, 1, 2]])

    >>> x = startai.array([[0.5, -0.7, 2.4],
    ...                [  1,    2,   3]])
    >>> y = startai.zeros((2, 1, 3))
    >>> startai.expand_dims(x, axis=1, out=y)
    >>> print(y)
    startai.array([[[0.5, -0.7, 2.4]],
               [[ 1.,   2.,  3.]]])

    >>> x = startai.array([[-1, -2],
    ...                [ 3,  4]])
    >>> y = startai.zeros((1, 2, 2))
    >>> startai.expand_dims(x, axis=0, out=y)
    >>> print(y)
    startai.array([[[-1, -2],
                [3,  4]]])

    >>> x = startai.array([[-1.1, -2.2, 3.3],
    ...                [ 4.4,  5.5, 6.6]])
    >>> y = startai.expand_dims(x, axis=(0, -1))
    >>> print(y)
    startai.array([[[[-1.1],
                 [-2.2],
                 [ 3.3]],
                [[ 4.4],
                 [ 5.5],
                 [ 6.6]]]])

    >>> x = startai.array([[-1.7, -3.2, 2.3],
    ...                [ 6.3,  1.4, 5.7]])
    >>> y = startai.expand_dims(x, axis=[0, 1, -1])
    >>> print(y)
    startai.array([[[[[-1.7],
                  [-3.2],
                  [ 2.3]],
                 [[ 6.3],
                  [ 1.4],
                  [ 5.7]]]]])

    With one :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> y = startai.expand_dims(x, axis=-1)
    >>> print(y)
    {
        a: startai.array([[0.],
                      [1.],
                      [2.]]),
        b: startai.array([[3.],
                      [4.],
                      [5.]])
    }

    With multiple :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> container_axis = startai.Container(a=0, b=1)
    >>> y = startai.expand_dims(x, axis=container_axis)
    >>> print(y)
    {
        a: startai.array([[0., 1., 2.]]),
        b: startai.array([[3.],
                      [4.],
                      [5.]])
    }
    """
    return current_backend(x).expand_dims(x, copy=copy, axis=axis, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def flip(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
    axis: Optional[Union[int, Sequence[int]]] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Reverses the order of elements in an array along the given axis. The
    shape of the array must be preserved.

    Parameters
    ----------
    x
        input array.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    axis
        axis (or axes) along which to flip. If axis is None, all input array axes are
        flipped. If axis is negative, axis is counted from the last dimension. If
        provided more than one axis, only the specified axes. Default: ``None``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an output array having the same data type and shape as`x and whose elements,
        relative to ``x``, are reordered.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.flip.html>`_
    in the standard.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([3, 4, 5])
    >>> y = startai.flip(x)
    >>> print(y)
    startai.array([5, 4, 3])

    >>> x = startai.array([[1, 2, 3], [4, 5, 6]])
    >>> y = startai.zeros((2, 3))
    >>> startai.flip(x, out=y)
    >>> print(y)
    startai.array([[6, 5, 4],
               [3, 2, 1]])

    >>> x = startai.array([[1, 2, 3], [4, 5, 6]])
    >>> y = startai.zeros((2, 3))
    >>> startai.flip(x, axis=0, out=y)
    >>> print(y)
    startai.array([[4, 5, 6],
               [1, 2, 3]])

    >>> x = startai.array([[[1, 2, 3], [4, 5, 6]],[[7, 8, 9], [10, 11, 12]]])
    >>> startai.flip(x, axis=[0, 1], out=x)
    >>> print(x)
    startai.array([[[10,11,12],[7,8,9]],[[4,5,6],[1,2,3]]])

    >>> x = startai.array([[[1, 2, 3], [4, 5, 6]],[[7, 8, 9], [10, 11, 12]]])
    >>> startai.flip(x, axis=(2, 1), out=x)
    >>> print(x)
    startai.array([[[ 6,  5,  4],
                [ 3,  2,  1]],
               [[12, 11, 10],
                [ 9,  8,  7]]])
    """
    return current_backend(x).flip(x, copy=copy, axis=axis, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def permute_dims(
    x: Union[startai.Array, startai.NativeArray],
    /,
    axes: Tuple[int, ...],
    *,
    copy: Optional[bool] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Permutes the axes (dimensions) of an array x.

    Parameters
    ----------
    x
        input array.
    axes
        tuple containing a permutation of (0, 1, ..., N-1) where N is the number of axes
        (dimensions) of x.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the axes permutation. The returned array must have the same
        data type as x.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.permute_dims.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[1, 2, 3], [4, 5, 6]])
    >>> y = startai.permute_dims(x, axes=(1, 0))
    >>> print(y)
    startai.array([[1, 4],
               [2, 5],
               [3, 6]])

    >>> x = startai.zeros((2, 3))
    >>> y = startai.permute_dims(x, axes=(1, 0))
    >>> print(y)
    startai.array([[0., 0.],
               [0., 0.],
               [0., 0.]])

    With one :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[0., 1. ,2.]]), b=startai.array([[3., 4., 5.]]))
    >>> y = startai.permute_dims(x, axes=(1, 0))
    >>> print(y)
    {
        a: startai.array([[0.],
                      [1.],
                      [2.]]),
        b: startai.array([[3.],
                      [4.],
                      [5.]])
    }

    >>> x = startai.Container(a=startai.array([[0., 1., 2.]]), b = startai.array([[3., 4., 5.]]))
    >>> y = startai.Container(a=startai.zeros((3, 1)), b= startai.zeros((3, 1)))
    >>> startai.permute_dims(x, axes=(1, 0), out=y)
    >>> print(y)
    {
        a: startai.array([[0.],
                      [1.],
                      [2.]]),
        b: startai.array([[3.],
                      [4.],
                      [5.]])
    }
    """
    return current_backend(x).permute_dims(x, axes, copy=copy, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def reshape(
    x: Union[startai.Array, startai.NativeArray],
    /,
    shape: Union[startai.Shape, startai.NativeShape, Sequence[int]],
    *,
    copy: Optional[bool] = None,
    order: str = "C",
    allowzero: bool = True,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Give a new shape to an array without changing its data.

    Parameters
    ----------
    x
        Input array to be reshaped.
    shape
        a new shape compatible with the original shape. One shape dimension
        can be -1. In this case, the value is inferred from the length of the array and
        remaining dimensions.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    order
        Read the elements of x using this index order, and place the elements into
        the reshaped array using this index order.
        ``C`` means to read / write the elements using C-like index order,
        with the last axis index changing fastest, back to the first axis index
        changing slowest.
        ``F`` means to read / write the elements using Fortran-like index order, with
        the first index changing fastest, and the last index changing slowest.
        Note that the ``C`` and ``F`` options take no account of the memory layout
        of the underlying array, and only refer to the order of indexing.
        Default order is ``C``
    allowzero
        When ``allowzero=True``, any value in the ``shape`` argument that is equal to
        zero, the zero value is honored. When ``allowzero=False``, any value in the
        ``shape`` argument that is equal to zero the corresponding dimension value is
        copied from the input tensor dynamically.
        Default value is ``True``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an output array having the same data type and elements as x.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.reshape.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[0., 1., 2.],[3., 4., 5.]])
    >>> y = startai.reshape(x,(3,2))
    >>> print(y)
    startai.array([[0., 1.],
               [2., 3.],
               [4., 5.]])

    >>> x = startai.array([[0., 1., 2.],[3., 4., 5.]])
    >>> y = startai.reshape(x,(3,2), order='F')
    >>> print(y)
    startai.array([[0., 4.],
               [3., 2.],
               [1., 5.]])

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([[0., 1., 2.],[3., 4., 5.]])
    >>> y = startai.reshape(x,(2,3))
    >>> print(y)
    startai.array([[0., 1., 2.],
               [3., 4., 5.]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0, 1, 2, 3, 4, 5]),
    ...                   b=startai.array([0, 1, 2, 3, 4, 5]))
    >>> y = startai.reshape(x,(2,3))
    >>> print(y)
    {
        a: startai.array([[0, 1, 2],
                      [3, 4, 5]]),
        b: startai.array([[0, 1, 2],
                      [3, 4, 5]])
    }

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[0., 1., 2.]]), b=startai.array([[3., 4., 5.]]))
    >>> y = startai.reshape(x, (-1, 1))
    >>> print(y)
    {
        a: startai.array([[0.],[1.],[2.]]),
        b: startai.array([[3.],[4.],[5.]])
    }
    """
    startai.utils.assertions.check_elem_in_list(order, ["C", "F"])
    return current_backend(x).reshape(
        x, shape=shape, copy=copy, allowzero=allowzero, out=out, order=order
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def roll(
    x: Union[startai.Array, startai.NativeArray, startai.Container],
    /,
    shift: Union[int, Sequence[int]],
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    out: Optional[startai.Array] = None,
) -> Union[startai.Array, startai.Container]:
    """Roll array elements along a specified axis. Array elements that roll
    beyond the last position are re-introduced at the first position. Array
    elements that roll beyond the first position are re-introduced at the last
    position.

    Parameters
    ----------
    x
        input array.
    shift
        number of places by which the elements are shifted. If shift is a tuple,
        then axis must be a tuple of the same size, and each of the given axes must
        be shifted by the corresponding element in shift. If shift is an int
        and axis a tuple, then the same shift must be used for all specified
        axes. If a shift is positive, then array elements must be shifted positively
        (toward larger indices) along the dimension of axis. If a shift is negative,
        then array elements must be shifted negatively (toward smaller indices) along
        the dimension of axis.
    axis
        axis (or axes) along which elements to shift. If axis is None, the array
        must be flattened, shifted, and then restored to its original shape.
        Default: ``None``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an output array having the same data type as x and whose elements, relative
        to x, are shifted.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.roll.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0., 1., 2.])
    >>> y = startai.roll(x, 1)
    >>> print(y)
    startai.array([2., 0., 1.])

    >>> x = startai.array([[0., 1., 2.],
    ...                [3., 4., 5.]])
    >>> y = startai.zeros((2, 3))
    >>> startai.roll(x, 2, axis=-1, out=y)
    >>> print(y)
    startai.array([[1., 2., 0.],
               [4., 5., 3.]])

    >>> x = startai.array([[[0., 0.], [1., 3.], [2., 6.]],
    ...                [[3., 9.], [4., 12.], [5., 15.]]])
    >>> startai.roll(x, shift=(1, -1), axis=(0, 2), out=x)
    >>> print(x)
    startai.array([[[ 9., 3.],
                [12., 4.],
                [15., 5.]],
               [[ 0., 0.],
                [ 3., 1.],
                [ 6., 2.]]])

    With one :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> y = startai.roll(x, 1)
    >>> print(y)
    {
        a: startai.array([2., 0., 1.]),
        b: startai.array([5., 3., 4.])
    }

    With multiple :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> shift = startai.Container(a=1, b=-1)
    >>> y = startai.roll(x, shift)
    >>> print(y)
    {
        a: startai.array([2., 0., 1.]),
        b: startai.array([4., 5., 3.])
    }
    """
    return current_backend(x).roll(x, shift, axis=axis, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def squeeze(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    copy: Optional[bool] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Remove singleton dimensions (axes) from x.

    Parameters
    ----------
    x
        input array.
    axis
        axis (or axes) to squeeze. If a specified axis has a size greater than one, a
        ValueError is. If None, then all squeezable axes are squeezed. Default: ``None``
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an output array having the same data type and elements as x.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.squeeze.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[[0, 1], [2, 3]]])
    >>> print(startai.squeeze(x, axis=0))
    startai.array([[0, 1], [2, 3]])

    >>> x = startai.array([[[[1, 2, 3]], [[4, 5, 6]]]])
    >>> print(startai.squeeze(x, axis=2))
    startai.array([[[1, 2, 3], [4, 5, 6]]])

    >>> x = startai.array([[[0], [1], [2]]])
    >>> print(startai.squeeze(x, axis=None))
    startai.array([0, 1, 2])

    >>> print(startai.squeeze(x, axis=0))
    startai.array([[0],
           [1],
           [2]])

    >>> print(startai.squeeze(x, axis=2))
    startai.array([[0, 1, 2]])

    >>> print(startai.squeeze(x, axis=(0, 2)))
    startai.array([0, 1, 2])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> y = startai.squeeze(x, axis=None)
    >>> print(y)
    {
        a: startai.array([0., 1., 2.]),
        b: startai.array([3., 4., 5.])
    }
    """
    return current_backend(x).squeeze(x, axis=axis, copy=copy, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def stack(
    arrays: Union[
        Tuple[Union[startai.Array, startai.NativeArray], ...],
        List[Union[startai.Array, startai.NativeArray]],
    ],
    /,
    *,
    axis: int = 0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Join a sequence of arrays along a new axis.

    Parameters
    ----------
    arrays
        input arrays to join. Each array must have the same shape.
    axis
        axis along which the arrays will be joined. Providing an axis specifies the
        index of the new axis in the dimensions of the result. For example, if axis
        is 0, the new axis will be the first dimension and the output array will
        have shape (N, A, B, C); if axis is 1, the new axis will be the
        second dimension and the output array will have shape (A, N, B, C); and, if
        axis is -1, the new axis will be the last dimension and the output array
        will have shape (A, B, C, N). A valid axis must be on the interval
        [-N, N), where N is the rank (number of dimensions) of x. If
        provided an axis outside of the required interval, the function must raise
        an exception. Default: ``0``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an output array having rank N+1, where N is the rank (number of
        dimensions) of x. If the input arrays have different data types, normal
        ref:`type-promotion` must apply. If the input arrays have the same data type,
        the output array must have the same data type as the input arrays.
        .. note::
           This specification leaves type promotion between data type families (i.e.,
           intxx and floatxx) unspecified.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.stack.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :code: `startai.Array` input:

    >>> x = startai.array([0., 1., 2., 3., 4.])
    >>> y = startai.array([6.,7.,8.,9.,10.])
    >>> startai.stack((x,y))
    startai.array([[ 0.,  1.,  2.,  3.,  4.],
        [ 6.,  7.,  8.,  9., 10.]])

    With :code: `startai.Array` input and different `axis` :

    >>> startai.stack((x,y),axis=1)
    startai.array([[ 0.,  6.],
        [ 1.,  7.],
        [ 2.,  8.],
        [ 3.,  9.],
        [ 4., 10.]])
    """
    res = current_backend(arrays).stack(arrays, axis=axis, out=out)
    if startai.exists(out):
        return startai.inplace_update(out, res)
    return res


# Extra #
# ------#


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def clip(
    x: Union[startai.Array, startai.NativeArray],
    /,
    x_min: Optional[Union[Number, startai.Array, startai.NativeArray]] = None,
    x_max: Optional[Union[Number, startai.Array, startai.NativeArray]] = None,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Clips (limits) the values in an array.

    Given an interval, values outside the interval are clipped to the interval edges
    (element-wise). For example, if an interval of [0, 1] is specified, values smaller
    than 0 become 0, and values larger than 1 become 1. Minimum value needs to smaller
    or equal to maximum value to return correct results.

    Parameters
    ----------
    x
        Input array containing elements to clip.
    x_min
        Minimum value.
    x_max
        Maximum value.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        An array with the elements of x, but where values < x_min are replaced with
        x_min, and those > x_max with x_max.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
    >>> y = startai.clip(x, 1., 5.)
    >>> print(y)
    startai.array([1., 1., 2., 3., 4., 5., 5., 5., 5., 5.])

    >>> x = startai.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
    >>> y = startai.zeros_like(x)
    >>> startai.clip(x, 2., 7., out=y)
    >>> print(y)
    startai.array([2., 2., 2., 3., 4., 5., 6., 7., 7., 7.])

    >>> x = startai.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
    >>> x_min = startai.array([3., 3., 1., 0., 2., 3., 4., 0., 4., 4.])
    >>> x_max = startai.array([5., 4., 3., 3., 5., 7., 8., 3., 8., 8.])
    >>> y = startai.clip(x, x_min, x_max)
    >>> print(y)
    startai.array([3., 3., 2., 3., 4., 5., 6., 3., 8., 8.])

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
    >>> x_min = startai.native_array([3., 3., 1., 0., 2., 3., 4., 2., 4., 4.])
    >>> x_max = startai.native_array([5., 4., 3., 3., 5., 7., 8., 3., 8., 8.])
    >>> y = startai.clip(x, x_min, x_max)
    >>> print(y)
    startai.array([3., 3., 2., 3., 4., 5., 6., 3., 8., 8.])

    With a mix of :class:`startai.Array` and :class:`startai.NativeArray` inputs:

    >>> x = startai.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
    >>> x_min = startai.native_array([3., 3., 1., 0., 2., 3., 4., 2., 4., 4.])
    >>> x_max = startai.native_array([5., 4., 3., 3., 5., 7., 8., 3., 8., 8.])
    >>> y = startai.clip(x, x_min, x_max)
    >>> print(y)
    startai.array([3., 3., 2., 3., 4., 5., 6., 3., 8., 8.])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> y = startai.clip(x, 1., 5.)
    >>> print(y)
    {
        a: startai.array([1., 1., 2.]),
        b: startai.array([3., 4., 5.])
    }

    With multiple :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> x_min = startai.Container(a=0, b=-3)
    >>> x_max = startai.Container(a=1, b=-1)
    >>> y = startai.clip(x, x_min,x_max)
    >>> print(y)
    {
        a: startai.array([0., 1., 1.]),
        b: startai.array([-1., -1., -1.])
    }

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.])
    >>> x_min = startai.array([3., 0., 1])
    >>> x_max = startai.array([5., 4., 3.])
    >>> y = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> z = startai.clip(y, x_min, x_max)
    >>> print(z)
    {
        a: startai.array([3., 1., 2.]),
        b: startai.array([3., 4., 3.])
    }
    """
    return current_backend(x).clip(x, x_min, x_max, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def constant_pad(
    x: Union[startai.Array, startai.NativeArray],
    /,
    pad_width: Iterable[Tuple[int]],
    *,
    value: Number = 0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Pad an array with a constant value.

    Parameters
    ----------
    x
        Input array to pad.
    pad_width
        Number of values padded to the edges of each axis.
        Specified as ((before_1, after_1), … (before_N, after_N)), where N is number of
        axes of x.
    value
        The constant value to pad the array with.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        Padded array of rank equal to x with shape increased according to pad_width.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1, 2, 3, 4, 5])
    >>> y = startai.constant_pad(x, pad_width = [[2, 3]])
    >>> print(y)
    startai.array([0, 0, 1, 2, 3, 4, 5, 0, 0, 0])

    >>> x = startai.array([[1, 2], [3, 4]])
    >>> y = startai.constant_pad(x, pad_width=[(2, 3), (2, 3)])
    >>> print(y)
    startai.array([[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2, 0, 0, 0],
            [0, 0, 3, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]])

    >>> x = startai.array([[1, 2], [3, 4]])
    >>> y = startai.constant_pad(x, pad_width = [[3, 2], [2, 3]])
    >>> print(y)
    startai.array([[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 2, 0, 0, 0],
                [0, 0, 3, 4, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]])

    >>> x = startai.array([[2.], [3.]])
    >>> y = startai.zeros((4, 3))
    >>> startai.constant_pad(x, pad_width = [(1, 1), (1, 1)], value = 5.0, out= y)
    >>> print(y)
    startai.array([[5., 5., 5.],
           [5., 2., 5.],
           [5., 3., 5.],
           [5., 5., 5.]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a = startai.array([1., 2., 3.]),
    ...                   b = startai.array([3., 4., 5.]))
    >>> y = startai.constant_pad(x, pad_width = [[2, 3]], value = 5.0)
    >>> print(y)
    {
        a: startai.array([5., 5., 1., 2., 3., 5., 5., 5.]),
        b: startai.array([5., 5., 3., 4., 5., 5., 5., 5.])
    }
    """
    return current_backend(x).constant_pad(x, pad_width=pad_width, value=value, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def repeat(
    x: Union[startai.Array, startai.NativeArray],
    /,
    repeats: Union[int, Iterable[int]],
    *,
    axis: Optional[int] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Repeat values along a given dimension.

    Parameters
    ----------
    x
        Input array.
    repeats
        The number of repetitions for each element. repeats is broadcast to fit the
        shape of the given axis.
    axis
        The axis along which to repeat values. By default, use the flattened input
        array, and return a flat output array.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The repeated output array.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([3, 4, 5])
    >>> y = startai.repeat(x, 2)
    >>> print(y)
    startai.array([3, 3, 4, 4, 5, 5])

    >>> x = startai.array([[1, 2, 3], [4, 5, 6]])
    >>> y = startai.repeat(x, [1, 2], axis=0)
    >>> print(y)
    startai.array([[1, 2, 3],
               [4, 5, 6],
               [4, 5, 6]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([0., 1., 2.]))
    >>> y = startai.repeat(x, 2, axis=0)
    >>> print(y)
    {
        a: startai.array([0., 0., 1., 1., 2., 2.]),
        b: startai.array([0., 0., 1., 1., 2., 2.])
    }
    """
    return current_backend(x).repeat(x, repeats, axis=axis, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@to_native_arrays_and_back
@handle_array_function
@handle_device
def split(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
    num_or_size_splits: Optional[
        Union[int, Sequence[int], startai.Array, startai.NativeArray]
    ] = None,
    axis: int = 0,
    with_remainder: bool = False,
) -> List[startai.Array]:
    """Split an array into multiple sub-arrays.

    Parameters
    ----------
    x
        array to be divided into sub-arrays.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    num_or_size_splits
        Number of equal arrays to divide the array into along the given axis if an
        integer. The size of each split element if a sequence of integers or 1-D array.
        Default is to divide into as many 1-dimensional arrays as the axis dimension.
    axis
        The axis along which to split, default is ``0``.
    with_remainder
        If the tensor does not split evenly, then store the last remainder entry.
        Default is ``False``.

    Returns
    -------
    ret
        A list of sub-arrays.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1, 2, 3])
    >>> y = startai.split(x)
    >>> print(y)
    [startai.array([1]),startai.array([2]),startai.array([3])]

    >>> x = startai.array([[3, 2, 1], [4, 5, 6]])
    >>> y = startai.split(x, num_or_size_splits=2, axis=1, with_remainder=True)
    >>> print(y)
    [startai.array([[3,2],[4,5]]),startai.array([[1],[6]])]

    >>> x = startai.array([4, 6, 5, 3])
    >>> y = x.split(num_or_size_splits=[1, 3], axis=0, with_remainder=False)
    >>> print(y)
    startai.array([[4], [6, 5, 3]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([10, 45, 2]))
    >>> y = startai.split(x)
    >>> print(y)
    [
        {
            a: startai.array([10])
        },
        {
            a: startai.array([45])
        },
        {
            a: startai.array([2])
        }
    ]
    """
    return current_backend(x).split(
        x,
        copy=copy,
        num_or_size_splits=num_or_size_splits,
        axis=axis,
        with_remainder=with_remainder,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def swapaxes(
    x: Union[startai.Array, startai.NativeArray],
    axis0: int,
    axis1: int,
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Interchange two axes of an array.

    Parameters
    ----------
    x
        Input array.
    axis0
        First axis to be swapped.
    axis1
        Second axis to be swapped.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        x with its axes permuted.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[0, 1, 2]])
    >>> y = startai.swapaxes(x, 0, 1)
    >>> print(y)
    startai.array([[0],
               [1],
               [2]])

    >>> x = startai.array([[[0,1],[2,3]],[[4,5],[6,7]]])
    >>> y = startai.swapaxes(x, 0, 1)
    >>> print(y)
    startai.array([[[0, 1],
                [4, 5]],
               [[2, 3],
                [6, 7]]])

    >>> x = startai.array([[[0,1],[2,3]],[[4,5],[6,7]]])
    >>> y = startai.swapaxes(x, 0, 2)
    >>> print(y)
    startai.array([[[0, 4],
                [2, 6]],
               [[1, 5],
                [3, 7]]])

    >>> x = startai.array([[[0,1],[2,3]],[[4,5],[6,7]]])
    >>> y = startai.swapaxes(x, 1, 2)
    >>> print(y)
    startai.array([[[0, 2],
                [1, 3]],
               [[4, 6],
                [5, 7]]])


    >>> x = startai.array([[0, 1, 2]])
    >>> y = startai.swapaxes(x, 0, 1)
    >>> print(y)
    startai.array([[0],
               [1],
               [2]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[0., 1., 2.]]), b=startai.array([[3., 4., 5.]]))
    >>> y = startai.swapaxes(x, 0, 1)
    >>> print(y)
    {
        a: startai.array([[0.],
                      [1.],
                      [2.]]),
        b: startai.array([[3.],
                      [4.],
                      [5.]])
    }

    # Both the description and the type hints above assumes an array input for
    simplicity, but this function is *nestable*, and therefore also accepts
    :class:`startai.Container` instances in place of any of the arguments.
    """
    return current_backend(x).swapaxes(x, axis0, axis1, copy=copy, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def tile(
    x: Union[startai.Array, startai.NativeArray],
    /,
    repeats: Iterable[int],
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Construct an array by repeating x the number of times given by reps.

    Parameters
    ----------
    x
        Input array.
    repeats
        The number of repetitions of x along each axis.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The tiled output array.


    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1,2,3,4])
    >>> y = startai.tile(x, 3)
    >>> print(y)
    startai.array([1,2,3,4,1,2,3,4,1,2,3,4])

    >>> x = startai.array([[1,2,3],
    ...                [4,5,6]])
    >>> y = startai.tile(x, (2,3))
    >>> print(y)
    startai.array([[1,2,3,1,2,3,1,2,3],
               [4,5,6,4,5,6,4,5,6],
               [1,2,3,1,2,3,1,2,3],
               [4,5,6,4,5,6,4,5,6]])

    >>> x = startai.array([[[0], [1]]])
    >>> y = startai.tile(x,(2,2,3))
    >>> print(y)
    startai.array([[[0,0,0],
                [1,1,1],
                [0,0,0],
                [1,1,1]],
               [[0,0,0],
                [1,1,1],
                [0,0,0],
                [1,1,1]]])

    With :class:`startai.Container` input:

    >>> x = startai.Container( a = startai.array([0,1,2]), b = startai.array([[3],[4]]))
    >>> y = startai.tile(x, (1,2))
    >>> print(y)
    {
        a: startai.array([[0,1,2,0,1,2]]),
        b: startai.array([[3,3],[4,4]])
    }


    # Both the description and the type hints above assumes an array input for
    simplicity, but this function is *nestable*, and therefore also accepts
    :class:`startai.Container` instances in place of any of the arguments.
    """
    return current_backend(x).tile(x, repeats, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@to_native_arrays_and_back
@handle_array_function
@handle_device
def unstack(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
    axis: int = 0,
    keepdims: bool = False,
) -> List[startai.Array]:
    """Unpacks the given dimension of a rank-R array into rank-(R-1) arrays.

    Parameters
    ----------
    x
        Input array to unstack.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    axis
        Axis for which to unpack the array.
    keepdims
        Whether to keep dimension 1 in the unstack dimensions. Default is ``False``.

    Returns
    -------
    ret
        List of arrays, unpacked along specified dimensions.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    >>> y = startai.unstack(x, axis=0)
    >>> print(y)
    [startai.array([[1, 2],
                [3, 4]]), startai.array([[5, 6],
                [7, 8]])]

    >>> x = startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    >>> y = startai.unstack(x, axis=1, keepdims=True)
    >>> print(y)
    [startai.array([[[1, 2]],
                [[5, 6]]]), startai.array([[[3, 4]],
                [[7, 8]]])]

    With :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
                            b=startai.array([[[9, 10], [11, 12]], [[13, 14], [15, 16]]]))
    >>> startai.unstack(x, axis=0)
    [{
        a: startai.array([[1, 2],
                      [3, 4]]),
        b: startai.array([[9, 10],
                      [11, 12]])
    }, {
        a: startai.array([[5, 6],
                      [7, 8]]),
        b: startai.array([[13, 14],
                      [15, 16]])
    }]

    >>> x = startai.Container(a=startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
    ...                   b=startai.array([[[9, 10], [11, 12]], [[13, 14], [15, 16]]]))
    >>> startai.unstack(x, axis=1, keepdims=True)
    [{
        a: startai.array([[[1, 2]],
                      [[5, 6]]]),
        b: startai.array([[[9, 10]],
                      [[13, 14]]])
    }, {
        a: startai.array([[[3, 4]],
                      [[7, 8]]]),
        b: startai.array([[[11, 12]],
                      [[15, 16]]])
    }]


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.
    """
    return current_backend(x).unstack(x, copy=copy, axis=axis, keepdims=keepdims)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def zero_pad(
    x: Union[startai.Array, startai.NativeArray],
    /,
    pad_width: Iterable[Tuple[int]],
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Pad an array with zeros.

    Parameters
    ----------
    x
        Input array to pad.
    pad_width
        Number of values padded to the edges of each axis. Specified as
        ((before_1, after_1), … (before_N, after_N)), where N is number of axes of x.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        Padded array of rank equal to x with shape increased according to pad_width.

    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/
    API_specification/generated/array_api.concat.html>`_
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1., 2., 3.,4, 5, 6])
    >>> y = startai.zero_pad(x, pad_width = [[2, 3]])
    >>> print(y)
    startai.array([0., 0., 1., 2., 3., 4., 5., 6., 0., 0., 0.])

    >>> x = startai.array([[1., 2., 3.],[4, 5, 6]])
    >>> y = startai.zero_pad(x, pad_width = [[2, 3], [2, 3]])
    >>> print(y)
    startai.array([[0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 1., 2., 3., 0., 0., 0.],
       [0., 0., 4., 5., 6., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0.]])

    >>> x = startai.Container(a = startai.array([1., 2., 3.]), b = startai.array([3., 4., 5.]))
    >>> y = startai.zero_pad(x, pad_width = [[2, 3]])
    >>> print(y)
    {
        a: startai.array([0., 0., 1., 2., 3., 0., 0., 0.]),
        b: startai.array([0., 0., 3., 4., 5., 0., 0., 0.])
    }
    """
    return current_backend(x).zero_pad(x, pad_width, out=out)
