import startai

from startai.functional.frontends.onnx.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def MatMul(x1, x2):
    return startai.matmul(x1, x2)
