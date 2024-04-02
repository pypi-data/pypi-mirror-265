# global
from typing import Dict, List, Optional, Union

# local
from startai.data_classes.container.base import ContainerBase
import startai


class _ContainerWithSet(ContainerBase):
    @staticmethod
    def _static_unique_all(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        by_value: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.unique_all. This method
        simply wraps the function, and so the docstring for startai.unique_all also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        axis
            the axis to apply unique on. If None, the unique elements of the flattened
            ``x`` are returned.
        by_value
            If False, the unique elements will be sorted in the same order that they
            occur in ''x''. Otherwise, they will be sorted by value.
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
            A container of namedtuples ``(values, indices, inverse_indices,
            counts)``. The details can be found in the docstring
            for startai.unique_all.


        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 1., 3. , 2. , 1. , 0.]),
        ...                   b=startai.array([1,2,1,3,4,1,3]))
        >>> y = startai.Container.static_unique_all(x)
        >>> print(y)
        {
            a: [
                values = startai.array([0., 1., 2., 3.]),
                indices = startai.array([0, 1, 3, 2]),
                inverse_indices = startai.array([0, 1, 3, 2, 1, 0]),
                counts = startai.array([2, 2, 1, 1])
            ],
            b: [
                values = startai.array([1, 2, 3, 4]),
                indices = startai.array([0, 1, 3, 4]),
                inverse_indices = startai.array([0, 1, 0, 2, 3, 0, 2]),
                counts = startai.array([3, 1, 2, 1])
            ]
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "unique_all",
            x,
            axis=axis,
            by_value=by_value,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def unique_all(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        by_value: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.unique_all. This method
        simply wraps the function, and so the docstring for startai.unique_all also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        axis
            the axis to apply unique on. If None, the unique elements of the flattened
            ``x`` are returned.
        by_value
            If False, the unique elements will be sorted in the same order that they
            occur in ''x''. Otherwise, they will be sorted by value.
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
            A container of namedtuples ``(values, indices, inverse_indices,
            counts)``. The details of each entry can be found in the docstring
            for startai.unique_all.


        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 1., 3. , 2. , 1. , 0.]),
        ...                   b=startai.array([1,2,1,3,4,1,3]))
        >>> y = x.unique_all()
        >>> print(y)
        [{
            a: startai.array([0., 1., 2., 3.]),
            b: startai.array([1, 2, 3, 4])
        }, {
            a: startai.array([0, 1, 3, 2]),
            b: startai.array([0, 1, 3, 4])
        }, {
            a: startai.array([0, 1, 3, 2, 1, 0]),
            b: startai.array([0, 1, 0, 2, 3, 0, 2])
        }, {
            a: startai.array([2, 2, 1, 1]),
            b: startai.array([3, 1, 2, 1])
        }]
        """
        return self._static_unique_all(
            self,
            axis=axis,
            by_value=by_value,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def _static_unique_counts(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.unique_counts. This
        method simply wraps the function, and so the docstring for
        startai.unique_counts also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. If ``x`` has more than one dimension, the function must
            flatten ``x`` and return the unique elements of the flattened array.
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
            a namedtuple ``(values, counts)`` whose

            - first element must have the field name ``values`` and must be an
            array containing the unique elements of ``x``.
            The array must have the same data type as ``x``.
            - second element must have the field name ``counts`` and must be an array
            containing the number of times each unique element occurs in ``x``.
            The returned array must have same shape as ``values`` and must
            have the default array index data type.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 1., 3. , 2. , 1. , 0.]),
        ...                   b=startai.array([1,2,1,3,4,1,3]))
        >>> y = startai.Container.static_unique_counts(x)
        >>> print(y)
        {
            a:[values=startai.array([0.,1.,2.,3.]),counts=startai.array([2,2,1,1])],
            b:[values=startai.array([1,2,3,4]),counts=startai.array([3,1,2,1])]
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "unique_counts",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def unique_counts(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.unique_counts. This
        method simply wraps the function, and so the docstring for
        startai.unique_counts also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. If ``x`` has more than one dimension, the function must
            flatten ``x`` and return the unique elements of the flattened array.
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
            a namedtuple ``(values, counts)`` whose

            - first element must have the field name ``values`` and must be an
            array containing the unique elements of ``x``.
            The array must have the same data type as ``x``.
            - second element must have the field name ``counts`` and must be an array
            containing the number of times each unique element occurs in ``x``.
            The returned array must have same shape as ``values`` and must
            have the default array index data type.

        Examples
        --------
        With :class:`startai.Container` instance method:

        >>> x = startai.Container(a=startai.array([0., 1., 3. , 2. , 1. , 0.]),
        ...                   b=startai.array([1,2,1,3,4,1,3]))
        >>> y = x.unique_counts()
        >>> print(y)
        [{
            a: startai.array([0., 1., 2., 3.]),
            b: startai.array([1, 2, 3, 4])
        }, {
            a: startai.array([2, 2, 1, 1]),
            b: startai.array([3, 1, 2, 1])
        }]
        """
        return self._static_unique_counts(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def _static_unique_values(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        return ContainerBase.cont_multi_map_in_function(
            "unique_values",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def unique_values(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.unique_values. This
        method simply wraps the function and applies it on the container.

        Parameters
        ----------
        self : startai.Container
            input container
        key_chains : list or dict, optional
            The key-chains to apply or not apply the method to. Default is `None`.
        to_apply : bool, optional
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is `True`.
        prune_unapplied : bool, optional
            Whether to prune key_chains for which the function was not applied.
            Default is `False`.
        map_sequences : bool, optional
            Whether to also map method to sequences (lists, tuples).
            Default is `False`.
        out : startai.Container, optional
            The container to return the results in. Default is `None`.

        Returns
        -------
        startai.Container
            The result container with the unique values for each input key-chain.

        Raises
        ------
        TypeError
            If the input container is not an instance of startai.Container.
        ValueError
            If the key_chains parameter is not None, and it is not a
            list or a dictionary.

        Example
        -------
        >>> x = startai.Container(a=[1, 2, 3], b=[2, 2, 3], c=[4, 4, 4])
        >>> y = x.unique_values()
        >>> print(y)
        {
            a: startai.array([1, 2, 3]),
            b: startai.array([2, 3]),
            c: startai.array([4])
        }

        >>> x = startai.Container(a=[1, 2, 3], b=[2, 2, 3], c=[4, 4, 4])
        >>> y = x.unique_values(key_chains=["a", "b"])
        >>> print(y)
        {
            a: startai.array([1, 2, 3]),
            b: startai.array([2, 3]),
            c: [
                4,
                4,
                4
            ]
        }
        """
        return self._static_unique_values(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_unique_inverse(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.unique_inverse. This
        method simply wraps the function, and so the docstring for
        startai.unique_inverse also applies to this method with minimal changes.

        Parameters
        ----------
        x
             input container. If ``x`` has more than one dimension, the function must
             flatten ``x`` and return the unique elements of the flattened array.
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

             a namedtuple ``(values, inverse_indices)`` whose

             - first element must have the field name ``values`` and must be an array
             containing the unique elements of ``x``. The array must have the same data
             type as ``x``.
             - second element must have the field name ``inverse_indices`` and
              must be an array containing the indices of ``values`` that
              reconstruct ``x``. The array must have the same shape as ``x`` and
              must have the default array index data type.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([4.,8.,3.,5.,9.,4.]),
        ...                   b=startai.array([7,6,4,5,6,3,2]))
        >>> y = startai.Container.static_unique_inverse(x)
        >>> print(y)
        {
            a:[values=startai.array([3.,4.,5.,8.,9.]),inverse_indices=startai.array([1,3,0,2,4,1])],
            b:[values=startai.array([2,3,4,5,6,7]),inverse_indices=startai.array([5,4,2,3,4,1,0])]
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "unique_inverse",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def unique_inverse(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.unique_inverse. This
        method simply wraps the function, and so the docstring for
        startai.unique_inverse also applies to this method with minimal changes.

        Parameters
        ----------
        self
             input container. If ``x`` has more than one dimension, the function must
             flatten ``x`` and return the unique elements of the flattened array.
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

             a namedtuple ``(values, inverse_indices)`` whose

             - first element must have the field name ``values`` and must be an array
             containing the unique elements of ``x``. The array must have the same data
             type as ``x``.
             - second element must have the field name ``inverse_indices`` and
              must be an array containing the indices of ``values`` that
              reconstruct ``x``. The array must have the same shape as ``x`` and
              must have the default array index data type.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([4.,8.,3.,5.,9.,4.]),
        ...                   b=startai.array([7,6,4,5,6,3,2]))
        >>> y = x.unique_inverse()
        >>> print(y)
        [{
            a: startai.array([3., 4., 5., 8., 9.]),
            b: startai.array([2, 3, 4, 5, 6, 7])
        }, {
            a: startai.array([1, 3, 0, 2, 4, 1]),
            b: startai.array([5, 4, 2, 3, 4, 1, 0])
        }]

        >>> x = startai.Container(a=startai.array([1., 4., 3. , 5. , 3. , 7.]),
        ...                   b=startai.array([3, 2, 6, 3, 7, 4, 9]))
        >>> y = startai.startai.unique_inverse(x)
        >>> print(y)
        [{
            a: startai.array([1., 3., 4., 5., 7.]),
            b: startai.array([2, 3, 4, 6, 7, 9])
        }, {
            a: startai.array([0, 2, 1, 3, 1, 4]),
            b: startai.array([1, 0, 3, 1, 4, 2, 5])
        }]
        """
        return self._static_unique_inverse(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )
