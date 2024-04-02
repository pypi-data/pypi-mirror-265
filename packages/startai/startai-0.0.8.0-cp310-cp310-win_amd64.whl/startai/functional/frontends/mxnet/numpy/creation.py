import startai
from startai.functional.frontends.mxnet.func_wrapper import (
    to_startai_arrays_and_back,
)
from startai.functional.frontends.numpy.func_wrapper import handle_numpy_dtype


@handle_numpy_dtype
@to_startai_arrays_and_back
def array(object, dtype=None, ctx=None):
    if not startai.is_array(object) and not dtype:
        return startai.array(object, dtype="float32", device=ctx)
    return startai.array(object, dtype=dtype, device=ctx)
