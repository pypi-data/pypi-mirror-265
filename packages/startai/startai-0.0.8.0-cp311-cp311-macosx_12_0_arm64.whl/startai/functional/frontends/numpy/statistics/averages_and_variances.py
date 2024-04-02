# global
import startai
from startai.func_wrapper import with_unsupported_dtypes
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def average(a, /, *, axis=None, weights=None, returned=False, keepdims=False):
    axis = tuple(axis) if isinstance(axis, list) else axis
    avg = 0

    if keepdims is None:
        keepdims_kw = {}
    else:
        keepdims_kw = {"keepdims": keepdims}

    dtype = a.dtype
    if weights is None:
        avg = a.mean(axis, **keepdims_kw)
        weights_sum = avg.dtype.type(a.count(axis))
    else:
        if a.shape != weights.shape:
            if axis is None:
                return 0
            weights = startai.broadcast_to(weights, (a.ndim - 1) * (1,) + weights.shape)
            weights = weights.swapaxes(-1, axis)
        weights_sum = weights.sum(axis=axis, **keepdims_kw)
        mul = startai.multiply(a, weights)
        avg = startai.sum(mul, axis=axis, **keepdims_kw) / weights_sum

    if returned:
        if weights_sum.shape != avg.shape:
            weights_sum = startai.broadcast_to(weights_sum, avg.shape).copy()
        return avg.astype(dtype), weights_sum
    else:
        return avg.astype(dtype)


@to_startai_arrays_and_back
def cov(
    m,
    y=None,
    /,
    *,
    rowvar=True,
    bias=False,
    ddof=None,
    fweights=None,
    aweights=None,
    dtype=None,
):
    return startai.cov(
        m,
        y,
        rowVar=rowvar,
        bias=bias,
        ddof=ddof,
        fweights=fweights,
        aweights=aweights,
        dtype=dtype,
    )


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def mean(a, axis=None, dtype=None, out=None, keepdims=False, *, where=True):
    axis = tuple(axis) if isinstance(axis, list) else axis
    dtype = dtype or a.dtype if not startai.is_int_dtype(a.dtype) else startai.float64
    where = startai.where(where, startai.ones_like(a), 0)
    if where is not True:
        a = startai.where(where, a, 0.0)
        sum = startai.sum(a, axis=axis, keepdims=keepdims, dtype=dtype)
        cnt = startai.sum(where, axis=axis, keepdims=keepdims, dtype=int)
        ret = startai.divide(sum, cnt, out=out)
    else:
        ret = startai.mean(a.astype(dtype), axis=axis, keepdims=keepdims, out=out)

    return ret.astype(dtype)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nanmean(a, axis=None, dtype=None, out=None, keepdims=False, *, where=True):
    where = ~startai.isnan(a) & where
    ret = mean(a, axis, dtype, keepdims=keepdims, where=where).startai_array
    if out is not None:
        out.data = ret.data
    return ret


# nanmedian
@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nanmedian(
    a,
    /,
    *,
    axis=None,
    keepdims=False,
    out=None,
    overwrite_input=False,
):
    ret = startai.nanmedian(
        a, axis=axis, keepdims=keepdims, out=out, overwrite_input=overwrite_input
    )
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nanstd(
    a, /, *, axis=None, dtype=None, out=None, ddof=0, keepdims=False, where=True
):
    a = startai.nan_to_num(a)
    axis = tuple(axis) if isinstance(axis, list) else axis

    if dtype:
        a = startai.astype(startai.array(a), startai.as_startai_dtype(dtype))

    ret = startai.std(a, axis=axis, correction=ddof, keepdims=keepdims, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)

    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.25.0 and below": ("float16", "bfloat16")}, "tensorflow")
def nanvar(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, *, where=True):
    is_nan = startai.isnan(a)
    axis = tuple(axis) if isinstance(axis, list) else axis

    if startai.any(is_nan):
        a = [i for i in a if startai.isnan(i) is False]

    if dtype is None:
        dtype = "float" if startai.is_int_dtype(a) else a.dtype

    a = startai.astype(startai.array(a), startai.as_startai_dtype(dtype))
    ret = startai.var(a, axis=axis, correction=ddof, keepdims=keepdims, out=out)

    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)

    if startai.all(startai.isnan(ret)):
        ret = startai.astype(ret, startai.array([float("inf")]))

    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def std(
    x,
    /,
    *,
    axis=None,
    ddof=0.0,
    keepdims=False,
    out=None,
    dtype=None,
    where=True,
):
    axis = tuple(axis) if isinstance(axis, list) else axis
    if dtype is None:
        if startai.is_int_dtype(x.dtype):
            dtype = startai.float64
        else:
            dtype = x.dtype
    ret = startai.std(x, axis=axis, correction=ddof, keepdims=keepdims, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret.astype(dtype, copy=False)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def var(x, /, *, axis=None, ddof=0.0, keepdims=False, out=None, dtype=None, where=True):
    axis = tuple(axis) if isinstance(axis, list) else axis
    dtype = (
        dtype
        if dtype is not None
        else startai.float64
        if startai.is_int_dtype(x.dtype)
        else x.dtype
    )
    ret = startai.var(x, axis=axis, correction=ddof, keepdims=keepdims, out=out)
    ret = (
        startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
        if startai.is_array(where)
        else ret
    )
    return ret.astype(dtype, copy=False)
