import sys
import startai
from startai.utils.exceptions import handle_exceptions
from startai.functional.frontends import set_frontend_to_specific_version


# global
from numbers import Number
from typing import Union, Tuple, Iterable


# Constructing dtypes are required as startai.<dtype>
# will change dynamically on the backend and may not be available
int8 = startai.IntDtype("int8")
int16 = startai.IntDtype("int16")
int32 = startai.IntDtype("int32")
int64 = startai.IntDtype("int64")
uint8 = startai.UintDtype("uint8")
float16 = startai.FloatDtype("float16")
float32 = startai.FloatDtype("float32")
float64 = startai.FloatDtype("float64")
complex64 = startai.ComplexDtype("complex64")
complex128 = startai.ComplexDtype("complex128")
bool = startai.Dtype("bool")


# data type promotion
paddle_promotion_table = {
    (uint8, uint8): uint8,
    (uint8, int8): int16,
    (uint8, int16): int16,
    (uint8, int32): int32,
    (uint8, int64): int64,
    (uint8, float16): float16,
    (uint8, float32): float32,
    (uint8, float64): float64,
    (uint8, bool): uint8,
    (uint8, complex64): complex64,
    (uint8, complex128): complex128,
    (int8, uint8): int16,
    (int8, int8): int8,
    (int8, int16): int16,
    (int8, int32): int32,
    (int8, int64): int64,
    (int8, float16): float16,
    (int8, float32): float32,
    (int8, float64): float64,
    (int8, bool): int8,
    (int8, complex64): complex64,
    (int8, complex128): complex128,
    (int16, uint8): int16,
    (int16, int8): int16,
    (int16, int16): int16,
    (int16, int32): int32,
    (int16, int64): int64,
    (int16, float16): float16,
    (int16, float32): float32,
    (int16, float64): float64,
    (int16, bool): int16,
    (int16, complex64): complex64,
    (int16, complex128): complex128,
    (int32, uint8): int32,
    (int32, int8): int32,
    (int32, int16): int32,
    (int32, int32): int32,
    (int32, int64): int64,
    (int32, float16): float16,
    (int32, float32): float32,
    (int32, float64): float64,
    (int32, bool): int32,
    (int32, complex64): complex64,
    (int32, complex128): complex128,
    (int64, uint8): int64,
    (int64, int8): int64,
    (int64, int16): int64,
    (int64, int32): int64,
    (int64, int64): int64,
    (int64, float16): float16,
    (int64, float32): float32,
    (int64, float64): float64,
    (int64, bool): int64,
    (int64, complex64): complex64,
    (int64, complex128): complex128,
    (float16, uint8): float16,
    (float16, int8): float16,
    (float16, int16): float16,
    (float16, int32): float16,
    (float16, int64): float16,
    (float16, float16): float16,
    (float16, float32): float32,
    (float16, float64): float64,
    (float16, bool): float16,
    (float16, complex64): complex64,
    (float16, complex128): complex128,
    (float32, uint8): float32,
    (float32, int8): float32,
    (float32, int16): float32,
    (float32, int32): float32,
    (float32, int64): float32,
    (float32, float16): float32,
    (float32, float32): float32,
    (float32, float64): float64,
    (float32, bool): float32,
    (float32, complex64): complex64,
    (float32, complex128): complex128,
    (float64, uint8): float64,
    (float64, int8): float64,
    (float64, int16): float64,
    (float64, int32): float64,
    (float64, int64): float64,
    (float64, float16): float64,
    (float64, float32): float64,
    (float64, float64): float64,
    (float64, bool): float64,
    (float64, complex64): complex128,
    (float64, complex128): complex128,
    (bool, uint8): uint8,
    (bool, int8): int8,
    (bool, int16): int16,
    (bool, int32): int32,
    (bool, int64): int64,
    (bool, float16): float16,
    (bool, float32): float32,
    (bool, float64): float64,
    (bool, bool): bool,
    (bool, complex64): complex64,
    (bool, complex128): complex128,
    (complex64, uint8): complex64,
    (complex64, int8): complex64,
    (complex64, int16): complex64,
    (complex64, int32): complex64,
    (complex64, int64): complex64,
    (complex64, float16): complex64,
    (complex64, float32): complex64,
    (complex64, float64): complex128,
    (complex64, bool): complex64,
    (complex64, complex64): complex64,
    (complex64, complex128): complex128,
    (complex128, uint8): complex128,
    (complex128, int8): complex128,
    (complex128, int16): complex128,
    (complex128, int32): complex128,
    (complex128, int64): complex128,
    (complex128, float16): complex128,
    (complex128, float32): complex128,
    (complex128, float64): complex128,
    (complex128, bool): complex128,
    (complex128, complex64): complex128,
    (complex128, complex128): complex128,
}


@handle_exceptions
def promote_types_paddle(
    type1: Union[startai.Dtype, startai.NativeDtype],
    type2: Union[startai.Dtype, startai.NativeDtype],
    /,
) -> startai.Dtype:
    """Promote the datatypes type1 and type2, returning the data type they
    promote to.

    Parameters
    ----------
    type1
        the first of the two types to promote
    type2
        the second of the two types to promote

    Returns
    -------
    ret
        The type that both input types promote to
    """
    try:
        ret = paddle_promotion_table[(startai.as_startai_dtype(type1), startai.as_startai_dtype(type2))]
    except KeyError as e:
        raise startai.utils.exceptions.StartaiException(
            "these dtypes are not type promotable"
        ) from e
    return ret


@handle_exceptions
def promote_types_of_paddle_inputs(
    x1: Union[startai.Array, Number, Iterable[Number]],
    x2: Union[startai.Array, Number, Iterable[Number]],
    /,
) -> Tuple[startai.Array, startai.Array]:
    """Promote the dtype of the given native array inputs to a common dtype
    based on type promotion rules.

    While passing float or integer values or any other non-array input
    to this function, it should be noted that the return will be an
    array-like object. Therefore, outputs from this function should be
    used as inputs only for those functions that expect an array-like or
    tensor-like objects, otherwise it might give unexpected results.
    """
    type1 = startai.default_dtype(item=x1).strip("u123456789")
    type2 = startai.default_dtype(item=x2).strip("u123456789")
    if hasattr(x1, "dtype") and not hasattr(x2, "dtype") and type1 == type2:
        x1 = startai.asarray(x1)
        x2 = startai.asarray(
            x2, dtype=x1.dtype, device=startai.default_device(item=x1, as_native=False)
        )
    elif not hasattr(x1, "dtype") and hasattr(x2, "dtype") and type1 == type2:
        x1 = startai.asarray(
            x1, dtype=x2.dtype, device=startai.default_device(item=x2, as_native=False)
        )
        x2 = startai.asarray(x2)
    else:
        x1 = startai.asarray(x1)
        x2 = startai.asarray(x2)
        promoted = promote_types_paddle(x1.dtype, x2.dtype)
        x1 = startai.asarray(x1, dtype=promoted)
        x2 = startai.asarray(x2, dtype=promoted)
    return x1, x2


from . import nn
from . import tensor
from .tensor.tensor import Tensor
from . import vision
from .attribute import *
from .creation import *
from .fft import *
from .linalg import *
from .logic import *
from .manipulation import *
from .math import *
from .random import *
from .search import *
from .stat import *


_frontend_array = Tensor

# setting to specific version #
# --------------------------- #

if startai.is_local():
    module = startai.utils._importlib.import_cache[__name__]
else:
    module = sys.modules[__name__]

__version__ = set_frontend_to_specific_version(module)
