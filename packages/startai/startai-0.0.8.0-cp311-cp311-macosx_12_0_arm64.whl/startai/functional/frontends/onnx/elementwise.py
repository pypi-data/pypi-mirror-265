import startai

from startai.functional.frontends.onnx.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def Abs(input):
    return startai.abs(input)


@to_startai_arrays_and_back
def Acos(input):
    return startai.acos(input)


@to_startai_arrays_and_back
def Acosh(input):
    return startai.acosh(input)


@to_startai_arrays_and_back
def Add(x1, x2):
    return startai.add(x1, x2)


@to_startai_arrays_and_back
def Asin(input):
    return startai.asin(input)
