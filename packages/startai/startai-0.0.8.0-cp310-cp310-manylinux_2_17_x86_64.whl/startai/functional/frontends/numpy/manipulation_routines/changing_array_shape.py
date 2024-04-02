# local
import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
)


@to_startai_arrays_and_back
def asanyarray(a, dtype=None, order=None, like=None):
    return startai.asarray(a)


@to_startai_arrays_and_back
def asarray_chkfinite(a, dtype=None, order=None):
    a = startai.asarray(a, dtype=dtype)
    if not startai.all(startai.isfinite(a)):
        raise ValueError("array must not contain infs or NaNs")
    return a


@to_startai_arrays_and_back
def asfarray(a, dtype=startai.float64):
    return startai.asarray(a, dtype=startai.float64)


@to_startai_arrays_and_back
def broadcast_to(array, shape, subok=False):
    return startai.broadcast_to(array, shape)


@to_startai_arrays_and_back
def moveaxis(a, source, destination):
    return startai.moveaxis(a, source, destination)


@to_startai_arrays_and_back
def ravel(a, order="C"):
    return startai.reshape(a, shape=(-1,), order=order)


@to_startai_arrays_and_back
def require(a, dtype=None, requirements=None, *, like=None):
    return startai.asarray(a, dtype=dtype)


@to_startai_arrays_and_back
def reshape(x, /, newshape, order="C"):
    return startai.reshape(x, shape=newshape, order=order)


@to_startai_arrays_and_back
def resize(x, newshape, /, refcheck=True):
    if isinstance(newshape, int):
        newshape = (newshape,)
    x_new = startai.reshape(x, shape=(-1,), order="C")
    total_size = 1
    for diff_size in newshape:
        total_size *= diff_size
        if diff_size < 0:
            raise ValueError("values must not be negative")
    if x_new.size == 0 or total_size == 0:
        return startai.zeros_like(x_new)
    repetition = -(-total_size // len(x_new))
    conc = (x_new,) * repetition
    x_new = startai.concat(conc)[:total_size]
    y = startai.reshape(x_new, shape=newshape, order="C")
    return y
