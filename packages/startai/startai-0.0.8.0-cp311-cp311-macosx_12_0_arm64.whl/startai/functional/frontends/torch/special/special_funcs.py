import startai
from startai.func_wrapper import (
    with_unsupported_dtypes,
)
from startai.functional.frontends.torch.func_wrapper import (
    to_startai_arrays_and_back,
)


@with_unsupported_dtypes({"2.2 and below": ("float16", "complex")}, "torch")
@to_startai_arrays_and_back
def erfc(input, *, out=None):
    return 1.0 - startai.erf(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16", "complex", "bfloat16")}, "torch")
@to_startai_arrays_and_back
def erfcx(input, *, out=None):
    ret = erfc(input) * startai.exp(input**2)
    return ret


@to_startai_arrays_and_back
def erfinv(input, *, out=None):
    return startai.erfinv(input, out=out)
