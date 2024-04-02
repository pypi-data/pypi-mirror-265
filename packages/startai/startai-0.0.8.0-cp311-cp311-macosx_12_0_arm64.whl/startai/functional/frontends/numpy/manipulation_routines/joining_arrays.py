# local
import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_casting,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)
import startai.functional.frontends.numpy as np_frontend


@to_startai_arrays_and_back
def column_stack(tup):
    out_dtype = startai.dtype(tup[0])
    for i in tup:
        out_dtype = startai.as_startai_dtype(
            np_frontend.promote_numpy_dtypes(i.dtype, out_dtype)
        )
    return startai.column_stack(tup)


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def concatenate(arrays, /, *, axis=0, out=None, dtype=None, casting="same_kind"):
    if dtype is not None:
        out_dtype = startai.as_startai_dtype(dtype)
    else:
        out_dtype = startai.dtype(arrays[0])
        for i in arrays:
            out_dtype = startai.as_startai_dtype(
                np_frontend.promote_numpy_dtypes(i.dtype, out_dtype)
            )
    return startai.concat(arrays, axis=axis, out=out).astype(out_dtype, copy=False)


@to_startai_arrays_and_back
def hstack(tup):
    out_dtype = startai.dtype(tup[0])
    for i in tup:
        out_dtype = startai.as_startai_dtype(
            np_frontend.promote_numpy_dtypes(i.dtype, out_dtype)
        )
    return startai.hstack(tup)


@handle_numpy_out
@to_startai_arrays_and_back
def stack(arrays, /, *, axis=0, out=None):
    out_dtype = startai.dtype(arrays[0])
    for i in arrays:
        out_dtype = startai.as_startai_dtype(
            np_frontend.promote_numpy_dtypes(i.dtype, out_dtype)
        )
    return startai.stack(arrays, axis=axis, out=out).astype(out_dtype, copy=False)


@to_startai_arrays_and_back
def vstack(tup):
    out_dtype = startai.dtype(tup[0])
    for i in tup:
        out_dtype = startai.as_startai_dtype(
            np_frontend.promote_numpy_dtypes(i.dtype, out_dtype)
        )
    return startai.vstack(tup)


row_stack = vstack
