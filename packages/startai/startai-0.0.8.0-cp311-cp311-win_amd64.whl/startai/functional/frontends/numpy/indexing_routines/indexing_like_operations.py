import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    inputs_to_startai_arrays,
    handle_numpy_out,
)


@to_startai_arrays_and_back
@handle_numpy_out
def compress(condition, a, axis=None, out=None):
    condition_arr = startai.asarray(condition).astype(bool)
    if condition_arr.ndim != 1:
        raise startai.utils.exceptions.StartaiException("Condition must be a 1D array")
    if axis is None:
        arr = startai.asarray(a).flatten()
        axis = 0
    else:
        arr = startai.moveaxis(a, axis, 0)
    if condition_arr.shape[0] > arr.shape[0]:
        raise startai.utils.exceptions.StartaiException(
            "Condition contains entries that are out of bounds"
        )
    arr = arr[: condition_arr.shape[0]]
    return startai.moveaxis(arr[condition_arr], 0, axis)


def diag(v, k=0):
    return startai.diag(v, k=k)


@to_startai_arrays_and_back
def diagonal(a, offset, axis1, axis2):
    return startai.diagonal(a, offset=offset, axis1=axis1, axis2=axis2)


@to_startai_arrays_and_back
def fill_diagonal(a, val, wrap=False):
    if a.ndim < 2:
        raise ValueError("array must be at least 2-d")
    end = None
    if a.ndim == 2:
        # Explicit, fast formula for the common case.  For 2-d arrays, we
        # accept rectangular ones.
        step = a.shape[1] + 1
        # This is needed to don't have tall matrix have the diagonal wrap.
        if not wrap:
            end = a.shape[1] * a.shape[1]
    else:
        # For more than d=2, the strided formula is only valid for arrays with
        # all dimensions equal, so we check first.
        if not startai.all(startai.diff(a.shape) == 0):
            raise ValueError("All dimensions of input must be of equal length")
        step = 1 + startai.sum(startai.cumprod(a.shape[:-1]))

    # Write the value out into the diagonal.
    shape = a.shape
    a = startai.reshape(a, a.size)
    a[:end:step] = val
    a = startai.reshape(a, shape)


@to_startai_arrays_and_back
def indices(dimensions, dtype=int, sparse=False):
    dimensions = tuple(dimensions)
    N = len(dimensions)
    shape = (1,) * N
    if sparse:
        res = ()
    else:
        res = startai.empty((N,) + dimensions, dtype=dtype)
    for i, dim in enumerate(dimensions):
        idx = startai.arange(dim, dtype=dtype).reshape(shape[:i] + (dim,) + shape[i + 1 :])
        if sparse:
            res = res + (idx,)
        else:
            res[i] = idx
    return res


@inputs_to_startai_arrays
def put_along_axis(arr, indices, values, axis):
    startai.put_along_axis(arr, indices, values, axis)


@to_startai_arrays_and_back
@handle_numpy_out
def take(a, indices, /, *, axis=None, out=None, mode="raise"):
    return startai.take(a, indices, axis=axis, out=out, mode=mode)


@to_startai_arrays_and_back
def take_along_axis(arr, indices, axis):
    return startai.take_along_axis(arr, indices, axis)


@to_startai_arrays_and_back
def tril_indices(n, k=0, m=None):
    return startai.tril_indices(n, m, k)


# unravel_index
@to_startai_arrays_and_back
def unravel_index(indices, shape, order="C"):
    ret = [x.astype("int64") for x in startai.unravel_index(indices, shape)]
    return tuple(ret)
