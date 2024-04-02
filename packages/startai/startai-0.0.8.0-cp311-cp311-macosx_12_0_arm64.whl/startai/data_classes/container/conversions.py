"""Startai wrapping functions for conversions.

Collection of Startai functions for wrapping functions to accept and return
startai.Array instances.
"""

# global
from typing import Union, Dict, Optional, List

# local
import startai
from startai.data_classes.container.base import ContainerBase


class _ContainerWithConversions(ContainerBase):
    @staticmethod
    def _static_to_native(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        nested: Union[bool, startai.Container] = False,
        include_derived: Optional[Union[Dict[str, bool], startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.to_native.

        This method simply wraps the function, and so the docstring for startai.to_native
        also applies to this method with minimal changes.

        Parameters
        ----------
        x
            The input to be converted.
        nested
            Whether to apply the conversion on arguments in a nested manner. If so, all
            dicts, lists and tuples will be traversed to their lowest leaves in search
            of startai.Array instances. Default is ``False``.
        include_derived
            Whether to also recursive for classes derived from tuple, list and dict.
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
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container object with all sub-arrays converted to their native format.
        """
        return ContainerBase.cont_multi_map_in_function(
            "to_native",
            x,
            nested=nested,
            include_derived=include_derived,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def to_native(
        self: startai.Container,
        nested: Union[bool, startai.Container] = False,
        include_derived: Optional[Union[Dict[str, bool], startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.to_native.

        This method simply wraps the function, and so the docstring for startai.to_native
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input to be converted.
        nested
            Whether to apply the conversion on arguments in a nested manner. If so, all
            dicts, lists and tuples will be traversed to their lowest leaves in search
            of startai.Array instances. Default is ``False``.
        include_derived
            Whether to also recursive for classes derived from tuple, list and dict.
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
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container object with all sub-arrays converted to their native format.
        """
        return self._static_to_native(
            self,
            nested,
            include_derived,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
            out=out,
        )

    @staticmethod
    def _static_to_startai(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        nested: Union[bool, startai.Container] = False,
        include_derived: Optional[Union[Dict[str, bool], startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.to_startai.

        This method simply wraps the function, and so the docstring for startai.to_startai also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            The input to be converted.
        nested
            Whether to apply the conversion on arguments in a nested manner. If so, all
            dicts, lists and tuples will be traversed to their lowest leaves in search
            of startai.Array instances. Default is ``False``.
        include_derived
            Whether to also recursive for classes derived from tuple, list and dict.
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
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container object with all native sub-arrays converted to their startai.Array
            instances.
        """
        return ContainerBase.cont_multi_map_in_function(
            "to_startai",
            x,
            nested=nested,
            include_derived=include_derived,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def to_startai(
        self: startai.Container,
        nested: Union[bool, startai.Container] = False,
        include_derived: Optional[Union[Dict[str, bool], startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.to_startai.

        This method simply wraps the function, and so the docstring for startai.to_startai also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input to be converted.
        nested
            Whether to apply the conversion on arguments in a nested manner. If so,
            all dicts, lists and tuples will be traversed to their lowest leaves in
            search of startai.Array instances. Default is ``False``.
        include_derived
            Whether to also recursive for classes derived from tuple, list and dict.
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
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container object with all native sub-arrays converted to their startai.Array
            instances.
        """
        return self._static_to_startai(
            self,
            nested,
            include_derived,
            key_chains,
            to_apply,
            prune_unapplied,
            map_sequences,
            out=out,
        )
