# global
import startai
from startai.func_wrapper import with_supported_dtypes
from startai.functional.frontends.paddle.func_wrapper import (
    to_startai_arrays_and_back,
)


@to_startai_arrays_and_back
def imag(x):
    return startai.imag(x)


@to_startai_arrays_and_back
def is_complex(x):
    return startai.is_complex_dtype(x)


@to_startai_arrays_and_back
def is_floating_point(x):
    return startai.is_float_dtype(x)


@to_startai_arrays_and_back
def is_integer(x):
    return startai.is_int_dtype(x)


@to_startai_arrays_and_back
def rank(input):
    return startai.get_num_dims(input)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "complex64",
            "complex128",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def real(x):
    return startai.real(x)
