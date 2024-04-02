# global
import startai

# local
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    inputs_to_startai_arrays,
    handle_numpy_casting,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)


# --- Helpers --- #
# --------------- #


@handle_numpy_out
@to_startai_arrays_and_back
@handle_numpy_dtype
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _equal(
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
    ret = startai.equal(x1, x2, out=out)
    if startai.is_array(where):
        where = startai.asarray(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@handle_numpy_dtype
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _greater(
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
    ret = startai.greater(x1, x2, out=out)
    if startai.is_array(where):
        where = startai.asarray(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@handle_numpy_dtype
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _greater_equal(
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
    ret = startai.greater_equal(x1, x2, out=out)
    if startai.is_array(where):
        where = startai.asarray(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@handle_numpy_dtype
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _less(
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
    ret = startai.less(x1, x2, out=out)
    if startai.is_array(where):
        where = startai.asarray(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@handle_numpy_dtype
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _less_equal(
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
    ret = startai.less_equal(x1, x2, out=out)
    if startai.is_array(where):
        where = startai.asarray(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


@handle_numpy_out
@to_startai_arrays_and_back
@handle_numpy_dtype
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _not_equal(
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
    ret = startai.not_equal(x1, x2, out=out)
    if startai.is_array(where):
        where = startai.asarray(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def array_equal(a1, a2, equal_nan=False):
    if not equal_nan:
        return startai.array(startai.array_equal(a1, a2))
    a1nan, a2nan = startai.isnan(a1), startai.isnan(a2)

    if not (a1nan == a2nan).all():
        return False
    return startai.array(startai.array_equal(a1 * ~a1nan, a2 * ~a2nan))


@inputs_to_startai_arrays
@from_zero_dim_arrays_to_scalar
def array_equiv(a1, a2):
    if len(startai.shape(a1)) < len(startai.shape(a2)):
        a1 = startai.broadcast_to(a1, startai.shape(a2))
    else:
        a2 = startai.broadcast_to(a2, startai.shape(a1))
    return startai.array_equal(a1, a2)
