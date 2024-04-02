"""Collection of Startai activation functions."""

from typing import Union, Optional, Callable, Literal

# local
import startai
from startai.utils.backend import current_backend
from startai.func_wrapper import (
    handle_array_function,
    handle_out_argument,
    to_native_arrays_and_back,
    handle_nestable,
    handle_array_like_without_promotion,
    handle_device,
    handle_complex_input,
    handle_backend_invalid,
)
from startai.utils.exceptions import handle_exceptions


def _gelu_jax_like(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    fn_original: Optional[Callable] = None,
    approximate: bool = False,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    # We don't have the exact implementation
    # cuz the erf function doesn't work on complex numbers
    return fn_original(x, approximate=True, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
@handle_complex_input
def gelu(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    approximate: bool = False,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the Gaussian error linear unit (GELU) activation function.

    Parameters
    ----------
    x
        Input array.
    approximate
        Whether to approximate, default is ``True``. An approximation is always used if
        the input array is complex.
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The input array with gelu applied element-wise.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([-1.2, -0.6, 1.5])
    >>> y = startai.gelu(x)
    >>> y
    startai.array([-0.138, -0.165, 1.4])

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([-1.3, 3.8, 2.1])
    >>> y = startai.gelu(x)
    >>> y
    startai.array([-0.126, 3.8, 2.06])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([1., 2.]), b=startai.array([-0.9, -1.]))
    >>> y = startai.gelu(x)
    >>> y
    {
        a: startai.array([0.841, 1.95]),
        b: startai.array([-0.166, -0.159])
    }
    """
    return current_backend(x).gelu(x, approximate=approximate, out=out)


gelu.jax_like = _gelu_jax_like


def _leaky_relu_jax_like(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    fn_original: Optional[Callable] = None,
    alpha: float = 0.2,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    return startai.where(
        (
            startai.logical_or(
                startai.real(x) < 0, startai.logical_and(startai.real(x) == 0, startai.imag(x) < 0)
            )
        ),
        startai.astype(x * alpha, x.dtype),
        x,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
@handle_complex_input
def leaky_relu(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    alpha: float = 0.2,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the leaky rectified linear unit function element-wise.

    If the input is complex, then by default each element is scaled by `alpha` if
    either its real part is strictly negative or if its real part is zero and its
    imaginary part is negative. This behaviour can be changed by specifying a different
    `complex_mode`.

    Parameters
    ----------
    x
        Input array.
    alpha
        Negative slope for ReLU.
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The input array with leaky relu applied element-wise.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0.39, -0.85])
    >>> y = startai.leaky_relu(x)
    >>> print(y)
    startai.array([ 0.39, -0.17])

    >>> x = startai.array([1.5, 0.7, -2.4])
    >>> y = startai.zeros(3)
    >>> startai.leaky_relu(x, out=y)
    >>> print(y)
    startai.array([ 1.5 ,  0.7 , -0.48])

    >>> x = startai.array([[1.1, 2.2, 3.3],
    ...                [-4.4, -5.5, -6.6]])
    >>> startai.leaky_relu(x, out=x)
    >>> print(x)
    startai.array([[ 1.1 ,  2.2 ,  3.3 ],
       [-0.88, -1.1 , -1.32]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0.0, -1.2]), b=startai.array([0.4, -0.2]))
    >>> x = startai.leaky_relu(x, out=x)
    >>> print(x)
    {
        a: startai.array([0., -0.24000001]),
        b: startai.array([0.40000001, -0.04])
    }
    """
    return current_backend(x).leaky_relu(x, alpha=alpha, out=out)


leaky_relu.jax_like = _leaky_relu_jax_like


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def log_softmax(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[int] = None,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the log_softmax function element-wise.

    Parameters
    ----------
    x
        Input array.
    axis
        The dimension log_softmax would be performed on. The default is ``None``.
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The output array with log_softmax applied element-wise to input.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([-1.0, -0.98])
    >>> y = startai.log_softmax(x)
    >>> print(y)
    startai.array([-0.703, -0.683])

    >>> x = startai.array([1.0, 2.0, 3.0])
    >>> y = startai.log_softmax(x)
    >>> print(y)
    startai.array([-2.41, -1.41, -0.408])

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([1.5, 0.5, 1.0])
    >>> y = startai.log_softmax(x)
    >>> print(y)
    startai.array([-0.68, -1.68, -1.18])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([1.5, 0.5, 1.0]))
    >>> y = startai.log_softmax(x)
    >>> print(y)
    {
        a: startai.array([-0.68, -1.68, -1.18])
    }

    >>> x = startai.Container(a=startai.array([1.0, 2.0]), b=startai.array([0.4, -0.2]))
    >>> y = startai.log_softmax(x)
    >>> print(y)
    {
        a: startai.array([-1.31, -0.313]),
        b: startai.array([-0.437, -1.04])
    }
    """
    return current_backend(x).log_softmax(x, axis=axis, out=out)


def _relu_jax_like(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    fn_original=None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    return startai.where(
        (
            startai.logical_or(
                startai.real(x) < 0, startai.logical_and(startai.real(x) == 0, startai.imag(x) < 0)
            )
        ),
        startai.array(0.0, dtype=x.dtype),
        x,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
@handle_complex_input
def relu(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the rectified linear unit function element-wise.

    If the input is complex, then by default each element is set to zero  if
    either its real part is strictly negative or if its real part is zero and its
    imaginary part is negative. This behaviour can be changed by specifying a different
    `complex_mode`.

    Parameters
    ----------
    x
        input array
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the rectified linear unit activation of each element in
        ``x``.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([-1., 0., 1.])
    >>> y = startai.relu(x)
    >>> print(y)
    startai.array([0., 0., 1.])

    >>> x = startai.array([1.5, 0.7, -2.4])
    >>> y = startai.zeros(3)
    >>> startai.relu(x, out = y)
    >>> print(y)
    startai.array([1.5, 0.7, 0.])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
    >>> x = startai.relu(x, out=x)
    >>> print(x)
    {
        a: startai.array([1., 0.]),
        b: startai.array([0.40000001, 0.])
    }
    """
    return current_backend(x).relu(x, out=out)


relu.jax_like = _relu_jax_like


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
@handle_complex_input
def sigmoid(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the sigmoid function element-wise.

    Parameters
    ----------
    x
        input array.
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        input broadcast to.
        default: None

    Returns
    -------
    ret
        an array containing the sigmoid activation of each element in ``x``.
        sigmoid activation of x is defined as 1/(1+exp(-x)).

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([-1.0, 1.0, 2.0])
    >>> y = startai.sigmoid(x)
    >>> print(y)
    startai.array([0.2689414 , 0.7310586 , 0.88079703])

    >>> x = startai.array([-1.0, 1.0, 2.0])
    >>> y = startai.zeros(3)
    >>> startai.sigmoid(x, out=y)
    >>> print(y)
    startai.array([0.2689414 , 0.7310586 , 0.88079703])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([0.]),
    ...                   b=startai.Container(c=startai.array([1.]),
    ...                                   d=startai.array([2.])))
    >>> y = startai.sigmoid(x)
    >>> print(y)
    {
        a: startai.array([0.5]),
        b: {
            c: startai.array([0.7310586]),
            d: startai.array([0.88079703])
        }
    }

    >>> x = startai.Container(a=startai.array([0.]),
    ...                   b=startai.Container(c=startai.array([1.]),
    ...                                   d=startai.array([2.])))
    >>> y = startai.Container(a=startai.array([0.]),
    ...                   b=startai.Container(c=startai.array([0.]),
    ...                                   d=startai.array([0.])))
    >>> startai.sigmoid(x, out=y)
    >>> print(y)
    {
        a: startai.array([0.5]),
        b: {
            c: startai.array([0.7310586]),
            d: startai.array([0.88079703])
        }
    }
    """
    return current_backend(x).sigmoid(x, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
@handle_complex_input
def softmax(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[int] = None,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the softmax function element-wise.

    Parameters
    ----------
    x
        Input array.
    axis
        The dimension softmax would be performed on. The default is ``None``.
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The input array with softmax applied element-wise.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1.0, 0, 1.0])
    >>> y = startai.softmax(x)
    >>> print(y)
    startai.array([0.422, 0.155, 0.422])

    >>> x = startai.array([[1.1, 2.2, 3.3],
    ...                [4.4, 5.5, 6.6]])
    >>> y = startai.softmax(x, axis = 1)
    >>> print(y)
    startai.array([[0.0768, 0.231 , 0.693 ],
               [0.0768, 0.231 , 0.693 ]])
    """
    return current_backend(x).softmax(x, axis=axis, out=out)


def _wrap_between(y, a):
    """Wrap y between [-a, a]"""
    a = startai.array(a, dtype=y.dtype)
    a2 = startai.array(2 * a, dtype=y.dtype)
    zero = startai.array(0, dtype=y.dtype)
    rem = startai.remainder(startai.add(y, a), a2)
    rem = startai.where(rem < zero, rem + a2, rem) - a
    return rem


def _softplus_jax_like(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    fn_original=None,
    beta: Optional[Union[int, float]] = None,
    threshold: Optional[Union[int, float]] = None,
    out: Optional[startai.Array] = None,
):
    if beta is not None:
        x_beta = startai.multiply(x, startai.array(beta, dtype=x.dtype))
    else:
        x_beta = x
    amax = startai.relu(x_beta)
    res = startai.subtract(x_beta, startai.multiply(amax, startai.array(2, dtype=x.dtype)))
    res = startai.add(amax, startai.log(startai.add(1, startai.exp(res))))
    res = startai.real(res) + _wrap_between(startai.imag(res), startai.pi).astype(
        x.dtype
    ) * startai.astype(1j, x.dtype)
    if beta is not None:
        res = startai.divide(res, startai.array(beta, dtype=x.dtype))
    if threshold is not None:
        res = startai.where(
            startai.real(x_beta) < threshold,
            res,
            x,
        ).astype(x.dtype)
    return res


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
@handle_complex_input
def softplus(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    beta: Optional[Union[int, float]] = None,
    threshold: Optional[Union[int, float]] = None,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the softplus function element-wise.

    If the input is complex, then by default we apply the softplus operation
    `log(1+ exp(x))` to  each element
    If threshold is set we check if either its real part is strictly negative or
    if its real part is zero and its imaginary part is negative then we apply
    `input×β > threshold`.

    Parameters
    ----------
    x
        input array.
    beta
        The beta value for the softplus formation. Default: ``None``.
    threshold
        values above this revert to a linear function
        If the input is complex, only its real part is considered. Default: ``None``
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the softplus activation of each element in ``x``.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([-0.3461, -0.6491])
    >>> y = startai.softplus(x)
    >>> print(y)
    startai.array([0.535,0.42])

    >>> x = startai.array([-0.3461, -0.6491])
    >>> y = startai.softplus(x, beta=0.5)
    >>> print(y)
    startai.array([1.22, 1.09])

    >>> x = startai.array([1., 2., 3.])
    >>> y = startai.softplus(x, threshold=2)
    >>> print(y)
    startai.array([1.31, 2.13, 3.  ])
    """
    return current_backend(x).softplus(x, beta=beta, threshold=threshold, out=out)


softplus.jax_like = _softplus_jax_like


# Softsign
@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def softsign(
    x: Union[startai.Array, startai.NativeArray],
    /,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the softsign function element-wise.

    Parameters
    ----------
    x
        Input array.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The input array with softsign applied element-wise.

    Examples
    --------
    With :class:`startai.Array` input:
    >>> x = startai.array([1.0, 2.0, 3.0])
    >>> y = startai.softsign(x)
    >>> print(y)
    startai.array([0.5, 0.66666667, 0.75])
    """
    return current_backend(x).softsign(x, out=out)


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
@handle_complex_input
def mish(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the mish activation function element-wise.

    Parameters
    ----------
    x
        input array
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the mish activation of each element in
        ``x``.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([-1., 0., 1.])
    >>> y = startai.mish(x)
    >>> print(y)
    startai.array([-0.30340147,  0.        ,  0.86509842])

    >>> x = startai.array([1.5, 0.7, -2.4])
    >>> y = startai.zeros(3)
    >>> startai.mish(x, out = y)
    >>> print(y)
    startai.array([ 1.40337825,  0.56114835, -0.20788449])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
    >>> x = startai.mish(x)
    >>> print(x)
    {
        a: startai.array([0.86509842, -0.30883577]),
        b: startai.array([0.28903052, -0.10714479])
    }
    """
    return current_backend(x).mish(x, out=out)


def _hardswish_jax_like(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    fn_original=None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    def hard_sigmoid(x):
        return startai.relu6(x + 3.0) / 6

    return startai.multiply(x, hard_sigmoid(x).astype(x.dtype))


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_complex_input
def hardswish(
    x: Union[startai.Array, startai.NativeArray],
    /,
    *,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply the hardswish activation function element-wise.

    Parameters
    ----------
    x
        input array
    complex_mode
        optional specifier for how to handle complex data types. See
        ``startai.func_wrapper.handle_complex_input`` for more detail.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the hardswish activation of each element in ``x``.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0., 0., 4.])
    >>> y = startai.hardswish(x)
    >>> y
    startai.array([0., 0., 4.])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([-3., 4., 5.]), b=startai.array([0., 5.]))
    >>> x = startai.hardswish(x, out=x)
    >>> x
    {
        a: startai.array([-0.,  4.,  5.]),
        b: startai.array([0., 5.])
    }
    """
    return current_backend(x).hardswish(x, out=out)


hardswish.jax_like = _hardswish_jax_like
