# global
from numbers import Number
from typing import Optional, Union, List, Dict

# local
import startai
from startai.data_classes.container.base import ContainerBase


# noinspection PyMissingConstructor
class _ContainerWithSearching(ContainerBase):
    @staticmethod
    def _static_argmax(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        select_last_index: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.argmax. This method
        simply wraps the function, and so the docstring for startai.argmax also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input array or container. Should have a numeric data type.
        axis
            axis along which to search. If None, the function must return the index of
            the maximum value of the flattened array. Default: ``None``.
        keepdims
            If this is set to True, the axes which are reduced are left in the result as
            dimensions with size one. With this option, the result will broadcast
            correctly against the array.
        dtype
             Optional data type of the output array.
        out
            If provided, the result will be inserted into this array. It should be of
            the appropriate shape and dtype.

        Returns
        -------
        ret
            a container containing the indices of the maximum values across the
            specified axis.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[4., 0., -1.], [2., -3., 6]]),\
        ...                   b=startai.array([[1., 2., 3.], [1., 1., 1.]])
        >>> y = startai.Container.static_argmax(x, axis=1, keepdims=True)
        >>> print(y)
        {
            a: startai.array([[0],
                          [2]]),
            b: startai.array([[2],
                          [0]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "argmax",
            x,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            select_last_index=select_last_index,
            out=out,
        )

    def argmax(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        select_last_index: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.argmax. This method
        simply wraps the function, and so the docstring for startai.argmax also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a numeric data type.
        axis
            axis along which to search. If None, the function must return the index of
            the maximum value of the flattened array. Default: ``None``.
        keepdims
            If this is set to True, the axes which are reduced are left in the result as
            dimensions with size one. With this option, the result will broadcast
            correctly against the array.
        dtype
            Optional output dtype of the container.
        out
            If provided, the result will be inserted into this array. It should be of
            the appropriate shape and dtype.

        Returns
        -------
        ret
            a container containing the indices of the maximum values across the
            specified axis.

        Examples
        --------
        >>> a = startai.array([[4., 0., -1.], [2., -3., 6]])
        >>> b = startai.array([[1., 2., 3.], [1., 1., 1.]])
        >>> x = startai.Container(a=a, b=b)
        >>> y = x.argmax(axis=1, keepdims=True)
        >>> print(y)
        {
            a: startai.array([[0],
                          [2]]),
            b: startai.array([[2],
                          [0]])
        }
        """
        return self._static_argmax(
            self,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            select_last_index=select_last_index,
            out=out,
        )

    @staticmethod
    def _static_argmin(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.int32, startai.int64, startai.Container]] = None,
        select_last_index: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.argmin. This method
        simply wraps the function, and so the docstring for startai.argmin also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input array or container. Should have a numeric data type.
        axis
            axis along which to search. If None, the function must return the index of
            the minimum value of the flattened array. Default = None.
        keepdims
            if True, the reduced axes (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the result must be compatible with
            the input array (see Broadcasting). Otherwise, if False, the reduced axes
            (dimensions) must not be included in the result. Default = False.
        dtype
            An optional output_dtype from: int32, int64. Defaults to int64.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the indices of the minimum values across the
            specified axis.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[4., 0., -1.], [2., -3., 6]]),\
        ...                   b=startai.array([[1., 2., 3.], [1., 1., 1.]])
        >>> y = startai.Container.static_argmin(axis=1, keepdims=True)
        >>> print(y)
        {
            a: startai.array([[2],
                          [1]]),
            b: startai.array([[0],
                          [0]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "argmin",
            x,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            select_last_index=select_last_index,
            out=out,
        )

    def argmin(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        keepdims: Union[bool, startai.Container] = False,
        dtype: Optional[Union[startai.Dtype, startai.NativeDtype, startai.Container]] = None,
        select_last_index: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.argmin. This method
        simply wraps the function, and so the docstring for startai.argmin also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a numeric data type.
        axis
            axis along which to search. If None, the function must return the index of
            the minimum value of the flattened array. Default = None.
        keepdims
            if True, the reduced axes (dimensions) must be included in the result as
            singleton dimensions, and, accordingly, the result must be compatible with
            the input array (see Broadcasting). Otherwise, if False, the reduced axes
            (dimensions) must not be included in the result. Default = False.
        dtype
            An optional output_dtype from: int32, int64. Defaults to int64.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the indices of the minimum values across the
            specified axis.

        Examples
        --------
        Using :class:`startai.Container` instance method:

        >>> x = startai.Container(a=startai.array([0., -1., 2.]), b=startai.array([3., 4., 5.]))
        >>> y = x.argmin()
        >>> print(y)
        {
            a: startai.array(1),
            b: startai.array(0)
        }

        >>> x = startai.Container(a=startai.array([[4., 0., -1.], [2., -3., 6]]),
        ...                   b=startai.array([[1., 2., 3.], [1., 1., 1.]]))
        >>> y = x.argmin(axis=1, keepdims=True)
        >>> print(y)
        {
            a: startai.array([[2],
                          [1]]),
            b: startai.array([[0],
                          [0]])
        }
        """
        return self._static_argmin(
            self,
            axis=axis,
            keepdims=keepdims,
            dtype=dtype,
            select_last_index=select_last_index,
            out=out,
        )

    @staticmethod
    def _static_nonzero(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        as_tuple: Union[bool, startai.Container] = True,
        size: Optional[Union[int, startai.Container]] = None,
        fill_value: Union[Number, startai.Container] = 0,
    ) -> startai.Container:
        """startai.Container static method variant of startai.nonzero. This method
        simply wraps the function, and so the docstring for startai.nonzero also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input array or container. Should have a numeric data type.
        as_tuple
            if True, the output is returned as a tuple of indices, one for each
            dimension of the input, containing the indices of the true elements in that
            dimension. If False, the coordinates are returned in a (N, ndim) array,
            where N is the number of true elements. Default = True.
        size
            if specified, the function will return an array of shape (size, ndim).
            If the number of non-zero elements is fewer than size, the remaining
            elements will be filled with fill_value. Default = None.
        fill_value
            when size is specified and there are fewer than size number of elements,
            the remaining elements in the output array will be filled with fill_value.
            Default = 0.

        Returns
        -------
        ret
            a container containing the indices of the nonzero values.
        """
        return ContainerBase.cont_multi_map_in_function(
            "nonzero", x, as_tuple=as_tuple, size=size, fill_value=fill_value
        )

    def nonzero(
        self: startai.Container,
        /,
        *,
        as_tuple: Union[bool, startai.Container] = True,
        size: Optional[Union[int, startai.Container]] = None,
        fill_value: Union[Number, startai.Container] = 0,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.nonzero. This method
        simply wraps the function, and so the docstring for startai.nonzero also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a numeric data type.
        as_tuple
            if True, the output is returned as a tuple of indices, one for each
            dimension of the input, containing the indices of the true elements in that
            dimension. If False, the coordinates are returned in a (N, ndim) array,
            where N is the number of true elements. Default = True.
        size
            if specified, the function will return an array of shape (size, ndim).
            If the number of non-zero elements is fewer than size, the remaining
            elements will be filled with fill_value. Default = None.
        fill_value
            when size is specified and there are fewer than size number of elements,
            the remaining elements in the output array will be filled with fill_value.
            Default = 0.

        Returns
        -------
        ret
            a container containing the indices of the nonzero values.
        """
        return self._static_nonzero(
            self, as_tuple=as_tuple, size=size, fill_value=fill_value
        )

    @staticmethod
    def _static_where(
        condition: Union[startai.Container, startai.Array, startai.NativeArray],
        x1: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.where. This method simply
        wraps the function, and so the docstring for startai.where also applies to
        this method with minimal changes.

        Parameters
        ----------
        condition
            input array or container. Should have a boolean data type.
        x1
            input array or container. Should have a numeric data type.
        x2
            input array or container. Should have a numeric data type.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the values of x1 where condition is True, and x2
            where condition is False.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([3, 1, 5]), b=startai.array([2, 4, 6]))
        >>> x2 = startai.Container(a=startai.array([0, 7, 2]), b=startai.array([3, 8, 5]))
        >>> res = startai.Container.static_where((x1.a > x2.a), x1, x2)
        >>> print(res)
        {
            a: startai.array([3, 7, 5]),
            b: startai.array([2, 8, 6])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "where", condition, x1, x2, out=out
        )

    def where(
        self: startai.Container,
        x1: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.where. This method
        simply wraps the function, and so the docstring for startai.where also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a boolean data type.
        x1
            input array or container. Should have a numeric data type.
        x2
            input array or container. Should have a numeric data type.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the values of x1 where condition is True, and x2
            where condition is False.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([3, 1, 5]), b=startai.array([2, 4, 6]))
        >>> x2 = startai.Container(a=startai.array([0, 7, 2]), b=startai.array([3, 8, 5]))
        >>> res = x1.where((x1.a > x2.a), x2)
        >>> print(res)
        {
            a: startai.array([1, 0, 1]),
            b: startai.array([1, 0, 1])
        }
        """
        return self._static_where(self, x1, x2, out=out)

    # Extra #
    # ----- #

    @staticmethod
    def _static_argwhere(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.argwhere. This method
        simply wraps the function, and so the docstring for startai.argwhere also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Boolean array, for which indices are desired.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains will
            be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied. Default
            is False.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.

        Returns
        -------
        ret
            Indices for where the boolean array is True.

        Examples
        --------
        Using :class:`startai.Container` instance method

        >>> x = startai.Container(a=startai.array([1, 2]), b=startai.array([3, 4]))
        >>> res = startai.Container.static_argwhere(x)
        >>> print(res)
        {
            a: startai.array([[0], [1]]),
            b: startai.array([[0], [1]])
        }

        >>> x = startai.Container(a=startai.array([1, 0]), b=startai.array([3, 4]))
        >>> res = startai.Container.static_argwhere(x)
        >>> print(res)
        {
            a: startai.array([[0]]),
            b: startai.array([[0], [1]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "argwhere",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def argwhere(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ):
        """startai.Container instance method variant of startai.argwhere. This method
        simply wraps the function, and so the docstring for startai.argwhere also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Boolean array, for which indices are desired.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains will
            be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied. Default
            is False.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.

        Returns
        -------
        ret
            Indices for where the boolean array is True.

        Examples
        --------
        Using :class:`startai.Container` instance method

        >>> x = startai.Container(a=startai.array([1, 2]), b=startai.array([3, 4]))
        >>> res = x.argwhere()
        >>> print(res)
        {
            a: startai.array([[0], [1]]),
            b: startai.array([[0], [1]])
        }

        >>> x = startai.Container(a=startai.array([1, 0]), b=startai.array([3, 4]))
        >>> res = x.argwhere()
        >>> print(res)
        {
            a: startai.array([[0]]),
            b: startai.array([[0], [1]])
        }
        """
        return self._static_argwhere(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )
