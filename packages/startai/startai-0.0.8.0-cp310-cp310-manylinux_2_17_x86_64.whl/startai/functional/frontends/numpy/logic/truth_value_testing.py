# global
import startai
import numbers
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)
import startai.functional.frontends.numpy as np_frontend


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def all(
    a,
    axis=None,
    out=None,
    keepdims=False,
    *,
    where=None,
):
    axis = tuple(axis) if isinstance(axis, list) else axis
    if where is not None:
        a = startai.where(where, a, True)
    ret = startai.all(a, axis=axis, keepdims=keepdims, out=out)
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def any(
    a,
    axis=None,
    out=None,
    keepdims=False,
    *,
    where=None,
):
    axis = tuple(axis) if isinstance(axis, list) else axis
    if where is not None:
        a = startai.where(where, a, False)
    ret = startai.any(a, axis=axis, keepdims=keepdims, out=out)
    return ret


@to_startai_arrays_and_back
def iscomplex(x):
    return startai.bitwise_invert(startai.isreal(x))


@to_startai_arrays_and_back
def iscomplexobj(x):
    if x.ndim == 0:
        return startai.is_complex_dtype(startai.dtype(x))
    for ele in x:
        return bool(startai.is_complex_dtype(startai.dtype(ele)))


@to_startai_arrays_and_back
def isfortran(a):
    return a.flags.fnc


@to_startai_arrays_and_back
def isreal(x):
    return startai.isreal(x)


@to_startai_arrays_and_back
def isrealobj(x: any):
    return not startai.is_complex_dtype(startai.dtype(x))


@to_startai_arrays_and_back
def isscalar(element):
    return isinstance(
        element,
        (
            int,
            float,
            complex,
            bool,
            bytes,
            str,
            memoryview,
            numbers.Number,
            np_frontend.generic,
        ),
    )
