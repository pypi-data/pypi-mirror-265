import functools
import inspect
from typing import Callable

import startai
from startai.functional.frontends.mxnet.numpy.ndarray import ndarray


# --- Helpers --- #
# --------------- #


def _startai_array_to_mxnet(x):
    if isinstance(x, startai.Array) or startai.is_native_array(x):
        return ndarray(x)
    return x


def _mxnet_frontend_array_to_startai(x):
    if hasattr(x, "startai_array"):
        return x.startai_array
    return x


def _native_to_startai_array(x):
    if isinstance(x, startai.NativeArray):
        return startai.array(x)
    return x


def _to_startai_array(x):
    return _mxnet_frontend_array_to_startai(_native_to_startai_array(x))


# --- Main --- #
# ------------ #


def handle_mxnet_out(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_mxnet_out(*args, **kwargs):
        if "out" not in kwargs:
            keys = list(inspect.signature(fn).parameters.keys())
            out_pos = keys.index("out")
            kwargs = {
                **dict(
                    zip(
                        keys[keys.index("out") :],
                        args[out_pos:],
                    )
                ),
                **kwargs,
            }
            args = args[:out_pos]
        return fn(*args, **kwargs)

    _handle_mxnet_out.handle_numpy_out = True
    return _handle_mxnet_out


def inputs_to_startai_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _inputs_to_startai_arrays_mxnet(*args, **kwargs):
        """Convert `ndarray.NDArray` into `startai.Array` instances.

        Convert all `ndarray.NDArray` instances in both the positional
        and keyword arguments into `startai.Array` instances, and then calls
        the function with the updated arguments.
        """
        # convert all arrays in the inputs to startai.Array instances
        new_args = startai.nested_map(
            _to_startai_array, args, include_derived={"tuple": True}, shallow=False
        )
        new_kwargs = startai.nested_map(
            _to_startai_array, kwargs, include_derived={"tuple": True}, shallow=False
        )
        return fn(*new_args, **new_kwargs)

    _inputs_to_startai_arrays_mxnet.inputs_to_startai_arrays = True
    return _inputs_to_startai_arrays_mxnet


def outputs_to_frontend_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _outputs_to_frontend_arrays_mxnet(*args, **kwargs):
        """Convert `startai.Array` into `ndarray.NDArray` instances.

        Call the function, and then converts all `startai.Array` instances
        in the function return into `ndarray.NDArray` instances.
        """
        # call unmodified function
        ret = fn(*args, **kwargs)

        # convert all arrays in the return to `frontend.Tensorflow.tensor` instances
        return startai.nested_map(_startai_array_to_mxnet, ret, include_derived={"tuple": True})

    _outputs_to_frontend_arrays_mxnet.outputs_to_frontend_arrays = True
    return _outputs_to_frontend_arrays_mxnet


def to_startai_arrays_and_back(fn: Callable) -> Callable:
    """Wrap `fn` so it receives and returns `startai.Array` instances.

    Wrap `fn` so that input arrays are all converted to `startai.Array`
    instances and return arrays are all converted to `ndarray.NDArray`
    instances.
    """
    return outputs_to_frontend_arrays(inputs_to_startai_arrays(fn))
