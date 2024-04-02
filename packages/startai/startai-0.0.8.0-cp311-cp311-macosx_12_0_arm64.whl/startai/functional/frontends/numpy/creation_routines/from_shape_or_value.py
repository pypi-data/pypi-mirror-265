# local
import startai
from startai.functional.frontends.numpy.func_wrapper import (
    outputs_to_frontend_arrays,
    handle_numpy_dtype,
)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def empty(shape, dtype="float64", order="C", *, like=None):
    return startai.empty(shape=shape, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def empty_like(prototype, dtype=None, order="K", subok=True, shape=None):
    if shape:
        return startai.empty(shape=shape, dtype=dtype)
    return startai.empty_like(prototype, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def eye(N, M=None, k=0, dtype="float64", order="C", *, like=None):
    return startai.eye(N, M, k=k, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def fromfunction(function, shape, *, dtype="float64", like=None, **kwargs):
    args = startai.indices(shape, dtype=dtype)
    return function(*args, **kwargs)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def full(shape, fill_value, dtype=None, order="C", *, like=None):
    return startai.full(shape, fill_value, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def full_like(a, fill_value, dtype=None, order="K", subok=True, shape=None):
    if shape:
        return startai.full(shape, fill_value, dtype=dtype)
    return startai.full_like(a, fill_value, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def identity(n, dtype=None, *, like=None):
    return startai.eye(n, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def ones(shape, dtype=None, order="C", *, like=None):
    return startai.ones(shape, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def ones_like(a, dtype=None, order="K", subok=True, shape=None):
    if shape:
        return startai.ones(shape, dtype=dtype)
    return startai.ones_like(a, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def zeros(shape, dtype=float, order="C", *, like=None):
    return startai.zeros(shape, dtype=dtype)


@handle_numpy_dtype
@outputs_to_frontend_arrays
def zeros_like(a, dtype=None, order="K", subok=True, shape=None):
    if shape:
        return startai.zeros(shape, dtype=dtype)
    return startai.zeros_like(a, dtype=dtype)
