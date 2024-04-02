import startai
from startai.functional.frontends.mxnet.func_wrapper import to_startai_arrays_and_back
from startai.functional.frontends.numpy.func_wrapper import handle_numpy_dtype


@handle_numpy_dtype
@to_startai_arrays_and_back
def softmax(data, length=None, axis=-1, temperature=None, use_length=False, dtype=None):
    ret = startai.softmax(data, axis=axis)
    if dtype:
        startai.utils.assertions.check_elem_in_list(
            dtype, ["float16", "float32", "float64"]
        )
        ret = startai.astype(ret, dtype)
    return ret
