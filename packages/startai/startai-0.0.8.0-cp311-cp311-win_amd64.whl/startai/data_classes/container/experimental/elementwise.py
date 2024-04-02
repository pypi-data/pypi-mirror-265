# global
from typing import Optional, Union, List, Dict, Tuple, Sequence
from numbers import Number

# local
import startai
from startai.data_classes.container.base import ContainerBase


class _ContainerWithElementWiseExperimental(ContainerBase):
    @staticmethod
    def static_amax(
        x: startai.Container,
        /,
        *,
        axis: Optional[Union[int, Sequence[int], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.amax. This method simply
        wraps the function, and so the docstring for startai.amax also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued data type.
        axis
            axis or axes along which maximum values must be computed.
            By default, the maximum value must be computed over the
            entire array. If a tuple of integers, maximum values must
            be computed over multiple axes. Default: ``None``.
        keepdims
            optional boolean, if ``True``, the reduced axes
            (dimensions) must be included in the result as singleton
            dimensions, and, accordingly, the result must be
            compatible with the input array
            (see `broadcasting<https://data-apis.org/array-api/
            latest/API_specification/
            broadcasting.html#broadcasting>`_).
            Otherwise, if ``False``, the reduced axes (dimensions)
            must not be included in the result.
            Default: ``False``.
        key_chains
            The key-chains to apply or not apply the method to.
            Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains,
            otherwise key_chains will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was
            not applied. Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            container, if the maximum value was computed over the entire array,
            a zero-dimensional array containing the maximum value;
            otherwise, a non-zero-dimensional array containing the
            maximum values. The returned array must have the same data type
            as ``x``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container.static_amax(x)
        >>> print(y)
        {
            a: startai.array(3),
            b: startai.array(4)
        }

        >>> x = startai.Container(a=startai.array([[1, 2, 3], [-1, 0, 2]]),
        ...                   b=startai.array([[2, 3, 4], [0, 1, 2]]))
        >>> y = startai.Container.static_amax(x, axis=1)
        >>> print(y)
        {
            a:startai.array([3, 2]),
            b:startai.array([4, 2])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "amax",
            x,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def amax(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, Sequence[int], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.amax. This method
        simply wraps the function, and so the docstring for startai.amax also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued data type.
        axis
            axis or axes along which maximum values must be computed.
            By default, the maximum value must be computed over the
            entire array. If a tuple of integers, maximum values must
            be computed over multiple axes. Default: ``None``.
        keepdims
            optional boolean, if ``True``, the reduced axes
            (dimensions) must be included in the result as singleton
            dimensions, and, accordingly, the result must be
            compatible with the input array
            (see `broadcasting<https://data-apis.org/array-api/
            latest/API_specification/
            broadcasting.html#broadcasting>`_).
            Otherwise, if ``False``, the reduced axes (dimensions)
            must not be included in the result.
            Default: ``False``.
        key_chains
            The key-chains to apply or not apply the method to.
            Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains,
            otherwise key_chains will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was
            not applied. Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            container, if the maximum value was computed over the entire array,
            a zero-dimensional array containing the maximum value;
            otherwise, a non-zero-dimensional array containing the
            maximum values. The returned array must have the same data type
            as ``x``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = x.amax()
        >>> print(y)
        {
            a: startai.array(3),
            b: startai.array(4)
        }

        >>> x = startai.Container(a=startai.array([[1, 2, 3], [-1, 0, 2]]),
        ...                   b=startai.array([[2, 3, 4], [0, 1, 2]]))
        >>> y = x.amax(axis=1)
        >>> print(y)
        {
            a:startai.array([3, 2]),
            b:startai.array([4, 2])
        }
        """
        return self.static_amax(
            self,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_amin(
        x: startai.Container,
        /,
        *,
        axis: Optional[Union[int, Sequence[int], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.amin. This method simply
        wraps the function, and so the docstring for startai.amin also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued data type.
        axis
            axis or axes along which minimum values must be computed.
            By default, the minimum value must be computed over the
            entire array. If a tuple of integers, minimum values must
            be computed over multiple axes. Default: ``None``.
        keepdims
            optional boolean, if ``True``, the reduced axes
            (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the
            result must be compatible with the input array
            (see `broadcasting<https://data-apis.org/array-api/latest/
            API_specification/broadcasting.html#broadcasting>`_). Otherwise,
            if ``False``, the reduced axes (dimensions)
            must not be included in the result.
            Default: ``False``.
        key_chains
            The key-chains to apply or not apply the method to.
            Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains,
            otherwise key_chains will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was
            not applied. Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            container, if the minimum value was computed over the entire array,
            a zero-dimensional array containing the minimum value;
            otherwise, a non-zero-dimensional array containing the
            minimum values. The returned array must have the same data type
            as ``x``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container.static_amin(x)
        >>> print(y)
        {
            a: startai.array(1),
            b: startai.array(2)
        }

        >>> x = startai.Container(a=startai.array([[1, 2, 3], [-1, 0, 2]]),
        ...                   b=startai.array([[2, 3, 4], [0, 1, 2]]))
        >>> y = startai.Container.static_amin(x, axis=1)
        >>> print(y)
        {
            a:startai.array([1, -1]),
            b:startai.array([2, 0])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "amin",
            x,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def amin(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, Sequence[int], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.amin. This method
        simply wraps the function, and so the docstring for startai.amin also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued data type.
        axis
            axis or axes along which minimum values must be computed.
            By default, the minimum value must be computed over the
            entire array. If a tuple of integers, minimum values must
            be computed over multiple axes. Default: ``None``.
        keepdims
            optional boolean, if ``True``, the reduced axes
            (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the
            result must be compatible with the input array
            (see `broadcasting<https://data-apis.org/array-api/latest/
            API_specification/broadcasting.html#broadcasting>`_). Otherwise,
            if ``False``, the reduced axes (dimensions)
            must not be included in the result.
            Default: ``False``.
        key_chains
            The key-chains to apply or not apply the method to.
            Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains,
            otherwise key_chains will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was
            not applied. Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            container, if the minimum value was computed over the entire array,
            a zero-dimensional array containing the minimum value;
            otherwise, a non-zero-dimensional array containing the
            minimum values. The returned array must have the same data type
            as ``x``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = x.amin()
        >>> print(y)
        {
            a: startai.array(1),
            b: startai.array(2)
        }

        >>> x = startai.Container(a=startai.array([[1, 2, 3], [-1, 0, 2]]),
        ...                   b=startai.array([[2, 3, 4], [0, 1, 2]]))
        >>> y = x.amin(axis=1)
        >>> print(y)
        {
            a:startai.array([1, -1]),
            b:startai.array([2, 0])
        }
        """
        return self.static_amin(
            self,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_sinc(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.sinc. This method simply
        wraps the function, and so the docstring for startai.sinc also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container whose elements are each expressed in radians.
            Should have a floating-point data type.
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
            a container containing the sinc of each element in ``x``. The returned
            container must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0.5, 1.5, 2.5]),
        ...                   b=startai.array([3.5, 4.5, 5.5]))
        >>> y = startai.Container.static_sinc(x)
        >>> print(y)
        {
            a: startai.array([0.636, -0.212, 0.127]),
            b: startai.array([-0.090, 0.070, -0.057])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "sinc",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def sinc(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.sinc. This method
        simply wraps the function, and so the docstring for startai.sinc also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container whose elements are each expressed in radians.
            Should have a floating-point data type.
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
            a container containing the sinc of each element in ``self``.
            The returned container must have a floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0.5, 1.5, 2.5]),
        ...                   b=startai.array([3.5, 4.5, 5.5]))
        >>> y = x.sinc()
        >>> print(y)
        {
            a: startai.array([0.637,-0.212,0.127]),
            b: startai.array([-0.0909,0.0707,-0.0579])
        }
        """
        return self.static_sinc(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_fmod(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        x2: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.fmod. This method simply
        wraps the function, and so the docstring for startai.fmod also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            container with the first input arrays.
        x2
            container with the second input arrays
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise remainder of divisions.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([2, 3, 4]),\
                               b=startai.array([startai.nan, 0, startai.nan]))
        >>> x2 = startai.Container(a=startai.array([1, 5, 2]),\
                               b=startai.array([0, startai.nan, startai.nan]))
        >>> startai.Container.static_fmod(x1, x2)
        {
            a: startai.array([ 0,  3,  0])
            b: startai.array([ nan,  nan,  nan])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "fmod",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def fmod(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.fmod. This method
        simply wraps the function, and so the docstring for startai.fmod also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            container with the first input arrays.
        x2
            container with the second input arrays
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise remainder of divisions.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([2, 3, 4]),\
                               b=startai.array([startai.nan, 0, startai.nan]))
        >>> x2 = startai.Container(a=startai.array([1, 5, 2]),\
                               b=startai.array([0, startai.nan, startai.nan]))
        >>> x1.fmod(x2)
        {
            a: startai.array([ 0,  3,  0])
            b: startai.array([ nan,  nan,  nan])
        }
        """
        return self.static_fmod(self, x2, out=out)

    @staticmethod
    def static_fmax(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        x2: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.fmax. This method simply
        wraps the function, and so the docstring for startai.fmax also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            container with the first input arrays.
        x2
            container with the second input arrays
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise maximums.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([2, 3, 4]),\
                               b=startai.array([startai.nan, 0, startai.nan]))
        >>> x2 = startai.Container(a=startai.array([1, 5, 2]),\
                               b=startai.array([0, startai.nan, startai.nan]))
        >>> startai.Container.static_fmax(x1, x2)
        {
            a: startai.array([ 2.,  5.,  4.])
            b: startai.array([ 0,  0,  nan])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "fmax",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def fmax(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.fmax. This method
        simply wraps the function, and so the docstring for startai.fmax also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            container with the first input arrays.
        x2
            container with the second input arrays
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise maximums.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([2, 3, 4]),\
                               b=startai.array([startai.nan, 0, startai.nan]))
        >>> x2 = startai.Container(a=startai.array([1, 5, 2]),\
                               b=startai.array([0, startai.nan, startai.nan]))
        >>> x1.fmax(x2)
        {
            a: startai.array([ 2.,  5.,  4.])
            b: startai.array([ 0,  0,  nan])
        }
        """
        return self.static_fmax(self, x2, out=out)

    @staticmethod
    def static_float_power(
        x1: Union[startai.Array, startai.NativeArray, startai.Container, float, list, tuple],
        x2: Union[startai.Array, startai.NativeArray, startai.Container, float, list, tuple],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.float_power. This method
        simply wraps the function, and so the docstring for startai.float_power
        also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            container with the base input arrays.
        x2
            container with the exponent input arrays
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with base arrays raised to the powers
            of exponents arrays, element-wise .

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1, 2, 3]),\
                               b=startai.array([2, 10]))
        >>> x2 = startai.Container(a=startai.array([1, 3, 1]), b=0)
        >>> startai.Container.static_float_power(x1, x2)
        {
            a: startai.array([1,  8,  3])
            b: startai.array([1, 1])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "float_power",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def float_power(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.float_power. This
        method simply wraps the function, and so the docstring for
        startai.float_power also applies to this method with minimal changes.

        Parameters
        ----------
        self
            container with the base input arrays.
        x2
            container with the exponent input arrays
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with base arrays raised to the powers
            of exponents arrays, element-wise .

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1, 2, 3]),\
                               b=startai.array([2, 10]))
        >>> x2 = startai.Container(a=startai.array([1, 3, 1]), b=0)
        >>> x1.float_power(x2)
        {
            a: startai.array([1,  8,  3])
            b: startai.array([1, 1])
        }
        """
        return self.static_float_power(self, x2, out=out)

    @staticmethod
    def static_copysign(
        x1: Union[startai.Array, startai.NativeArray, startai.Container, Number],
        x2: Union[startai.Array, startai.NativeArray, startai.Container, Number],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.copysign. This method
        simply wraps the function, and so the docstring for startai.copysign also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            Container, Array, or scalar to change the sign of
        x2
            Container, Array, or scalar from which the new signs are applied
            Unsigned zeroes are considered positive.
        out
            optional output Container, for writing the result to.

        Returns
        -------
        ret
            x1 with the signs of x2.
            This is a scalar if both x1 and x2 are scalars.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([0,1,2]), b=startai.array(-1))
        >>> x2 = startai.Container(a=-1, b=startai.array(10))
        >>> startai.Container.static_copysign(x1, x2)
        {
            a: startai.array([-0., -1., -2.]),
            b: startai.array(1.)
        }
        >>> startai.Container.static_copysign(23, x1)
        {
            a: startai.array([23., 23., 23.]),
            b: startai.array(-23.)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "copysign",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def copysign(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.copysign. This method
        simply wraps the function, and so the docstring for startai.copysign also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Container to change the sign of
        x2
            Container from which the new signs are applied
            Unsigned zeroes are considered positive.
        out
            optional output Container, for writing the result to.

        Returns
        -------
        ret
            x1 with the signs of x2.
            This is a scalar if both x1 and x2 are scalars.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([0,1,2]), b=startai.array(-1))
        >>> x2 = startai.Container(a=-1, b=startai.array(10))
        >>> x1.copysign(x2)
        {
            a: startai.array([-0., -1., -2.]),
            b: startai.array(1.)
        }
        >>> x1.copysign(-1)
        {
            a: startai.array([-0., -1., -2.]),
            b: startai.array(-1.)
        }
        """
        return self.static_copysign(self, x2, out=out)

    @staticmethod
    def static_count_nonzero(
        a: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Optional[Union[int, Tuple[int, ...], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.count_nonzero. This
        method simply wraps the function, and so the docstring for
        startai.count_nonzero also applies to this method with minimal changes.

        Parameters
        ----------
        a
            container with the base input arrays.
        axis
            optional axis or tuple of axes along which to count non-zeros. Default is
            None, meaning that non-zeros will be counted along a flattened
            version of the input array.
        keepdims
            optional, if this is set to True, the axes that are counted are left in the
            result as dimensions with size one. With this option, the result
            will broadcast correctly against the input array.
        dtype
            optional output dtype. Default is of type integer.
        key_chains
            The key-chains to apply or not apply the method to. Default is None.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is True.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is False.
        map_sequences
            Whether to also map method to sequences (lists, tuples). Default is False.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including number of non-zero values in the array along a
            given axis. Otherwise, container with the total number of non-zero
            values in the array is returned.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[0, 1, 2, 3],[4, 5, 6, 7]]),\
                        b=startai.array([[[0,1],[2,3]],[[4,5],[6,7]]]))
        >>> startai.Container.static_count_nonzero(x)
        {
            a: startai.array(7),
            b: startai.array(7)
        }
        >>> x = startai.Container(a=startai.array([[0, 1, 2, 3],[4, 5, 6, 7]]),\
                        b=startai.array([[[0,1],[2,3]],[[4,5],[6,7]]]))
        >>> startai.Container.static_count_nonzero(x, axis=0)
        {
            a: startai.array([1, 2, 2, 2]),
            b: startai.array([[1, 2],
                          [2, 2]])
        }
        >>> x = startai.Container(a=startai.array([[0, 1, 2, 3],[4, 5, 6, 7]]),\
                        b=startai.array([[[0,1],[2,3]],[[4,5],[6,7]]]))
        >>> startai.Container.static_count_nonzero(x, axis=(0,1), keepdims=True)
        {
            a: startai.array([[7]]),
            b: startai.array([[[3, 4]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "count_nonzero",
            a,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def count_nonzero(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, Tuple[int, ...], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.count_nonzero. This
        method simply wraps the function, and so the docstring for
        startai.count_nonzero also applies to this method with minimal changes.

        Parameters
        ----------
        self
            container with the base input arrays.
        axis
            optional axis or tuple of axes along which to count non-zeros. Default is
            None, meaning that non-zeros will be counted along a flattened
            version of the input array.
        keepdims
            optional, if this is set to True, the axes that are counted are left in the
            result as dimensions with size one. With this option, the result
            will broadcast correctly against the input array.
        dtype
            optional output dtype. Default is of type integer.
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
            Default is ``False``
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including number of non-zero values in the array along a
            given axis. Otherwise, container with the total number of non-zero
            values in the array is returned.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[0, 1, 2, 3],[4, 5, 6, 7]]),\
                        b=startai.array([[[0,1],[2,3]],[[4,5],[6,7]]]))
        >>> x.count_nonzero()
        {
            a: startai.array(7),
            b: startai.array(7)
        }
        >>> x = startai.Container(a=startai.array([[0, 1, 2, 3],[4, 5, 6, 7]]),\
                        b=startai.array([[[0,1],[2,3]],[[4,5],[6,7]]]))
        >>> x.count_nonzero(axis=0)
        {
            a: startai.array([1, 2, 2, 2]),
            b: startai.array([[1, 2],
                          [2, 2]])
        }
        >>> x = startai.Container(a=startai.array([[0, 1, 2, 3],[4, 5, 6, 7]]),\
                        b=startai.array([[[0,1],[2,3]],[[4,5],[6,7]]]))
        >>> x.count_nonzero(axis=(0,1), keepdims=True)
        {
            a: startai.array([[7]]),
            b: startai.array([[[3, 4]]])
        }
        """
        return self.static_count_nonzero(
            self,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_nansum(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        axis: Optional[Union[tuple, int, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.nansum. This method
        simply wraps the function, and so the docstring for startai.nansum also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input array.
        axis
            Axis or axes along which the sum is computed.
            The default is to compute the sum of the flattened array.
        dtype
            The type of the returned array and of the accumulator in
            which the elements are summed. By default, the dtype of input is used.
        keepdims
            If this is set to True, the axes which are reduced are left
            in the result as dimensions with size one.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            A new array holding the result is returned unless out is specified,
            in which it is returned.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([[10, 7, 4], [3, 2, 1]]),\
                b=startai.array([[1, 4, 2], [startai.nan, startai.nan, 0]]))
        >>> startai.Container.static_nansum(x)
        {
            a: 27,
            b: 7.0
        }
        >>> startai.Container.static_nansum(x, axis=0)
        {
            a: startai.array([13, 9, 5]),
            b: startai.array([1., 4., 2.])
        }
        >>> startai.Container.static_nansum(x, axis=1)
        {
            a: startai.array([21, 6]),
            b: startai.array([7., 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "nansum",
            x,
            axis=axis,
            dtype=dtype,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def nansum(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[tuple, int, startai.Container]] = None,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.nansum. This method
        simply wraps the function, and so the docstring for startai.nansum also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container including arrays.
        axis
            Axis or axes along which the sum is computed.
            The default is to compute the sum of the flattened array.
        dtype
            The type of the returned array and of the accumulator in
            which the elements are summed. By default, the dtype of input is used.
        keepdims
            If this is set to True, the axes which are reduced are left
            in the result as dimensions with size one.
        out
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            A new array holding the result is returned unless out is specified,
            in which it is returned.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([[10, 7, 4], [3, 2, 1]]),\
                b=startai.array([[1, 4, 2], [startai.nan, startai.nan, 0]]))
        >>> x.nansum(axis=0)
        {
            a: startai.array([13, 9, 5]),
            b: startai.array([1., 4., 2.])
        }
        >>> x.nansum(axis=1)
        {
            a: startai.array([21, 6]),
            b: startai.array([7., 0.])
        }
        """
        return self.static_nansum(
            self, axis=axis, dtype=dtype, keepdims=keepdims, out=out
        )

    @staticmethod
    def static_isclose(
        a: Union[startai.Container, startai.Array, startai.NativeArray],
        b: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        rtol: Union[float, startai.Container] = 1e-05,
        atol: Union[float, startai.Container] = 1e-08,
        equal_nan: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.isclose. This method
        simply wraps the function, and so the docstring for startai.isclose also
        applies to this method with minimal changes.

        Parameters
        ----------
        a
            Input container containing first input array.
        b
            Input container containing second input array.
        rtol
            The relative tolerance parameter.
        atol
            The absolute tolerance parameter.
        equal_nan
            Whether to compare NaN's as equal. If True, NaN's in a will be
            considered equal to NaN's in b in the output array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            A new array holding the result is returned unless out is specified,
            in which it is returned.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1.0, startai.nan]),\
                b=startai.array([1.0, startai.nan]))
        >>> y = startai.Container(a=startai.array([1.0, startai.nan]),\
                b=startai.array([1.0, startai.nan]))
        >>> startai.Container.static_isclose(x, y)
        {
            a: startai.array([True, False]),
            b: startai.array([True, False])
        }
        >>> startai.Container.static_isclose(x, y, equal_nan=True)
        {
            a: startai.array([True, True]),
            b: startai.array([True, True])
        }
        >>> x = startai.Container(a=startai.array([1.0, 2.0]),\
                b=startai.array([1.0, 2.0]))
        >>> y = startai.Container(a=startai.array([1.0, 2.001]),\
                b=startai.array([1.0, 2.0]))
        >>> startai.Container.static_isclose(x, y, atol=0.0)
        {
            a: startai.array([True, False]),
            b: startai.array([True, True])
        }
        >>> startai.Container.static_isclose(x, y, rtol=0.01, atol=0.0)
        {
            a: startai.array([True, True]),
            b: startai.array([True, True])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "isclose",
            a,
            b,
            rtol=rtol,
            atol=atol,
            equal_nan=equal_nan,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def isclose(
        self: startai.Container,
        b: startai.Container,
        /,
        *,
        rtol: Union[float, startai.Container] = 1e-05,
        atol: Union[float, startai.Container] = 1e-08,
        equal_nan: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.isclose. This method
        simply wraps the function, and so the docstring for startai.isclose also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container containing first input array.
        b
            Input container containing second input array.
        rtol
            The relative tolerance parameter.
        atol
            The absolute tolerance parameter.
        equal_nan
            Whether to compare NaN's as equal. If True, NaN's in a will be
            considered equal to NaN's in b in the output array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            A new array holding the result is returned unless out is specified,
            in which it is returned.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1.0, startai.nan]),\
                b=startai.array([1.0, startai.nan]))
        >>> y = startai.Container(a=startai.array([1.0, startai.nan]),\
                b=startai.array([1.0, startai.nan]))
        >>> x.isclose(y)
        {
            a: startai.array([True, False]),
            b: startai.array([True, False])
        }
        >>> x.isclose(y, equal_nan=True)
        {
            a: startai.array([True, True]),
            b: startai.array([True, True])
        }
        >>> x = startai.Container(a=startai.array([1.0, 2.0]),\
                b=startai.array([1.0, 2.0]))
        >>> y = startai.Container(a=startai.array([1.0, 2.001]),\
                b=startai.array([1.0, 2.0]))
        >>> x.isclose(y, atol=0.0)
        {
            a: startai.array([True, False]),
            b: startai.array([True, True])
        }
        >>> x.isclose(y, rtol=0.01, atol=0.0)
        {
            a: startai.array([True, True]),
            b: startai.array([True, True])
        }
        """
        return self.static_isclose(
            self,
            b,
            rtol=rtol,
            atol=atol,
            equal_nan=equal_nan,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_signbit(
        x: Union[startai.Array, startai.NativeArray, startai.Container, float, int, list, tuple],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.signbit. This method
        simply wraps the function, and so the docstring for startai.signbit also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container with array-like items.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise signbit of input arrays.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, -2, 3]),\
                               b=-5)
        >>> startai.Container.static_signbit(x)
        {
            a: startai.array([False, True, False])
            b: startai.array([True])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "signbit",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def signbit(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.signbit. This method
        simply wraps the function, and so the docstring for startai.signbit also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container with array-like items.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise signbit of input arrays.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, -2, 3]),\
                               b=-5)
        >>> x.signbit()
        {
            a: startai.array([False, True, False])
            b: startai.array([True])
        }
        """
        return self.static_signbit(self, out=out)

    @staticmethod
    def static_hypot(
        x1: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.hypot. This method simply
        wraps the function, and so the docstring for startai.hypot also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            Input container containing first input array.
        x2
            Input container containing second input array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the hypot function computed element-wise

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.0]),\
        ...                         b=startai.array([3.0]))
        >>> y = startai.Container(a=startai.array([3.0]),\
                                    b=startai.array([4.0]))
        >>> startai.Container.static_hypot(x, y)
        {
            a: startai.array([3.6055]),
            b: startai.array([5.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "hypot",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def hypot(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.hypot. This method
        simply wraps the function, and so the docstring for startai.hypot also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container containing first input array.
        x2
            Input container containing second input array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the hypot function computed element-wise

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.0]),\
        ...                         b=startai.array([3.0]))
        >>> y = startai.Container(a=startai.array([3.0]),\
                                    b=startai.array([4.0]))
        >>> x.hypot(y)
        {
            a: startai.array([3.6055]),
            b: startai.array([5.])
        }
        """
        return self.static_hypot(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_allclose(
        x1: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        rtol: Union[float, startai.Container] = 1e-05,
        atol: Union[float, startai.Container] = 1e-08,
        equal_nan: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.allclose. This method
        simply wraps the function, and so the docstring for startai.allclose also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            Input container containing first input array.
        x2
            Input container containing second input array.
        rtol
            The relative tolerance parameter.
        atol
            The absolute tolerance parameter.
        equal_nan
            Whether to compare NaN's as equal. If True, NaN's in x1 will be
            considered equal to NaN's in x2 in the output array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            A new container holding the result is returned unless out is specified,
            in which it is returned.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1., 2., 3.]),\
        ...                         b=startai.array([1., 2., 3.]))
        >>> x2 = startai.Container(a=startai.array([1., 2., 3.]),\
        ...                         b=startai.array([1., 2., 3.]))
        >>> y = startai.Container.static_allclose(x1, x2)
        >>> print(y)
        {
            a: startai.array(True),
            b: startai.array(True)
        }

        >>> x1 = startai.Container(a=startai.array([1., 2., 3.]),\
        ...                         b=startai.array([1., 2., 3.]))
        >>> x2 = startai.Container(a=startai.array([1., 2., 3.0003]),\
        ...                         b=startai.array([1.0006, 2., 3.]))
        >>> y = startai.Container.static_allclose(x1, x2, rtol=1e-3)
        >>> print(y)
        {
            a: startai.array(True),
            b: startai.array(True)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "allclose",
            x1,
            x2,
            rtol=rtol,
            atol=atol,
            equal_nan=equal_nan,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def allclose(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        rtol: Union[float, startai.Container] = 1e-05,
        atol: Union[float, startai.Container] = 1e-08,
        equal_nan: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.allclose. This method
        simply wraps the function, and so the docstring for startai.allclose also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container containing first input array.
        x2
            Input container containing second input array.
        rtol
            The relative tolerance parameter.
        atol
            The absolute tolerance parameter.
        equal_nan
            Whether to compare NaN's as equal. If True, NaN's in x1 will be
            considered equal to NaN's in x2 in the output array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            A new container holding the result is returned unless out is specified,
            in which it is returned.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([1., 2., 3.]))
        >>> x2 = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([1., 2., 3.]))
        >>> y = x1.allclose(x2)
        >>> print(y)
        {
            a: startai.array(True),
            b: startai.array(True)
        }

        >>> x1 = startai.Container(a=startai.array([1., 2., 3.]),
        ...                         b=startai.array([1., 2., 3.]))
        >>> x2 = startai.Container(a=startai.array([1., 2., 3.0003]),
        ...                         b=startai.array([1.0006, 2., 3.]))
        >>> y = x1.allclose(x2, rtol=1e-3)
        >>> print(y)
        {
            a: startai.array(True),
            b: startai.array(True)
        }
        """
        return self.static_allclose(
            self,
            x2,
            rtol=rtol,
            atol=atol,
            equal_nan=equal_nan,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_diff(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        n: Union[int, startai.Container] = 1,
        axis: Union[int, startai.Container] = -1,
        prepend: Optional[
            Union[startai.Array, startai.NativeArray, int, list, tuple, startai.Container]
        ] = None,
        append: Optional[
            Union[startai.Array, startai.NativeArray, int, list, tuple, startai.Container]
        ] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.diff. This method simply
        wraps the function, and so the docstring for startai.diff also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container with array-like items.
        n
            The number of times values are differenced. If zero, the input is returned
            as-is.
        axis
            The axis along which the difference is taken, default is the last axis.
        prepend,append
            Values to prepend/append to x along given axis prior to performing the
            difference. Scalar values are expanded to arrays with length 1 in the
            direction of axis and the shape of the input array in along all other
            axes. Otherwise the dimension and shape must match x except along axis.
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
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with the n-th discrete difference along
            the given axis.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 4, 7, 0]),
                              b=startai.array([1, 2, 4, 7, 0]))
        >>> startai.Container.static_diff(x)
        {
            a: startai.array([ 1,  2,  3, -7]),
            b: startai.array([ 1,  2,  3, -7])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "diff",
            x,
            n=n,
            axis=axis,
            prepend=prepend,
            append=append,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def diff(
        self: startai.Container,
        /,
        *,
        n: Union[int, startai.Container] = 1,
        axis: Union[int, startai.Container] = -1,
        prepend: Optional[
            Union[startai.Array, startai.NativeArray, int, list, tuple, startai.Container]
        ] = None,
        append: Optional[
            Union[startai.Array, startai.NativeArray, int, list, tuple, startai.Container]
        ] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.diff. This method
        simply wraps the function, and so the docstring for startai.diff also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container with array-like items.
        n
            The number of times values are differenced. If zero, the input is returned
            as-is.
        axis
            The axis along which the difference is taken, default is the last axis.
        prepend,append
            Values to prepend/append to x along given axis prior to performing the
            difference. Scalar values are expanded to arrays with length 1 in the
            direction of axis and the shape of the input array in along all other
            axes. Otherwise the dimension and shape must match x except along axis.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with the n-th discrete difference along the
            given axis.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 4, 7, 0]),
                              b=startai.array([1, 2, 4, 7, 0]))
        >>> x.diff()
        {
            a: startai.array([1, 2, 3, -7]),
            b: startai.array([1, 2, 3, -7])
        }
        """
        return self.static_diff(
            self, n=n, axis=axis, prepend=prepend, append=append, out=out
        )

    @staticmethod
    def static_fix(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.fix. This method simply
        wraps the function, and so the docstring for startai.fix also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container with array items.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise rounding of
            input arrays elements.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.1, 2.9, -2.1]),\
                               b=startai.array([3.14]))
        >>> startai.Container.static_fix(x)
        {
            a: startai.array([ 2.,  2., -2.])
            b: startai.array([ 3.0 ])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "fix",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def fix(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.fix. This method simply
        wraps the function, and so the docstring for startai.fix also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container with array items.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise rounding of
            input arrays elements.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.1, 2.9, -2.1]),\
                               b=startai.array([3.14]))
        >>> x.fix()
        {
            a: startai.array([ 2.,  2., -2.])
            b: startai.array([ 3.0 ])
        }
        """
        return self.static_fix(self, out=out)

    @staticmethod
    def static_nextafter(
        x1: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.nextafter. This method
        simply wraps the function, and so the docstring for startai.nextafter also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            Input container containing first input arrays.
        x2
            Input container containing second input arrays.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the next representable values of
            input container's arrays, element-wise

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1.0e-50, 2.0e+50]),\
        ...                         b=startai.array([2.0, 1.0])
        >>> x2 = startai.Container(a=startai.array([5.5e-30]),\
        ...                         b=startai.array([-2.0]))
        >>> startai.Container.static_nextafter(x1, x2)
        {
            a: startai.array([1.4013e-45., 3.4028e+38]),
            b: startai.array([5.5e-30])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "nextafter",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def nextafter(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.nextafter. This method
        simply wraps the function, and so the docstring for startai.nextafter also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container containing first input array.
        x2
            Input container containing second input array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the next representable values of
            input container's arrays, element-wise

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1.0e-50, 2.0e+50]),\
        ...                         b=startai.array([2.0, 1.0])
        >>> x2 = startai.Container(a=startai.array([5.5e-30]),\
        ...                         b=startai.array([-2.0]))
        >>> x1.nextafter(x2)
        {
            a: startai.array([1.4013e-45., 3.4028e+38]),
            b: startai.array([5.5e-30])
        }
        """
        return self.static_nextafter(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_zeta(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        q: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.zeta. This method simply
        wraps the function, and so the docstring for startai.zeta also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            Input container containing first input arrays.
        q
            Input container containing second input arrays.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the zeta function computed element-wise

        Examples
        --------
        >>> x = startai.Container(a=startai.array([5.0, 3.0]),\
        ...                         b=startai.array([2.0, 1.0])
        >>> q = startai.Container(a=startai.array([2.0]),\
        ...                         b=startai.array([5.0]))
        >>> startai.Container.static_zeta(x1, x2)
        {
            a: startai.array([0.0369, 0.2021]),
            b: startai.array([0.0006, 0.0244])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "zeta",
            x,
            q,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def zeta(
        self: startai.Container,
        q: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.zeta. This method
        simply wraps the function, and so the docstring for startai.zeta also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container containing first input array.
        q
            Input container containing second input array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the zeta function computed element-wise

        Examples
        --------
        >>> x = startai.Container(a=startai.array([5.0, 3.0]),\
        ...                         b=startai.array([2.0, 1.0])
        >>> q = startai.Container(a=startai.array([2.0]),\
        ...                         b=startai.array([5.0]))
        >>> x.zeta(q)
        {
            a: startai.array([0.0369, 0.2021]),
            b: startai.array([0.0006, 0.0244])
        }
        """
        return self.static_zeta(
            self,
            q,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_gradient(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        spacing: Union[int, list, tuple, startai.Container] = 1,
        edge_order: Union[int, startai.Container] = 1,
        axis: Optional[Union[int, list, tuple, startai.Container]] = None,
    ) -> startai.Container:
        return ContainerBase.cont_multi_map_in_function(
            "gradient",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            spacing=spacing,
            edge_order=edge_order,
            axis=axis,
        )

    def gradient(
        self: startai.Container,
        /,
        *,
        spacing: Union[int, list, tuple, startai.Container] = 1,
        edge_order: Union[int, startai.Container] = 1,
        axis: Optional[Union[int, list, tuple, startai.Container]] = None,
    ) -> startai.Container:
        """Calculate gradient of x with respect to (w.r.t.) spacing.

        Parameters
        ----------
            x
                input array representing outcomes of the function
                spacing
                if not given, indices of x will be used
                if scalar indices of x will be scaled with this value
                if array gradient of x w.r.t. spacing
            edge_order
                1 or 2, for 'frist order' and 'second order' estimation
                of boundary values of gradient respectively.
            axis
                dimension(s) to approximate the gradient over.
                By default, partial gradient is computed in every dimension


        Returns
        -------
        ret
            Array with values computed from gradient function from
            inputs

        Examples
        --------
        >>> coordinates = startai.Container(
        >>>     a=(startai.array([-2., -1., 1., 4.]),),
        >>>     b=(startai.array([2., 1., -1., -4.]),)
        >>> )
        >>> values = startai.Container(
        >>>     a=startai.array([4., 1., 1., 16.]),
        >>>     b=startai.array([4., 1., 1., 16.])
        >>> )
        >>> startai.gradient(values, spacing=coordinates)
        {
            a: startai.array([-3., -2., 2., 5.]),
            b: startai.array([3., 2., -2., -5.])
        }

        >>> values = startai.Container(
        >>>     a=startai.array([[1, 2, 4, 8], [10, 20, 40, 80]]),
        >>>     b=startai.array([[-1, -2, -4, -8], [-10, -20, -40, -80]])
        >>> )
        >>> startai.gradient(values)
        [{
            a: startai.array([[9., 18., 36., 72.],
                          [9., 18., 36., 72.]]),
            b: startai.array([[-9., -18., -36., -72.],
                          [-9., -18., -36., -72.]])
        }, {
            a: startai.array([[1., 1.5, 3., 4.],
                          [10., 15., 30., 40.]]),
            b: startai.array([[-1., -1.5, -3., -4.],
                          [-10., -15., -30., -40.]])
        }]

        >>> values = startai.Container(
        >>>     a=startai.array([[1, 2, 4, 8], [10, 20, 40, 80]]),
        >>>     b=startai.array([[-1, -2, -4, -8], [-10, -20, -40, -80]])
        >>> )
        >>> startai.gradient(values, spacing=2.0)
        [{
            a: startai.array([[4.5, 9., 18., 36.],
                          [4.5, 9., 18., 36.]]),
            b: startai.array([[-4.5, -9., -18., -36.],
                          [-4.5, -9., -18., -36.]])
        }, {
            a: startai.array([[0.5, 0.75, 1.5, 2.],
                          [5., 7.5, 15., 20.]]),
            b: startai.array([[-0.5, -0.75, -1.5, -2.],
                          [-5., -7.5, -15., -20.]])
        }]

        >>> values = startai.Container(
        >>>     a=startai.array([[1, 2, 4, 8], [10, 20, 40, 80]]),
        >>>     b=startai.array([[-1, -2, -4, -8], [-10, -20, -40, -80]])
        >>> )
        >>> startai.gradient(values, axis=1)
        {
            a: startai.array([[1., 1.5, 3., 4.],
                          [10., 15., 30., 40.]]),
            b: startai.array([[-1., -1.5, -3., -4.],
                          [-10., -15., -30., -40.]])
        }

        >>> values = startai.Container(
        >>>     a=startai.array([[1, 2, 4, 8], [10, 20, 40, 80]]),
        >>>     b=startai.array([[-1, -2, -4, -8], [-10, -20, -40, -80]])
        >>> )
        >>> startai.gradient(values, spacing = [3., 2.])
        [{
            a: startai.array([[3., 6., 12., 24.],
                          [3., 6., 12., 24.]]),
            b: startai.array([[-3., -6., -12., -24.],
                          [-3., -6., -12., -24.]])
        }, {
            a: startai.array([[0.5, 0.75, 1.5, 2.],
                          [5., 7.5, 15., 20.]]),
            b: startai.array([[-0.5, -0.75, -1.5, -2.],
                          [-5., -7.5, -15., -20.]])
        }]

        >>> coords = startai.Container(
        >>>    a=(startai.array([0, 2]), startai.array([0, 3, 6, 9])),
        >>>    b=(startai.array([0, -2]), startai.array([0, -3, -6, -9]))
        >>>)
        >>> values = startai.Container(
        >>>     a=startai.array([[1, 2, 4, 8], [10, 20, 40, 80]]),
        >>>     b=startai.array([[-1, -2, -4, -8], [-10, -20, -40, -80]])
        >>>)
        >>> startai.gradient(values, spacing = coords)
        [{
            a: startai.array([[4.5, 9., 18., 36.],
                          [4.5, 9., 18., 36.]]),
            b: startai.array([[4.5, 9., 18., 36.],
                          [4.5, 9., 18., 36.]])
        }, {
            a: startai.array([[0.33333333, 0.5, 1., 1.33333333],
                          [3.33333333, 5., 10., 13.33333333]]),
            b: startai.array([[0.33333333, 0.5, 1., 1.33333333],
                          [3.33333333, 5., 10., 13.33333333]])
        }]
        """
        return self.static_gradient(
            self, spacing=spacing, edge_order=edge_order, axis=axis
        )

    @staticmethod
    def static_xlogy(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        y: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.xlogy. This method simply
        wraps the function, and so the docstring for startai.xlogy also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            Input container containing first input arrays.
        y
            Input container containing second input arrays.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the next representable values of
            input container's arrays, element-wise

        Examples
        --------
        >>> x = startai.Container(a=startai.zeros(3)),\
        ...                         b=startai.array([1.0, 2.0, 3.0]))
        >>> y = startai.Container(a=startai.array([-1.0, 0.0, 1.0]),\
        ...                         b=startai.array([3.0, 2.0, 1.0]))
        >>> startai.Container.static_xlogy(x, y)
        {
            a: startai.array([0.0, 0.0, 0.0]),
            b: startai.array([1.0986, 1.3863, 0.0000])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "xlogy",
            x,
            y,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def xlogy(
        self: startai.Container,
        y: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.xlogy. This method
        simply wraps the function, and so the docstring for startai.xlogy also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container containing first input array.
        y
            Input container containing second input array.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the next representable values of
            input container's arrays, element-wise

        Examples
        --------
        >>> x = startai.Container(a=startai.zeros(3)),\
        ...                         b=startai.array([1.0, 2.0, 3.0]))
        >>> y = startai.Container(a=startai.array([-1.0, 0.0, 1.0]),\
        ...                         b=startai.array([3.0, 2.0, 1.0]))
        >>> x.xlogy(y)
        {
            a: startai.array([0.0, 0.0, 0.0]),
            b: startai.array([1.0986, 1.3863, 0.0000])
        }
        """
        return self.static_xlogy(
            self,
            y,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_binarizer(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        threshold: Union[float, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """Map the values of the input tensor to either 0 or 1, element-wise,
        based on the outcome of a comparison against a threshold value.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
        threshold
            Values greater than this are
            mapped to 1, others to 0.
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
            Binarized output data
        """
        return ContainerBase.cont_multi_map_in_function(
            "binarizer",
            x,
            threshold=threshold,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def binarizer(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        *,
        threshold: Union[float, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """Map the values of the input tensor to either 0 or 1, element-wise,
        based on the outcome of a comparison against a threshold value.

        Parameters
        ----------
        threshold
            Values greater than this are
            mapped to 1, others to 0.
        key_chains
            The keychains to apply or not apply the method to. Default is ``None``.
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
            Binarized output data
        """
        return self.static_binarizer(
            self,
            threshold=threshold,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_conj(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.conj. This method simply
        wraps the function, and so the docstring for startai.conj also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container.
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
            a container containing output array(s) of the same
            dtype as the input array(s) with the complex conjugates of
            the complex values present in the input array. If x is a
            container of scalar(s) then a container of scalar(s)
            will be returned.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1+5j, 0-0j, 1.23j]),
        ...                   b=startai.array([7.9, 0.31+3.3j, -4.2-5.9j]))
        >>> z = startai.Container.static_conj(x)
        >>> print(z)
        {
            a: startai.array([-1-5j, 0+0j, -1.23j]),
            b: startai.array([7.9, 0.31-3.3j, -4.2+5.9j])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "conj",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def conj(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.conj. This method
        simply wraps the function, and so the docstring for startai.conj also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container.
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
            a container containing output array(s) of the same dtype
            as the input array(s) with the complex conjugates of the
            complex values present in the input array.
            If x is a container of scalar(s) then a container of
            scalar(s) will be returned.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1j, 0.335+2.345j, 1.23+7j]),\
                          b=startai.array([0.0, 1.2+3.3j, 1+0j]))
        >>> x.conj()
        {
            a: startai.array([1j, 0.335-2345j, 1.23-7j]),
            b: startai.array([0.0, 1.2-3.3j, 1-0j])
        }
        """
        return self.static_conj(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_ldexp(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        x2: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.ldexp. This method simply
        wraps the function, and so the docstring for startai.ldexp also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            The container whose arrays should be multiplied by 2**i.
        x2
            The container whose arrays should be used to multiply x by 2**i.
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
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including x1 * 2**x2.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x1 = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([1, 5, 10]))
        >>> x2 = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([1, 5, 10]))
        >>> startai.Container.static_ldexp(x1, x2)
        {
            a: startai.array([2, 8, 24]),
            b: startai.array([2, 160, 10240])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "ldexp",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def ldexp(
        self: startai.Container,
        x2: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.ldexp. This method
        simply wraps the function, and so the docstring for startai.ldexp also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container whose arrays should be multiplied by 2**x2.
        x2
            The container whose arrays should be used to multiply x1 by 2**x2.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including x1 * 2**x2.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x1 = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([1, 5, 10]))
        >>> x2 = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([1, 5, 10]))
        >>> x1.ldexp(x2)
        {
            a: startai.array([2, 8, 24]),
            b: startai.array([2, 160, 10240])
        }
        """
        return self.static_ldexp(self, x2, out=out)

    @staticmethod
    def static_lerp(
        input: Union[startai.Array, startai.NativeArray, startai.Container],
        end: Union[startai.Array, startai.NativeArray, startai.Container],
        weight: Union[startai.Array, startai.NativeArray, float, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.lerp. This method simply
        wraps the function, and so the docstring for startai.lerp also applies to
        this method with minimal changes.

        Parameters
        ----------
        input
            The container whose arrays should be used as parameter: input
        end
            The container whose arrays should be used as parameter: end
        weight
            The container whose arrays or scalar should be used as parameter: weight
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
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including  input + ((end - input) * weight)

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> input = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.]))
        >>> end = startai.array([10.])
        >>> weight = 1.1
        >>> y = startai.Container.static_lerp(input, end, weight)
        >>> print(y)
        {
            a: startai.array([11., 10.90000057, 10.80000019]),
            b: startai.array([10.70000076, 10.60000038, 10.5])
        }
        >>> input = startai.Container(a=startai.array([10.1, 11.1]), b=startai.array([10, 11]))
        >>> end = startai.Container(a=startai.array([5]))
        >>> weight = startai.Container(a=0.5)
        >>> y = startai.Container.static_lerp(input, end, weight)
        >>> print(y)
        {
            a: startai.array([7.55000019, 8.05000019]),
            b: {
                a: startai.array([7.5, 8.])
            }
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "lerp",
            input,
            end,
            weight,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def lerp(
        self: startai.Container,
        end: Union[startai.Array, startai.NativeArray, startai.Container],
        weight: Union[startai.Array, startai.NativeArray, float, startai.Container],
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.lerp. This method
        simply wraps the function, and so the docstring for startai.lerp also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container whose arrays should be used as parameter: input
        end
            The container whose arrays should be used as parameter: end
        weight
            The container whose arrays or scalar should be used as parameter: weight
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including  input + ((end - input) * weight)

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> input = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([1, 5, 10]))
        >>> end = startai.Container(a=startai.array([10, 10, 10]), b=startai.array([20, 20, 20]))
        >>> weight = startai.Container(a=startai.array(0.5), b=startai.array([0.4, 0.5, 0.6]))
        >>> input.lerp(end, weight)
        {
            a: startai.array([5.5, 6., 6.5]),
            b: startai.array([8.60000038, 12.5, 16.])
        }
        """
        return self.static_lerp(self, end, weight, out=out)

    @staticmethod
    def static_frexp(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.frexp. This method simply
        wraps the function, and so the docstring for startai.frexp also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            The container whose arrays should be split into mantissa and exponent.
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
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including the mantissa and exponent of x.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array([1, 5, 10]))
        >>> startai.Container.static_frexp(x)
        {
            a: (startai.array([0.5, 0.5, 0.75]), startai.array([1, 1, 2])),
            b: (startai.array([0.5, 0.625, 0.625]), startai.array([1, 3, 4]))
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "frexp",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def frexp(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.frexp. This method
        simply wraps the function, and so the docstring for startai.frexp also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container whose arrays should be split into mantissa and exponent.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including the mantissa and exponent of x.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1, 2, 3]),\
                                            b=startai.array([1, 5, 10]))
        >>> x.frexp()
        {
            a: (startai.array([0.5, 0.5, 0.75]), startai.array([1, 1, 2])),
            b: (startai.array([0.5, 0.625, 0.625]), startai.array([1, 3, 4]))
        }
        """
        return self.static_frexp(self, out=out)

    @staticmethod
    def static_modf(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.modf. This method simply
        wraps the function, and so the docstring for startai.modf also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            The container whose arrays should be split into
            the fractional and integral parts.
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
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including the fractional and integral parts of x.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1.2, 2.7, 3.9]),
        >>> b = startai.array([-1.5, 5.3, -10.7]))
        >>> startai.Container.static_modf(x)
        {
            a: (startai.array([0.2, 0.7, 0.9]), startai.array([1.0, 2.0, 3.0])),
            b: (startai.array([-0.5, 0.3, -0.7]), startai.array([-1.0, 5.0, -10.0]))
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "modf",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def modf(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        r"""startai.Container instance method variant of startai.modf. This method
        simply wraps the function, and so the docstring for startai.modf also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container whose arrays should be split into
            the fractional and integral parts.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including the fractional and integral parts of x.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1.2, 2.7, 3.9]),
        >>> b = startai.array([-1.5, 5.3, -10.7]))
        >>> x.modf()
        {
            a: (startai.array([0.2, 0.7, 0.9]), startai.array([1.0, 2.0, 3.0])),
            b: (startai.array([-0.5, 0.3, -0.7]), startai.array([-1.0, 5.0, -10.0]))
        }
        """
        return self.static_modf(self, out=out)

    @staticmethod
    def static_digamma(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        out: Optional[startai.Array] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.digamma. This method
        simply wraps the function, and so the docstring for startai.digamma also
        applies to this method with minimal changes.

        Note
        ----
        The Startai version only accepts real-valued inputs.

        Parameters
        ----------
        x
            Input container containing input arrays.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the digamma function computed element-wise

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 0.5]),\
        ...                         b=startai.array([-2.0, 3.0]))
        >>> startai.Container.static_digamma(x)
        {
            a: startai.array([-0.57721537, -1.96351004]),
            b: startai.array([nan, 0.92278427])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "digamma",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def digamma(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.digamma. This method
        simply wraps the function, and so the docstring for startai.digamma also
        applies to this method with minimal changes.

        Note
        ----
        The Startai version only accepts real-valued inputs.

        Parameters
        ----------
        self
            Input container containing input arrays.
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
            Alternate output array in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the digamma function computed element-wise

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 0.5]), b=startai.array([2.0, 3.0])
        >>> x.digamma()
        {
            a: startai.array([-0.5772, -1.9635]),
            b: startai.array([0.4228, 0.9228])
        }
        """
        return self.static_digamma(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_sparsify_tensor(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        card: Union[int, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.sparsify_tensor. This
        method simply wraps the function, and so the docstring for
        startai.sparsify_tensor also applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input container containing input arrays.
        card
            The number of values to keep in each tensor.
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
            Alternate output container in which to place the result.
            The default is None.

        Returns
        -------
        ret
            container including the sparsified tensor computed element-wise

        Examples
        --------
        >>> x = startai.Container(
                a=startai.reshape(startai.arange(100), (10, 10)),
                b=startai.reshape(startai.arange(100), (10, 10)),
            )
        >>> startai.Container.static_sparsify_tensor(x, 10)
            {
                a: (<class startai.data_classes.array.array.Array> shape=[10, 10]),
                b: (<class startai.data_classes.array.array.Array> shape=[10, 10])
            }
        """
        return ContainerBase.cont_multi_map_in_function(
            "sparsify_tensor",
            x,
            card,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def sparsify_tensor(
        self: Union[startai.Container, startai.Array, startai.NativeArray],
        card: Union[int, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.sparsify_tensor.

        This method simply wraps the function, and so the docstring for
        startai.sparsify_tensor also applies to this method with minimal
        changes.
        """
        return self.static_sparsify_tensor(
            self,
            card,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_erfc(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.erfc. This method simply
        wraps the function, and so the docstring for startai.erfc also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            The container whose array contains real or complex valued argument.
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
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container with values of the complementary error function.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., 2.]), b=startai.array([-3., -4.]))
        >>> startai.Container.static_erfc(x)
        {
            a: startai.array([0.15729921, 0.00467773]),
            b: startai.array([1.99997795, 2.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "erfc",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def erfc(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.erfc. This method
        simply wraps the function, and so the docstring for startai.erfc also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container whose array contains real or complex valued argument.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container with values of the complementary error function.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([-1., -2., -3.]))
        >>> x.erfc()
        {
            a: startai.array([1.57299206e-01, 4.67773480e-03, 2.20904985e-05]),
            b: startai.array([1.84270084, 1.99532223, 1.99997795])
        }
        """
        return self.static_erfc(self, out=out)

    @staticmethod
    def static_erfinv(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.erfinv. This method
        simply wraps the function, and so the docstring for startai.erfinv also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            The container whose array contains real or complex valued argument.
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
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container with values of the inverse error function.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., 2.]), b=startai.array([-3., -4.]))
        >>> startai.Container.static_erfinv(x)
        {
            a: startai.array([0.15729921, 0.00467773]),
            b: startai.array([1.99997795, 2.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "erfinv",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def erfinv(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.erfinv. This method
        simply wraps the function, and so the docstring for startai.erfinv also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container whose array contains real or complex valued argument.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container with values of the inverse error function.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([-1., -2., -3.]))
        >>> x.erfinv()
        {
            a: startai.array([1.57299206e-01, 4.67773480e-03, 2.20904985e-05]),
            b: startai.array([1.84270084, 1.99532223, 1.99997795])
        }
        """
        return self.static_erfinv(self, out=out)
