import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back
from startai.func_wrapper import with_supported_dtypes


@with_supported_dtypes({"1.26.3 and below": ("int64",)}, "numpy")
@to_startai_arrays_and_back
def bincount(x, /, weights=None, minlength=0):
    return startai.bincount(x, weights=weights, minlength=minlength)
