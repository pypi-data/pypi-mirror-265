# global
from typing import Optional, Union, Dict, List

# local
import startai
from startai.data_classes.container.base import ContainerBase


class _ContainerWithUtilityExperimental(ContainerBase):
    @staticmethod
    def static_optional_get_element(
        x: Optional[Union[startai.Array, startai.Container]] = None,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.optional_get_element.
        This method simply wraps the function, and so the docstring for
        startai.optional_get_element also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            container with array inputs.
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
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container with arrays flattened at leaves.
        """
        return ContainerBase.cont_multi_map_in_function(
            "optional_get_element",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def optional_get_element(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.optional_get_element.
        This method simply wraps the function, and so the docstring for
        startai.optional_get_element also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            Input container
        out
            Optional output container, for writing the result to.

        Returns
        -------
        ret
            Output container.
        """
        return self.static_optional_get_element(self, out=out)
