# global
from typing import Optional, Union, Dict, Sequence

# local
import startai
from startai.data_classes.container.base import ContainerBase


# noinspection PyMissingConstructor
class _ContainerWithUtility(ContainerBase):
    @staticmethod
    def _static_all(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Optional[Union[int, Sequence[int], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[
            Union[Sequence[str], Dict[str, str], startai.Container]
        ] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.all. This method simply
        wraps the function, and so the docstring for startai.all also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        axis
            axis or axes along which to perform a logical AND reduction. By default, a
            logical AND reduction must be performed over the entire array. If a tuple of
            integers, logical AND reductions must be performed over multiple axes. A
            valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N``
            is the rank(number of dimensions) of ``self``. If an ``axis`` is specified
            as a negative integer, the function must determine the axis along which to
            perform a reduction by counting backward from the last dimension (where
            ``-1`` refers to the last dimension). If provided an invalid ``axis``, the
            function must raise an exception. Default  ``None``.
        keepdims
            If ``True``, the reduced axes (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the result must be compatible with
            the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the
            reduced axes(dimensions) must not be included in the result.
            Default: ``False``.
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
            if a logical AND reduction was performed over the entire array, the returned
            container must be a zero-dimensional array containing the test result;
            otherwise, the returned container must be a non-zero-dimensional array
            containing the test results. The returned container must have a data type of
            ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, 1, 2]), b=startai.array([0, 1, 1]))
        >>> y = startai.Container.static_all(x)
        >>> print(y)
        {
            a: startai.array(False),
            b: startai.array(False)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "all",
            x,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def all(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, Sequence[int], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[
            Union[Sequence[str], Dict[str, str], startai.Container]
        ] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.all. This method simply
        wraps the function, and so the docstring for startai.all also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        axis
            axis or axes along which to perform a logical AND reduction. By default, a
            logical AND reduction must be performed over the entire array. If a tuple of
            integers, logical AND reductions must be performed over multiple axes. A
            valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N``
            is the rank(number of dimensions) of ``self``. If an ``axis`` is specified
            as a negative integer, the function must determine the axis along which to
            perform a reduction by counting backward from the last dimension (where
            ``-1`` refers to the last dimension). If provided an invalid ``axis``, the
            function must raise an exception. Default  ``None``.
        keepdims
            If ``True``, the reduced axes (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the result must be compatible with
            the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the
            reduced axes(dimensions) must not be included in the result.
            Default: ``False``.
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
            if a logical AND reduction was performed over the entire array, the returned
            container must be a zero-dimensional array containing the test result;
            otherwise, the returned container must have non-zero-dimensional arrays
            containing the test results. The returned container must have a data type of
            ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, 1, 2]), b=startai.array([0, 1, 1]))
        >>> y = x.all()
        >>> print(y)
        {
            a: startai.array(False),
            b: startai.array(False)
        }
        """
        return self._static_all(
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
    def _static_any(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Optional[Union[int, Sequence[int], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[
            Union[Sequence[str], Dict[str, str], startai.Container]
        ] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.any. This method simply
        wraps the function, and so the docstring for startai.any also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        axis
            axis or axes along which to perform a logical OR reduction. By default, a
            logical OR reduction must be performed over the entire array. If a tuple of
            integers, logical OR reductions must be performed over multiple axes. A
            valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N``
            is the rank(number of dimensions) of ``self``. If an ``axis`` is specified
            as a negative integer, the function must determine the axis along which to
            perform a reduction by counting backward from the last dimension (where
            ``-1`` refers to the last dimension). If provided an invalid ``axis``, the
            function must raise an exception. Default: ``None``.
        keepdims
            If ``True``, the reduced axes (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the result must be compatible with
            the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the
            reduced axes(dimensions) must not be included in the result.
            Default: ``False``.
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
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            if a logical OR reduction was performed over the entire array, the returned
            container must be a zero-dimensional array containing the test result;
            otherwise, the returned container must have non-zero-dimensional arrays
            containing the test results. The returned container must have a data type of
            ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, 1, 2]), b=startai.array([0, 0, 0]))
        >>> y = startai.Container.static_any(x)
        >>> print(y)
        {
            a: startai.array(True),
            b: startai.array(False)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "any",
            x,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def any(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, Sequence[int], startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[
            Union[Sequence[str], Dict[str, str], startai.Container]
        ] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.any. This method simply
        wraps the function, and so the docstring for startai.any also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        axis
            axis or axes along which to perform a logical OR reduction. By default, a
            logical OR reduction must be performed over the entire array. If a tuple of
            integers, logical OR reductions must be performed over multiple axes. A
            valid ``axis`` must be an integer on the interval ``[-N, N)``, where ``N``
            is the rank(number of dimensions) of ``self``. If an ``axis`` is specified
            as a negative integer, the function must determine the axis along which to
            perform a reduction by counting backward from the last dimension (where
            ``-1`` refers to the last dimension). If provided an invalid ``axis``, the
            function must raise an exception. Default: ``None``.
        keepdims
            If ``True``, the reduced axes (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the result must be compatible with
            the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the
            reduced axes(dimensions) must not be included in the result.
            Default: ``False``.
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
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            if a logical OR reduction was performed over the entire array, the returned
            container must be a zero-dimensional array containing the test result;
            otherwise, the returned container must have non-zero-dimensional arrays
            containing the test results. The returned container must have a data type of
            ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, 1, 2]), b=startai.array([0, 0, 0]))
        >>> y = x.any()
        >>> print(y)
        {
            a: startai.array(True),
            b: startai.array(False)
        }
        """
        return self._static_any(
            self,
            axis=axis,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )
