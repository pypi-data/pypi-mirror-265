# global
import abc
from typing import Optional, Union

# local
import startai


class _ArrayWithRandomExperimental(abc.ABC):
    def dirichlet(
        self: startai.Array,
        /,
        *,
        size: Optional[Union[startai.Shape, startai.NativeShape]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
        seed: Optional[int] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.dirichlet. This method
        simply wraps the function, and so the docstring for startai.shuffle also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Sequence of floats of length k
        size
            optional int or tuple of ints, Output shape. If the given shape is,
            e.g., (m, n), then m * n * k samples are drawn. Default is None,
            in which case a vector of length k is returned.
        dtype
            output array data type. If ``dtype`` is ``None``, the output array data
            type will be the default floating-point data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The drawn samples, of shape (size, k).

        Examples
        --------
        >>> alpha = startai.array([1.0, 2.0, 3.0])
        >>> alpha.dirichlet()
        startai.array([0.10598304, 0.21537054, 0.67864642])

        >>> alpha = startai.array([1.0, 2.0, 3.0])
        >>> alpha.dirichlet(size = (2,3))
        startai.array([[[0.48006698, 0.07472073, 0.44521229],
            [0.55479872, 0.05426367, 0.39093761],
            [0.19531053, 0.51675832, 0.28793114]],

        [[0.12315625, 0.29823365, 0.5786101 ],
            [0.15564976, 0.50542368, 0.33892656],
            [0.1325352 , 0.44439589, 0.42306891]]])
        """
        return startai.dirichlet(self, size=size, dtype=dtype, seed=seed, out=out)

    def beta(
        self: startai.Array,
        beta: Union[int, startai.Array, startai.NativeArray],
        /,
        *,
        shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
        device: Optional[Union[startai.Device, startai.NativeDevice]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
        seed: Optional[int] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.beta. This method simply
        wraps the function, and so the docstring for startai.beta also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input Array.
        alpha
            The first parameter of the beta distribution.
        beta
            The second parameter of the beta distribution.
        device
            device on which to create the array.
        dtype
             output array data type. If ``dtype`` is ``None``, the output array data
             type will be the default data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized beta distribution with the shape of
            the array.
        """
        return startai.beta(
            self,
            beta,
            shape=shape,
            device=device,
            dtype=dtype,
            seed=seed,
            out=out,
        )

    def gamma(
        self: startai.Array,
        beta: Union[int, startai.Array, startai.NativeArray],
        /,
        *,
        shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
        device: Optional[Union[startai.Device, startai.NativeDevice]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
        seed: Optional[int] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.gamma. This method simply
        wraps the function, and so the docstring for startai.gamma also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input Array and the first parameter of the gamma distribution.
        beta
            The second parameter of the gamma distribution.
        shape
            If the given shape is, e.g '(m, n, k)', then 'm * n * k' samples are drawn.
            (Default value = 'None', where 'startai.shape(logits)' samples are drawn)
        device
            device on which to create the array.
        dtype
             output array data type. If ``dtype`` is ``None``, the output array data
             type will be the default data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized gamma distribution with the shape of
            the input array.
        """
        return startai.gamma(
            self,
            beta,
            shape=shape,
            device=device,
            dtype=dtype,
            seed=seed,
            out=out,
        )

    def poisson(
        self: startai.Array,
        *,
        shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
        device: Optional[Union[startai.Device, startai.NativeDevice]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
        seed: Optional[int] = None,
        fill_value: Optional[Union[float, int]] = 0,
        out: Optional[startai.Array] = None,
    ):
        """
        Parameters
        ----------
        self
            Input Array of rate parameter(s). It must have a shape that is broadcastable
            to the requested shape
        shape
            If the given shape is, e.g '(m, n, k)', then 'm * n * k' samples are drawn.
            (Default value = 'None', where 'startai.shape(lam)' samples are drawn)
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None).
        dtype
            output array data type. If ``dtype`` is ``None``, the output array data
            type will be the default floating-point data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        fill_value
            if lam is negative, fill the output array with this value
            on that specific dimension.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized poisson distribution.

        Examples
        --------
        >>> lam = startai.array([1.0, 2.0, 3.0])
        >>> lam.poisson()
        startai.array([1., 4., 4.])

        >>> lam = startai.array([1.0, 2.0, 3.0])
        >>> lam.poisson(shape=(2,3))
        startai.array([[0., 2., 2.],
                   [1., 2., 3.]])
        """
        return startai.poisson(
            self,
            shape=shape,
            device=device,
            dtype=dtype,
            seed=seed,
            fill_value=fill_value,
            out=out,
        )

    def bernoulli(
        self: startai.Array,
        *,
        logits: Optional[Union[float, startai.Array, startai.NativeArray]] = None,
        shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
        device: Optional[Union[startai.Device, startai.NativeDevice]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
        seed: Optional[int] = None,
        out: Optional[startai.Array] = None,
    ):
        """

        Parameters
        ----------
        self
             An N-D Array representing the probability of a 1 event.
             Each entry in the Array parameterizes an independent Bernoulli
             distribution. Only one of logits or probs should be passed in
        logits
            An N-D Array representing the log-odds of a 1 event.
            Each entry in the Array parameterizes an independent Bernoulli
            distribution where the probability of an event is sigmoid
            (logits). Only one of logits or probs should be passed in.

        shape
            If the given shape is, e.g '(m, n, k)', then 'm * n * k' samples are drawn.
            (Default value = 'None', where 'startai.shape(logits)' samples are drawn)
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None).

        dtype
            output array data type. If ``dtype`` is ``None``, the output array data
            type will be the default floating-point data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must
            have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the Bernoulli distribution
        """
        return startai.bernoulli(
            self,
            logits=logits,
            shape=shape,
            device=device,
            dtype=dtype,
            seed=seed,
            out=out,
        )
