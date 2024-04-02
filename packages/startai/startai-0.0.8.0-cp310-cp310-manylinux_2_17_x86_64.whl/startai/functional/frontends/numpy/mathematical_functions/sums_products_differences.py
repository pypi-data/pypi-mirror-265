# global
import startai

# local
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)
import startai.functional.frontends.numpy as np_frontend


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
def cumprod(a, /, axis=None, dtype=None, out=None):
    return startai.cumprod(a, axis=axis, dtype=dtype, out=out)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
def cumsum(a, /, axis=None, dtype=None, out=None):
    return startai.cumsum(a, axis=axis, dtype=dtype, out=out)


@to_startai_arrays_and_back
def diff(x, /, *, n=1, axis=-1, prepend=None, append=None):
    return startai.diff(x, n=n, axis=axis, prepend=prepend, append=append)


@to_startai_arrays_and_back
def ediff1d(ary, to_end=None, to_begin=None):
    diffs = startai.diff(ary)
    if to_begin is not None:
        if not isinstance(to_begin, (list, tuple)):
            to_begin = [to_begin]
        to_begin = startai.array(to_begin)
        diffs = startai.concat((to_begin, diffs))
    if to_end is not None:
        if not isinstance(to_end, (list, tuple)):
            to_end = [to_end]
        to_end = startai.array(to_end)
        diffs = startai.concat((diffs, to_end))
    return diffs


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
def nancumprod(a, /, axis=None, dtype=None, out=None):
    a = startai.where(startai.isnan(a), startai.ones_like(a), a)
    return startai.cumprod(a, axis=axis, dtype=dtype, out=out)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
def nancumsum(a, /, axis=None, dtype=None, out=None):
    a = startai.where(startai.isnan(a), startai.zeros_like(a), a)
    return startai.cumsum(a, axis=axis, dtype=dtype, out=out)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nanprod(
    a, /, *, axis=None, dtype=None, out=None, keepdims=False, initial=None, where=None
):
    fill_values = startai.ones_like(a)
    a = startai.where(startai.isnan(a), fill_values, a)
    if startai.is_array(where):
        a = startai.where(where, a, startai.default(out, fill_values), out=out)
    if initial is not None:
        a[axis] = 1
        s = startai.shape(a, as_array=False)
        header = startai.full(s, initial)
        a = startai.concat([header, a], axis=axis)
    return startai.prod(a, axis=axis, dtype=dtype, keepdims=keepdims, out=out)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nansum(
    a, /, *, axis=None, dtype=None, out=None, keepdims=False, initial=None, where=None
):
    fill_values = startai.zeros_like(a)
    a = startai.where(startai.isnan(a), fill_values, a)
    if startai.is_array(where):
        a = startai.where(where, a, startai.default(out, fill_values), out=out)
    if initial is not None:
        a[axis] = 1
        s = startai.shape(a, as_array=False)
        header = startai.full(s, initial)
        a = startai.concat([header, a], axis=axis)
    return startai.sum(a, axis=axis, dtype=dtype, keepdims=keepdims, out=out)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def prod(
    x,
    /,
    *,
    axis=None,
    dtype=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
    if where is not True:
        x = startai.where(where, x, startai.default(out, startai.ones_like(x)), out=out)
    if initial is not None:
        initial = np_frontend.array(initial, dtype=dtype).tolist()
        if axis is not None:
            s = startai.to_list(startai.shape(x, as_array=True))
            s[axis] = 1
            header = startai.full(startai.Shape(tuple(s)), initial)
            x = startai.concat([header, x], axis=axis)
        else:
            x[0] *= initial
    return startai.prod(x, axis=axis, dtype=dtype, keepdims=keepdims, out=out)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def sum(
    x,
    /,
    *,
    axis=None,
    dtype=None,
    keepdims=False,
    out=None,
    initial=None,
    where=True,
):
    if startai.is_array(where):
        x = startai.where(where, x, startai.default(out, startai.zeros_like(x)), out=out)
    if initial is not None:
        s = startai.to_list(startai.shape(x, as_array=True))
        s[axis] = 1
        header = startai.full(startai.Shape(tuple(s)), initial)
        if startai.is_array(where):
            x = startai.where(where, x, startai.default(out, startai.zeros_like(x)), out=out)
        x = startai.concat([header, x], axis=axis)
    else:
        x = startai.where(startai.isnan(x), startai.zeros_like(x), x)
    return startai.sum(x, axis=axis, dtype=dtype, keepdims=keepdims, out=out)


@to_startai_arrays_and_back
def trapz(y, x=None, dx=1.0, axis=-1):
    return startai.trapz(y, x=x, dx=dx, axis=axis)
