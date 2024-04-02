# global
import startai
from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
import startai.functional.frontends.paddle as paddle_frontend
from startai.functional.frontends.paddle.func_wrapper import (
    to_startai_arrays_and_back,
)


@with_unsupported_dtypes({"2.6.0 and below": ("float16", "bfloat16")}, "paddle")
@to_startai_arrays_and_back
def arange(start, end=None, step=1, dtype=None, name=None):
    return startai.arange(start, end, step=step, dtype=dtype)


@with_supported_dtypes(
    {"2.6.0 and below": ("float16", "float32", "float64", "int32", "int64", "bool")},
    "paddle",
)
@to_startai_arrays_and_back
def assign(x, output=None):
    if len(startai.shape(x)) != 0:
        x = startai.reshape(x, startai.shape(x))
    ret = startai.copy_array(x, to_startai_array=False, out=output)
    return ret


@with_unsupported_dtypes(
    {"2.6.0 and below": ("bfloat16", "uint16", "uint32", "uint64")}, "paddle"
)
@to_startai_arrays_and_back
def clone(x):
    return startai.copy_array(x)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64")},
    "paddle",
)
@to_startai_arrays_and_back
def complex(real, imag, name=None):
    assert real.dtype == imag.dtype, (
        "(InvalidArgument) The type of data we are trying to retrieve does not match"
        " the type of data currently contained in the container."
    )
    complex_dtype = "complex64" if real.dtype == "float32" else "complex128"
    imag_cmplx = startai.astype(imag, complex_dtype) * 1j
    complex_array = real + imag_cmplx
    return complex_array


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")}, "paddle"
)
@to_startai_arrays_and_back
def diag(x, offset=0, padding_value=0, name=None):
    if len(x.shape) == 1:
        padding_value = startai.astype(padding_value, startai.dtype(x))
        ret = startai.diagflat(x, offset=offset, padding_value=padding_value)
        if len(ret.shape) != 2:
            ret = startai.reshape(ret, (1, 1))
    else:
        ret = startai.diag(x, k=offset)
    return ret


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")}, "paddle"
)
@to_startai_arrays_and_back
def diagflat(x, offset=0, name=None):
    arr = startai.diagflat(x, offset=offset)
    return arr


@to_startai_arrays_and_back
def empty(shape, dtype=None):
    return startai.empty(shape=shape, dtype=dtype)


@to_startai_arrays_and_back
def empty_like(x, dtype=None, name=None):
    return startai.empty_like(x, dtype=dtype)


@with_supported_dtypes(
    {"2.6.0 and below": ("float16", "float32", "float64", "int32", "int64")}, "paddle"
)
@to_startai_arrays_and_back
def eye(num_rows, num_columns=None, dtype=None, name=None):
    return startai.eye(num_rows, num_columns, dtype=dtype)


@to_startai_arrays_and_back
def full(shape, fill_value, /, *, dtype=None, name=None):
    dtype = "float32" if dtype is None else dtype
    return startai.full(shape, fill_value, dtype=dtype)


@to_startai_arrays_and_back
def full_like(x, fill_value, /, *, dtype=None, name=None):
    dtype = x.dtype if dtype is None else dtype
    return startai.full_like(x, fill_value, dtype=dtype)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")}, "paddle"
)
@to_startai_arrays_and_back
def linspace(start, stop, num, dtype=None, name=None):
    return startai.linspace(start, stop, num=num, dtype=dtype)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")}, "paddle"
)
@to_startai_arrays_and_back
def logspace(start, stop, num, base=10.0, dtype=None, name=None):
    return startai.logspace(start, stop, num=num, base=base, dtype=dtype)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")}, "paddle"
)
@to_startai_arrays_and_back
def meshgrid(*args, **kwargs):
    return startai.meshgrid(*args, indexing="ij")


@with_unsupported_dtypes({"2.6.0 and below": "int8"}, "paddle")
@to_startai_arrays_and_back
def ones(shape, /, *, dtype=None, name=None):
    dtype = "float32" if dtype is None else dtype
    return startai.ones(shape, dtype=dtype)


@with_unsupported_dtypes(
    {"2.6.0 and below": ("uint8", "int8", "complex64", "complex128")}, "paddle"
)
@to_startai_arrays_and_back
def ones_like(x, /, *, dtype=None, name=None):
    dtype = x.dtype if dtype is None else dtype
    return startai.ones_like(x, dtype=dtype)


@to_startai_arrays_and_back
def to_tensor(data, /, *, dtype=None, place=None, stop_gradient=True):
    array = startai.array(data, dtype=dtype, device=place)
    return paddle_frontend.Tensor(array, dtype=dtype, place=place)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "bool",
            "float64",
            "float32",
            "int32",
            "int64",
            "complex64",
            "complex128",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def tril(x, diagonal=0, name=None):
    return startai.tril(x, k=diagonal)


@with_supported_dtypes({"2.6.0 and below": ("int32", "int64")}, "paddle")
@to_startai_arrays_and_back
def tril_indices(row, col, offset=0, dtype="int64"):
    arr = startai.tril_indices(row, col, offset)
    arr = startai.astype(arr, dtype)
    return arr


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "float64",
            "float32",
            "int32",
            "int64",
            "complex64",
            "complex128",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def triu(x, diagonal=0, name=None):
    return startai.triu(x, k=diagonal)


@with_supported_dtypes({"2.6.0 and below": ("int32", "int64")}, "paddle")
@to_startai_arrays_and_back
def triu_indices(row, col=None, offset=0, dtype="int64"):
    arr = startai.triu_indices(row, col, offset)
    if not startai.to_scalar(startai.shape(arr[0], as_array=True)):
        return arr
    arr = startai.astype(arr, dtype)
    return arr


@with_unsupported_dtypes({"2.6.0 and below": "int8"}, "paddle")
@to_startai_arrays_and_back
def zeros(shape, /, *, dtype=None, name=None):
    dtype = "float32" if dtype is None else dtype
    return startai.zeros(shape, dtype=dtype)


@with_unsupported_dtypes(
    {"2.6.0 and below": ("uint8", "int8", "complex64", "complex128")}, "paddle"
)
@to_startai_arrays_and_back
def zeros_like(x, /, *, dtype=None, name=None):
    dtype = x.dtype if dtype is None else dtype
    return startai.zeros_like(x, dtype=dtype)
