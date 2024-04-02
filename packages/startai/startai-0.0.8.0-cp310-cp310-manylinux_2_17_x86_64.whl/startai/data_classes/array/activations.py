# global
import abc
from typing import Optional, Union, Literal

# local
import startai


# ToDo: implement all methods here as public instance methods


class _ArrayWithActivations(abc.ABC):
    def relu(
        self: startai.Array,
        /,
        *,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.relu. This method simply
        wraps the function, and so the docstring for startai.relu also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the relu activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.relu()
        >>> print(y)
        startai.array([0., 0., 1.])
        """
        return startai.relu(self._data, complex_mode=complex_mode, out=out)

    def leaky_relu(
        self: startai.Array,
        /,
        *,
        alpha: float = 0.2,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.leaky_relu. This method
        simply wraps the function, and so the docstring for startai.leaky_relu also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        alpha
            the slope of the negative section.
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the leaky relu activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([0.39, -0.85])
        >>> y = x.leaky_relu()
        >>> print(y)
        startai.array([ 0.39, -0.17])
        """
        return startai.leaky_relu(
            self._data, alpha=alpha, complex_mode=complex_mode, out=out
        )

    def gelu(
        self: startai.Array,
        /,
        *,
        approximate: bool = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.gelu. This method simply
        wraps the function, and so the docstring for startai.gelu also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        approximate
            whether to use the approximate version of the gelu function.
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the gelu activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([-1.2, -0.6, 1.5])
        >>> y = x.gelu()
        >>> print(y)
        startai.array([-0.138, -0.165, 1.4])
        """
        return startai.gelu(
            self._data, approximate=approximate, complex_mode=complex_mode, out=out
        )

    def sigmoid(
        self: startai.Array,
        /,
        *,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.sigmoid.

        This method simply wraps the function, and so the docstring for startai.sigmoid also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array for writing the result to. It must have the same shape
            the input broadcast to default: None

        Returns
        -------
        ret
            an array with the sigmoid activation function applied element-wise.


        Examples
        --------
        >>> x = startai.array([-1., 1., 2.])
        >>> y = x.sigmoid()
        >>> print(y)
        startai.array([0.269, 0.731, 0.881])
        """
        return startai.sigmoid(self._data, complex_mode=complex_mode, out=out)

    def softmax(
        self: startai.Array,
        /,
        *,
        axis: Optional[int] = None,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.softmax. This method simply
        wraps the function, and so the docstring for startai.softmax also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        axis
            the axis or axes along which the softmax should be computed
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the softmax activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([1.0, 0, 1.0])
        >>> y = x.softmax()
        >>> print(y)
        startai.array([0.422, 0.155, 0.422])
        """
        return startai.softmax(self._data, axis=axis, complex_mode=complex_mode, out=out)

    def softplus(
        self: startai.Array,
        /,
        *,
        beta: Optional[Union[int, float]] = None,
        threshold: Optional[Union[int, float]] = None,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.softplus. This method
        simply wraps the function, and so the docstring for startai.softplus also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        beta
            the beta parameter of the softplus function.
        threshold
            the threshold parameter of the softplus function.
        complex_mode
           optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to. It must have a shape

        Returns
        -------
        ret
            an array with the softplus activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([-0.3461, -0.6491])
        >>> y = x.softplus()
        >>> print(y)
        startai.array([0.535,0.42])

        >>> x = startai.array([-0.3461, -0.6491])
        >>> y = x.softplus(beta=0.5)
        >>> print(y)
        startai.array([1.22, 1.09])

        >>> x = startai.array([1.31, 2., 2.])
        >>> y = x.softplus(threshold=2, out=x)
        >>> print(x)
        startai.array([1.55, 2.13, 2.13])
        """
        return startai.softplus(
            self._data,
            beta=beta,
            threshold=threshold,
            complex_mode=complex_mode,
            out=out,
        )

    def log_softmax(
        self: startai.Array,
        /,
        *,
        axis: Optional[int] = -1,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.log_softmax. This method
        simply wraps the function, and so the docstring for startai.log_softmax
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        axis
            the axis or axes along which the log_softmax should be computed
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the log_softmax activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([-1.0, -0.98, 2.3])
        >>> y = x.log_softmax()
        >>> print(y)
        startai.array([-3.37, -3.35, -0.0719])

        >>> x = startai.array([2.0, 3.4, -4.2])
        >>> y = x.log_softmax(x)
        startai.array([-1.62, -0.221, -7.82 ])
        """
        return startai.log_softmax(
            self._data,
            axis=axis,
            complex_mode=complex_mode,
            out=out,
        )

    def mish(
        self: startai.Array,
        /,
        *,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.mish. This method simply
        wraps the function, and so the docstring for startai.mish also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Examples
        --------
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.mish()
        >>> print(y)
        startai.array([-0.30340147,  0.        ,  0.86509842])
        """
        return startai.mish(self._data, complex_mode=complex_mode, out=out)

    def hardswish(
        self: startai.Array,
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
            optional output array, for writing the result to. It must have
            a shape that the inputs broadcast to.

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
        return startai.hardswish(self._data, complex_mode=complex_mode, out=out)
