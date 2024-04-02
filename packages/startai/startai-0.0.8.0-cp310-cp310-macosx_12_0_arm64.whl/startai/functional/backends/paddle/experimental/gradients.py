# global
from typing import Callable
import paddle

# local
import startai
from startai.func_wrapper import inputs_to_native_arrays
from startai.functional.startai.gradients import (
    _flatten_containers,
    _rebuild_flattened_containers,
)
from startai.utils.exceptions import StartaiNotImplementedException


def bind_custom_gradient_function(func, custom_grad_fn):
    class _CustomModule(paddle.autograd.PyLayer):
        @staticmethod
        def forward(ctx, x):
            ret = startai.to_native(func(x), nested=True, include_derived=True)
            ctx.save_for_backward(x, ret)
            return ret

        @staticmethod
        def backward(ctx, upstream):
            grads = custom_grad_fn(
                *startai.to_startai(
                    (ctx.saved_tensor(), upstream), nested=True, include_derived=True
                )
            )
            return startai.to_native(grads, nested=True, include_derived=True)

    custom_module = _CustomModule.apply
    return inputs_to_native_arrays(custom_module)


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
        )[0]

    # primals_out = _rebuild_flattened_containers(
    #     grad_fn(*startai.to_startai(flattened_primals, nested=True)), ret_idxs
    # )
    primals_out = func(*startai.to_startai(primals, nested=True))

    def vjpfun(x_in):
        _, vjp_result = startai.to_startai(
            paddle.incubate.autograd.vjp(
                grad_fn,
                startai.to_native(flattened_primals, nested=True),
                startai.to_native(_flatten_containers(x_in)[0], nested=True),
            )
        )
        return startai.to_startai(
            _rebuild_flattened_containers(vjp_result, ret_idxs),
            nested=True,
            include_derived=True,
        )

    return (startai.to_startai(primals_out, nested=True, include_derived=True), vjpfun)


def jvp(func: Callable, primals, tangents):
    raise StartaiNotImplementedException()
