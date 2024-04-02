# global
import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_out,
    handle_numpy_dtype,
    handle_numpy_casting,
    from_zero_dim_arrays_to_scalar,
)


# --- Helpers --- #
# --------------- #


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _conj(
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
    ret = startai.conj(x, out=out)
    if startai.is_array(where):
        ret = startai.where(where, ret, startai.default(out, startai.zeros_like(ret)), out=out)
    return ret


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def angle(z, deg=False):
    angle = startai.angle(z, deg=deg)
    if deg and len(z.shape) == 0:
        angle = startai.astype(angle, startai.float64)
    return angle


@to_startai_arrays_and_back
def imag(val):
    return startai.imag(val)


@to_startai_arrays_and_back
def real(val):
    return startai.real(val)
