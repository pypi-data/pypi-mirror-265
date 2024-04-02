# global
from typing import Optional, Union, List, Dict, Callable, Sequence

# local
from startai.data_classes.container.base import ContainerBase
import startai


class _ContainerWithGeneralExperimental(ContainerBase):
    @staticmethod
    def _static_reduce(
        operand: Union[startai.Container, startai.Array, startai.NativeArray],
        init_value: Union[int, float, startai.Container],
        computation: Union[Callable, startai.Container],
        /,
        *,
        axes: Union[int, Sequence[int], startai.Container] = 0,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.reduce. This method
        simply wraps the function, and so the docstring for startai.reduce also
        applies to this method with minimal changes.

        Parameters
        ----------
        operand
            The array to act on.
        init_value
            The value with which to start the reduction.
        computation
            The reduction function.
        axes
            The dimensions along which the reduction is performed.
        keepdims
            If this is set to True, the axes which are reduced are left in the result as
            dimensions with size one.
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

        Returns
        -------
        ret
            The reduced array.

        Examples
        --------
        >>> x = startai.Container(
        >>>     a=startai.array([[1, 2, 3], [4, 5, 6]]),
        >>>     b=startai.native_array([[7, 8, 9], [10, 5, 1]])
        >>> )
        >>> y = startai.Container.static_reduce(x, 0, startai.add)
        >>> print(y)
        {
            a: startai.array([6, 15]),
            b: startai.array([24, 16])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "reduce",
            operand,
            init_value,
            computation,
            axes=axes,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def reduce(
        self: startai.Container,
        init_value: Union[int, float, startai.Container],
        computation: Union[Callable, startai.Container],
        /,
        *,
        axes: Union[int, Sequence[int], startai.Container] = 0,
        keepdims: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.reduce. This method
        simply wraps the function, and so the docstring for startai.reduce also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The array to act on.
        init_value
            The value with which to start the reduction.
        computation
            The reduction function.
        axes
            The dimensions along which the reduction is performed.
        keepdims
            If this is set to True, the axes which are reduced are left in the result as
            dimensions with size one.
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

        Returns
        -------
        ret
            The reduced array.

        Examples
        --------
        >>> x = startai.Container(
        ...     a=startai.array([[1, 2, 3], [4, 5, 6]]),
        ...     b=startai.native_array([[7, 8, 9], [10, 5, 1]]))
        >>> y = x.reduce(0, startai.add)
        >>> print(y)
        {
            a: startai.array([5, 7, 9]),
            b: startai.array([17, 13, 10])
        }
        """
        return self._static_reduce(
            self,
            init_value,
            computation,
            axes=axes,
            keepdims=keepdims,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )
