from typing import Callable
import functools


import startai
import startai.functional.frontends.paddle as paddle_frontend


# --- Helpers --- #
# --------------- #


def _from_startai_array_to_paddle_frontend_tensor(x, nested=False, include_derived=None):
    if nested:
        return startai.nested_map(
            _from_startai_array_to_paddle_frontend_tensor, x, include_derived, shallow=False
        )
    elif isinstance(x, startai.Array) or startai.is_native_array(x):
        a = paddle_frontend.Tensor(x)
        return a
    return x


def _to_startai_array(x):
    # if x is a native array return it as an startai array
    if isinstance(x, startai.NativeArray):
        return startai.array(x)

    # else if x is a frontend torch Tensor (or any frontend "Tensor" actually) return the wrapped startai array # noqa: E501
    elif hasattr(x, "startai_array"):
        return x.startai_array

    # else just return x
    return x


# --- Main --- #
# ------------ #


def inputs_to_startai_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        """Convert `Tensor` into `startai.Array` instances.

        Convert all `Tensor` instances in both the positional and keyword arguments
        into `startai.Array` instances, and then call the function with the updated
        arguments.
        """
        # convert all input arrays to startai.Array instances
        new_args = startai.nested_map(
            _to_startai_array, args, include_derived={"tuple": True}, shallow=False
        )
        new_kwargs = startai.nested_map(
            _to_startai_array, kwargs, include_derived={"tuple": True}, shallow=False
        )

        return fn(*new_args, **new_kwargs)

    return new_fn


def outputs_to_frontend_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        """Convert `startai.Array` into `Tensor` instances.

        Call the function, and then convert all `startai.Array` instances returned by the
        function into `Tensor` instances.
        """
        # call unmodified function
        # ToDo: Remove this default dtype setting
        #  once frontend specific backend setting is added
        # startai.set_default_int_dtype("int64")
        # startai.set_default_float_dtype(paddle_frontend.get_default_dtype())
        try:
            ret = fn(*args, **kwargs)
        finally:
            startai.unset_default_int_dtype()
            startai.unset_default_float_dtype()
        # convert all arrays in the return to `paddle_frontend.Tensor` instances
        return _from_startai_array_to_paddle_frontend_tensor(
            ret, nested=True, include_derived={"tuple": True}
        )

    return new_fn


def to_startai_arrays_and_back(fn: Callable) -> Callable:
    """Wrap `fn` so it receives and returns `startai.Array` instances.

    Wrap `fn` so that input arrays are all converted to `startai.Array` instances and
    return arrays are all converted to `Tensor` instances.
    """
    return outputs_to_frontend_arrays(inputs_to_startai_arrays(fn))
