# global
from typing import Callable
import mxnet as mx

# local
import startai
from startai.functional.startai.gradients import (
    _flatten_containers,
    _rebuild_flattened_containers,
)
from startai.utils.exceptions import StartaiNotImplementedException


def bind_custom_gradient_function(func, custom_grad_fn):
    raise StartaiNotImplementedException()


def vjp(func: Callable, *primals):
    flattened_primals, ret_idxs = _flatten_containers(primals)

    def grad_fn(*x_in):
        return _flatten_containers(
            startai.to_native(
                func(
                    *startai.to_startai(
                        _rebuild_flattened_containers(x_in, ret_idxs), nested=True
                    )
                ),
                nested=True,
                include_derived=True,
            )
        )

    with mx.autograd.record():
        flat_primals_out, func_ret_idxs = grad_fn(
            *startai.to_native(flattened_primals, nested=True)
        )

    primals_out = _rebuild_flattened_containers(flat_primals_out, func_ret_idxs)

    def vjpfun(x_in):
        grads = mx.autograd.grad(
            flat_primals_out,
            startai.to_native(flattened_primals, nested=True),
            head_grads=startai.to_native(_flatten_containers(x_in)[0], nested=True),
        )

        return _rebuild_flattened_containers(
            startai.to_startai(grads, nested=True, include_derived=True), ret_idxs
        )

    return (startai.to_startai(primals_out, nested=True, include_derived=True), vjpfun)


def jvp(func: Callable, primals, tangents):
    raise StartaiNotImplementedException()
