# global
import startai
import startai.functional.frontends.paddle as paddle
from startai.func_wrapper import (
    with_unsupported_dtypes,
    handle_out_argument,
    with_supported_dtypes,
)
from startai.functional.frontends.paddle.func_wrapper import (
    to_startai_arrays_and_back,
)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "float32",
            "float64",
            "bool",
            "uint8",
            "int8",
            "int16",
            "int32",
            "int64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def allclose(x, y, rtol=1e-05, atol=1e-08, equal_nan=False, name=None):
    ret = startai.allclose(x, y, rtol=rtol, atol=atol, equal_nan=equal_nan)
    return paddle.to_tensor([ret])


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "uint8",
            "int8",
            "int16",
            "int32",
            "int64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def bitwise_and(x, y, /, *, name=None, out=None):
    return startai.bitwise_and(x, y, out=out)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "uint8",
            "int8",
            "int16",
            "int32",
            "int64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def bitwise_not(x, out=None, name=None):
    return startai.bitwise_invert(x, out=out)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "uint8",
            "int8",
            "int16",
            "int32",
            "int64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def bitwise_or(x, y, name=None, out=None):
    return startai.bitwise_or(x, y, out=out)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "uint8",
            "int8",
            "int16",
            "int32",
            "int64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def bitwise_xor(x, y, /, *, name=None, out=None):
    return startai.bitwise_xor(x, y, out=out)


@with_unsupported_dtypes(
    {"2.6.0 and below": ("uint8", "int8", "int16", "complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def equal(x, y, /, *, name=None):
    return startai.equal(x, y)


@with_unsupported_dtypes(
    {
        "2.6.0 and below": (
            "uint8",
            "int8",
            "int16",
            "float16",
            "complex64",
            "complex128",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def equal_all(x, y, /, *, name=None):
    return paddle.to_tensor([startai.array_equal(x, y)])


@with_unsupported_dtypes(
    {"2.6.0 and below": ("bool", "uint8", "int8", "int16", "complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def greater_equal(x, y, /, *, name=None):
    return startai.greater_equal(x, y)


@with_unsupported_dtypes(
    {"2.6.0 and below": ("bool", "uint8", "int8", "int16", "complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def greater_than(x, y, /, *, name=None):
    return startai.greater(x, y)


@with_unsupported_dtypes(
    {
        "2.6.0 and below": (
            "uint8",
            "int8",
            "int16",
            "complex64",
            "complex128",
            "bool",
            "float16",
            "bfloat16",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def is_empty(x, name=None):
    if 0 in startai.shape(x):
        return startai.array(True)
    else:
        return startai.array(False)


@to_startai_arrays_and_back
def is_tensor(x):
    return startai.is_array(x)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def isclose(x, y, rtol=1e-05, atol=1e-08, equal_nan=False, name=None):
    return startai.isclose(x, y, rtol=rtol, atol=atol, equal_nan=equal_nan)


@with_unsupported_dtypes(
    {"2.6.0 and below": ("bool", "uint8", "int8", "int16", "complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def less_equal(x, y, /, *, name=None):
    return startai.less_equal(x, y)


@with_supported_dtypes(
    {"2.6.0 and below": ("bool", "float16", "float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def less_than(x, y, /, *, name=None):
    return startai.astype(startai.less(x, y), startai.bool)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "int8",
            "int16",
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def logical_and(x, y, /, *, name=None, out=None):
    return startai.logical_and(x, y, out=out)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "int8",
            "int16",
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def logical_not(x, /, *, name=None, out=None):
    return startai.logical_not(x, out=out)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "int8",
            "int16",
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def logical_or(x, y, /, *, name=None, out=None):
    return startai.logical_or(x, y, out=out)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "int8",
            "int16",
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
@handle_out_argument
def logical_xor(x, y, /, *, name=None, out=None):
    return startai.logical_xor(x, y, out=out)


@with_unsupported_dtypes(
    {"2.6.0 and below": ("uint8", "int8", "int16", "complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def not_equal(x, y, /, *, name=None):
    if startai.is_float_dtype(x):
        diff = startai.abs(startai.subtract(x, y))
        res = startai.not_equal(x, y)
        return startai.where(diff < 1e-8, False, res)
    return startai.not_equal(x, y)
