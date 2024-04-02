# global
import startai
from startai.func_wrapper import with_supported_dtypes
from startai.functional.frontends.paddle.func_wrapper import (
    to_startai_arrays_and_back,
)


@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def mean(input, axis=None, keepdim=False, out=None):
    ret = startai.mean(input, axis=axis, keepdims=keepdim, out=out)
    return ret


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def median(x, axis=None, keepdim=False, name=None):
    x = (
        startai.astype(x, startai.float64)
        if startai.dtype(x) == "float64"
        else startai.astype(x, startai.float32)
    )
    return startai.median(x, axis=axis, keepdims=keepdim)


@with_supported_dtypes(
    {"2.5.0 and below": ("float16", "float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def nanmedian(x, axis=None, keepdim=True, name=None):
    return startai.nanmedian(x, axis=axis, keepdims=keepdim)


@with_supported_dtypes(
    {"2.6.0 and below": ("bool", "float16", "float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def numel(x, name=None):
    prod = startai.prod(x.size, dtype=startai.int64)
    try:
        length = len(x)
    except (ValueError, TypeError):
        length = 1  # if 0 dimensional tensor with 1 element
    return startai.array(prod if prod > 0 else startai.array(length, dtype=startai.int64))


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "uint16")},
    "paddle",
)
@to_startai_arrays_and_back
def std(x, axis=None, unbiased=True, keepdim=False, name=None):
    x = (
        startai.astype(x, startai.float64)
        if startai.dtype(x) == "float64"
        else startai.astype(x, startai.float32)
    )
    return startai.std(x, axis=axis, correction=int(unbiased), keepdims=keepdim)


@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def var(x, axis=None, unbiased=True, keepdim=False, name=None):
    if unbiased:
        correction = 1
    else:
        correction = 0
    return startai.var(x, axis=axis, correction=correction, keepdims=keepdim)
