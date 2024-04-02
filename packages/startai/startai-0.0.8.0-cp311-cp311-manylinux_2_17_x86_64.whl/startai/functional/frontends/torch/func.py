import startai
from startai.functional.frontends.torch.func_wrapper import (
    to_startai_arrays_and_back,
    outputs_to_native_arrays,
)
from startai.func_wrapper import outputs_to_startai_arrays


def vmap(func, in_dims=0, out_dims=0, randomness="error", *, chunk_size=None):
    fun = outputs_to_native_arrays(func)
    return to_startai_arrays_and_back(
        outputs_to_startai_arrays(startai.vmap(fun, in_axes=in_dims, out_axes=out_dims))
    )
