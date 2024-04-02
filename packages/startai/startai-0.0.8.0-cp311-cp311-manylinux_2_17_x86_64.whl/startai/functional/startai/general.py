"""Collection of general Startai functions."""

# global
import gc
import inspect
import itertools
import math
from functools import wraps
from numbers import Number
from typing import (
    Callable,
    Any,
    Union,
    List,
    Tuple,
    Dict,
    Iterable,
    Optional,
    Sequence,
    Literal,
)
import einops
import ml_dtypes  # noqa
import numpy as np

# local
import startai
from startai.utils.backend import current_backend, backend_stack
from startai.functional.startai.gradients import _is_variable
from startai.utils.exceptions import handle_exceptions
from startai.func_wrapper import (
    handle_array_function,
    inputs_to_startai_arrays,
    inputs_to_native_arrays,
    to_native_arrays_and_back,
    inputs_to_native_shapes,
    outputs_to_startai_shapes,
    outputs_to_startai_arrays,
    handle_out_argument,
    handle_nestable,
    handle_array_like_without_promotion,
    handle_view_indexing,
    handle_device,
    handle_partial_mixed_function,
    handle_backend_invalid,
)
from startai.functional.startai.device import dev

FN_CACHE = {}
INF = float("inf")

precise_mode_stack = []
queue_timeout_stack = []
array_mode_stack = []
shape_array_mode_stack = []
nestable_mode_stack = []
exception_trace_mode_stack = []
inplace_mode_stack = []
trace_mode_dict = {
    "frontend": "startai/functional/frontends",
    "startai": "startai/",
    "full": "",
    "none": "",
}
show_func_wrapper_trace_mode_stack = []
min_denominator_stack = []
min_base_stack = []
tmp_dir_stack = []


# Extra #
# ------#


class PreciseMode:
    """Precise Mode Context Manager."""

    # noinspection PyShadowingNames
    def __init__(self, precise_mode: bool):
        self._precise_mode = precise_mode

    def __enter__(self):
        set_precise_mode(self._precise_mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unset_precise_mode()
        if self and (exc_type is not None):
            raise exc_val
        return self


startai.precise_mode = precise_mode_stack[-1] if precise_mode_stack else True


@handle_exceptions
def set_precise_mode(mode: bool) -> None:
    """Set the mode of whether to use a promotion table that avoids any
    precision loss or a compute efficient table that avoids most wider-than-
    necessary promotions.

    Parameter
    ---------
    mode
        boolean whether to use high precision promotion table

    Examples
    --------
    >>> startai.set_precise_mode(False)
    >>> startai.precise_mode
    False

    >>> startai.set_precise_mode(True)
    >>> startai.precise_mode
    True
    """
    global precise_mode_stack
    startai.utils.assertions.check_isinstance(mode, bool)
    precise_mode_stack.append(mode)
    startai.__setattr__("precise_mode", mode, True)
    _update_promotion_table(precise=mode)


@handle_exceptions
def unset_precise_mode() -> None:
    """Reset the mode of whether to use a promotion table that avoids any
    precision loss or a compute efficient table that avoids most wider-than-
    necessary promotions.

    Examples
    --------
    >>> startai.set_precise_mode(False)
    >>> startai.precise_mode
    False

    >>> startai.unset_precise_mode()
    >>> startai.precise_mode
    True
    """
    global precise_mode_stack
    if precise_mode_stack:
        precise_mode_stack.pop(-1)
        mode = precise_mode_stack[-1] if precise_mode_stack else True
        startai.__setattr__("precise_mode", mode, True)
        _update_promotion_table(precise=mode)


def _update_promotion_table(precise):
    """Update the current datatype promotion table."""
    if precise:
        startai.promotion_table = {
            **startai.array_api_promotion_table,
            **startai.common_extra_promotion_table,
            **startai.precise_extra_promotion_table,
        }

    else:
        startai.promotion_table = {
            **startai.array_api_promotion_table,
            **startai.common_extra_promotion_table,
            **startai.extra_promotion_table,
        }


class ArrayMode:
    """Array Mode Context Manager."""

    # noinspection PyShadowingNames
    def __init__(self, array_mode):
        self._array_mode = array_mode

    def __enter__(self):
        set_array_mode(self._array_mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unset_array_mode()
        if self and (exc_type is not None):
            raise exc_val
        return self


def get_referrers_recursive(
    item: object,
    *,
    depth: int = 0,
    max_depth: Optional[int] = None,
    seen_set: Optional[set] = None,
    local_set: Optional[set] = None,
) -> startai.Container:
    """Recursively retrieve referrers for an object.

    This function recursively fetches referrers for the specified `item` up to a given
    `max_depth`.

    Parameters
    ----------
    item
        The object for which referrers should be retrieved.
    depth
        Current depth in the recursion. (default is 0)
    max_depth
        Maximum depth of recursion. If `None`, there's no depth limit. (default is None)
    seen_set
        Set of seen referrer IDs to prevent duplicates. (default is None)
    local_set
        Set of local referrer IDs to avoid redundancy. (default is None)

    Returns
    -------
    ret
        A container representing referrers and their sub-referrers, respecting the
        `max_depth`.

    Examples
    --------
    >>> import gc
    >>> example_function = lambda: (obj := [1, 2, 3]) and startai.get_referrers_recursive(obj, max_depth=2)
    >>> result = example_function()
    >>> print(result)
    {repr:[1,2,3]}
    """  # noqa: E501
    seen_set = startai.default(seen_set, set())
    local_set = startai.default(local_set, set())
    ret_cont = startai.Container(
        repr=str(item).replace(" ", ""),
        alphabetical_keys=False,
        keyword_color_dict={"repr": "magenta"},
    )

    referrers = [
        ref
        for ref in gc.get_referrers(item)
        if not (
            isinstance(ref, dict)
            and min(k in ref for k in ["depth", "max_depth", "seen_set", "local_set"])
        )
    ]

    local_set.add(str(id(referrers)))
    for ref in referrers:
        ref_id = str(id(ref))
        if ref_id in local_set or hasattr(ref, "cell_contents"):
            continue
        seen = ref_id in seen_set
        seen_set.add(ref_id)

        def get_referrers_recursive_inner():
            return get_referrers_recursive(
                ref,
                depth=depth + 1,
                max_depth=max_depth,
                seen_set=seen_set,
                local_set=local_set,
            )

        this_repr = "tracked" if seen else str(ref).replace(" ", "")

        if not seen and (not max_depth or depth < max_depth):
            val = startai.Container(
                repr=this_repr,
                alphabetical_keys=False,
                keyword_color_dict={"repr": "magenta"},
            )

            refs = get_referrers_recursive_inner()
            for k, v in refs.items():
                val[k] = v
        else:
            val = this_repr
        ret_cont[str(ref_id)] = val

    return ret_cont


@handle_exceptions
@handle_backend_invalid
def is_native_array(
    x: Union[startai.Array, startai.NativeArray], /, *, exclusive: bool = False
) -> bool:
    """Determine whether the input x is an :class:`startai.NativeArray` instance.

    Parameters
    ----------
    x
        The input to check
    exclusive
        Whether to check if the data type is exclusively an array, rather than a
        variable or traced array.

    Returns
    -------
    ret
        Boolean, whether or not x is an :class:`startai.NativeArray`.

    Examples
    --------
    >>> x = startai.array([0, 1, 2])
    >>> startai.is_native_array(x)
    False

    >>> x = startai.native_array([9.1, -8.3, 2.8, 3.0])
    >>> startai.is_native_array(x, exclusive=True)
    True
    """
    try:
        return current_backend(x).is_native_array(x, exclusive=exclusive)
    except ValueError:
        return False


@handle_exceptions
@handle_backend_invalid
def is_startai_array(
    x: Union[startai.Array, startai.NativeArray], /, *, exclusive: Optional[bool] = False
) -> bool:
    """Determine whether the input x is a valid Startai Array.

    Parameters
    ----------
    x
        The input to check
    exclusive
        Whether to check if the data type is exclusively an array, rather than a
        variable or traced array.

    Returns
    -------
    ret
        Boolean, whether or not x is a valid Startai Array.

    Examples
    --------
    >>> x = startai.array([0, 1, 2])
    >>> startai.is_startai_array(x)
    True

    >>> x = startai.native_array([9.1, -8.3, 2.8, 3.0])
    >>> startai.is_startai_array(x, exclusive=True)
    False
    """
    return isinstance(x, startai.Array) and startai.is_native_array(x.data, exclusive=exclusive)


@handle_exceptions
@handle_backend_invalid
def is_array(x: Any, /, *, exclusive: bool = False) -> bool:
    """Determine whether the input x is either an Startai Array or a Native Array.

    Parameters
    ----------
    x
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
    >>> print(startai.is_array(x))
    True

    >>> x = startai.native_array([9.1, -8.3, 2.8, 3.0])
    >>> print(startai.is_array(x, exclusive=True))
    True

    >>> x = [2, 3]
    >>> print(startai.is_array(x))
    False
    """
    return startai.is_startai_array(x, exclusive=exclusive) or startai.is_native_array(
        x, exclusive=exclusive
    )


@handle_exceptions
def is_startai_container(x: Any, /) -> bool:
    """Determine whether the input x is an Startai Container.

    Parameters
    ----------
    x
        The input to check

    Returns
    -------
    ret
        Boolean, whether or not x is an startai container.

    Examples
    --------
    >>> x = startai.Container()
    >>> print(startai.is_startai_container(x))
    True

    >>> x = [2, 3]
    >>> print(startai.is_startai_container(x))
    False
    """
    return isinstance(x, startai.Container)


startai.array_mode = array_mode_stack[-1] if array_mode_stack else True


@handle_exceptions
def set_array_mode(mode: bool) -> None:
    """Set the mode of whether to convert inputs to startai.NativeArray, then
    convert outputs back to startai.Array.

    It Stops the conversion of startai.NativeArray to startai.Array in the
    case when it is set to False.

    Parameter
    ---------
    mode
        boolean whether to perform startai.Array conversions

    Examples
    --------
    >>> startai.set_array_mode(False)
    >>> startai.array_mode
    False

    >>> startai.set_array_mode(True)
    >>> startai.array_mode
    True
    """
    global array_mode_stack
    startai.utils.assertions.check_isinstance(mode, bool)
    array_mode_stack.append(mode)
    startai.__setattr__("array_mode", mode, True)


@handle_exceptions
def unset_array_mode() -> None:
    """Reset the mode of converting inputs to startai.NativeArray, then converting
    outputs back to startai.Array to the previous state.

    Examples
    --------
    >>> startai.set_array_mode(False)
    >>> startai.array_mode
    False

    >>> startai.unset_shape_array_mode()
    >>> startai.array_mode
    True
    """
    global array_mode_stack
    if array_mode_stack:
        array_mode_stack.pop(-1)
        mode = array_mode_stack[-1] if array_mode_stack else True
        startai.__setattr__("array_mode", mode, True)


startai.nestable_mode = nestable_mode_stack[-1] if nestable_mode_stack else True


@handle_exceptions
def set_nestable_mode(mode: bool) -> None:
    """Set the mode of whether to check if function inputs are startai.Container.

    Parameter
    ---------
    mode
        boolean whether to check if function inputs are startai.Container

    Examples
    --------
    >>> startai.set_nestable_mode(False)
    >>> startai.nestable_mode
    False

    >>> startai.set_nestable_mode(True)
    >>> startai.nestable_mode
    True
    """
    global nestable_mode_stack
    startai.utils.assertions.check_isinstance(mode, bool)
    nestable_mode_stack.append(mode)
    startai.__setattr__("nestable_mode", mode, True)


@handle_exceptions
def unset_nestable_mode() -> None:
    """Reset the mode of whether to check if function inputs are startai.Container
    to the previous state.

    Examples
    --------
    >>> startai.set_nestable_mode(False)
    >>> startai.nestable_mode
    False

    >>> startai.unset_nestable_mode()
    >>> startai.nestable_mode
    True
    """
    global nestable_mode_stack
    if nestable_mode_stack:
        nestable_mode_stack.pop(-1)
        mode = nestable_mode_stack[-1] if nestable_mode_stack else True
        startai.__setattr__("nestable_mode", mode, True)


startai.exception_trace_mode = (
    exception_trace_mode_stack[-1] if exception_trace_mode_stack else "full"
)


@handle_exceptions
def set_exception_trace_mode(mode: Literal["startai", "full", "frontend"]) -> None:
    """Set the mode of whether to show frontend-truncated exception stack
    traces, startai- truncated exception stack traces or full exception stack
    traces.

    Parameter
    ---------
    mode
        str exception trace mode, one of `startai`, `full` or `frontend`

    Examples
    --------
    >>> startai.set_exception_trace_mode("startai")
    >>> startai.exception_trace_mode
    'startai'

    >>> startai.set_exception_trace_mode("full")
    >>> startai.exception_trace_mode
    'full'
    """
    global exception_trace_mode_stack
    trace_modes = list(trace_mode_dict.keys())
    startai.utils.assertions.check_elem_in_list(
        mode, trace_modes, False, f"trace mode must be one of {trace_modes}"
    )
    exception_trace_mode_stack.append(mode)
    startai.__setattr__("exception_trace_mode", mode, True)


@handle_exceptions
def unset_exception_trace_mode() -> None:
    """Reset the trace mode to the previously set mode.

    Examples
    --------
    >>> startai.set_exception_trace_mode("startai")
    >>> startai.exception_trace_mode
    'startai'

    >>> startai.unset_exception_trace_mode()
    >>> startai.exception_trace_mode
    'full'
    """
    global exception_trace_mode_stack
    if exception_trace_mode_stack:
        exception_trace_mode_stack.pop(-1)
        mode = exception_trace_mode_stack[-1] if exception_trace_mode_stack else "full"
        startai.__setattr__("exception_trace_mode", mode, True)


startai.show_func_wrapper_trace_mode = (
    show_func_wrapper_trace_mode_stack[-1]
    if show_func_wrapper_trace_mode_stack
    else True
)


@handle_exceptions
def set_show_func_wrapper_trace_mode(mode: bool) -> None:
    """Set the mode of whether to show the full stack trace with function
    wrapping traces.

    Parameter
    ---------
    mode
        boolean whether to perform startai.Array conversions

    Examples
    --------
    >>> startai.set_show_func_wrapper_trace_mode(False)
    >>> startai.show_func_wrapper_trace_mode
    False

    >>> startai.set_show_func_wrapper_trace_mode(True)
    >>> startai.show_func_wrapper_trace_mode
    True
    """
    global show_func_wrapper_trace_mode_stack
    startai.utils.assertions.check_isinstance(mode, bool)
    show_func_wrapper_trace_mode_stack.append(mode)
    startai.__setattr__("show_func_wrapper_trace_mode", mode, True)


@handle_exceptions
def unset_show_func_wrapper_trace_mode() -> None:
    """Reset the mode of whether to show the full stack trace with function
    wrapping traces.

    Examples
    --------
    >>> startai.set_show_func_wrapper_trace_mode(False)
    >>> startai.show_func_wrapper_trace_mode
    False

    >>> startai.unset_show_func_wrapper_trace_mode()
    >>> startai.show_func_wrapper_trace_mode
    True
    """
    global show_func_wrapper_trace_mode_stack
    if show_func_wrapper_trace_mode_stack:
        show_func_wrapper_trace_mode_stack.pop(-1)
        mode = (
            show_func_wrapper_trace_mode_stack[-1]
            if show_func_wrapper_trace_mode_stack
            else True
        )
        startai.__setattr__("show_func_wrapper_trace_mode", mode, True)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_native_arrays
@handle_array_function
@handle_device
def array_equal(
    x0: Union[startai.Array, startai.NativeArray],
    x1: Union[startai.Array, startai.NativeArray],
    /,
) -> bool:
    """Determine whether two input arrays are equal across all elements.

    Parameters
    ----------
    x0
        The first input array to compare.
    x1
        The second input array to compare.

    Returns
    -------
    ret
        Boolean, whether or not the input arrays are equal across all elements.

    Examples
    --------
    >>> x = startai.array([1,0,1])
    >>> y = startai.array([1,0,-1])
    >>> z = startai.array_equal(x,y)
    >>> print(z)
    False

    >>> a = startai.array([1, 2])
    >>> b = startai.array([1, 2])
    >>> c = startai.array_equal(a,b)
    >>> print(c)
    True

    >>> i = startai.array([1, 2])
    >>> j = startai.array([1, 2, 3])
    >>> k = startai.array_equal(i,j)
    >>> print(k)
    False
    """
    return current_backend(x0).array_equal(x0, x1)


@handle_exceptions
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
def all_equal(
    *xs: Iterable[Any], equality_matrix: bool = False
) -> Union[bool, startai.Array, startai.NativeArray]:
    """Determine whether the inputs are all equal.

    Parameters
    ----------
    xs
        inputs to compare.
    equality_matrix
        Whether to return a matrix of equalities comparing each input with every other.
        Default is ``False``.

    Returns
    -------
    ret
        Boolean, whether or not the inputs are equal, or matrix array of booleans if
        equality_matrix=True is set.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> x1 = startai.array([1, 1, 0, 0, 1, -1])
    >>> x2 = startai.array([1, 1, 0, 0, 1, -1])
    >>> y = startai.all_equal(x1, x2)
    >>> print(y)
    True

    >>> x1 = startai.array([0, 0])
    >>> x2 = startai.array([0, 0])
    >>> x3 = startai.array([1, 0])
    >>> y = startai.all_equal(x1, x2, x3, equality_matrix=True)
    >>> print(y)
    startai.array([[ True,  True, False],
       [ True,  True, False],
       [False, False,  True]])

    With one :class:`startai.Container` inputs:

    >>> x1 = startai.Container(a=startai.array([0, 0, -1, 1, 0]),
    ...                    b=startai.array([0, 0, -1, 1, 0]))
    >>> x2 = startai.array([0, 0, -1, 1, 0])
    >>> y = startai.all_equal(x1, x2, equality_matrix=False)
    >>> print(y)
    {
        a: True,
        b: True
    }

    With multiple :class:`startai.Container` inputs:

    >>> x1 = startai.Container(a=startai.array([1, 0, 1, 1]),
    ...                    b=startai.array([1, 0, 0, 1]))
    >>> x2 = startai.Container(a=startai.array([1, 0, 1, 1]),
    ...                    b=startai.array([1, 0, -1, -1]))
    >>> y = startai.all_equal(x1, x2, equality_matrix=False)
    >>> print(y)
    {
        a: True,
        b: False
    }
    """
    equality_fn = startai.array_equal if startai.is_array(xs[0]) else lambda a, b: a == b
    if equality_matrix:
        num_arrays = len(xs)
        mat = [[None for _ in range(num_arrays)] for _ in range(num_arrays)]
        for i, xa in enumerate(xs):
            for j_, xb in enumerate(xs[i:]):
                j = j_ + i
                res = equality_fn(xa, xb)
                if startai.is_native_array(res):
                    # noinspection PyTypeChecker
                    res = startai.to_scalar(res)
                # noinspection PyTypeChecker
                mat[i][j] = res
                # noinspection PyTypeChecker
                mat[j][i] = res
        return startai.array(mat)
    x0 = xs[0]
    for x in xs[1:]:
        if not equality_fn(x0, x):
            return False
    return True


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_native_arrays
@handle_array_function
@handle_device
def to_numpy(
    x: Union[startai.Array, startai.NativeArray], /, *, copy: bool = True
) -> np.ndarray:
    """Convert an array into a numpy array.

    Parameters
    ----------
    x
        input array
    copy
        whether to copy the array to a new address or not.
        Default is ``True``.

    Returns
    -------
    ret
        a numpy array copying all the element of the array ``x``.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> x = startai.array([-1, 0, 1])
    >>> y = startai.to_numpy(x, copy=True)
    >>> print(y)
    [-1  0  1]

    >>> x = startai.array([[-1, 0, 1],[-1, 0, 1], [1,0,-1]])
    >>> y = startai.to_numpy(x, copy=True)
    >>> print(y)
    [[-1  0  1]
    [-1  0  1]
    [ 1  0 -1]]

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([-1, 0, 1]))
    >>> y = startai.to_numpy(x)
    >>> print(y)
    {
        a: array([-1, 0, 1], dtype=int32)
    }

    >>> x = startai.Container(a=startai.array([[-1.0, 0., 1.], [-1, 0, 1], [1, 0, -1]]),
    ...                   b=startai.array([[-1, 0, 0], [1, 0, 1], [1, 1, 1]]))
    >>> y = startai.to_numpy(x)
    >>> print(y)
    {
        a: array([[-1., 0., 1.],
                  [-1., 0., 1.],
                  [1., 0., -1.]], dtype=float32),
        b: array([[-1, 0, 0],
                  [1, 0, 1],
                  [1, 1, 1]], dtype=int32)
    }
    """
    return current_backend(x).to_numpy(x, copy=copy)


@handle_exceptions
@handle_nestable
def isscalar(x: Any, /) -> bool:
    return np.isscalar(x)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_native_arrays
@handle_array_function
@handle_device
def to_scalar(x: Union[startai.Array, startai.NativeArray], /) -> Number:
    """Convert an array with a single element into a scalar.

    Parameters
    ----------
    x
        Input array with a single element.

    Returns
    -------
    ret
        a scalar copying the element of the array ``x``.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([3])
    >>> y = startai.to_scalar(x)
    >>> print(y)
    3

    With a mix of :class:`startai.Container` and :class:`startai.Array` input:

    >>> x = startai.Container(a=startai.array([-1]), b=startai.array([3]))
    >>> y = startai.to_scalar(x)
    >>> print(y)
    {
        a: -1,
        b: 3
    }

    >>> x = startai.Container(a=startai.array([1]), b=startai.array([0]),
    ...                   c=startai.array([-1]))
    >>> y = startai.to_scalar(x)
    >>> print(y)
    {
        a: 1,
        b: 0,
        c: -1
    }
    """
    return current_backend(x).to_scalar(x)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_native_arrays
@handle_array_function
@handle_device
def to_list(x: Union[startai.Array, startai.NativeArray], /) -> List:
    """Create a (possibly nested) list from input array.

    Parameters
    ----------
    x
        Input array.

    Returns
    -------
    ret
        A list representation of the input array ``x``.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([-1, 0, 1])
    >>> y = startai.to_list(x)
    >>> print(y)
    [-1, 0, 1]

    >>> x = startai.array([[ 1.1,  2.2,  3.3],
    ...                [-4.4, -5.5, -6.6]])
    >>> y = startai.to_list(x)
    >>> print(y)
    [[1.100000023841858,2.200000047683716,3.299999952316284],
    [-4.400000095367432,-5.5,-6.599999904632568]]

    >>> x = startai.array([[[-1,  0,  1],
    ...                 [ 1,  0, -1]],
    ...                [[ 1, -1,  0],
    ...                 [ 1,  0, -1]]])
    >>> y = startai.to_list(x)
    >>> print(y)
    [[[-1, 0, 1], [1, 0, -1]], [[1, -1, 0], [1, 0, -1]]]

    With a mix of :class:`startai.Container` and :class:`startai.Array` input:

    >>> x = startai.Container(a=startai.array([-1, 0, 1]))
    >>> y = startai.to_list(x)
    >>> print(y)
    {
        a: [-1, 0, 1]
    }

    >>> x = startai.Container(a=startai.array([[-1, 0, 1],
    ...                                [-1, 0, 1],
    ...                                [1, 0, -1]]))
    >>> y = startai.to_list(x)
    >>> print(y)
    {
        a: [[-1, 0, 1], [-1, 0, 1], [1,0,-1]]
    }

    >>> x = startai.Container(a=startai.array([[[-1, 0, 1],[1, 0, -1]],
    ...                                [[1, -1, 0],[1, 0, -1]]]))
    >>> y = startai.to_list(x)
    >>> print(y)
    {
        a: [[[-1, 0, 1], [1, 0, -1]], [[1, -1, 0], [1, 0, -1]]]
    }
    """
    return current_backend(x).to_list(x)


@handle_exceptions
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
def clip_vector_norm(
    x: Union[startai.Array, startai.NativeArray],
    max_norm: float,
    /,
    *,
    p: float = 2.0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Clips (limits) the vector p-norm of an array.

    Parameters
    ----------
    x
        Input array containing elements to clip.
    max_norm
        The maximum value of the array norm.
    p
        The p-value for computing the p-norm.
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
    With :class:`startai.Array` input:

    >>> x = startai.array([0., 1., 2.])
    >>> y = startai.clip_vector_norm(x, 2.0)
    >>> print(y)
    startai.array([0.        , 0.89442718, 1.78885436])

    >>> x = startai.array([0.5, -0.7, 2.4])
    >>> y = startai.clip_vector_norm(x, 3.0, p=1.0)
    >>> print(y)
    startai.array([ 0.41666666, -0.58333331,  2.        ])

    >>> x = startai.array([[[0., 0.], [1., 3.], [2., 6.]],
    ...                [[3., 9.], [4., 12.], [5., 15.]]])
    >>> y = startai.zeros(((2, 3, 2)))
    >>> startai.clip_vector_norm(x, 4.0, p=1.0, out=y)
    >>> print(y)
    startai.array([[[0.        , 0.        ],
        [0.06666667, 0.20000002],
        [0.13333334, 0.40000004]],

       [[0.20000002, 0.60000002],
        [0.26666668, 0.80000007],
        [0.33333334, 1.        ]]]))

    >>> x = startai.array([[1.1, 2.2, 3.3],
    ...                [-4.4, -5.5, -6.6]])
    >>> startai.clip_vector_norm(x, 1.0, p=3.0, out=x)
    >>> print(x)
    startai.array([[ 0.13137734,  0.26275468,  0.39413199],
       [-0.52550936, -0.6568867 , -0.78826398]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> y = startai.clip_vector_norm(x, 2.0)
    >>> print(y)
    {
        a: startai.array([0., 0.89442718, 1.78885436]),
        b: startai.array([0.84852815, 1.1313709, 1.41421366])
    }

    With multiple :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> max_norm = startai.Container(a=2, b=3)
    >>> y = startai.clip_vector_norm(x, max_norm)
    >>> print(y)
    {
        a: startai.array([0., 0.89442718, 1.78885436]),
        b: startai.array([1.27279221, 1.69705628, 2.12132034])
    }
    """
    norm = startai.vector_norm(x, keepdims=True, ord=p)
    ratio = startai.stable_divide(max_norm, norm)
    if ratio < 1:
        ret = ratio * x
    else:
        ret = startai.copy_array(x)
    if out is not None:
        ret = startai.inplace_update(out, ret)
    return ret


@handle_exceptions
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
def clip_matrix_norm(
    x: Union[startai.Array, startai.NativeArray],
    max_norm: float,
    /,
    *,
    p: float = 2.0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Clips (limits) the matrix norm of an array.

    Parameters
    ----------
    x
        Input array containing elements to clip.
    max_norm
        The maximum value of the array norm.
    p
        The p-value for computing the p-norm.
        Default is 2.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        An array with the matrix norm downscaled to the max norm if needed.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[0., 1., 2.]])
    >>> y = startai.clip_matrix_norm(x, 2.0)
    >>> print(y)
    startai.array([[0.   , 0.894, 1.79 ]])

    >>> x = startai.array([[0.1, -1.2, 3.7], [0., 7.3, -0.5]])
    >>> y = startai.clip_matrix_norm(x, 3.0, p=1.0)
    >>> print(y)
    startai.array([[ 0.0353, -0.424 ,  1.31  ],
               [ 0.    ,  2.58  , -0.176 ]])

    >>> x = startai.array([[[5., 4.], [-2., 6.]],
    ...                [[3., 7.], [0., -5.]]])
    >>> y = startai.empty((2, 2, 2))
    >>> y = startai.clip_matrix_norm(x, 0.5, p=2.0)
    >>> print(y)
    startai.array([[[ 0.339,  0.271],
                [-0.135,  0.406]],
               [[ 0.168,  0.391],
                [ 0.   , -0.279]]])

    >>> x = startai.array([[0., 1.],
    ...                [2., 3.]])
    >>> startai.clip_matrix_norm(x, 5.0, p=1.0, out=x)
    >>> print(x)
    startai.array([[0., 1.],
               [2., 3.]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[0., 1., 2.]]),
    ...                   b=startai.array([[3., 4., 5.]]))
    >>> y = startai.clip_matrix_norm(x, 2.0)
    >>> print(y)
    {
        a: startai.array([[0., 0.894, 1.79]]),
        b: startai.array([[0.849, 1.13, 1.41]])
    }
    """
    norms = startai.matrix_norm(x, ord=p, keepdims=True)
    ratios = startai.minimum(startai.stable_divide(max_norm, norms), 1.0)
    return startai.multiply(ratios, x, out=out)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def fourier_encode(
    x: Union[startai.Array, startai.NativeArray],
    max_freq: Union[float, startai.Array, startai.NativeArray],
    /,
    *,
    num_bands: int = 4,
    linear: bool = False,
    concat: bool = True,
    flatten: bool = False,
) -> Union[startai.Array, startai.NativeArray, Tuple]:
    """Pad an array with fourier encodings.

    Parameters
    ----------
    x
        Input array to encode.
    max_freq
        The maximum frequency of the encoding.
    num_bands
        The number of frequency bands for the encoding.
        Default is 4.
    linear
        Whether to space the frequency bands linearly as opposed to geometrically.
        Default is ``False``.
    concat
        Whether to concatenate the position, sin and cos values, or return separately.
        Default is ``True``.
    flatten
        Whether to flatten the position dimension into the batch dimension.
        Default is False.

    Returns
    -------
    ret
        New array with the final dimension expanded, and the encodings stored in this
        channel.

    Examples
    --------
    >>> x = startai.array([1,2,3])
    >>> y = 1.5
    >>> z = startai.fourier_encode(x,y)
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


    >>> x = startai.array([3,10])
    >>> y = 2.5
    >>> z = startai.fourier_encode(x, y, num_bands=3)
    >>> print(z)
    startai.array([[ 3.0000000e+00,  3.6739404e-16,  3.6739404e-16, 3.6739404e-16,
                -1.0000000e+00, -1.0000000e+00, -1.0000000e+00],
               [ 1.0000000e+01, -1.2246468e-15, -1.2246468e-15, -1.2246468e-15,
                 1.0000000e+00,  1.0000000e+00,  1.0000000e+00]])
    """
    x_in = x
    dim = x.shape[-1]
    x = startai.expand_dims(x, axis=-1)
    orig_x = x
    if linear:
        scales = startai.linspace(1.0, max_freq / 2, num_bands, device=dev(x))
    elif startai.backend == "torch" and isinstance(max_freq, float):
        scales = startai.logspace(
            0.0,
            startai.log(startai.array(max_freq / 2)) / math.log(10),
            num_bands,
            base=10,
            device=dev(x),
        )
    else:
        scales = startai.logspace(
            0.0,
            startai.log(max_freq / 2) / math.log(10),
            num_bands,
            base=10,
            device=dev(x),
        )
    scales = startai.astype(scales, startai.dtype(x))
    scales = scales[(*((None,) * (len(x.shape) - len(scales.shape))), Ellipsis)]
    x = x * scales * math.pi
    sin_x = startai.sin(x)
    cos_x = startai.cos(x)
    if flatten:
        orig_x = x_in
        sin_x = startai.reshape(sin_x, [-1, num_bands * dim])
        cos_x = startai.reshape(cos_x, [-1, num_bands * dim])
    if concat:
        return startai.concat([orig_x, sin_x, cos_x], axis=-1)
    return sin_x, cos_x


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def value_is_nan(
    x: Union[startai.Array, startai.NativeArray, Number],
    /,
    *,
    include_infs: bool = True,
) -> bool:
    """Determine whether the single valued array or scalar is of nan type.

    Parameters
    ----------
    x
        The input to check Input array.
    include_infs
        Whether to include infs and -infs in the check.
        Default is ``True``.

    Returns
    -------
    ret
        Boolean as to whether the input value is a nan or not.

    Examples
    --------
    >>> x = startai.array([451])
    >>> y = startai.value_is_nan(x)
    >>> print(y)
    False

    >>> x = startai.array([float('inf')])
    >>> y = startai.value_is_nan(x)
    >>> print(y)
    True

    >>> x = startai.array([float('inf')])
    >>> y = startai.value_is_nan(x, include_infs=False)
    >>> print(y)
    False

    >>> x = startai.array([float('nan')])
    >>> y = startai.value_is_nan(x, include_infs=False)
    >>> print(y)
    True

    >>> x = startai.array([0])
    >>> y = startai.value_is_nan(x)
    >>> print(y)
    False
    """
    x_scalar = startai.to_scalar(x) if startai.is_array(x) else x
    if x_scalar != x:
        return True
    if include_infs and (x_scalar in [INF, -INF]):
        return True
    return False


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def has_nans(
    x: Union[startai.Array, startai.NativeArray], /, *, include_infs: bool = True
) -> bool:
    """Determine whether the array contains any nans, as well as infs or -infs
    if specified.

    Parameters
    ----------
    x
        Input array.
    include_infs
        Whether to include ``+infinity`` and ``-infinity`` in the check.
        Default is ``True``.

    Returns
    -------
    ret
        Boolean as to whether the array contains nans.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1, 2, 3])
    >>> y = startai.has_nans(x)
    >>> print(y)
    False

    >>> x = startai.array([float('nan'), 2, 3])
    >>> y = startai.has_nans(x)
    >>> print(y)
    True

    >>> x = startai.array([float('inf'), 2, 3])
    >>> y = startai.has_nans(x)
    >>> print(y)
    True

    >>> x = startai.array([float('inf'), 2, 3])
    >>> y = startai.has_nans(x, include_infs=False)
    >>> print(y)
    False

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.]))
    >>> y = startai.has_nans(x)
    >>> print(y)
    {
        a: False,
        b: False
    }
    """
    return startai.value_is_nan(startai.sum(x), include_infs=include_infs)


@handle_exceptions
def exists(x: Any, /) -> bool:
    """Check as to whether the input is None or not.

    Parameters
    ----------
    x
        Input to check.

    Returns
    -------
    ret
        True if x is not None, else False.

    Examples
    --------
    With :code:`Any` input:

    >>> x = None
    >>> y = startai.exists(x)
    >>> print(y)
    False

    >>> x = ""
    >>> y = startai.exists(x)
    >>> print(y)
    True

    >>> x = []
    >>> y = startai.exists(x)
    >>> print(y)
    True

    >>> x = 1
    >>> y = startai.exists(x)
    >>> print(y)
    True

    >>> x = "abc"
    >>> y = startai.exists(x)
    >>> print(y)
    True

    >>> x = [1, 0, -1, 1]
    >>> y = startai.exists(x)
    >>> print(y)
    True

    >>> x = startai.array([1, 2, 3, 1.2])
    >>> y = startai.exists(x)
    >>> print(y)
    True

    With a mix of :class:`startai.Container` and :code:`Any` input:

    >>> x = startai.Container(a=None, b=None)
    >>> y = startai.exists(x)
    >>> print(y)
    True

    >>> x = startai.Container(a=None, b="")
    >>> y = startai.exists(x)
    >>> print(y)
    True

    >>> x = startai.Container(a=123, b="")
    >>> y = startai.exists(x)
    >>> print(y)
    True
    """
    return x is not None


@handle_exceptions
def default(
    x: Any,
    /,
    default_val: Any,
    *,
    catch_exceptions: bool = False,
    rev: bool = False,
    with_callable: bool = False,
) -> Any:
    """Return x provided it exists (is not None), else returns default value.

    Parameters
    ----------
    x
        Input which may or may not exist (be None).
    default_val
        The default value.
    catch_exceptions
        Whether to catch exceptions from callable x.
        Default is ``False``.
    rev
        Whether to reverse the input x and default_val.
        Default is ``False``.
    with_callable
        Whether either of the arguments might be callable functions.
        Default is ``False``.

    Returns
    -------
    ret
        x if x exists (is not None), else default.

    Examples
    --------
    With :code:`Any` input:

    >>> x = None
    >>> y = startai.default(x, "default_string")
    >>> print(y)
    default_string

    >>> x = ""
    >>> y = startai.default(x, "default_string")
    >>> print(y)


    >>> x = startai.array([4, 5, 6])
    >>> y = startai.default(x, startai.array([1, 2, 3]), rev=True)
    >>> print(y)
    startai.array([1, 2, 3])

    >>> x = lambda: startai.array([1, 2, 3])
    >>> y = startai.default(x, startai.array([4, 5, 6]), with_callable=True)
    >>> print(y)
    startai.array([1, 2, 3])

    >>> x = lambda: None
    >>> y = startai.default(x, lambda: startai.array([1, 2, 3]), with_callable=True)
    >>> print(y)
    startai.array([1, 2, 3])

    >>> x = lambda: None
    >>> y = startai.default(x, lambda: startai.array([1, 2, 3]), catch_exceptions=True)
    >>> print(y)
    startai.array([1, 2, 3])

    >>> x = lambda a, b: a + b
    >>> y = startai.default(x, lambda: startai.array([1, 2, 3]), with_callable=True,
    ...                 catch_exceptions=True)
    >>> print(y)
    startai.array([1, 2, 3])

    >>> x = lambda a, b: a + b
    >>> y = startai.default(x, lambda: startai.array([1, 2, 3]), with_callable=True,
    ...                 catch_exceptions=True, rev=True)
    >>> print(y)
    startai.array([1, 2, 3])
    """
    with_callable = catch_exceptions or with_callable
    if rev:
        x, default_val = default_val, x
    if with_callable:
        x_callable = callable(x)
        default_callable = callable(default_val)
    else:
        x_callable = False
        default_callable = False
    if catch_exceptions:
        # noinspection PyBroadException
        try:
            x = x() if x_callable else x
        except Exception:
            return default_val() if default_callable else default_val
    else:
        x = x() if x_callable else x
    return x if exists(x) else default_val() if default_callable else default_val


@handle_exceptions
def to_startai_shape(shape: Union[startai.Shape, startai.NativeShape]) -> startai.Shape:
    """Return the input shape in startai.Shape form.

    Parameters
    ----------
    shape
        The input to be converted

    Returns
    -------
     ret
        the input in startai.Shape form
    """
    if isinstance(shape, startai.Shape):
        return shape
    return startai.Shape(shape)


@handle_exceptions
def to_native_shape(
    shape: Union[startai.Array, startai.Shape, startai.NativeShape, tuple, int, list],
) -> startai.NativeShape:
    """Return the input shape in its native backend framework form.

    Parameters
    ----------
    shape
        The input to be converted

    Returns
    -------
     ret
        the input in its native framework form
    """
    native_shape_type = (startai.NativeShape,)
    if startai.current_backend_str() == "torch":
        native_shape_type += (tuple,)
    if len(backend_stack) != 0 and isinstance(shape, native_shape_type):
        return shape
    startai.utils.assertions.check_isinstance(
        shape, (int, list, tuple, startai.Array, startai.NativeArray, startai.Shape)
    )
    if isinstance(shape, int):
        shape = (shape,)
    elif isinstance(shape, list):
        shape = tuple(shape)
    elif is_array(shape):
        shape = startai.to_numpy(shape).tolist()
    elif isinstance(shape, startai.Shape):
        shape = shape.shape
    startai.utils.assertions.check_all(
        [isinstance(v, int) for v in shape if not is_array(v)],
        "shape must take integers only",
        as_array=False,
    )
    startai.utils.assertions.check_true(
        not is_array(shape) or startai.is_int_dtype(shape), "shape must take integers only"
    )
    return startai.NativeShape(shape) if len(backend_stack) != 0 else startai.Shape(shape)


@handle_exceptions
@handle_nestable
def try_else_none(fn: Callable, *args: Any, **kwargs: Any) -> Union[Callable, None]:
    """Try and return the function, otherwise return None if an exception was
    raised during function execution.

    Parameters
    ----------
    fn
        Function to try and call and return.
    args
        list of arguments.
    kwargs
        dictionary of keyword arguments

    Returns
    -------
        Either the function itself or None if an exception was raised
        during function execution.

    Examples
    --------
    with a function that is executed without any exception:

    >>> x = startai.array([1, 2, 3])
    >>> y = startai.array([4, 5, 6])
    >>> z = startai.try_else_none(startai.add, x, y)
    >>> print(z.__name__)
    add

    with a function that is executed with an exception:

    >>> x = startai.array([1, 2, 3])
    >>> y = 'hemant'
    >>> z = startai.try_else_none(startai.add,x, y)
    >>> print(z)
    None
    """
    try:
        _ = fn(*args, **kwargs)
        return fn
    except Exception:
        return None


@handle_exceptions
def arg_names(receiver):
    """Get the expected keyword arguments for a function or class constructor.

    Parameters
    ----------
    receiver
        Function or class constructor

    Returns
    -------
    ret
        List containing the keyword arguments' names for a function or class constructor

    Examples
    --------
    >>> x = startai.arg_names(startai.tan)
    >>> print(x)
    ['x', 'out']

    >>> x = startai.arg_names(startai.optimizers.Adam)
    >>> print(x)
    ['lr', 'beta1', 'beta2', 'epsilon', 'inplace',
    'stop_gradients', 'trace_on_next_step', 'device']
    """
    return list(inspect.signature(receiver).parameters.keys())


@handle_exceptions
def match_kwargs(
    kwargs: Dict, *receivers: Iterable[Callable], allow_duplicates: bool = False
) -> Union[List[Dict], Dict]:
    """Match keyword arguments to either class or function receivers.

    Parameters
    ----------
    kwargs
        Keyword arguments to match.
    receivers
        Functions and/or classes to match the keyword arguments to.
    allow_duplicates
        Whether to allow one keyword argument to be used for multiple receivers.
        Default is ``False``.

    Returns
    -------
    ret
        Sequence of keyword arguments split as best as possible.

    Examples
    --------
    >>> o = startai.zeros(3)
    >>> kwargs = {'out': o, 'bias': startai.arange(3)}
    >>> x = startai.match_kwargs(kwargs, startai.add, startai.linear)
    >>> print(x)
    [{'out': startai.array([0., 0., 0.])}, {'bias': startai.array([0, 1, 2])}]

    >>> o = startai.zeros(3)
    >>> kwargs = {'out': o, 'bias': startai.arange(3)}
    >>> x = startai.match_kwargs(kwargs, startai.linear, startai.add)
    >>> print(x)
    [{'out': startai.array([0., 0., 0.]), 'bias': startai.array([0, 1, 2])}, {}]
    """
    split_kwargs = []
    for receiver in receivers:
        expected_kwargs = arg_names(receiver)
        found_kwargs = {k: v for k, v in kwargs.items() if k in expected_kwargs}
        if not allow_duplicates:
            for k in found_kwargs:
                del kwargs[k]
        split_kwargs.append(found_kwargs)
    if len(split_kwargs) == 1:
        return split_kwargs[0]
    return split_kwargs


@handle_exceptions
def cache_fn(func: Callable) -> Callable:
    """Cache function outputs.

    A decorator to wrap a function, such that computed outputs are cached to avoid
    recalculating them later.

    Parameters
    ----------
    func
        The function to wrap, whose output should be cached for later.

    Returns
    -------
    ret
        The newly cache wrapped function.

    Examples
    --------
    With positional arguments only:

    >>> def my_sum(val1:float, val2:float)->float: return val1 + val2
    >>> cached_sum = startai.cache_fn(my_sum)
    >>> print(cached_sum(3, 5))
    8

    With keyword arguments:

    >>> def line_eq(x:float, /, *, slp:float=2, itc:float=0)->float: return x*slp+itc
    >>> cached_line_eq = startai.cache_fn(line_eq)
    >>> print(cached_line_eq(3, itc=5, slp=2))
    11
    """
    global FN_CACHE
    if func not in FN_CACHE:
        FN_CACHE[func] = {}

    @wraps(func)
    def cached_fn(*args, **kwargs):
        key = "".join(
            ([f"{str(i)}, " for i in args] + [" kw, "])
            + [f"{str(i)}, " for i in sorted(kwargs.items())]
        )
        cache = FN_CACHE[func]
        if key in cache:
            return cache[key]
        ret = func(*args, **kwargs)
        cache[key] = ret
        return ret

    return cached_fn


@handle_exceptions
def current_backend_str() -> Union[str, None]:
    """Return framework string.

    Returns
    -------
    ret
        The framework string.
    """
    fw = current_backend()
    if not backend_stack:
        return ""
    return fw.current_backend_str()


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def einops_rearrange(
    x: Union[startai.Array, startai.NativeArray],
    pattern: str,
    /,
    *,
    out: Optional[startai.Array] = None,
    **axes_lengths: Dict[str, int],
) -> startai.Array:
    """Perform einops rearrange operation on input array x.

    Parameters
    ----------
    x
        Input array to be re-arranged.
    pattern
        Rearrangement pattern.
    axes_lengths
        Any additional specifications for dimensions.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

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

    >>> x = startai.array([[1, 2, 3, 4, 5, 6],
    ...            [7, 8, 9, 10, 11, 12]])
    >>> y = startai.zeros((4,3))
    >>> x.einops_rearrange("c (h w) -> (c h) w", out=y, h=2, w=3)
    >>> print(y)
    startai.array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 7,  8,  9],
           [10, 11, 12]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[-4.47, 0.93, -3.34],
    ...                            [3.66, 24.29, 3.64]]),
    ...               b=startai.array([[4.96, 1.52, -10.67],
    ...                            [4.36, 13.96, 0.3]]))
    >>> y = startai.einops_rearrange(x, 'a b -> b a')
    >>> print(y)
    {
        a: startai.array([[-4.46999979, 3.66000009],
                      [0.93000001, 24.29000092],
                      [-3.33999991, 3.6400001]]),
        b: startai.array([[4.96000004, 4.36000013],
                      [1.51999998, 13.96000004],
                      [-10.67000008, 0.30000001]])
    }

    With varying pattern:

    Suppose we have a set of 32 images in "h w c" format (height-width-channel)
    and concatenate images along height (vertical axis), 960 = 32 * 30

    >>> images = startai.asarray([startai.random_normal(shape=(30, 40, 3)) for _ in range(32)])
    >>> x = startai.einops_rearrange(images, 'b h w c -> (b h) w c')
    >>> print(x.shape)
    (960, 40, 3)

    # Concatenate images along horizontal axis, 1280 = 32 * 40

    >>> images = startai.asarray([startai.random_normal(shape=(30, 40, 3)) for _ in range(32)])
    >>> x = startai.einops_rearrange(images, 'b h w c -> h (b w) c')
    >>> print(x.shape)
    (30, 1280, 3)

    # Reorder axes to "b c h w" format for deep learning

    >>> images = startai.asarray([startai.random_normal(shape=(30, 40, 3)) for _ in range(32)])
    >>> x = startai.einops_rearrange(images, 'b h w c -> b c h w')
    >>> print(x.shape)
    (32, 3, 30, 40)

    # Flatten each image into a vector, 3600 = 30 * 40 * 3

    >>> images = startai.asarray([startai.random_normal(shape=(30, 40, 3)) for _ in range(32)])
    >>> x = startai.einops_rearrange(images, 'b h w c -> b (c h w)')
    >>> print(x.shape)
    (32, 3600)

    # Split each image into 4 smaller (top-left, top-right, bottom-left, bottom-right),
    # 128 = 32 * 2 * 2

    >>> images = startai.asarray([startai.random_normal(shape=(30, 40, 3)) for _ in range(32)])
    >>> x = startai.einops_rearrange(images, 'b (h1 h) (w1 w) c -> (b h1 w1) h w c',
    ... h1=2, w1=2)
    >>> print(x.shape)
    (128, 15, 20, 3)

    # Space-to-depth operation
    >>> images = startai.asarray([startai.random_normal(shape=(30, 40, 3)) for _ in range(32)])
    >>> x = startai.einops_rearrange(images, 'b (h h1) (w w1) c -> b h w (c h1 w1)', h1=2,
    ... w1=2)
    >>> print(x.shape)
    (32, 15, 20, 12)
    """
    ret = einops.rearrange(x._data, pattern, **axes_lengths)
    ret = startai.array(ret, dtype=x.dtype)
    if startai.exists(out):
        return startai.inplace_update(out, ret)
    return ret


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_native_arrays
@handle_array_function
def einops_reduce(
    x: Union[startai.Array, startai.NativeArray],
    pattern: str,
    reduction: Union[str, Callable],
    /,
    *,
    out: Optional[startai.Array] = None,
    **axes_lengths: Dict[str, int],
) -> startai.Array:
    """Perform einops reduce operation on input array x.

    Parameters
    ----------
    x
        Input array to be reduced.
    pattern
        Reduction pattern.
    reduction
        One of available reductions ('min', 'max', 'sum', 'mean', 'prod'), or callable.
    axes_lengths
        Any additional specifications for dimensions.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        New array with einops.reduce having been applied.

    This function is *nestable*, and therefore also accepts :code:'startai.Container'
    instance in place of the argument.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[-4.47, 0.93, -3.34],
    ...                [3.66, 24.29, 3.64]])
    >>> reduced = startai.einops_reduce(x, 'a b -> b', 'mean')
    >>> print(reduced)
    startai.array([-0.40499985, 12.61000061, 0.1500001 ])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[-4.47, 0.93, -3.34],
    ...                                [3.66, 24.29, 3.64]]),
    ...                   b=startai.array([[4.96, 1.52, -10.67],
    ...                                [4.36, 13.96, 0.3]]))
    >>> reduced = startai.einops_reduce(x, 'a b -> a', 'mean')
    >>> print(reduced)
    {
        a: startai.array([-2.29333329, 10.53000069]),
        b: startai.array([-1.39666676, 6.20666695])
    }
    """
    ret = einops.reduce(x, pattern, reduction, **axes_lengths)
    ret = startai.array(ret, dtype=x.dtype)
    if startai.exists(out):
        return startai.inplace_update(out, ret)
    return ret


# IMPORTANT: assign attribute directly to function instead of wrapper here
einops_reduce.unsupported_dtypes = {
    "torch": ("float16",),
    "tensorflow": ("complex",),
    "paddle": ("complex", "uint8", "int8", "int16", "float16"),
}


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def einops_repeat(
    x: Union[startai.Array, startai.NativeArray],
    pattern: str,
    /,
    *,
    out: Optional[startai.Array] = None,
    **axes_lengths: Dict[str, int],
) -> startai.Array:
    """Perform einops repeat operation on input array x.

    Parameters
    ----------
    x
        Input array to be repeated.
    pattern
        Rearrangement pattern.
    axes_lengths
        Any additional specifications for dimensions.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        New array with einops.repeat having been applied.

    This function is *nestable*, and therefore also accepts :code:'startai.Container'
    instance in place of the argument.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1, 2, 3, 4])
    >>> repeated = startai.einops_repeat(x, 'a -> b a', b=2)
    >>> print(repeated)
    startai.array([[1, 2, 3, 4],
               [1, 2, 3, 4]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[4,5],
    ...                                [1, 3]]),
    ...                    b=startai.array([[9, 10],
    ...                                 [4, 2]]))
    >>> repeated = startai.einops_repeat(x, 'h w -> h (c w)', c=2)
    >>> print(repeated)
    {
        a: startai.array([[4, 5, 4, 5],
                      [1, 3, 1, 3]]),
        b: startai.array([[9, 10, 9, 10],
                      [4, 2, 4, 2]])
    }
    """
    ret = einops.repeat(x._data, pattern, **axes_lengths)
    ret = startai.array(ret, dtype=x.dtype)
    if startai.exists(out):
        return startai.inplace_update(out, ret)
    return ret


startai.min_denominator = min_denominator_stack[-1] if min_denominator_stack else 1e-12


@handle_exceptions
@handle_array_function
def set_min_denominator(val: float) -> None:
    """Set the global minimum denominator used by startai for numerically stable
    division.

    Parameters
    ----------
    val
        The value to set the global minimum denominator to.

    Examples
    --------
    >>> x = startai.min_denominator
    >>> print(x)
    1e-12

    >>> startai.set_min_denominator(1e-13)
    >>> y = startai.min_denominator
    >>> print(y)
    1e-13
    """
    global min_denominator_stack
    startai.utils.assertions.check_isinstance(val, (int, float))
    min_denominator_stack.append(val)
    startai.__setattr__("min_denominator", val, True)


@handle_exceptions
def unset_min_denominator() -> None:
    """Reset the global minimum denominator used by startai for numerically stable
    division to the previous value.

    Examples
    --------
    >>> startai.set_min_denominator(1e-10)
    >>> y = startai.min_denominator
    >>> print(y)
    1e-10

    >>> startai.unset_min_denominator()
    >>> startai.min_denominator
    1e-12
    """
    global min_denominator_stack
    if min_denominator_stack:
        min_denominator_stack.pop(-1)
        val = min_denominator_stack[-1] if min_denominator_stack else 1e-12
        startai.__setattr__("min_denominator", val, True)


startai.min_base = min_base_stack[-1] if min_base_stack else 1e-05


@handle_exceptions
@handle_array_function
def set_min_base(val: float) -> None:
    """Set the global minimum base used by startai for numerically stable power
    raising.

    Parameters
    ----------
    val
        The new value to set the minimum base to.

    Examples
    --------
    Retrieve the minimum base
    >>> x = startai.min_base
    >>> print(x)
    1e-05

    >>> # Set the minimum base to 1e-04:
    >>> startai.set_min_base(1e-04)

    Retrieve the minimum base:
    >>> y = startai.min_base
    >>> print(y)
    1e-04

    >>> # unset the min_base
    >>> startai.unset_min_base()
    """
    global min_base_stack

    # Ensure val is an instance of 'float' or 'int'
    startai.utils.assertions.check_isinstance(val, (int, float))

    # Access and modify min_base_stack
    min_base_stack.append(val)

    # Set the min_base attribute
    startai.__setattr__("min_base", val, True)


@handle_exceptions
def unset_min_base() -> None:
    """Reset the global minimum base used by startai for numerically stable power
    raising to the previous value.

    Examples
    --------
    >>> startai.set_min_base(1e-07)
    >>> y = startai.min_base
    >>> print(y)
    1e-07

    >>> startai.unset_min_base()
    >>> startai.min_base
    1e-05
    """
    global min_base_stack
    if min_base_stack:
        min_base_stack.pop(-1)
        val = min_base_stack[-1] if min_base_stack else 1e-05
        startai.__setattr__("min_base", val, True)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def stable_divide(
    numerator: Union[Number, startai.Array, startai.NativeArray],
    denominator: Union[Number, startai.Array, startai.NativeArray],
    /,
    *,
    min_denominator: Union[Number, startai.Array, startai.NativeArray] = None,
) -> Union[Number, startai.Array]:
    """Divide the numerator by the denominator, with min denominator added to
    the denominator for numerical stability.

    Parameters
    ----------
    numerator
        The numerator of the division.
    denominator
        The denominator of the division.
    min_denominator
        The minimum denominator to use, use global startai._MIN_DENOMINATOR (1e-12)
        by default.

    Returns
    -------
    ret
        The new item following the numerically stable division.

    Examples
    --------
    With :code:`int` input:

    >>> x = startai.stable_divide(1, 2)
    >>> print(x)
    0.49999999999975

    >>> x = startai.stable_divide(1, 4, min_denominator=1)
    >>> print(x)
    0.2

    With float input:

    >>> x = startai.stable_divide(5.0, 3.33)
    >>> print(x)
    1.5015015015010504

    With :code:`complex` input:

    >>> x = startai.stable_divide(1+1j, 1-1j)
    >>> print(x)
    (5.000444502911705e-13+0.9999999999995j)

    With :class:`startai.Array` input:

    >>> x = startai.asarray([[10., 20., 30.],
    ...                  [40., 50., 60.]])
    >>> y = startai.stable_divide(x, 10.)
    >>> print(y)
    startai.array([[1., 2., 3.],
              [4., 5., 6.]])


    >>> x = startai.asarray([1,2,3])
    >>> y = np.array((1., 3., 5.))
    >>> z = startai.stable_divide(x, y)
    >>> print(z)
    startai.array([1.   , 0.667, 0.6  ])

    >>> x = startai.asarray([1., 2., 4.])
    >>> y = startai.asarray([1., 0.5, 0.25])
    >>> z = startai.asarray([0.01, 0.02, 0.03])
    >>> w = startai.stable_divide(x, y, min_denominator=z)
    >>> print(w)
    startai.array([ 0.99,  3.85, 14.3 ])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.asarray([10., 15.]), b=startai.asarray([20., 25.]))
    >>> y = startai.stable_divide(x, 0.5)
    >>> print(y)
    {
        a: startai.array([20., 30.]),
        b: startai.array([40., 50.])
    }


    >>> x = startai.Container(a=startai.asarray([1., 2.]), b=startai.asarray([3., 4.]))
    >>> y = startai.Container(a=startai.asarray([0.5, 2.5]), b=startai.asarray([3.5, 0.4]))
    >>> z = startai.stable_divide(x, y)
    >>> print(z)
    {
        a: startai.array([2., 0.8]),
        b: startai.array([0.857, 10.])
    }
    """
    return numerator / (denominator + default(min_denominator, startai.min_denominator))


@handle_exceptions
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
def stable_pow(
    base: Union[Number, startai.Array, startai.NativeArray],
    exponent: Union[Number, startai.Array, startai.NativeArray],
    /,
    *,
    min_base: Optional[float] = None,
) -> Any:
    """Raise the base by the power, with startai.min_base added to the base when
    exponent > 1 for numerical stability.

    Parameters
    ----------
    base
        The base number.
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
    With :code:`int` input:

    >>> x = startai.stable_pow(2, 2)
    >>> print(x)
    startai.array(4.00004)

    >>> x = startai.stable_pow(2, 2, min_base=2)
    >>> print(x)
    startai.array(16)

    With float input:

    >>> x = startai.stable_pow(4.0, .5)
    >>> print(x)
    startai.array(2.00000262)

    With :code:`complex` input:

    >>> x = startai.stable_pow(3+4j, 2j)
    >>> print(x)
    startai.array(-0.15605032-0.01208451j)

    With :class:`startai.Array` input:

    >>> x = startai.asarray([[2, 4],
    ...                  [6, 8]])
    >>> y = startai.stable_pow(x, 2)
    >>> print(y)
    startai.array([[ 4.00004, 16.00008],
           [36.00012, 64.00016]])

    >>> x = startai.asarray([2, 4, 6])
    >>> y = startai.asarray([2, 3, 4])
    >>> z = startai.stable_pow(x, y)
    >>> print(z)
    startai.array([   4.00004,   64.00048, 1296.00864])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.asarray([2, 4]), b=startai.asarray([6, 8]))
    >>> y = startai.stable_pow(x, 2)
    >>> print(y)
    {
        a: startai.array([4.00004, 16.00008]),
        b: startai.array([36.00012, 64.00016])
    }

    >>> x = startai.Container(a=startai.asarray([2, 4]), b=startai.asarray([6, 8]))
    >>> y = startai.Container(a=startai.asarray([1, 3]), b=startai.asarray([4, 5]))
    >>> z = startai.stable_pow(x, y)
    >>> print(z)
    {
        a: startai.array([2.00001, 64.00048]),
        b: startai.array([1296.00864, 32768.2048])
    }
    """
    return_dtype = startai.promote_types(
        startai.default_dtype(item=base),
        startai.default_dtype(item=default(min_base, startai.min_base)),
    )
    return_dtype = startai.promote_types(return_dtype, startai.default_dtype(item=exponent))
    ret = (base + default(min_base, startai.min_base)) ** startai.array(exponent)
    return ret.astype(return_dtype)


stable_pow.unsupported_dtypes = ("bfloat16",)


@handle_exceptions
def get_all_arrays_in_memory() -> List[Union[startai.Array, startai.NativeArray]]:
    """Get all arrays which are currently alive.

    Returns
    -------
    ret
        All arrays which are alive.

    Examples
    --------
    >>> startai.get_all_arrays_in_memory()
    []
    >>> x = startai.get_all_arrays_in_memory()
    >>> x
    []
    >>> y = startai.array([0, 1, 2])
    >>> x
    [startai.array([0, 1, 2])]
    """
    all_arrays = []
    for obj in gc.get_objects():
        try:
            if startai.current_backend_str() in ["", "numpy"]:
                if startai.is_startai_array(obj):
                    all_arrays.append(obj)
            else:
                if startai.is_native_array(obj):
                    all_arrays.append(obj)

        except Exception:
            pass
    return all_arrays


@handle_exceptions
def num_arrays_in_memory() -> int:
    """Return the number of arrays which are currently alive.

    Returns
    -------
    ret
        Number of all arrays which are alive.

    Examples
    --------
    >>> startai.num_arrays_in_memory()
    0
    >>> x = startai.num_arrays_in_memory()
    >>> x
    0
    >>> y = startai.array([0, 1, 2])
    >>> x
    1
    """
    return len(get_all_arrays_in_memory())


@handle_exceptions
def print_all_arrays_in_memory():
    """Print all native Startai arrays in memory to the console.

    Gets all the native Startai arrays which are currently alive(in the
    garbage collector) from get_all_arrays_in_memory() function and
    prints them to the console.
    """
    for arr in get_all_arrays_in_memory():
        print(type(arr), arr.shape)


startai.queue_timeout = queue_timeout_stack[-1] if queue_timeout_stack else 15.0


@handle_exceptions
@handle_array_function
def set_queue_timeout(timeout: float):
    """Set a timeout value (in seconds) for the global queue.

    Set the global queue timeout value (in seconds) Default value without this function
    being called is 15 seconds.

    Parameters
    ----------
    timeout
        The timeout when waiting for containers to arrive from the queues.
        To be set in seconds.

    Examples
    --------
    >>> x = startai.set_queue_timeout(10)
    >>> x = startai.queue_timeout
    >>> print(x)
    10.0

    >>> startai.set_queue_timeout(30)
    >>> y = startai.queue_timeout
    >>> print(y)
    30
    """
    global queue_timeout_stack
    startai.utils.assertions.check_isinstance(timeout, (int, float))
    queue_timeout_stack.append(timeout)
    startai.__setattr__("queue_timeout", timeout, True)


@handle_exceptions
def unset_queue_timeout() -> None:
    """Reset the global queue timeout value (in seconds) to the previous state.

    Examples
    --------
    >>> startai.set_queue_timeout(10.0)
    >>> y = startai.queue_timeout
    >>> print(y)
    10.0

    >>> startai.unset_queue_timeout()
    >>> startai.queue_timeout
    15.0
    """
    global queue_timeout_stack
    if queue_timeout_stack:
        queue_timeout_stack.pop(-1)
        timeout = queue_timeout_stack[-1] if queue_timeout_stack else 15.0
        startai.__setattr__("queue_timeout", timeout, True)


startai.tmp_dir = tmp_dir_stack[-1] if tmp_dir_stack else "/tmp"


@handle_exceptions
def set_tmp_dir(tmp_dr: str) -> None:
    """Set the directory for saving temporary files.

    Parameters
    ----------
    tmp_dr
        The new directory for saving temporary files

    Examples
    --------
    >>> x = startai.tmp_dir
    >>> print(x)
    /tmp

    >>> startai.set_tmp_dir("/my_tmp")
    >>> y = startai.tmp_dir
    >>> print(y)
    /my_tmp

    >>> # Unset the tmp_dr
    >>> startai.unset_tmp_dir()
    """
    global tmp_dir_stack
    startai.utils.assertions.check_isinstance(tmp_dr, str)
    tmp_dir_stack.append(tmp_dr)
    startai.__setattr__("tmp_dir", tmp_dr, True)


@handle_exceptions
def unset_tmp_dir() -> None:
    """Reset the directory for saving temporary files to the previous value.

    Examples
    --------
    >>> startai.set_tmp_dir("/my_dir")
    >>> y = startai.tmp_dir
    >>> print(y)
    /my_dir

    >>> startai.unset_tmp_dir()
    >>> startai.tmp_dir
    /tmp
    """
    global tmp_dir_stack
    if tmp_dir_stack:
        tmp_dir_stack.pop(-1)
        tmp_dr = tmp_dir_stack[-1] if tmp_dir_stack else "/tmp"
        startai.__setattr__("tmp_dir", tmp_dr, True)


@handle_exceptions
def container_types():
    """Summary.

    Returns
    -------
    ret
        a key-value structure, and exposes public methods .keys(), .values() and
        items().
    """
    # noinspection PyBroadException
    try:
        return current_backend().container_types()
    except ValueError:
        return []


@handle_exceptions
def inplace_arrays_supported() -> bool:
    """Determine whether inplace arrays are supported for the current backend
    framework.

    Returns
    -------
    ret
        Boolean, whether or not inplace arrays are supported.
    """
    return current_backend().inplace_arrays_supported()


@handle_exceptions
def inplace_variables_supported() -> bool:
    """Determine whether inplace variables are supported for the current
    backend framework.

    Returns
    -------
    ret
        Boolean, whether or not inplace variables are supported.
    """
    return current_backend().inplace_variables_supported()


@handle_exceptions
@handle_nestable
@inputs_to_native_arrays
@handle_array_function
def supports_inplace_updates(x: Union[startai.Array, startai.NativeArray], /) -> bool:
    """Return if in-place operations are supported for x's data type.

    Determine whether in-place operations are supported for x's data type, by the
    current backend framework setting.

    Parameters
    ----------
    x
        Input variable for whose data type we check whether the current backend
        framework supports in-place operations.

    Returns
    -------
    ret
        Value depends on whether in-place operations are supported for
        data type of x.

    Raises
    ------
    StartaiException
        If x isn't a class instance of startai.Array or startai.NativeArray, an exception will
        be raised.

    This function is *nestable*, and therefore also accepts :code:'startai.Container'
    instance in place of the argument.

    Examples
    --------
    With :class:`startai.Array` input and default backend set as `numpy`:

    >>> x = startai.array([0, 1, 2])
    >>> y = startai.supports_inplace_updates(x)
    >>> print(y)
    True

    With :class:`startai.Container` input and backend set as `torch`:

    >>> x = startai.Container(a=startai.array([5., 6.]), b=startai.array([7., 8.]))
    >>> y = startai.supports_inplace_updates(x)
    >>> print(y)
    {
        a: True,
        b: True
    }

    With `startai.Array` input and backend set as "tensorflow":

    >>> x = startai.array([1., 4.2, 2.2])
    >>> ret = x.supports_inplace_updates()
    >>> print(ret)
    False
    """
    if _is_variable(x):
        return startai.inplace_variables_supported()
    elif startai.is_native_array(x):
        return startai.inplace_arrays_supported()
    raise startai.utils.exceptions.StartaiException(
        "Input x must be either a variable or an array."
    )


@handle_exceptions
@handle_nestable
@inputs_to_native_arrays
@handle_array_function
def assert_supports_inplace(x: Union[startai.Array, startai.NativeArray], /) -> bool:
    """Assert that inplace operations are supported for x.

    Parameters
    ----------
    x
        Input variable or array to check for inplace support for.

    Returns
    -------
    ret
        True if supports, raises StartaiBackendException otherwise

    This function is *nestable*, and therefore also accepts :code:'startai.Container'
    instance in place of the argument.

    Examples
    --------
    With :class:`startai.Array` input and default backend set as `numpy`:

    >>> startai.set_backend("numpy")
    >>> x = startai.array([1, 2, 3])
    >>> print(x.assert_supports_inplace())
    True

    With :class:`startai.Array` input and default backend set as `torch`:

    >>> startai.set_backend("torch")
    >>> x = startai.array([1, 2, 3])
    >>> print(x.assert_supports_inplace())
    True

    With :class:`startai.Container` input and default backend set as `numpy`:

    >>> startai.set_backend("numpy")
    >>> x = startai.Container(a=startai.array([5, 6]), b=startai.array([7, 8]))
    >>> print(x.assert_supports_inplace())
    {
        a: True,
        b: True
    }

    With :class:`startai.Container` input and default backend set as `torch`:

    >>> startai.set_backend("torch")
    >>> x = startai.Container(a=startai.array([5, 6]), b=startai.array([7, 8]))
    >>> print(x.assert_supports_inplace())
    {
        a: True,
        b: True
    }
    """
    startai.utils.assertions.check_true(
        startai.supports_inplace_updates(x),
        f"Inplace operations are not supported {type(x)} types with"
        f" {startai.current_backend_str()} backend",
    )
    return True


@handle_nestable
@handle_partial_mixed_function
@handle_view_indexing
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def get_item(
    x: Union[startai.Array, startai.NativeArray],
    /,
    query: Union[startai.Array, startai.NativeArray, Tuple],
    *,
    copy: Optional[bool] = None,
) -> startai.Array:
    """Gather slices from x according to query array, identical to x[query].

    Parameters
    ----------
    x
        array, the array from which to gather values.
    query
        array, index array, integer indices or boolean mask.
    copy
        boolean indicating whether or not to copy the input array.
        If True, the function must always copy.
        If False, the function must never copy.
        In case copy is False we avoid copying by returning a view of the input array.

    Returns
    -------
    ret
        New array with the values gathered at the specified indices.

    Examples
    --------
    >>> x = startai.array([0, -1, 20])
    >>> query = startai.array([0, 1])
    >>> print(startai.get_item(x, query))
    startai.array([ 0, -1])

    >>> x = startai.array([[4, 5], [20, 128], [-2, -10]])
    >>> query = startai.array([[True, False], [False, False], [True, True]])
    >>> print(startai.get_item(x, query))
    startai.array([  4,  -2, -10])
    """
    if startai.is_array(query) and startai.is_bool_dtype(query):
        if query.ndim == 0:
            if query is False:
                return startai.zeros(shape=(0,) + x.shape, dtype=x.dtype)
            return x[None]  # equivalent to startai.expand_dims(x, axis=0)
        query = startai.nonzero(query, as_tuple=False)
        ret = startai.gather_nd(x, query)
    else:
        query, target_shape, vector_inds = _parse_query(
            query, startai.shape(x, as_array=True)
        )
        if vector_inds is not None:
            x = startai.permute_dims(
                x,
                axes=[
                    *vector_inds,
                    *[i for i in range(len(x.shape)) if i not in vector_inds],
                ],
            )
        ret = startai.gather_nd(x, query)
        ret = startai.reshape(ret, target_shape) if target_shape != list(ret.shape) else ret
    return ret


get_item.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}


@handle_nestable
@handle_partial_mixed_function
@inputs_to_startai_arrays
@handle_array_function
def set_item(
    x: Union[startai.Array, startai.NativeArray],
    query: Union[startai.Array, startai.NativeArray, Tuple],
    val: Union[startai.Array, startai.NativeArray],
    /,
    *,
    copy: Optional[bool] = False,
) -> startai.Array:
    """Replace slices of x (defined by query) with val, identical to x[query] =
    val.

    Parameters
    ----------
    x
        the array to be updated.
    query
        either an index array, or a tuple of integers or slices.
    val
        the array containing the values to be infused into x
    copy
        boolean indicating whether to copy x.
        If True, the function will update and return a copy of x.
        If False, the function will update x inplace.

    Returns
    -------
    ret
        the array with updated values at the specified indices.

    Examples
    --------
    >>> x = startai.array([0, -1, 20])
    >>> query = startai.array([0, 1])
    >>> val = startai.array([10, 10])
    >>> startai.set_item(x, query, val)
    >>> print(x)
    startai.array([10, 10, 20])

    >>> x = startai.array([[0, -1, 20], [5, 2, -8]])
    >>> query = startai.array([1, 1])
    >>> val = startai.array([10, 10])
    >>> y = startai.set_item(x, query, val, copy=True)
    >>> print(y)
    startai.array([[ 0, -1, 20],
           [10, 10, 10]])
    """
    if copy:
        x = startai.copy_array(x)
    if not startai.is_array(val):
        val = startai.array(val)
    if 0 in x.shape or 0 in val.shape:
        return x
    if startai.is_array(query) and startai.is_bool_dtype(query):
        if not len(query.shape):
            query = startai.tile(query, (x.shape[0],))
        indices = startai.nonzero(query, as_tuple=False)
    else:
        indices, target_shape, _ = _parse_query(
            query, startai.shape(x, as_array=True), scatter=True
        )
        if indices is None:
            return x
    val = val.astype(x.dtype)
    ret = startai.scatter_nd(indices, val, reduction="replace", out=x)
    return ret


set_item.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}


def _parse_query(query, x_shape, scatter=False):
    query = (query,) if not isinstance(query, tuple) else query

    # sequence and integer queries are dealt with as array queries
    query = [startai.array(q) if isinstance(q, (tuple, list, int)) else q for q in query]

    # check if non-slice queries are in consecutive positions
    # if so, they have to be moved to the front
    # https://numpy.org/neps/nep-0021-advanced-indexing.html#mixed-indexing
    non_slice_q_idxs = [i for i, q in enumerate(query) if startai.is_array(q)]
    to_front = (
        len(non_slice_q_idxs) > 1
        and any(startai.diff(non_slice_q_idxs) != 1)
        and non_slice_q_idxs[-1] < len(x_shape)
    )

    # extract newaxis queries
    new_axes = [i for i, q in enumerate(query) if q is None]
    query = [q for q in query if q is not None]
    query = [Ellipsis] if query == [] else query

    # parse ellipsis
    ellipsis_inds = None
    if any(q is Ellipsis for q in query):
        query, ellipsis_inds = _parse_ellipsis(query, len(x_shape))

    # broadcast array queries
    array_inds = [i for i, v in enumerate(query) if startai.is_array(v)]
    if array_inds:
        array_queries = startai.broadcast_arrays(
            *[v for i, v in enumerate(query) if i in array_inds]
        )
        array_queries = [
            startai.nonzero(q, as_tuple=False)[0] if startai.is_bool_dtype(q) else q
            for q in array_queries
        ]
        array_queries = [
            (
                startai.where(arr < 0, arr + x_shape[i], arr).astype(startai.int64)
                if arr.size
                else arr.astype(startai.int64)
            )
            for arr, i in zip(array_queries, array_inds)
        ]
        for idx, arr in zip(array_inds, array_queries):
            query[idx] = arr

    # convert slices to range arrays
    query = [
        _parse_slice(q, x_shape[i]).astype(startai.int64) if isinstance(q, slice) else q
        for i, q in enumerate(query)
    ]

    # fill in missing queries
    if len(query) < len(x_shape):
        query += [startai.arange(0, s, 1).astype(startai.int64) for s in x_shape[len(query) :]]

    # calculate target_shape, i.e. the shape the gathered/scattered values should have
    if len(array_inds) and to_front:
        target_shape = (
            [list(array_queries[0].shape)]
            + [list(query[i].shape) for i in range(len(query)) if i not in array_inds]
            + [[] for _ in range(len(array_inds) - 1)]
        )
    elif len(array_inds):
        target_shape = (
            [list(query[i].shape) for i in range(0, array_inds[0])]
            + [list(startai.shape(array_queries[0], as_array=True))]
            + [[] for _ in range(len(array_inds) - 1)]
            + [list(query[i].shape) for i in range(array_inds[-1] + 1, len(query))]
        )
    else:
        target_shape = [list(q.shape) for q in query]
    if ellipsis_inds is not None:
        target_shape = (
            target_shape[: ellipsis_inds[0]]
            + [target_shape[ellipsis_inds[0] : ellipsis_inds[1]]]
            + target_shape[ellipsis_inds[1] :]
        )
    for i, ax in enumerate(new_axes):
        if len(array_inds) and to_front:
            ax -= sum(1 for x in array_inds if x < ax) - 1
            ax = ax + i
        target_shape = [*target_shape[:ax], 1, *target_shape[ax:]]
    target_shape = _deep_flatten(target_shape)

    # calculate the indices mesh (indices in gather_nd/scatter_nd format)
    query = [startai.expand_dims(q) if not len(q.shape) else q for q in query]
    if len(array_inds):
        array_queries = [
            (
                arr.reshape((-1,))
                if len(arr.shape) > 1
                else startai.expand_dims(arr) if not len(arr.shape) else arr
            )
            for arr in array_queries
        ]
        array_queries = startai.stack(array_queries, axis=1)
    if len(array_inds) == len(query):  # advanced indexing
        indices = array_queries.reshape((*target_shape, len(x_shape)))
    elif len(array_inds) == 0:  # basic indexing
        indices = startai.stack(startai.meshgrid(*query, indexing="ij"), axis=-1).reshape(
            (*target_shape, len(x_shape))
        )
    else:  # mixed indexing
        if to_front:
            post_array_queries = (
                startai.stack(
                    startai.meshgrid(
                        *[v for i, v in enumerate(query) if i not in array_inds],
                        indexing="ij",
                    ),
                    axis=-1,
                ).reshape((-1, len(query) - len(array_inds)))
                if len(array_inds) < len(query)
                else startai.empty((1, 0))
            )
            indices = startai.array(
                [
                    (*arr, *post)
                    for arr, post in itertools.product(
                        array_queries, post_array_queries
                    )
                ]
            ).reshape((*target_shape, len(x_shape)))
        else:
            pre_array_queries = (
                startai.stack(
                    startai.meshgrid(
                        *[v for i, v in enumerate(query) if i < array_inds[0]],
                        indexing="ij",
                    ),
                    axis=-1,
                ).reshape((-1, array_inds[0]))
                if array_inds[0] > 0
                else startai.empty((1, 0))
            )
            post_array_queries = (
                startai.stack(
                    startai.meshgrid(
                        *[v for i, v in enumerate(query) if i > array_inds[-1]],
                        indexing="ij",
                    ),
                    axis=-1,
                ).reshape((-1, len(query) - 1 - array_inds[-1]))
                if array_inds[-1] < len(query) - 1
                else startai.empty((1, 0))
            )
            indices = startai.array(
                [
                    (*pre, *arr, *post)
                    for pre, arr, post in itertools.product(
                        pre_array_queries, array_queries, post_array_queries
                    )
                ]
            ).reshape((*target_shape, len(x_shape)))

    return (
        indices.astype(startai.int64),
        target_shape,
        array_inds if len(array_inds) and to_front else None,
    )


def _parse_ellipsis(so, ndims):
    pre = list()
    for s in so:
        if s is Ellipsis:
            break
        pre.append(s)
    post = list()
    for s in reversed(so):
        if s is Ellipsis:
            break
        post.append(s)
    ret = list(
        pre
        + [slice(None, None, None) for _ in range(ndims - len(pre) - len(post))]
        + list(reversed(post))
    )
    return ret, (len(pre), ndims - len(post))


def _parse_slice(idx, s):
    step = 1 if idx.step is None else idx.step
    if step > 0:
        start = 0 if idx.start is None else idx.start
        if start >= s:
            stop = start
        else:
            if start <= -s:
                start = 0
            elif start < 0:
                start = start + s
            stop = s if idx.stop is None else idx.stop
            if stop > s:
                stop = s
            elif start <= -s:
                stop = 0
            elif stop < 0:
                stop = stop + s
    else:
        start = s - 1 if idx.start is None else idx.start
        if start < -s:
            stop = start
        else:
            if start >= s:
                start = s - 1
            elif start < 0:
                start = start + s
            if idx.stop is None:
                stop = -1
            else:
                stop = idx.stop
                if stop > s:
                    stop = s
                elif stop < -s:
                    stop = -1
                elif stop == -s:
                    stop = 0
                elif stop < 0:
                    stop = stop + s
    q_i = startai.arange(start, stop, step)
    q_i = [q for q in q_i if 0 <= q < s]
    q_i = (
        startai.array(q_i)
        if len(q_i) or start == stop or idx.stop is not None
        else startai.arange(0, s, 1)
    )
    return q_i


def _deep_flatten(iterable):
    def _flatten_gen(iterable):
        for item in iterable:
            if isinstance(item, list):
                yield from _flatten_gen(item)
            else:
                yield item

    return list(_flatten_gen(iterable))


def _numel(shape):
    shape = tuple(shape)
    return startai.prod(shape).to_scalar() if shape != () else 1


def _broadcast_to(input, target_shape):
    if _numel(tuple(input.shape)) == _numel(tuple(target_shape)):
        return startai.reshape(input, target_shape)
    else:
        input = input if len(input.shape) else startai.expand_dims(input, axis=0)
        return startai.broadcast_to(input, target_shape)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def inplace_update(
    x: Union[startai.Array, startai.NativeArray],
    val: Union[startai.Array, startai.NativeArray],
    /,
    *,
    ensure_in_backend: bool = False,
    keep_input_dtype: bool = False,
) -> startai.Array:
    """Perform in-place update for the input array.

    This will always be performed on startai.Array instances pass in the input, and will
    also be performed on the native array classes in the backend when the backend
    supports this. If the backend does not natively support inplace updates, and x is an
    startai.NativeArray instance, then an
    exception will be thrown.

    Parameters
    ----------
    x
        The variable to update.
    val
        The array to update the variable with.
    ensure_in_backend
        Whether or not to ensure that the `startai.NativeArray` is also inplace updated.
        In cases where it should be, backends which do not natively support inplace
        updates will raise an exception.
    keep_input_dtype
        Whether or not to preserve `x` data type after the update, otherwise `val`
        data type will be applied. Defaults to False.

    Returns
    -------
    ret
        The array following the in-place update.

    Raises
    ------
    StartaiException
        If backend set doesn't natively support inplace updates and ensure_in_backend is
        True, above exception will be raised.

    This function is *nestable*, and therefore also accepts :code:'startai.Container'
    instance in place of the arguments.

    Examples
    --------
    With :class:`startai.Array` input and default backend set as `numpy`:

    >>> startai.set_backend("numpy")
    >>> x = startai.array([1, 2, 3])
    >>> y = startai.array([0])
    >>> startai.inplace_update(x, y)
    >>> print(x)
    startai.array([0])

    With :class:`startai.Array` input and default backend set as `numpy`:

    >>> startai.set_backend("numpy")
    >>> x = startai.array([1, 2, 3], dtype=startai.float32)
    >>> y = startai.array([0, 0, 0], dtype=startai.int32)
    >>> startai.inplace_update(x, y, keep_input_dtype=True)
    >>> print(x)
    startai.array([0., 0., 0.])

    With :class:`startai.Container` instances:, and backend set as `torch`:

    >>> startai.set_backend("torch")
    >>> x = startai.Container(a=startai.array([5, 6]), b=startai.array([7, 8]))
    >>> y = startai.Container(a=startai.array([1]), b=startai.array([2]))
    >>> startai.inplace_update(x, y)
    >>> print(x)
    {
        a: startai.array([1, 1]),
        b: startai.array([2, 2])
    }

    With mix of :class:`startai.Array` and :class:`startai.Container` instances:, and backend
    set as `torch`:

    >>> startai.set_backend("torch")
    >>> x = startai.Container(a=startai.array([5, 6]), b=startai.array([7, 8]))
    >>> y = startai.array([1, 2])
    >>> startai.inplace_update(x, y)
    >>> print(x)
    {
        a: startai.array([1, 2]),
        b: startai.array([1, 2])
    }
    """
    return current_backend(x).inplace_update(
        x,
        val,
        ensure_in_backend=ensure_in_backend,
        keep_input_dtype=keep_input_dtype,
    )


inplace_update.unsupported_dtypes = {"torch": ("bfloat16",)}

startai.inplace_mode = inplace_mode_stack[-1] if inplace_mode_stack else "lenient"


@handle_exceptions
def set_inplace_mode(mode: str = "lenient") -> None:
    """Set the memory management behavior for in-place updates in Startai.

    By default, Startai creates new arrays in the backend for in-place updates.
    However, this behavior can be controlled by the user
    using the 'inplace_mode' parameter.

    Parameters
    ----------
    mode : str
        The mode for memory management during in-place updates.
        - 'lenient': (Default) In this mode, new arrays will be created during
                    in-place updates to avoid breaking existing code.
                    This is the default behavior.
        - 'strict': In this mode, an error will be raised if the
                    'inplace_update' function is called
                    in a backend that doesn't support inplace updates natively.

    Returns
    -------
    None

    Examples
    --------
    >>> set_inplace_mode('lenient')
    >>> startai.inplace_mode
    'lenient'

    >>> set_inplace_mode('strict')
    >>> startai.inplace_mode
    'strict'

    Note
    ----
    Enabling strict mode can help users have more control over memory management
    but may lead to errors if the backend doesn't support inplace updates natively.
    """
    global inplace_mode_stack
    inplace_modes = ["lenient", "strict"]
    startai.utils.assertions.check_elem_in_list(
        mode, inplace_modes, False, f"inplace mode must be one of {inplace_modes}"
    )
    inplace_mode_stack.append(mode)
    startai.__setattr__("inplace_mode", mode, True)


@handle_exceptions
def unset_inplace_mode() -> None:
    """Reset the memory management behavior for in-place updates in Startai to the
    previous state.

    Examples
    --------
    >>> set_inplace_mode('strict')
    >>> startai.inplace_mode
    'strict'

    >>> unset_inplace_mode()
    >>> startai.inplace_mode
    'lenient'
    """
    global inplace_mode_stack
    if inplace_mode_stack:
        inplace_mode_stack.pop(-1)
        mode = inplace_mode_stack[-1] if inplace_mode_stack else "lenient"
        startai.__setattr__("inplace_mode", mode, True)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def inplace_decrement(
    x: Union[startai.Array, startai.NativeArray],
    val: Union[startai.Array, startai.NativeArray],
) -> startai.Array:
    """Perform in-place decrement for the input array.

    Parameters
    ----------
    x
        The input array to be decremented by the defined value.
    val
        The value of decrement.

    Returns
    -------
    ret
        The array following the in-place decrement.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[5.3, 7., 0.],[6.8, 8, 3.9],[0., 10., 6.3]])
    >>> y = startai.inplace_decrement(x, 1.25)
    >>> print(y)
    startai.array([[ 4.05,  5.75, -1.25],
       [ 5.55,  6.75,  2.65],
       [-1.25,  8.75,  5.05]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0.5, -5., 30.]), b=startai.array([0., -25., 50.]))
    >>> y = startai.inplace_decrement(x, 1.5)
    >>> print(y)
    {
        a: startai.array([-1., -6.5, 28.5]),
        b: startai.array([-1.5, -26.5, 48.5])
    }

    >>> x = startai.Container(a=startai.array([0., 15., 30.]), b=startai.array([0., 25., 50.]))
    >>> y = startai.Container(a=startai.array([0., 15., 30.]), b=startai.array([0., 25., 50.]))
    >>> z = startai.inplace_decrement(x, y)
    >>> print(z)
    {
        a: startai.array([0., 0., 0.]),
        b: startai.array([0., 0., 0.])
    }

    >>> x = startai.Container(a=startai.array([3., 7., 10.]), b=startai.array([0., 75., 5.5]))
    >>> y = startai.Container(a=startai.array([2., 5.5, 7.]), b=startai.array([0., 25., 2.]))
    >>> z = startai.inplace_decrement(x, y)
    >>> print(z)
    {
        a: startai.array([1., 1.5, 3.]),
        b: startai.array([0., 50., 3.5])
    }
    """
    return current_backend(x).inplace_decrement(x, val)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@inputs_to_startai_arrays
@handle_array_function
@handle_device
def inplace_increment(
    x: Union[startai.Array, startai.NativeArray],
    val: Union[startai.Array, startai.NativeArray],
) -> startai.Array:
    """Perform in-place increment for the input array.

    Parameters
    ----------
    x
        The input array to be incremented by the defined value.
    val
        The value of increment.

    Returns
    -------
    ret
        The array following the in-place increment.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[5.3, 7., 0.],[6.8, 8, 3.9],[0., 10., 6.3]])
    >>> y = startai.inplace_increment(x, 3.)
    >>> print(y)
    startai.array([[ 8.3, 10.,  3.],
       [ 9.8, 11.,  6.9],
       [ 3., 13.,  9.3]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0., 15., 30.]), b=startai.array([0., 25., 50.]))
    >>> y = startai.inplace_increment(x, 2.5)
    >>> print(y)
    {
        a: startai.array([2.5, 17.5, 32.5]),
        b: startai.array([2.5, 27.5, 52.5])
    }


    >>> x = startai.Container(a=startai.array([0., 15., 30.]), b=startai.array([0., 25., 50.]))
    >>> y = startai.Container(a=startai.array([0., 15., 30.]), b=startai.array([0., 25., 50.]))
    >>> z = startai.inplace_increment(x, y)
    >>> print(z)
    {
        a: startai.array([0., 30., 60.]),
        b: startai.array([0., 50., 100.])
    }
    """
    return current_backend(x).inplace_increment(x, val)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@to_native_arrays_and_back
@handle_array_function
@handle_device
def scatter_flat(
    indices: Union[startai.Array, startai.NativeArray],
    updates: Union[startai.Array, startai.NativeArray],
    /,
    *,
    size: Optional[int] = None,
    reduction: str = "sum",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Scatter flat updates into a new flat array according to flat indices.

    Parameters
    ----------
    indices
        Indices for the new values to occupy.
    updates
        Values for the new array to hold.
    size
        The size of the result. Default is `None`, in which case tensor
        argument out must be provided.
    reduction
        The reduction method for the scatter, one of 'sum', 'min', 'max' or 'replace'
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        New array of given shape, with the values scattered at the indices.

    This function is *nestable*, and therefore also accepts :code:'startai.Container'
    instance in place of the argument.

    Examples
    --------
    With :class:`startai.Array` input:
    >>> indices = startai.array([0, 0, 1, 0, 2, 2, 3, 3])
    >>> updates = startai.array([5, 1, 7, 2, 3, 2, 1, 3])
    >>> out = startai.array([0, 0, 0, 0, 0, 0, 0, 0])
    >>> startai.scatter_flat(indices, updates, out=out)
    >>> print(out)
    startai.array([8, 7, 5, 4, 0, 0, 0, 0])


    With :class:`startai.Array` input:
    >>> indices = startai.array([1, 0, 1, 0, 2, 2, 3, 3])
    >>> updates = startai.array([9, 2, 0, 2, 3, 2, 1, 8])
    >>> size = 8
    >>> print(startai.scatter_flat(indices, updates, size=size))
    startai.array([2, 0, 2, 8, 0, 0, 0, 0])


    With :class:`startai.Container` and :class:`startai.Array` input:
    >>> indices = startai.array([1, 0, 1, 0, 2, 2, 3, 3])
    >>> updates = startai.Container(a=startai.array([9, 2, 0, 2, 3, 2, 1, 8]),
    ...                 b=startai.array([5, 1, 7, 2, 3, 2, 1, 3]))
    >>> size = 8
    >>> print(startai.scatter_flat(indices, updates, size=size))
    {
        a: startai.array([2, 0, 2, 8, 0, 0, 0, 0]),
        b: startai.array([2, 7, 2, 3, 0, 0, 0, 0])
    }


    With :class:`startai.Container` input:
    >>> indices = startai.Container(a=startai.array([1, 0, 1, 0, 2, 2, 3, 3]),
    ...                 b=startai.array([0, 0, 1, 0, 2, 2, 3, 3]))
    >>> updates = startai.Container(a=startai.array([9, 2, 0, 2, 3, 2, 1, 8]),
    ...                 b=startai.array([5, 1, 7, 2, 3, 2, 1, 3]))
    >>> size = 8
    >>> print(startai.scatter_flat(indices, updates, size=size))
    {
        a: startai.array([2, 0, 2, 8, 0, 0, 0, 0]),
        b: startai.array([2, 7, 2, 3, 0, 0, 0, 0])
    }
    """
    return current_backend(indices).scatter_flat(
        indices, updates, size=size, reduction=reduction, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@inputs_to_native_shapes
@to_native_arrays_and_back
@handle_array_function
@handle_device
def scatter_nd(
    indices: Union[startai.Array, startai.NativeArray],
    updates: Union[startai.Array, startai.NativeArray],
    /,
    shape: Optional[Union[tuple, list, startai.Array, startai.Shape, startai.NativeShape]] = None,
    *,
    reduction: str = "sum",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Scatter updates into a new array according to indices.

    Parameters
    ----------
    indices
        Indices for the new values to occupy.
    updates
        Values for the new array to hold.
    shape
        The shape of the result. Default is ``None``, in which case tensor
        argument must be provided.
    reduction
        The reduction method for the scatter, one of 'sum', 'min', 'max' or 'replace'
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        New array of given shape, with the values scattered at the indices.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> indices = startai.array([[4], [3], [7], [7]])
    >>> updates = startai.array([9, 12, 11, 10])
    >>> shape = startai.array([8])
    >>> scatter = startai.scatter_nd(indices, updates, shape)
    >>> print(scatter)
    startai.array([ 0,  0,  0, 12,  9,  0,  0, 21])

    >>> indices = startai.array([[0, 1], [1, 0], [1, 1], [1, 1]])
    >>> updates = startai.array([9, 11, 12, 10])
    >>> shape = (2, 2)
    >>> scatter = startai.scatter_nd(indices, updates, shape, reduction="max")
    >>> print(scatter)
    startai.array([[ 0,  9], [11, 12]])

    >>> indices = startai.array([[[0], [1]], [[2], [1]]])
    >>> updates = startai.array([[9, 12], [11, 10]])
    >>> shape = [4]
    >>> scatter = startai.scatter_nd(indices, updates, shape, reduction="replace")
    >>> print(scatter)
    startai.array([ 9, 10, 11,  0])

    >>> indices = startai.array([[[1, 1], [0, 0]], [[1, 1], [0, 0]]])
    >>> updates = startai.array([[-1, 12], [11, 10]])
    >>> shape = startai.Shape([2, 2])
    >>> result = startai.zeros([2, 2])
    >>> scatter = startai.scatter_nd(indices, updates, shape, reduction="min", out=result)
    >>> print(result)
    startai.array([[ 0.,  0.], [ 0., -1.]])

    With :class:`startai.Container` input:

    >>> indices = startai.Container(a=startai.array([[4],[3],[6]]),
    ...                         b=startai.array([[5],[1],[2]]))
    >>> updates = startai.Container(a=startai.array([100, 200, 200]),
    ...                         b=startai.array([20, 30, 40]))
    >>> shape = startai.Container(a=startai.array([10]),
    ...                       b=startai.array([10]))
    >>> z = startai.scatter_nd(indices, updates, shape=shape)
    >>> print(z)
    {
        a: startai.array([0, 0, 0, 200, 100, 0, 200, 0, 0, 0]),
        b: startai.array([0, 30, 40, 0, 0, 20, 0, 0, 0, 0])
    }

    With :class:`startai.Container` and :class:`startai.Array` input:

    >>> indices = startai.array([[4],[3],[1]])
    >>> updates = startai.Container(a=startai.array([10, 20, 30]),
    ...                         b=startai.array([200, 300, 400]))
    >>> z = startai.Container(a=startai.array([1, 2, 3, 4, 5]),
    ...                   b=startai.array([10, 20, 30, 40, 50]))
    >>> startai.scatter_nd(indices, updates, reduction="replace", out=z)
    >>> print(z)
    {
        a: startai.array([1, 30, 3, 20, 10]),
        b: startai.array([10, 400, 30, 300, 200])
    }
    """
    return current_backend(indices).scatter_nd(
        indices, updates, shape=shape, reduction=reduction, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def gather(
    params: Union[startai.Array, startai.NativeArray],
    indices: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: int = -1,
    batch_dims: int = 0,
    out: Optional[Union[startai.Array, startai.NativeArray]] = None,
) -> Union[startai.Array, startai.NativeArray]:
    """Gather slices from params at axis according to indices.

    Parameters
    ----------
    params
        The array from which to gather values.
    indices
        The array which indicates the indices that will be gathered along
        the specified axis.
    axis
        Optional int, the axis from which to gather from.
        Default is ``-1``.
    batch_dims
        Optional int, lets you gather different items from each element of a batch.
        Default is ``0``.
    out
        Optional array, for writing the result to. It must have a shape
        that the inputs broadcast to.

    Returns
    -------
    ret
        New array with the values gathered at the specified indices along the
        specified axis.


    Both the description and the type hints above assumes an array input for
    simplicity, but this function is *nestable*, and therefore also accepts
    :class:`startai.Container` instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0., 1., 2.])
    >>> y = startai.array([1, 2])
    >>> print(startai.gather(x, y))
    startai.array([1., 2.])

    >>> x = startai.array([[0., 1., 2.],[3., 4., 5.]])
    >>> y = startai.array([[0, 1],[1, 2]])
    >>> z = startai.zeros((2, 2, 2))
    >>> startai.gather(x, y, out=z)
    >>> print(z)
    startai.array([[[0., 1.],[1., 2.]],[[3., 4.],[4., 5.]]])

    >>> x = startai.array([[[0., 1.], [2., 3.]],
    ...                [[8., 9.], [10., 11.]]])
    >>> y = startai.array([[0, 1]])
    >>> z = startai.zeros((1, 2, 2, 2))
    >>> startai.gather(x, y, axis=0, out=z)
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
    >>> z = startai.gather(x, y, batch_dims=1)
    >>> print(z)
    startai.array([[10, 20], [30, 40],[10, 40]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a = startai.array([0., 1., 2.]),
    ...                   b = startai.array([4., 5., 6.]))
    >>> y = startai.Container(a = startai.array([0, 1]),
    ...                   b = startai.array([1, 2]))
    >>> print(startai.gather(x, y))
    {
        a: startai.array([0., 1.]),
        b: startai.array([5., 6.])
    }

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.Container(a = startai.array([0., 1., 2.]),
    ...                   b = startai.array([4., 5., 6.]))
    >>> y = startai.array([0, 1])
    >>> print(startai.gather(x, y))
    {
        a: startai.array([0., 1.]),
        b: startai.array([4., 5.])
    }
    """
    return current_backend(params, indices).gather(
        params, indices, axis=axis, batch_dims=batch_dims, out=out
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def gather_nd(
    params: Union[startai.Array, startai.NativeArray],
    indices: Union[startai.Array, startai.NativeArray],
    /,
    *,
    batch_dims: int = 0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Gather slices from params into a array with shape specified by indices.

    Parameters
    ----------
    params
        The array from which to gather values.
    indices
        Index array.
    batch_dims
        optional int, lets you gather different items from each element of a batch.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        New array of given shape, with the values gathered at the indices.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0., 1., 2., 3., 4., 5., 6.])
    >>> y = startai.array([1])
    >>> print(startai.gather_nd(x, y))
    startai.array(1.)

    >>> x = startai.array([[0., 1.], [2., 3.], [4., 5.]])
    >>> y = startai.array([[0],[1],[1]], dtype='int32')
    >>> z = startai.gather_nd(x,y,batch_dims=1)
    startai.array([0., 3., 5.])

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),b=startai.array([4., 5., 6.]))
    >>> y = startai.array([1])
    >>> print(startai.gather_nd(x, y))
    {
        a: startai.array(1.),
        b: startai.array(5.)
    }

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[0., 10., 20.],[30.,40.,50.]]),
    ...                   b=startai.array([[0., 100., 200.],[300.,400.,500.]]))
    >>> y = startai.Container(a=startai.array([1,0]),
    ...                   b=startai.array([0]))
    >>> print(startai.gather_nd(x, y))
    {
        a: startai.array(30.),
        b: startai.array([0., 100., 200.])
    }
    """
    res = current_backend(params, indices).gather_nd(
        params, indices, batch_dims=batch_dims
    )
    if startai.exists(out):
        return startai.inplace_update(out, res)
    return res


@handle_exceptions
@handle_nestable
@handle_array_function
def multiprocessing(context: Optional[str] = None):
    """Return backend-specific multiprocessing module.

    Parameters
    ----------
    context
        The context of the multiprocessing, either 'fork', 'forkserver' or 'spawn'.
        Default is ``None``.

    Returns
    -------
    ret
        Multiprocessing module

    Examples
    --------
    >>> import startai

    Using the default context (None):

    >>> mp_default = startai.multiprocessing()
    >>> print(mp_default)
    <multiprocessing.context.DefaultContext object at 0x7f4e3193e520>

    Specifying 'fork' as the context:

    >>> mp_fork = startai.multiprocessing(context='fork')
    >>> print(mp_fork)
    <multiprocessing.context.ForkContext object at 0x7f4e3193e580>

    Specifying 'spawn' as the context:

    >>> mp_spawn = startai.multiprocessing(context='spawn')
    >>> print(mp_spawn)
    <multiprocessing.context.SpawnContext object at 0x7f4e3193e5e0>

    Specifying 'forkserver' as the context:

    >>> mp_forkserver = startai.multiprocessing(context='forkserver')
    >>> print(mp_forkserver)
    <multiprocessing.context.ForkServerContext object at 0x7f4e3193e640>
    """
    return current_backend().multiprocessing(context)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_native_arrays
@outputs_to_startai_shapes
@outputs_to_startai_arrays
@handle_array_function
@handle_device
def shape(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    as_array: bool = False,
) -> Union[startai.Shape, startai.NativeShape]:
    """Return the shape of the array ``x``.

    Parameters
    ----------
    x
        Input array to infer the shape of.
    as_array
        Whether to return the shape as an array.
        Default is False.

    Returns
    -------
    ret
        Shape of the array ``x``.

    Examples
    --------
    >>> x = startai.array([[-1, 0, 1], [1, 0, -1]])
    >>> y = startai.shape(x)
    >>> z = startai.shape(x, as_array = True)
    >>> print(y)
    (2, 3)

    >>> print(z)
    startai.array([2, 3])
    """
    return current_backend(x).shape(x, as_array=as_array)


startai.shape_array_mode = shape_array_mode_stack[-1] if shape_array_mode_stack else False


@handle_exceptions
def set_shape_array_mode(mode: bool) -> None:
    """Set the mode of returning shape as startai.Array to the given mode instance.

    Parameter
    ---------
    mode
        boolean whether to return shape as startai.Array

    Examples
    --------
    >>> startai.set_shape_array_mode(False)
    >>> startai.shape_array_mode
    False

    >>> startai.set_shape_array_mode(True)
    >>> startai.shape_array_mode
    True
    """
    global shape_array_mode_stack
    startai.utils.assertions.check_isinstance(mode, bool)
    shape_array_mode_stack.append(mode)
    startai.__setattr__("shape_array_mode", mode, True)


@handle_exceptions
def unset_shape_array_mode() -> None:
    """Reset the mode of returning shape as startai.Array to the previous state.

    Examples
    --------
    >>> startai.set_shape_array_mode(True)
    >>> startai.shape_array_mode
    True

    >>> startai.unset_shape_array_mode()
    >>> startai.shape_array_mode
    False
    """
    global shape_array_mode_stack
    if shape_array_mode_stack:
        shape_array_mode_stack.pop(-1)
        mode = shape_array_mode_stack[-1] if shape_array_mode_stack else False
        startai.__setattr__("shape_array_mode", mode, True)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@to_native_arrays_and_back
@handle_array_function
@handle_device
def get_num_dims(
    x: Union[startai.Array, startai.NativeArray], /, *, as_array: bool = False
) -> int:
    """Return the number of dimensions of the array x.

    Parameters
    ----------
    x
        Input array to infer the number of dimensions for.
    as_array
        Whether to return the shape as a array, default False.

    Returns
    -------
    ret
        Shape of the array

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> a = startai.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ...                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ...                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]])
    >>> b = startai.get_num_dims(a, as_array=False)
    >>> print(b)
    3

    With :class:`startai.Container` input:

    >>> a = startai.Container(b = startai.asarray([[0.,1.,1.],[1.,0.,0.],[8.,2.,3.]]))
    >>> print(startai.get_num_dims(a))
    {
        b: 2
    }

    >>> b = startai.get_num_dims(a, as_array=True)
    >>> print(b)
    {
        b: startai.array(2)
    }
    """
    return current_backend(x).get_num_dims(x, as_array=as_array)


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@to_native_arrays_and_back
@handle_array_function
@handle_device
def size(x: Union[startai.Array, startai.NativeArray]) -> int:
    """Return the number of elements of the array x.

    Parameters
    ----------
    x
        Input array to infer the number of elements for.

    Returns
    -------
    ret
        Number of elements of the array

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> a = startai.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ...                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ...                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]])
    >>> b = startai.size(a)
    >>> print(b)
    27

    With :class:`startai.Container` input:

    >>> a = startai.Container(b = startai.asarray([[0.,1.,1.],[1.,0.,0.],[8.,2.,3.]]))
    >>> print(startai.size(a))
    {
        b: 9
    }
    """
    return current_backend(x).size(x)


@handle_exceptions
def arg_info(fn: Callable, *, name: Optional[str] = None, idx: Optional[int] = None):
    """Return the index and `inspect.Parameter` representation of the specified
    argument. In the form of a dict with keys "idx" and "param".

    Parameters
    ----------
    fn
        The function to retrieve the argument information for
    name
        The name of the argument
    idx
        the index of the argument in the inputs

    Returns
    -------
    ret
        a `dict` containing the idx, and the `inspect.Parameter` for the argument,
        which itself contains the parameter name, type, and other helpful information.
    """
    startai.utils.assertions.check_all_or_any_fn(
        name,
        idx,
        fn=startai.exists,
        type="any",
        limit=[1],
        message="exactly one of the keyword arguments name or idx must be provided",
        as_array=False,
    )
    params = inspect.signature(fn).parameters
    if startai.exists(name):
        return {"idx": list(params).index(name), "param": params[name]}
    return {"idx": idx, "param": list(params.values())[idx]}


def _valid_attrib_combinations(fn, backend, dnd_dict, first_attr_name, other_attr_name):
    attr_list = ()
    if hasattr(fn, other_attr_name):
        attr_list = getattr(fn, other_attr_name)
        if isinstance(attr_list, dict):
            attr_list = attr_list.get(backend, ())
    startai.utils.assertions.check_false(
        dnd_dict and attr_list,
        f"Cannot specify both {first_attr_name} and {other_attr_name} "
        "cannot both be defined for the same function",
    )


def _is_valid_device_and_dtypes_attributes(fn: Callable) -> bool:
    fn_unsupported_dnd = {}
    fn_supported_dnd = {}
    backend = startai.current_backend_str()
    if hasattr(fn, "unsupported_device_and_dtype"):
        fn_unsupported_dnd = fn.unsupported_device_and_dtype
        # if it's a nested dict, unwrap for the current backend
        if fn_unsupported_dnd and isinstance(
            list(fn_unsupported_dnd.__get__().values())[0], dict
        ):
            fn_unsupported_dnd = fn_unsupported_dnd.get(backend, {})
    if hasattr(fn, "supported_device_and_dtype"):
        fn_supported_dnd = fn.supported_device_and_dtype
        # if it's a nested dict, unwrap for the current backend
        if fn_supported_dnd and isinstance(
            list(fn_supported_dnd.__get__().values())[0], dict
        ):
            fn_supported_dnd = fn_supported_dnd.get(backend, {})

    startai.utils.assertions.check_false(
        fn_unsupported_dnd and fn_supported_dnd,
        "unsupported_device_and_dtype and supported_device_and_dtype cannot"
        " both be defined for the same function",
    )

    us = "unsupported_device_and_dtype"
    _valid_attrib_combinations(fn, backend, fn_unsupported_dnd, us, "supported_devices")
    _valid_attrib_combinations(fn, backend, fn_unsupported_dnd, us, "supported_dtypes")

    ss = "supported_device_and_dtype"
    _valid_attrib_combinations(fn, backend, fn_supported_dnd, ss, "unsupported_device")
    _valid_attrib_combinations(fn, backend, fn_supported_dnd, ss, "unsupported_dtypes")

    return True


def _all_dnd_combinations():
    all_comb = {}
    for device in startai.all_devices:
        all_comb[device] = startai.all_dtypes
    return all_comb


def _dnd_dict_intersection(a, b):
    res = {}
    for device in a:
        if device in b:
            intersection = set.intersection(set(a[device]), set(b[device]))
            if intersection:
                res[device] = tuple(intersection)
    return res


def _dnd_dict_difference(a, b):
    res = a
    for device in list(a):
        if device in b:
            difference = set.difference(set(a[device]), set(b[device]))
            if difference:
                res[device] = tuple(difference)
            else:
                del res[device]
    return res


def _dnd_dict_union(a, b):
    res = {}
    for device in set(list(a) + list(b)):
        u1 = set(a.get(device, ()))
        u2 = set(b.get(device, ()))
        res[device] = tuple(set.union(u1, u2))

    return res


# allow passing "integer" if all integer dtypes are supported/unsupported for e.g.
def _expand_typesets(dtypes):
    typesets = {
        "valid": startai.valid_dtypes,
        "numeric": startai.valid_numeric_dtypes,
        "float": startai.valid_float_dtypes,
        "integer": startai.valid_int_dtypes,
        "unsigned": startai.valid_uint_dtypes,
        "complex": startai.valid_complex_dtypes,
    }
    dtypes = list(dtypes)
    typeset_list = []
    for i, dtype in reversed(list(enumerate(dtypes))):
        if dtype in typesets:
            typeset_list.extend(typesets[dtype])
            dtypes.pop(i)
    dtypes += typeset_list
    return dtypes


def _get_devices_and_dtypes(fn, recurse=True, complement=True):
    supported_devices = startai.function_supported_devices(fn, recurse=recurse)
    supported_dtypes = startai.function_supported_dtypes(fn, recurse=recurse)

    if hasattr(fn, "partial_mixed_handler"):
        supported_devices = supported_devices["primary"]
        supported_dtypes = supported_dtypes["primary"]

    supported = {}
    # Generate a base supported set from other attributes
    for device in supported_devices:
        supported[device] = supported_dtypes

    is_frontend_fn = "frontend" in fn.__module__
    is_backend_fn = "backend" in fn.__module__ and not is_frontend_fn
    is_einops_fn = hasattr(fn, "__name__") and "einops" in fn.__name__
    if not is_backend_fn and not is_frontend_fn and not is_einops_fn:
        if complement:
            all_comb = _all_dnd_combinations()
            supported = _dnd_dict_difference(all_comb, supported)
        return supported

    backend = startai.current_backend_str()

    # Their values are formatted like either
    # 1. fn.supported_device_and_dtype = {"cpu":("float16",)}
    if hasattr(fn, "supported_device_and_dtype"):
        fn_supported_dnd = fn.supported_device_and_dtype.__get__()

        if is_einops_fn and isinstance(fn_supported_dnd, dict):
            fn_supported_dnd = fn_supported_dnd.get(backend, supported)

        if fn_supported_dnd:
            startai.utils.assertions.check_isinstance(
                list(fn_supported_dnd.values())[0], tuple
            )

        if isinstance(fn_supported_dnd, dict):
            for device, dtypes in fn_supported_dnd.items():
                fn_supported_dnd[device] = tuple(_expand_typesets(dtypes))

        # dict intersection
        supported = _dnd_dict_intersection(supported, fn_supported_dnd)

    if hasattr(fn, "unsupported_device_and_dtype"):
        fn_unsupported_dnd = fn.unsupported_device_and_dtype.__get__()

        if is_einops_fn and isinstance(fn_unsupported_dnd, dict):
            fn_unsupported_dnd = fn_unsupported_dnd.get(backend, supported)

        if fn_unsupported_dnd:
            startai.utils.assertions.check_isinstance(
                list(fn_unsupported_dnd.values())[0], tuple
            )

        if isinstance(fn_unsupported_dnd, dict):
            for device, dtypes in fn_unsupported_dnd.items():
                fn_unsupported_dnd[device] = tuple(_expand_typesets(dtypes))

        # dict difference
        supported = _dnd_dict_difference(supported, fn_unsupported_dnd)

    if complement:
        # dict difference
        all_comb = _all_dnd_combinations()
        supported = _dnd_dict_difference(all_comb, supported)
    return supported


@handle_exceptions
@handle_nestable
def function_supported_devices_and_dtypes(fn: Callable, recurse: bool = True) -> Dict:
    """Return the supported combination of devices and dtypes of the current
    backend's function. The function returns a dict containing the supported
    combination of devices and dtypes of the primary and compositional
    implementations in case of partial mixed functions.

    Parameters
    ----------
    fn
        The function to check for the supported device and dtype attribute
    recurse
        Whether to recurse into used startai functions.
        Default is ``True``.

    Returns
    -------
    ret
        Tuple or dict containing the supported devices and dtypes of the function
    """
    startai.utils.assertions.check_true(
        _is_valid_device_and_dtypes_attributes(fn),
        "supported_device_and_dtypes and unsupported_device_and_dtypes "
        "attributes cannot both exist in a particular backend",
    )

    if hasattr(fn, "partial_mixed_handler"):
        return {
            "compositional": function_supported_devices_and_dtypes(
                fn.compos, recurse=recurse
            ),
            "primary": _get_devices_and_dtypes(fn, complement=False),
        }
    else:
        supported_devices_dtypes = _get_devices_and_dtypes(fn, complement=False)
        if recurse:
            supported_devices_dtypes = startai.functional.data_type._nested_get(
                fn,
                supported_devices_dtypes,
                _dnd_dict_intersection,
                function_supported_devices_and_dtypes,
                wrapper=lambda x: x,
            )

    return supported_devices_dtypes


@handle_exceptions
@handle_nestable
def function_unsupported_devices_and_dtypes(fn: Callable, recurse: bool = True) -> Dict:
    """Return the unsupported combination of devices and dtypes of the current
    backend's function. The function returns a dict containing the unsupported
    combination of devices and dtypes of the primary and compositional
    implementations in case of partial mixed functions.

    Parameters
    ----------
    fn
        The function to check for the unsupported device and dtype attribute
    recurse
        Whether to recurse into used startai functions.
        Default is ``True``.

    Returns
    -------
    ret
        Tuple or dict containing the unsupported devices and dtypes of the function
    """
    startai.utils.assertions.check_true(
        _is_valid_device_and_dtypes_attributes(fn),
        "supported_device_and_dtypes and unsupported_device_and_dtypes "
        "attributes cannot both exist in a particular backend",
    )
    if hasattr(fn, "partial_mixed_handler"):
        return {
            "compositional": function_unsupported_devices_and_dtypes(
                fn.compos, recurse=recurse
            ),
            "primary": _get_devices_and_dtypes(fn, complement=True),
        }
    else:
        unsupported_devices_dtypes = _get_devices_and_dtypes(fn, complement=True)
        if recurse:
            unsupported_devices_dtypes = startai.functional.data_type._nested_get(
                fn,
                unsupported_devices_dtypes,
                _dnd_dict_union,
                function_unsupported_devices_and_dtypes,
                wrapper=lambda x: x,
            )
    return unsupported_devices_dtypes


@handle_exceptions
def vmap(
    func: Callable,
    in_axes: Union[int, Sequence[int], Sequence[None]] = 0,
    out_axes: int = 0,
) -> Callable:
    """Vectorizing map. Creates a function which maps func over argument axes.

    Parameters
    ----------
    func
        Function to be mapped over additional axes.
    in_axes
       An integer, None, or (nested) standard Python container
       (tuple/list) thereof specifying which input array
       axes to map over.If each positional argument to fun
       is an array, then in_axes can be an integer, a None,
       or a tuple of integers and Nones with length equal
       to the number of positional arguments to fun. An
       integer or None indicates which array axis to map
       over for all arguments (with None indicating not to map any axis),
       and a tuple indicates which axis to map for each
       corresponding positional argument. Axis integers must
       be in the range [-ndim, ndim) for each array,
       where ndim is the number of dimensions (axes) of the
       corresponding input array.
    out_axes
        An integer indicating where the mapped axis should appear in the output.

    Returns
    -------
    ret
        Batched/vectorized version of func with arguments
        that correspond to those of func, but with extra
        array axes at positions indicated by in_axes,
        and a return value that corresponds
        to that of fun, but with extra array axes
        at positions indicated by out_axes.


    This docstring is a summarised version of the `docstring
    <https://jax.readthedocs.io/en/latest/_autosummary/jax.vmap.html#jax-vmap>`_
    for vmap from JAX documentation.

    Examples
    --------
    With :func:`startai.matmul` and :class:`startai.Array` input:

    >>> x = startai.array(startai.arange(60).reshape((3, 5, 4)))
    >>> y = startai.array(startai.arange(40).reshape((5, 4, 2)))
    >>> z = startai.vmap(startai.matmul, (1, 0), 1)(x, y)
    >>> z.shape
    (3, 5, 2)
    """
    # TODO: optimize in the numpy and tensorflow backends and extend functionality
    return current_backend().vmap(func, in_axes, out_axes)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@to_native_arrays_and_back
@handle_device
def isin(
    elements: Union[startai.Array, startai.NativeArray],
    test_elements: Union[startai.Array, startai.NativeArray],
    /,
    *,
    assume_unique: bool = False,
    invert: bool = False,
) -> startai.Array:
    """Test if each element of elements is in test_elements.

    Parameters
    ----------
    elements
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
        output a boolean array of the same shape as elements that is True for elements
        in test_elements and False otherwise.

    Examples
    --------
    >>> x = startai.array([[10, 7, 4], [3, 2, 1]])
    >>> y = startai.array([1, 2, 3])
    >>> startai.isin(x, y)
    startai.array([[False, False, False], [ True,  True,  True]])

    >>> x = startai.array([3, 2, 1, 0])
    >>> y = startai.array([1, 2, 3])
    >>> startai.isin(x, y, invert=True)
    startai.array([False, False, False,  True])
    """
    return startai.current_backend(elements, test_elements).isin(
        elements, test_elements, assume_unique=assume_unique, invert=invert
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@inputs_to_native_arrays
@handle_device
def itemsize(
    x: Union[startai.Array, startai.NativeArray],
    /,
) -> int:
    """Return the size of the input array's elements.

    Parameters
    ----------
    x
       The input array.

    Returns
    -------
    ret
        An integer specifying the element size in bytes.

    Examples
    --------
    >>> x = startai.array([1,2,3], dtype=startai.float64)
    >>> startai.itemsize(x)
    8

    >>> x = startai.array([1,2,3], dtype=startai.complex128)
    >>> startai.itemsize(x)
    16
    """
    return startai.current_backend(x).itemsize(x)


@handle_exceptions
@handle_nestable
@handle_device
def strides(
    x: Union[startai.Array, startai.NativeArray],
    /,
) -> Tuple[int]:
    """Return the input array's strides across each dimension.

    Parameters
    ----------
    x
       The input array.

    Returns
    -------
    ret
        A tuple containing the strides.

    Examples
    --------
    >>> x = startai.array([[1, 5, 9], [2, 6, 10]])
    >>> startai.strides(x)
    (4, 8)
    """
    if startai.is_native_array(x) or (startai.is_startai_array(x) and x.base is None):
        return startai.to_numpy(x).strides
    # if x is an startai array with a base,
    # convert it to a numpy array with the same base:
    ret = startai.to_numpy(x.base)
    startai_numpy = startai.with_backend("numpy")
    for fn, args, kwargs, index in x._manipulation_stack:
        ret = startai_numpy.__dict__[fn](ret, *args, **kwargs)
        ret = ret[index] if startai.exists(index) else ret
    return ret.to_native().strides


def is_startai_nested_array(x: Any, /) -> bool:
    """Determine whether the input x is an Startai Nested Array.

    Parameters
    ----------
    x
        The input to check

    Returns
    -------
    ret
        Boolean, whether or not x is an startai nested array.
    """
    return isinstance(x, startai.NestedArray)
