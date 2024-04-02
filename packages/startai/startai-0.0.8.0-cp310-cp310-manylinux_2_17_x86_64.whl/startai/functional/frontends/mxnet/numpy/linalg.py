import startai
from startai.functional.frontends.mxnet.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def tensordot(a, b, axes=2):
    return startai.tensordot(a, b, axes=axes)
