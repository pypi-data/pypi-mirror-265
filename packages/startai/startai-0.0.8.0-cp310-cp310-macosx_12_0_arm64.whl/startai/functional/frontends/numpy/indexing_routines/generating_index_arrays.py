import inspect

import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
)


@to_startai_arrays_and_back
def diag_indices(n, ndim=2):
    idx = startai.arange(n)
    res = startai.array((idx,) * ndim)
    res = tuple(res.astype("int64"))
    return res


@to_startai_arrays_and_back
def indices(dimensions, dtype=int, sparse=False):
    return startai.indices(dimensions, dtype=dtype, sparse=sparse)


@to_startai_arrays_and_back
def mask_indices(n, mask_func, k=0):
    mask_func_obj = inspect.unwrap(mask_func)
    mask_func_name = mask_func_obj.__name__
    try:
        startai_mask_func_obj = getattr(startai.functional.frontends.numpy, mask_func_name)
        a = startai.ones((n, n))
        mask = startai_mask_func_obj(a, k=k)
        indices = startai.argwhere(mask.startai_array)
        ret = indices[:, 0], indices[:, 1]
        return tuple(ret)
    except AttributeError as e:
        print(f"Attribute error: {e}")


@to_startai_arrays_and_back
def tril_indices(n, k=0, m=None):
    return startai.tril_indices(n, m, k)


@to_startai_arrays_and_back
def tril_indices_from(arr, k=0):
    return startai.tril_indices(arr.shape[0], arr.shape[1], k)


# unravel_index
@to_startai_arrays_and_back
def unravel_index(indices, shape, order="C"):
    ret = [x.astype("int64") for x in startai.unravel_index(indices, shape)]
    return tuple(ret)
