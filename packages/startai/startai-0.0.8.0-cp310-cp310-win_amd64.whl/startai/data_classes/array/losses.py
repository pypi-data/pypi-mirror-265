# global
import abc
from typing import Optional, Union

# local
import startai


class _ArrayWithLosses(abc.ABC):
    def cross_entropy(
        self: startai.Array,
        pred: Union[startai.Array, startai.NativeArray],
        /,
        *,
        axis: int = -1,
        epsilon: float = 1e-7,
        reduction: str = "mean",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.cross_entropy. This method
        simply wraps the function, and so the docstring for startai.cross_entropy
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array containing true labels.
        pred
            input array containing the predicted labels.
        axis
            the axis along which to compute the cross-entropy. If axis is ``-1``,
            the cross-entropy will be computed along the last dimension.
            Default: ``-1``.
        epsilon
            a float in [0.0, 1.0] specifying the amount of smoothing when calculating
            the loss. If epsilon is ``0``, no smoothing will be applied.
            Default: ``1e-7``.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The cross-entropy loss between the given distributions.

        Examples
        --------
        >>> x = startai.array([0, 0, 1, 0])
        >>> y = startai.array([0.25, 0.25, 0.25, 0.25])
        >>> z = x.cross_entropy(y)
        >>> print(z)
        startai.array(0.34657359)
        """
        return startai.cross_entropy(
            self._data, pred, axis=axis, epsilon=epsilon, reduction=reduction, out=out
        )

    def binary_cross_entropy(
        self: startai.Array,
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
        """startai.Array instance method variant of startai.binary_cross_entropy. This
        method simply wraps the function, and so the docstring for
        startai.binary_cross_entropy also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            input array containing true labels.
        pred
            input array containing Predicted labels.
        from_logits
            Whether `pred` is expected to be a logits tensor. By
            default, we assume that `pred` encodes a probability distribution.
        epsilon
            a float in [0.0, 1.0] specifying the amount of smoothing when calculating
            the loss. If epsilon is ``0``, no smoothing will be applied. Default: ``0``.
        reduction
            ``'none'``: No reduction will be applied to the output.
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed. Default: ``'none'``.
        pos_weight
            a weight for positive examples. Must be an array with length equal
            to the number of classes.
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
        >>> x = startai.array([1 , 1, 0])
        >>> y = startai.array([0.7, 0.8, 0.2])
        >>> z = x.binary_cross_entropy(y)
        >>> print(z)
        startai.array(0.26765382)
        """
        return startai.binary_cross_entropy(
            self._data,
            pred,
            from_logits=from_logits,
            epsilon=epsilon,
            reduction=reduction,
            pos_weight=pos_weight,
            axis=axis,
            out=out,
        )

    def sparse_cross_entropy(
        self: startai.Array,
        pred: Union[startai.Array, startai.NativeArray],
        /,
        *,
        axis: int = -1,
        epsilon: float = 1e-7,
        reduction: str = "mean",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.sparse_cross_entropy. This
        method simply wraps the function, and so the docstring for
        startai.sparse_cross_entropy also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            input array containing the true labels as logits.
        pred
            input array containing the predicted labels as logits.
        axis
            the axis along which to compute the cross-entropy. If axis is ``-1``, the
            cross-entropy will be computed along the last dimension. Default: ``-1``.
            epsilon
            a float in [0.0, 1.0] specifying the amount of smoothing when calculating
            the loss. If epsilon is ``0``, no smoothing will be applied.
            Default: ``1e-7``.
        epsilon
            a float in [0.0, 1.0] specifying the amount of smoothing when calculating
            the loss. If epsilon is ``0``, no smoothing will be applied. Default:
            ``1e-7``.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The sparse cross-entropy loss between the given distributions.

        Examples
        --------
        >>> x = startai.array([1 , 1, 0])
        >>> y = startai.array([0.7, 0.8, 0.2])
        >>> z = x.sparse_cross_entropy(y)
        >>> print(z)
        startai.array([0.07438118, 0.07438118, 0.11889165])
        """
        return startai.sparse_cross_entropy(
            self._data, pred, axis=axis, epsilon=epsilon, reduction=reduction, out=out
        )
