# global
import startai
from startai.func_wrapper import with_supported_dtypes
from startai.functional.frontends.paddle.func_wrapper import (
    to_startai_arrays_and_back,
)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int16", "int32", "int64", "uint8")},
    "paddle",
)
@to_startai_arrays_and_back
def argmax(x, /, *, axis=None, keepdim=False, dtype="int64", name=None):
    return startai.argmax(x, axis=axis, keepdims=keepdim, dtype=dtype)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int16", "int32", "int64", "uint8")},
    "paddle",
)
@to_startai_arrays_and_back
def argmin(x, /, *, axis=None, keepdim=False, dtype="int64", name=None):
    return startai.argmin(x, axis=axis, keepdims=keepdim, dtype=dtype)


@with_supported_dtypes(
    {"2.4.2 and below": ("float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def argsort(x, /, *, axis=-1, descending=False, name=None):
    return startai.argsort(x, axis=axis, descending=descending)


@with_supported_dtypes(
    {"2.6.0 and below": ("int32", "int64", "float32", "float64")},
    "paddle",
)
@to_startai_arrays_and_back
def index_sample(x, index):
    index_dtype = index.dtype
    arange_tensor = startai.arange(x.shape[0], dtype=index_dtype)[:, None]
    return x[arange_tensor, index]


# kthvalue
@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")}, "paddle"
)
@to_startai_arrays_and_back
def kthvalue(x, k, axis=None, keepdim=False, name=None):
    if axis is None:
        axis = -1
    sorted_input = startai.sort(x, axis=axis)
    sort_indices = startai.argsort(x, axis=axis)

    values = startai.gather(sorted_input, startai.array(k - 1), axis=axis)
    indices = startai.gather(sort_indices, startai.array(k - 1), axis=axis)

    if keepdim:
        values = startai.expand_dims(values, axis=axis)
        indices = startai.expand_dims(indices, axis=axis)

    ret = (values, indices)
    return ret


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def masked_select(x, mask, name=None):
    return startai.flatten(x[mask])


@with_supported_dtypes(
    {"2.4.2 and below": ("float32", "float64", "int16", "int32", "int64", "uint8")},
    "paddle",
)
@to_startai_arrays_and_back
def nonzero(input, /, *, as_tuple=False):
    ret = startai.nonzero(input)
    if as_tuple is False:
        ret = startai.matrix_transpose(startai.stack(ret))
    return ret


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def searchsorted(sorted_sequence, values, out_int32=False, right=False, name=None):
    if right:
        side = "right"
    else:
        side = "left"
    ret = startai.searchsorted(sorted_sequence, values, side=side)
    if out_int32:
        ret = startai.astype(ret, "int32")
    return ret


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def sort(x, /, *, axis=-1, descending=False, name=None):
    return startai.sort(x, axis=axis, descending=descending)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def topk(x, k, axis=None, largest=True, sorted=True, name=None):
    return startai.top_k(x, k, axis=axis, largest=largest, sorted=sorted)


# where
@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")},
    "paddle",
)
@to_startai_arrays_and_back
def where(condition, x, y, name=None):
    return startai.where(condition, x, y)
