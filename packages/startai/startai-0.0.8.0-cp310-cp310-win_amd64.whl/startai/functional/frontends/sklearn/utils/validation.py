import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back
from startai.func_wrapper import with_unsupported_dtypes


@to_startai_arrays_and_back
def as_float_array(X, *, copy=True, force_all_finite=True):
    if X.dtype in [startai.float32, startai.float64]:
        return X.copy_array() if copy else X
    if ("bool" in X.dtype or "int" in X.dtype or "uint" in X.dtype) and startai.itemsize(
        X
    ) <= 4:
        return_dtype = startai.float32
    else:
        return_dtype = startai.float64
    return startai.asarray(X, dtype=return_dtype)


@with_unsupported_dtypes({"1.3.0 and below": ("complex",)}, "sklearn")
@to_startai_arrays_and_back
def column_or_1d(y, *, warn=False):
    shape = y.shape
    if len(shape) == 2 and shape[1] == 1:
        y = startai.reshape(y, (-1,))
    elif len(shape) > 2:
        raise ValueError("y should be a 1d array or a column vector")
    return y
