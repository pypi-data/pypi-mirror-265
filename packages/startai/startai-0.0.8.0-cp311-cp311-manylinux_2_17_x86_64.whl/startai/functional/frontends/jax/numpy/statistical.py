# local

import startai
from startai.func_wrapper import with_unsupported_dtypes
from startai.functional.frontends.jax.func_wrapper import (
    to_startai_arrays_and_back,
    handle_jax_dtype,
)
from startai.functional.frontends.jax.numpy import promote_types_of_jax_inputs


@to_startai_arrays_and_back
def argmin(a, axis=None, out=None, keepdims=None):
    return startai.argmin(a, axis=axis, out=out, keepdims=keepdims)


@to_startai_arrays_and_back
def average(a, axis=None, weights=None, returned=False, keepdims=False):
    # canonicalize_axis to ensure axis or the values in axis > 0
    if isinstance(axis, (tuple, list)):
        a_ndim = len(startai.shape(a))
        new_axis = [0] * len(axis)
        for i, v in enumerate(axis):
            if not -a_ndim <= v < a_ndim:
                raise ValueError(
                    f"axis {v} is out of bounds for array of dimension {a_ndim}"
                )
            new_axis[i] = v + a_ndim if v < 0 else v
        axis = tuple(new_axis)

    if weights is None:
        ret = startai.mean(a, axis=axis, keepdims=keepdims)
        if axis is None:
            fill_value = int(a.size) if startai.is_int_dtype(ret) else float(a.size)
            weights_sum = startai.full((), fill_value, dtype=ret.dtype)
        else:
            if isinstance(axis, tuple):
                # prod with axis has dtype Sequence[int]
                fill_value = 1
                for d in axis:
                    fill_value *= a.shape[d]
            else:
                fill_value = a.shape[axis]
            weights_sum = startai.full_like(ret, fill_value=fill_value)
    else:
        a = startai.asarray(a, copy=False)
        weights = startai.asarray(weights, copy=False)
        a, weights = promote_types_of_jax_inputs(a, weights)

        a_shape = startai.shape(a)
        a_ndim = len(a_shape)
        weights_shape = startai.shape(weights)

        # Make sure the dimensions work out
        if a_shape != weights_shape:
            if len(weights_shape) != 1:
                raise ValueError(
                    "1D weights expected when shapes of a and weights differ."
                )
            if axis is None:
                raise ValueError(
                    "Axis must be specified when shapes of a and weights differ."
                )
            elif isinstance(axis, tuple):
                raise ValueError(
                    "Single axis expected when shapes of a and weights differ"
                )
            elif weights.shape[0] != a.shape[axis]:
                raise ValueError(
                    "Length of weights not compatible with specified axis."
                )

            weights = startai.broadcast_to(
                weights, shape=(a_ndim - 1) * (1,) + weights_shape
            )
            weights = startai.moveaxis(weights, -1, axis)

        weights_sum = startai.sum(weights, axis=axis)
        ret = startai.sum(a * weights, axis=axis, keepdims=keepdims) / weights_sum

    if returned:
        if ret.shape != weights_sum.shape:
            weights_sum = startai.broadcast_to(weights_sum, shape=ret.shape)
        return ret, weights_sum

    return ret


@to_startai_arrays_and_back
def bincount(x, weights=None, minlength=0, *, length=None):
    x_list = [int(x[i]) for i in range(x.shape[0])]
    max_val = int(startai.max(startai.array(x_list)))
    ret = [x_list.count(i) for i in range(0, max_val + 1)]
    ret = startai.array(ret)
    ret = startai.astype(ret, startai.as_startai_dtype(startai.int64))
    return ret


@to_startai_arrays_and_back
def corrcoef(x, y=None, rowvar=True):
    return startai.corrcoef(x, y=y, rowvar=rowvar)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"0.4.24 and below": ("float16", "bfloat16")}, "jax")
def correlate(a, v, mode="valid", precision=None):
    if startai.get_num_dims(a) != 1 or startai.get_num_dims(v) != 1:
        raise ValueError("correlate() only support 1-dimensional inputs.")
    if a.shape[0] == 0 or v.shape[0] == 0:
        raise ValueError(
            f"correlate: inputs cannot be empty, got shapes {a.shape} and {v.shape}."
        )
    if v.shape[0] > a.shape[0]:
        need_flip = True
        a, v = v, a
    else:
        need_flip = False

    out_order = slice(None)

    if mode == "valid":
        padding = [(0, 0)]
    elif mode == "same":
        padding = [(v.shape[0] // 2, v.shape[0] - v.shape[0] // 2 - 1)]
    elif mode == "full":
        padding = [(v.shape[0] - 1, v.shape[0] - 1)]
    else:
        raise ValueError("mode must be one of ['full', 'same', 'valid']")

    result = startai.conv_general_dilated(
        a[None, None, :],
        v[:, None, None],
        (1,),
        padding,
        dims=1,
        data_format="channel_first",
    )
    return startai.flip(result[0, 0, out_order]) if need_flip else result[0, 0, out_order]


@to_startai_arrays_and_back
def cov(m, y=None, rowvar=True, bias=False, ddof=None, fweights=None, aweights=None):
    return startai.cov(
        m, y, rowVar=rowvar, bias=bias, ddof=ddof, fweights=fweights, aweights=aweights
    )


@handle_jax_dtype
@to_startai_arrays_and_back
def cumprod(a, axis=None, dtype=None, out=None):
    if dtype is None:
        dtype = startai.as_startai_dtype(a.dtype)
    return startai.cumprod(a, axis=axis, dtype=dtype, out=out)


@handle_jax_dtype
@to_startai_arrays_and_back
def cumsum(a, axis=0, dtype=None, out=None):
    if dtype is None:
        dtype = startai.uint8
    return startai.cumsum(a, axis, dtype=dtype, out=out)


@to_startai_arrays_and_back
def einsum(
    subscripts,
    *operands,
    out=None,
    optimize="optimal",
    precision=None,
    preferred_element_type=None,
    _use_xeinsum=False,
    _dot_general=None,
):
    return startai.einsum(subscripts, *operands, out=out)


@to_startai_arrays_and_back
def max(a, axis=None, out=None, keepdims=False, where=None):
    ret = startai.max(a, axis=axis, out=out, keepdims=keepdims)
    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_jax_dtype
@to_startai_arrays_and_back
def mean(a, axis=None, dtype=None, out=None, keepdims=False, *, where=None):
    axis = tuple(axis) if isinstance(axis, list) else axis
    if dtype is None:
        dtype = "float32" if startai.is_int_dtype(a) else a.dtype
    ret = startai.mean(a, axis=axis, keepdims=keepdims, out=out)
    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return startai.astype(ret, startai.as_startai_dtype(dtype), copy=False)


@to_startai_arrays_and_back
def median(a, axis=None, out=None, overwrite_input=False, keepdims=False):
    return startai.median(a, axis=axis, out=out, keepdims=keepdims)


@to_startai_arrays_and_back
def min(a, axis=None, out=None, keepdims=False, where=None):
    ret = startai.min(a, axis=axis, out=out, keepdims=keepdims)
    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_jax_dtype
@to_startai_arrays_and_back
def nancumprod(a, axis=None, dtype=None, out=None):
    a = startai.where(startai.isnan(a), startai.zeros_like(a), a)
    return startai.cumprod(a, axis=axis, dtype=dtype, out=out)


@handle_jax_dtype
@to_startai_arrays_and_back
def nancumsum(a, axis=None, dtype=None, out=None):
    a = startai.where(startai.isnan(a), startai.zeros_like(a), a)
    return startai.cumsum(a, axis=axis, dtype=dtype, out=out)


@to_startai_arrays_and_back
def nanmax(
    a,
    axis=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
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
            else:
                ax = axis % len(s)
            s[ax] = startai.array(1)
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
    return res.astype(startai.dtype(a))


@handle_jax_dtype
@to_startai_arrays_and_back
def nanmean(a, axis=None, dtype=None, out=None, keepdims=False, *, where=None):
    axis = tuple(axis) if isinstance(axis, list) else axis
    if dtype is None:
        dtype = "float64" if startai.is_int_dtype(a) else a.dtype
    if startai.is_array(where):
        where1 = startai.array(where, dtype=startai.bool)
        a = startai.where(where1, a, startai.full_like(a, startai.nan))
    nan_mask1 = startai.isnan(a)
    not_nan_mask1 = ~startai.isnan(a)
    b1 = startai.where(startai.logical_not(nan_mask1), a, startai.zeros_like(a))
    array_sum1 = startai.sum(b1, axis=axis, dtype=dtype, keepdims=keepdims, out=out)
    not_nan_mask_count1 = startai.sum(
        not_nan_mask1, axis=axis, dtype=dtype, keepdims=keepdims, out=out
    )
    count_zero_handel = startai.where(
        not_nan_mask_count1 != 0,
        not_nan_mask_count1,
        startai.full_like(not_nan_mask_count1, startai.nan),
    )
    return startai.divide(array_sum1, count_zero_handel)


@to_startai_arrays_and_back
def nanmedian(
    a,
    /,
    *,
    axis=None,
    keepdims=False,
    out=None,
    overwrite_input=False,
):
    return startai.nanmedian(
        a, axis=axis, keepdims=keepdims, out=out, overwrite_input=overwrite_input
    ).astype(a.dtype)


@to_startai_arrays_and_back
def nanmin(
    a,
    axis=None,
    out=None,
    keepdims=False,
    initial=None,
    where=True,
):
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
            else:
                ax = axis % len(s)

            s[ax] = startai.array(1)
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
    return res.astype(startai.dtype(a))


@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"0.4.14 and below": ("complex64", "complex128", "bfloat16", "bool", "float16")},
    "jax",
)
def nanpercentile(
    a, q, axis=None, out=None, overwrite_input=False, method="linear", keepdims=None
):
    def _remove_nan_1d(arr1d, overwrite_input=False):
        if arr1d.dtype == object:
            c = startai.not_equal(arr1d, arr1d)
        else:
            c = startai.isnan(arr1d)
        s = startai.nonzero(c)[0]
        if s.size == arr1d.size:
            return arr1d[:0], True
        elif s.size == 0:
            return arr1d, overwrite_input
        else:
            if not overwrite_input:
                arr1d = arr1d.copy()

                enonan = arr1d[-s.size :][~c[-s.size :]]
                arr1d[s[: enonan.size]] = enonan

                return arr1d[: -s.size], True

    def _nanquantile_1d(arr1d, q, overwrite_input=False, method="linear"):
        arr1d, overwrite_input = _remove_nan_1d(arr1d, overwrite_input=overwrite_input)
        if arr1d.size == 0:
            return startai.full(q.shape, startai.nan)
        return startai.quantile(arr1d, q, interpolation=method)

    def apply_along_axis(func1d, axis, arr, *args, **kwargs):
        ndim = startai.get_num_dims(arr)
        if axis is None:
            raise ValueError("Axis must be an integer.")
        if not -ndim <= axis < ndim:
            raise ValueError(
                f"axis {axis} is out of bounds for array of dimension {ndim}"
            )
        if axis < 0:
            axis = axis + ndim

        def func(elem):
            return func1d(elem, *args, **kwargs)

        for i in range(1, ndim - axis):
            func = startai.vmap(func, in_axes=i, out_axes=-1)
        for i in range(axis):
            func = startai.vmap(func, in_axes=0, out_axes=0)

        return startai.asarray(func(arr))

    def _nanquantile_ureduce_func(
        a, q, axis=None, out=None, overwrite_input=False, method="linear"
    ):
        if axis is None or a.ndim == 1:
            part = a.ravel()
            result = _nanquantile_1d(
                part, q, overwrite_input=overwrite_input, method=method
            )
        else:
            result = apply_along_axis(
                _nanquantile_1d, axis, a, q, overwrite_input, method
            )

            if q.ndim != 0:
                result = startai.moveaxis(result, axis, 0)

        if out is not None:
            out[...] = result

        return result

    def _ureduce(a, func, keepdims=False, **kwargs):
        axis = kwargs.get("axis", None)
        out = kwargs.get("out", None)

        if keepdims is None:
            keepdims = False

        nd = a.ndim
        if axis is not None:
            axis = startai._normalize_axis_tuple(axis, nd)

            if keepdims:
                if out is not None:
                    index_out = tuple(
                        0 if i in axis else slice(None) for i in range(nd)
                    )
                    kwargs["out"] = out[(Ellipsis,) + index_out]

            if len(axis) == 1:
                kwargs["axis"] = axis[0]
            else:
                keep = set(range(nd)) - set(axis)
                nkeep = len(keep)
                # swap axis that should not be reduced to front
                for i, s in enumerate(sorted(keep)):
                    a = a.swapaxes(i, s)
                # merge reduced axis
                a = a.reshape(a.shape[:nkeep] + (-1,))
                kwargs["axis"] = -1
        else:
            if keepdims:
                if out is not None:
                    index_out = (0,) * nd
                    kwargs["out"] = out[(Ellipsis,) + index_out]

        r = func(a, **kwargs)

        if out is not None:
            return out

        if keepdims:
            if axis is None:
                index_r = (startai.newaxis,) * nd
            else:
                index_r = tuple(
                    startai.newaxis if i in axis else slice(None) for i in range(nd)
                )
            r = r[(Ellipsis,) + index_r]

        return r

    def _nanquantile_unchecked(
        a,
        q,
        axis=None,
        out=None,
        overwrite_input=False,
        method="linear",
        keepdims=None,
    ):
        """Assumes that q is in [0, 1], and is an ndarray."""
        if a.size == 0:
            return startai.nanmean(a, axis=axis, out=out, keepdims=keepdims)
        return _ureduce(
            a,
            func=_nanquantile_ureduce_func,
            q=q,
            keepdims=keepdims,
            axis=axis,
            out=out,
            overwrite_input=overwrite_input,
            method=method,
        )

    a = startai.array(a)
    q = startai.divide(q, 100.0)
    q = startai.array(q)
    if q.ndim == 1 and q.size < 10:
        for i in range(q.size):
            if not (0.0 <= q[i] <= 1.0):
                startai.logging.warning("percentile s must be in the range [0, 100]")
                return []
    else:
        if not (startai.all(q >= 0) and startai.all(q <= 1)):
            startai.logging.warning("percentile s must be in the range [0, 100]")
            return []
    return _nanquantile_unchecked(a, q, axis, out, overwrite_input, method, keepdims)


@handle_jax_dtype
@to_startai_arrays_and_back
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


@handle_jax_dtype
@to_startai_arrays_and_back
def nanvar(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, *, where=True):
    is_nan = startai.isnan(a)
    if dtype is None:
        dtype = "float16" if startai.is_int_dtype(a) else a.dtype
    if startai.any(is_nan):
        a = [i for i in a if startai.isnan(i) is False]

    if dtype:
        a = startai.astype(startai.array(a), startai.as_startai_dtype(dtype))

    ret = startai.var(a, axis=axis, correction=ddof, keepdims=keepdims, out=out)
    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)

    all_nan = startai.isnan(ret)
    if startai.all(all_nan):
        ret = startai.astype(ret, startai.array([float("inf")]))
    return ret


@to_startai_arrays_and_back
def ptp(a, axis=None, out=None, keepdims=False):
    x = startai.max(a, axis=axis, keepdims=keepdims)
    y = startai.min(a, axis=axis, keepdims=keepdims)
    return startai.subtract(x, y)


@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"0.4.24 and below": ("complex64", "complex128", "bfloat16", "bool", "float16")},
    "jax",
)
def quantile(
    a,
    q,
    /,
    *,
    axis=None,
    out=None,
    overwrite_input=False,
    method="linear",
    keepdims=False,
    interpolation=None,
):
    if method == "nearest":
        return startai.quantile(
            a, q, axis=axis, keepdims=keepdims, interpolation="nearest_jax", out=out
        )
    return startai.quantile(
        a, q, axis=axis, keepdims=keepdims, interpolation=method, out=out
    )


@handle_jax_dtype
@with_unsupported_dtypes({"0.4.24 and below": ("bfloat16",)}, "jax")
@to_startai_arrays_and_back
def std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, *, where=None):
    axis = tuple(axis) if isinstance(axis, list) else axis
    if dtype is None:
        dtype = "float32" if startai.is_int_dtype(a) else a.dtype
    std_a = startai.std(a, axis=axis, correction=ddof, keepdims=keepdims, out=out)
    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        std_a = startai.where(
            where, std_a, startai.default(out, startai.zeros_like(std_a)), out=out
        )
    return startai.astype(std_a, startai.as_startai_dtype(dtype), copy=False)


@handle_jax_dtype
@to_startai_arrays_and_back
def sum(
    a,
    axis=None,
    dtype=None,
    out=None,
    keepdims=False,
    initial=None,
    where=None,
    promote_integers=True,
):
    # TODO: promote_integers is only supported from JAX v0.4.10
    if dtype is None and promote_integers:
        if startai.is_bool_dtype(a.dtype):
            dtype = startai.default_int_dtype()
        elif startai.is_uint_dtype(a.dtype):
            dtype = "uint64"
            a = startai.astype(a, dtype)
        elif startai.is_int_dtype(a.dtype):
            dtype = "int64"
            a = startai.astype(a, dtype)
        else:
            dtype = a.dtype
    elif dtype is None and not promote_integers:
        dtype = "float32" if startai.is_int_dtype(a.dtype) else startai.as_startai_dtype(a.dtype)

    if initial:
        if axis is None:
            a = startai.reshape(a, (1, -1))
            axis = 0
        s = list(startai.shape(a))
        s[axis] = 1
        header = startai.full(s, initial)
        a = startai.concat([a, header], axis=axis)

    ret = startai.sum(a, axis=axis, keepdims=keepdims, out=out)

    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return startai.astype(ret, startai.as_startai_dtype(dtype))


@handle_jax_dtype
@to_startai_arrays_and_back
def var(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, *, where=None):
    axis = tuple(axis) if isinstance(axis, list) else axis
    if dtype is None:
        dtype = "float32" if startai.is_int_dtype(a) else a.dtype
    ret = startai.var(a, axis=axis, correction=ddof, keepdims=keepdims, out=out)
    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return startai.astype(ret, startai.as_startai_dtype(dtype), copy=False)


amax = max
amin = min
cumproduct = cumprod
