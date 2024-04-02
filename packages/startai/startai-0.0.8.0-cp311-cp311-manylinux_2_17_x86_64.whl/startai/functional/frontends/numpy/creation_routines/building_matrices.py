import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_dtype,
)


@to_startai_arrays_and_back
def diag(v, k=0):
    return startai.diag(v, k=k)


# diagflat
@to_startai_arrays_and_back
def diagflat(v, k=0):
    ret = startai.diagflat(v, offset=k)
    while len(startai.shape(ret)) < 2:
        ret = ret.expand_dims(axis=0)
    return ret


@handle_numpy_dtype
@to_startai_arrays_and_back
def tri(N, M=None, k=0, dtype="float64", *, like=None):
    if M is None:
        M = N
    ones = startai.ones((N, M), dtype=dtype)
    return startai.tril(ones, k=k)


@to_startai_arrays_and_back
def tril(m, k=0):
    return startai.tril(m, k=k)


@to_startai_arrays_and_back
def triu(m, k=0):
    return startai.triu(m, k=k)


@to_startai_arrays_and_back
def vander(x, N=None, increasing=False):
    if startai.is_float_dtype(x):
        x = x.astype(startai.float64)
    elif startai.is_bool_dtype or startai.is_int_dtype(x):
        x = x.astype(startai.int64)
    return startai.vander(x, N=N, increasing=increasing)
