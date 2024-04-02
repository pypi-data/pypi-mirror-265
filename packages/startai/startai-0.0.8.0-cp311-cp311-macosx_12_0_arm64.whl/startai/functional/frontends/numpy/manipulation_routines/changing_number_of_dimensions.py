# global
import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back


# atleast_1d
@to_startai_arrays_and_back
def atleast_1d(
    *arys,
):
    return startai.atleast_1d(*arys)


@to_startai_arrays_and_back
def atleast_2d(*arys):
    return startai.atleast_2d(*arys)


@to_startai_arrays_and_back
def atleast_3d(*arys):
    return startai.atleast_3d(*arys)


# broadcast_arrays
@to_startai_arrays_and_back
def broadcast_arrays(*args):
    return startai.broadcast_arrays(*args)


# expand_dims
@to_startai_arrays_and_back
def expand_dims(
    a,
    axis,
):
    return startai.expand_dims(a, axis=axis)


# squeeze
@to_startai_arrays_and_back
def squeeze(
    a,
    axis=None,
):
    return startai.squeeze(a, axis=axis)
