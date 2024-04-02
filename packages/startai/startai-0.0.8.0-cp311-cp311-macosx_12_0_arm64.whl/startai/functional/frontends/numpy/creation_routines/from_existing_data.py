import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_dtype,
)


@handle_numpy_dtype
@to_startai_arrays_and_back
def array(object, dtype=None, *, copy=True, order="K", subok=False, ndmin=0, like=None):
    ret = startai.array(object, copy=copy, dtype=dtype)
    if startai.get_num_dims(ret) < ndmin:
        ret = startai.expand_dims(ret, axis=list(range(ndmin - startai.get_num_dims(ret))))
    return ret


@handle_numpy_dtype
@to_startai_arrays_and_back
def asarray(
    a,
    dtype=None,
    order=None,
    *,
    like=None,
):
    return startai.asarray(a, dtype=dtype)


@to_startai_arrays_and_back
def copy(a, order="K", subok=False):
    return startai.copy_array(a)


@handle_numpy_dtype
def frombuffer(buffer, dtype=float, count=-1, offset=0, *, like=None):
    return startai.frombuffer(buffer)
