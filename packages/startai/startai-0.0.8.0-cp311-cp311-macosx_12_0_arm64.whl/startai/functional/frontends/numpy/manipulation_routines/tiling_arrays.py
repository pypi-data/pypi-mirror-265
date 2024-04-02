# local
import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def repeat(a, repeats, axis=None):
    return startai.repeat(a, repeats, axis=axis)


@to_startai_arrays_and_back
def tile(A, reps):
    return startai.tile(A, reps)
