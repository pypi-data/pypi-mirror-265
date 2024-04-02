# global
from typing import Optional, Union, List, Dict, Tuple, Sequence

# local
import startai
from startai.data_classes.container.base import ContainerBase


class _ContainerWithStatisticalExperimental(ContainerBase):
    @staticmethod
    def static_histogram(
        a: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        bins: Optional[
            Union[int, startai.Array, startai.NativeArray, startai.Container, str]
        ] = None,
        axis: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        extend_lower_interval: Optional[Union[bool, startai.Container]] = False,
        extend_upper_interval: Optional[Union[bool, startai.Container]] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        range: Optional[Tuple[Union[bool, startai.Container]]] = None,
        weights: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        density: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.<func_name>. This method
        simply wraps the function, and so the docstring for startai.histogram also
        applies to this method with minimal changes.

        Parameters
        ----------
        a
            input array.
        bins
            if ``bins`` is an int, it defines the number of equal-width bins in the
            given range.
            if ``bins`` is an array, it defines a monotonically increasing array of bin
            edges, including the rightmost edge, allowing for non-uniform bin widths.
        axis
            dimension along which maximum values must be computed. By default, the
            maximum value must be computed over the entire array. Default: ``None``.
        extend_lower_interval
            if True, extend the lowest interval I0 to (-inf, c1].
        extend_upper_interval
            ff True, extend the upper interval I_{K-1} to [c_{K-1}, +inf).
        dtype
            the output type.
        range
            the lower and upper range of the bins. The first element of the range must
            be less than or equal to the second.
        weights
            each value in ``a`` only contributes its associated weight towards the bin
            count (instead of 1). Must be of the same shape as a.
        density
            if True, the result is the value of the probability density function at the
            bin, normalized such that the integral over the range of bins is 1.
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
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            a tuple containing the values of the histogram and the bin edges.

        Both the description and the type hints above assumes an array input for
        simplicity, but this function is *nestable*, and therefore also accepts
        :class:`startai.Container` instances in place of any of the arguments.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.]))
        >>> y = startai.array([0., 1., 2., 3., 4., 5.])
        >>> dtype = startai.int32
        >>> z = startai.Container.static_histogram(x, bins=y, dtype=dtype)
        >>> print(z.a)
        >>> print(z.b)
        (startai.array([1, 1, 1, 0, 0]), startai.array([0., 1., 2., 3., 4., 5.]))
        (startai.array([0, 0, 0, 1, 2]), startai.array([0., 1., 2., 3., 4., 5.]))
        """
        return ContainerBase.cont_multi_map_in_function(
            "histogram",
            a,
            bins=bins,
            axis=axis,
            extend_lower_interval=extend_lower_interval,
            extend_upper_interval=extend_upper_interval,
            dtype=dtype,
            range=range,
            weights=weights,
            density=density,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def histogram(
        self: startai.Container,
        /,
        *,
        bins: Optional[
            Union[int, startai.Array, startai.NativeArray, startai.Container, str]
        ] = None,
        axis: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        extend_lower_interval: Optional[Union[bool, startai.Container]] = False,
        extend_upper_interval: Optional[Union[bool, startai.Container]] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        range: Optional[Union[Tuple[float], startai.Container]] = None,
        weights: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        density: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.<func_name>. This
        method simply wraps the function, and so the docstring for
        startai.histogram also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array.
        bins
            if ``bins`` is an int, it defines the number of equal-width bins in the
            given range.
            if ``bins`` is an array, it defines a monotonically increasing array of bin
            edges, including the rightmost edge, allowing for non-uniform bin widths.
        axis
            dimension along which maximum values must be computed. By default, the
            maximum value must be computed over the entire array. Default: ``None``.
        extend_lower_interval
            if True, extend the lowest interval I0 to (-inf, c1].
        extend_upper_interval
            ff True, extend the upper interval I_{K-1} to [c_{K-1}, +inf).
        dtype
            the output type.
        range
            the lower and upper range of the bins. The first element of the range must
            be less than or equal to the second.
        weights
            each value in ``a`` only contributes its associated weight towards the bin
            count (instead of 1). Must be of the same shape as a.
        density
            if True, the result is the value of the probability density function at the
            bin, normalized such that the integral over the range of bins is 1.
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
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            a tuple containing the values of the histogram and the bin edges.

        Both the description and the type hints above assumes an array input for
        simplicity, but this function is *nestable*, and therefore also accepts
        :class:`startai.Container` instances in place of any of the arguments.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.]))
        >>> y = startai.array([0., 1., 2., 3., 4., 5.])
        >>> dtype = startai.int32
        >>> z = x.histogram(bins=y, dtype=dtype)
        >>> print(z)
        {
            a: startai.array([1, 1, 1, 0, 0]),
            b: startai.array([0, 0, 0, 1, 2])
        }
        """
        return self.static_histogram(
            self,
            bins=bins,
            axis=axis,
            extend_lower_interval=extend_lower_interval,
            extend_upper_interval=extend_upper_interval,
            dtype=dtype,
            range=range,
            weights=weights,
            density=density,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_median(
        input: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.median. This method
        simply wraps the function, and so the docstring for startai.median also
        applies to this method with minimal changes.

        Parameters
        ----------
        input
            Input container including arrays.
        axis
            Axis or axes along which the medians are computed. The default is to compute
            the median along a flattened version of the array.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The median of the array elements.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.zeros((3, 4, 5)), b=startai.zeros((2,7,6)))
        >>> startai.Container.static_moveaxis(x, 0, -1).shape
        {
            a: (4, 5, 3)
            b: (7, 6, 2)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "median",
            input,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def median(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.median. This method
        simply wraps the function, and so the docstring for startai.median also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container including arrays.
        axis
            Axis or axes along which the medians are computed. The default is to compute
            the median along a flattened version of the array.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The median of the array elements.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(
        >>>     a=startai.array([[10, 7, 4], [3, 2, 1]]),
        >>>     b=startai.array([[1, 4, 2], [8, 7, 0]])
        >>> )
        >>> x.median(axis=0)
        {
            a: startai.array([6.5, 4.5, 2.5]),
            b: startai.array([4.5, 5.5, 1.])
        }
        """
        return self.static_median(self, axis=axis, keepdims=keepdims, out=out)

    @staticmethod
    def static_nanmean(
        input: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.nanmean. This method
        simply wraps the function, and so the docstring for startai.nanmean also
        applies to this method with minimal changes.

        Parameters
        ----------
        input
            Input container including arrays.
        axis
            Axis or axes along which the means are computed.
            The default is to compute the mean of the flattened array.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original a. If the value is anything but the default,
            then keepdims will be passed through to the mean or sum methods of
            sub-classes of ndarray. If the sub-classes methods does not implement
            keepdims any exceptions will be raised.
        dtype
            The desired data type of returned tensor. Default is None.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The nanmean of the array elements in the container.

        Examples
        --------
        >>> a = startai.Container(x=startai.array([[1, startai.nan], [3, 4]]),\
                                y=startai.array([[startai.nan, 1, 2], [1, 2, 3]])
        >>> startai.Container.static_moveaxis(a)
        {
            x: 2.6666666666666665
            y: 1.8
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "nanmean",
            input,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def nanmean(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.nanmean. This method
        simply wraps the function, and so the docstring for startai.nanmean also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container including arrays.
        axis
            Axis or axes along which the means are computed.
            The default is to compute the mean of the flattened array.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original a. If the value is anything but the default,
            then keepdims will be passed through to the mean or sum methods of
            sub-classes of ndarray. If the sub-classes methods does not implement
            keepdims any exceptions will be raised.
        dtype
            The desired data type of returned tensor. Default is None.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The nanmean of the array elements in the input container.

        Examples
        --------
        >>> a = startai.Container(x=startai.array([[1, startai.nan], [3, 4]]),\
                                y=startai.array([[startai.nan, 1, 2], [1, 2, 3]])
        >>> a.nanmean()
        {
            x: 2.6666666666666665
            y: 1.8
        }
        """
        return self.static_nanmean(
            self, axis=axis, keepdims=keepdims, dtype=dtype, out=out
        )

    @staticmethod
    def _static_nanmin(
        x: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        keepdims: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        initial: Optional[Union[int, float, complex, startai.Container]] = None,
        where: Optional[Union[startai.Array, startai.Container]] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.nanmin. This method
        simply wraps the function, and so the docstring for startai.nanmin also
        applies to this method with minimal changes.

        Parameters
        ----------
        input
            Input container including arrays.
        axis
            Axis or axes along which the minimum is computed.
            The default is to compute the minimum of the flattened array.
        out
            optional output array, for writing the result to.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original a.
        initial
            The maximum value of an output element
        where
            Elements to compare for the minimum

        Returns
        -------
        ret
            Return minimum of an array or minimum along an axis, ignoring any NaNs.

        Examples
        --------
        >>> a = startai.Container(x=startai.array([[1, 2], [3, startai.nan]]),\
                                y=startai.array([[startai.nan, 1, 2], [1, 2, 3]])
        >>> startai.Container.static_nanmin(a)
        {
            x: 1.
            y: 1.
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "nanmin",
            x,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
            initial=initial,
            where=where,
        )

    def nanmin(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        keepdims: Optional[Union[bool, startai.Container]] = False,
        out: Optional[startai.Container] = None,
        initial: Optional[Union[int, float, complex, startai.Container]] = None,
        where: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.nanmin. This method
        simply wraps the function, and so the docstring for startai.nanmin also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container including arrays.
        axis
            Axis or axes along which the minimum is computed.
            The default is to compute the minimum of the flattened array.
        out
            optional output array, for writing the result to.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original a.
        initial
            The maximum value of an output element.
        where
            Elements to compare for the minimum.

        Returns
        -------
        ret
            Return minimum of an array or minimum along an axis, ignoring any NaNs

        Examples
        --------
        >>> a = startai.Container(x=startai.array([[1, 2], [3, startai.nan]]),\
                                y=startai.array([[startai.nan, 1, 2], [1, 2, 3]])
        >>> a.nanmin()
        {
            x: 12.0
            y: 12.0
        }
        """
        return self._static_nanmin(
            self,
            axis=axis,
            keepdims=keepdims,
            out=out,
            initial=initial,
            where=where,
        )

    @staticmethod
    def static_nanprod(
        input: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        keepdims: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
        initial: Optional[Union[int, float, complex, startai.Container]] = 1,
        where: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.nanprod. This method
        simply wraps the function, and so the docstring for startai.nanprod also
        applies to this method with minimal changes.

        Parameters
        ----------
        input
            Input container including arrays.
        axis
            Axis or axes along which the product is computed.
            The default is to compute the product of the flattened array.
        dtype
            The desired data type of returned array. Default is None.
        out
            optional output array, for writing the result to.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original a.
        initial
            The starting value for this product.
        where
            Elements to include in the product

        Returns
        -------
        ret
            The product of array elements over a given axis treating
            Not a Numbers (NaNs) as ones

        Examples
        --------
        >>> a = startai.Container(x=startai.array([[1, 2], [3, startai.nan]]),\
                                y=startai.array([[startai.nan, 1, 2], [1, 2, 3]])
        >>> startai.Container.static_nanprod(a)
        {
            x: 12.0
            y: 12.0
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "nanprod",
            input,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
            initial=initial,
            where=where,
        )

    def nanprod(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        keepdims: Optional[Union[bool, startai.Container]] = False,
        out: Optional[startai.Container] = None,
        initial: Optional[Union[int, float, complex, startai.Container]] = None,
        where: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.nanprod. This method
        simply wraps the function, and so the docstring for startai.nanprod also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container including arrays.
        axis
            Axis or axes along which the product is computed.
            The default is to compute the product of the flattened array.
        dtype
            The desired data type of returned array. Default is None.
        out
            optional output array, for writing the result to.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original a.
        initial
            The starting value for this product.
        where
            Elements to include in the product

        Returns
        -------
        ret
            The product of array elements over a given axis treating
            Not a Numbers (NaNs) as ones

        Examples
        --------
        >>> a = startai.Container(x=startai.array([[1, 2], [3, startai.nan]]),\
                                y=startai.array([[startai.nan, 1, 2], [1, 2, 3]])
        >>> a.nanprod()
        {
            x: 12.0
            y: 12.0
        }
        """
        return self.static_nanprod(
            self,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            out=out,
            initial=initial,
            where=where,
        )

    @staticmethod
    def static_quantile(
        a: Union[startai.Container, startai.Array, startai.NativeArray],
        q: Union[startai.Array, float, startai.Container],
        /,
        *,
        axis: Optional[Union[Sequence[int], int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        interpolation: Union[str, startai.Container] = "linear",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.quantile. This method
        simply wraps the function, and so the docstring for startai.quantile also
        applies to this method with minimal changes.

        Parameters
        ----------
        a
            Input container including arrays.
        q
            Quantile or sequence of quantiles to compute, which must be
            between 0 and 1 inclusive.
        axis
            Axis or axes along which the quantiles are computed. The default
            is to compute the quantile(s) along a flattened version of the array.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original array a.
        interpolation
            {'nearest', 'linear', 'lower', 'higher', 'midpoint'}. Default value:
            'linear'.
            This specifies the interpolation method to use when the desired quantile
            lies between two data points i < j:
            - linear: i + (j - i) * fraction, where fraction is the fractional part of
            the index surrounded by i and j.
            - lower: i.
            - higher: j.
            - nearest: i or j, whichever is nearest.
            - midpoint: (i + j) / 2. linear and midpoint interpolation do not work with
            integer dtypes.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Container with (rank(q) + N - len(axis)) dimensional arrays of same dtype
            as input arrays in the container, or, if axis is None, rank(q) arrays. The
            first rank(q) dimensions index quantiles for different values of q.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> a = startai.Container(x=startai.array([[10., 7., 4.], [3., 2., 1.]]),
                              y=startai.array([1., 2., 3., 4.]))
        >>> q = 0.5
        >>> b = startai.Container.static_quantile(a, q)
        >>> print(b)
        {
            x: 3.5,
            y: 2.5
        }

        >>> a = startai.Container(x=startai.array([[10., 7., 4.], [3., 2., 1.]]),
                              y=startai.array([1., 2., 3., 4.]))
        >>> q = startai.array([0.5, 0.75])
        >>> b = startai.Container.static_quantile(a, q)
        >>> print(b)
        {
            x: startai.array([3.5, 6.25]),
            y: startai.array([2.5, 3.25])
        }

        >>> a = startai.Container(x=startai.array([[10., 7., 4.], [3., 2., 1.]]),
                              y=startai.array([1., 2., 3., 4.]))
        >>> q = startai.array([0.5, 0.75])
        >>> b = startai.Container.static_quantile(a, q, axis = 0)
        >>> print(b)
        {
            x: startai.array([[6.5, 4.5, 2.5],
                        [8.25, 5.75, 3.25]]),
            y: startai.array([2.5, 3.25])
        }

        >>> a = startai.Container(x=startai.array([[10., 7., 4.], [3., 2., 1.]]))
        >>> b = startai.Container.static_quantile(a, q, axis = 1, keepdims=True)
        >>> print(b)
        {
            x: startai.array([[[7.],
                    [2.]],
                    [[8.5],
                    [2.5]]])
        }

        >>> a = startai.Container(x=startai.array([[10., 7., 4.], [3., 2., 1.]]),
                              y=startai.array([1., 2., 3., 4.]))
        >>> q = startai.array([0.3, 0.7])
        >>> b = startai.Container.static_quantile(a, q, axis = 0, interpolation="lower")
        >>> print(b)
        {
            x: startai.array([[3., 2., 1.],
                        [3., 2., 1.]]),
            y: startai.array([1., 3.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "quantile",
            a,
            q,
            axis=axis,
            keepdims=keepdims,
            interpolation=interpolation,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def quantile(
        self: startai.Container,
        q: Union[startai.Array, float, startai.Container],
        /,
        *,
        axis: Optional[Union[Sequence[int], int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        interpolation: Union[str, startai.Container] = "linear",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.quantile. This method
        simply wraps the function, and so the docstring for startai.quantile also
        applies to this method with minimal changes.

        Parameters
        ----------
        a
            Input container including arrays.
        q
            Quantile or sequence of quantiles to compute, which must be
            between 0 and 1 inclusive.
        axis
            Axis or axes along which the quantiles are computed. The default
            is to compute the quantile(s) along a flattened version of the array.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original array a.
        interpolation
            {'nearest', 'linear', 'lower', 'higher', 'midpoint'}. Default value:
            'linear'.
            This specifies the interpolation method to use when the desired quantile
            lies between two data points i < j:
            - linear: i + (j - i) * fraction, where fraction is the fractional part of
            the index surrounded by i and j.
            - lower: i.
            - higher: j.
            - nearest: i or j, whichever is nearest.
            - midpoint: (i + j) / 2. linear and midpoint interpolation do not work with
            integer dtypes.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Container with (rank(q) + N - len(axis)) dimensional arrays of same dtype
            as input arrays in the container, or, if axis is None, rank(q) arrays. The
            first rank(q) dimensions index quantiles for different values of q.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([[10., 7., 4.], [3., 2., 1.]]),
        ...                   b=startai.array([1., 2., 3., 4.]))
        >>> z = startai.array([0.5])
        >>> y = x.quantile(z)
        >>> print(y)
        {
            a: startai.array(3.5),
            b: startai.array(2.5)
        }

        >>> x = startai.Container(a=startai.array([[10., 7., 4.], [3., 2., 1.]]),
        ...                   b=startai.array([1., 2., 3., 4.]))
        >>> z = startai.array([0.5, 0.75])
        >>> y = x.quantile(z)
        >>> print(y)
        {
            a: startai.array([3.5, 6.25]),
            b: startai.array([2.5, 3.25])
        }

        >>> x = startai.Container(a=startai.array([[10., 7., 4.], [3., 2., 1.]]),
        ...                   b=startai.array([1., 2., 3., 4.]))
        >>> z = startai.array([0.5, 0.75])
        >>> y = x.quantile(z, axis = 0)
        >>> print(y)
        {
            a: startai.array([[6.5, 4.5, 2.5],
                          [8.25, 5.75, 3.25]]),
            b: startai.array([2.5, 3.25])
        }

        >>> x = startai.Container(a=startai.array([[10., 7., 4.], [3., 2., 1.]]))
        >>> z = startai.array([0.5, 0.75])
        >>> y = x.quantile(z, axis = 1, keepdims=True)
        >>> print(y)
        {
            a: startai.array([[[7.],
                           [2.]],
                          [[8.5],
                           [2.5]]])
        }

        >>> x = startai.Container(a=startai.array([[10., 7., 4.], [3., 2., 1.]]),
        ...                   b=startai.array([1., 2., 3., 4.]))
        >>> z = startai.array([0.3, 0.7])
        >>> y = x.quantile(z, axis = 0, interpolation="lower")
        >>> print(y)
        {
            a: startai.array([[3., 2., 1.],
                          [3., 2., 1.]]),
            b: startai.array([1., 3.])
        }
        """
        return self.static_quantile(
            self,
            q,
            axis=axis,
            keepdims=keepdims,
            interpolation=interpolation,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_corrcoef(
        x: startai.Container,
        /,
        *,
        y: Optional[startai.Container] = None,
        rowvar: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = False,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.corrcoef. This method
        simply wraps the function, and so the docstring for startai.corrcoef also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input container including arrays.
        y
            An additional input container.
        rowvar
            If rowvar is True (default), then each row represents a variable, with
            observations in the columns. Otherwise, the relationship is transposed:
            each column represents a variable, while the rows contain observations.

        Returns
        -------
        ret
            The corrcoef of the array elements in the container.

        Examples
        --------
        >>> a = startai.Container(w=startai.array([[1., 2.], [3., 4.]]), \
                                 z=startai.array([[0., 1., 2.], [2., 1., 0.]]))
        >>> startai.Container.corrcoef(a)
        {
            w: startai.array([[1., 1.],
                          [1., 1.]]),
            z: startai.array([[1., -1.],
                          [-1., 1.]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "corrcoef",
            x,
            y=y,
            rowvar=rowvar,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def corrcoef(
        self: startai.Container,
        /,
        *,
        y: Optional[startai.Container] = None,
        rowvar: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.corrcoef. This method
        simply wraps the function, and so the docstring for startai.corrcoef also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container including arrays.
        y
            An additional input container.
        rowvar
            If rowvar is True (default), then each row represents a variable, with
            observations in the columns. Otherwise, the relationship is transposed:
            each column represents a variable, while the rows contain observations.

        Returns
        -------
        ret
            The corrcoef of the array elements in the input container.

        Examples
        --------
        >>> a = startai.Container(w=startai.array([[1., 2.], [3., 4.]]), \
                                 z=startai.array([[0., 1., 2.], [2., 1., 0.]]))
        >>> startai.Container.corrcoef(a)
        {
            w: startai.array([[1., 1.],
                          [1., 1.]]),
            z: startai.array([[1., -1.],
                          [-1., 1.]])
        }
        """
        return self.static_corrcoef(self, y=y, rowvar=rowvar, out=out)

    @staticmethod
    def static_nanmedian(
        input: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        overwrite_input: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.median. This method
        simply wraps the function, and so the docstring for startai.median also
        applies to this method with minimal changes.

        Parameters
        ----------
        input
            Input container including arrays.
        axis
            Axis or axes along which the medians are computed. The default is to compute
            the median along a flattened version of the array.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one.
        overwrite_input
            If True, then allow use of memory of input array for calculations.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The median of the array elements.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([[10.0, startai.nan, 4], [3, 2, 1]]))
        >>> startai.Container.static_nanmedian(x)
        {
            a: startai.array(3.)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "nanmedian",
            input,
            axis=axis,
            keepdims=keepdims,
            overwrite_input=overwrite_input,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def nanmedian(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[Tuple[int], int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        overwrite_input: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.nanmedian. This method
        simply wraps the function, and so the docstring for startai.nanmedian also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        axis
            The axis or axes along which the means are computed.
            The default is to compute the mean of the flattened array.
        keepdims
            If this is set to True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original container. If the value is anything
            but the default, then keepdims will be passed through to the mean or
            sum methods of sub-classes of ndarray. If the sub-classes methods
            does not implement keepdims any exceptions will be raised.
        overwrite_input
            If True, then allow use of memory of input array a for calculations.
            The input array will be modified by the call to median.
            This will save memory when you do not need to preserve
            the contents of the input array.Treat the input as undefined,
            but it will probably be fully or partially sorted.
            Default is False. If overwrite_input is True and
            input container does not already have leaves which are
            of the ndarray kind, an error will be raised.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            A new array holding the result. If the input contains integers

        Examples
        --------
        With :class:`startai.Container` input and default backend set as `numpy`:
        >>> x = startai.Container(a=startai.array([[10.0, startai.nan, 4], [3, 2, 1]]),
                b=startai.array([[12, 10, 34], [45, 23, startai.nan]]))
        >>> x.nanmedian()
        {
            a: startai.array(3.),
            b: startai.array(23.)
        }
        >>> x.nanmedian(axis=0)
        {
            a: startai.array([6.5, 2., 2.5]),
            b: startai.array([28.5, 16.5, 34.])
        }
        """
        return self.static_nanmedian(
            self, axis=axis, keepdims=keepdims, overwrite_input=overwrite_input, out=out
        )

    @staticmethod
    def static_bincount(
        x: startai.Container,
        /,
        *,
        weights: Optional[startai.Container] = None,
        minlength: Union[int, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.bincount. This method
        simply wraps the function, and so the docstring for startai.bincount also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input container including arrays.
        weights
            An optional input container including arrays.
        minlength
            A minimum number of bins for the output array.

        Returns
        -------
        ret
            The bincount of the array elements.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1, 1, 2, 2, 2, 3]),
                            b=startai.array([1, 1, 2, 2, 2, 3]))
        >>> startai.Container.static_bincount(x)
            {
                a: array([0, 2, 3, 1])
                b: array([0, 2, 3, 1])
            }
        """
        return ContainerBase.cont_multi_map_in_function(
            "bincount",
            x,
            weights=weights,
            minlength=minlength,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def bincount(
        self: startai.Container,
        /,
        *,
        weights: Optional[startai.Container] = None,
        minlength: Union[int, startai.Container] = 0,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Array instance method variant of startai.bincount. This method
        simply wraps the function, and so the docstring for startai.bincount also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        weights
            An optional input array.
        minlength
            A minimum number of bins for the output array.

        Returns
        -------
        ret
            The bincount of the array elements.

        Examples
        --------
        >>> a = startai.Container([[10.0, startai.nan, 4], [3, 2, 1]])
        >>> a.bincount(a)
            3.0
        >>> a.bincount(a, axis=0)
            array([6.5, 2. , 2.5])
        """
        return self.static_bincount(self, weights=weights, minlength=minlength, out=out)

    @staticmethod
    def static_igamma(
        a: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.igamma. This method
        simply wraps the function, and so the docstring for startai.igamma also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        x
            An additional input array.
            `x` has the same type as `a`.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The lower incomplete gamma function of the array elements.

        Examples
        --------
        >>> a = startai.array([2.5])
        >>> x = startai.array([1.7, 1.2])
        >>> a.igamma(x)
            startai.array([0.3614, 0.2085])
        """
        return ContainerBase.cont_multi_map_in_function(
            "igamma",
            a,
            x=x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def igamma(
        self: startai.Container,
        /,
        *,
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.igamma. This method
        simply wraps the function, and so the docstring for startai.igamma also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array.
        x
            An additional input array.
            `x` has the same type as `a`.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            The lower incomplete gamma function of the array elements.

        Examples
        --------
        >>> a = startai.array([2.5])
        >>> x = startai.array([1.7, 1.2])
        >>> a.igamma(x)
            startai.array([0.3614, 0.2085])
        """
        return self.static_igamma(self, x=x, out=out)

    @staticmethod
    def static_lgamma(
        a: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        return ContainerBase.cont_multi_map_in_function(
            "lgamma",
            a,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def lgamma(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        return self.static_lgamma(self, out=out)

    @staticmethod
    def static_cov(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        x2: Union[startai.Array, startai.NativeArray, startai.Container] = None,
        /,
        *,
        rowVar: Union[bool, startai.Container] = True,
        bias: Union[bool, startai.Container] = False,
        ddof: Union[int, startai.Container] = None,
        fweights: Union[startai.Array, startai.Container] = None,
        aweights: Union[startai.Array, startai.Container] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.cov. This method simply
        wraps the function, and so the docstring for startai.cov also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            a 1D or 2D input array, nativearray or container, with a numeric data type.
        x2
            optional second 1D or 2D input array, nativearray, or container, with a
            numeric data type. Must have the same shape as x1.
        rowVar
            optional variable where each row of input is interpreted as a variable
            (default = True). If set to False, each column is instead interpreted
            as a variable.
        bias
            optional variable for normalizing input (default = False) by (N - 1) where
            N is the number of given observations. If set to True, then normalization
            is instead by N. Can be overridden by keyword ``ddof``.
        ddof
            optional variable to override ``bias`` (default = None). ddof=1 will return
            the unbiased estimate, even with fweights and aweights given. ddof=0 will
            return the simple average.
        fweights
            optional 1D array of integer frequency weights; the number of times each
            observation vector should be repeated.
        aweights
            optional 1D array of observation vector weights. These relative weights are
            typically large for observations considered "important" and smaller for
            observations considered less "important". If ddof=0 is specified, the array
            of weights can be used to assign probabilities to observation vectors.
        dtype
            optional variable to set data-type of the result. By default, data-type
            will have at least ``numpy.float64`` precision.
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
            a container containing the covariance matrix of an input matrix, or the
            covariance matrix of two variables. The returned container must have a
            floating-point data type determined by Type Promotion Rules and must be
            a square matrix of shape (N, N), where N is the number of rows in the
            input(s).

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.array([1., 2., 3.])
        >>> y = startai.Container(a=startai.array([3. ,2. ,1.]), b=startai.array([-1., -2., -3.]))
        >>> z = startai.Container.static_cov(x, y)
        >>> print(z)
        {
            a: startai.array([ 1., -1.]
                         [-1.,  1.]),
            b: startai.array([ 1., -1.]
                         [-1.,  1.])
        }

        With multiple :class:`startai.Container` inputs:
        >>> x = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([1., 2., 3.]))
        >>> y = startai.Container(a=startai.array([3., 2., 1.]), b=startai.array([3., 2., 1.]))
        >>> z = startai.Container.static_cov(x, y)
        >>> print(z)
        {
            a: startai.container([ 1., -1., -1., -1.]
                         [ 1.,  1., -1., -1.]),
            b: startai.container([-1., -1.,  1.,  1.]
                         [-1.,  1.,  1.,  1.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "cov",
            x1,
            x2,
            rowVar=rowVar,
            bias=bias,
            ddof=ddof,
            fweights=fweights,
            aweights=aweights,
            dtype=dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def cov(
        self: startai.Container,
        x2: startai.Container = None,
        /,
        *,
        rowVar: Union[bool, startai.Container] = True,
        bias: Union[bool, startai.Container] = False,
        ddof: Optional[Union[int, startai.Container]] = None,
        fweights: Optional[Union[startai.Array, startai.Container]] = None,
        aweights: Optional[Union[startai.Array, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.cov. This method simply
        wraps the function, and so the docstring for startai.cov also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            a 1D or 2D input container, with a numeric data type.
        x2
            optional second 1D or 2D input array, nativearray, or container, with a
            numeric data type. Must have the same shape as ``self``.
        rowVar
            optional variable where each row of input is interpreted as a variable
            (default = True). If set to False, each column is instead interpreted
            as a variable.
        bias
            optional variable for normalizing input (default = False) by (N - 1) where
            N is the number of given observations. If set to True, then normalization
            is instead by N. Can be overridden by keyword ``ddof``.
        ddof
            optional variable to override ``bias`` (default = None). ddof=1 will return
            the unbiased estimate, even with fweights and aweights given. ddof=0 will
            return the simple average.
        fweights
            optional 1D array of integer frequency weights; the number of times each
            observation vector should be repeated.
        aweights
            optional 1D array of observation vector weights. These relative weights are
            typically large for observations considered "important" and smaller for
            observations considered less "important". If ddof=0 is specified, the array
            of weights can be used to assign probabilities to observation vectors.
        dtype
            optional variable to set data-type of the result. By default, data-type
            will have at least ``numpy.float64`` precision.
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
            a container containing the covariance matrix of an input matrix, or the
            covariance matrix of two variables. The returned container must have a
            floating-point data type determined by Type Promotion Rules and must be
            a square matrix of shape (N, N), where N is the number of variables in the
            input(s).

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([1., 2., 3.]))
        >>> y = startai.Container(a=startai.array([3., 2., 1.]), b=startai.array([3., 2., 1.]))
        >>> z = x.cov(y)
        >>> print(z)

        {
            a: startai.array([[1., -1.],
                          [-1., 1.]]),
            b: startai.array([[1., -1.],
                          [-1., 1.]])
        }
        """
        return self.static_cov(
            self,
            x2,
            rowVar=rowVar,
            bias=bias,
            ddof=ddof,
            fweights=fweights,
            aweights=aweights,
            dtype=dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def cummax(
        self: startai.Container,
        /,
        *,
        axis: Union[int, startai.Container] = 0,
        exclusive: Union[bool, startai.Container] = False,
        reverse: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.cummax. This method
        simply wraps the function, and so the docstring for startai.cummax also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container to cummax at leaves.
        axis
            Axis along which the cumulative product is computed. Default is ``0``.
        exclusive
            Whether to exclude the first element of the input array.
            Default is ``False``.
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
        dtype
            Data type of the returned array. Default is ``None``.
        out
            Optional output container. Default is ``None``.

        Returns
        -------
        ret
            Containers with arrays cummax at leaves along specified axis.

        --------
        With one :class:`startai.Container` instances:

        >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([4, 5, 6]))
        >>> y = x.cummax(axis=0)
        >>> print(y)
        [{
            a: startai.array([1, 2, 3]),
            b: startai.array([4, 5, 6])
        }, {
            a: startai.array([0, 1, 2]),
            b: startai.array([0, 1, 2])
        }]

        >>> x = startai.Container(a=startai.array([[2, 3], [5, 7], [11, 13]]),
        ...                   b=startai.array([[3, 4], [4, 5], [5, 6]]))
        >>> y = startai.Container(a = startai.zeros((3, 2)), b = startai.zeros((3, 2)))
        >>> x.cummax(axis=1, exclusive=True, out=y)
        >>> print(y)
        {
            a: startai.array([[0., 1.],
                          [0., 1.],
                          [0., 1.]]),
            b: startai.array([[0., 1.],
                          [0., 1.],
                          [0., 1.]])
        }
        """
        return self._static_cummax(
            self,
            axis=axis,
            exclusive=exclusive,
            reverse=reverse,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            dtype=dtype,
            out=out,
        )

    def cummin(
        self: startai.Container,
        /,
        *,
        axis: Union[int, startai.Container] = 0,
        exclusive: Union[bool, startai.Container] = False,
        reverse: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.cummin. This method
        simply wraps the function, and so the docstring for startai.cummin also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container to cummin at leaves.
        axis
            Axis along which the cumulative product is computed. Default is ``0``.
        exclusive
            Whether to exclude the first element of the input array.
            Default is ``False``.
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
        dtype
            Data type of the returned array. Default is ``None``.
        out
            Optional output container. Default is ``None``.

        Returns
        -------
        ret
            Containers with arrays cummin at leaves along specified axis.

        Examples #TODO: change examples and change doc string
        --------
        With one :class:`startai.Container` instances:

        >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([4, 5, 6]))
        >>> y = x.cummin(axis=0)
        >>> print(y)
        {
            a: startai.array([1, 1, 1]),
            b: startai.array([4, 4, 4])
        }

        >>> x = startai.Container(a=startai.array([[2, 3], [5, 7], [11, 13]]),
                              b=startai.array([[3, 4], [4, 5], [5, 6]]))
        >>> y = startai.Container(a = startai.zeros((3, 2)), b = startai.zeros((3, 2)))
        >>> x.cummin(axis=1, out=y)
        {
            a: startai.array([[2, 2],
                          [5, 5],
                          [11, 11]]),
            b: startai.array([[3, 3],
                          [4, 4],
                          [5, 5]])
        }
        """
        return self._static_cummin(
            self,
            axis=axis,
            exclusive=exclusive,
            reverse=reverse,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            dtype=dtype,
            out=out,
        )

    @staticmethod
    def _static_cummax(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        axis: Union[int, startai.Container] = 0,
        exclusive: Union[bool, startai.Container] = False,
        reverse: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.cummax. This method
        simply wraps the function, and so the docstring for startai.cummax also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input array or container to cummax.
        axis
            Axis to cummax along. Default is ``0``.
        exclusive
            Whether to exclude the first element of the input array.
            Default is ``False``.
        reverse
            Whether to perform the cummax from last to first element in the selected
            axis. Default is ``False`` (from first to last element)
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
            Optional output container. Default is ``None``.

        Returns
        -------
        ret
            Containers with arrays cummax at leaves along specified axis.

        --------
        With one :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([4, 5, 6]))
        >>> y = startai.Container.static_cummax(x, axis=0)
        >>> print(y)
        {
            a: startai.array([1, 2, 3]),
            b: startai.array([4, 5, 6])
        }

        >>> x = startai.Container(a=startai.array([[2, 3], [5, 7], [11, 13]]),
                              b=startai.array([[3, 4], [4, 5], [5, 6]]))
        >>> y = startai.Container(a = startai.zeros((3, 2)), b = startai.zeros((3, 2)))
        >>> startai.Container.static_cummax(x, axis=1, out=y)
        >>> print(y)
        {
            a: startai.array([[2., 3.],
                          [5., 7.],
                          [11., 13.]]),
            b: startai.array([[3., 4.],
                          [4., 5.],
                          [5., 6.]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "cummax",
            x,
            axis=axis,
            exclusive=exclusive,
            reverse=reverse,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            dtype=dtype,
            out=out,
        )

    @staticmethod
    def _static_cummin(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        axis: Union[int, startai.Container] = 0,
        exclusive: Union[bool, startai.Container] = False,
        reverse: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.cummin. This method
        simply wraps the function, and so the docstring for startai.cummin also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input array or container to cummin.
        axis
            Axis to cummin along. Default is ``0``.
        exclusive
            Whether to exclude the first element of the input array.
            Default is ``False``.
        reverse
            Whether to perform the cummin from last to first element in the selected
            axis. Default is ``False`` (from first to last element)
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
        dtype
            Data type of the returned array. Default is ``None``.
        out
            Optional output container. Default is ``None``.

        Returns
        -------
        ret
            Containers with arrays cummin at leaves along specified axis.

        Examples #TODO: fix examples and this doc
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([4, 5, 6]))
        >>> y = startai.Container.static_cummin(x, axis=0)
        >>> print(y)
        {
            a: startai.array([1, 1, 1]),
            b: startai.array([4, 4, 4])
        }

        >>> x = startai.Container(a=startai.array([[2, 3], [5, 7], [11, 13]]),
                              b=startai.array([[3, 4], [4, 5], [5, 6]]))
        >>> y = startai.Container(a = startai.zeros((3, 2)), b = startai.zeros((3, 2)))
        >>> x.static_cummin(axis=1, out=y)
        {
            a: startai.array([[2, 2],
                          [5, 5],
                          [11, 11]]),
            b: startai.array([[3, 3],
                          [4, 4],
                          [5, 5]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "cummin",
            x,
            axis=axis,
            exclusive=exclusive,
            reverse=reverse,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            dtype=dtype,
            out=out,
        )
