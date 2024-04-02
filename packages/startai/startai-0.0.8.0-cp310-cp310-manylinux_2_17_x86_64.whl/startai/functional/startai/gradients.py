"""Collection of gradient Startai functions."""

# global
from typing import Sequence, Union, Optional, Tuple, Callable
import numpy as np
import itertools

# local
import startai
from startai.utils.backend import current_backend

from startai.func_wrapper import (
    handle_array_function,
    inputs_to_startai_arrays,
    to_native_arrays_and_back,
    handle_out_argument,
    handle_nestable,
    handle_array_like_without_promotion,
    handle_device,
    handle_backend_invalid,
)
from startai.utils.exceptions import handle_exceptions


# Helpers #
# ------- #


def _get_duplicate_index_chains(xs):
    """Generate a list of duplicate index chains for a given nested
    structure."""
    duplicate_index_chains = ()
    if isinstance(xs, startai.Container):
        duplicate_index_chains = xs.cont_duplicate_array_keychains()
    elif isinstance(xs, (list, tuple, dict)):
        duplicate_index_chains = startai.duplicate_array_index_chains(xs)
    return duplicate_index_chains


def _arrays_to_float_variables(xs, xs_grad_idxs=None):
    """Convert all required arrays to float variables for gradient
    calculation."""

    def inner_fn(x):
        if startai.is_array(x, exclusive=True):
            if startai.is_int_dtype(x.dtype):
                x = startai.astype(x, startai.default_float_dtype())
            elif _is_variable(x):
                x = startai.stop_gradient(x, preserve_type=False)
            return _variable(x)
        return x

    # Convert all required arrays to float variables
    def map_fn(x):
        return startai.nested_map(inner_fn, x, include_derived=True, shallow=False)

    if xs_grad_idxs is not None:
        xs_required = startai.multi_index_nest(xs, xs_grad_idxs)
        startai.nested_map(map_fn, xs_required, include_derived=True)
        startai.set_nest_at_indices(xs, xs_grad_idxs, xs_required)
        return xs
    return startai.nested_map(map_fn, xs, include_derived=True, shallow=False)


def _get_required_native_variables(xs, xs_grad_idxs):
    """Extract all required native variables from a nested structure."""
    # To make sure that only the required arrays are converted to native arrays
    xs = startai.nested_map(startai.to_startai, xs, include_derived=True, shallow=False)
    if xs_grad_idxs is not None:
        xs_required = startai.multi_index_nest(xs, xs_grad_idxs)
        startai.nested_map(startai.to_native, xs_required, include_derived=True)
        startai.set_nest_at_indices(xs, xs_grad_idxs, xs_required)
    else:
        xs = startai.nested_map(startai.to_native, xs, include_derived=True, shallow=False)

    def map_fn(x):
        if startai.is_native_array(x):
            return x
        return None

    # Extract all those required native arrays and None for all others
    xs = startai.nested_map(
        map_fn, xs, include_derived=True, to_mutable=True, shallow=False
    )

    # Prune all None values
    none_idxs = startai.nested_argwhere(xs, lambda x: x is None)
    not _check_if_empty(none_idxs) and startai.prune_nest_at_indices(
        xs, list(reversed(none_idxs))
    )
    xs = (
        xs
        if startai.is_array(xs)
        else (
            xs.cont_prune_empty()
            if isinstance(xs, startai.Container)
            else startai.prune_empty(xs)
        )
    )

    # return a single array instead of a list if possible, otherwise return the nest
    if isinstance(xs, list) and len(xs) == 1:
        return xs[0]
    return xs


def _get_required_float_variables(xs, xs_grad_idxs):
    """Convert all required arrays to float variables for gradient calculation.

    Also, returns a list of duplicate index chains for the nested
    structure.
    """
    if (startai.is_startai_container(xs) or startai.is_array(xs)) and xs_grad_idxs == ((0,),):
        xs_grad_idxs = None
    duplicate_index_chains = _get_duplicate_index_chains(xs)
    xs = _to_startai(xs)
    xs = _arrays_to_float_variables(xs, xs_grad_idxs=xs_grad_idxs)
    xs = _set_duplicates(xs, duplicate_index_chains)
    xs_required = _get_required_native_variables(xs, xs_grad_idxs)
    required_duplicate_index_chains = _get_duplicate_index_chains(xs_required)
    return (
        xs,
        xs_grad_idxs,
        xs_required,
        required_duplicate_index_chains,
        duplicate_index_chains,
    )


def _get_native_variables_and_indices(x, reshape=True, idxs=None, create_var=False):
    """Extract all relevant results from the output nested structure of a
    function."""

    def map_fn(x_):
        if startai.is_array(x_):
            x_ = startai.to_startai(x_) if startai.is_native_array(x_) else x_
            if create_var:
                x_ = x_ if _is_variable(x_, exclusive=True) else _variable(x_)
            if len(x_.shape) == 0:
                return startai.to_native(x_)
            if reshape:
                if x_.size == 1:
                    if reshape:
                        return startai.to_native(startai.reshape(x_, []))
                    return startai.to_native(x_)
                else:
                    return startai.to_startai(x_)
            else:
                return startai.to_native(x_)
        return x_

    if startai.is_array(x):
        return [], map_fn(x)

    x = startai.nested_map(map_fn, x, include_derived=True, shallow=False)
    arr_idxs = startai.nested_argwhere(x, lambda x: startai.is_native_array(x))
    if _check_if_empty(arr_idxs):
        return arr_idxs, []
    else:
        if idxs is not None:
            arr_idxs = [
                arr_idx
                for arr_idx in arr_idxs
                if "_".join(str(x) for x in arr_idx) in _idxs_to_str(idxs)
            ]
        arr_values = startai.multi_index_nest(x, arr_idxs)
        arr_idxs = _idxs_to_str(arr_idxs)
        return arr_idxs, arr_values


def _set_duplicates(xs, duplicate_index_chains):
    """Set the duplicates in the nested structure to have the same
    reference."""
    originals = list(
        map(
            lambda key_chains: [key_chains[0]] * (len(key_chains) - 1),
            duplicate_index_chains,
        )
    )
    originals = startai.multi_index_nest(xs, list(itertools.chain(*originals)))
    duplicates = list(
        map(lambda index_chains: list(index_chains[1:]), duplicate_index_chains)
    )
    nullifying_index_chains = (
        list(
            map(
                lambda index_chain: index_chain.split("/"),
                list(itertools.chain(*duplicates)),
            )
        )
        if isinstance(xs, startai.Container)
        else list(itertools.chain(*duplicates))
    )
    startai.set_nest_at_indices(xs, nullifying_index_chains, originals)
    return xs


def _get_y_and_ret_idxs(func_ret, ret_grad_idxs, create_var=False, reshape=True):
    """Get the relevant outputs from the function return value."""
    if (startai.is_startai_container(func_ret) or startai.is_array(func_ret)) and ret_grad_idxs == [
        [0]
    ]:
        ret_grad_idxs = None
    ret_idxs, ret_values = _get_native_variables_and_indices(
        func_ret, idxs=ret_grad_idxs, create_var=create_var, reshape=reshape
    )
    if ret_values is None or (isinstance(ret_values, list) and len(ret_values) == 0):
        return func_ret, {}
    if isinstance(ret_values, list) and len(ret_values) == 1 and ret_grad_idxs is None:
        y = ret_values[0]
    else:
        y = ret_values
    return ret_grad_idxs, y, ret_idxs


def _get_native_y(y):
    """Convert all outputs to native arrays."""
    array_idxs = startai.nested_argwhere(y, lambda x: startai.is_native_array(x))
    y_final = []
    if isinstance(array_idxs, list) and np.asarray(array_idxs, "object").size > 0:
        y_final = startai.multi_index_nest(y, array_idxs)
    return y_final


def _stop_grad_and_index(func_ret, retain_grads, grads):
    """Stop gradient propagation of the function results."""
    if not retain_grads:
        func_ret = startai.nested_map(
            lambda x: startai.stop_gradient(x) if startai.is_array(x) else x,
            func_ret,
            include_derived=True,
        )
    if isinstance(grads, dict):
        grads = startai.Container(grads)
    return func_ret, grads


def _process_func_ret_and_grads(func_ret, grads, retain_grads):
    """Stop gradients propagation.

    Set the gradients of non-finite values to zero, and stopping
    gradient propagation of the function results.
    """
    grads = _non_finite_to_zero(grads)
    func_ret, grads = _stop_grad_and_index(func_ret, retain_grads, grads)
    grads = _to_startai(grads)
    return func_ret, grads


def _check_if_empty(idxs):
    return not isinstance(idxs, list) or np.asarray(idxs, dtype="object").size == 0


def _idxs_to_str(idxs):
    return ["_".join(list(map(lambda x: str(x), idxs[i]))) for i in range(len(idxs))]


def _to_startai(xs):
    return startai.nested_map(
        lambda x: startai.to_startai(x) if startai.is_array(x) else x,
        xs,
        include_derived=True,
        shallow=False,
    )


def _non_finite_to_zero(xs):
    return startai.nested_map(
        lambda x: startai.where(startai.isfinite(x), x, 0.0) if startai.is_array(x) else x,
        xs,
        include_derived=True,
        shallow=False,
    )


def _flatten_containers(inputs):
    """Flatten containers into a single tuple of arrays.

    Returns a flattened tuple of arrays and the indices of the arrays in
    the original containers.
    """
    if startai.is_array(inputs) or startai.is_startai_container(inputs):
        inputs = (inputs,)
    values = []
    ret_idxs = []
    for idx, input in enumerate(inputs):
        if isinstance(input, startai.Container):
            grad_arr_idxs = startai.nested_argwhere(input, lambda x: startai.is_array(x))
            grad_arr_values = startai.multi_index_nest(input, grad_arr_idxs)
            values.extend(grad_arr_values)
            ret_idxs.append(grad_arr_idxs)
        elif startai.is_array(input):
            values.append(input)
            ret_idxs.append(None)
    return tuple(values), ret_idxs


def _rebuild_flattened_containers(outputs, ret_idxs):
    """Rebuild the containers from the flattened arrays into a single tuple."""
    rebuilt_outputs = []
    curr_idx = 0
    for ret_idx in ret_idxs:
        if ret_idx is None:
            rebuilt_outputs.append(outputs[curr_idx])
            curr_idx += 1
        else:
            cont = startai.Container()
            num_elements = len(ret_idx)
            cont_outputs = outputs[curr_idx : curr_idx + num_elements]
            startai.insert_into_nest_at_indices(cont, ret_idx, cont_outputs)
            rebuilt_outputs.append(cont)
            curr_idx += num_elements
    return tuple(rebuilt_outputs)


# Private Variable Helpers #
# -------------------------#


def _variable(x):
    x = startai.to_native(x, nested=True)
    ret = startai.nested_map(
        current_backend(x).variable, x, include_derived=True, shallow=False
    )
    return startai.nested_map(startai.to_startai, ret, include_derived=True)


def _is_variable(x, exclusive=False, to_ignore=None) -> bool:
    x = startai.to_native(x, nested=True, to_ignore=to_ignore)
    return startai.nested_map(
        lambda x: current_backend(x).is_variable(x, exclusive=exclusive),
        x,
        include_derived=True,
        shallow=False,
        to_ignore=to_ignore,
    )


def _variable_data(
    x: Union[startai.Array, startai.NativeArray],
) -> Union[startai.Array, startai.NativeArray]:
    """Get the contents of the input.

    Parameters
    ----------
    x
        Input array.

    Returns
    -------
    ret
        An array with contents of the input.
    """
    x = startai.to_native(x, nested=True)
    ret = startai.nested_map(
        lambda x: current_backend(x).variable_data(x), x, include_derived=True
    )
    return startai.nested_map(startai.to_startai, ret, include_derived=True)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def stop_gradient(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    preserve_type: bool = True,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Stop gradient computation.

    Parameters
    ----------
    x
        Array for which to stop the gradient.
    preserve_type
        Whether to preserve gradient computation on startai.Array instances. Default is
        True.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The same array x, but with no gradient information.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> x = startai.array([1., 2., 3.])
    >>> y = startai.stop_gradient(x, preserve_type=True)
    >>> print(y)
    startai.array([1., 2., 3.])

    >>> x = startai.zeros((2, 3))
    >>> startai.stop_gradient(x, preserve_type=False, out=x)
    >>> print(x)
    startai.array([[0., 0., 0.],
               [0., 0., 0.]])

    With one :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> y = startai.stop_gradient(x, preserve_type=False)
    >>> print(y)
    {
        a: startai.array([0., 1., 2.]),
        b: startai.array([3., 4., 5.])
    }

    With multiple :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> startai.stop_gradient(x, preserve_type=True, out=x)
    >>> print(x)
    {
        a: startai.array([0., 1., 2.]),
        b: startai.array([3., 4., 5.])
    }
    """
    return current_backend(x).stop_gradient(x, preserve_type=preserve_type, out=out)


# AutoGrad #


@handle_exceptions
@handle_device
def execute_with_gradients(
    func,
    xs: Union[startai.Array, startai.NativeArray],
    /,
    *,
    retain_grads: bool = False,
    xs_grad_idxs: Sequence[Sequence[Union[str, int]]] = ((0,),),
    ret_grad_idxs: Sequence[Sequence[Union[str, int]]] = ((0,),),
) -> Tuple[startai.Array, startai.Array]:
    """Call function func with input of xs variables, and return the function
    result func_ret and the gradients of each output variable w.r.t each input
    variable,

    Parameters
    ----------
    func
        Function for which we compute the gradients of the output with respect to xs
        input.
    xs
        Variables for which to compute the function gradients with respective to. This
        can be a single array or an arbitrary nest of arrays.
    retain_grads
        Whether to retain the gradients of the returned values. (Default value = False)
    xs_grad_idxs
        Indices of the input arrays to compute gradients with respect to. If None,
        gradients are returned with respect to all input arrays. If ``xs`` is an
        ``startai.Array`` or ``startai.Container``, the default value is ``None``, otherwise the
        default value is ``[[0]]``.
    ret_grad_idxs
        Indices of the returned arrays for which to return computed gradients. If None,
        gradients are returned for all returned arrays. If the returned object from the
        ``func`` is an ``startai.Array`` or ``startai.Container``, the default value is ``None``
        otherwise the default value is ``[[0]]``.

    Returns
    -------
    ret
        the function result func_ret and a dictionary of gradients of each output
        variable w.r.t each input variable.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[1, 4, 6], [2, 6, 9]])
    >>> func = lambda x: startai.mean(startai.square(x))
    >>> func_ret = startai.execute_with_gradients(func, x, retain_grads=True)
    >>> print(func_ret)
    (startai.array(29.), startai.array([[0.33333334, 1.33333337, 2.        ],
       [0.66666669, 2.        , 3.        ]]))

    With :class:`startai.Container` input:

    >>> x = startai.Container(a = startai.array([1, 4, 6]),
    ...                   b = startai.array([2, 6, 9]))
    >>> func = lambda x: startai.mean(startai.square(x))
    >>> func_ret = startai.execute_with_gradients(func, x, retain_grads=True)
    >>> print(func_ret)
    ({
    a: startai.array(17.666666),
    b: startai.array(40.333332)
    },
    {
    a: {
        a: startai.array([0.66666669, 2.66666675, 4.]),
        b: startai.array([0., 0., 0.])
    },
    b: {
        a: startai.array([0., 0., 0.]),
        b: startai.array([1.33333337, 4., 6.])
    }
    })
    """
    return current_backend(None).execute_with_gradients(
        func,
        xs,
        retain_grads=retain_grads,
        xs_grad_idxs=xs_grad_idxs,
        ret_grad_idxs=ret_grad_idxs,
    )


execute_with_gradients.computes_gradients = True


@handle_exceptions
def value_and_grad(func: Callable) -> Callable:
    """Create a function that evaluates both func and the gradient of func.

    Parameters
    ----------
    func
        Function for which we compute the gradients of the output with respect to xs
        input.

    Returns
    -------
    ret
        A function that returns both func and the gradient of func.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[4.6, 2.1, 5], [2.8, 1.3, 6.2]])
    >>> func = lambda x: startai.mean(startai.square(x))
    >>> grad_fn = startai.value_and_grad(func)
    >>> value_grad = grad_fn(x)
    >>> print(value_grad)
    (startai.array(16.42333412), startai.array([[1.5333333 , 0.69999999, 1.66666675],
           [0.93333334, 0.43333334, 2.0666666 ]]))
    """
    return current_backend(None).value_and_grad(func)


value_and_grad.computes_gradients = True


@handle_exceptions
def jac(func: Callable) -> Callable:
    """Call function func, and return func's Jacobian partial derivatives.

    Parameters
    ----------
    func
        Function for which we compute the gradients of the output with respect to xs
        input.

    Returns
    -------
    ret
        the Jacobian function

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[4.6, 2.1, 5], [2.8, 1.3, 6.2]])
    >>> func = lambda x: startai.mean(startai.square(x))
    >>> jac_fn = startai.jac(func)
    >>> jacobian = jac_fn(x)
    >>> print(jacobian)
    startai.array([[1.53 , 0.7  , 1.67 ],
    ...        [0.933, 0.433, 2.07 ]])
    """
    return current_backend(None).jac(func)


jac.computes_gradients = True


@handle_exceptions
def grad(func: Callable, argnums: Union[int, Sequence[int]] = 0) -> Callable:
    """Call function func, and return func's gradients.

    Parameters
    ----------
    func
        Function for which we compute the gradients of the output with respect to xs
        input.
    argnums
        Indices of the input arrays to compute gradients with respect to. Default is 0.

    Returns
    -------
    ret
        the grad function

    Examples
    --------
    >>> x = startai.array([[4.6, 2.1, 5], [2.8, 1.3, 6.2]])
    >>> func = lambda x: startai.mean(startai.square(x))
    >>> grad_fn = startai.grad(func)
    >>> grad = grad_fn(x)
    >>> print(grad)
    startai.array([[1.53 , 0.7  , 1.67 ],
    ...        [0.933, 0.433, 2.07 ]])
    """
    return current_backend(None).grad(func, argnums=argnums)


grad.computes_gradients = True


# Optimizer Steps #


@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def adam_step(
    dcdw: Union[startai.Array, startai.NativeArray],
    mw: Union[startai.Array, startai.NativeArray],
    vw: Union[startai.Array, startai.NativeArray],
    step: Union[int, float],
    /,
    *,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-7,
    out: Optional[startai.Array] = None,
) -> Tuple[startai.Array, startai.Array, startai.Array]:
    """Compute adam step delta, given the derivatives of some cost c with
    respect to weights ws, using ADAM update. `[reference]

    <https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Adam>`_

    Parameters
    ----------
    dcdw
        Derivates of the cost c with respect to the weights ws, [dc/dw for w in ws].
    mw
        running average of the gradients
    vw
        running average of second moments of the gradients
    step
        training step
    beta1
        gradient forgetting factor (Default value = 0.9)
    beta2
        second moment of gradient forgetting factor (Default value = 0.999)
    epsilon
        divisor during adam update, preventing division by zero (Default value = 1e-7)
    out
        optional output array, for writing the effective grad of adam_step to. It must
        have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        The adam step delta.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> dcdw = startai.array([1, 2, 3])
    >>> mw = startai.ones(3)
    >>> vw = startai.ones(1)
    >>> step = startai.array(3)
    >>> adam_step_delta = startai.adam_step(dcdw, mw, vw, step)
    >>> print(adam_step_delta)
    (startai.array([0.2020105 , 0.22187898, 0.24144873]),
    startai.array([0.99999998, 1.09999998, 1.19999998]),
    startai.array([1.00000001, 1.00300001, 1.00800001]))

    >>> dcdw = startai.array([[1., 4., -3.], [2., 3., 0.5]])
    >>> mw = startai.zeros((2,3))
    >>> vw = startai.zeros(3)
    >>> step = startai.array(1)
    >>> beta1 = 0.86
    >>> beta2 = 0.95
    >>> epsilon = 1e-6
    >>> adam_step_delta = startai.adam_step(dcdw, mw, vw, step, beta1=beta1, beta2=beta2,
    ...                                 epsilon=epsilon)
    >>> print(adam_step_delta)
    (startai.array([[ 1.,  1., -1.],
                [ 1.,  1.,  1.]]),
        startai.array([[ 0.14,  0.56, -0.42],
                   [ 0.28,  0.42,  0.07]]),
     startai.array([[0.05  , 0.8   , 0.45  ],
                [0.2   , 0.45  , 0.0125]]))

    >>> dcdw = startai.array([0.1, -0.7, 2])
    >>> mw = startai.ones(1)
    >>> vw = startai.ones(1)
    >>> step = startai.array(3.6)
    >>> out = startai.zeros_like(dcdw)
    >>> adam_step_delta = startai.adam_step(dcdw, mw, vw, step, out=out)
    >>> print(out)
    startai.array([0.17294501, 0.15770318, 0.20863818])

    With one :class:`startai.Container` input:

    >>> dcdw = startai.Container(a=startai.array([0., 1., 2.]),
    ...                      b=startai.array([3., 4., 5.]))
    >>> mw = startai.array([1., 4., 9.])
    >>> vw = startai.array([0.,])
    >>> step = startai.array([3.4])
    >>> beta1 = 0.87
    >>> beta2 = 0.976
    >>> epsilon = 1e-5
    >>> adam_step_delta = startai.adam_step(dcdw, mw, vw, step, beta1=beta1, beta2=beta2,
    ...                                 epsilon=epsilon)
    >>> print(adam_step_delta)
    ({
        a: startai.array([6.49e+04, 1.74e+01, 1.95e+01]),
        b: startai.array([2.02, 4.82, 8.17])
    }, {
        a: startai.array([0.87, 3.61, 8.09]),
        b: startai.array([1.26, 4., 8.48])
    }, {
        a: startai.array([0., 0.024, 0.096]),
        b: startai.array([0.216, 0.384, 0.6])
    })

    With multiple :class:`startai.Container` inputs:

    >>> dcdw = startai.Container(a=startai.array([0., 1., 2.]),
    ...                      b=startai.array([3., 4., 5.]))
    >>> mw = startai.Container(a=startai.array([0., 0., 0.]),
    ...                    b=startai.array([0., 0., 0.]))
    >>> vw = startai.Container(a=startai.array([0.,]),
    ...                    b=startai.array([0.,]))
    >>> step = startai.array([3.4])
    >>> beta1 = 0.87
    >>> beta2 = 0.976
    >>> epsilon = 1e-5
    >>> adam_step_delta = startai.adam_step(dcdw, mw, vw, step, beta1=beta1, beta2=beta2,
    ...                                 epsilon=epsilon)
    >>> print(adam_step_delta)
    ({
        a: startai.array([0., 0.626, 0.626]),
        b: startai.array([0.626, 0.626, 0.626])
    }, {
        a: startai.array([0., 0.13, 0.26]),
        b: startai.array([0.39, 0.52, 0.65])
    }, {
        a: startai.array([0., 0.024, 0.096]),
        b: startai.array([0.216, 0.384, 0.6])
    })
    """
    step = float(step)
    mw = startai.add(beta1 * mw, (1 - beta1) * dcdw)
    dcdw_sqrd = dcdw**2
    vw = startai.add(startai.multiply(beta2, vw), (1 - beta2) * dcdw_sqrd)
    vw_sqrt = startai.maximum(vw, 0.0) ** 0.5
    beta1_pow = beta1**step
    beta2_pow = beta2**step
    alpha = (1 - beta2_pow) ** 0.5 / (1 - beta1_pow + epsilon)
    return startai.divide(alpha * mw, vw_sqrt + epsilon, out=out), mw, vw


adam_step.out_index = 0


# Optimizer Updates #


@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def optimizer_update(
    w: Union[startai.Array, startai.NativeArray],
    effective_grad: Union[startai.Array, startai.NativeArray],
    lr: Union[float, startai.Array, startai.NativeArray],
    /,
    *,
    stop_gradients: bool = True,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Update weights ws of some function, given the true or effective
    derivatives of some cost c with respect to ws, [dc/dw for w in ws].

    Parameters
    ----------
    w
        Weights of the function to be updated.
    effective_grad
        Effective gradients of the cost c with respect to the weights ws,
        [dc/dw for w in ws].
    lr
        Learning rate(s), the rate(s) at which the weights should be updated relative to
        the gradient.
    stop_gradients
        Whether to stop the gradients of the variables after each gradient step.
        Default is ``True``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The new function weights ws_new, following the optimizer updates.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> w = startai.array([1., 2., 3.])
    >>> effective_grad = startai.zeros(3)
    >>> lr = 3e-4
    >>> ws_new = startai.optimizer_update(w, effective_grad, lr)
    >>> print(ws_new)
    startai.array([1., 2., 3.])

    >>> w = startai.array([1., 2., 3.])
    >>> effective_grad = startai.zeros(3)
    >>> lr = 3e-4
    >>> ws_new = startai.optimizer_update(w, effective_grad, lr,
    ...                               out=None, stop_gradients=True)
    >>> print(ws_new)
    startai.array([1., 2., 3.])

    >>> w = startai.array([[1., 2.], [4., 5.]])
    >>> out = startai.zeros_like(w)
    >>> effective_grad = startai.array([[4., 5.], [7., 8.]])
    >>> lr = startai.array([3e-4, 1e-2])
    >>> ws_new = startai.optimizer_update(w, effective_grad, lr, out=out)
    >>> print(out)
    startai.array([[0.999, 1.95],
               [4., 4.92]])

    >>> w = startai.array([1., 2., 3.])
    >>> out = startai.zeros_like(w)
    >>> effective_grad = startai.array([4., 5., 6.])
    >>> lr = startai.array([3e-4])
    >>> ws_new = startai.optimizer_update(w, effective_grad, lr,
    ...                               stop_gradients=False, out=out)
    >>> print(out)
    startai.array([0.999, 2.   , 3.   ])

    With one :class:`startai.Container` input:

    >>> w = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> effective_grad = startai.array([0., 0., 0.])
    >>> lr = 3e-4
    >>> ws_new = startai.optimizer_update(w, effective_grad, lr)
    >>> print(ws_new)
    {
        a: startai.array([0., 1., 2.]),
        b: startai.array([3., 4., 5.])
    }

    With multiple :class:`startai.Container` inputs:

    >>> w = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> effective_grad = startai.Container(a=startai.array([0., 0., 0.]),
    ...                                b=startai.array([0., 0., 0.]))
    >>> lr = 3e-4
    >>> ws_new = startai.optimizer_update(w, effective_grad, lr, out=w)
    >>> print(w)
    {
        a: startai.array([0., 1., 2.]),
        b: startai.array([3., 4., 5.])
    }

    >>> w = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> effective_grad = startai.Container(a=startai.array([0., 0., 0.]),
    ...                                b=startai.array([0., 0., 0.]))
    >>> lr = startai.array([3e-4])
    >>> ws_new = startai.optimizer_update(w, effective_grad, lr,
    ...                               stop_gradients=False)
    >>> print(ws_new)
    {
        a: startai.array([0., 1., 2.]),
        b: startai.array([3., 4., 5.])
    }
    """
    deltas = effective_grad * lr
    w = startai.subtract(w, deltas, out=out)
    if stop_gradients:
        return startai.stop_gradient(w, preserve_type=True, out=out)
    return w


@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def gradient_descent_update(
    w: Union[startai.Array, startai.NativeArray],
    dcdw: Union[startai.Array, startai.NativeArray],
    lr: Union[float, startai.Array, startai.NativeArray],
    /,
    *,
    stop_gradients: bool = True,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Update weights ws of some function, given the derivatives of some cost c
    with respect to ws, [dc/dw for w in ws].

    Parameters
    ----------
    w
        Weights of the function to be updated.
    dcdw
        Derivates of the cost c with respect to the weights ws, [dc/dw for w in ws].
    lr
        Learning rate(s), the rate(s) at which the weights should be updated relative to
        the gradient.
    stop_gradients
        Whether to stop the gradients of the variables after each gradient step.
        Default is ``True``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The new weights, following the gradient descent updates.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> w = startai.array([[1., 2, 3],
    ...                [4, 6, 1],
    ...                [1, 0, 7]])
    >>> dcdw = startai.array([[0.5, 0.2, 0.1],
    ...                   [0.3, 0.6, 0.4],
    ...                   [0.4, 0.7, 0.2]])
    >>> lr = startai.array(0.1)
    >>> new_weights = startai.gradient_descent_update(w, dcdw, lr, stop_gradients=True)
    >>> print(new_weights)
    startai.array([[ 0.95,  1.98,  2.99],
    ...        [ 3.97,  5.94,  0.96],
    ...        [ 0.96, -0.07,  6.98]])

    >>> w = startai.array([1., 2., 3.])
    >>> dcdw = startai.array([0.5, 0.2, 0.1])
    >>> lr = startai.array(0.3)
    >>> out = startai.zeros_like(w)
    >>> startai.gradient_descent_update(w, dcdw, lr, out=out)
    >>> print(out)
    startai.array([0.85, 1.94, 2.97])

    With one :class:`startai.Container` inputs:

    >>> w = startai.Container(a=startai.array([1., 2., 3.]),
    ...                   b=startai.array([3.48, 5.72, 1.98]))
    >>> dcdw = startai.array([0.5, 0.2, 0.1])
    >>> lr = startai.array(0.3)
    >>> w_new = startai.gradient_descent_update(w, dcdw, lr)
    >>> print(w_new)
    {
        a: startai.array([0.85, 1.94, 2.97]),
        b: startai.array([3.33, 5.66, 1.95])
    }

    With multiple :class:`startai.Container` inputs:

    >>> w = startai.Container(a=startai.array([1., 2., 3.]),
    ...                   b=startai.array([3.48, 5.72, 1.98]))
    >>> dcdw = startai.Container(a=startai.array([0.5, 0.2, 0.1]),
    ...                      b=startai.array([2., 3.42, 1.69]))
    >>> lr = startai.array(0.3)
    >>> w_new = startai.gradient_descent_update(w, dcdw, lr)
    >>> print(w_new)
    {
        a: startai.array([0.85, 1.94, 2.97]),
        b: startai.array([2.88, 4.69, 1.47])
    }
    """
    return startai.optimizer_update(w, dcdw, lr, stop_gradients=stop_gradients, out=out)


@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def lars_update(
    w: Union[startai.Array, startai.NativeArray],
    dcdw: Union[startai.Array, startai.NativeArray],
    lr: Union[float, startai.Array, startai.NativeArray],
    /,
    *,
    decay_lambda: float = 0,
    stop_gradients: bool = True,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Update weights ws of some function, given the derivatives of some cost c
    with respect to ws, [dc/dw for w in ws], by applying Layerwise Adaptive
    Rate Scaling (LARS) method.

    Parameters
    ----------
    w
        Weights of the function to be updated.
    dcdw
        Derivates of the cost c with respect to the weights ws, [dc/dw for w in ws].
    lr
        Learning rate, the rate at which the weights should be updated relative to the
        gradient.
    decay_lambda
        The factor used for weight decay. Default is zero.
    stop_gradients
        Whether to stop the gradients of the variables after each gradient step.
        Default is ``True``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The new function weights ws_new, following the LARS updates.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> w = startai.array([[3., 1, 5],
    ...                [7, 2, 9]])
    >>> dcdw = startai.array([[0.3, 0.1, 0.2],
    ...                   [0.1, 0.2, 0.4]])
    >>> lr = startai.array(0.1)
    >>> new_weights = startai.lars_update(w, dcdw, lr)
    >>> print(new_weights)
    startai.array([[2.34077978, 0.78025991, 4.56051969],
    ...        [6.78026009, 1.56051981, 8.12103939]])

    >>> w = startai.array([3., 1, 5])
    >>> dcdw = startai.array([0.3, 0.1, 0.2])
    >>> lr = startai.array(0.1)
    >>> out = startai.zeros_like(dcdw)
    >>> startai.lars_update(w, dcdw, lr, out=out)
    >>> print(out)
    startai.array([2.52565837, 0.8418861 , 4.68377209])

    With one :class:`startai.Container` inputs:

    >>> w = startai.Container(a=startai.array([3.2, 2.6, 1.3]),
    ...                    b=startai.array([1.4, 3.1, 5.1]))
    >>> dcdw = startai.array([0.2, 0.4, 0.1])
    >>> lr = startai.array(0.1)
    >>> new_weights = startai.lars_update(w, dcdw, lr)
    >>> print(new_weights)
    {
        a: startai.array([3.01132035, 2.22264051, 1.2056601]),
        b: startai.array([1.1324538, 2.56490755, 4.96622658])
    }

    With multiple :class:`startai.Container` inputs:

    >>> w = startai.Container(a=startai.array([3.2, 2.6, 1.3]),
    ...                    b=startai.array([1.4, 3.1, 5.1]))
    >>> dcdw = startai.Container(a=startai.array([0.2, 0.4, 0.1]),
    ...                       b=startai.array([0.3,0.1,0.2]))
    >>> lr = startai.array(0.1)
    >>> new_weights = startai.lars_update(w, dcdw, lr)
    >>> print(new_weights)
    {
        a: startai.array([3.01132035, 2.22264051, 1.2056601]),
        b: startai.array([0.90848625, 2.93616199, 4.77232409])
    }
    """
    w_norm = startai.vector_norm(w)
    lr = startai.stable_divide(w_norm * lr, startai.vector_norm(dcdw))
    if decay_lambda > 0:
        lr /= w_norm * decay_lambda
    return startai.gradient_descent_update(
        w, dcdw, lr, stop_gradients=stop_gradients, out=out
    )


@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def adam_update(
    w: Union[startai.Array, startai.NativeArray],
    dcdw: Union[startai.Array, startai.NativeArray],
    lr: Union[float, startai.Array, startai.NativeArray],
    mw_tm1: Union[startai.Array, startai.NativeArray],
    vw_tm1: Union[startai.Array, startai.NativeArray],
    step: int,
    /,
    *,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-7,
    stop_gradients: bool = True,
    out: Optional[startai.Array] = None,
) -> Tuple[startai.Array, startai.Array, startai.Array]:
    """Update weights ws of some function, given the derivatives of some cost c
    with respect to ws, using ADAM update. `[reference]

    <https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Adam>`_

    Parameters
    ----------
    w
        Weights of the function to be updated.
    dcdw
        Derivates of the cost c with respect to the weights ws, [dc/dw for w in ws].
    lr
        Learning rate(s), the rate(s) at which the weights should be updated relative to
        the gradient.
    mw_tm1
        running average of the gradients, from the previous time-step.
    vw_tm1
        running average of second moments of the gradients, from the previous time-step.
    step
        training step.
    beta1
        gradient forgetting factor (Default value = 0.9).
    beta2
        second moment of gradient forgetting factor (Default value = 0.999).
    epsilon
        divisor during adam update, preventing division by zero (Default value = 1e-7).
    stop_gradients
        Whether to stop the gradients of the variables after each gradient step.
        Default is ``True``.
    out
        optional output array, for writing the new function weights ws_new to. It must
        have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        The new function weights ws_new, and also new mw and vw, following the adam
        updates.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> w = startai.array([1., 2, 3])
    >>> dcdw = startai.array([0.5,0.2,0.1])
    >>> lr = startai.array(0.1)
    >>> vw_tm1 = startai.zeros(1)
    >>> mw_tm1 = startai.zeros(3)
    >>> step = 1
    >>> updated_weights = startai.adam_update(w, dcdw, lr, mw_tm1, vw_tm1, step)
    >>> print(updated_weights)
    (startai.array([0.90000075, 1.90000164, 2.9000032 ]),
    startai.array([0.05, 0.02, 0.01]),
    startai.array([2.50000012e-04, 4.00000063e-05, 1.00000016e-05]))

    >>> w = startai.array([[1., 2, 3],[4, 2, 4],[6, 4, 2]])
    >>> dcdw = startai.array([[0.1, 0.2, 0.3],[0.4, 0.5, 0.1],[0.1, 0.5, 0.3]])
    >>> lr = startai.array(0.1)
    >>> mw_tm1 = startai.zeros((3,3))
    >>> vw_tm1 = startai.zeros(3)
    >>> step = 2
    >>> beta1 = 0.9
    >>> beta2 = 0.999
    >>> epsilon = 1e-7
    >>> out = startai.zeros_like(w)
    >>> stop_gradients = True
    >>> updated_weights = startai.adam_update(w, dcdw, lr, mw_tm1, vw_tm1, step,
    ...                               beta1=beta1, beta2=beta2,
    ...                               epsilon=epsilon, out=out,
    ...                               stop_gradients=stop_gradients)
    >>> print(updated_weights)
    (
    startai.array([[0.92558873, 1.92558754, 2.92558718],
               [3.92558694, 1.92558682, 3.92558861],
               [5.92558861, 3.92558694, 1.92558718]]),
    startai.array([[0.01, 0.02, 0.03],
               [0.04, 0.05, 0.01],
               [0.01, 0.05, 0.03]]),
    startai.array([[1.00000016e-05, 4.00000063e-05, 9.00000086e-05],
               [1.60000025e-04, 2.50000012e-04, 1.00000016e-05],
               [1.00000016e-05, 2.50000012e-04, 9.00000086e-05]])
    )

    With one :class:`startai.Container` input:

    >>> w = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([4., 5., 6.]))
    >>> dcdw = startai.array([0.5, 0.2, 0.4])
    >>> mw_tm1 = startai.array([0., 0., 0.])
    >>> vw_tm1 = startai.array([0.])
    >>> lr = startai.array(0.01)
    >>> step = 2
    >>> updated_weights = startai.adam_update(w, dcdw, mw_tm1, vw_tm1, lr, step)
    >>> print(updated_weights)
    ({
        a: startai.array([1., 2., 3.]),
        b: startai.array([4., 5., 6.])
    }, startai.array([0.05, 0.02, 0.04]), startai.array([0.01024, 0.01003, 0.01015]))

    With multiple :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([0., 1., 2.]),
    ...                   b=startai.array([3., 4., 5.]))
    >>> dcdw = startai.Container(a=startai.array([0.1,0.3,0.3]),
    ...                      b=startai.array([0.3,0.2,0.2]))
    >>> mw_tm1 = startai.Container(a=startai.array([0.,0.,0.]),
    ...                        b=startai.array([0.,0.,0.]))
    >>> vw_tm1 = startai.Container(a=startai.array([0.,]),
    ...                        b=startai.array([0.,]))
    >>> step = 3
    >>> beta1 = 0.9
    >>> beta2 = 0.999
    >>> epsilon = 1e-7
    >>> stop_gradients = False
    >>> lr = startai.array(0.001)
    >>> updated_weights = startai.adam_update(w, dcdw, lr, mw_tm1, vw_tm1, step,
    ...                               beta1=beta1,
    ...                               beta2=beta2, epsilon=epsilon,
    ...                               stop_gradients=stop_gradients)
    >>> print(updated_weights)
    ({
        a: startai.array([0.99936122, 1.99936116, 2.99936128]),
        b: startai.array([3.99936128, 4.99936104, 5.99936104])
    }, {
        a: startai.array([0.01, 0.03, 0.03]),
        b: startai.array([0.03, 0.02, 0.02])
    }, {
        a: startai.array([1.00000016e-05, 9.00000086e-05, 9.00000086e-05]),
        b: startai.array([9.00000086e-05, 4.00000063e-05, 4.00000063e-05])
    })
    """
    effective_grads, mw, vw = startai.adam_step(
        dcdw, mw_tm1, vw_tm1, step, beta1=beta1, beta2=beta2, epsilon=epsilon
    )
    return (
        startai.optimizer_update(
            w, effective_grads, lr, stop_gradients=stop_gradients, out=out
        ),
        mw,
        vw,
    )


adam_update.out_index = 0


@handle_exceptions
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def lamb_update(
    w: Union[startai.Array, startai.NativeArray],
    dcdw: Union[startai.Array, startai.NativeArray],
    lr: Union[float, startai.Array, startai.NativeArray],
    mw_tm1: Union[startai.Array, startai.NativeArray],
    vw_tm1: Union[startai.Array, startai.NativeArray],
    step: int,
    /,
    *,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-7,
    max_trust_ratio: Union[int, float] = 10,
    decay_lambda: float = 0,
    stop_gradients: bool = True,
    out: Optional[startai.Array] = None,
) -> Tuple[startai.Array, startai.Array, startai.Array]:
    """Update weights ws of some function, given the derivatives of some cost c
    with respect to ws, [dc/dw for w in ws], by applying LAMB method.

    Parameters
    ----------
    w
        Weights of the function to be updated.
    dcdw
        Derivates of the cost c with respect to the weights ws, [dc/dw for w in ws].
    lr
        Learning rate(s), the rate(s) at which the weights should be updated relative to
        the gradient.
    mw_tm1
        running average of the gradients, from the previous time-step.
    vw_tm1
        running average of second moments of the gradients, from the previous time-step.
    step
        training step.
    beta1
        gradient forgetting factor (Default value = 0.9).
    beta2
        second moment of gradient forgetting factor (Default value = 0.999).
    epsilon
        divisor during adam update, preventing division by zero (Default value = 1e-7).
    max_trust_ratio
        The maximum value for the trust ratio. (Default value = 10)
    decay_lambda
        The factor used for weight decay. (Default value = 0).
    stop_gradients
        Whether to stop the gradients of the variables after each gradient step.
        Default is ``True``.
    out
        optional output array, for writing the new function weights ws_new to. It must
        have a shape that the inputs broadcast to.

    Returns
    -------
    ret
        The new function weights ws_new, following the LAMB updates.

    Examples
    --------
    With :class:`startai.Array` inputs:

    >>> w = startai.array([1., 2, 3])
    >>> dcdw = startai.array([0.5,0.2,0.1])
    >>> lr = startai.array(0.1)
    >>> vw_tm1 = startai.zeros(1)
    >>> mw_tm1 = startai.zeros(3)
    >>> step = startai.array(1)
    >>> new_weights = startai.lamb_update(w, dcdw, lr, mw_tm1, vw_tm1, step)
    >>> print(new_weights)
    (startai.array([0.784, 1.78 , 2.78 ]),
    ... startai.array([0.05, 0.02, 0.01]),
    ... startai.array([2.5e-04, 4.0e-05, 1.0e-05]))

    >>> w = startai.array([[1., 2, 3],[4, 6, 1],[1, 0, 7]])
    >>> dcdw = startai.array([[0.5, 0.2, 0.1],[0.3, 0.6, 0.4],[0.4, 0.7, 0.2]])
    >>> lr = startai.array(0.1)
    >>> mw_tm1 = startai.zeros((3,3))
    >>> vw_tm1 = startai.zeros(3)
    >>> step = startai.array(1)
    >>> beta1 = 0.9
    >>> beta2 = 0.999
    >>> epsilon = 1e-7
    >>> max_trust_ratio = 10
    >>> decay_lambda = 0
    >>> out = startai.zeros_like(w)
    >>> stop_gradients = True
    >>> new_weights = startai.lamb_update(w, dcdw, lr, mw_tm1, vw_tm1, step, beta1=beta1,
    ...                               beta2=beta2, epsilon=epsilon,
    ...                               max_trust_ratio=max_trust_ratio,
    ...                               decay_lambda=decay_lambda, out=out,
    ...                               stop_gradients=stop_gradients)
    >>> print(out)
    startai.array([[ 0.639,  1.64 ,  2.64 ],
    ...        [ 3.64 ,  5.64 ,  0.639],
    ...        [ 0.639, -0.361,  6.64 ]])

    With one :class:`startai.Container` inputs:

    >>> w = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([4., 5., 6.]))
    >>> dcdw = startai.array([3., 4., 5.])
    >>> mw_tm1 = startai.array([0., 0., 0.])
    >>> vw_tm1 = startai.array([0.])
    >>> lr = startai.array(1.)
    >>> step = startai.array([2])
    >>> new_weights = startai.lamb_update(w, dcdw, mw_tm1, vw_tm1, lr, step)
    >>> print(new_weights)
    ({
        a: startai.array([1., 2., 3.]),
        b: startai.array([4., 5., 6.])
    }, startai.array([0.3, 0.4, 0.5]), startai.array([1.01, 1.01, 1.02]))

    With multiple :class:`startai.Container` inputs:

    >>> w = startai.Container(a=startai.array([1.,3.,5.]),
    ...                   b=startai.array([3.,4.,2.]))
    >>> dcdw = startai.Container(a=startai.array([0.2,0.3,0.6]),
    ...                      b=startai.array([0.6,0.4,0.7]))
    >>> mw_tm1 = startai.Container(a=startai.array([0.,0.,0.]),
    ...                        b=startai.array([0.,0.,0.]))

    >>> vw_tm1 = startai.Container(a=startai.array([0.,]),
    ...                        b=startai.array([0.,]))
    >>> step = startai.array([3.4])
    >>> beta1 = 0.9
    >>> beta2 = 0.999
    >>> epsilon = 1e-7
    >>> max_trust_ratio = 10
    >>> decay_lambda = 0
    >>> stop_gradients = True
    >>> lr = startai.array(0.5)
    >>> new_weights = startai.lamb_update(w, dcdw, lr, mw_tm1, vw_tm1, step, beta1=beta1,
    ...                               beta2=beta2, epsilon=epsilon,
    ...                               max_trust_ratio=max_trust_ratio,
    ...                               decay_lambda=decay_lambda,
    ...                               stop_gradients=stop_gradients)
    >>> print(new_weights)
    ({
        a: startai.array([-0.708, 1.29, 3.29]),
        b: startai.array([1.45, 2.45, 0.445])
    }, {
        a: startai.array([0.02, 0.03, 0.06]),
        b: startai.array([0.06, 0.04, 0.07])
    }, {
        a: startai.array([4.0e-05, 9.0e-05, 3.6e-04]),
        b: startai.array([0.00036, 0.00016, 0.00049])
    })
    """
    r1 = startai.vector_norm(w)
    eff_grads, mw, vw = startai.adam_step(
        dcdw, mw_tm1, vw_tm1, step, beta1=beta1, beta2=beta2, epsilon=epsilon
    )
    if decay_lambda > 0:
        r2 = startai.vector_norm(eff_grads + decay_lambda * w)
    else:
        r2 = startai.vector_norm(eff_grads)
    r = startai.minimum(startai.stable_divide(r1, r2), startai.array(max_trust_ratio))
    lr = r * lr
    return (
        startai.optimizer_update(w, eff_grads, lr, stop_gradients=stop_gradients, out=out),
        mw,
        vw,
    )


lamb_update.out_index = 0
