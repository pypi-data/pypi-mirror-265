# global
from typing import Optional, List, Union, Dict, Literal

# local
from startai.data_classes.container.base import ContainerBase
import startai

# ToDo: implement all methods here as public instance methods


# noinspection PyMissingConstructor
class _ContainerWithSorting(ContainerBase):
    @staticmethod
    def _static_argsort(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Union[int, startai.Container] = -1,
        descending: Union[bool, startai.Container] = False,
        stable: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.argsort. This method
        simply wraps the function, and so the docstring for startai.argsort also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input array or container. Should have a numeric data type.
        axis
            axis along which to sort. If set to ``-1``, the function must sort
            along the last axis. Default: ``-1``.
        descending
            sort order. If ``True``, the returned indices sort
            ``x`` in descending order (by value). If ``False``,
            the returned indices sort ``x`` in ascending order
            (by value). Default: ``False``.
        stable
            sort stability. If ``True``, the returned indices must maintain
            the relative order of ``x`` values which compare as equal.
            If ``False``, the returned indices may or may not maintain
            the relative order of ``x`` values which compare as equal (i.e., the
            relative order of ``x`` values which compare as equal
            is implementation-dependent). Default: ``True``.
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
            a container containing the index values of sorted
            array. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([7, 2, 1]),
        ...                   b=startai.array([3, 2]))
        >>> y = startai.Container.static_argsort(x, axis=-1, descending=True, stable=False)
        >>> print(y)
        {
            a: startai.array([0, 1, 2]),
            b: startai.array([0, 1])
        }

        >>> x = startai.Container(a=startai.array([7, 2, 1]),
        ...                   b=startai.array([[3, 2], [7, 0.2]]))
        >>> y = startai.Container.static_argsort(x, axis=-1, descending=True, stable=False)
        >>> print(y)
        {
            a: startai.array([0, 1, 2]),
            b: startai.array([[0, 1]],[0, 1]])
        }

        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([2, 5, 1]),
        ...                   b=startai.array([1, 5], [.2,.1]))
        >>> y = startai.Container.static_argsort(x,axis=-1, descending=True, stable=False)
        >>> print(y)
        {
            a: startai.array([2, 0, 1]),
            b: startai.array([[1, 0],[0,1]])
        }

        >>> x = startai.Container(a=startai.native_array([2, 5, 1]),
        ...                   b=startai.array([1, 5], [.2,.1]))
        >>> y = startai.Container.static_argsort(x, axis=-1, descending=True, stable=False)
        >>> print(y)
        {
            a: startai.array([2, 0, 1]),
            b: startai.array([[1, 0],[0,1]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "argsort",
            x,
            axis=axis,
            descending=descending,
            stable=stable,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def argsort(
        self: startai.Container,
        /,
        *,
        axis: Union[int, startai.Container] = -1,
        descending: Union[bool, startai.Container] = False,
        stable: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.argsort. This method
        simply wraps the function, and so the docstring for startai.argsort also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a numeric data type.
        axis
            axis along which to sort. If set to ``-1``, the function
            must sort along the last axis. Default: ``-1``.
        descending
            sort order. If ``True``, the returned indices sort ``x``
            in descending order (by value). If ``False``, the
            returned indices sort ``x`` in ascending order (by value).
            Default: ``False``.
        stable
            sort stability. If ``True``, the returned indices must
            maintain the relative order of ``x`` values which compare
            as equal. If ``False``, the returned indices may or may not
            maintain the relative order of ``x`` values which compare
            as equal (i.e., the relative order of ``x`` values which
            compare as equal is implementation-dependent).
            Default: ``True``.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains,
            otherwise key_chains will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the index values of sorted array.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([7, 2, 1]),
        ...                   b=startai.array([3, 2]))
        >>> y = x.argsort(axis=-1, descending=True, stable=False)
        >>> print(y)
        {
            a: startai.array([0, 1, 2]),
            b: startai.array([0, 1])
        }
        """
        return self._static_argsort(
            self,
            axis=axis,
            descending=descending,
            stable=stable,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_sort(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Union[int, startai.Container] = -1,
        descending: Union[bool, startai.Container] = False,
        stable: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.sort. This method simply
        wraps the function, and so the docstring for startai.sort also applies to
        this method with minimal changes.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([5, 9, 0.2]),
        ...                   b=startai.array([[8, 1], [5, 0.8]]))
        >>> y = startai.Container.static_sort(x)
        >>> print(y)
        {
            a: startai.array([0.2, 5., 9.]),
            b: startai.array([[1., 8.], [0.8, 5.]])
        }

        >>> x = startai.Container(a=startai.array([8, 0.5, 6]),
        ...                   b=startai.array([[9, 0.7], [0.4, 0]]))
        >>> y = startai.Container.static_sort(x)
        >>> print(y)
        {
            a: startai.array([0.5, 6., 8.]),
            b: startai.array([[0.7, 9.], [0., 0.4]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "sort",
            x,
            axis=axis,
            descending=descending,
            stable=stable,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def sort(
        self: startai.Container,
        /,
        *,
        axis: Union[int, startai.Container] = -1,
        descending: Union[bool, startai.Container] = False,
        stable: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.sort. This method
        simply wraps the function, and so the docstring for startai.sort also
        applies to this method with minimal changes.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([5, 9, 0.2]),
        ...                   b=startai.array([8, 1]))
        >>> y = x.sort()
        >>> print(y)
        {
            a: startai.array([0.2, 5., 9.]),
            b: startai.array([1, 8])
        }

        >>> x = startai.Container(a=startai.array([5, 9, 0.2]),
        ...                   b=startai.array([[8, 1], [5, 0.8]]))
        >>> y = x.sort()
        >>> print(y)
        {
            a: startai.array([0.2, 5., 9.]),
            b: startai.array([[1., 8.], [0.8, 5.]])
        }

        >>> x = startai.Container(a=startai.array([8, 0.5, 6]),
        ...                   b=startai.array([[9, 0.7], [0.4, 0]]))
        >>> y = startai.sort(x)
        >>> print(y)
        {
            a: startai.array([0.5, 6., 8.]),
            b: startai.array([[0.7, 9.],[0., 0.4]])
        }

        >>> x = startai.Container(a=startai.native_array([8, 0.5, 6]),
        ...                   b=startai.array([[9, 0.7], [0.4, 0]]))
        >>> y = startai.sort(x)
        >>> print(y)
        {
            a: startai.array([0.5, 6., 8.]),
            b: startai.array([[0.7, 9.],[0., 0.4]])
        }
        """
        return self._static_sort(
            self,
            axis=axis,
            descending=descending,
            stable=stable,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_msort(
        a: Union[startai.Array, startai.NativeArray, startai.Container, list, tuple],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.msort. This method simply
        wraps the function, and so the docstring for startai.msort also applies to
        this method with minimal changes.

        Parameters
        ----------
        a
            array-like or container input.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            a container containing sorted input arrays.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> a = startai.Container(x = startai.asarray([[8, 9, 6],[6, 2, 6]]),
        ...                   y = startai.asarray([[7, 2],[3, 4]])
        >>> startai.Container.static_lexsort(a)
        {
            x: startai.array(
                [[6, 2, 6],
                 [8, 9, 6]]
                ),
            y: startai.array(
                [[3, 4],
                 [7, 2]]
                )
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "msort",
            a,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def msort(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.msort. This method
        simply wraps the function, and so the docstring for startai.msort also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container with array-like inputs to sort.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            a container containing the sorted input arrays.

        Examples
        --------
        >>> a = startai.Container(x = startai.asarray([[8, 9, 6],[6, 2, 6]]),
        ...                   y = startai.asarray([[7, 2],[3, 4]])
        >>> a.msort()
        {
            x: startai.array(
                [[6, 2, 6],
                 [8, 9, 6]]
                ),
            y: startai.array(
                [[3, 4],
                 [7, 2]]
                )
        }
        """
        return self.static_msort(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_searchsorted(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        v: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        side: Union[str, startai.Container] = "left",
        sorter: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container, List[int]]
        ] = None,
        ret_dtype: Union[startai.Dtype, startai.Container] = startai.int64,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.searchsorted.

        This method simply wraps the function, and so the docstring for
        startai.searchsorted also applies to this method with minimal
        changes.
        """
        return ContainerBase.cont_multi_map_in_function(
            "searchsorted",
            x1,
            v,
            side=side,
            sorter=sorter,
            ret_dtype=ret_dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def searchsorted(
        self: startai.Container,
        v: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        side: Union[Literal["left", "right"], startai.Container] = "left",
        sorter: Optional[
            Union[startai.Array, startai.NativeArray, List[int], startai.Container]
        ] = None,
        ret_dtype: Union[startai.Dtype, startai.NativeDtype, startai.Container] = startai.int64,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.searchsorted.

        This method simply wraps the function, and so the docstring for
        startai.searchsorted also applies to this method with minimal
        changes.
        """
        return self._static_searchsorted(
            self,
            v,
            side=side,
            sorter=sorter,
            ret_dtype=ret_dtype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )
