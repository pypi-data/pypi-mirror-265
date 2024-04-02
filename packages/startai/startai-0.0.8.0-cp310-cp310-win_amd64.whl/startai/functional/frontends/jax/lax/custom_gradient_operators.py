import startai
from startai.functional.frontends.jax.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def stop_gradient(x):
    return startai.stop_gradient(x)
