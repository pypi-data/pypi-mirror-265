# global
import torch
from typing import Callable

# local
import startai
from startai.func_wrapper import inputs_to_native_arrays
from startai.functional.startai.gradients import (
    _flatten_containers,
    _rebuild_flattened_containers,
)


def bind_custom_gradient_function(func, custom_grad_fn):
    class _CustomModule(torch.autograd.Function):
        @staticmethod
        def forward(ctx, x):
            ret = startai.to_native(func(x), nested=True, include_derived=True)
            ctx.save_for_backward(x, ret)
            return ret

        @staticmethod
        def backward(ctx, upstream):
            grads = custom_grad_fn(
                *startai.to_startai(
                    (ctx.saved_tensors, upstream), nested=True, include_derived=True
                )
            )
            return startai.to_native(grads, nested=True, include_derived=True)

    custom_module = _CustomModule.apply
    return inputs_to_native_arrays(custom_module)


def vjp(func: Callable, *primals):
    flattened_primals, ret_idxs = _flatten_containers(primals)
    unique_keys = list(
        {
            startai.index_nest(ret_idxs, i)
            for i in startai.nested_argwhere(ret_idxs, lambda x: isinstance(x, str))
        }
    )

    def grad_fn(*x_in):
        ret, idxs = _flatten_containers(
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

        # replave the idxs with the unique keys
        func_ret_idxs = torch.tensor(
            startai.nested_map(
                lambda x: (
                    unique_keys.index(x)
                    if isinstance(x, str)
                    else -1 if x is None else x
                ),
                idxs,
            )
        )

        return (ret, func_ret_idxs)

    primals_out, _vjpfun, func_ret_idxs = startai.outputs_to_startai_arrays(torch.func.vjp)(
        grad_fn, *startai.to_native(flattened_primals, nested=True), has_aux=True
    )

    func_ret_idxs = startai.nested_map(
        lambda x: unique_keys[x] if x >= 0 and x < len(unique_keys) else None,
        func_ret_idxs.tolist(),
    )
    primals_out = _rebuild_flattened_containers(primals_out, func_ret_idxs)

    def vjpfun(*x_in):
        startai.assertions.check_isinstance(x_in, tuple)
        return _rebuild_flattened_containers(
            startai.to_startai(
                _vjpfun(startai.to_native(_flatten_containers(x_in)[0], nested=True)),
                nested=True,
                include_derived=True,
            ),
            ret_idxs,
        )

    return (primals_out, vjpfun)


def jvp(func: Callable, primals, tangents):
    flattened_primals, ret_idxs = _flatten_containers(primals)
    flattened_tangents, _ = _flatten_containers(tangents)
    unique_keys = list(
        {
            startai.index_nest(ret_idxs, i)
            for i in startai.nested_argwhere(ret_idxs, lambda x: isinstance(x, str))
        }
    )

    def grad_fn(*x_in):
        ret, idxs = _flatten_containers(
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

        # replave the idxs with the unique keys
        func_ret_idxs = torch.tensor(
            startai.nested_map(
                lambda x: (
                    unique_keys.index(x)
                    if isinstance(x, str)
                    else -1 if x is None else x
                ),
                idxs,
            )
        )

        return (ret, func_ret_idxs)

    primals_out, tangents_out, func_ret_idxs = startai.outputs_to_startai_arrays(
        torch.func.jvp
    )(
        grad_fn,
        startai.to_native(flattened_primals, nested=True),
        startai.to_native(flattened_tangents, nested=True),
        has_aux=True,
    )

    func_ret_idxs = startai.nested_map(
        lambda x: unique_keys[x] if x >= 0 and x < len(unique_keys) else None,
        func_ret_idxs.tolist(),
    )

    primals_out = _rebuild_flattened_containers(primals_out, func_ret_idxs)
    tangents_out = _rebuild_flattened_containers(tangents_out, func_ret_idxs)

    return (primals_out, tangents_out)
