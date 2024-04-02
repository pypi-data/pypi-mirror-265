import startai
from startai.functional.frontends.jax.func_wrapper import (
    to_startai_arrays_and_back,
    outputs_to_native_arrays,
)
from startai.func_wrapper import outputs_to_startai_arrays


@to_startai_arrays_and_back
def device_get(x):
    if startai.dev(x) != "cpu":
        x = startai.to_device(x, "cpu")
    return x


@to_startai_arrays_and_back
def device_put(x, device=None, *, src=None):
    if device is not None:
        cur_dev = startai.dev(x)
        device = startai.as_startai_dev(device)
        if cur_dev != device:
            x = startai.to_device(x, device)
    return x


def vmap(
    fun, in_axes=0, out_axes=0, axis_name=None, axis_size=None, spmd_axis_name=None
):
    fun = outputs_to_native_arrays(fun)
    return to_startai_arrays_and_back(
        outputs_to_startai_arrays(startai.vmap(fun, in_axes=in_axes, out_axes=out_axes))
    )
