# global
import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_casting,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)


# --- Helpers --- #
# --------------- #


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def _fmax(
    x1,
    x2,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.fmax(x1, x2, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _fmin(
    x1,
    x2,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.fmin(x1, x2, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _maximum(
    x1,
    x2,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.maximum(x1, x2, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _minimum(
    x1,
    x2,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.minimum(x1, x2, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


# --- Main --- #
# ------------ #


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def amax(
    a,
    /,
    *,
    axis=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
    out_dtype = startai.dtype(a)
    where_mask = None
    if initial is not None:
        if startai.is_array(where):
            a = startai.where(where, a, a.full_like(initial))
            where_mask = startai.all(startai.logical_not(where), axis=axis, keepdims=keepdims)
        s = startai.shape(a, as_array=True)
        if axis is not None:
            if isinstance(axis, (tuple, list)) or startai.is_array(axis):
                # introducing the initial in one dimension is enough
                ax = axis[0] % len(s)
                s[ax] = 1
            else:
                ax = axis % len(s)
                s[ax] = 1
        header = startai.full(startai.Shape(s.to_list()), initial, dtype=startai.dtype(a))
        if axis:
            if isinstance(axis, (tuple, list)) or startai.is_array(axis):
                a = startai.concat([a, header], axis=axis[0])
            else:
                a = startai.concat([a, header], axis=axis)
        else:
            a = startai.concat([a, header], axis=0)
    res = startai.max(a, axis=axis, keepdims=keepdims, out=out)
    if where_mask is not None and startai.any(where_mask):
        res = startai.where(startai.logical_not(where_mask), res, initial, out=out)
    return startai.astype(res, out_dtype, out=out, copy=False)


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def amin(
    a,
    /,
    *,
    axis=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
    out_dtype = startai.dtype(a)
    where_mask = None
    if initial is not None:
        if startai.is_array(where):
            a = startai.where(where, a, a.full_like(initial))
            where_mask = startai.all(startai.logical_not(where), axis=axis, keepdims=keepdims)
        s = startai.shape(a, as_array=True)
        if axis is not None:
            if isinstance(axis, (tuple, list)) or startai.is_array(axis):
                # introducing the initial in one dimension is enough
                ax = axis[0] % len(s)
                s[ax] = 1
            else:
                ax = axis % len(s)
                s[ax] = 1
        header = startai.full(startai.Shape(s.to_list()), initial, dtype=startai.dtype(a))
        if axis:
            if isinstance(axis, (tuple, list)) or startai.is_array(axis):
                a = startai.concat([a, header], axis=axis[0])
            else:
                a = startai.concat([a, header], axis=axis)
        else:
            a = startai.concat([a, header], axis=0)
    res = startai.min(a, axis=axis, keepdims=keepdims, out=out)
    if where_mask is not None and startai.any(where_mask):
        res = startai.where(startai.logical_not(where_mask), res, initial, out=out)
    return startai.astype(res, out_dtype, out=out, copy=False)


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def max(
    a,
    /,
    *,
    axis=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
    return amax(a, axis=axis, out=out, keepdims=keepdims, initial=initial, where=where)


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def min(
    a,
    /,
    *,
    axis=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
    return amin(a, axis=axis, out=out, keepdims=keepdims, initial=initial, where=where)


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nanmax(
    a,
    axis=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
    out_dtype = startai.dtype(a)
    nan_mask = startai.isnan(a)
    a = startai.where(startai.logical_not(nan_mask), a, a.full_like(-startai.inf))
    where_mask = None
    if initial is not None:
        if startai.is_array(where):
            a = startai.where(where, a, a.full_like(initial))
            where_mask = startai.all(startai.logical_not(where), axis=axis, keepdims=keepdims)
        s = startai.shape(a, as_array=True)
        if axis is not None:
            if isinstance(axis, (tuple, list)) or startai.is_array(axis):
                # introducing the initial in one dimension is enough
                ax = axis[0] % len(s)
                s[ax] = 1
            else:
                ax = axis % len(s)
                s[ax] = 1
        header = startai.full(startai.Shape(s.to_list()), initial, dtype=startai.dtype(a))
        if axis:
            if isinstance(axis, (tuple, list)) or startai.is_array(axis):
                a = startai.concat([a, header], axis=axis[0])
            else:
                a = startai.concat([a, header], axis=axis)
        else:
            a = startai.concat([a, header], axis=0)
    res = startai.max(a, axis=axis, keepdims=keepdims, out=out)
    if nan_mask is not None:
        nan_mask = startai.all(nan_mask, axis=axis, keepdims=keepdims, out=out)
        if startai.any(nan_mask):
            res = startai.where(
                startai.logical_not(nan_mask),
                res,
                initial if initial is not None else startai.nan,
                out=out,
            )
    if where_mask is not None and startai.any(where_mask):
        res = startai.where(startai.logical_not(where_mask), res, startai.nan, out=out)
    return startai.astype(res, out_dtype, out=out, copy=False)


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nanmin(
    a,
    axis=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
    out_dtype = startai.dtype(a)
    nan_mask = startai.isnan(a)
    a = startai.where(startai.logical_not(nan_mask), a, a.full_like(+startai.inf))
    where_mask = None
    if initial is not None:
        if startai.is_array(where):
            a = startai.where(where, a, a.full_like(initial))
            where_mask = startai.all(startai.logical_not(where), axis=axis, keepdims=keepdims)
        s = startai.shape(a, as_array=True)
        if axis is not None:
            if isinstance(axis, (tuple, list)) or startai.is_array(axis):
                # introducing the initial in one dimension is enough
                ax = axis[0] % len(s)
                s[ax] = 1
            else:
                ax = axis % len(s)
                s[ax] = 1
        header = startai.full(startai.Shape(s.to_list()), initial, dtype=startai.dtype(a))
        if axis:
            if isinstance(axis, (tuple, list)) or startai.is_array(axis):
                a = startai.concat([a, header], axis=axis[0])
            else:
                a = startai.concat([a, header], axis=axis)
        else:
            a = startai.concat([a, header], axis=0)
    res = startai.min(a, axis=axis, keepdims=keepdims, out=out)
    if nan_mask is not None:
        nan_mask = startai.all(nan_mask, axis=axis, keepdims=keepdims, out=out)
        if startai.any(nan_mask):
            res = startai.where(
                startai.logical_not(nan_mask),
                res,
                initial if initial is not None else startai.nan,
                out=out,
            )
    if where_mask is not None and startai.any(where_mask):
        res = startai.where(startai.logical_not(where_mask), res, startai.nan, out=out)
    return startai.astype(res, out_dtype, out=out, copy=False)
