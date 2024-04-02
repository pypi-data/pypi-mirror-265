import functools
from typing import Callable

import startai
import startai.functional.frontends.onnx as onnx_frontend


# --- Helpers --- #
# --------------- #


def _from_startai_array_to_onnx_frontend_tensor(x, nested=False, include_derived=None):
    if nested:
        return startai.nested_map(
            _from_startai_array_to_onnx_frontend_tensor, x, include_derived, shallow=False
        )
    elif isinstance(x, startai.Array) or startai.is_native_array(x):
        a = onnx_frontend.Tensor(x)
        return a
    return x


def _startai_array_to_onnx(x):
    if isinstance(x, startai.Array) or startai.is_native_array(x):
        return onnx_frontend.Tensor(x)
    return x


def _native_to_startai_array(x):
    if isinstance(x, startai.NativeArray):
        return startai.array(x)
    return x


def _onnx_frontend_array_to_startai(x):
    if hasattr(x, "startai_array"):
        return x.startai_array
    return x


def _to_startai_array(x):
    return _onnx_frontend_array_to_startai(_native_to_startai_array(x))


# --- Main --- #
# ------------ #


def inputs_to_startai_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _inputs_to_startai_arrays_onnx(*args, **kwargs):
        """Convert `Tensor` into `startai.Array` instances.

        Convert all `Tensor` instances in both the positional and
        keyword arguments into `startai.Array` instances, and then calls the
        function with the updated arguments.
        """
        # convert all arrays in the inputs to startai.Array instances
        new_args = startai.nested_map(
            _to_startai_array, args, include_derived={"tuple": True}, shallow=False
        )
        new_kwargs = startai.nested_map(
            _to_startai_array, kwargs, include_derived={"tuple": True}, shallow=False
        )
        return fn(*new_args, **new_kwargs)

    return _inputs_to_startai_arrays_onnx


def outputs_to_frontend_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _outputs_to_frontend_arrays_onnx(*args, **kwargs):
        """Convert `startai.Array` into `Tensor` instances.

        Call the function, and then converts all `startai.Array` instances
        returned by the function into `Tensor` instances.
        """
        # call unmodified function
        ret = fn(*args, **kwargs)

        # convert all arrays in the return to `frontend.onnx.Tensor` instances
        return _from_startai_array_to_onnx_frontend_tensor(
            ret, nested=True, include_derived={"tuple": True}
        )

    return _outputs_to_frontend_arrays_onnx


def to_startai_arrays_and_back(fn: Callable) -> Callable:
    """Wrap `fn` so it receives and returns `startai.Array` instances.

    Wrap `fn` so that input arrays are all converted to `startai.Array`
    instances and return arrays are all converted to `ndarray.NDArray`
    instances.
    """
    return outputs_to_frontend_arrays(inputs_to_startai_arrays(fn))
