"""Collection of Startai normalization functions."""

# local
from typing import List, Union, Optional
import startai
from startai.func_wrapper import (
    handle_array_like_without_promotion,
    handle_nestable,
    handle_array_function,
    inputs_to_startai_arrays,
)
from startai.utils.exceptions import handle_exceptions


# Extra #
# ------#


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def layer_norm(
    x: Union[startai.Array, startai.NativeArray],
    normalized_idxs: List[int],
    /,
    *,
    scale: Optional[Union[startai.Array, startai.NativeArray]] = None,
    offset: Optional[Union[startai.Array, startai.NativeArray]] = None,
    eps: float = 1e-05,
    new_std: float = 1.0,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply Layer Normalization over a mini-batch of inputs.

    Parameters
    ----------
    x
        Input array
    normalized_idxs
        Indices to apply the normalization to.
    scale
        Learnable gamma variables for elementwise post-multiplication,
        default is ``None``.
    offset
        Learnable beta variables for elementwise post-addition, default is ``None``.
    eps
        small constant to add to the denominator. Default is ``1e-05``
    new_std
        The standard deviation of the new normalized values. Default is ``1``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
     ret
        The layer after applying layer normalization.

    Examples
    --------
    With :class:`startai.Array` input:
    >>> x = startai.array([[1.0, 2.0], [3.0, 4.0]])
    >>> y = startai.layer_norm(x, [0, 1], new_std=2.0)
    >>> print(y)
    startai.array([[-2.68 , -0.894],
               [ 0.894,  2.68 ]])
    >>> x = startai.array([[1., 2., 3.], [4., 5., 6.]])
    >>> y = startai.zeros((2, 3))
    >>> startai.layer_norm(x, [0], out=y)
    >>> print(y)
    startai.array([[-1., -1., -1.],
               [ 1.,  1.,  1.]])
    >>> x = startai.array([[0.0976, -0.3452,  1.2740],
    ...                [0.1047,  0.5886,  1.2732],
    ...                [0.7696, -1.7024, -2.2518]])
    >>> y = startai.layer_norm(x, [0, 1], eps=0.001,
    ...                       new_std=1.5, scale=0.5, offset=[0.5, 0.02, 0.1])
    >>> print(y)
    startai.array([[ 0.826, -0.178, 0.981 ],
               [ 0.831,  0.421, 0.981 ],
               [ 1.26 , -1.05 , -1.28 ]])
    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:
    >>> x = startai.array([[1., 2., 3.], [4., 5., 6.]])
    >>> normalized_idxs = startai.Container({'a': [0], 'b': [1]})
    >>> y = startai.layer_norm(x, normalized_idxs, new_std=1.25, offset=0.2)
    >>> print(y)
    {
        a: startai.array([[-1.25, -1.25, -1.25],
                      [1.25, 1.25, 1.25]]),
        b: startai.array([[-1.53, 0., 1.53],
                      [-1.53, 0., 1.53]])
    }
    With one :class:`startai.Container` input:
    >>> x = startai.Container({'a': startai.array([7., 10., 12.]),
    ...                    'b': startai.array([[1., 2., 3.], [4., 5., 6.]])})
    >>> normalized_idxs = [0]
    >>> y = startai.layer_norm(x, normalized_idxs, eps=1.25, scale=0.3)
    >>> print(y)
    {
        a: startai.array([-0.34198591, 0.04274819, 0.29923761]),
        b: startai.array([[-0.24053511, -0.24053511, -0.24053511],
                      [0.24053511, 0.24053511, 0.24053511]])
    }

    With multiple :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([7.0, 10.0, 12.0]),
    ...                   b=startai.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
    >>> normalized_idxs = startai.Container(a=[0], b=[1])
    >>> new_std = startai.Container(a=1.25, b=1.5)
    >>> bias = startai.Container(a=[0.2, 0.5, 0.7], b=0.3)
    >>> y = startai.layer_norm(x, normalized_idxs, new_std=new_std, offset=0.2)
    >>> print(y)
    {
        a: startai.array([-1.62, 0.203, 1.42]),
        b: startai.array([[-1.84, 0., 1.84],
                      [-1.84, 0., 1.84]])
    }
    # Both the description and the type hints above assumes an array input for
    simplicity, but this function is *nestable*, and therefore also accepts
    :class:`startai.Container` instances in place of any of the arguments.
    """
    mean = startai.mean(x, axis=normalized_idxs, keepdims=True)
    var = startai.var(x, axis=normalized_idxs, keepdims=True)

    x = (x - mean) / (var + eps) ** 0.5

    if scale is not None:
        if offset is not None:
            return startai.multiply(
                startai.add(startai.multiply(x, scale), offset), new_std, out=out
            )
        return startai.multiply(startai.multiply(x, scale), new_std, out=out)

    return startai.multiply(x, new_std, out=out)


layer_norm.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "handle_out_argument",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}
