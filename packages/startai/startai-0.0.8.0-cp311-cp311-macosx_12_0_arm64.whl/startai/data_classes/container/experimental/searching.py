# global
from typing import Optional, Union, List, Dict, Tuple

# local
import startai
from startai.data_classes.container.base import ContainerBase


class _ContainerWithSearchingExperimental(ContainerBase):
    @staticmethod
    def static_unravel_index(
        indices: startai.Container,
        shape: Union[Tuple[int], startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.unravel_index. This
        method simply wraps the function, and so the docstring for
        startai.unravel_index also applies to this method with minimal changes.

        Parameters
        ----------
        indices
            Input container including arrays.
        shape
            The shape of the array to use for unraveling indices.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Container with tuples that have arrays with the same shape as
            the arrays in the input container.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> indices = startai.Container(a=startai.array([22, 41, 37])), b=startai.array([30, 2]))
        >>> startai.Container.static_unravel_index(indices, (7,6))
        {
            a: (startai.array([3, 6, 6]), startai.array([4, 5, 1]))
            b: (startai.array([5, 0], startai.array([0, 2])))
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "unravel_index",
            indices,
            shape,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def unravel_index(
        self: startai.Container,
        shape: Union[Tuple[int], startai.Container],
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.unravel_index. This
        method simply wraps the function, and so the docstring for
        startai.unravel_index also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container including arrays.
        shape
            The shape of the array to use for unraveling indices.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Container with tuples that have arrays with the same shape as
            the arrays in the input container.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> indices = startai.Container(a=startai.array([22, 41, 37])), b=startai.array([30, 2]))
        >>> indices.unravel_index((7, 6))
        {
            a: (startai.array([3, 6, 6]), startai.array([4, 5, 1]))
            b: (startai.array([5, 0], startai.array([0, 2])))
        }
        """
        return self.static_unravel_index(self, shape, out=out)
