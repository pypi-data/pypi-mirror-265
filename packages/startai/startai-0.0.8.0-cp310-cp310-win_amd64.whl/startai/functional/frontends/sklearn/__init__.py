from . import tree
import startai
from startai.functional.frontends.numpy import array

_int8 = startai.IntDtype("int8")
_int16 = startai.IntDtype("int16")
_int32 = startai.IntDtype("int32")
_int64 = startai.IntDtype("int64")
_uint8 = startai.UintDtype("uint8")
_uint16 = startai.UintDtype("uint16")
_uint32 = startai.UintDtype("uint32")
_uint64 = startai.UintDtype("uint64")
_bfloat16 = startai.FloatDtype("bfloat16")
_float16 = startai.FloatDtype("float16")
_float32 = startai.FloatDtype("float32")
_float64 = startai.FloatDtype("float64")
_complex64 = startai.ComplexDtype("complex64")
_complex128 = startai.ComplexDtype("complex128")
_bool = startai.Dtype("bool")

_frontend_array = array
