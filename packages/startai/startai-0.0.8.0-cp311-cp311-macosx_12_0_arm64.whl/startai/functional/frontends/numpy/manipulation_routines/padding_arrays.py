# local
import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
)


@to_startai_arrays_and_back
def pad(array, pad_width, mode="constant", **kwargs):
    return startai.pad(array, pad_width, mode=mode, **kwargs)
