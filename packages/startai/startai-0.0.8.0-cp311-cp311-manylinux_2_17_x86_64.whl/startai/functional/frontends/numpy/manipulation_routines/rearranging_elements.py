# local
import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def flip(m, axis=None):
    return startai.flip(m, axis=axis, out=None)


@to_startai_arrays_and_back
def fliplr(m):
    return startai.fliplr(m, out=None)


@to_startai_arrays_and_back
def flipud(m):
    return startai.flipud(m, out=None)


@to_startai_arrays_and_back
def roll(a, shift, axis=None):
    return startai.roll(a, shift, axis=axis)


@to_startai_arrays_and_back
def rot90(m, k=1, axes=(0, 1)):
    return startai.rot90(m, k=k, axes=axes)
