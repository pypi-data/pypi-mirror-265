# global
import startai

# local
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_out,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_casting,
)


# --- Helpers --- #
# --------------- #


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _nextafter(
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
    return startai.nextafter(x1, x2, out=out)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _signbit(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="safe",
    order="K",
    dtype=None,
    subok=True,
):
    x = startai.astype(x, startai.float64)
    return startai.logical_or(startai.less(x, 0), startai.atan2(0.0, x) == startai.pi, out=out)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _spacing(
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
    # Implement the frontend function using Startai compositions
    if dtype is None:
        dtype = startai.dtype(x)
    y = startai.floor(startai.log2(startai.abs(x + 1)))
    spacing = startai.multiply(startai.finfo(dtype).eps, startai.pow(2, y))
    if dtype != "float16":
        spacing = startai.sign(x) * spacing
    return spacing
