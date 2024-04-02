# global
import startai

# local
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    from_zero_dim_arrays_to_scalar,
)


@to_startai_arrays_and_back
def sinc(x):
    if startai.get_num_dims(x) == 0:
        x = startai.astype(x, startai.float64)
    return startai.sinc(x)


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def unwrap(p, discont=None, axis=-1, *, period=2 * startai.pi):
    p = startai.asarray(p)
    nd = p.ndim
    dd = startai.diff(p, axis=axis)
    if discont is None:
        discont = period / 2
    slice1 = [slice(None, None)] * nd  # full slices
    slice1[axis] = startai.slice(1, None)
    slice1 = startai.tuple(slice1)
    dtype = startai.result_type(dd, period)
    if startai.issubdtype(dtype, startai.integer):
        interval_high, rem = startai.divmod(period, 2)
        boundary_ambiguous = rem == 0
    else:
        interval_high = period / 2
        boundary_ambiguous = True
    interval_low = -interval_high
    ddmod = startai.mod(dd - interval_low, period) + interval_low
    if boundary_ambiguous:
        startai.copyto(ddmod, interval_high, where=(ddmod == interval_low) & (dd > 0))
    ph_correct = ddmod - dd
    startai.copyto(ph_correct, 0, where=startai.abs(dd) < discont)
    up = startai.array(p, copy=True, dtype=dtype)
    up[slice1] = p[slice1] + ph_correct.cumsum(axis)
    return up
