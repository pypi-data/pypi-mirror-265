# local
import startai
from startai.func_wrapper import with_unsupported_dtypes
from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def linear(input, weight, bias=None):
    return startai.linear(input, weight, bias=bias)
