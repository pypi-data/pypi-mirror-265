# global
import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    from_zero_dim_arrays_to_scalar,
)


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def count_nonzero(a, axis=None, *, keepdims=False):
    x = startai.array(a)
    zero = startai.zeros(startai.shape(x), dtype=x.dtype)
    return startai.sum(
        startai.astype(startai.not_equal(x, zero), startai.int64),
        axis=axis,
        keepdims=keepdims,
    )
