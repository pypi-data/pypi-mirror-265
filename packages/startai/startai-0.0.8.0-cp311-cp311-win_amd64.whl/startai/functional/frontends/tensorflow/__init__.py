# global
import sys

# local
import startai
from startai.utils.exceptions import handle_exceptions
from startai.functional.frontends import set_frontend_to_specific_version
from numbers import Number
from typing import Union, Tuple, Iterable
from .dtypes import DType


# Constructing dtypes are required as startai.<dtype>
# will change dynamically on the backend and may not be available
tensorflow_enum_to_type = {
    1: startai.FloatDtype("float32"),
    2: startai.FloatDtype("float64"),
    3: startai.IntDtype("int32"),
    4: startai.UintDtype("uint8"),
    5: startai.IntDtype("int16"),
    6: startai.IntDtype("int8"),
    8: startai.ComplexDtype("complex64"),
    9: startai.IntDtype("int64"),
    10: startai.Dtype("bool"),
    14: startai.FloatDtype("bfloat16"),
    17: startai.UintDtype("uint16"),
    18: startai.ComplexDtype("complex128"),
    19: startai.FloatDtype("float16"),
    22: startai.UintDtype("uint32"),
    23: startai.UintDtype("uint64"),
}

tensorflow_type_to_enum = {v: k for k, v in tensorflow_enum_to_type.items()}

float32 = DType(1)
float64 = DType(2)
int32 = DType(3)
uint8 = DType(4)
int16 = DType(5)
int8 = DType(6)
int64 = DType(9)
bool = DType(10)
bfloat16 = DType(14)
uint16 = DType(17)
float16 = DType(19)
uint32 = DType(22)
uint64 = DType(23)

# type aliases
double = float64
half = float16


@handle_exceptions
def check_tensorflow_casting(x1, x2):
    """Check whether the two arguments provided in the function have the same
    dtype, unless one of them is an array_like or scalar, where it gets casted
    to the other input's dtype.

    Parameters
    ----------
    x1
        First argument which can be tensor, array_like or scalar
    x2
        Second argument which can be tensor, array_like or scalar

    Returns
    -------
    x1
        First tensor promoted accordingly.
    x2
        Second tensor promoted accordingly.
    """
    if hasattr(x1, "dtype") and not hasattr(x2, "dtype"):
        x1 = startai.asarray(x1)
        x2 = startai.asarray(x2, dtype=x1.dtype)
    elif hasattr(x2, "dtype") and not hasattr(x1, "dtype"):
        x2 = startai.asarray(x2)
        x1 = startai.asarray(x1, dtype=x2.dtype)
    else:
        x1 = startai.asarray(x1)
        if not hasattr(x2, "dtype"):
            x2 = startai.asarray(x2, dtype=x1.dtype)
        startai.utils.assertions.check_same_dtype(x1, x2)
    return x1, x2


from . import dtypes
from .dtypes import as_dtype, cast
from . import ragged
from .ragged import *
from . import tensor
from .tensor import EagerTensor, Tensor
from .tensorarray import TensorArray
from . import variable
from .variable import Variable, IndexedSlices
from .python.ops.resource_variable_ops import ResourceVariable
from . import keras
from . import compat
from . import image
from . import linalg
from .linalg import matmul, tensordot, eig, eye, norm
from . import math
from .math import *
from . import nest
from . import nn
from . import __operators__
from . import quantization
from . import random
from . import general_functions
from .general_functions import *
from . import raw_ops
from . import sets
from . import signal
from . import sparse


_frontend_array = constant

# setting to specific version #
# --------------------------- #

if startai.is_local():
    module = startai.utils._importlib.import_cache[__name__]
else:
    module = sys.modules[__name__]

__version__ = set_frontend_to_specific_version(module)
