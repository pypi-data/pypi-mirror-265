# global
import startai

# local
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_casting,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)


from startai.func_wrapper import with_supported_dtypes, with_unsupported_dtypes


# --- Helpers --- #
# --------------- #


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _absolute(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.abs(x)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _cbrt(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    all_positive = startai.pow(startai.abs(x), 1.0 / 3.0)
    ret = startai.where(startai.less(x, 0.0), startai.negative(all_positive), all_positive)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _clip(
    a,
    a_min,
    a_max,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    startai.utils.assertions.check_all_or_any_fn(
        a_min,
        a_max,
        fn=startai.exists,
        type="any",
        limit=[1, 2],
        message="at most one of a_min and a_max can be None",
    )
    if a_min is None:
        ret = startai.minimum(a, a_max, out=out)
    elif a_max is None:
        ret = startai.maximum(a, a_min, out=out)
    else:
        ret = startai.clip(a, a_min, a_max, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _copysign(
    x1,
    x2,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="k",
    dtype=None,
    subok=True,
):
    ret = startai.copysign(x1, x2, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _fabs(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.abs(x)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
@with_supported_dtypes(
    {"1.26.3 and below": ("int8", "int16", "int32", "int64")}, "numpy"
)  # Add
def _gcd(
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
    ret = startai.gcd(x1, x2, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _heaviside(
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
    ret = startai.heaviside(x1, x2, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def _lcm(
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
    ret = startai.lcm(x1, x2, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _reciprocal(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.reciprocal(x)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _sign(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.sign(x, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _sqrt(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.sqrt(x)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _square(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    ret = startai.square(x)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def convolve(a, v, mode="full"):
    if a.ndim != 1 or v.ndim != 1:
        raise ValueError("convolve() only support 1-dimensional inputs.")
    if a.shape[0] < v.shape[0]:
        a, v = v, a
    v = startai.flip(v)

    out_order = slice(None)

    if mode == "valid":
        padding = [(0, 0)]
    elif mode == "same":
        padding = [(v.shape[0] // 2, v.shape[0] - v.shape[0] // 2 - 1)]
    elif mode == "full":
        padding = [(v.shape[0] - 1, v.shape[0] - 1)]

    result = startai.conv_general_dilated(
        a[None, None, :],
        v[:, None, None],
        (1,),
        padding,
        dims=1,
        data_format="channel_first",
    )
    return result[0, 0, out_order]


@with_unsupported_dtypes({"2.0.1 and below": ("bfloat16",)}, "numpy")
@to_startai_arrays_and_back
def gradient(f, *varargs, axis=None, edge_order=None):
    edge_order = edge_order if edge_order is not None else 1
    return startai.gradient(f, spacing=varargs, axis=axis, edge_order=edge_order)


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def interp(x, xp, fp, left=None, right=None, period=None):
    return startai.interp(x, xp, fp, left=left, right=right, period=period)


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nan_to_num(x, copy=True, nan=0.0, posinf=None, neginf=None):
    bounds = startai.finfo(x.dtype)
    if posinf is None:
        posinf = bounds.max
    if neginf is None:
        neginf = bounds.min
    pos_where = startai.isinf(x, detect_negative=False)
    neg_where = startai.isinf(x, detect_positive=False)
    nan_where = startai.isnan(x)
    ret = startai.where(nan_where, nan, x)
    ret = startai.where(pos_where, posinf, ret)
    ret = startai.where(neg_where, neginf, ret)
    ret = ret.astype(x.dtype, copy=False)
    if not copy:
        return startai.inplace_update(x, ret)
    return ret


@to_startai_arrays_and_back
def real_if_close(a, tol=100):
    a = startai.array(a, dtype=a.dtype)
    dtype_ = a.dtype

    if not startai.is_complex_dtype(dtype_):
        return a

    if tol > 1:
        f = startai.finfo(dtype_)
        tol = f.eps * tol

    if startai.all(startai.abs(startai.imag(a)) < tol):
        a = startai.real(a)

    return a
