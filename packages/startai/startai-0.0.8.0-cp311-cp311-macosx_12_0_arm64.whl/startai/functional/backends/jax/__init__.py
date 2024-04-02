# global
import sys
from packaging import version
import jaxlib
import jax
import jax.numpy as jnp
import importlib
from typing import Union

# make startai.Container compatible with jax pytree traversal
from jax.tree_util import register_pytree_node
from jax.tree_util import tree_flatten, tree_unflatten

# local
import startai
from startai.func_wrapper import _dtype_from_version

backend_version = {"version": jax.__version__}

try:
    register_pytree_node(
        startai.Container,
        lambda c: tree_flatten(c.cont_to_dict()),
        lambda a, c: startai.Container(tree_unflatten(a, c)),
    )
except Exception as e:
    if "Duplicate custom PyTreeDef type registration" not in str(e):
        raise


# make startai.Array compatible with jax pytree traversal
def _array_flatten(tree):
    return ((tree.data,), None)


def _array_unflatten(aux_data, children):
    if type(*children) == object:
        return children
    return startai.Array(*children)


try:
    register_pytree_node(startai.Array, _array_flatten, _array_unflatten)
except Exception as e:
    if "Duplicate custom PyTreeDef type registration" not in str(e):
        raise


# noinspection PyUnresolvedReferences
if not startai.is_local():
    _module_in_memory = sys.modules[__name__]
else:
    _module_in_memory = sys.modules[startai.import_module_path].import_cache[__name__]

use = startai.utils.backend.ContextManager(_module_in_memory)

if version.parse(jax.__version__) >= version.parse("0.4.1"):
    JaxArray = jax.Array
    NativeArray = jax.Array
else:
    JaxArray = jaxlib.xla_extension.DeviceArray
    NativeArray = jaxlib.xla_extension.DeviceArray

# noinspection PyUnresolvedReferences,PyProtectedMember
NativeDevice = jaxlib.xla_extension.Device
NativeDtype = jnp.dtype
NativeShape = tuple

NativeSparseArray = None


# devices
valid_devices = ("cpu", "gpu")

invalid_devices = ("tpu",)


# native data types
native_int8 = jnp.dtype("int8")
native_int16 = jnp.dtype("int16")
native_int32 = jnp.dtype("int32")
native_int64 = jnp.dtype("int64")
native_uint8 = jnp.dtype("uint8")
native_uint16 = jnp.dtype("uint16")
native_uint32 = jnp.dtype("uint32")
native_uint64 = jnp.dtype("uint64")
native_bfloat16 = jnp.dtype("bfloat16")
native_float16 = jnp.dtype("float16")
native_float32 = jnp.dtype("float32")
native_float64 = jnp.dtype("float64")
native_complex64 = jnp.dtype("complex64")
native_complex128 = jnp.dtype("complex128")
native_double = native_float64
native_bool = jnp.dtype("bool")

# valid data types
# ToDo: Add complex dtypes to valid_dtypes and fix all resulting failures.

# update these to add new dtypes
valid_dtypes = {
    "0.4.25 and below": (
        startai.int8,
        startai.int16,
        startai.int32,
        startai.int64,
        startai.uint8,
        startai.uint16,
        startai.uint32,
        startai.uint64,
        startai.bfloat16,
        startai.float16,
        startai.float32,
        startai.float64,
        startai.complex64,
        startai.complex128,
        startai.bool,
    )
}
valid_numeric_dtypes = {
    "0.4.25 and below": (
        startai.int8,
        startai.int16,
        startai.int32,
        startai.int64,
        startai.uint8,
        startai.uint16,
        startai.uint32,
        startai.uint64,
        startai.bfloat16,
        startai.float16,
        startai.float32,
        startai.float64,
        startai.complex64,
        startai.complex128,
    )
}

valid_int_dtypes = {
    "0.4.25 and below": (
        startai.int8,
        startai.int16,
        startai.int32,
        startai.int64,
        startai.uint8,
        startai.uint16,
        startai.uint32,
        startai.uint64,
    )
}

valid_uint_dtypes = {
    "0.4.25 and below": (startai.uint8, startai.uint16, startai.uint32, startai.uint64)
}
valid_float_dtypes = {
    "0.4.25 and below": (startai.bfloat16, startai.float16, startai.float32, startai.float64)
}
valid_complex_dtypes = {"0.4.25 and below": (startai.complex64, startai.complex128)}


# leave these untouched
valid_dtypes = _dtype_from_version(valid_dtypes, backend_version)
valid_numeric_dtypes = _dtype_from_version(valid_numeric_dtypes, backend_version)
valid_int_dtypes = _dtype_from_version(valid_int_dtypes, backend_version)
valid_float_dtypes = _dtype_from_version(valid_float_dtypes, backend_version)
valid_uint_dtypes = _dtype_from_version(valid_uint_dtypes, backend_version)
valid_complex_dtypes = _dtype_from_version(valid_complex_dtypes, backend_version)


# invalid data types

# update these to add new dtypes
invalid_dtypes = {"0.4.25 and below": ()}
invalid_numeric_dtypes = {"0.4.25 and below": ()}
invalid_int_dtypes = {"0.4.25 and below": ()}
invalid_float_dtypes = {"0.4.25 and below": ()}
invalid_uint_dtypes = {"0.4.25 and below": ()}
invalid_complex_dtypes = {"0.4.25 and below": ()}

# leave these untouched
invalid_dtypes = _dtype_from_version(invalid_dtypes, backend_version)
invalid_numeric_dtypes = _dtype_from_version(invalid_numeric_dtypes, backend_version)
invalid_int_dtypes = _dtype_from_version(invalid_int_dtypes, backend_version)
invalid_float_dtypes = _dtype_from_version(invalid_float_dtypes, backend_version)
invalid_uint_dtypes = _dtype_from_version(invalid_uint_dtypes, backend_version)
invalid_complex_dtypes = _dtype_from_version(invalid_complex_dtypes, backend_version)

native_inplace_support = False

supports_gradients = True


def closest_valid_dtype(type=None, /, as_native=False):
    if type is None:
        type = startai.default_dtype()
    if isinstance(type, str) and type in invalid_dtypes:
        return {"int64": startai.int32, "uint64": startai.uint32, "float64": startai.float32}[type]
    return startai.as_startai_dtype(type) if not as_native else startai.as_native_dtype(type)


backend = "jax"


# local sub-modules
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
from . import module
from .module import *


# sub-backends
from . import sub_backends
from .sub_backends import *


if importlib.util.find_spec("flax"):
    import flax

    NativeModule = flax.linen.Module
elif importlib.util.find_spec("haiku"):
    import haiku as hk

    NativeModule = hk.Module
else:
    NativeModule = None
