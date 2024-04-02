# global
from typing import (
    Optional,
    Union,
    List,
    Dict,
    Sequence,
    Tuple,
    Literal,
    Any,
    Callable,
    Iterable,
)
from numbers import Number

# local
import startai
from startai.data_classes.container.base import ContainerBase


class _ContainerWithManipulationExperimental(ContainerBase):
    @staticmethod
    def static_moveaxis(
        a: Union[startai.Array, startai.NativeArray, startai.Container],
        source: Union[int, Sequence[int], startai.Container],
        destination: Union[int, Sequence[int], startai.Container],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.moveaxis. This method
        simply wraps the function, and so the docstring for startai.moveaxis also
        applies to this method with minimal changes.

        Parameters
        ----------
        a
            The container with the arrays whose axes should be reordered.
        source
            Original positions of the axes to move. These must be unique.
        destination
            Destination positions for each of the original axes.
            These must also be unique.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with moved axes.

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
            "moveaxis",
            a,
            source,
            destination,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def moveaxis(
        self: startai.Container,
        source: Union[int, Sequence[int], startai.Container],
        destination: Union[int, Sequence[int], startai.Container],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.moveaxis. This method
        simply wraps the function, and so the docstring for startai.flatten also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container with the arrays whose axes should be reordered.
        source
            Original positions of the axes to move. These must be unique.
        destination
            Destination positions for each of the original axes.
            These must also be unique.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with moved axes.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container(a=startai.zeros((3, 4, 5)), b=startai.zeros((2,7,6)))
        >>> x.moveaxis(, 0, -1).shape
        {
            a: (4, 5, 3)
            b: (7, 6, 2)
        }
        """
        return self.static_moveaxis(self, source, destination, copy=copy, out=out)

    @staticmethod
    def static_heaviside(
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
        """startai.Container static method variant of startai.heaviside. This method
        simply wraps the function, and so the docstring for startai.heaviside also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input container including the arrays.
        x2
            values to use where the array is zero.
        out
            optional output container array, for writing the result to.

        Returns
        -------
        ret
            output container with element-wise Heaviside step function of each array.

        Examples
        --------
        With :class:`startai.Array` input:
        >>> x1 = startai.Container(a=startai.array([-1.5, 0, 2.0]), b=startai.array([3.0, 5.0])
        >>> x2 = startai.Container(a=0.5, b=[1.0, 2.0])
        >>> startai.Container.static_heaviside(x1, x2)
        {
            a: startai.array([ 0. ,  0.5,  1. ])
            b: startai.array([1.0, 1.0])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "heaviside",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def heaviside(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.heaviside. This method
        simply wraps the function, and so the docstring for startai.heaviside also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container including the arrays.
        x2
            values to use where the array is zero.
        out
            optional output container array, for writing the result to.

        Returns
        -------
        ret
            output container with element-wise Heaviside step function of each array.

        Examples
        --------
        With :class:`startai.Array` input:
        >>> x1 = startai.Container(a=startai.array([-1.5, 0, 2.0]), b=startai.array([3.0, 5.0])
        >>> x2 = startai.Container(a=0.5, b=[1.0, 2.0])
        >>> x1.heaviside(x2)
        {
            a: startai.array([ 0. ,  0.5,  1. ])
            b: startai.array([1.0, 1.0])
        }
        """
        return self.static_heaviside(self, x2, out=out)

    @staticmethod
    def static_flipud(
        m: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.flipud. This method
        simply wraps the function, and so the docstring for startai.flipud also
        applies to this method with minimal changes.

        Parameters
        ----------
        m
            the container with arrays to be flipped.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including arrays corresponding to the input container's array
            with elements order reversed along axis 0.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> m = startai.Container(a=startai.diag([1, 2, 3]), b=startai.arange(4))
        >>> startai.Container.static_flipud(m)
        {
            a: startai.array(
                [[ 0.,  0.,  3.],
                 [ 0.,  2.,  0.],
                 [ 1.,  0.,  0.]]
            )
            b: startai.array([3, 2, 1, 0])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "flipud",
            m,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def flipud(
        self: startai.Container,
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.flipud. This method
        simply wraps the function, and so the docstring for startai.flipud also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            the container with arrays to be flipped.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including arrays corresponding to the input container's array
            with elements order reversed along axis 0.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> m = startai.Container(a=startai.diag([1, 2, 3]), b=startai.arange(4))
        >>> m.flipud()
        {
            a: startai.array(
                [[ 0.,  0.,  3.],
                 [ 0.,  2.,  0.],
                 [ 1.,  0.,  0.]]
            )
            b: startai.array([3, 2, 1, 0])
        }
        """
        return self.static_flipud(self, copy=copy, out=out)

    def vstack(
        self: startai.Container,
        /,
        xs: Union[
            Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
            List[Union[startai.Array, startai.NativeArray, startai.Container]],
        ],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.stack. This method
        simply wraps the function, and so the docstring for startai.stack also
        applies to this method with minimal changes.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[0, 1], [2,3]]), b=startai.array([[4, 5]]))
        >>> y = startai.Container(a=startai.array([[3, 2], [1,0]]), b=startai.array([[1, 0]]))
        >>> x.vstack([y])
        {
            a: startai.array([[[0, 1],
                        [2, 3]],
                        [[3, 2],
                        [1, 0]]]),
            b: startai.array([[[4, 5]],
                        [[1, 0]]])
        }
        """
        new_xs = xs.cont_copy() if startai.is_startai_container(xs) else xs.copy()
        new_xs.insert(0, self.cont_copy())
        return self.static_vstack(
            new_xs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_vstack(
        xs: Union[
            Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
            List[Union[startai.Array, startai.NativeArray, startai.Container]],
        ],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.stack. This method simply
        wraps the function, and so the docstring for startai.vstack also applies to
        this method with minimal changes.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> c = startai.Container(a=[startai.array([1,2,3]), startai.array([0,0,0])],
                              b=startai.arange(3))
        >>> y = startai.Container.static_vstack(c)
        >>> print(y)
        {
            a: startai.array([[1, 2, 3],
                          [0, 0, 0]]),
            b: startai.array([[0],
                          [1],
                          [2]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "vstack",
            xs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def hstack(
        self: startai.Container,
        /,
        xs: Union[
            Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
            List[Union[startai.Array, startai.NativeArray, startai.Container]],
        ],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.hstack. This method
        simply wraps the function, and so the docstring for startai.hstack also
        applies to this method with minimal changes.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[0, 1], [2,3]]), b=startai.array([[4, 5]]))
        >>> y = startai.Container(a=startai.array([[3, 2], [1,0]]), b=startai.array([[1, 0]]))
        >>> z = x.hstack([y])
        >>> print(z)
        {
            a: startai.array([[0, 1, 3, 2],
                          [2, 3, 1, 0]]),
            b: startai.array([[4, 5, 1, 0]])
        }
        """
        new_xs = xs.cont_copy() if startai.is_startai_container(xs) else xs.copy()
        new_xs.insert(0, self.cont_copy())
        return self.static_hstack(
            new_xs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_hstack(
        xs: Union[
            Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
            List[Union[startai.Array, startai.NativeArray, startai.Container]],
        ],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.hstack. This method
        simply wraps the function, and so the docstring for startai.hstack also
        applies to this method with minimal changes.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> c = startai.Container(a=[startai.array([1,2,3]), startai.array([0,0,0])])
        >>> startai.Container.static_hstack(c)
        {
            a: startai.array([1, 2, 3, 0, 0, 0])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "hstack",
            xs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_rot90(
        m: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        copy: Union[bool, startai.Container] = None,
        k: Union[int, startai.Container] = 1,
        axes: Union[Tuple[int, int], startai.Container] = (0, 1),
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.rot90. This method simply
        wraps the function, and so the docstring for startai.rot90 also applies to
        this method with minimal changes.

        Parameters
        ----------
        m
            Input array of two or more dimensions.
        k
            Number of times the array is rotated by 90 degrees.
        axes
            The array is rotated in the plane defined by the axes. Axes must be
            different.
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
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container with a rotated view of m.

        Examples
        --------
        >>> m = startai.Container(a=startai.array([[1,2], [3,4]]),\
                        b=startai.array([[1,2,3,4],\
                                    [7,8,9,10]]))
        >>> n = startai.Container.static_rot90(m)
        >>> print(n)
        {
            a: startai.array([[2, 4],
                          [1, 3]]),
            b: startai.array([[4, 10],
                          [3, 9],
                          [2, 8],
                          [1, 7]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "rot90",
            m,
            copy=copy,
            k=k,
            axes=axes,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def rot90(
        self: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        copy: Union[bool, startai.Container] = None,
        k: Union[int, startai.Container] = 1,
        axes: Union[Tuple[int, int], startai.Container] = (0, 1),
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.rot90. This method simply
        wraps the function, and so the docstring for startai.rot90 also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array of two or more dimensions.
        k
            Number of times the array is rotated by 90 degrees.
        axes
            The array is rotated in the plane defined by the axes. Axes must be
            different.
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
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container with a rotated view of input array.

        Examples
        --------
        >>> m = startai.Container(a=startai.array([[1,2], [3,4]]),
        ...                   b=startai.array([[1,2,3,4],[7,8,9,10]]))
        >>> n = m.rot90()
        >>> print(n)
        {
            a: startai.array([[2, 4],
                          [1, 3]]),
            b: startai.array([[4, 10],
                          [3, 9],
                          [2, 8],
                          [1, 7]])
        }
        """
        return self.static_rot90(
            self,
            copy=copy,
            k=k,
            axes=axes,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_top_k(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        k: Union[int, startai.Container],
        /,
        *,
        axis: Union[int, startai.Container] = -1,
        largest: Union[bool, startai.Container] = True,
        sorted: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[Tuple[startai.Container, startai.Container], startai.Container]] = None,
    ) -> Tuple[startai.Container, startai.Container]:
        """startai.Container static method variant of startai.top_k. This method simply
        wraps the function, and so the docstring for startai.top_k also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            The container to compute top_k for.
        k
            Number of top elements to return must not exceed the array size.
        axis
            The axis along which we must return the top elements default value is 1.
        largest
            If largest is set to False we return k smallest elements of the array.
        sorted
            If sorted is set to True we return the elements in sorted order.
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
        out:
            Optional output tuple, for writing the result to. Must have two Container,
            with a shape that the returned tuple broadcast to.

        Returns
        -------
        ret
            a container with indices and values.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([-1, 2, -4]), b=startai.array([4., 5., 0.]))
        >>> y = startai.Container.static_top_k(x, 2)
        >>> print(y)
        {
            a: [
                values = startai.array([ 2, -1]),
                indices = startai.array([1, 0])
            ],
            b: [
                values = startai.array([5., 4.]),
                indices = startai.array([1, 0])
            ]
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "top_k",
            x,
            k,
            axis=axis,
            largest=largest,
            sorted=sorted,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def top_k(
        self: startai.Container,
        k: Union[int, startai.Container],
        /,
        *,
        axis: Union[int, startai.Container] = -1,
        largest: Union[bool, startai.Container] = True,
        sorted: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Tuple[startai.Container, startai.Container]] = None,
    ) -> Tuple[startai.Container, startai.Container]:
        """startai.Container instance method variant of startai.top_k. This method
        simply wraps the function, and so the docstring for startai.top_k also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container to compute top_k for.
        k
            Number of top elements to return must not exceed the array size.
        axis
            The axis along which we must return the top elements default value is 1.
        largest
            If largest is set to False we return k smallest elements of the array.
        sorted
            If sorted is set to True we return the elements in sorted order.
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
        out:
            Optional output tuple, for writing the result to. Must have two Container,
            with a shape that the returned tuple broadcast to.

        Returns
        -------
        ret
            a container with indices and values.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([-1, 2, -4]), b=startai.array([4., 5., 0.]))
        >>> y = x.top_k(2)
        >>> print(y)
        [{
            a: startai.array([2, -1]),
            b: startai.array([5., 4.])
        }, {
            a: startai.array([1, 0]),
            b: startai.array([1, 0])
        }]
        """
        return self.static_top_k(
            self,
            k,
            axis=axis,
            largest=largest,
            sorted=sorted,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_fliplr(
        m: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.fliplr. This method
        simply wraps the function, and so the docstring for startai.fliplr also
        applies to this method with minimal changes.

        Parameters
        ----------
        m
            the container with arrays to be flipped. Arrays must be at least 2-D.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
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
            container including arrays corresponding to the input container's array
            with elements order reversed along axis 1.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> m = startai.Container(a=startai.diag([1, 2, 3]),\
        ...                    b=startai.array([[1, 2, 3],[4, 5, 6]]))
        >>> startai.Container.static_fliplr(m)
        {
            a: startai.array([[0, 0, 1],
                          [0, 2, 0],
                          [3, 0, 0]]),
            b: startai.array([[3, 2, 1],
                          [6, 5, 4]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "fliplr",
            m,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def fliplr(
        self: startai.Container,
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.fliplr. This method
        simply wraps the function, and so the docstring for startai.fliplr also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            the container with arrays to be flipped. Arrays must be at least 2-D.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including arrays corresponding to the input container's array
            with elements order reversed along axis 1.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> m = startai.Container(a=startai.diag([1, 2, 3]),\
        ...                    b=startai.array([[1, 2, 3],[4, 5, 6]]))
        >>> m.fliplr()
        {
            a: startai.array([[0, 0, 1],
                          [0, 2, 0],
                          [3, 0, 0]]),
            b: startai.array([[3, 2, 1],
                          [6, 5, 4]])
        }
        """
        return self.static_fliplr(self, copy=copy, out=out)

    @staticmethod
    def static_i0(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.i0. This method simply
        wraps the function, and so the docstring for startai.i0 also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            the container with array inputs.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including arrays with the modified Bessel
            function evaluated at each of the elements of x.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array(4))
        >>> startai.Container.static_i0(x)
        {
            a: startai.array([1.26606588, 2.2795853 , 4.88079259])
            b: startai.array(11.30192195)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "i0",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def i0(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.i0. This method simply
        wraps the function, and so the docstring for startai.i0 also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            the container with array inputs.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including arrays with the modified Bessel
            function evaluated at each of the elements of x.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([1, 2, 3]), b=startai.array(4))
        >>> x.i0()
        {
            a: startai.array([1.26606588, 2.2795853 , 4.88079259])
            b: startai.array(11.30192195)
        }
        """
        return self.static_i0(self, out=out)

    @staticmethod
    def static_flatten(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        copy: Optional[Union[bool, startai.Container]] = None,
        start_dim: Union[int, startai.Container] = 0,
        end_dim: Union[int, startai.Container] = -1,
        order: Union[str, startai.Container] = "C",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.flatten. This method
        simply wraps the function, and so the docstring for startai.flatten also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container to flatten at leaves.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        start_dim
            first dim to flatten. If not set, defaults to 0.
        end_dim
            last dim to flatten. If not set, defaults to -1.
        order
            Read the elements of the input container using this index order,
            and place the elements into the reshaped array using this index order.
            ‘C’ means to read / write the elements using C-like index order,
            with the last axis index changing fastest, back to the first axis index
            changing slowest.
            ‘F’ means to read / write the elements using Fortran-like index order, with
            the first index changing fastest, and the last index changing slowest.
            Note that the ‘C’ and ‘F’ options take no account of the memory layout
            of the underlying array, and only refer to the order of indexing.
            Default order is 'C'

        Returns
        -------
        ret
            Container with arrays flattened at leaves.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
        ...                   b=startai.array([[[9, 10], [11, 12]], [[13, 14], [15, 16]]]))
        >>> startai.flatten(x)
        [{
            a: startai.array([1, 2, 3, 4, 5, 6, 7, 8])
            b: startai.array([9, 10, 11, 12, 13, 14, 15, 16])
        }]

        >>> x = startai.Container(a=startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
        ...                   b=startai.array([[[9, 10], [11, 12]], [[13, 14], [15, 16]]]))
        >>> startai.flatten(x, order="F")
        [{
            a: startai.array([1, 5, 3, 7, 2, 6, 4, 8])
            b: startai.array([9, 13, 11, 15, 10, 14, 12, 16])
        }]
        """
        return ContainerBase.cont_multi_map_in_function(
            "flatten",
            x,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            start_dim=start_dim,
            end_dim=end_dim,
            order=order,
            out=out,
        )

    def flatten(
        self: startai.Container,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        start_dim: Union[int, startai.Container] = 0,
        end_dim: Union[int, startai.Container] = -1,
        order: Union[str, startai.Container] = "C",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.flatten. This method
        simply wraps the function, and so the docstring for startai.flatten also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container to flatten at leaves.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        start_dim
            first dim to flatten. If not set, defaults to 0.
        end_dim
            last dim to flatten. If not set, defaults to -1.
        order
            Read the elements of the input container using this index order,
            and place the elements into the reshaped array using this index order.
            ‘C’ means to read / write the elements using C-like index order,
            with the last axis index changing fastest, back to the first axis index
            changing slowest.
            ‘F’ means to read / write the elements using Fortran-like index order, with
            the first index changing fastest, and the last index changing slowest.
            Note that the ‘C’ and ‘F’ options take no account of the memory layout
            of the underlying array, and only refer to the order of indexing.
            Default order is 'C'

        Returns
        -------
        ret
            Container with arrays flattened at leaves.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
        ...                   b=startai.array([[[9, 10], [11, 12]], [[13, 14], [15, 16]]]))
        >>> x.flatten()
        [{
            a: startai.array([1, 2, 3, 4, 5, 6, 7, 8])
            b: startai.array([9, 10, 11, 12, 13, 14, 15, 16])
        }]

        >>> x = startai.Container(a=startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
        ...                   b=startai.array([[[9, 10], [11, 12]], [[13, 14], [15, 16]]]))
        >>> x.flatten(order="F")
        [{
            a: startai.array([1, 5, 3, 7, 2, 6, 4, 8])
            b: startai.array([9, 13, 11, 15, 10, 14, 12, 16])
        }]
        """
        return self.static_flatten(
            self, copy=copy, start_dim=start_dim, end_dim=end_dim, out=out, order=order
        )

    @staticmethod
    def static_pad(
        input: startai.Container,
        pad_width: Union[Iterable[Tuple[int]], int, startai.Container],
        /,
        *,
        mode: Union[
            Literal[
                "constant",
                "dilated",
                "edge",
                "linear_ramp",
                "maximum",
                "mean",
                "median",
                "minimum",
                "reflect",
                "symmetric",
                "wrap",
                "empty",
            ],
            Callable,
            startai.Container,
        ] = "constant",
        stat_length: Union[Iterable[Tuple[int]], int, startai.Container] = 1,
        constant_values: Union[Iterable[Tuple[Number]], Number, startai.Container] = 0,
        end_values: Union[Iterable[Tuple[Number]], Number, startai.Container] = 0,
        reflect_type: Union[Literal["even", "odd"], startai.Container] = "even",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
        **kwargs: Optional[Union[Any, startai.Container]],
    ) -> startai.Container:
        """startai.Container static method variant of startai.pad.

        This method simply wraps the function, and so the docstring for
        startai.pad also applies to this method with minimal changes.
        """
        return ContainerBase.cont_multi_map_in_function(
            "pad",
            input,
            pad_width,
            mode=mode,
            stat_length=stat_length,
            constant_values=constant_values,
            end_values=end_values,
            reflect_type=reflect_type,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
            **kwargs,
        )

    def pad(
        self: startai.Container,
        pad_width: Union[Iterable[Tuple[int]], int, startai.Container],
        /,
        *,
        mode: Union[
            Literal[
                "constant",
                "dilated",
                "edge",
                "linear_ramp",
                "maximum",
                "mean",
                "median",
                "minimum",
                "reflect",
                "symmetric",
                "wrap",
                "empty",
            ],
            Callable,
            startai.Container,
        ] = "constant",
        stat_length: Union[Iterable[Tuple[int]], int, startai.Container] = 1,
        constant_values: Union[Iterable[Tuple[Number]], Number, startai.Container] = 0,
        end_values: Union[Iterable[Tuple[Number]], Number, startai.Container] = 0,
        reflect_type: Union[Literal["even", "odd"], startai.Container] = "even",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
        **kwargs: Optional[Union[Any, startai.Container]],
    ) -> startai.Container:
        """startai.Container instance method variant of startai.pad.

        This method simply wraps the function, and so the docstring for
        startai.pad also applies to this method with minimal changes.
        """
        return self.static_pad(
            self,
            pad_width,
            mode=mode,
            stat_length=stat_length,
            constant_values=constant_values,
            end_values=end_values,
            reflect_type=reflect_type,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
            **kwargs,
        )

    @staticmethod
    def static_vsplit(
        ary: Union[startai.Array, startai.NativeArray, startai.Container],
        indices_or_sections: Union[
            int, Sequence[int], startai.Array, startai.NativeArray, startai.Container
        ],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container static method variant of startai.vsplit. This method
        simply wraps the function, and so the docstring for startai.vsplit also
        applies to this method with minimal changes.

        Parameters
        ----------
        ary
            the container with array inputs.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        indices_or_sections
            If indices_or_sections is an integer n, the array is split into n
            equal sections, provided that n must be a divisor of the split axis.
            If indices_or_sections is a sequence of ints or 1-D array,
            then input is split at each of the indices.
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

        Returns
        -------
        ret
            list of containers holding arrays split vertically from the input

        Examples
        --------
        >>> ary = startai.Container(
                a = startai.array(
                        [[[0.,  1.],
                          [2.,  3.]],
                          [[4.,  5.],
                          [6.,  7.]]]
                    ),
                b=startai.array(
                        [[ 0.,  1.,  2.,  3.],
                         [ 4.,  5.,  6.,  7.],
                         [ 8.,  9., 10., 11.],
                         [12., 13., 14., 15.]]
                    )
                )
        >>> startai.Container.static_vsplit(ary, 2)
        [{
            a: startai.array([[[0., 1.],
                           [2., 3.]]]),
            b: startai.array([[0., 1., 2., 3.],
                          [4., 5., 6., 7.]])
        }, {
            a: startai.array([[[4., 5.],
                           [6., 7.]]]),
            b: startai.array([[8., 9., 10., 11.],
                          [12., 13., 14., 15.]])
        }]
        """
        return ContainerBase.cont_multi_map_in_function(
            "vsplit",
            ary,
            indices_or_sections,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def vsplit(
        self: startai.Container,
        indices_or_sections: Union[
            int, Sequence[int], startai.Array, startai.NativeArray, startai.Container
        ],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
    ) -> List[startai.Container]:
        """startai.Container instance method variant of startai.vsplit. This method
        simply wraps the function, and so the docstring for startai.vsplit also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            the container with array inputs.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
        indices_or_sections
            If indices_or_sections is an integer n, the array is split into n
            equal sections, provided that n must be a divisor of the split axis.
            If indices_or_sections is a sequence of ints or 1-D array,
            then input is split at each of the indices.

        Returns
        -------
        ret
            list of containers holding arrays split vertically from the input

        Examples
        --------
        >>> ary = startai.Container(
                a = startai.array(
                        [[[0.,  1.],
                          [2.,  3.]],
                          [[4.,  5.],
                          [6.,  7.]]]
                    ),
                b=startai.array(
                        [[ 0.,  1.,  2.,  3.],
                         [ 4.,  5.,  6.,  7.],
                         [ 8.,  9., 10., 11.],
                         [12., 13., 14., 15.]]
                    )
                )
        >>> ary.vsplit(2)
        [{
            a: startai.array([[[0., 1.],
                           [2., 3.]]]),
            b: startai.array([[0., 1., 2., 3.],
                          [4., 5., 6., 7.]])
        }, {
            a: startai.array([[[4., 5.],
                           [6., 7.]]]),
            b: startai.array([[8., 9., 10., 11.],
                          [12., 13., 14., 15.]])
        }]
        """
        return self.static_vsplit(self, indices_or_sections, copy=copy)

    @staticmethod
    def static_dsplit(
        ary: Union[startai.Array, startai.NativeArray, startai.Container],
        indices_or_sections: Union[
            int, Sequence[int], startai.Array, startai.NativeArray, startai.Container
        ],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container static method variant of startai.dsplit. This method
        simply wraps the function, and so the docstring for startai.dsplit also
        applies to this method with minimal changes.

        Parameters
        ----------
        ary
            the container with array inputs.
        indices_or_sections
            If indices_or_sections is an integer n, the array is split into n
            equal sections, provided that n must be a divisor of the split axis.
            If indices_or_sections is a sequence of ints or 1-D array,
            then input is split at each of the indices.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
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

        Returns
        -------
        ret
            list of containers holding arrays split from the input at the 3rd axis

        Examples
        --------
        >>> ary = startai.Container(
            a = startai.array(
                    [[[0.,  1.],
                      [2.,  3.]],
                      [[4.,  5.],
                      [6.,  7.]]]
                ),
            b=startai.array(
                    [[[ 0.,  1.,  2.,  3.],
                      [ 4.,  5.,  6.,  7.],
                      [ 8.,  9., 10., 11.],
                      [12., 13., 14., 15.]]]
                )
            )
        >>> startai.Container.static_dsplit(ary, 2)
        [{
            a: startai.array([[[0.], [2.]],
                          [[4.], [6.]]]),
            b: startai.array([[[0., 1.], [4., 5.], [8., 9.], [12., 13.]]])
        }, {
            a: startai.array([[[1.], [3.]],
                          [[5.], [7.]]]),
            b: startai.array([[[2., 3.], [6., 7.], [10., 11.], [14., 15.]]])
        }]
        """
        return ContainerBase.cont_multi_map_in_function(
            "dsplit",
            ary,
            indices_or_sections,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def dsplit(
        self: startai.Container,
        indices_or_sections: Union[
            int, Sequence[int], startai.Array, startai.NativeArray, startai.Container
        ],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
    ) -> List[startai.Container]:
        """startai.Container instance method variant of startai.dsplit. This method
        simply wraps the function, and so the docstring for startai.dsplit also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            the container with array inputs.
        indices_or_sections
            If indices_or_sections is an integer n, the array is split into n
            equal sections, provided that n must be a divisor of the split axis.
            If indices_or_sections is a sequence of ints or 1-D array,
            then input is split at each of the indices.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.

        Returns
        -------
        ret
            list of containers holding arrays split from the input at the 3rd axis

        Examples
        --------
        >>> ary = startai.Container(
            a = startai.array(
                    [[[0.,  1.],
                      [2.,  3.]],
                      [[4.,  5.],
                      [6.,  7.]]]
                ),
            b=startai.array(
                    [[[ 0.,  1.,  2.,  3.],
                      [ 4.,  5.,  6.,  7.],
                      [ 8.,  9., 10., 11.],
                      [12., 13., 14., 15.]]]
                )
            )
        >>> ary.dsplit(2)
        [{
            a: startai.array([[[0.], [2.]],
                          [[4.], [6.]]]),
            b: startai.array([[[0., 1.], [4., 5.], [8., 9.], [12., 13.]]])
        }, {
            a: startai.array([[[1.], [3.]],
                          [[5.], [7.]]]),
            b: startai.array([[[2., 3.], [6., 7.], [10., 11.], [14., 15.]]])
        }]
        """
        return self.static_dsplit(self, indices_or_sections, copy=copy)

    @staticmethod
    def static_atleast_1d(
        *arys: Union[startai.Array, startai.NativeArray, startai.Container],
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container static method variant of startai.atleast_1d. This method
        simply wraps the function, and so the docstring for startai.atleast_1d also
        applies to this method with minimal changes.

        Parameters
        ----------
        arys
            one or more container with array inputs.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
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

        Returns
        -------
        ret
            container or list of container where each elements within container is
            at least 1d. Copies are made only if necessary.

        Examples
        --------
        >>> ary = startai.Container(a=startai.array(1), b=startai.array([3,4,5]),\
                        c=startai.array([[3]]))
        >>> startai.Container.static_atleast_1d(ary)
        {
            a: startai.array([1]),
            b: startai.array([3, 4, 5]),
            c: startai.array([[3]]),
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "atleast_1d",
            *arys,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def atleast_1d(
        self: Union[startai.Container, startai.Array, startai.NativeArray],
        *arys: Union[startai.Container, startai.Array, startai.NativeArray, bool, Number],
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container instance method variant of startai.atleast_1d. This method
        simply wraps the function, and so the docstring for startai.atleast_1d also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            the container with array inputs.
        arys
            one or more container with array inputs.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
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

        Returns
        -------
        ret
            container or list of container where each elements within container is
            at least 1d. Copies are made only if necessary.

        Examples
        --------
        >>> ary1 = startai.Container(a=startai.array(1), b=startai.array([3,4]),\
                            c=startai.array([[5]]))
        >>> ary2 = startai.Container(a=startai.array(9), b=startai.array(2),\
                            c=startai.array(3))
        >>> ary1.atleast_1d(ary2)
        [{
            a: startai.array([1]),
            b: startai.array([3, 4]),
            c: startai.array([[5]])
        }, {
            a: startai.array([9]),
            b: startai.array([2]),
            c: startai.array([3])
        }]
        """
        return self.static_atleast_1d(
            self,
            *arys,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def dstack(
        self: startai.Container,
        /,
        xs: Union[
            Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
            List[Union[startai.Array, startai.NativeArray, startai.Container]],
        ],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.stack. This method
        simply wraps the function, and so the docstring for startai.stack also
        applies to this method with minimal changes.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[0, 1], [2,3]]), b=startai.array([[4, 5]]))
        >>> y = startai.Container(a=startai.array([[3, 2], [1,0]]), b=startai.array([[1, 0]]))
        >>> x.dstack([y])
        {
            a: startai.array([[[0, 3],
                           [1, 2]],
                          [[2, 1],
                           [3, 0]]]),
            b: startai.array([[[4, 1]],
                           [[5, 0]]])
        }
        """
        new_xs = xs.cont_copy() if startai.is_startai_container(xs) else xs.copy()
        new_xs.insert(0, self.cont_copy())
        return self.static_dstack(
            new_xs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_dstack(
        xs: Union[
            Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
            List[Union[startai.Array, startai.NativeArray, startai.Container]],
        ],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.stack. This method simply
        wraps the function, and so the docstring for startai.dstack also applies to
        this method with minimal changes.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> c = startai.Container(a=[startai.array([1,2,3]), startai.array([0,0,0])],
                              b=startai.arange(3))
        >>> startai.Container.static_dstack(c)
        {
            a: startai.array([[1, 0],
                          [2, 0]
                          [3,0]]),
            b: startai.array([[0, 1, 2])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "dstack",
            xs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_atleast_2d(
        *arys: Union[startai.Array, startai.NativeArray, startai.Container],
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container static method variant of startai.atleast_2d. This method
        simply wraps the function, and so the docstring for startai.atleast_2d also
        applies to this method with minimal changes.

        Parameters
        ----------
        arys
            one or more container with array inputs.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
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

        Returns
        -------
        ret
            container or list of container where each elements within container is
            at least 2D. Copies are made only if necessary.

        Examples
        --------
        >>> ary = startai.Container(a=startai.array(1), b=startai.array([3,4,5]),\
                        c=startai.array([[3]]))
        >>> startai.Container.static_atleast_2d(ary)
        {
            a: startai.array([[1]]),
            b: startai.array([[3, 4, 5]]),
            c: startai.array([[3]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "atleast_2d",
            *arys,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def atleast_2d(
        self: Union[startai.Container, startai.Array, startai.NativeArray],
        *arys: Union[startai.Container, startai.Array, startai.NativeArray],
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container instance method variant of startai.atleast_2d. This method
        simply wraps the function, and so the docstring for startai.atleast_2d also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            container with array inputs.
        arys
            one or more container with array inputs.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
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

        Returns
        -------
        ret
            container or list of container where each elements within container is
            at least 2D. Copies are made only if necessary.

        Examples
        --------
        >>> ary1 = startai.Container(a=startai.array(1), b=startai.array([3,4]),\
                            c=startai.array([[5]]))
        >>> ary2 = startai.Container(a=startai.array(9), b=startai.array(2),\
                            c=startai.array(3))
        >>> ary1.atleast_2d(ary2)
        [{
            a: startai.array([[1]]),
            b: startai.array([[3, 4]]),
            c: startai.array([[5]])
        }, {
            a: startai.array([[9]]),
            b: startai.array([[2]]),
            c: startai.array([[3]])
        }]
        """
        return self.static_atleast_2d(
            self,
            *arys,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_atleast_3d(
        *arys: Union[startai.Array, startai.NativeArray, startai.Container],
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container static method variant of startai.atleast_3d. This method
        simply wraps the function, and so the docstring for startai.atleast_3d also
        applies to this method with minimal changes.

        Parameters
        ----------
        arys
            one or more container with array inputs.
        copy
            boolean indicating whether or not to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
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

        Returns
        -------
        ret
            container or list of container where each elements within container is
            at least 3D. Copies are made only if necessary. For example, a 1-D array
            of shape (N,) becomes a view of shape (1, N, 1), and a 2-D array of shape
            (M, N) becomes a view of shape (M, N, 1).

        Examples
        --------
        >>> ary = startai.Container(a=startai.array(1), b=startai.array([3,4,5]),\
                        c=startai.array([[3]]))
        >>> startai.Container.static_atleast_3d(ary)
        {
            a: startai.array([[[1]]]),
            b: startai.array([[[3],
                           [4],
                           [5]]]),
            c: startai.array([[[3]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "atleast_3d",
            *arys,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def atleast_3d(
        self: Union[startai.Container, startai.Array, startai.NativeArray],
        *arys: Union[startai.Container, startai.Array, startai.NativeArray, bool, Number],
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container instance method variant of startai.atleast_3d. This method
        simply wraps the function, and so the docstring for startai.atleast_3d also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            container with array inputs.
        arys
            one or more container with array inputs.

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

        Returns
        -------
        ret
            container or list of container where each elements within container is
            at least 3D. Copies are made only if necessary. For example, a 1-D array
            of shape (N,) becomes a view of shape (1, N, 1), and a 2-D array of shape
            (M, N) becomes a view of shape (M, N, 1).

        Examples
        --------
        >>> ary1 = startai.Container(a=startai.array(1), b=startai.array([3,4]),\
                            c=startai.array([[5]]))
        >>> ary2 = startai.Container(a=startai.array(9), b=startai.array(2),\
                            c=startai.array(3))
        >>> ary1.atleast_3d(ary2)
        [{
            a: startai.array([[[1]]]),
            b: startai.array([[[3],
                           [4]]]),
            c: startai.array([[[5]]])
        }, {
            a: startai.array([[[9]]]),
            b: startai.array([[[2]]]),
            c: startai.array([[[3]]])
        }]
        """
        return self.static_atleast_3d(
            self,
            *arys,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_take_along_axis(
        arr: Union[startai.Array, startai.NativeArray, startai.Container],
        indices: Union[startai.Array, startai.NativeArray, startai.Container],
        axis: Union[int, startai.Container],
        mode: Union[str, startai.Container] = "fill",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.take_along_axis. This
        method simply wraps the function, and so the docstring for
        startai.take_along_axis also applies to this method with minimal changes.

        Parameters
        ----------
        arr
            container with array inputs.
        indices
            container with indices of the values to extract.
        axis
            The axis over which to select values. If axis is None, then arr and indices
            must be 1-D sequences of the same length.
        mode
            One of: 'clip', 'fill', 'drop'. Parameter controlling how out-of-bounds
            indices will be handled.
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
            a container with arrays of the same shape as those in indices.

        Examples
        --------
        >>> arr = startai.Container(a=startai.array([[1, 2], [3, 4]]),\
                                b=startai.array([[5, 6], [7, 8]]))
        >>> indices = startai.Container(a=startai.array([[0, 0], [1, 1]]),\
                                    b=startai.array([[1, 0], [1, 0]]))
        >>> startai.Container.static_take_along_axis(arr, indices, axis=1)
        {
            a: startai.array([[1, 1],
                          [4, 4]]),
            b: startai.array([[6, 5],
                          [8, 7]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "take_along_axis",
            arr,
            indices,
            axis,
            mode=mode,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def take_along_axis(
        self: Union[startai.Container, startai.Array, startai.NativeArray],
        indices: Union[startai.Container, startai.Array, startai.NativeArray],
        axis: Union[int, startai.Container],
        mode: Union[str, startai.Container] = "fill",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.take_along_axis. This
        method simply wraps the function, and so the docstring for
        startai.take_along_axis also applies to this method with minimal changes.

        Parameters
        ----------
        self
            container with array inputs.
        indices
            container with indices of the values to extract.
        axis
            The axis over which to select values. If axis is None, then arr and indices
            must be 1-D sequences of the same length.
        mode
            One of: 'clip', 'fill', 'drop'. Parameter controlling how out-of-bounds
            indices will be handled.
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
            a container with arrays of the same shape as those in indices.

        Examples
        --------
        >>> arr = startai.Container(a=startai.array([[1, 2], [3, 4]]),\
                                b=startai.array([[5, 6], [7, 8]]))
        >>> indices = startai.Container(a=startai.array([[0, 0], [1, 1]]),\
                                    b=startai.array([[1, 0], [1, 0]]))
        >>> arr.take_along_axis(indices, axis=1)
        [{
            a: startai.array([[1, 1],
                          [4, 4]]),
            b: startai.array([[6, 5],
                            [8, 7]])
        }]
        """
        return self.static_take_along_axis(
            self,
            indices,
            axis,
            mode=mode,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_hsplit(
        ary: Union[startai.Array, startai.NativeArray, startai.Container],
        indices_or_sections: Union[
            int, Sequence[int], startai.Array, startai.NativeArray, startai.Container
        ],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> List[startai.Container]:
        """startai.Container static method variant of startai.hsplit. This method
        simply wraps the function, and so the docstring for startai.hsplit also
        applies to this method with minimal changes.

        Parameters
        ----------
        ary
            the container with array inputs.
        indices_or_sections
            If indices_or_sections is an integer n, the array is split into n
            equal sections, provided that n must be a divisor of the split axis.
            If indices_or_sections is a sequence of ints or 1-D array,
            then input is split at each of the indices.
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

        Returns
        -------
        ret
            list of containers split horizontally from input array.

        Examples
        --------
        >>> ary = startai.Container(
            a = startai.array(
                    [[[0.,  1.],
                      [2.,  3.]],
                      [[4.,  5.],
                      [6.,  7.]]]
                ),
            b=startai.array(
                    [0.,  1.,  2.,  3.,
                     4.,  5.,  6.,  7.,
                     8.,  9.,  10., 11.,
                     12., 13., 14., 15.]
                )
            )
        >>> startai.Container.static_hsplit(ary, 2)
        [{
            a: startai.array([[[0., 1.]],
                          [[4., 5.]]]),
            b: startai.array([0., 1., 2., 3., 4., 5., 6., 7.])
        }, {
            a: startai.array([[[2., 3.]],
                          [[6., 7.]]]),
            b: startai.array([8., 9., 10., 11., 12., 13., 14., 15.])
        }]
        """
        return ContainerBase.cont_multi_map_in_function(
            "hsplit",
            ary,
            indices_or_sections,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def hsplit(
        self: startai.Container,
        indices_or_sections: Union[
            int, Sequence[int], startai.Array, startai.NativeArray, startai.Container
        ],
        copy: Optional[Union[bool, startai.Container]] = None,
        /,
    ) -> List[startai.Container]:
        """startai.Container instance method variant of startai.hsplit. This method
        simply wraps the function, and so the docstring for startai.hsplit also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            the container with array inputs.
        indices_or_sections
            If indices_or_sections is an integer n, the array is split into n
            equal sections, provided that n must be a divisor of the split axis.
            If indices_or_sections is a sequence of ints or 1-D array,
            then input is split at each of the indices.

        Returns
        -------
        ret
            list of containers split horizontally from input container

        Examples
        --------
        >>> ary = startai.Container(
            a = startai.array(
                    [[[0.,  1.],
                      [2.,  3.]],
                      [[4.,  5.],
                      [6.,  7.]]]
                ),
            b=startai.array(
                    [0.,  1.,  2.,  3.,
                     4.,  5.,  6.,  7.,
                     8.,  9.,  10., 11.,
                     12., 13., 14., 15.]
                )
            )
        >>> ary.hsplit(2)
        [{
            a: startai.array([[[0., 1.]],
                          [[4., 5.]]]),
            b: startai.array([0., 1., 2., 3., 4., 5., 6., 7.])
        }, {
            a: startai.array([[[2., 3.]],
                          [[6., 7.]]]),
            b: startai.array([8., 9., 10., 11., 12., 13., 14., 15.])
        }]
        """
        return self.static_hsplit(self, indices_or_sections, copy=copy)

    @staticmethod
    def static_broadcast_shapes(
        shapes: Union[startai.Container, List[Tuple[int]]],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.broadcast_shapes. This
        method simply wraps the function, and so the docstring for startai.hsplit
        also applies to this method with minimal changes.

        Parameters
        ----------
        shapes
            the container with shapes to broadcast.
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

        Returns
        -------
        ret
            Container with broadcasted shapes.

        Examples
        --------
        >>> shapes = startai.Container(a = [(2, 3), (2, 1)],
        ...                        b = [(2, 3), (1, 3)],
        ...                        c = [(2, 3), (2, 3)],
        ...                        d = [(2, 3), (2, 1), (1, 3), (2, 3)])
        >>> z = startai.Container.static_broadcast_shapes(shapes)
        >>> print(z)
        {
            a: (2, 3),
            b: (2, 3),
            c: (2, 3),
            d: (2, 3)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "broadcast_shapes",
            shapes,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def broadcast_shapes(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.broadcast_shapes. This
        method simply wraps the function, and so the docstring for
        startai.broadcast_shapes also applies to this method with minimal changes.

        Parameters
        ----------
        self
            the container with shapes to broadcast.

        Returns
        -------
        ret
            Container with broadcasted shapes.

        Examples
        --------
        >>> shapes = startai.Container(a = (2, 3, 5),
        ...                        b = (2, 3, 1))
        >>> z = shapes.broadcast_shapes()
        >>> print(z)
        {
            a: [2, 3, 5],
            b: [2, 3, 1]
        }
        """
        return self.static_broadcast_shapes(self, out=out)

    @staticmethod
    def static_expand(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        shape: Union[startai.Shape, startai.NativeShape, startai.Container],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """

        Parameters
        ----------
        x
            input container.
        shape
            A 1-D Array indicates the shape you want to expand to,
            following the broadcast rule.
        copy
            boolean indicating whether to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
            device
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
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            An output Container with the results.
        """
        return ContainerBase.cont_multi_map_in_function(
            "expand",
            x,
            shape,
            copy=copy,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def expand(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        shape: Union[startai.Shape, startai.NativeShape, startai.Container],
        /,
        *,
        copy: Optional[Union[bool, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """

        Parameters
        ----------
        self
            input container.
        shape
            A 1-D Array indicates the shape you want to expand to,
            following the broadcast rule.
        copy
            boolean indicating whether to copy the input array.
            If True, the function must always copy.
            If False, the function must never copy and must
            raise a ValueError in case a copy would be necessary.
            If None, the function must reuse existing memory buffer if possible
            and copy otherwise. Default: ``None``.
            device
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            An output Container with the results.


        """
        return self.static_expand(self, shape, copy=copy, out=out)

    @staticmethod
    def static_as_strided(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        shape: Union[startai.Shape, startai.NativeShape, Sequence[int], startai.Container],
        strides: Union[Sequence[int], startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.as_strided. This method
        simply wraps the function, and so the docstring for startai.as_strided also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input container.
        shape
            The shape of the new arrays.
        strides
            The strides of the new arrays (specified in bytes).
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

        Returns
        -------
        ret
            Output container.
        """
        return ContainerBase.cont_multi_map_in_function(
            "as_strided",
            x,
            shape,
            strides,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def as_strided(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        shape: Union[startai.Shape, startai.NativeShape, Sequence[int], startai.Container],
        strides: Union[Sequence[int], startai.Container],
        /,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.as_strided. This method
        simply wraps the function, and so the docstring for startai.as_strided also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container.
        shape
            The shape of the new arrays.
        strides
            The strides of the new arrays (specified in bytes).

        Returns
        -------
        ret
            Output container.
        """
        return self.static_as_strided(self, shape, strides)

    @staticmethod
    def static_concat_from_sequence(
        input_sequence: Union[
            Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
            List[Union[startai.Array, startai.NativeArray, startai.Container]],
        ],
        /,
        *,
        new_axis: Union[int, startai.Container] = 0,
        axis: Union[int, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.concat_from_sequence.
        This method simply wraps the function, and so the docstring for
        startai.concat_from_sequence also applies to this method with minimal
        changes.

        Parameters
        ----------
        input_sequence
            Container with leaves to join. Each array leave must have the same shape.
        new_axis
            Insert and concatenate on a new axis or not,
            default 0 means do not insert new axis.
            new_axis = 0: concatenate
            new_axis = 1: stack
        axis
            axis along which the array leaves will be concatenated. More details
            can be found in the docstring for startai.concat_from_sequence.

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
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an output container with the results.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[0, 1], [2,3]]), b=startai.array([[4, 5]]))
        >>> z = startai.Container.static_concat_from_sequence(x,new_axis = 1, axis = 1)
        >>> print(z)
        {
            a: startai.array([[0, 2],
                        [1, 3]]),
            b: startai.array([[4],
                        [5]])
        }

        >>> x = startai.Container(a=startai.array([[0, 1], [2,3]]), b=startai.array([[4, 5]]))
        >>> y = startai.Container(a=startai.array([[3, 2], [1,0]]), b=startai.array([[1, 0]]))
        >>> z = startai.Container.static_concat_from_sequence([x,y])
        >>> print(z)
        {
            a: startai.array([[0, 1],
                          [2, 3],
                          [3, 2],
                          [1, 0]]),
            b: startai.array([[4, 5],
                          [1, 0]])
        }

        >>> x = startai.Container(a=startai.array([[0, 1], [2,3]]), b=startai.array([[4, 5]]))
        >>> y = startai.Container(a=startai.array([[3, 2], [1,0]]), b=startai.array([[1, 0]]))
        >>> z = startai.Container.static_concat_from_sequence([x,y],new_axis=1, axis=1)
        >>> print(z)
        {
            a: startai.array([[[0, 1],
                        [3, 2]],
                        [[2, 3],
                        [1, 0]]]),
            b: startai.array([[[4, 5],
                        [1, 0]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "concat_from_sequence",
            input_sequence,
            new_axis=new_axis,
            axis=axis,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def concat_from_sequence(
        self: startai.Container,
        /,
        input_sequence: Union[
            Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
            List[Union[startai.Array, startai.NativeArray, startai.Container]],
        ],
        *,
        new_axis: Union[int, startai.Container] = 0,
        axis: Union[int, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.stack. This method
        simply wraps the function, and so the docstring for startai.stack also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Container with leaves to join with leaves of other arrays/containers.
             Each array leave must have the same shape.
        input_sequence
            Container with other leaves to join.
            Each array leave must have the same shape.
        new_axis
            Insert and concatenate on a new axis or not,
            default 0 means do not insert new axis.
            new_axis = 0: concatenate
            new_axis = 1: stack
        axis
            axis along which the array leaves will be concatenated. More details can
            be found in the docstring for startai.stack.
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
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            an output container with the results.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[0, 1], [2,3]]), b=startai.array([[4, 5]]))
        >>> y = startai.Container(a=startai.array([[3, 2], [1,0]]), b=startai.array([[1, 0]]))
        >>> z = startai.Container.static_concat_from_sequence([x,y],axis=1)
        >>> print(z)
        {
            a: startai.array([[[0, 1],
                        [3, 2]],
                        [[2, 3],
                        [1, 0]]]),
            b: startai.array([[[4, 5],
                        [1, 0]]])
        }
        """
        new_input_sequence = (
            input_sequence.cont_copy()
            if startai.is_startai_container(input_sequence)
            else input_sequence.copy()
        )
        new_input_sequence.insert(0, self.cont_copy())
        return self.concat_from_sequence(
            new_input_sequence,
            new_axis=new_axis,
            axis=axis,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def associative_scan(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        fn: Union[Callable, startai.Container],
        /,
        *,
        reverse: Union[bool, startai.Container] = False,
        axis: Union[int, startai.Container] = 0,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.associative_scan. This
        method simply wraps the function, and so the docstring for
        startai.associative_scan also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The Container to scan over.
        fn
            The associative function to apply.
        reverse
            Whether to scan in reverse with respect to the given axis.
        axis
            The axis to scan over.

        Returns
        -------
        ret
            The result of the scan.
        """
        return startai.associative_scan(self, fn, reverse=reverse, axis=axis)

    @staticmethod
    def _static_unique_consecutive(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.unique_consecutive.

        This method simply wraps the function, and so the docstring for
        startai.unique_consecutive also applies to this method with minimal
        changes.
        """
        return ContainerBase.cont_multi_map_in_function(
            "unique_consecutive",
            x,
            axis=axis,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def unique_consecutive(
        self: startai.Container,
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.unique_consecutive.

        This method simply wraps the function, and so the docstring for
        startai.unique_consecutive also applies to this method with minimal
        changes.
        """
        return self._static_unique_consecutive(
            self,
            axis=axis,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def _static_fill_diagonal(
        a: Union[startai.Array, startai.NativeArray, startai.Container],
        v: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        wrap: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.fill_diagonal.

        This method simply wraps the function, and so the docstring for
        startai.fill_diagonal also applies to this method with minimal
        changes.
        """
        return ContainerBase.cont_multi_map_in_function(
            "fill_diagonal",
            a,
            v,
            wrap=wrap,
        )

    def fill_diagonal(
        self: startai.Container,
        v: Union[int, float, startai.Container],
        /,
        *,
        wrap: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.fill_diagonal.

        This method simply wraps the function, and so the docstring for
        startai.fill_diagonal also applies to this method with minimal
        changes.
        """
        return self._static_fill_diagonal(
            self,
            v,
            wrap=wrap,
        )

    @staticmethod
    def static_unfold(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        mode: Optional[Union[int, startai.Container]] = 0,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.unfold.

        This method simply wraps the function, and so the docstring for
        startai.unfold also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            input tensor to be unfolded
        mode
            indexing starts at 0, therefore mode is in ``range(0, tensor.ndim)``
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container of unfolded tensors
        """
        return ContainerBase.cont_multi_map_in_function(
            "unfold",
            x,
            mode,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def unfold(
        self: startai.Container,
        /,
        mode: Optional[Union[int, startai.Container]] = 0,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.unfold.

        This method simply wraps the function, and so the docstring for
        startai.unfold also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            input tensor to be unfolded
        mode
            indexing starts at 0, therefore mode is in ``range(0, tensor.ndim)``
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container of unfolded tensors
        """
        return self.static_unfold(self, mode, out=out)

    @staticmethod
    def static_fold(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        mode: Union[int, startai.Container],
        shape: Union[startai.Shape, startai.NativeShape, Sequence[int], startai.Container],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.fold.

        This method simply wraps the function, and so the docstring for
        startai.fold also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            input tensor to be unfolded
        mode
            indexing starts at 0, therefore mode is in ``range(0, tensor.ndim)``
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container of folded tensors
        """
        return ContainerBase.cont_multi_map_in_function(
            "fold",
            x,
            mode,
            shape,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def fold(
        self: startai.Container,
        /,
        mode: Union[int, startai.Container],
        shape: Union[startai.Shape, startai.NativeShape, Sequence[int], startai.Container],
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.fold.

        This method simply wraps the function, and so the docstring for
        startai.fold also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            input tensor to be folded
        mode
            indexing starts at 0, therefore mode is in ``range(0, tensor.ndim)``
        shape
            shape of the original tensor before unfolding
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        -------
        ret
            Container of folded tensors
        """
        return self.static_fold(self, mode, shape, out=out)

    @staticmethod
    def static_partial_unfold(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        mode: Optional[Union[int, startai.Container]] = 0,
        skip_begin: Optional[Union[int, startai.Container]] = 1,
        skip_end: Optional[Union[int, startai.Container]] = 0,
        ravel_tensors: Optional[Union[bool, startai.Container]] = False,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.partial_unfold.

        This method simply wraps the function, and so the docstring for
        startai.partial_unfold also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            tensor of shape n_samples x n_1 x n_2 x ... x n_i
        mode
            indexing starts at 0, therefore mode is in range(0, tensor.ndim)
        skip_begin
            number of dimensions to leave untouched at the beginning
        skip_end
            number of dimensions to leave untouched at the end
        ravel_tensors
            if True, the unfolded tensors are also flattened
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            partially unfolded tensor
        """
        return ContainerBase.cont_multi_map_in_function(
            "partial_unfold",
            x,
            mode,
            skip_begin,
            skip_end,
            ravel_tensors,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def partial_unfold(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        mode: Optional[Union[int, startai.Container]] = 0,
        skip_begin: Optional[Union[int, startai.Container]] = 1,
        skip_end: Optional[Union[int, startai.Container]] = 0,
        ravel_tensors: Optional[Union[bool, startai.Container]] = False,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.partial_unfold.

        This method simply wraps the function, and so the docstring for
        startai.partial_unfold also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            tensor of shape n_samples x n_1 x n_2 x ... x n_i
        mode
            indexing starts at 0, therefore mode is in range(0, tensor.ndim)
        skip_begin
            number of dimensions to leave untouched at the beginning
        skip_end
            number of dimensions to leave untouched at the end
        ravel_tensors
            if True, the unfolded tensors are also flattened
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            partially unfolded tensor
        """
        return self.static_partial_unfold(
            self, mode, skip_begin, skip_end, ravel_tensors, out=out
        )

    @staticmethod
    def static_partial_fold(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        mode: Union[int, startai.Container],
        shape: Union[startai.Shape, startai.NativeShape, Sequence[int], startai.Container],
        skip_begin: Optional[Union[int, startai.Container]] = 1,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.partial_fold.

        This method simply wraps the function, and so the docstring for
        startai.partial_fold also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            a partially unfolded tensor
        mode
            indexing starts at 0, therefore mode is in range(0, tensor.ndim)
        shape
            the shape of the original full tensor (including skipped dimensions)
        skip_begin
            number of dimensions left untouched at the beginning
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            partially re-folded tensor
        """
        return ContainerBase.cont_multi_map_in_function(
            "partial_fold",
            x,
            mode,
            shape,
            skip_begin,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def partial_fold(
        self: Union[startai.Array, startai.NativeArray],
        /,
        mode: Union[int, startai.Container],
        shape: Union[startai.Shape, startai.NativeShape, Sequence[int], startai.Container],
        skip_begin: Optional[Union[int, startai.Container]] = 1,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.partial_fold.

        This method simply wraps the function, and so the docstring for
        startai.partial_fold also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            a partially unfolded tensor
        mode
            indexing starts at 0, therefore mode is in range(0, tensor.ndim)
        shape
            the shape of the original full tensor (including skipped dimensions)
        skip_begin
            number of dimensions left untouched at the beginning
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            partially re-folded tensor
        """
        return self.static_partial_fold(self, mode, shape, skip_begin, out=out)

    @staticmethod
    def static_partial_tensor_to_vec(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        skip_begin: Optional[Union[int, startai.Container]] = 1,
        skip_end: Optional[Union[int, startai.Container]] = 0,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.partial_tensor_to_vec.

        This method simply wraps the function, and so the docstring for
        startai.partial_tensor_to_vec also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            tensor to partially vectorise
        skip_begin
            number of dimensions to leave untouched at the beginning
        skip_end
            number of dimensions to leave untouched at the end
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            partially vectorised tensor with the
            `skip_begin` first and `skip_end` last dimensions untouched
        """
        return ContainerBase.cont_multi_map_in_function(
            "partial_tensor_to_vec",
            x,
            skip_begin,
            skip_end,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def partial_tensor_to_vec(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        skip_begin: Optional[Union[int, startai.Container]] = 1,
        skip_end: Optional[Union[int, startai.Container]] = 0,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.partial_tensor_to_vec.

        This method simply wraps the function, and so the docstring for
        startai.partial_tensor_to_vec also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            tensor to partially vectorise
        skip_begin
            number of dimensions to leave untouched at the beginning
        skip_end
            number of dimensions to leave untouched at the end
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            partially re-folded tensor
        """
        return self.static_partial_tensor_to_vec(self, skip_begin, skip_end, out=out)

    @staticmethod
    def static_partial_vec_to_tensor(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        shape: Union[startai.Shape, startai.NativeShape, Sequence[int], startai.Container],
        skip_begin: Optional[Union[int, startai.Container]] = 1,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.partial_vec_to_tensor.

        This method simply wraps the function, and so the docstring for
        startai.partial_vec_to_tensor also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            a partially vectorised tensor
        shape
            the shape of the original full tensor (including skipped dimensions)
        skip_begin
            number of dimensions to leave untouched at the beginning
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
            full tensor
        """
        return ContainerBase.cont_multi_map_in_function(
            "partial_vec_to_tensor",
            x,
            shape,
            skip_begin,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def partial_vec_to_tensor(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        shape: Union[startai.Shape, startai.NativeShape, Sequence[int], startai.Container],
        skip_begin: Optional[Union[int, startai.Container]] = 1,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.partial_vec_to_tensor.

        This method simply wraps the function, and so the docstring for
        startai.partial_vec_to_tensor also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            partially vectorized tensor
        shape
            the shape of the original full tensor (including skipped dimensions)
        skip_begin
            number of dimensions to leave untouched at the beginning
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            full tensor
        """
        return self.static_partial_vec_to_tensor(self, shape, skip_begin, out=out)

    @staticmethod
    def static_matricize(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        row_modes: Union[Sequence[int], startai.Container],
        column_modes: Optional[Union[Sequence[int], startai.Container]] = None,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.matricize.

        This method simply wraps the function, and so the docstring for
        startai.matricize also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            the input tensor
        row_modes
            modes to use as row of the matrix (in the desired order)
        column_modes
            modes to use as column of the matrix, in the desired order
            if None, the modes not in `row_modes` will be used in ascending order
        out
            optional output array, for writing the result to.

        ret
        -------
            startai.Container
        """
        return ContainerBase.cont_multi_map_in_function(
            "matricize",
            x,
            row_modes,
            column_modes,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def matricize(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        row_modes: Union[Sequence[int], startai.Container],
        column_modes: Optional[Union[Sequence[int], startai.Container]] = None,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.matricize.

        This method simply wraps the function, and so the docstring for
        startai.matricize also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            the input tensor
        row_modes
            modes to use as row of the matrix (in the desired order)
        column_modes
            modes to use as column of the matrix, in the desired order
            if None, the modes not in `row_modes` will be used in ascending order
        out
            optional output array, for writing the result to.
        ret
        -------
            startai.Container
        """
        return self.static_matricize(self, row_modes, column_modes, out=out)

    @staticmethod
    def static_soft_thresholding(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        threshold: Union[float, startai.Array, startai.NativeArray, startai.Container],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.soft_thresholding.

        This method simply wraps the function, and so the docstring for
        startai.soft_thresholding also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            the input tensor
        threshold
            float or array with shape tensor.shape
            * If float the threshold is applied to the whole tensor
            * If array, one threshold is applied per elements, 0 values are ignored
        out
            optional output array, for writing the result to.

        Returns
        -------
        startai.Container
            thresholded tensor on which the operator has been applied
        """
        return ContainerBase.cont_multi_map_in_function(
            "soft_thresholding",
            x,
            threshold,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def soft_thresholding(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        threshold: Union[float, startai.Array, startai.NativeArray, startai.Container],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.soft_thresholding.

        This method simply wraps the function, and so the docstring for
        startai.soft_thresholding also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            the input tensor
        threshold
            float or array with shape tensor.shape
            * If float the threshold is applied to the whole tensor
            * If array, one threshold is applied per elements, 0 values are ignored
        out
            optional output array, for writing the result to.

        Returns
        -------
        startai.Container
            thresholded tensor on which the operator has been applied
        """
        return self.static_soft_thresholding(self, threshold, out=out)

    @staticmethod
    def static_column_stack(
        xs: Sequence[Union[startai.Array, startai.NativeArray, startai.Container]],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.column_stack.

        This method simply wraps the function, and so the docstring for
        startai.column_stack also applies to this method with minimal
        changes.

        Parameters
        ----------
        xs
            Container with leaves to stack.

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
            Optional output array, for writing the result to.

        Returns
        -------
        ret
            An output container with the results.
        """
        return ContainerBase.cont_multi_map_in_function(
            "column_stack",
            xs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def column_stack(
        self: startai.Container,
        /,
        xs: Sequence[Union[startai.Array, startai.NativeArray, startai.Container]],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.column_stack.

        This method simply wraps the function, and so the docstring for
        startai.column_stack also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            Container with leaves to stack with leaves of other arrays/containers.
        xs
            Container with other leaves to join.

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
            Optional output array, for writing the result to.

        Returns
        -------
        ret
            An output container with the results.
        """
        new_xs = xs.cont_copy() if startai.is_startai_container(xs) else list(xs).copy()
        new_xs.insert(0, self.cont_copy())
        return self.static_column_stack(
            new_xs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_put_along_axis(
        arr: Union[startai.Array, startai.NativeArray, startai.Container],
        indices: Union[startai.Array, startai.NativeArray, startai.Container],
        values: Union[startai.Array, startai.NativeArray, startai.Container],
        axis: Union[int, startai.Container],
        /,
        *,
        mode: Optional[
            Union[Literal["sum", "min", "max", "mul", "mean", "replace"], startai.Container]
        ] = "replace",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.put_along_axis.

        This method simply wraps the function, and so the docstring for
        startai.put_along_axis also applies to this method with minimal
        changes.
        """
        return ContainerBase.cont_multi_map_in_function(
            "put_along_axis",
            arr,
            indices,
            values,
            axis,
            mode=mode,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def put_along_axis(
        self: startai.Container,
        indices: Union[startai.Array, startai.NativeArray, startai.Container],
        values: Union[startai.Array, startai.NativeArray, startai.Container],
        axis: Union[int, startai.Container],
        /,
        *,
        mode: Optional[
            Union[Literal["sum", "min", "max", "mul", "mean", "replace"], startai.Container]
        ] = "replace",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.put_along_axis.

        This method simply wraps the function, and so the docstring for
        startai.put_along_axis also applies to this method with minimal
        changes.
        """
        return self._static_put_along_axis(
            self,
            indices,
            values,
            axis,
            mode=mode,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_take(
        x: Union[int, startai.Array, startai.NativeArray, startai.Container],
        indices: Union[int, startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        mode: Union[str, startai.Container] = "fill",
        fill_value: Optional[Union[Number, startai.Container]] = None,
        out: Optional[Union[startai.Array, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.take.

        This method simply wraps the function, and so the docstring for
        startai.take also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input array
        indices
            array indices. Must have an integer data type.
        axis
            axis over which to select values. If `axis` is negative,
            the function must determine the axis along which to select values
            by counting from the last dimension.
            By default, the flattened input array is used.
        mode
            specifies how out-of-bounds `indices` will behave.
            -   ‘raise’ – raise an error
            -   ‘wrap’ – wrap around
            -   ‘clip’ – clip to the range (all indices that are too large are
            replaced by the index that addresses the last element along that axis.
            Note that this disables indexing with negative numbers.)
            -   'fill' (default) = returns invalid values (e.g. NaN)
            for out-of bounds indices (see also fill_value below)
        fill_value
            fill value to return for out-of-bounds slices
            (Defaults to NaN for inexact types,
            the largest negative value for signed types,
            the largest positive value for unsigned types, and True for booleans.)
        out
            optional output array, for writing the result to. It must
            have a shape that the inputs broadcast to.
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

        Returns
        -------
            ret
                an array having the same data type as `x`.
                The output array must have the same rank
                (i.e., number of dimensions) as `x` and
                must have the same shape as `x`,
                except for the axis specified by `axis`
                whose size must equal the number of elements in `indices`.

        Examples
        --------
        With `startai.Container` input:

        >>> x = startai.Container(a=startai.array([True,False,False]),
        ...                     b=startai.array([2.3,4.5,6.7]),
        ...                     c=startai.array([1,2,3]))
        >>> indices = startai.array([[1,9,2]])
        >>> y = startai.Container._static_take(x, indices)
        >>> print(y)
        {
            a: startai.array([[False, True, False]]),
            b: startai.array([[4.5, nan, 6.69999981]]),
            c: startai.array([[2, -2147483648, 3]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "take",
            x,
            indices,
            axis=axis,
            mode=mode,
            fill_value=fill_value,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def take(
        self: Union[int, startai.Array, startai.NativeArray, startai.Container],
        indices: Union[int, startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        axis: Optional[Union[int, startai.Container]] = None,
        mode: Union[str, startai.Container] = "fill",
        fill_value: Optional[Union[Number, startai.Container]] = None,
        out: Optional[Union[startai.Array, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.take.

        This method simply wraps the function, and so the docstring for
        startai.take also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        indices
            array indices. Must have an integer data type.
        axis
            axis over which to select values. If `axis` is negative,
            the function must determine the axis along which to select values
            by counting from the last dimension.
            By default, the flattened input array is used.
        mode
            specifies how out-of-bounds `indices` will behave.
            -   ‘raise’ – raise an error
            -   ‘wrap’ – wrap around
            -   ‘clip’ – clip to the range (all indices that are too large are
            replaced by the index that addresses the last element along that axis.
            Note that this disables indexing with negative numbers.)
            -   'fill' (default) = returns invalid values (e.g. NaN)
            for out-of bounds indices (see also fill_value below)
        fill_value
            fill value to return for out-of-bounds slices
            (Defaults to NaN for inexact types,
            the largest negative value for signed types,
            the largest positive value for unsigned types, and True for booleans.)
        out
            optional output array, for writing the result to. It must
            have a shape that the inputs broadcast to.
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

        Returns
        -------
            ret
                an array having the same data type as `x`.
                The output array must have the same rank
                (i.e., number of dimensions) as `x` and
                must have the same shape as `x`,
                except for the axis specified by `axis`
                whose size must equal the number of elements in `indices`.

        Examples
        --------
        With `startai.Container` input:

        >>> x = startai.Container(a=startai.array([True,False,False]),
        ...                     b=startai.array([2.3,4.5,6.7]),
        ...                     c=startai.array([1,2,3]))
        >>> indices = startai.array([[1,9,2]])
        >>> y = x.take(indices)
        >>> print(y)
        {
            a: startai.array([[False, True, False]]),
            b: startai.array([[4.5, nan, 6.69999981]]),
            c: startai.array([[2, -2147483648, 3]])
        }
        """
        return self._static_take(
            self,
            indices,
            axis=axis,
            mode=mode,
            fill_value=fill_value,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def _static_trim_zeros(
        a: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        trim: Optional[str] = "fb",
    ) -> startai.Container:
        """startai.Container static method variant of startai.trim_zeros. This method
        simply wraps the function, and so the docstring for startai.trim_zeros also
        applies to this method with minimal changes.

        Parameters
        ----------
        self : 1-D array
            Input array.
        trim : str, optional
            A string with 'f' representing trim from front and 'b' to trim from
            back. Default is 'fb', trim zeros from both front and back of the
            array.

        Returns
        -------
            1-D array
            The result of trimming the input. The input data type is preserved.

        Examples
        --------
        >>> a = startai.array([0, 0, 0, 0, 8, 3, 0, 0, 7, 1, 0])
        >>> startai.trim_zeros(a)
        array([8, 3, 0, 0, 7, 1])
        >>> startai.trim_zeros(a, 'b')
        array([0, 0, 0, 0, 8, 3, 0, 0, 7, 1])
        >>> startai.trim_zeros([0, 8, 3, 0, 0])
        [8, 3]
        """
        return ContainerBase.cont_multi_map_in_function(a, trim)

    def trim_zeros(
        self: startai.Container,
        /,
        *,
        trim: Optional[str] = "fb",
    ) -> startai.Array:
        """startai.Container instance method variant of startai.trim_zeros. This method
        simply wraps the function, and so the docstring for startai.trim_zeros also
        applies to this method with minimal changes.

        Parameters
        ----------
        self : 1-D array
            Input array.
        trim : str, optional
            A string with 'f' representing trim from front and 'b' to trim from
            back. Default is 'fb', trim zeros from both front and back of the
            array.

        Returns
        -------
            1-D array
            The result of trimming the input. The input data type is preserved.

        Examples
        --------
        >>> a = startai.array([0, 0, 0, 0, 8, 3, 0, 0, 7, 1, 0])
        >>> startai.trim_zeros(a)
        array([8, 3, 0, 0, 7, 1])
        >>> startai.trim_zeros(a, 'b')
        array([0, 0, 0, 0, 8, 3, 0, 0, 7, 1])
        >>> startai.trim_zeros([0, 8, 3, 0, 0])
        [8, 3]
        """
        return self._static_trim_zeros(self, trim=trim)

    @staticmethod
    def _static_unflatten(
        x: Union[int, startai.Array, startai.NativeArray, startai.Container],
        /,
        shape: Union[Tuple[int], startai.Array, startai.NativeArray, startai.Container],
        dim: Optional[Union[int, startai.Container]] = 0,
        *,
        out: Optional[Union[startai.Array, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.unflatten. This method
        simply wraps the function, and so the docstring for startai.unflatten also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input array
        shape
            array indices. Must have an integer data type.
        dim
            axis over which to select values. If `axis` is negative,
            the function must determine the axis along which to select values
            by counting from the last dimension.
            By default, the flattened input array is used.
        out
            optional output array, for writing the result to. It must
            have a shape that the inputs broadcast to.
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

        Returns
        -------
            ret
                an array having the same data type as `x`.
                The output array must have the same rank
                (i.e., number of dimensions) as `x` and
                must have the same shape as `x`,
                except for the axis specified by `axis`
                whose size must equal the number of elements in `indices`.


        Examples
        --------
        With 'startai.Container' input:

        >>> x = startai.Container(a = startai.array([[True, False, False, True],
                                            [False, True, False, True]])),
        ...                     b = startai.array([[1.2, 2.3, 3.4, 4.5],
                                            [5.6, 6.7, 7.8, 8.9]]),
        ...                     c = startai.array([[1, 2, 3, 4],
                                            [5, 6, 7, 8]]))
        >>> dim = 1
        >>> shape = (2, 2)
        >>> y = startai.Container._static_unflatten(x, shape=shape, dim=dim)
        >>> print(y)
        {
            a: startai.array([[[True, False], [False, True]],
                        [[False, True], [False, True]]])
            b: startai.array([[[1.2, 2.3], [3.4, 4.5]], [[5.6, 6.7], [7.8, 8.9]]])
            c: startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "unflatten",
            x,
            shape=shape,
            dim=dim,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def unflatten(
        self: startai.Container,
        /,
        shape: Union[Tuple[int], startai.Array, startai.NativeArray, startai.Container],
        dim: Optional[Union[int, startai.Container]] = 0,
        *,
        out: Optional[Union[startai.Array, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.unflatten. This method
        simply wraps the function, and so the docstring for startai.unflatten also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array
        shape
            array indices. Must have an integer data type.
        dim
            axis over which to unflatten. If `axis` is negative,
            the function must determine the axis along which to select values
            by counting from the last dimension.
            By default, the flattened input array is used.
        out
            optional output array, for writing the result to. It must
            have a shape that the inputs broadcast to.
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

        Returns
        -------
            ret
                an array having the same data type as `x`.
                The output array must have the same rank
                (i.e., number of dimensions) as `x` and
                must have the same shape as `x`,
                except for the axis specified by `dim`
                which is replaced with a tuple specified in `shape`.


        Examples
        --------
        With 'startai.Container' input:

        >>> x = startai.Container(a = startai.array([[True, False, False, True],
        ...                                 [False, True, False, True]]),
        ...                     b = startai.array([[1.2, 2.3, 3.4, 4.5],
        ...                                   [5.6, 6.7, 7.8, 8.9]]),
        ...                     c = startai.array([[1, 2, 3, 4],
        ...                                   [5, 6, 7, 8]]))
        >>> dim = 1
        >>> shape = (2, 2)
        >>> y = x.unflatten(shape=shape, dim=dim)
        >>> print(y)
        {
            a: startai.array([[[True, False], [False, True]],
                          [[False, True], [False, True]]]),
            b: startai.array([[[1.2, 2.3], [3.4, 4.5]], [[5.6, 6.7], [7.8, 8.9]]]),
            c: startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        }
        """
        return self._static_unflatten(
            self,
            shape=shape,
            dim=dim,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )


def concat_from_sequence(
    self: startai.Container,
    /,
    input_sequence: Union[
        Tuple[Union[startai.Array, startai.NativeArray, startai.Container]],
        List[Union[startai.Array, startai.NativeArray, startai.Container]],
    ],
    *,
    new_axis: Union[int, startai.Container] = 0,
    axis: Union[int, startai.Container] = 0,
    key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
    to_apply: Union[bool, startai.Container] = True,
    prune_unapplied: Union[bool, startai.Container] = False,
    map_sequences: Union[bool, startai.Container] = False,
    out: Optional[startai.Container] = None,
) -> startai.Container:
    """startai.Container instance method variant of startai.stack. This method simply
    wraps the function, and so the docstring for startai.stack also applies to this
    method with minimal changes.

    Parameters
    ----------
    self
    Container with leaves to join with leaves of other arrays/containers.
    Each array leave must have the same shape.
    input_sequence
    Container with other leaves to join.
    Each array leave must have the same shape.
    new_axis
    Insert and concatenate on a new axis or not,
    default 0 means do not insert new axis.
    new_axis = 0: concatenate
    new_axis = 1: stack
    axis
    axis along which the array leaves will be concatenated. More details can be found in
    the docstring for startai.stack.
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
    optional output array, for writing the result to. It must have a shape
    that the inputs broadcast to.

    Returns
    -------
    ret
    an output container with the results.

    Examples
    --------
    >>> x = startai.Container(a=startai.array([[0, 1], [2,3]]), b=startai.array([[4, 5]]))
    >>> y = startai.Container(a=startai.array([[3, 2], [1,0]]), b=startai.array([[1, 0]]))
    >>> z = startai.Container.static_concat_from_sequence([x,y],axis=1)
    >>> print(z)
    {
    'a': startai.array([[[0, 1],
                    [3, 2]],
                    [[2, 3],
                    [1, 0]]]),
    'b': startai.array([[[4, 5],
                    [1, 0]]])
    }
    """
    new_input_sequence = (
        input_sequence.cont_copy()
        if startai.is_startai_container(input_sequence)
        else input_sequence.copy()
    )
    new_input_sequence.insert(0, self.cont_copy())
    return self.concat_from_sequence(
        new_input_sequence,
        new_axis=new_axis,
        axis=axis,
        key_chains=key_chains,
        to_apply=to_apply,
        prune_unapplied=prune_unapplied,
        map_sequences=map_sequences,
        out=out,
    )
