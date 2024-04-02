# local

import startai

from startai.functional.frontends.numpy import promote_types_of_numpy_inputs

from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)


# --- Helpers --- #
# --------------- #


# nanargmin and nanargmax composition helper
def _nanargminmax(a, axis=None):
    # check nans
    nans = startai.isnan(a).astype(startai.bool)
    # replace nans with inf
    a = startai.where(nans, startai.inf, a)
    if nans is not None:
        nans = startai.all(nans, axis=axis)
        if startai.any(nans):
            raise startai.utils.exceptions.StartaiError("All-NaN slice encountered")
    return a


# --- Main --- #
# ------------ #


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def argmax(
    a,
    /,
    *,
    axis=None,
    out=None,
    keepdims=False,
):
    return startai.argmax(a, axis=axis, out=out, keepdims=keepdims)


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def argmin(a, /, *, axis=None, keepdims=False, out=None):
    return startai.argmin(a, axis=axis, out=out, keepdims=keepdims)


@to_startai_arrays_and_back
def argwhere(a):
    return startai.argwhere(a)


@to_startai_arrays_and_back
def extract(cond, arr, /):
    if cond.dtype == "bool":
        return arr[cond]
    else:
        return arr[cond != 0]


@to_startai_arrays_and_back
def flatnonzero(a):
    return startai.nonzero(startai.reshape(a, (-1,)))


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nanargmax(a, /, *, axis=None, out=None, keepdims=False):
    a = _nanargminmax(a, axis=axis)
    return startai.argmax(a, axis=axis, keepdims=keepdims, out=out)


@handle_numpy_out
@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def nanargmin(a, /, *, axis=None, out=None, keepdims=False):
    a = _nanargminmax(a, axis=axis)
    return startai.argmin(a, axis=axis, keepdims=keepdims, out=out)


@to_startai_arrays_and_back
def nonzero(a):
    return startai.nonzero(a)


@to_startai_arrays_and_back
def searchsorted(a, v, side="left", sorter=None):
    return startai.searchsorted(a, v, side=side, sorter=sorter)


@to_startai_arrays_and_back
def where(cond, x1=None, x2=None, /):
    if x1 is None and x2 is None:
        # numpy where behaves as np.asarray(condition).nonzero() when x and y
        # not included
        return startai.asarray(cond).nonzero()
    elif x1 is not None and x2 is not None:
        x1, x2 = promote_types_of_numpy_inputs(x1, x2)
        return startai.where(cond, x1, x2)
    else:
        raise startai.utils.exceptions.StartaiException("where takes either 1 or 3 arguments")
