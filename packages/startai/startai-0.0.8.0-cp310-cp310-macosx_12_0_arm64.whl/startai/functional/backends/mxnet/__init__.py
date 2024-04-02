import sys
import numpy as np
import mxnet as mx
import startai
from startai.func_wrapper import _dtype_from_version
from startai.utils.exceptions import StartaiNotImplementedException

backend_version = {"version": mx.__version__}
if not startai.is_local():
    _module_in_memory = sys.modules[__name__]
else:
    _module_in_memory = sys.modules[startai.import_module_path].import_cache[__name__]
use = startai.utils.backend.ContextManager(_module_in_memory)


# wrap dunder methods of native tensors to return NotImplemented to prioritize Startai array methods.
def dunder_wrapper(func):
    def rep_method(*args, **kwargs):
        for arg in args:
            if startai.is_startai_array(arg):
                return NotImplemented
        return func(*args, **kwargs)

    return rep_method


# check for previously imported mxnet modules
modules_to_patch = []
tensors_to_patch = []
tmp_globals = dict(globals())
for name, value in tmp_globals.items():
    if value == "mxnet.ndarray.ndarray.NDArray":
        tensors_to_patch.append(name)
    try:
        if value.__name__ == "mxnet":
            modules_to_patch.append(name)
    except AttributeError:
        pass

methods_to_patch = [
    "__add__",
    "__sub__",
    "__mul__",
    "__div__",
    "__truediv__",
    "__mod__",
    "__lt__",
    "__le__",
    "__gt__",
    "__ge__",
    "__ne__",
    "__eq__",
    "__pow__",
]

for module in modules_to_patch:
    for method in methods_to_patch:
        exec(
            module
            + ".ndarray.NDArray."
            + method
            + " = dunder_wrapper("
            + module
            + ".ndarray.NDArray."
            + method
            + ")"
        )

for tensor in tensors_to_patch:
    for method in methods_to_patch:
        exec(tensor + "." + method + " = dunder_wrapper(" + tensor + "." + method + ")")


NativeArray = mx.ndarray.NDArray
NativeDevice = str
NativeDtype = np.dtype
NativeShape = tuple
NativeSparseArray = mx.ndarray.sparse.BaseSparseNDArray


valid_devices = ("cpu", "gpu")
invalid_devices = ("tpu",)

# native data types
native_int8 = np.dtype("int8")
native_int32 = np.dtype("int32")
native_int64 = np.dtype("int64")
native_uint8 = np.dtype("uint8")
native_float16 = np.dtype("float16")
native_float32 = np.dtype("float32")
native_float64 = np.dtype("float64")
native_double = native_float64
native_bool = np.dtype("bool")


# update these to add new dtypes
valid_dtypes = {
    "1.9.1 and below": (
        startai.int8,
        startai.int32,
        startai.int64,
        startai.uint8,
        startai.bfloat16,
        startai.float16,
        startai.float32,
        startai.float64,
        startai.bool,
    )
}
valid_numeric_dtypes = {
    "1.9.1 and below": (
        startai.int8,
        startai.int32,
        startai.int64,
        startai.uint8,
        startai.float16,
        startai.float32,
        startai.float64,
    )
}
valid_int_dtypes = {"1.9.1 and below": (startai.int8, startai.int32, startai.int64, startai.uint8)}
valid_float_dtypes = {"1.9.1 and below": (startai.float16, startai.float32, startai.float64)}
valid_uint_dtypes = {"1.9.1 and below": (startai.uint8,)}
valid_complex_dtypes = {"1.9.1 and below": ()}

# leave these untouched
valid_dtypes = _dtype_from_version(valid_dtypes, backend_version)
valid_numeric_dtypes = _dtype_from_version(valid_numeric_dtypes, backend_version)
valid_int_dtypes = _dtype_from_version(valid_int_dtypes, backend_version)
valid_float_dtypes = _dtype_from_version(valid_float_dtypes, backend_version)
valid_uint_dtypes = _dtype_from_version(valid_uint_dtypes, backend_version)
valid_complex_dtypes = _dtype_from_version(valid_complex_dtypes, backend_version)


# update these to add new dtypes
invalid_dtypes = {"1.9.1 and below": (startai.int16, startai.uint32, startai.uint64, startai.uint16)}
invalid_numeric_dtypes = {
    "1.9.1 and below": (startai.int16, startai.uint32, startai.uint64, startai.uint16)
}
invalid_int_dtypes = {
    "1.9.1 and below": (startai.int16, startai.uint16, startai.uint32, startai.uint64)
}
invalid_float_dtypes = {"1.9.1 and below": (startai.bfloat16,)}
invalid_uint_dtypes = {"1.9.1 and below": (startai.uint16, startai.uint32, startai.uint64)}
invalid_complex_dtypes = {"1.9.1 and below": (startai.complex64, startai.complex128)}


# leave these untouched
invalid_dtypes = _dtype_from_version(invalid_dtypes, backend_version)
invalid_numeric_dtypes = _dtype_from_version(invalid_numeric_dtypes, backend_version)
invalid_int_dtypes = _dtype_from_version(invalid_int_dtypes, backend_version)
invalid_float_dtypes = _dtype_from_version(invalid_float_dtypes, backend_version)
invalid_uint_dtypes = _dtype_from_version(invalid_uint_dtypes, backend_version)
invalid_complex_dtypes = _dtype_from_version(invalid_complex_dtypes, backend_version)


native_inplace_support = True
supports_gradients = True


def closest_valid_dtype(type=None, /, as_native=False):
    raise StartaiNotImplementedException()


backend = "mxnet"
from . import activations
from .activations import *
from . import creation
from .creation import *
from . import data_type
from .data_type import *
from . import device
from .device import *
from . import elementwise
from .elementwise import *
from . import general
from .general import *
from . import gradients
from .gradients import *
from . import layers
from .layers import *
from . import linear_algebra as linalg
from .linear_algebra import *
from . import manipulation
from .manipulation import *
from . import random
from .random import *
from . import searching
from .searching import *
from . import set
from .set import *
from . import sorting
from .sorting import *
from . import statistical
from .statistical import *
from . import utility
from .utility import *
from . import experimental
from .experimental import *
from . import control_flow_ops
from .control_flow_ops import *
from . import sub_backends
from .sub_backends import *
from . import module
from .module import *


NativeModule = mx.gluon.nn.Block
