# global
from typing import (
    Optional,
    Union,
    Tuple,
    Iterable,
    Sequence,
    Callable,
    Any,
    Literal,
    List,
)
from numbers import Number
from functools import partial
import math

# local
import startai
from startai.func_wrapper import (
    handle_out_argument,
    handle_partial_mixed_function,
    to_native_arrays_and_back,
    inputs_to_native_shapes,
    handle_nestable,
    handle_array_like_without_promotion,
    handle_view,
    inputs_to_startai_arrays,
    handle_array_function,
    handle_device,
    handle_backend_invalid,
)
from startai.functional.startai.general import _numel
from startai.utils.backend import current_backend
from startai.utils.exceptions import handle_exceptions


# Helpers #
# ------- #


def _to_tf_padding(pad_width, ndim):
    if isinstance(pad_width, Number):
        pad_width = [[pad_width] * 2] * ndim
    elif len(pad_width) == 2 and isinstance(pad_width[0], Number):
        pad_width = [pad_width] * ndim
    elif (
        isinstance(pad_width, (list, tuple))
        and isinstance(pad_width[0], (list, tuple))
        and len(pad_width) < ndim
    ):
        pad_width = pad_width * ndim
    return pad_width


def _check_paddle_pad(
    mode, reflect_type, pad_width, input_shape, constant_values, ndim_limit, extend=True
):
    if extend:
        pad_width = _to_tf_padding(pad_width, len(input_shape))
    return isinstance(constant_values, Number) and (
        mode == "constant"
        or (
            (
                (
                    mode == "reflect"
                    and reflect_type == "even"
                    and all(
                        pad_width[i][0] < s and pad_width[i][1] < s
                        for i, s in enumerate(input_shape)
                    )
                )
                or mode in ["edge", "wrap"]
            )
            and len(input_shape) <= ndim_limit
        )
    )


def _to_paddle_padding(pad_width, ndim):
    if isinstance(pad_width, Number):
        pad_width = [pad_width] * (2 * ndim)
    else:
        if len(pad_width) == 2 and isinstance(pad_width[0], Number) and ndim != 1:
            pad_width = [pad_width] * ndim
        pad_width = [item for sublist in pad_width for item in sublist[::-1]][::-1]
    return pad_width


@handle_exceptions
@handle_nestable
@handle_partial_mixed_function
@handle_array_like_without_promotion
@handle_view
@inputs_to_startai_arrays
@handle_array_function
def flatten(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
    start_dim: int = 0,
    end_dim: int = -1,
    order: str = "C",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Flattens input by reshaping it into a one-dimensional tensor. If
    start_dim or end_dim are passed, only dimensions starting with start_dim
    and ending with end_dim are flattened. The order of elements in input is
    unchanged.

    Parameters
    ----------
    x
        input array to flatten.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    start_dim
        first dim to flatten. If not set, defaults to 0.
    end_dim
        last dim to flatten. If not set, defaults to -1.
    order
        Read the elements of the input container using this index order,
        and place the elements into the reshaped array using this index order.
        ‘C’ means to read / write the elements using C-like index order,
        with the last axis index changing fastest, back to the first axis index
        changing slowest.
        ‘F’ means to read / write the elements using Fortran-like index order, with
        the first index changing fastest, and the last index changing slowest.
        Note that the ‘C’ and ‘F’ options take no account of the memory layout
        of the underlying array, and only refer to the order of indexing.
        Default order is 'C'
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        the flattened array over the specified dimensions.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[1,2], [3,4]])
    >>> startai.flatten(x)
    startai.array([1, 2, 3, 4])

    >>> x = startai.array([[1,2], [3,4]])
    >>> startai.flatten(x, order='F')
    startai.array([1, 3, 2, 4])

    >>> x = startai.array(
        [[[[ 5,  5,  0,  6],
         [17, 15, 11, 16],
         [ 6,  3, 13, 12]],

        [[ 6, 18, 10,  4],
         [ 5,  1, 17,  3],
         [14, 14, 18,  6]]],


       [[[12,  0,  1, 13],
         [ 8,  7,  0,  3],
         [19, 12,  6, 17]],

        [[ 4, 15,  6, 15],
         [ 0,  5, 17,  9],
         [ 9,  3,  6, 19]]],


       [[[17, 13, 11, 16],
         [ 4, 18, 17,  4],
         [10, 10,  9,  1]],

        [[19, 17, 13, 10],
         [ 4, 19, 16, 17],
         [ 2, 12,  8, 14]]]]
         )
    >>> startai.flatten(x, start_dim = 1, end_dim = 2)
    startai.array(
        [[[ 5,  5,  0,  6],
          [17, 15, 11, 16],
          [ 6,  3, 13, 12],
          [ 6, 18, 10,  4],
          [ 5,  1, 17,  3],
          [14, 14, 18,  6]],

         [[12,  0,  1, 13],
          [ 8,  7,  0,  3],
          [19, 12,  6, 17],
          [ 4, 15,  6, 15],
          [ 0,  5, 17,  9],
          [ 9,  3,  6, 19]],

         [[17, 13, 11, 16],
          [ 4, 18, 17,  4],
          [10, 10,  9,  1],
          [19, 17, 13, 10],
          [ 4, 19, 16, 17],
          [ 2, 12,  8, 14]]]))
    """
    if x.shape == ():
        x = startai.reshape(x, (1, -1))[0, :]
    if start_dim == end_dim:
        return startai.inplace_update(out, x) if startai.exists(out) else x
    if start_dim not in range(-len(x.shape), len(x.shape)):
        raise IndexError(
            "Dimension out of range (expected to be in range of"
            f" {[-len(x.shape), len(x.shape) - 1]}, but got {start_dim}"
        )
    if end_dim not in range(-len(x.shape), len(x.shape)):
        raise IndexError(
            "Dimension out of range (expected to be in range of"
            f" {[-len(x.shape), len(x.shape) - 1]}, but got {end_dim}"
        )
    if start_dim < 0:
        start_dim = len(x.shape) + start_dim
    if end_dim < 0:
        end_dim = len(x.shape) + end_dim
    c = 1
    for i in range(start_dim, end_dim + 1):
        c *= x.shape[i]
    lst = [c]
    if start_dim != 0:
        for i in range(0, start_dim):
            lst.insert(i, x.shape[i])
    for i in range(end_dim + 1, len(x.shape)):
        lst.insert(i, x.shape[i])
    return startai.reshape(x, tuple(lst), order=order, out=out)


flatten.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "handle_out_argument",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays", "handle_partial_mixed_function"),
}


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def moveaxis(
    a: Union[startai.Array, startai.NativeArray],
    source: Union[int, Sequence[int]],
    destination: Union[int, Sequence[int]],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> Union[startai.Array, startai.NativeArray]:
    """Move axes of an array to new positions..

    Parameters
    ----------
    a
        The array whose axes should be reordered.
    source
        Original positions of the axes to move. These must be unique.
    destination
        Destination positions for each of the original axes.
        These must also be unique.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Array with moved axes. This array is a view of the input array.

    Examples
    --------
    With :class:`startai.Array` input:
    >>> x = startai.zeros((3, 4, 5))
    >>> startai.moveaxis(x, 0, -1).shape
    (4, 5, 3)
    >>> startai.moveaxis(x, -1, 0).shape
    (5, 3, 4)
    """
    return startai.current_backend().moveaxis(a, source, destination, copy=copy, out=out)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def heaviside(
    x1: Union[startai.Array, startai.NativeArray],
    x2: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute the Heaviside step function for each element in x1.

    Parameters
    ----------
    x1
        input array.
    x2
        values to use where x1 is zero.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        output array with element-wise Heaviside step function of x1.
        This is a scalar if both x1 and x2 are scalars.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x1 = startai.array([-1.5, 0, 2.0])
    >>> x2 = startai.array([0.5])
    >>> startai.heaviside(x1, x2)
    startai.array([0.0000, 0.5000, 1.0000])

    >>> x1 = startai.array([-1.5, 0, 2.0])
    >>> x2 = startai.array([1.2, -2.0, 3.5])
    >>> startai.heaviside(x1, x2)
    startai.array([0., -2., 1.])
    """
    return startai.current_backend().heaviside(x1, x2, out=out)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def flipud(
    m: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> Union[startai.Array, startai.NativeArray]:
    """Flip array in the up/down direction. Flip the entries in each column in
    the up/down direction. Rows are preserved, but appear in a different order
    than before.

    Parameters
    ----------
    m
        The array to be flipped.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Array corresponding to input array with elements
        order reversed along axis 0.

    Examples
    --------
    >>> m = startai.diag([1, 2, 3])
    >>> startai.flipud(m)
    startai.array([[ 0.,  0.,  3.],
        [ 0.,  2.,  0.],
        [ 1.,  0.,  0.]])
    """
    return startai.current_backend().flipud(m, copy=copy, out=out)


@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def vstack(
    arrays: Sequence[startai.Array],
    /,
    *,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> startai.Array:
    """Stack arrays in sequence vertically (row wise).

    Parameters
    ----------
    arrays
        Sequence of arrays to be stacked.

    Returns
    -------
    ret
        The array formed by stacking the given arrays.

    Examples
    --------
    >>> x = startai.array([1, 2, 3])
    >>> y = startai.array([2, 3, 4])
    >>> startai.vstack((x, y))
    startai.array([[1, 2, 3],
           [2, 3, 4]])
    >>> startai.vstack((x, y, x, y))
    startai.array([[1, 2, 3],
               [2, 3, 4],
               [1, 2, 3],
               [2, 3, 4]])

    >>> y = [startai.array([[5, 6]]), startai.array([[7, 8]])]
    >>> print(startai.vstack(y))
    startai.array([[5, 6],
               [7, 8]])
    """
    return startai.current_backend().vstack(arrays, out=out)


@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def hstack(
    arrays: Sequence[startai.Array],
    /,
    *,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> startai.Array:
    """Stack arrays in sequence horizotally (column wise).

    Parameters
    ----------
    arrays
        Sequence of arrays to be stacked.

    Returns
    -------
    ret
        The array formed by stacking the given arrays.

    Examples
    --------
    >>> x = startai.array([1, 2, 3])
    >>> y = startai.array([2, 3, 4])
    >>> startai.hstack((x, y))
    startai.array([1, 2, 3, 2, 3, 4])
    >>> x = startai.array([1, 2, 3])
    >>> y = startai.array([0, 0, 0])
    >>> startai.hstack((x, y, x))
    startai.array([1, 2, 3, 0, 0, 0, 1, 2, 3])
    >>> y = [startai.array([[5, 6]]), startai.array([[7, 8]])]
    >>> print(startai.hstack(y))
    startai.array([[5, 6, 7, 8]])
    """
    return startai.current_backend().hstack(arrays, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def rot90(
    m: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
    k: int = 1,
    axes: Tuple[int, int] = (0, 1),
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Rotate an array by 90 degrees in the plane specified by axes. Rotation
    direction is from the first towards the second axis.

    Parameters
    ----------
    m
        Input array of two or more dimensions.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    k
        Number of times the array is rotated by 90 degrees.
    axes
        The array is rotated in the plane defined by the axes. Axes must be
        different.
    out
        optional output container, for writing the result to. It must have a shape
        that the inputs broadcast to.

    Returns
    -------
    ret
        A rotated view of m.

    Examples
    --------
    With :code:`startai.Array` input:
    >>> m = startai.array([[1,2], [3,4]])
    >>> startai.rot90(m)
    startai.array([[2, 4],
           [1, 3]])
    >>> m = startai.array([[1,2], [3,4]])
    >>> startai.rot90(m, k=2)
    startai.array([[4, 3],
           [2, 1]])
    >>> m = startai.array([[[0, 1],\
                        [2, 3]],\
                       [[4, 5],\
                        [6, 7]]])
    >>> startai.rot90(m, k=2, axes=(1,2))
    startai.array([[[3, 2],
            [1, 0]],

           [[7, 6],
            [5, 4]]])
    With :code:`startai.NativeArray` input:
    >>> m = startai.native_array([[1,2], [3,4]])
    >>> startai.rot90(m)
    startai.array([[2, 4],
           [1, 3]])
    >>> m = startai.native_array([[1,2], [3,4]])
    >>> startai.rot90(m, k=2)
    startai.array([[4, 3],
           [2, 1]])
    >>> m = startai.native_array([[[0, 1],\
                               [2, 3]],\
                              [[4, 5],\
                               [6, 7]]])
    >>> startai.rot90(m, k=2, axes=(1,2))
    startai.array([[[3, 2],
            [1, 0]],

           [[7, 6],
            [5, 4]]])
    """
    return startai.current_backend(m).rot90(m, copy=copy, k=k, axes=axes, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def top_k(
    x: Union[startai.Array, startai.NativeArray],
    k: int,
    /,
    *,
    axis: int = -1,
    largest: bool = True,
    sorted: bool = True,
    out: Optional[tuple] = None,
) -> Tuple[startai.Array, startai.NativeArray]:
    """Return the `k` largest elements of the given input array along a given
    axis.

    Parameters
    ----------
    x
        The array to compute top_k for.
    k
        Number of top elements to return must not exceed the array size.
    axis
        The axis along which we must return the top elements default value is 1.
    largest
        If largest is set to False we return k smallest elements of the array.
    sorted
        If sorted is set to True we return the elements in sorted order.
    out:
        Optional output tuple, for writing the result to. Must have two arrays inside,
        with a shape that the returned tuple broadcast to.

    Returns
    -------
    ret
        A named tuple with values and indices of top k elements.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([2., 1., -3., 5., 9., 0., -4])
    >>> y = startai.top_k(x, 2)
    >>> print(y)
    top_k(values=startai.array([9., 5.]), indices=startai.array([4, 3]))

    >>> x = startai.array([[-2., 3., 4., 0.], [-8., 0., -1., 2.]])
    >>> y = startai.top_k(x, 2, axis=1, largest=False)
    >>> print(y)
    top_k(values=startai.array([[-2.,  0.],
           [-8., -1.]]), indices=startai.array([[0, 3],
           [0, 2]]))

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([2., 1., -3., 5., 9., 0., -4])
    >>> y = startai.top_k(x, 3)
    >>> print(y)
    top_k(values=startai.array([9., 5., 2.]), indices=startai.array([4, 3, 0]))

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([-1, 2, -4]), b=startai.array([4., 5., 0.]))
    >>> y = x.top_k(2)
    >>> print(y)
    [{
        a: startai.array([2, -1]),
        b: startai.array([5., 4.])
    }, {
        a: startai.array([1, 0]),
        b: startai.array([1, 0])
    }]
    """
    return current_backend(x).top_k(
        x, k, axis=axis, largest=largest, sorted=sorted, out=out
    )


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def fliplr(
    m: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> Union[startai.Array, startai.NativeArray]:
    """Flip array in the left/right direction. Flip the entries in each column
    in the left/right direction. Columns are preserved, but appear in a
    different order than before.

    Parameters
    ----------
    m
        The array to be flipped. Must be at least 2-D.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Array corresponding to input array with elements
        order reversed along axis 1.

    Examples
    --------
    >>> m = startai.diag([1, 2, 3])
    >>> startai.fliplr(m)
    startai.array([[0, 0, 1],
           [0, 2, 0],
           [3, 0, 0]])
    """
    return startai.current_backend().fliplr(m, copy=copy, out=out)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def i0(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute the Bessel i0 function of x element-wise.

    Parameters
    ----------
    x
        Array input.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Array with the modified Bessel function
        evaluated at each of the elements of x.

    Examples
    --------
    >>> x = startai.array([1, 2, 3])
    >>> startai.i0(x)
    startai.array([1.26606588, 2.2795853 , 4.88079259])
    """
    return startai.current_backend(x).i0(x, out=out)


def _slice_at_axis(sl, axis):
    return (slice(None),) * axis + (sl,) + (...,)


def _set_pad_area(padded, axis, width_pair, value_pair):
    if width_pair[0] > 0:
        left_slice = _slice_at_axis(slice(None, width_pair[0]), axis)
        padded[left_slice] = value_pair[0]
    if width_pair[1] > 0:
        right_slice = _slice_at_axis(
            slice(padded.shape[axis] - width_pair[1], None), axis
        )
        padded[right_slice] = value_pair[1]
    return padded


def _get_edges(padded, axis, width_pair):
    left_index = width_pair[0]
    left_slice = _slice_at_axis(slice(left_index, left_index + 1), axis)
    left_edge = padded[left_slice]
    right_index = padded.shape[axis] - width_pair[1]
    right_slice = _slice_at_axis(slice(right_index - 1, right_index), axis)
    right_edge = padded[right_slice]
    return left_edge, right_edge


def _get_linear_ramps(padded, axis, width_pair, end_value_pair):
    edge_pair = _get_edges(padded, axis, width_pair)
    if width_pair[0] > 0:
        left_ramp = startai.linspace(
            end_value_pair[0],
            startai.array(edge_pair[0].squeeze(axis=axis)),
            num=width_pair[0],
            endpoint=False,
            dtype=startai.Dtype(str(padded.dtype)),
            axis=axis,
        )
    else:
        left_ramp = startai.empty((0,))
    if width_pair[1] > 0:
        right_ramp = startai.flip(
            startai.linspace(
                end_value_pair[1],
                startai.array(edge_pair[1].squeeze(axis=axis)),
                num=width_pair[1],
                endpoint=False,
                dtype=startai.Dtype(str(padded.dtype)),
                axis=axis,
            ),
            axis=axis,
        )
    else:
        right_ramp = startai.empty((0,))
    return left_ramp, right_ramp


def _get_stats(padded, axis, width_pair, length_pair, stat_func):
    left_index = width_pair[0]
    right_index = padded.shape[axis] - width_pair[1]
    max_length = right_index - left_index
    left_length, right_length = length_pair
    if left_length is None or max_length < left_length:
        left_length = max_length
    if right_length is None or max_length < right_length:
        right_length = max_length
    left_slice = _slice_at_axis(slice(left_index, left_index + left_length), axis)
    left_chunk = padded[left_slice]
    left_chunk = (
        left_chunk.astype("float32") if startai.is_int_dtype(left_chunk) else left_chunk
    )
    left_stat = stat_func(left_chunk, axis=axis, keepdims=True)
    left_stat = (
        startai.round(left_stat).astype(padded.dtype)
        if startai.is_int_dtype(padded)
        else left_stat
    )
    if left_length == right_length == max_length:
        return left_stat, left_stat
    right_slice = _slice_at_axis(slice(right_index - right_length, right_index), axis)
    right_chunk = padded[right_slice]
    right_chunk = (
        right_chunk.astype("float32") if startai.is_int_dtype(right_chunk) else right_chunk
    )
    right_stat = stat_func(right_chunk, axis=axis, keepdims=True)
    right_stat = (
        startai.round(right_stat).astype(padded.dtype)
        if startai.is_int_dtype(padded)
        else right_stat
    )
    return left_stat, right_stat


def _set_reflect_both(padded, axis, width_pair, method, include_edge=False):
    left_pad, right_pad = width_pair
    old_length = padded.shape[axis] - right_pad - left_pad
    if include_edge:
        edge_offset = 1
    else:
        edge_offset = 0
        old_length -= 1
    if left_pad > 0:
        chunk_length = min(old_length, left_pad)
        stop = left_pad - edge_offset
        start = stop + chunk_length
        left_slice = _slice_at_axis(slice(start, stop, -1), axis)
        left_chunk = padded[left_slice]
        if method == "odd":
            edge_slice = _slice_at_axis(slice(left_pad, left_pad + 1), axis)
            left_chunk = 2 * padded[edge_slice] - left_chunk
        start = left_pad - chunk_length
        stop = left_pad
        pad_area = _slice_at_axis(slice(start, stop), axis)
        padded[pad_area] = left_chunk
        left_pad -= chunk_length
    if right_pad > 0:
        chunk_length = min(old_length, right_pad)
        start = -right_pad + edge_offset - 2
        stop = start - chunk_length
        right_slice = _slice_at_axis(slice(start, stop, -1), axis)
        right_chunk = padded[right_slice]
        if method == "odd":
            edge_slice = _slice_at_axis(slice(-right_pad - 1, -right_pad), axis)
            right_chunk = 2 * padded[edge_slice] - right_chunk
        start = padded.shape[axis] - right_pad
        stop = start + chunk_length
        pad_area = _slice_at_axis(slice(start, stop), axis)
        padded[pad_area] = right_chunk
        right_pad -= chunk_length
    return left_pad, right_pad, padded


def _set_wrap_both(padded, axis, width_pair):
    left_pad, right_pad = width_pair
    period = padded.shape[axis] - right_pad - left_pad
    while left_pad > 0:
        right_slice = _slice_at_axis(
            slice(
                -width_pair[1] - min(period, left_pad),
                -width_pair[1] if width_pair[1] != 0 else None,
            ),
            axis,
        )
        right_chunk = padded[right_slice]
        if left_pad > period:
            pad_area = _slice_at_axis(slice(left_pad - period, left_pad), axis)
            left_pad = left_pad - period
        else:
            pad_area = _slice_at_axis(slice(None, left_pad), axis)
            left_pad = 0
        padded[pad_area] = right_chunk
    while right_pad > 0:
        left_slice = _slice_at_axis(
            slice(
                width_pair[0],
                width_pair[0] + min(period, right_pad),
            ),
            axis,
        )
        left_chunk = padded[left_slice]
        if right_pad > period:
            pad_area = _slice_at_axis(slice(-right_pad, -right_pad + period), axis)
            right_pad = right_pad - period
        else:
            pad_area = _slice_at_axis(slice(-right_pad, None), axis)
            right_pad = 0
        padded[pad_area] = left_chunk
    return padded


def _init_pad(array, pad_width, fill_value=None):
    new_shape = tuple(
        left + size + right for size, (left, right) in zip(array.shape, pad_width)
    )
    if fill_value is not None:
        padded = startai.ones(new_shape, dtype=array.dtype) * fill_value
    else:
        padded = startai.zeros(new_shape, dtype=array.dtype)
    original_area_slice = tuple(
        slice(left, left + size) for size, (left, right) in zip(array.shape, pad_width)
    )
    padded[original_area_slice] = array
    return padded


def _to_pairs(x, n, m=2):
    if startai.isscalar(x):
        return ((x,) * m,) * n
    elif len(x) == m and startai.isscalar(x[0]):
        return ((*x[:m],),) * n
    elif len(x) != n:
        startai.utils.assertions.check_equal(
            startai.asarray(list(x)).shape,
            (n, m),
            message=(
                "tuple argument should contain "
                "ndim pairs where ndim is the number of "
                "the input's dimensions"
            ),
            as_array=False,
        )
    return x


def check_scalar(x, force_integer, force_positive):
    return (
        startai.isscalar(x)
        and (startai.is_int_dtype(x) if force_integer else True)
        and (x >= 0 if force_positive else True)
    )


def _check_tuple_arg(arg, arg_name, force_integer=False, force_positive=False):
    if not (
        check_scalar(arg, force_integer, force_positive)
        or (
            isinstance(arg, (tuple, list))
            and (
                all(check_scalar(elem, force_integer, force_positive) for elem in arg)
                or (
                    isinstance(elem, (tuple, list))
                    and all(
                        check_scalar(sub_elem, force_integer, force_positive)
                        for sub_elem in elem
                    )
                )
                for elem in arg
            )
        )
    ):
        if force_integer:
            raise startai.utils.exceptions.StartaiException(
                f"{arg_name} should be int, tuple of ints or tuple of int tuples"
            )
        else:
            raise startai.utils.exceptions.StartaiException(
                f"{arg_name} should be scalar, tuple of scalars or tuple of scalar"
                " tuples"
            )


def _check_arguments(
    mode,
    pad_width,
    stat_length,
    constant_values,
    end_values,
    reflect_type,
):
    supported_modes = [
        "constant",
        "dilated",
        "edge",
        "linear_ramp",
        "maximum",
        "mean",
        "median",
        "minimum",
        "reflect",
        "symmetric",
        "wrap",
        "empty",
    ]
    startai.utils.assertions.check_true(
        callable(mode) or mode in supported_modes,
        message=f"Only modes {supported_modes} are supported. Got {mode}.",
    )
    _check_tuple_arg(
        pad_width, "pad_width", force_positive=mode != "dilated", force_integer=True
    )
    if mode in ["maximum", "mean", "median", "minimum"]:
        _check_tuple_arg(
            stat_length, "stat_length", force_positive=True, force_integer=True
        )
    elif mode in ["constant", "dilated"]:
        _check_tuple_arg(constant_values, "constant_values")
    elif mode == "linear_ramp":
        _check_tuple_arg(end_values, "end_values")
    elif mode in ["reflect", "symmetric"]:
        startai.utils.assertions.check_true(
            reflect_type in ["even", "odd"],
            message=(
                f"Only reflect types ['even', 'odd'] are supported. Got {reflect_type}."
            ),
        )


@handle_exceptions
@handle_nestable
@handle_partial_mixed_function
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def pad(
    input: Union[startai.Array, startai.NativeArray],
    pad_width: Union[Iterable[Tuple[int]], int],
    /,
    *,
    mode: Union[
        Literal[
            "constant",
            "dilated",
            "edge",
            "linear_ramp",
            "maximum",
            "mean",
            "median",
            "minimum",
            "reflect",
            "symmetric",
            "wrap",
            "empty",
        ],
        Callable,
    ] = "constant",
    stat_length: Union[Iterable[Tuple[int]], int] = 1,
    constant_values: Union[Iterable[Tuple[Number]], Number] = 0,
    end_values: Union[Iterable[Tuple[Number]], Number] = 0,
    reflect_type: Literal["even", "odd"] = "even",
    **kwargs: Optional[Any],
) -> startai.Array:
    """Pad an array.

    Parameters
    ----------
    input
        Input array to pad.
    pad_width
        Number of values padded to the edges of each axis.
             - ((before_1, after_1), … (before_N, after_N)) yields unique pad widths
               for each axis.
             - ((before, after),) yields same before and after pad for each axis.
             - pad (integer) is shortcut for before = after = pad width for all axes.
    mode
        One of the following string values or a user-supplied function.
             - "constant": Pads with a constant value.
             - "edge": Pads with the input's edge values.
             - "linear_ramp": Pads with the linear ramp between end_value
               and the input's edge value.
             - "maximum": Pads with the maximum value of all or part of the vector
               along each axis.
             - "mean": Pads with the mean value of all or part of the vector along
               each axis.
             - "median": Pads with the median value of all or part of the vector
               along each axis.
             - "minimum": Pads with the minimum value of all or part of the vector
               along each axis.
             - "reflect": Pads with the reflection mirrored on the first and last
               values of the vector along each axis.
             - "symmetric": Pads with the reflection of the vector mirrored along
               the edge of the input.
             - "wrap": Pads with the wrap of the vector along the axis.
               The first values are used to pad the end and the end values are used
               to pad the beginning.
             - "empty": Pads with undefined values.
             - <function>: Pads with a user-defined padding function. The padding
               function should modify a rank 1 array following the signature
               `padding_func(vector, iaxis_pad_width, iaxis, kwargs)`, where:
                    - `vector` is a rank 1 array already padded with zeros. Padded
                      values are `vector[:iaxis_pad_width[0]]` and
                      `vector[-iaxis_pad_width[1]:]`.
                    - `iaxis_pad_width` is a 2-tuple of ints, where
                      `iaxis_pad_width[0]` represents the number of values padded at
                      the beginning of `vector` and `iaxis_pad_width[1]` represents
                      the number of values padded at the end of `vector`.
                    - `iaxis` is the axis currently being calculated.
                    - `kwargs` is a dict of keyword arguments the function requires.
    stat_length
        Used in "maximum", "mean", "median", and "minimum". Number of values at edge
        of each axis used to calculate the statistic value.
             - ((before_1, after_1), … (before_N, after_N)) yields unique statistic
               lengths for each axis.
             - ((before, after),) yields same before and after statistic lengths for
               each axis.
             - stat_length (integer) is a shortcut for before = after = stat_length
               length for all axes.
             - None uses the entire axis.
    constant_values
        Used in "constant". The values to set the padded values for each axis.
             - ((before_1, after_1), ... (before_N, after_N)) yields unique pad
               constants for each axis.
             - ((before, after),) yields same before and after constants for each axis.
             - constant (integer) is a shortcut for before = after = constant for
               all axes.
    end_values
        Used in "linear_ramp". The values used for the ending value of the linear_ramp
        and that will form the edge of the padded array.
             - ((before_1, after_1), ... (before_N, after_N)) yields unique end values
               for each axis.
             - ((before, after),) yields same before and after end values for each axis
             - end (integer) is a shortcut for before = after = end for all axes.
    reflect_type
        Used in "reflect", and "symmetric". The "even" style is the default with an
        unaltered reflection around the edge value. For the "odd" style, the extended
        part of the array is created by subtracting the reflected values from two
        times the edge value.

    Returns
    -------
    ret
        Padded array of the same rank as the input but with shape increased according
        to pad_width.


    Both the description and the type hints above assume an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[1, 2, 3], [4, 5, 6]])
    >>> padding = ((1, 1), (2, 2))
    >>> y = startai.pad(x, padding, mode="constant", constant_values=0)
    >>> print(y)
    startai.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 2, 3, 0, 0],
               [0, 0, 4, 5, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]])

    >>> x = startai.array([[1, 2, 3], [4, 5, 6]])
    >>> padding = ((1, 1), (2, 2))
    >>> y = startai.pad(x, padding, mode="reflect")
    >>> print(y)
    startai.array([[6, 5, 4, 5, 6, 5, 4],
               [3, 2, 1, 2, 3, 2, 1],
               [6, 5, 4, 5, 6, 5, 4],
               [3, 2, 1, 2, 3, 2, 1]])

    >>> x = startai.array([[1, 2, 3], [4, 5, 6]])
    >>> padding = ((1, 1), (2, 2))
    >>> y = startai.pad(x, padding, mode="symmetric")
    >>> print(y)
    startai.array([[2, 1, 1, 2, 3, 3, 2],
               [2, 1, 1, 2, 3, 3, 2],
               [5, 4, 4, 5, 6, 6, 5],
               [5, 4, 4, 5, 6, 6, 5]])

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([[1, 2, 3], [4, 5, 6]])
    >>> padding = ((1, 1), (2, 2))
    >>> y = startai.pad(x, padding, mode="constant", constant_values=7)
    >>> print(y)
    startai.array([[7, 7, 7, 7, 7, 7, 7],
               [7, 7, 1, 2, 3, 7, 7],
               [7, 7, 4, 5, 6, 7, 7],
               [7, 7, 7, 7, 7, 7, 7]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0, 1, 2]), b=startai.array([4, 5, 6]))
    >>> padding = (1, 1)
    >>> y = startai.pad(x, padding, mode="constant")
    >>> print(y)
    {
        a: startai.array([0, 0, 1, 2, 0]),
        b: startai.array([0, 4, 5, 6, 0])
    }
    """
    _check_arguments(
        mode,
        pad_width,
        stat_length,
        constant_values,
        end_values,
        reflect_type,
    )
    ndim = input.ndim
    if mode == "dilated":
        pad_width = _to_pairs(pad_width, ndim, m=3)
        if not startai.is_array(constant_values) or constant_values.dtype != input.dtype:
            constant_values = startai.asarray(constant_values, dtype=input.dtype)
        return _interior_pad(input, constant_values, pad_width)
    pad_width = _to_pairs(pad_width, len(input.shape))
    if callable(mode):
        func = mode
        padded = _init_pad(input, pad_width, fill_value=0)
        for axis in range(ndim):
            padded = startai.moveaxis(padded, axis, -1)
            inds = startai.ndindex(padded.shape[:-1])
            for ind in inds:
                padded[ind] = func(padded[ind], pad_width[axis], axis, kwargs)
        return padded
    padded = _init_pad(input, pad_width)
    stat_functions = {
        "maximum": startai.max,
        "minimum": startai.min,
        "mean": startai.mean,
        "median": startai.median,
    }
    if mode == "constant":
        constant_values = _to_pairs(constant_values, ndim)
        for axis, (width_pair, value_pair) in enumerate(
            zip(pad_width, constant_values)
        ):
            padded = _set_pad_area(padded, axis, width_pair, value_pair)
    elif mode == "empty":
        pass
    elif mode == "edge":
        for axis, width_pair in enumerate(pad_width):
            edge_pair = _get_edges(padded, axis, width_pair)
            padded = _set_pad_area(padded, axis, width_pair, edge_pair)
    elif mode == "linear_ramp":
        end_values = _to_pairs(end_values, ndim)
        for axis, (width_pair, value_pair) in enumerate(zip(pad_width, end_values)):
            ramp_pair = _get_linear_ramps(padded, axis, width_pair, value_pair)
            padded = _set_pad_area(padded, axis, width_pair, ramp_pair)
    elif mode in stat_functions:
        func = stat_functions[mode]
        stat_length = _to_pairs(stat_length, ndim)
        for axis, (width_pair, length_pair) in enumerate(zip(pad_width, stat_length)):
            stat_pair = _get_stats(padded, axis, width_pair, length_pair, func)
            padded = _set_pad_area(padded, axis, width_pair, stat_pair)
    elif mode in {"reflect", "symmetric"}:
        include_edge = True if mode == "symmetric" else False
        for axis, (left_index, right_index) in enumerate(pad_width):
            if input.shape[axis] == 1 and (left_index > 0 or right_index > 0):
                edge_pair = _get_edges(padded, axis, (left_index, right_index))
                padded = _set_pad_area(
                    padded, axis, (left_index, right_index), edge_pair
                )
                continue
            while left_index > 0 or right_index > 0:
                left_index, right_index, padded = _set_reflect_both(
                    padded, axis, (left_index, right_index), reflect_type, include_edge
                )
    elif mode == "wrap":
        for axis, (left_index, right_index) in enumerate(pad_width):
            padded = _set_wrap_both(padded, axis, (left_index, right_index))
    return padded


pad.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@to_native_arrays_and_back
@handle_array_function
@handle_device
def vsplit(
    ary: Union[startai.Array, startai.NativeArray],
    indices_or_sections: Union[int, Sequence[int], startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[startai.Array]:
    """Split an array vertically into multiple sub-arrays.

    Parameters
    ----------
    ary
        Array input.
    indices_or_sections
        If indices_or_sections is an integer n, the array is split into n
        equal sections, provided that n must be a divisor of the split axis.
        If indices_or_sections is a sequence of ints or 1-D array,
        then input is split at each of the indices.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.

    Returns
    -------
    ret
        input array split vertically.

    Examples
    --------
    >>> ary = startai.array(
        [[[0.,  1.],
          [2.,  3.]],
         [[4.,  5.],
          [6.,  7.]]]
        )
    >>> startai.vsplit(ary, 2)
    [startai.array([[[0., 1.], [2., 3.]]]), startai.array([[[4., 5.], [6., 7.]]])])
    """
    return startai.current_backend(ary).vsplit(ary, indices_or_sections, copy=copy)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@to_native_arrays_and_back
@handle_device
def dsplit(
    ary: Union[startai.Array, startai.NativeArray],
    indices_or_sections: Union[int, Sequence[int], startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[startai.Array]:
    """Split an array into multiple sub-arrays along the 3rd axis.

    Parameters
    ----------
    ary
        Array input.
    indices_or_sections
        If indices_or_sections is an integer n, the array is split into n sections.
        If the array is divisible by n along the 3rd axis, each section will be of
        equal size. If input is not divisible by n, the sizes of the first
        int(ary.size(0) % n) sections will have size int(ary.size(0) / n) + 1, and
        the rest will have size int(ary.size(0) / n).
        If indices_or_sections is a sequence of ints or 1-D array,
        then input is split at each of the indices.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.

    Returns
    -------
    ret
        input array split along the 3rd axis.

    Examples
    --------
    >>> ary = startai.array(
        [[[ 0.,   1.,   2.,   3.],
          [ 4.,   5.,   6.,   7.]],
         [[ 8.,   9.,  10.,  11.],
          [12.,  13.,  14.,  15.]]]
        )
    >>> startai.dsplit(ary, 2)
    [startai.array([[[ 0.,  1.], [ 4.,  5.]], [[ 8.,  9.], [12., 13.]]]),
     startai.array([[[ 2.,  3.], [ 6.,  7.]], [[10., 11.], [14., 15.]]])]
    """
    return startai.current_backend(ary).dsplit(ary, indices_or_sections, copy=copy)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@to_native_arrays_and_back
@handle_device
def atleast_1d(
    *arys: Union[startai.Array, startai.NativeArray, bool, Number],
    copy: Optional[bool] = None,
) -> List[startai.Array]:
    """Convert inputs to arrays with at least one dimension. Scalar inputs are
    converted to 1-dimensional arrays, whilst higher-dimensional inputs are
    preserved.

    Parameters
    ----------
    arys
        One or more input arrays.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.

    Returns
    -------
    ret
        An array, or list of arrays, each with at least 1D.
        Copies are made only if necessary.

    Examples
    --------
    >>> ary1 = startai.array(5)
    >>> startai.atleast_1d(ary1)
    startai.array([5])
    >>> ary2 = startai.array([[3,4]])
    >>> startai.atleast_1d(ary2)
    startai.array([[3, 4]])
    >>> startai.atleast_1d(6,7,8)
    [startai.array([6]), startai.array([7]), startai.array([8])]
    """
    return startai.current_backend().atleast_1d(*arys, copy=copy)


@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def dstack(
    arrays: Sequence[startai.Array],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Stack arrays in sequence depth wise (along third axis).

    Parameters
    ----------
    arrays
        Sequence of arrays to be stacked.

    Returns
    -------
    ret
        The array formed by stacking the given arrays.

    Examples
    --------
    >>> x = startai.array([1, 2, 3])
    >>> y = startai.array([2, 3, 4])
    >>> startai.dstack((x, y))
    startai.array([[[1, 2],
                [2, 3],
                [3, 4]]])
    >>> x = startai.array([[1], [2], [3]])
    >>> y = startai.array([[2], [3], [4]])
    >>> startai.dstack((x, y))
    startai.array([[[1, 2]],
               [[2, 3]],
               [[3, 4]]])
    """
    return startai.current_backend().dstack(arrays, out=out)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@to_native_arrays_and_back
@handle_device
def atleast_2d(
    *arys: Union[startai.Array, startai.NativeArray],
    copy: Optional[bool] = None,
) -> List[startai.Array]:
    """Convert inputs to arrays with at least two dimension. Scalar inputs are
    converted to 2-dimensional arrays, whilst higher-dimensional inputs are
    preserved.

    Parameters
    ----------
    arys
        One or more array-like sequences. Non-array inputs are
        converted to arrays. Arrays that already have two or more
        dimensions are preserved.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.

    Returns
    -------
    ret
        An array, or list of arrays, each with at least 2D.
        Copies are made only if necessary.

    Examples
    --------
    >>> ary1 = startai.array(5)
    >>> startai.atleast_2d(ary1)
    startai.array([[5]])
    >>> ary2 = startai.array([[[3,4]]])
    >>> startai.atleast_2d(ary2)
    startai.array([[[3, 4]]])
    >>> startai.atleast_2d(6,7,8)
    [startai.array([[6]]), startai.array([[7]]), startai.array([[8]])]
    """
    return startai.current_backend().atleast_2d(*arys, copy=copy)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@to_native_arrays_and_back
@handle_device
def atleast_3d(
    *arys: Union[startai.Array, startai.NativeArray, bool, Number],
    copy: Optional[bool] = None,
) -> List[startai.Array]:
    """Convert inputs to arrays with at least three dimension. Scalar inputs
    are converted to 3-dimensional arrays, whilst higher-dimensional inputs are
    preserved.

    Parameters
    ----------
    arys
        One or more array-like sequences. Non-array inputs are
        converted to arrays. Arrays that already have three or more
        dimensions are preserved.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.

    Returns
    -------
    ret
        An array, or list of arrays, each with a.ndim >= 3. Copies
        are avoided where possible, and views with three or more
        dimensions are returned. For example, a 1-D array of shape
        (N,) becomes a view of shape (1, N, 1), and a 2-D array of
        shape (M, N) becomes a view of shape (M, N, 1).

    Examples
    --------
    >>> ary1 = startai.array([5,6])
    >>> startai.atleast_3d(ary1)
    startai.array([[[5],
            [6]]])
    >>> ary2 = startai.array([[[3,4]]])
    >>> startai.atleast_3d(ary2)
    startai.array([[[3, 4]]])
    >>> ary3 = startai.array([[3,4],[9,10]])
    >>> startai.atleast_3d(6,7,ary3)
    [startai.array([[[6]]]), startai.array([[[7]]]), startai.array([[[ 3],
            [ 4]],

           [[ 9],
            [10]]])]
    """
    return startai.current_backend().atleast_3d(*arys, copy=copy)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def take_along_axis(
    arr: Union[startai.Array, startai.NativeArray],
    indices: Union[startai.Array, startai.NativeArray],
    axis: int,
    /,
    *,
    mode: str = "fill",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Take values from the input array by matching 1d index and data slices.

    Parameters
    ----------
    arr
        The source array.
    indices
        The indices of the values to extract.
    axis
        The axis over which to select values.
        If axis is None, arr is treated as a flattened 1D array.
    mode
        One of: 'clip', 'fill', 'drop'. Parameter controlling how out-of-bounds indices
        will be handled.
    out
        The output array.

    Returns
    -------
    ret
        The returned array has the same shape as `indices`.

    Examples
    --------
    >>> arr = startai.array([[4, 3, 5], [1, 2, 1]])
    >>> indices = startai.array([[0, 1, 1], [2, 0, 0]])
    >>> y = startai.take_along_axis(arr, indices, 1)
    >>> print(y)
    startai.array([[4, 3, 3], [1, 1, 1]])
    """
    return startai.current_backend(arr).take_along_axis(
        arr, indices, axis, mode=mode, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@to_native_arrays_and_back
@handle_array_function
@handle_device
def hsplit(
    ary: Union[startai.Array, startai.NativeArray],
    indices_or_sections: Union[int, Sequence[int], startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[startai.Array]:
    """Split an array into multiple sub-arrays horizontally.

    Parameters
    ----------
    ary
        Array input.
    indices_or_sections
        If indices_or_sections is an integer n, the array is split into n
        equal sections, provided that n must be a divisor of the split axis.
        If indices_or_sections is a tuple of ints, then input is split at each of
        the indices in the tuple.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.

    Returns
    -------
    ret
        input array split horizontally.

    Examples
    --------
    >>> ary = startai.array(
            [[0.,  1., 2., 3.],
             [4.,  5., 6,  7.],
             [8.,  9., 10., 11.],
             [12., 13., 14., 15.]]
            )
    >>> startai.hsplit(ary, 2)
        [startai.array([[ 0.,  1.],
                    [ 4.,  5.],
                    [ 8.,  9.],
                    [12., 13.]]),
         startai.array([[ 2.,  3.],
                    [ 6.,  7.],
                    [10., 11.],
                    [14., 15.]])]
    """
    return startai.current_backend(ary).hsplit(ary, indices_or_sections, copy=copy)


@handle_exceptions
@inputs_to_native_shapes
def broadcast_shapes(*shapes: Union[List[int], List[Tuple]]) -> Tuple[int]:
    """Broadcasts shapes.

    Parameters
    ----------
    shapes
        The shapes to broadcast.

    Returns
    -------
    ret
        The broadcasted shape.

    Examples
    --------
    >>> x = [(3, 3), (3, 1)]
    >>> print(startai.broadcast_shapes(*x))
    (3, 3)

    >>> print(startai.broadcast_shapes(*[(3, 3),(3, 1),(1, 3)]))
    (3, 3)
    """
    return startai.current_backend().broadcast_shapes(*shapes)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@inputs_to_native_shapes
@to_native_arrays_and_back
@handle_device
def expand(
    x: Union[startai.Array, startai.NativeArray],
    shape: Union[startai.Shape, startai.NativeShape],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Broadcast the input Array following the given shape and the broadcast
    rule.

    Parameters
    ----------
    x
        Array input.
    shape
        A 1-D Array indicates the shape you want to expand to,
        following the broadcast rule.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Output Array
    """
    return startai.current_backend(x).expand(x, shape, out=out, copy=copy)


# ToDo: add 'mean' modes to scatter_nd and then to put_along_axis
@inputs_to_startai_arrays
@handle_array_like_without_promotion
@handle_partial_mixed_function
@handle_nestable
@handle_exceptions
def put_along_axis(
    arr: Union[startai.Array, startai.NativeArray],
    indices: Union[startai.Array, startai.NativeArray],
    values: Union[startai.Array, startai.NativeArray],
    axis: int,
    /,
    *,
    mode: Literal["sum", "min", "max", "mul", "mean", "replace"] = "replace",
    out: Optional[startai.Array] = None,
) -> None:
    """Put values into the input array by matching 1d index and data slices
    along a specified axis.

    Parameters
    ----------
    arr : array_like
        The input array to modify.
    indices : array_like
        The indices of the values to put into `arr`.
    values : array_like
        The values to put into `arr`.
    axis : int
        The axis over which to put the `values`.
    mode : {'sum', 'min', 'max', 'mul', 'replace'}
        The reduction operation to apply.
    out : ndarray, optional
        Output array in which to place the result.
        If not specified, a new array is created.

    Note
    ----
    In case `indices` contains duplicates, the updates get accumulated in each place.

    Returns
    -------
    None

    Examples
    --------
    >>> arr = startai.array([[4, 3, 5], [1, 2, 1]])
    >>> indices = startai.array([[0, 1, 1], [2, 0, 0]])
    >>> values = startai.array([[9, 8, 7], [6, 5, 4]])
    >>> startai.put_along_axis(arr, indices, values, 1, mode='replace')
    >>> print(arr)
    startai.array([[9, 7, 5],
               [4, 2, 6]])

    >>> arr = startai.array([[10, 30, 20], [60, 40, 50]])
    >>> axis = 1
    >>> indices = startai.argmax(arr, axis=axis, keepdims=True)
    >>> value = 100
    >>> startai.put_along_axis(arr, indices, value, axis, mode='sum')
    >>> print(arr)
    startai.array([[10, 30, 20],
              [60, 40, 50]])
    """
    arr_shape = arr.shape

    # array containing all flat indices
    arr_ = startai.arange(0, _numel(arr_shape)).reshape(arr_shape)

    # use take_along_axis to get the queried indices
    arr_idxs = startai.take_along_axis(arr_, indices, axis)

    # convert the flat indices to multi-D indices
    arr_idxs = startai.unravel_index(arr_idxs, arr_shape)

    # stack the multi-D indices to bring them to scatter_nd format
    arr_idxs = startai.stack(arr_idxs, axis=-1).astype(startai.int64)

    ret = startai.scatter_nd(arr_idxs, values, reduction=mode, out=startai.copy_array(arr))
    return startai.inplace_update(out, ret) if startai.exists(out) else ret


put_along_axis.mixed_backend_wrappers = {
    "to_add": (
        "handle_out_argument",
        "outputs_to_startai_arrays",
        "inputs_to_native_arrays",
    ),
    "to_skip": "handle_partial_mixed_function",
}


def _check_bounds(shape0, shape1, strides1, itemsize):
    numel0 = math.prod(shape0)
    ndim1 = len(shape1)
    return (
        sum((shape1[i] - 1) * strides1[i] for i in range(ndim1)) + itemsize
        <= numel0 * itemsize
    )


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@inputs_to_native_shapes
def as_strided(
    x: Union[startai.Array, startai.NativeArray],
    shape: Union[startai.Shape, startai.NativeShape, Sequence[int]],
    strides: Sequence[int],
    /,
) -> startai.Array:
    """Create a copy of the input array with the given shape and strides.

    Parameters
    ----------
    x
        Input Array.
    shape
        The shape of the new array.
    strides
        The strides of the new array (specified in bytes).

    Returns
    -------
    ret
        Output Array

    Examples
    --------
    >>> x = startai.array([1, 2, 3, 4, 5, 6])
    >>> startai.as_strided(x, (4, 3), (8, 8))
    startai.array([[1, 2, 3],
       [2, 3, 4],
       [3, 4, 5],
       [4, 5, 6]])
    """
    itemsize = x.itemsize
    if not _check_bounds(x.shape, shape, strides, itemsize):
        raise startai.exceptions.StartaiException("attempted unsafe memory access")
    if any(strides[i] % itemsize != 0 for i in range(len(strides))):
        raise startai.exceptions.StartaiException("strides must be multiple of itemsize")

    src = memoryview(startai.to_numpy(x)).cast("b")

    src_ind = startai.inner(
        startai.indices(shape).reshape((len(shape), -1)).T,
        startai.array(strides),
    )
    src_ind = startai.expand_dims(src_ind, axis=-1)
    src_ind = src_ind + startai.arange(itemsize)
    src_ind = startai.reshape(src_ind, (-1,)).to_numpy()

    temp_list = [src[i] for i in src_ind]
    temp_array = startai.asarray(temp_list, dtype=startai.int8)
    result = bytearray(temp_array.to_numpy())

    return startai.reshape(
        startai.frombuffer(result, dtype=x.dtype, count=math.prod(shape)),
        shape,
    )


as_strided.unsupported_dtypes = ("bfloat16",)
as_strided.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def concat_from_sequence(
    input_sequence: Union[
        Tuple[Union[startai.Array, startai.NativeArray]],
        List[Union[startai.Array, startai.NativeArray]],
    ],
    /,
    *,
    new_axis: int = 0,
    axis: int = 0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Concatenate a sequence of arrays along a new or an existing axis.

    Parameters
    ----------
    input_sequence
        A sequence of arrays.
    new_axis
        Insert and concatenate on a new axis or not,
        default 0 means do not insert new axis.
        new_axis = 0: concatenate
        new_axis = 1: stack
    axis
        axis along which the arrays will be concatenated.

    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Output Array
    """
    return current_backend(input_sequence).concat_from_sequence(
        input_sequence, new_axis=new_axis, axis=axis, out=out
    )


def _slice(operand, start_indices, limit_indices, strides=None):
    strides = [1] * len(operand.shape) if strides is None else strides

    full_slice = ()
    for i, _ in enumerate(operand.shape):
        strides_i = int(strides[i])
        start_i = int(start_indices[i])
        limit_i = int(limit_indices[i])
        full_slice += (slice(start_i, limit_i, strides_i),)
    return operand[full_slice]


def _slice_along_axis(x, start=0, stop=None, stride=1, axis=0):
    if axis >= 0:
        slices = [slice(None)] * axis + [slice(start, stop, stride)]
    else:
        slices = [Ellipsis, slice(start, stop, stride)] + [slice(None)] * (-1 - axis)
    return x[tuple(slices)]


def _interior_pad(operand, padding_value, padding_config):
    for axis, (_, _, interior) in enumerate(padding_config):
        if interior > 0:
            new_shape = list(operand.shape)
            new_shape[axis] = new_shape[axis] + (new_shape[axis] - 1) * interior
            new_array = startai.full(new_shape, padding_value, dtype=operand.dtype)
            src_indices = startai.arange(operand.shape[axis])
            dst_indices = src_indices * (interior + 1)
            index_tuple = [slice(None)] * operand.ndim
            index_tuple[axis] = dst_indices
            new_array[tuple(index_tuple)] = operand
            operand = new_array

    start_indices = [0] * operand.ndim
    limit_indices = [0] * operand.ndim
    for axis, (low, high, _) in enumerate(padding_config):
        if low < 0:
            start_indices[axis] = abs(low)
        if high < 0:
            limit_indices[axis] = high
        else:
            limit_indices[axis] = operand.shape[axis] + 1
    padded = _slice(operand, start_indices, limit_indices)

    pad_width = [(0, 0)] * operand.ndim
    for axis, (low, high, _) in enumerate(padding_config):
        if low > 0 and high > 0:
            pad_width[axis] = (low, high)
        elif low > 0:
            pad_width[axis] = (low, 0)
        elif high > 0:
            pad_width[axis] = (0, high)
    padded = startai.constant_pad(padded, pad_width, value=padding_value)
    return padded


def _interleave(a, b, axis):
    assert a.shape[axis] in [b.shape[axis], b.shape[axis] + 1]
    a_pad = [(0, 0, 0)] * a.ndim
    b_pad = [(0, 0, 0)] * b.ndim
    a_pad[axis] = (0, 1 if a.shape[axis] == b.shape[axis] else 0, 1)
    b_pad[axis] = (1, 0 if a.shape[axis] == b.shape[axis] else 1, 1)
    a = _interior_pad(a, 0.0, a_pad)
    b = _interior_pad(b, 0.0, b_pad)
    return startai.add(a, b)


@handle_exceptions
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
def associative_scan(
    x: Union[startai.Array, startai.NativeArray],
    fn: Callable,
    /,
    *,
    reverse: bool = False,
    axis: int = 0,
) -> startai.Array:
    """Perform an associative scan over the given array.

    Parameters
    ----------
    x
        The array to scan over.
    fn
        The associative function to apply.
    reverse
        Whether to scan in reverse with respect to the given axis.
    axis
        The axis to scan over.

    Returns
    -------
    ret
        The result of the scan.
    """
    elems = [x]

    if reverse:
        elems = [startai.flip(elem, axis=[axis]) for elem in elems]

    def _combine(a, b):
        a = a[0]
        b = b[0]
        if a.shape[axis] == 0:
            return [a]
        c = fn(a, b)
        return [c]

    def _scan(elems):
        num_elems = elems[0].shape[axis]

        if num_elems < 2:
            return elems

        reduced_elems = _combine(
            [_slice_along_axis(elem, 0, -1, stride=2, axis=axis) for elem in elems],
            [_slice_along_axis(elem, 1, None, stride=2, axis=axis) for elem in elems],
        )

        odd_elems = _scan(reduced_elems)

        if num_elems % 2 == 0:
            even_elems = _combine(
                [_slice_along_axis(e, 0, -1, axis=axis) for e in odd_elems],
                [_slice_along_axis(e, 2, None, stride=2, axis=axis) for e in elems],
            )
        else:
            even_elems = _combine(
                odd_elems,
                [_slice_along_axis(e, 2, None, stride=2, axis=axis) for e in elems],
            )
        even_elems = [
            startai.concat([_slice_along_axis(elem, 0, 1, axis=axis), result], axis=axis)
            for (elem, result) in zip(elems, even_elems)
        ]
        return list(map(partial(_interleave, axis=axis), even_elems, odd_elems))

    scans = _scan(elems)

    if reverse:
        scans = [startai.flip(scanned, axis=[axis]) for scanned in scans]

    return startai.reshape(startai.asarray(scans), elems[0].shape)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@to_native_arrays_and_back
@handle_array_function
@handle_device
def unique_consecutive(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[int] = None,
) -> Tuple[
    Union[startai.Array, startai.NativeArray],
    Union[startai.Array, startai.NativeArray],
    Union[startai.Array, startai.NativeArray],
]:
    """Eliminates all but the first element from every consecutive group of
    equivalent elements in ``x``.

    Parameters
    ----------
    x
        input array.

    axis
        the axis to apply unique on. If None, unique is applied on flattened ``x``.

    Returns
    -------
    ret
        a namedtuple ``(output, inverse_indices, counts)`` whose
        - first element has the field name ``output`` and is an array
          containing ``x`` with its equivalent consecutive elements eliminated.
        - second element has the field name ``inverse_indices`` and is an
          array containing the indices of ``output`` that reconstruct ``x``.
        - third element has the field name ``counts`` and is an array
          containing the number of occurrences for each unique value or array in ``x``.


    Examples
    --------
    With :class:`startai.Array` input:
    >>> x = startai.array([1, 1, 2, 2, 3, 1, 1, 2])
    >>> startai..unique_consecutive(x)
    Results(values=startai.array([1, 2, 3, 1, 2]),
        inverse_indices=startai.array([0, 0, 1, 1, 2, 3, 3, 4]),
        counts=startai.array([2, 2, 1, 2, 1]))
    """
    return startai.current_backend(x).unique_consecutive(x, axis=axis)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def fill_diagonal(
    a: Union[startai.Array, startai.NativeArray],
    v: Union[int, float, startai.Array, startai.NativeArray],
    /,
    *,
    wrap: bool = False,
) -> Union[startai.Array, startai.NativeArray]:
    """Fill the main diagonal of the given array of any dimensionality..

    Parameters
    ----------
    a
        Array at least 2D.
    v
        Value(s) to write on the diagonal. If val is scalar, the
        value is written along the diagonal. If array-like, the
        flattened val is written along the diagonal, repeating if
        necessary to fill all diagonal entries.

    wrap
        The diagonal 'wrapped' after N columns for tall matrices.

    Returns
    -------
    ret
        Array with the diagonal filled.
    """
    shape = a.shape
    max_end = startai.prod(startai.array(shape))
    end = max_end
    if len(shape) == 2:
        step = shape[1] + 1
        if not wrap:
            end = shape[1] * shape[1]
    else:
        step = int(1 + (startai.cumprod(startai.array(shape[:-1]), axis=0)).sum())
    end = int(min(end, max_end))
    a = startai.reshape(a, (-1,))
    steps = startai.arange(0, end, step)
    if isinstance(v, (startai.Array, startai.NativeArray)):
        v = startai.reshape(v, (-1,)).astype(a.dtype)
        v = startai.tile(v, int(startai.ceil(len(steps) / v.shape[0])))[: len(steps)]
    else:
        v = startai.repeat(v, len(steps))
    startai.scatter_flat(steps, v, size=a.shape[0], reduction="replace", out=a)
    a = startai.reshape(a, shape)
    return a


fill_diagonal.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}


@handle_nestable
@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def unfold(
    x: Union[startai.Array, startai.NativeArray],
    /,
    mode: int = 0,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return the mode-`mode` unfolding of `tensor` with modes starting at `0`.

    Parameters
    ----------
    x
        input tensor to be unfolded
    mode
        indexing starts at 0, therefore mode is in ``range(0, tensor.ndim)``
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        unfolded_tensor of shape ``(tensor.shape[mode], -1)``
    """
    return startai.reshape(startai.moveaxis(x, mode, 0), (x.shape[mode], -1), out=out)


@handle_nestable
@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def fold(
    x: Union[startai.Array, startai.NativeArray],
    /,
    mode: int,
    shape: Union[startai.Shape, startai.NativeShape, Sequence[int]],
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Refolds the mode-`mode` unfolding into a tensor of shape `shape` In
    other words, refolds the n-mode unfolded tensor into the original tensor of
    the specified shape.

    Parameters
    ----------
    input
        unfolded tensor of shape ``(shape[mode], -1)``
    mode
        the mode of the unfolding
    shape
        shape of the original tensor before unfolding
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        folded_tensor of shape `shape`
    """
    full_shape = list(shape)
    mode_dim = full_shape.pop(mode)
    full_shape.insert(0, mode_dim)
    return startai.moveaxis(startai.reshape(x, full_shape), 0, mode, out=out)


@handle_nestable
@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def partial_unfold(
    x: Union[startai.Array, startai.NativeArray],
    /,
    mode: int = 0,
    skip_begin: int = 1,
    skip_end: int = 0,
    ravel_tensors: bool = False,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Partial unfolding of a tensor while ignoring the specified number of
    dimensions at the beginning and the end. For instance, if the first
    dimension of the tensor is the number of samples, to unfold each sample,
    set skip_begin=1. This would, for each i in ``range(tensor.shape[0])``,
    unfold ``tensor[i, ...]``.

    Parameters
    ----------
    x
        tensor of shape n_samples x n_1 x n_2 x ... x n_i
    mode
        indexing starts at 0, therefore mode is in range(0, tensor.ndim)
    skip_begin
        number of dimensions to leave untouched at the beginning
    skip_end
        number of dimensions to leave untouched at the end
    ravel_tensors
        if True, the unfolded tensors are also flattened
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        partially unfolded tensor
    """
    if ravel_tensors:
        new_shape = [-1]
    else:
        new_shape = [x.shape[mode + skip_begin], -1]

    if skip_begin:
        new_shape = [x.shape[i] for i in range(skip_begin)] + new_shape

    if skip_end:
        new_shape += [x.shape[-i] for i in range(1, 1 + skip_end)]

    return startai.reshape(
        startai.moveaxis(x, mode + skip_begin, skip_begin), new_shape, out=out
    )


@handle_nestable
@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def partial_fold(
    x: Union[startai.Array, startai.NativeArray],
    /,
    mode: int,
    shape: Union[startai.Shape, startai.NativeShape, Sequence[int]],
    skip_begin: int = 1,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Re-folds a partially unfolded tensor.

    Parameters
    ----------
    x
        a partially unfolded tensor
    mode
        indexing starts at 0, therefore mode is in range(0, tensor.ndim)
    shape
        the shape of the original full tensor (including skipped dimensions)
    skip_begin
        number of dimensions left untouched at the beginning
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        partially re-folded tensor
    """
    transposed_shape = list(shape)
    mode_dim = transposed_shape.pop(skip_begin + mode)
    transposed_shape.insert(skip_begin, mode_dim)
    return startai.moveaxis(
        startai.reshape(x, transposed_shape), skip_begin, skip_begin + mode, out=out
    )


@handle_nestable
@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def partial_tensor_to_vec(
    x: Union[startai.Array, startai.NativeArray],
    /,
    skip_begin: int = 1,
    skip_end: int = 0,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Partial vectorization of a tensor while ignoring the specified dimension
    at the beginning and the end.

    Parameters
    ----------
    x
        tensor to partially vectorise
    skip_begin
        number of dimensions to leave untouched at the beginning
    skip_end
        number of dimensions to leave untouched at the end
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        partially vectorised tensor with the
        `skip_begin` first and `skip_end` last dimensions untouched
    """
    return partial_unfold(
        x,
        mode=0,
        skip_begin=skip_begin,
        skip_end=skip_end,
        ravel_tensors=True,
        out=out,
    )


@handle_nestable
@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def partial_vec_to_tensor(
    x: Union[startai.Array, startai.NativeArray],
    /,
    shape: Union[startai.Shape, startai.NativeShape, Sequence[int]],
    skip_begin: int = 1,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Refolds a partially vectorised tensor into a full one.

    Parameters
    ----------
    x
        a partially vectorised tensor
    shape
        the shape of the original full tensor (including skipped dimensions)
    skip_begin
        number of dimensions to leave untouched at the beginning
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        full tensor
    """
    return partial_fold(x, mode=0, shape=shape, skip_begin=skip_begin, out=out)


@handle_nestable
@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def matricize(
    x: Union[startai.Array, startai.NativeArray],
    /,
    row_modes: Sequence[int],
    column_modes: Optional[Sequence[int]] = None,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Matricizes the given tensor.

    Parameters
    ----------
    x
        the input tensor
    row_modes
        modes to use as row of the matrix (in the desired order)
    column_modes
        modes to use as column of the matrix, in the desired order
        if None, the modes not in `row_modes` will be used in ascending order
    out
        optional output array, for writing the result to.

    ret
    -------
        startai.Array : tensor of size (startai.prod(x.shape[i] for i in row_modes), -1)
    """
    ndims = len(x.shape)
    row_indices = list(row_modes)

    if column_modes:
        column_indices = list(column_modes)
    else:
        column_indices = [i for i in range(ndims) if i not in row_indices]
        if sorted(column_indices + row_indices) != list(range(ndims)):
            msg = (
                "If you provide both column and row modes for the matricization then"
                " column_modes + row_modes must contain all the modes of the tensor."
                f" Yet, got row_modes={row_modes} and column_modes={column_modes}."
            )
            raise ValueError(msg)

    row_size, column_size = 1, 1
    row_size = int(startai.prod([x.shape[i] for i in row_indices]))
    column_size = int(startai.prod([x.shape[i] for i in column_indices]))

    return startai.reshape(
        startai.permute_dims(x, row_indices + column_indices),
        (row_size, column_size),
        out=out,
    )


@handle_nestable
@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def soft_thresholding(
    x: Union[startai.Array, startai.NativeArray],
    /,
    threshold: Union[float, startai.Array, startai.NativeArray],
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Soft-thresholding operator.

        sign(tensor) * max[abs(tensor) - threshold, 0]

    Parameters
    ----------
    x
      input array
    threshold
          float or array with shape tensor.shape
        * If float the threshold is applied to the whole tensor
        * If array, one threshold is applied per elements, 0 values are ignored
    out
        optional output array, for writing the result to.

    Returns
    -------
    startai.Array
        thresholded tensor on which the operator has been applied

    Examples
    --------
    Basic shrinkage

    >>> x = startai.array([[1, -2, 1.5], [-4, 3, -0.5]])
    >>> soft_thresholding(x, 1.1)
    array([[ 0. , -0.9,  0.4],
           [-2.9,  1.9,  0. ]])


    Example with missing values

    >>> mask = startai.array([[0, 0, 1], [1, 0, 1]])
    >>> soft_thresholding(x, mask*1.1)
    array([[ 1. , -2. ,  0.4],
           [-2.9,  3. ,  0. ]])
    """
    res = startai.abs(x) - threshold
    res = startai.where(res < 0.0, 0.0, res) * startai.sign(x)

    if startai.exists(out):
        return startai.inplace_update(out, res)
    return res


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def choose(
    arr: Union[startai.Array, startai.NativeArray],
    choices: Union[startai.Array, startai.NativeArray],
    /,
    *,
    out: None = None,
    mode: Union[str, None] = None,
) -> startai.Array:
    """Take values from the input array by matching 1d index and data slices.

    Parameters
    ----------
    arr
        The source array.
    choices
        The indices of the values to extract.
    out
        The output array.
    mode
        One of: 'wrap', 'clip'. Parameter controlling how out-of-bounds indices
        will be handled.

    Returns
    -------
    ret
        The returned array has the same shape as `indices`.

    Examples
    --------
    >>> choices = startai.array([[0, 1, 2, 3], [10, 11, 12, 13],
    ...                     [20, 21, 22, 23],[30, 31, 32, 33]])
    >>> print(startai.choose(choices, startai.array([2, 3, 1, 0]))
    startai.array([20, 31, 12, 3])
    >>> arr = startai.array([2, 4, 1, 0])
    >>> print(startai.choose(choices, arr, mode='clip')) # 4 goes to 3 (4-1)
    startai.array([20, 31, 12, 3])
    >>> arr = startai.array([2, 4, 1, 0])
    >>> print(startai.choose(choices, arr, mode='wrap')) # 4 goes to (4 mod 4)
    startai.array([20, 1, 12, 3])
    """
    return startai.current_backend().choose(arr, choices, out=out, mode=mode)


@handle_array_function
@inputs_to_startai_arrays
@handle_nestable
@handle_exceptions
@handle_device
def column_stack(
    arrays: Sequence[Union[startai.Array, startai.NativeArray]],
    /,
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Create a new array by horizontally stacking the arrays in arrays.

    Equivalent to `startai.hstack(arrays)`, except each zero or one dimensional
    array `x` in arrays is first reshaped into a `(x.size(), 1)` column
    before being stacked horizontally.

    Parameters
    ----------
    arrays
        Arrays to be stacked.
    out
        Output array.

    Returns
    -------
    ret
        Stacked input.

    Examples
    --------
    Arrays of different dtypes up to dimension 2.
    >>> a0 = startai.array(True)
    >>> a1 = startai.array([7])
    >>> a2 = startai.array([[11.3, 13.7]])
    >>> startai.column_stack((a0, a1, a2))
    startai.array([[ 1.        ,  7.        , 11.30000019, 13.69999981]])

    Arrays of dimension 3.
    >>> a = startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    >>> b = startai.array([[[11, 12]], [[13, 14]]])
    >>> startai.column_stack((a, b))
    startai.array([[[ 1,  2],
                [ 3,  4],
                [11, 12]],

               [[ 5,  6],
                [ 7,  8],
                [13, 14]]])
    """
    arrays = [startai.reshape(x, shape=(-1, 1)) if x.ndim < 2 else x for x in arrays]

    return startai.hstack(arrays, out=out)


column_stack.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_out_argument",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_device
def take(
    x: Union[int, startai.Array, startai.NativeArray],
    indices: Union[int, startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[int] = None,
    mode: str = "fill",
    fill_value: Optional[Number] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Return elements of an array along an axis.

    .. note::
        Conceptually, take(x, indices, axis=3) is equivalent to x[:,:,:,indices,...];
        however, explicit indexing via arrays of indices is not currently supported
        in this specification due to concerns regarding __setitem__
        and array mutation semantics.

    Parameters
    ----------
    x
        input array
    indices
        array indices. Must have an integer data type.
    axis
        axis over which to select values. If `axis` is negative,
        the function must determine the axis along which to select values
        by counting from the last dimension.
        By default, the flattened input array is used.
    mode
        specifies how out-of-bounds `indices` will behave.
        -   ‘raise’ – raise an error
        -   ‘wrap’ – wrap around
        -   ‘clip’ – clip to the range (all indices that are too large are
        replaced by the index that addresses the last element along that axis.
        Note that this disables indexing with negative numbers.)
        -   'fill' (default) = returns invalid values (e.g. NaN)
        for out-of bounds indices (see also fill_value below)
    fill_value
        fill value to return for out-of-bounds slices
        (Defaults to NaN for inexact types,
        the largest negative value for signed types,
        the largest positive value for unsigned types, and True for booleans.)
    out
        optional output array, for writing the result to. It must
        have a shape that the inputs broadcast to.

    Returns
    -------
        ret
            an array having the same data type as `x`.
            The output array must have the same rank (i.e., number of dimensions) as `x`
            and must have the same shape as `x`, except for the axis specified by `axis`
            whose size must equal the number of elements in `indices`.

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
    With `startai.Array` input:

    >>> x = startai.array([4,5,6])
    >>> indices = startai.array([2,1,0])
    >>> y = startai.take(x, indices)
    >>> print(y)
    startai.array([6, 5, 4])

    >>> x = startai.array([4.7,5.2,6.5])
    >>> indices = startai.array([[0,1]])
    >>> y = startai.zeros_like(indices, dtype=x.dtype)
    >>> startai.take(x, indices, out=y)
    >>> print(y)
    startai.array([[4.7, 5.2]])

    >>> x = startai.array([False, False, True])
    >>> indices = startai.array([[4,3,2]])
    >>> y = startai.zeros_like(indices, dtype=x.dtype)
    >>> startai.take(x, indices, out=y, mode="wrap")
    >>> print(y)
    startai.array([[False, False, True]])

    With `startai.Container` input:

    >>> x = startai.Container(a=startai.array([True,False,False]),
    ...                     b=startai.array([2.3,4.5,6.7]),
    ...                     c=startai.array([1,2,3]))
    >>> indices = startai.array([[1,9,2]])
    >>> y = startai.take(x, indices)
    >>> print(y)
    {
        a: startai.array([[False, True, False]]),
        b: startai.array([[4.5, nan, 6.69999981]]),
        c: startai.array([[2, -2147483648, 3]])
    }
    """
    return startai.current_backend().take(
        x, indices, axis=axis, mode=mode, fill_value=fill_value, out=out
    )


@inputs_to_startai_arrays
@handle_exceptions
@handle_device
def trim_zeros(
    a: Union[startai.Array, startai.NativeArray],
    /,
    *,
    trim: str = "fb",
) -> startai.Array:
    """startai.Container instance method variant of startai.trim_zeros. This method
    simply wraps the function, and so the docstring for startai.trim_zeros also
    applies to this method with minimal changes.

    Parameters
    ----------
    a : 1-D array
        Input array.
    trim : str, optional
        A string with 'f' representing trim from front and 'b' to trim from
        back. Default is 'fb', trim zeros from both front and back of the
        array.

    Returns
    -------
        1-D array
        The result of trimming the input. The input data type is preserved.

    Examples
    --------
    >>> a = startai.array([0, 0, 0, 0, 8, 3, 0, 0, 7, 1, 0])
    >>> startai.trim_zeros(a)
    array([8, 3, 0, 0, 7, 1])
    >>> startai.trim_zeros(a, 'b')
    array([0, 0, 0, 0, 8, 3, 0, 0, 7, 1])
    >>> startai.trim_zeros([0, 8, 3, 0, 0])
    [8, 3]
    """
    return startai.current_backend(a).trim_zeros(a, trim=trim)


trim_zeros.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_view
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def unflatten(
    x: Union[startai.Array, startai.NativeArray],
    /,
    dim: int,
    shape: Tuple[int],
    *,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Expand a dimension of the input tensor over multiple dimensions.

    Parameters
    ----------
    x
        input tensor.
    dim
        dimension to be unflattened, specified as an index into input.shape.
    shape
        new shape of the unflattened dimension. One of its elements can be -1 in
        which case the corresponding output dimension is inferred. Otherwise,
        the product of sizes must equal input.shape[dim].
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        view of input with the specified dimension unflattened.


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
    >>> startai.unflatten(torch.randn(3, 4, 1), dim=1, shape=(2, 2)).shape
    torch.Size([3, 2, 2, 1])
    >>> startai.unflatten(torch.randn(3, 4, 1), dim=1, shape=(-1, 2)).shape
    torch.Size([3, 2, 2, 1])
    >>> startai.unflatten(torch.randn(5, 12, 3), dim=-2, shape=(2, 2, 3, 1, 1)).shape
    torch.Size([5, 2, 2, 3, 1, 1, 3])
    """
    return startai.current_backend(x).unflatten(x, dim=dim, shape=shape, out=out)
