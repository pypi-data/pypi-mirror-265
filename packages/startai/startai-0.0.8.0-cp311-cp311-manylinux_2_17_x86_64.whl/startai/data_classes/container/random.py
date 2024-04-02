# global
from typing import Optional, Union, List, Dict

# local
import startai
from startai.data_classes.container.base import ContainerBase


# noinspection PyMissingConstructor
class _ContainerWithRandom(ContainerBase):
    @staticmethod
    def _static_random_uniform(
        *,
        low: Union[float, startai.Container, startai.Array, startai.NativeArray] = 0.0,
        high: Union[float, startai.Container, startai.Array, startai.NativeArray] = 1.0,
        shape: Optional[Union[startai.Shape, startai.NativeShape, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        device: Optional[Union[startai.Device, startai.NativeDevice, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        seed: Optional[Union[int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.random_uniform. This
        method simply wraps the function, and so the docstring for
        startai.random_uniform also applies to this method with minimal changes.

        Parameters
        ----------
        low
            Lower boundary of the output interval. All values generated will be
            greater than or equal to ``low``. If array, must have same shape as
            ``high``.
        high
            Upper boundary of the output interval. All the values generated will be
            less than ``high``. If array, must have same shape as ``low``.
        shape
            If the given shape is, e.g ``(m, n, k)``, then ``m * n * k`` samples
            are drawn. Can only be specified when ``low`` and ``high`` are numeric
            values, else exception will be raised.
            Default is ``None``, where a single value is returned.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None).
        dtype
            output array data type. If ``dtype`` is ``None``, the output array data
            type will be the default floating-point data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized uniform distribution.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([[9.8,7.6],[6.5,2.3]]),
        ...                   b=startai.array([[0.9,2.4],[7.6,5.4]]))
        >>> y = startai.Container(a=startai.array([[10.9,32.4],[18.7,19.6]]),
        ...                   b=startai.array([[4.3,5.6],[23.4,54.3]]))
        >>> startai.Container.static_random_uniform(low=x, high=y, device='cpu',
        ...                                     dtype='float64')
        {
            a: startai.array([[10.8, 23.7],
                          [17., 16.6]]),
            b: startai.array([[2.35, 3.69],
                          [17.4, 48.]])
        }

        With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

        >>> x = startai.array([-1.0,-9.0,-3.4])
        >>> y = startai.Container(a=startai.array([0.6, 0.2, 0.3]),b=startai.array([0.8, 0.2, 0.2]))
        >>> startai.Container.static_random_uniform(low=x, high=y)
        {
            a: startai.array([0.481, -8.03, -2.74]),
            b: startai.array([0.0999, -7.38, -1.29])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "random_uniform",
            low=low,
            high=high,
            shape=shape,
            device=device,
            dtype=dtype,
            seed=seed,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def random_uniform(
        self: startai.Container,
        /,
        *,
        high: Union[float, startai.Container, startai.Array, startai.NativeArray] = 1.0,
        shape: Optional[Union[startai.Shape, startai.NativeShape, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        device: Optional[Union[startai.Device, startai.NativeDevice, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        seed: Optional[Union[int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.random_uniform. This
        method simply wraps the function, and so the docstring for
        startai.random_uniform also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Lower boundary of the output interval. All values generated will be
            greater than or equal to ``low``. If array, must have same shape as
            ``high``.
        high
            Upper boundary of the output interval. All the values generated will be
            less than ``high``. If array, must have same shape as ``low``.
        shape
            If the given shape is, e.g ``(m, n, k)``, then ``m * n * k`` samples
            are drawn. Can only be specified when ``low`` and ``high`` are numeric
            values, else exception will be raised.
            Default is ``None``, where a single value is returned.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None).
        dtype
            output array data type. If ``dtype`` is ``None``, the output array data
            type will be the default floating-point data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized uniform distribution.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([7.5,6.7,0.9]), b=startai.array([8.7,9.8,4.5]))
        >>> x.random_uniform(high=17.4)
        {
            a: startai.array([11.2, 10.5, 13.1]),
            b: startai.array([11.2, 11.9, 6.01])
        }

        >>> x.random_uniform(high=10.2, device='cpu')
        {
            a: startai.array([8.55, 10.1, 4.08]),
            b: startai.array([9.45, 9.9, 8.6])
        }

        >>> x.random_uniform(high=14.2, dtype='float16')
        {
            a: startai.array([12.4, 11.7, 7.25]),
            b: startai.array([11.8, 11.8, 4.96])
        }

        >>> x.random_uniform(high=10.8, device='cpu', dtype='float64')
        {
            a: startai.array([8.86, 9.24, 6.43]),
            b: startai.array([8.95, 10.1, 8.51])
        }

        >>> z = startai.Container(a=startai.zeros((3,)), b=startai.ones((3,)))
        >>> x.random_uniform(high=11.2, device='cpu', dtype='float64', out=z)
        {
            a: startai.array([9.6, 8.24, 3.67]),
            b: startai.array([9.29, 11.2, 9.84])
        }

        >>> y = startai.Container(a=10.4, b=17.4)
        >>> x.random_uniform(high=y)
        {
            a: startai.array([8.24, 9.22, 1.52]),
            b: startai.array([16.5, 13.4, 17.3])
        }

        >>> x.random_uniform(high=y, device='cpu')
        {
            a: startai.array([8.55, 10.1, 4.08]),
            b: startai.array([9.45, 9.9, 8.6])
        }

        >>> x.random_uniform(high=y, dtype='float16')
        {
            a: startai.array([12.4, 11.7, 7.25]),
            b: startai.array([11.8, 11.8, 4.96])
        }

        >>> x.random_uniform(high=y, device='cpu', dtype='float64')
        {
            a: startai.array([8.86, 9.24, 6.43]),
            b: startai.array([8.95, 10.1, 8.51])
        }

        >>> z = startai.Container(a=startai.zeros((3,)), b=startai.ones((3,)))
        >>> x.random_uniform(high=y, device='cpu', dtype='float64', out=z)
        {
            a: startai.array([9.6, 8.24, 3.67]),
            b: startai.array([9.29, 11.2, 9.84])
        }

        >>> x = startai.Container(a=startai.array([[9.8,7.6],[6.5,2.3]]),
        ...                   b=startai.array([[0.9,2.4],[7.6,5.4]]))
        >>> y = startai.Container(a=startai.array([[10.9,32.4],[18.7,19.6]]),
        ...                   b=startai.array([[4.3,5.6],[23.4,54.3]]))
        >>> x.random_uniform(high=y)
        {
            a: startai.array([[10.4, 17.],
                          [9.81, 10.9]]),
            b: startai.array([[3.6, 4.31],
                          [18.8, 54.2]])
        }

        >>> x.random_uniform(high=y, device='cpu')
        {
            a: startai.array([[10.1, 7.93],
                          [7.98, 6.]]),
            b: startai.array([[4.28, 4.65],
                          [13.9, 28.9]])
        }

        >>> x.random_uniform(high=y, dtype='float16')
        {
            a: startai.array([[10.6, 28.],
                          [16.4, 4.92]]),
            b: startai.array([[3.61, 4.82],
                          [12.6, 10.2]])
        }

        >>> x.random_uniform(high=y, device='cpu', dtype='float64')
        {
            a: startai.array([[10.7, 28.4],
                          [9.29, 17.4]]),
            b: startai.array([[1.88, 4.94],
                          [17., 9.68]])
        }

        >>> z = startai.Container(a=startai.zeros((2,2)), b=startai.ones((2,2)))
        >>> x.random_uniform(high=y, device='cpu', dtype='float64', out=z)
        {
            a: startai.array([[10.4, 29.8],
                          [12.1, 3.9]]),
            b: startai.array([[3.79, 5.4],
                          [16.2, 31.7]])
        }
        """
        return self._static_random_uniform(
            low=self,
            high=high,
            shape=shape,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            device=device,
            dtype=dtype,
            seed=seed,
            out=out,
        )

    @staticmethod
    def _static_random_normal(
        *,
        mean: Union[float, startai.Container, startai.Array, startai.NativeArray] = 0.0,
        std: Union[float, startai.Container, startai.Array, startai.NativeArray] = 1.0,
        shape: Optional[Union[startai.Shape, startai.NativeShape, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        device: Optional[Union[startai.Device, startai.NativeDevice, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        seed: Optional[Union[int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.random_normal. This
        method simply wraps the function, and so the docstring for
        startai.random_normal also applies to this method with minimal changes.

        Parameters
        ----------
        mean
            The mean of the normal distribution to sample from. Default is ``0.0``.
        std
            The standard deviation of the normal distribution to sample from.
            Must be non-negative. Default is ``1.0``.
        shape
            If the given shape is, e.g ``(m, n, k)``, then ``m * n * k`` samples
            are drawn. Can only be specified when ``mean`` and ``std`` are numeric
            values, else exception will be raised.
            Default is ``None``, where a single value is returned.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None).
        dtype
             output array data type. If ``dtype`` is ``None``, the output array data
             type will be the default floating-point data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized normal distribution.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([[9.8,7.6],[6.5,2.3]]),
        ...                   b=startai.array([[0.9,2.4],[7.6,5.4]]))
        >>> y = startai.Container(a=startai.array([[10.9,32.4],[18.7,19.6]]),
        ...                   b=startai.array([[4.3,5.6],[23.4,54.3]]))
        >>> startai.Container.static_random_normal(mean=x, std=y, device='cpu',
        ...                                       dtype='float64')
        {
            a: startai.array([[-4.11, 0.651],
                          [19.3, -30.4]]),
            b: startai.array([[1.15, 3.39],
                          [-9.35, -13.9]])
        }

        With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

        >>> x = startai.array([-1.0,-9.0,-3.4])
        >>> y = startai.Container(a=startai.array([0.6, 0.2, 0.3]),b=startai.array([0.8, 0.2, 0.2]))
        >>> startai.Container.static_random_normal(mean=x, std=y)
        {
            a: startai.array([-0.651, -9.25, -3.54]),
            b: startai.array([0.464, -8.51, -3.75])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "random_normal",
            mean=mean,
            std=std,
            shape=shape,
            device=device,
            dtype=dtype,
            seed=seed,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def random_normal(
        self: startai.Container,
        /,
        *,
        std: Union[float, startai.Container, startai.Array, startai.NativeArray] = 1.0,
        shape: Optional[Union[startai.Shape, startai.NativeShape, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        device: Optional[Union[startai.Device, startai.NativeDevice, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        seed: Optional[Union[int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.random_normal. This
        method simply wraps the function, and so the docstring for
        startai.random_normal also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The mean of the normal distribution to sample from. Default is ``0.0``.
        std
            The standard deviation of the normal distribution to sample from.
            Must be non-negative. Default is ``1.0``.
        shape
            If the given shape is, e.g ``(m, n, k)``, then ``m * n * k`` samples
            are drawn. Can only be specified when ``mean`` and ``std`` are numeric
            values, else exception will be raised.
            Default is ``None``, where a single value is returned.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None).
        dtype
            output array data type. If ``dtype`` is ``None``, the output array data
            type will be the default floating-point data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized normal distribution.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([7.5,6.7,0.9]),
        ...                   b=startai.array([8.7,9.8,4.5]))
        >>> x.random_normal(std=17.4)
        {
            a: startai.array([11.9, -22.9, -24.8]),
            b: startai.array([44.3, -21.6, 2.03])
        }

        >>> x.random_normal(std=10.2, device='cpu')
        {
            a: startai.array([7.82, 6.21, -0.431]),
            b: startai.array([13.8, 9.9, 7.64])
        }

        >>> x.random_normal(std=14.2, dtype='float16')
        {
            a: startai.array([-18.3, -3.42, 9.55]),
            b: startai.array([-1.31, 7.68, -6.93])
        }

        >>> x.random_normal(std=10.8, device='cpu', dtype='float64')
        {
            a: startai.array([13.4, -3.14, 10.7]),
            b: startai.array([11.7, 4.85, 5.83])
        }

        >>> z = startai.Container(a=startai.zeros((3,)), b=startai.ones((3,)))
        >>> x.random_normal(std=11.2, device='cpu', dtype='float64', out=z)
        {
            a: startai.array([-6.84, 0.274, 14.2]),
            b: startai.array([29.1, 7.19, 3.])
        }

        >>> y = startai.Container(a=10.4, b=17.4)
        >>> x.random_normal(std=y)
        {
            a: startai.array([-9.5, 8.54, -9.13]),
            b: startai.array([-24.5, 18.9, 11.])
        }

        >>> x.random_normal(std=y, device='cpu')
        {
            a: startai.array([8.47, 8.23, 8.69]),
            b: startai.array([10.7, 16.2, 16.1])
        }

        >>> x.random_normal(std=y, dtype='float16')
        {
            a: startai.array([8.22, -15.9, 10.4]),
            b: startai.array([19.9, 11.5, -2.15])
        }

        >>> x.random_normal(std=y, device='cpu', dtype='float64')
        {
            a: startai.array([19.6, -4.08, 6.09]),
            b: startai.array([-23.9, 6.86, 17.6])
        }

        >>> z = startai.Container(a=startai.zeros((3,)), b=startai.ones((3,)))
        >>> x.random_normal(std=y, device='cpu', dtype='float64', out=z)
        {
            a: startai.array([14.7, 8.99, 8.46]),
            b: startai.array([22.9, -5.97, -1.28])
        }

        >>> x = startai.Container(a=startai.array([[9.8,7.6],[6.5,2.3]]),
        ...                   b=startai.array([[0.9,2.4],[7.6,5.4]]))
        >>> y = startai.Container(a=startai.array([[10.9,32.4],[18.7,19.6]]),
        ...                   b=startai.array([[4.3,5.6],[23.4,54.3]]))
        >>> x.random_normal(std=y)
        {
            a: startai.array([[10.6, 7.89],
                          [9.39, 19.4]]),
            b: startai.array([[3.76, 4.68],
                          [17.7, 24.]])
        }

        >>> x.random_normal(std=y, device='cpu')
        {
            a: startai.array([[30.9, 24.6],
                          [29.9, -25.3]]),
            b: startai.array([[8.02, 1.92],
                          [-5.34, -54.1]])
        }

        >>> x.random_normal(std=y, dtype='float16')
        {
            a: startai.array([[7.82, -35.],
                          [11.7, 0.696]]),
            b: startai.array([[-4.07, -2.91],
                          [19.2, 46.8]])
        }

        >>> x.random_normal(std=y, device='cpu', dtype='float64')
        {
            a: startai.array([[25.4, 28.3],
                          [19.6, -9.83]]),
            b: startai.array([[2.95, 2.48],
                          [-30.8, -40.1]])
        }

        >>> z = startai.Container(a=startai.zeros((2,2)), b=startai.ones((2,2)))
        >>> x.random_normal(std=y, device='cpu', dtype='float64', out=z)
        {
            a: startai.array([[2.8, -45.6],
                          [-10.4, 0.65]]),
            b: startai.array([[3.8, 1.43],
                          [23., 29.4]])
        }
        """
        return self._static_random_normal(
            mean=self,
            std=std,
            shape=shape,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            device=device,
            dtype=dtype,
            seed=seed,
            out=out,
        )

    @staticmethod
    def _static_multinomial(
        population_size: Union[int, startai.Container],
        num_samples: Union[int, startai.Container],
        /,
        *,
        batch_size: Union[int, startai.Container] = 1,
        probs: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        replace: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        device: Optional[Union[startai.Device, startai.NativeDevice, startai.Container]] = None,
        seed: Optional[Union[int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.multinomial. This method
        simply wraps the function, and so the docstring for startai.multinomial
        also applies to this method with minimal changes.

        Parameters
        ----------
        population_size
            The size of the population from which to draw samples.
        num_samples
            Number of independent samples to draw from the population.
        batch_size
            Number of tensors to generate. Default is 1.
        probs
            The unnormalized probabilities for all elements in population,
            default is uniform *[batch_shape, population_size]*
        replace
            Whether to replace samples once they've been drawn. Default is ``True``.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None)
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized normal distribution.
        """
        return ContainerBase.cont_multi_map_in_function(
            "multinomial",
            population_size,
            num_samples,
            batch_size=batch_size,
            probs=probs,
            replace=replace,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            device=device,
            seed=seed,
            out=out,
        )

    def multinomial(
        self: startai.Container,
        population_size: Union[int, startai.Container],
        num_samples: Union[int, startai.Container],
        /,
        *,
        batch_size: Union[int, startai.Container] = 1,
        replace: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        device: Optional[Union[startai.Device, startai.NativeDevice, startai.Container]] = None,
        seed: Optional[Union[int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.multinomial. This
        method simply wraps the function, and so the docstring for
        startai.multinomial also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The unnormalized probabilities for all elements in population,
            default is uniform *[batch_shape, population_size]*
        population_size
            The size of the population from which to draw samples.
        num_samples
            Number of independent samples to draw from the population.
        batch_size
            Number of tensors to generate. Default is 1.
        replace
            Whether to replace samples once they've been drawn. Default is ``True``.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None)
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Drawn samples from the parameterized normal distribution.
        """
        return self._static_multinomial(
            population_size,
            num_samples,
            batch_size=batch_size,
            probs=self,
            replace=replace,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            device=device,
            seed=seed,
            out=out,
        )

    @staticmethod
    def _static_randint(
        low: Union[int, startai.Container, startai.Array, startai.NativeArray],
        high: Union[int, startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        shape: Optional[Union[startai.Shape, startai.NativeShape, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        device: Optional[Union[startai.Device, startai.NativeDevice, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        seed: Optional[Union[int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.randint. This method
        simply wraps the function, and so the docstring for startai.randint also
        applies to this method with minimal changes.

        Parameters
        ----------
        low
            Lowest integer that can be drawn from the distribution.
        high
            One above the highest integer that can be drawn from the distribution.
        shape
            If the given shape is, e.g ``(m, n, k)``, then ``m * n * k`` samples
            are drawn. Can only be specified when ``low`` and ``high`` are numeric
            values, else exception will be raised.
            Default is ``None``, where a single value is returned.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None).
        dtype
             output array data type. If ``dtype`` is ``None``, the output array data
             type will be the default integer data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Returns an array with the given shape filled with integers from
            the uniform distribution in the “half-open” interval [low, high)

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([[9,7],[6,2]]),
        ...                   b=startai.array([[0,2],[10,6]]))
        >>> y = startai.Container(a=startai.array([[10,32],[18,19]]),
        ...                   b=startai.array([[44,5],[23,54]]))
        >>> startai.Container.static_randint(x, y, device='cpu', dtype='int32')
        {
            a: startai.array([[9, 27],
                          [16, 17]]),
            b: startai.array([[13, 3],
                          [16, 19]])
        }

        With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

        >>> x = startai.array([-1,-9,3])
        >>> y = startai.Container(a=startai.array([4,7,9]),b=startai.array([14,17,34]))
        >>> startai.Container.static_randint(x, y)
        {
            a: startai.array([1, 6, 5]),
            b: startai.array([0, 10, 17])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "randint",
            low,
            high,
            shape=shape,
            device=device,
            dtype=dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            seed=seed,
            out=out,
        )

    def randint(
        self: startai.Container,
        high: Union[int, startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        shape: Optional[Union[startai.Shape, startai.NativeShape, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        device: Optional[Union[startai.Device, startai.NativeDevice, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        seed: Optional[Union[int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.randint. This method
        simply wraps the function, and so the docstring for startai.randint also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Lowest integer that can be drawn from the distribution.
        high
            One above the highest integer that can be drawn from the distribution.
        shape
            If the given shape is, e.g ``(m, n, k)``, then ``m * n * k`` samples
            are drawn. Can only be specified when ``low`` and ``high`` are numeric
            values, else exception will be raised.
            Default is ``None``, where a single value is returned.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        device
            device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc.
            (Default value = None).
        dtype
             output array data type. If ``dtype`` is ``None``, the output array data
             type will be the default integer data type. Default ``None``
        seed
            A python integer. Used to create a random seed distribution
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Returns an array with the given shape filled with integers from
            the uniform distribution in the “half-open” interval [low, high)

        Examples
        --------
        >>> x = startai.Container(a=startai.array([7,6,0]),
        ...                   b=startai.array([8,9,4]))
        >>> x.randint(30)
        {
            a: startai.array([23, 15, 20]),
            b: startai.array([28, 22, 18])
        }

        >>> x.randint(10, device='cpu')
        {
            a: startai.array([9, 7, 7]),
            b: startai.array([8, 9, 9])
        }

        >>> x.randint(102, dtype='int8')
        {
            a: startai.array([9, 8, 2]),
            b: startai.array([62, 62, 60])
        }

        >>> x.randint(54, device='cpu', dtype='int64')
        {
            a: startai.array([30, 29, 26]),
            b: startai.array([24, 24, 21])
        }

        >>> z = startai.Container(a=startai.zeros((3,)), b=startai.ones((3,)))
        >>> x.randint(21, device='cpu', dtype='int8', out=z)
        {
            a: startai.array([7, 6, 0]),
            b: startai.array([8, 9, 4])
        }

        >>> y = startai.Container(a=54, b=17)
        >>> x.randint(y)
        {
            a: startai.array([7, 6, 0]),
            b: startai.array([8, 9, 4])
        }

        >>> x.randint(y, device='cpu')
        {
            a: startai.array([7, 6, 0]),
            b: startai.array([8, 9, 4])
        }

        >>> x.randint(y, dtype='int64')
        {
            a: startai.array([7, 6, 0]),
            b: startai.array([8, 9, 4])
        }

        >>> x.randint(y, device='cpu', dtype='int32')
        {
            a: startai.array([7, 6, 0]),
            b: startai.array([8, 9, 4])
        }

        >>> z = startai.Container(a=startai.zeros((3,)), b=startai.ones((3,)))
        >>> x.randint(y, device='cpu', dtype='int16', out=z)
        {
            a: startai.array([7, 6, 0]),
            b: startai.array([8, 9, 4])
        }

        >>> x = startai.Container(a=startai.array([[9,7],[6,2]]),
        ...                   b=startai.array([[0,2],[10,6]]))
        >>> y = startai.Container(a=startai.array([[10,32],[18,19]]),
        ...                   b=startai.array([[44,5],[23,54]]))
        >>> x.randint(y)
        {
            a: startai.array([[9, 7],
                          [6, 2]]),
            b: startai.array([[0, 2],
                          [10, 6]])
        }

        >>> x.randint(y, device='cpu')
        {
            a: startai.array([[9, 7],
                          [6, 2]]),
            b: startai.array([[0, 2],
                          [10, 6]])
        }

        >>> x.randint(y, dtype='int64')
        {
            a: startai.array([[9, 7],
                          [6, 2]]),
            b: startai.array([[0, 2],
                          [10, 6]])
        }

        >>> x.randint(y, device='cpu', dtype='int32')
        {
            a: startai.array([[9, 7],
                          [6, 2]]),
            b: startai.array([[0, 2],
                          [10, 6]])
        }

        >>> z = startai.Container(a=startai.zeros((2,2)), b=startai.ones((2,2)))
        >>> x.randint(y, device='cpu', dtype='int16', out=z)
        {
            a: startai.array([[9, 7],
                          [6, 2]]),
            b: startai.array([[0, 2],
                          [10, 6]])
        }
        """
        return self._static_randint(
            self,
            high,
            shape=shape,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            device=device,
            dtype=dtype,
            seed=seed,
            out=out,
        )

    @staticmethod
    def _static_shuffle(
        x: Union[int, startai.Container, startai.Array, startai.NativeArray],
        axis: Optional[Union[int, startai.Container]] = 0,
        /,
        *,
        seed: Optional[Union[int, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.shuffle. This method
        simply wraps the function, and so the docstring for startai.shuffle also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input array or container. Should have a numeric data type.
        axis
            The axis which input array or container is shuffled along. Default is 0.
        seed
            A python integer. Used to create a random seed distribution
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            A container object, shuffled along the first dimension.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([7, 6, 0]),
        ...                   b=startai.array([8, 9, 4]))
        >>> startai.Container.static_shuffle(x)
        {
            a: startai.array([7, 0, 6]),
            b: startai.array([8, 4, 9])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "shuffle",
            x,
            axis,
            seed=seed,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def shuffle(
        self: startai.Container,
        axis: Optional[Union[int, startai.Container]] = 0,
        /,
        *,
        seed: Optional[Union[int, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.shuffle. This method
        simply wraps the function, and so the docstring for startai.shuffle also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container. Should have a numeric data type.
        axis
            The axis which input container is shuffled along. Default is 0.
        seed
            A python integer. Used to create a random seed distribution
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            A container object, shuffled along the first dimension.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([5, 2, 9]),
        ...                   b=startai.array([7, 1, 6]))
        >>> y = startai.Container.shuffle(x)
        >>> print(y)
        {
            a: startai.array([9, 5, 2]),
            b: startai.array([6, 7, 1])
        }
        """
        return self._static_shuffle(
            self,
            axis,
            seed=seed,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )
