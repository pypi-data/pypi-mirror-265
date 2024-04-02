"""Collection of Startai loss functions."""

# local
import startai
from typing import Optional, Union
from startai.func_wrapper import (
    handle_array_function,
    handle_nestable,
    handle_array_like_without_promotion,
    inputs_to_startai_arrays,
)
from startai.utils.exceptions import handle_exceptions


# Helpers #
# ------- #


def _reduce_loss(red, loss, axis, out):
    if red == "sum":
        return startai.negative(startai.sum(loss, axis=axis), out=out)
    elif red == "mean":
        return startai.negative(startai.mean(loss, axis=axis), out=out)
    else:
        return startai.negative(loss, out=out)


# Extra #
# ------#


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def cross_entropy(
    true: Union[startai.Array, startai.NativeArray],
    pred: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: Optional[int] = None,
    epsilon: float = 1e-7,
    reduction: str = "mean",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute cross-entropy between predicted and true discrete distributions.

    Parameters
    ----------
    true
        input array containing true labels.
    pred
        input array containing the predicted labels.
    axis
        the axis along which to compute the cross-entropy. If axis is ``-1``,
        the cross-entropy will be computed along the last dimension. Default: ``-1``.
    epsilon
        a float in [0.0, 1.0] specifying the amount of smoothing when calculating
        the loss. If epsilon is ``0``, no smoothing will be applied. Default: ``1e-7``.
    out
        optional output array, for writing the result to. It must have a shape
        that the inputs broadcast to.

    Returns
    -------
    ret
        The cross-entropy loss between the given distributions

    Examples
    --------
    >>> x = startai.array([0, 0, 1, 0])
    >>> y = startai.array([0.25, 0.25, 0.25, 0.25])
    >>> print(startai.cross_entropy(x, y))
    startai.array(0.34657359)

    >>> z = startai.array([0.1, 0.1, 0.7, 0.1])
    >>> print(startai.cross_entropy(x, z))
    startai.array(0.08916873)
    """
    startai.utils.assertions.check_elem_in_list(reduction, ["none", "sum", "mean"])
    pred = startai.clip(pred, epsilon, 1 - epsilon)
    log_pred = startai.log(pred)
    return _reduce_loss(reduction, log_pred * true, axis, out)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def binary_cross_entropy(
    true: Union[startai.Array, startai.NativeArray],
    pred: Union[startai.Array, startai.NativeArray],
    /,
    *,
    from_logits: bool = False,
    epsilon: float = 0.0,
    reduction: str = "mean",
    pos_weight: Optional[Union[startai.Array, startai.NativeArray]] = None,
    axis: Optional[int] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute the binary cross entropy loss.

    Parameters
    ----------
    true
        input array containing true labels.
    pred
        input array containing Predicted labels.
    from_logits
        Whether `pred` is expected to be a logits tensor. By
        default, we assume that `pred` encodes a probability distribution.
    epsilon
        a float in [0.0, 1.0] specifying the amount of smoothing when calculating the
        loss. If epsilon is ``0``, no smoothing will be applied. Default: ``0``.
    reduction
        ``'none'``: No reduction will be applied to the output.
        ``'mean'``: The output will be averaged.
        ``'sum'``: The output will be summed. Default: ``'none'``.
    pos_weight
        a weight for positive examples. Must be an array with length equal to the number
        of classes.
    axis
        Axis along which to compute crossentropy.
    out
        optional output array, for writing the result to. It must have a shape
        that the inputs broadcast to.

    Returns
    -------
    ret
        The binary cross entropy between the given distributions.


    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([0, 1, 0, 0])
    >>> y = startai.array([0.2, 0.8, 0.3, 0.8])
    >>> z = startai.binary_cross_entropy(x, y)
    >>> print(z)
    startai.array(0.60309976)

    >>> x = startai.array([[0, 1, 1, 0]])
    >>> y = startai.array([[2.6, 6.2, 3.7, 5.3]])
    >>> z = startai.binary_cross_entropy(x, y, reduction='mean')
    >>> print(z)
    startai.array(7.6666193)

    >>> x = startai.array([[0, 1, 1, 0]])
    >>> y = startai.array([[2.6, 6.2, 3.7, 5.3]])
    >>> pos_weight = startai.array([1, 2, 3, 4])
    >>> z = startai.binary_cross_entropy(x, y, pos_weight=pos_weight, from_logits=True)
    startai.array(2.01348412)

    >>> x = startai.array([[0, 1, 1, 0]])
    >>> y = startai.array([[2.6, 6.2, 3.7, 5.3]])
    >>> pos_weight = startai.array([1, 2, 3, 4])
    >>> z = startai.binary_cross_entropy(x, y, pos_weight=pos_weight, from_logits=True, reduction='sum', axis=1)
    >>> print(z)
    startai.array([8.05393649])

    >>> x = startai.array([[0, 1, 1, 0]])
    >>> y = startai.array([[2.6, 6.2, 3.7, 5.3]])
    >>> z = startai.binary_cross_entropy(x, y, reduction='none', epsilon=0.5)
    >>> print(z)
    startai.array([[11.49992943,  3.83330965,  3.83330965, 11.49992943]])

    >>> x = startai.array([[0, 1, 0, 0]])
    >>> y = startai.array([[0.6, 0.2, 0.7, 0.3]])
    >>> z = startai.binary_cross_entropy(x, y, epsilon=1e-3)
    >>> print(z)
    startai.array(1.02136981)

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([0, 1, 0, 1])
    >>> y = startai.native_array([0.2, 0.7, 0.2, 0.6])
    >>> z = startai.binary_cross_entropy(x, y)
    >>> print(z)
    startai.array(0.32844672)

    With a mix of :class:`startai.Array` and :class:`startai.NativeArray` inputs:

    >>> x = startai.array([0, 0, 1, 1])
    >>> y = startai.native_array([0.1, 0.2, 0.8, 0.6])
    >>> z = startai.binary_cross_entropy(x, y)
    >>> print(z)
    startai.array(0.26561815)

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([1, 0, 0]),b=startai.array([0, 0, 1]))
    >>> y = startai.Container(a=startai.array([0.6, 0.2, 0.3]),b=startai.array([0.8, 0.2, 0.2]))
    >>> z = startai.binary_cross_entropy(x, y)
    >>> print(z)
    {
        a: startai.array(0.36354783),
        b: startai.array(1.14733934)
    }

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.array([1 , 1, 0])
    >>> y = startai.Container(a=startai.array([0.7, 0.8, 0.2]))
    >>> z = startai.binary_cross_entropy(x, y)
    >>> print(z)
    {
       a: startai.array(0.26765382)
    }

    Instance Method Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Using :class:`startai.Array` instance method:

    >>> x = startai.array([1, 0, 0, 0])
    >>> y = startai.array([0.8, 0.2, 0.2, 0.2])
    >>> z = startai.binary_cross_entropy(x, y)
    >>> print(z)
    startai.array(0.22314337)
    """  # noqa: E501
    startai.utils.assertions.check_elem_in_list(reduction, ["none", "sum", "mean"])

    if not (0.0 <= epsilon <= 1.0):
        raise ValueError("epsilon should be a float in [0, 1]")

    if not from_logits and pos_weight is not None:
        raise ValueError("pos_weight is only allowed when from_logits is set to True")

    true = true.astype(pred.dtype)

    epsilon = startai.asarray(epsilon, dtype=pred.dtype)

    true = true * (1.0 - epsilon) + 0.5 * epsilon

    if from_logits:
        if pos_weight is not None:
            num_classes = pred.shape[0] if len(pred.shape) == 1 else pred.shape[1]
            if pos_weight.shape[0] != num_classes:
                raise ValueError(
                    "pos_weight must have the same size as the number of classes in"
                    " pred at non-singleton dimension 1"
                )
            epsilon_ = 1e-7
            pred = startai.sigmoid(pred)
            pred = startai.clip(pred, epsilon_, 1 - epsilon_)
            loss = -(
                true * -startai.log(pred) * pos_weight + (1 - true) * -startai.log(1 - pred)
            )
        else:
            zeros = startai.zeros_like(pred, dtype=pred.dtype)
            cond = pred >= zeros
            relu_logits = startai.where(cond, pred, zeros)
            neg_abs_logits = startai.where(cond, -pred, pred)
            loss = (
                startai.add(relu_logits - pred * true, startai.log1p(startai.exp(neg_abs_logits)))
                * -1
            )
    else:
        epsilon_ = 1e-7
        pred = startai.clip(pred, epsilon_, 1 - epsilon_)
        loss = true * startai.log(pred + epsilon_) + (1 - true) * startai.log(
            1 - pred + epsilon_
        )

    return _reduce_loss(reduction, loss, axis, out)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def sparse_cross_entropy(
    true: Union[startai.Array, startai.NativeArray],
    pred: Union[startai.Array, startai.NativeArray],
    /,
    *,
    axis: int = -1,
    epsilon: float = 1e-7,
    reduction: str = "mean",
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute sparse cross entropy between logits and labels.

    Parameters
    ----------
    true
     input array containing the true labels as logits.
    pred
     input array containing the predicted labels as logits.
    axis
     the axis along which to compute the cross-entropy. If axis is ``-1``, the
     cross-entropy will be computed along the last dimension. Default: ``-1``.
    epsilon
     a float in [0.0, 1.0] specifying the amount of smoothing when calculating the
     loss. If epsilon is ``0``, no smoothing will be applied. Default: ``1e-7``.
    out
     optional output array, for writing the result to. It must have a shape
     that the inputs broadcast to.

    Returns
    -------
    ret
        The sparse cross-entropy loss between the given distributions

    Examples
    --------
    With :class:`startai.Array` input:

    >> x = startai.array([2])
    >> y = startai.array([0.1, 0.1, 0.7, 0.1])
    >> print(startai.sparse_cross_entropy(x, y))
    startai.array([0.08916873])

    >>> x = startai.array([3])
    >>> y = startai.array([0.1, 0.1, 0.7, 0.1])
    >>> print(startai.cross_entropy(x, y))
    startai.array(5.44832274)

    >>> x = startai.array([2,3])
    >>> y = startai.array([0.1, 0.1])
    >>> print(startai.cross_entropy(x, y))
    startai.array(5.75646281)

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([4])
    >>> y = startai.native_array([0.1, 0.2, 0.1, 0.1, 0.5])
    >>> print(startai.sparse_cross_entropy(x, y))
    startai.array([0.13862944])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([4]))
    >>> y = startai.Container(a=startai.array([0.1, 0.2, 0.1, 0.1, 0.5]))
    >>> print(startai.sparse_cross_entropy(x, y))
    {
        a: startai.array([0.13862944])
    }

    With a mix of :class:`startai.Array` and :class:`startai.NativeArray` inputs:

    >>> x = startai.array([0])
    >>> y = startai.native_array([0.1, 0.2, 0.6, 0.1])
    >>> print(startai.sparse_cross_entropy(x,y))
    startai.array([0.57564628])

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.array([0])
    >>> y = startai.Container(a=startai.array([0.1, 0.2, 0.6, 0.1]))
    >>> print(startai.sparse_cross_entropy(x,y))
    {
        a: startai.array([0.57564628])
    }

    Instance Method Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~
    With :class:`startai.Array` input:

    >>> x = startai.array([2])
    >>> y = startai.array([0.1, 0.1, 0.7, 0.1])
    >>> print(x.sparse_cross_entropy(y))
    startai.array([0.08916873])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([2]))
    >>> y = startai.Container(a=startai.array([0.1, 0.1, 0.7, 0.1]))
    >>> print(x.sparse_cross_entropy(y))
    {
        a: startai.array([0.08916873])
    }
    """
    startai.utils.assertions.check_elem_in_list(reduction, ["none", "sum", "mean"])
    true = startai.one_hot(true, pred.shape[axis])
    return startai.cross_entropy(
        true, pred, axis=axis, epsilon=epsilon, reduction=reduction, out=out
    )
