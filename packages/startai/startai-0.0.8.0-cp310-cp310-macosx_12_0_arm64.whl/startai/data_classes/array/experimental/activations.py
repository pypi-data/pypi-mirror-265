# global
import abc
from typing import Optional, Union, Literal

# local
import startai


class _ArrayWithActivationsExperimental(abc.ABC):
    def logit(
        self,
        /,
        *,
        eps: Optional[float] = None,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.logit. This method simply
        wraps the function, and so the docstring for startai.logit also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        eps
            When eps is None the function outputs NaN where x < 0 or x > 1.
            and inf or -inf where x = 1 or x = 0, respectively.
            Otherwise if eps is defined, x is clamped to [eps, 1 - eps]
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            Optional output array.

        Returns
        -------
        ret
            Array containing elementwise logits of x.

        Examples
        --------
        >>> x = startai.array([1, 0, 0.9])
        >>> z = x.logit()
        >>> print(z)
        startai.array([       inf,       -inf, 2.19722438])

        >>> x = startai.array([1, 2, -0.9])
        >>> z = x.logit(eps=0.2)
        >>> print(z)
        startai.array([ 1.38629448,  1.38629448, -1.38629436])
        """
        return startai.logit(self, eps=eps, complex_mode=complex_mode, out=out)

    def thresholded_relu(
        self: startai.Array,
        /,
        *,
        threshold: Union[int, float] = 0,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.thresholded_relu. This
        method simply wraps the function, and so the docstring for
        startai.thresholded_relu also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        threshold
            threshold value above which the activation is linear. Default: ``0``.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the relu activation function applied element-wise
            with custom threshold.

        Examples
        --------
        >>> x = startai.array([-1., .2, 1.])
        >>> y = x.thresholded_relu(threshold=0.5)
        >>> print(y)
        startai.array([0., 0., 1.])
        """
        return startai.thresholded_relu(self._data, threshold=threshold, out=out)

    def prelu(
        self,
        slope: Union[float, startai.NativeArray, startai.Array],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """Prelu takes input data (Array) and slope array as input,

        and produces one output data (array) where the function
        f(x) = slope * x for x < 0, f(x) = x for x >= 0., is applied
        to the data array elementwise. This operator supports unidirectional
        broadcasting (array slope should be unidirectional broadcastable to
        input tensor X);

        Parameters
        ----------
        self
            input array.
        slope
            Slope Array. The shape of slope can be smaller than first input X;
            if so, its shape must be unidirectional broadcastable to X.
        out
            Optional output array.

        Returns
        -------
        ret
            input array with prelu applied elementwise.
        """
        return startai.prelu(self._data, slope, out=out)

    def relu6(
        self,
        /,
        *,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """Apply the rectified linear unit 6 function element-wise.

        Parameters
        ----------
        self
            input array
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rectified linear unit 6 activation
            of each element in input.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x = startai.array([-1.,  0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.])
        >>> y = startai.relu6(x)
        >>> print(y)
        startai.array([0., 0., 1., 2., 3., 4., 5., 6., 6.])

        >>> x = startai.array([-1.,  0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.])
        >>> y = startai.zeros(9)
        >>> startai.relu6(x, out = y)
        >>> print(y)
        startai.array([0., 0., 1., 2., 3., 4., 5., 6., 6.])
        """
        return startai.relu6(self._data, complex_mode=complex_mode, out=out)

    def logsigmoid(
        self: startai.Array,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    ) -> startai.Array:
        """startai.Array instance method variant of startai.logsigmoid. This method
        simply wraps the function, and so the docstring for startai.logsigmoid also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.

        Returns
        -------
            Array with same shape as input with Log-sigmoid applied to every element.

        Examples
        --------
        >>> x = startai.array([-1., 2., 4., -10.])
        >>> z = x.logsigmoid()
        >>> print(z)
        startai.array([ -1.31326175,  -0.126928  ,  -0.01814993, -10.00004578])

        >>> x = startai.array([-2.5, 1., 0, 4.5])
        >>> z = x.logsigmoid()
        >>> print(z)
        startai.array([-2.57888985, -0.31326169, -0.69314718, -0.01104775])
        """
        return startai.logsigmoid(self._data, complex_mode=complex_mode)

    def selu(self, /, *, out: Optional[startai.Array] = None) -> startai.Array:
        """Apply the scaled exponential linear unit function element-wise.

        Parameters
        ----------
        self
            input array
        out
            optional output array, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the scaled exponential linear unit activation
            of each element in input.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x = startai.array([-1.,  0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.])
        >>> y = x.selu()
        >>> print(y)
        startai.array([-1.11133075,  0.,  1.05070102,  2.10140204,  3.15210295,
                    4.20280409,  5.25350523,  6.30420589,  7.35490704])

        >>> x = startai.array([-1.,  0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.])
        >>> y = startai.zeros(9)
        >>> x.selu(out = y)
        >>> print(y)
        startai.array([-1.11133075,  0.,  1.05070102,  2.10140204,  3.15210295,
                    4.20280409,  5.25350523,  6.30420589,  7.35490704])
        """
        return startai.selu(self._data, out=out)

    def silu(self: startai.Array, /, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.silu. This method simply
        wraps the function, and so the docstring for startai.silu also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Examples
        --------
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.silu()
        >>> print(y)
        startai.array([-0.26894143,  0.        ,  0.73105854])
        """
        return startai.silu(self._data, out=out)

    def elu(
        self,
        /,
        *,
        alpha: float = 1.0,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """Startai.Array instance method variant of startai.elu. This method simply
        wraps the function, and so the docstring for startai.elu also applies to
        this method with minimal.

        Parameters
        ----------
        self
            input array.
        alpha
            scaler for controlling the slope of the function for x <= 0 Default: 1.0
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the elu activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([0.39, -0.85])
        >>> y = x.elu()
        >>> print(y)
        startai.array([ 0.39, -0.57])
        """
        return startai.elu(self._data, alpha=alpha, out=out)

    def hardtanh(
        self: startai.Array,
        /,
        *,
        max_val: float = 1,
        min_val: float = -1,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.hardtanh. This method
        simply wraps the function, and so the docstring for startai.hardtanh also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        min_val
            minimum value of the linear region range. Default: -1.
        max_val
            maximum value of the linear region range. Default: 1.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the hardtanh activation function applied element-wise
            with custom linear region range.

        Examples
        --------
        >>> x = startai.array([-1., .2, 1.])
        >>> y = x.hardtanh()
        >>> print(y)
        startai.array([-1. ,  0.2,  1. ])
        """
        return startai.hardtanh(self._data, min_val=min_val, max_val=max_val, out=out)

    def tanhshrink(self: startai.Array, /, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.tanhshrink. This method
        simply wraps the function, and so the docstring for startai.tanhshrink also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Examples
        --------
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.tanhshrink()
        >>> print(y)
        startai.array([-0.23840582,  0.        ,  0.23840582])
        """
        return startai.tanhshrink(self._data, out=out)

    def threshold(
        self: startai.Array,
        /,
        *,
        threshold: Union[int, float],
        value: Union[int, float],
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.threshold. This method
        simply wraps the function, and so the docstring for startai.threshold also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        threshold
            threshold value for thresholding operation.
        value
            value to replace with if thresholding condition is not met.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the thresholding function applied element-wise.

        Examples
        --------
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.hreshold(threshold=0.5, value=0.0)
        >>> print(y)
        startai.array([0.5, 0.5 , 1. ])
        """
        return startai.threshold(self._data, threshold=threshold, value=value, out=out)

    def softshrink(
        self: startai.Array,
        /,
        *,
        lambd: float = 0.5,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.softshrink. This method
        simply wraps the function, and so the docstring for startai.softshrink also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        lambd
            the value of the lower bound of the linear region range.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the softshrink activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.softshrink()
        >>> print(y)
        startai.array([-0.5,  0. ,  0.5])
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.softshrink(lambd=1.0)
        >>> print(y)
        startai.array([0., 0., 0.])
        """
        return startai.softshrink(self._data, lambd=lambd, out=out)

    def celu(
        self: startai.Array,
        /,
        *,
        alpha: float = 1.0,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.celu. This method simply
        wraps the function, and so the docstring for startai.celu also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        alpha
            the alpha (negative slope) value for CELU formulation.
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the celu activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([0.39, -0.85])
        >>> y = x.celu()
        >>> print(y)
        startai.array([ 0.39, -0.57])
        """
        return startai.celu(self._data, alpha=alpha, complex_mode=complex_mode, out=out)

    def scaled_tanh(
        self: startai.Array,
        /,
        *,
        alpha: float = 1.7159,
        beta: float = 0.67,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.scaled_tanh. This method
        simply wraps the function, and so the docstring for startai.scaled_tanh
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        alpha
            The scaling parameter for the output.
            Determines the amplitude of the tanh function.
            Default: 1.7159
        beta
            The scaling parameter for the input.
            Determines the slope of the tanh function.
            Default: 0.67
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array after applying the scaled_tanh activation.

        Examples
        --------
        >>> x = startai.array([-3., 2., 3.])
        >>> x.scaled_tanh()
        startai.array([-1.65537548,  1.49570239,  1.65537548])

        >>> x = startai.array([2., 2., 2.])
        >>> x.scaled_tanh(alpha=9, beta=0.1)
        startai.array([1.77637792, 1.77637792, 1.77637792])

        >>> x = startai.array([2., 2., 2.])
        >>> x.scaled_tanh(alpha=0.1, beta=9)
        startai.array([0.1, 0.1, 0.1])
        """
        return startai.scaled_tanh(self._data, alpha=alpha, beta=beta, out=out)

    def hardshrink(
        self: startai.Array,
        /,
        *,
        lambd: float = 0.5,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.hardshrink. This method
        simply wraps the function, and so the docstring for startai.hardshrink also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        lambd
            the lambd value for the Hardshrink formulation
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an array with the hardshrink activation function applied element-wise.

        Examples
        --------
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.hardshrink()
        >>> print(y)
        startai.array([-1.,  0.,  1.])
        >>> x = startai.array([-1., 0., 1.])
        >>> y = x.hardshrink(lambd=1.0)
        >>> print(y)
        startai.array([0., 0., 0.])
        """
        return startai.hardshrink(self._data, lambd=lambd, out=out)

    def hardsilu(self, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method which acts as a wrapper for startai.hardsilu.

        Parameters
        ----------
        self
            input array
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
            an array containing the output of the hardsilu/hardswish function applied
            to each element in ``x``.

        Examples
        --------
        >>> x = startai.array([1., 2., 3.])
        >>> y = x.hardsilu()
        >>> print(y)
        startai.array([0.66666667, 1.66666667, 3.])
        """
        return startai.hardsilu(self._data, out=out)
