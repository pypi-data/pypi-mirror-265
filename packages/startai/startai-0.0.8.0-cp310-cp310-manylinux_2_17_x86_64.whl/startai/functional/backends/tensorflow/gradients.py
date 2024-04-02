"""Tensorflow gradient functions.

Collection of TensorFlow gradient functions, wrapped to fit Startai syntax
and signature.
"""

# global
import tensorflow as tf
from typing import Sequence, Union, Optional, Callable

# local
import startai
from startai.func_wrapper import outputs_to_startai_arrays, inputs_to_native_arrays
from startai.functional.startai.gradients import (
    _get_required_float_variables,
    _get_y_and_ret_idxs,
    _get_native_y,
    _set_duplicates,
    _process_func_ret_and_grads,
)


def variable(x, /):
    with tf.device(startai.dev(x, as_native=True)):
        return tf.Variable(x, trainable=True)


def is_variable(x, /, *, exclusive=False):
    return isinstance(x, tf.Variable)


def variable_data(x: tf.Variable, /) -> tf.Variable:
    return x.value()


def _grad_func(y, xs, xs_required, tape):
    """Gradient calculation function."""
    # Creating a zero gradient nest for the case where no gradients are computed
    grads_ = startai.nested_map(
        lambda x: startai.to_native(startai.zeros_like(x)),
        xs_required,
        include_derived=True,
        shallow=False,
    )

    # Gradient calculation
    grads = tape.gradient(y, xs_required)

    # Returning zeros if no gradients are computed for consistent results
    if isinstance(xs, startai.NativeArray):
        grads = grads_ if grads is None else grads
    else:
        grads = startai.nested_map(
            lambda x: 0 if x is None else x,
            grads,
            include_derived=True,
        )
        if isinstance(grads, startai.Container):
            grads += grads_
        else:
            grads = startai.nested_multi_map(lambda x, _: (x[0] + x[1]), [grads, grads_])
    return grads


def execute_with_gradients(
    func,
    xs: Union[tf.Tensor, tf.Variable],
    /,
    *,
    retain_grads: bool = False,
    xs_grad_idxs: Sequence[Sequence[Union[str, int]]] = ((0,),),
    ret_grad_idxs: Sequence[Sequence[Union[str, int]]] = ((0,),),
):
    # Conversion of required arrays to float variables and duplicate index chains
    xs, xs_grad_idxs, xs_required, required_duplicate_index_chains, _ = (
        _get_required_float_variables(xs, xs_grad_idxs)
    )

    # Creating a tape to record operations
    with tf.GradientTape(persistent=True, watch_accessed_variables=False) as tape:
        tape.watch(xs_required)
        func_ret = func(xs)

    # Getting the relevant outputs from the function return for gradient calculation
    ret_grad_idxs, y, ret_idxs = _get_y_and_ret_idxs(
        func_ret, ret_grad_idxs, reshape=False
    )

    if isinstance(y, startai.NativeArray):
        # Gradient calculation for a single output
        grads = _set_duplicates(
            startai.to_startai(_grad_func(y, xs, xs_required, tape)),
            required_duplicate_index_chains,
        )
    else:
        # Gradient calculation for multiple outputs
        y = _get_native_y(y)
        grads_ = startai.nested_map(
            lambda x: _grad_func(x, xs, xs_required, tape),
            y,
            include_derived=True,
            shallow=False,
        )
        grads = grads_
        if isinstance(ret_idxs, list) and len(ret_idxs):
            grads = {
                ret_idxs[i]: _set_duplicates(grad, required_duplicate_index_chains)
                for i, grad in enumerate(grads_)
            }

    # Deleting the tape if not retaining gradients
    if not retain_grads:
        del tape

    # Stop further gradient propagation if not retaining gradients
    return _process_func_ret_and_grads(func_ret, grads, retain_grads)


def value_and_grad(func):
    def grad_fn(xs):
        grads = startai.nested_map(
            lambda x: startai.zeros_like(x), xs, include_derived=True, shallow=False
        )
        with tf.GradientTape(watch_accessed_variables=False) as tape:
            xs = startai.nested_map(lambda x: startai.to_native(x), xs, include_derived=True)
            tape.watch(xs)
            y = func(xs)
        y = y.to_native(y)
        grads_ = tape.gradient(y, xs)
        grads_ = startai.nested_map(
            lambda x: startai.to_startai(x),
            grads_,
            include_derived=True,
        )
        grads_ = startai.to_startai(grads_)
        grad_idxs = startai.nested_argwhere(grads_, lambda x: startai.is_startai_array(x))
        grad_array_vals = list(startai.multi_index_nest(grads_, grad_idxs))
        xs = startai.to_startai(xs)
        if isinstance(xs, startai.Array):
            grads = grads_
        else:
            startai.set_nest_at_indices(grads, grad_idxs, grad_array_vals)
        y = startai.to_startai(y)
        return y, grads

    return grad_fn


def stop_gradient(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    preserve_type: bool = True,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    is_var = is_variable(x)
    x = tf.stop_gradient(x)
    if is_var and preserve_type:
        return variable(x)
    return x


def jac(func: Callable):
    def grad_fn(x_in):
        return startai.to_native(
            func(startai.to_startai(x_in, nested=True)), nested=True, include_derived=True
        )

    def callback_fn(x_in):
        with tf.GradientTape(persistent=True) as tape:
            startai.nested_map(startai.copy_array, x_in)
            x_in = startai.to_native(x_in, nested=True)
            tape.watch(x_in)
            y = grad_fn(x_in)

            # Deal with multiple outputs
            if not isinstance(y, startai.NativeArray):
                jacobian = startai.nested_map(
                    lambda yi: startai.to_startai(
                        tape.jacobian(yi, x_in, unconnected_gradients="zero"),
                        nested=True,
                    ),
                    y,
                    include_derived=True,
                )
            else:
                jacobian = startai.to_startai(tape.jacobian(y, x_in))
        return jacobian

    return callback_fn


def grad(f, argnums=0):
    if grad.nth == 0:
        grad.f_original = f

    def _nth_derivative(n):
        @outputs_to_startai_arrays
        @inputs_to_native_arrays
        def _inner(*args, **kwargs):
            max_argnum = argnums if isinstance(argnums, int) else max(argnums)
            if max_argnum >= len(args):
                raise TypeError(
                    f"differentiating with respect to {argnums=} requires at least "
                    f"{max_argnum + 1} positional arguments to be passed by the "
                    f"caller, but got only {len(args)} positional arguments."
                )
            if isinstance(argnums, int):
                x = args[argnums]
            elif isinstance(argnums, (tuple, list)):
                x = []
                for i in argnums:
                    x.append(args[i])
            else:
                raise TypeError(
                    "argnums should be passed as int or a list/tuple of ints."
                    f" Found {type(argnums)}"
                )
            if n == 0:
                ret = (
                    grad.f_original(*args, **kwargs)
                    if grad.f_original is not None
                    else f(*args, **kwargs)
                )
                grad.nth = 0
                return ret
            else:
                with tf.GradientTape() as tape:
                    tape.watch(x)
                    y = _nth_derivative(n - 1)(*args, *kwargs)
                    ret = tape.gradient(y, x)
                return ret

        return _inner

    grad.nth += 1

    return _nth_derivative(grad.nth)


grad.f_original = None
grad.nth = 0
