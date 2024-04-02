# global
from typing import Optional, Union, List, Dict, Literal

# local
import startai
from startai.data_classes.container.base import ContainerBase


class _ContainerWithElementwise(ContainerBase):
    @staticmethod
    def _static_abs(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:  # noqa
        """startai.Container static method variant of startai.abs. This method simply
        wraps the function, and so the docstring for startai.abs also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a numeric data type.
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
            a container containing the absolute value of each element in ``x``. The
            returned container must have the same data type as ``x``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 2.6, -3.5]),
        ...                   b=startai.array([4.5, -5.3, -0, -2.3]))
        >>> y = startai.Container.static_abs(x)
        >>> print(y)
        {
            a: startai.array([0., 2.6, 3.5]),
            b: startai.array([4.5, 5.3, 0, 2.3])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "abs",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def abs(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.abs. This method simply
        wraps the function, and so the docstring for startai.abs also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a numeric data type.
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
            a container containing the absolute value of each element in ``self``. The
            returned container must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1.6, 2.6, -3.5]),
        ...                   b=startai.array([4.5, -5.3, -2.3]))
        >>> y = x.abs()
        >>> print(y)
        {
            a: startai.array([1.6, 2.6, 3.5]),
            b: startai.array([4.5, 5.3, 2.3])
        }
        """
        return self._static_abs(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_acosh(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.cosh. This method simply
        wraps the function, and so the docstring for startai.cosh also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container whose elements each represent the area of a hyperbolic
            sector. Should have a floating-point data type.
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
            a container containing the inverse hyperbolic cosine of each element
            in ``x``. The returned container must have a floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., 2., 3, 4]),
        ...                   b=startai.array([1., 3., 10.0, 6]))
        >>> y = startai.Container.static_acosh(x)
        >>> print(y)
        {
            a: startai.array([0., 1.32, 1.76, 2.06]),
            b: startai.array([0., 1.76, 2.99, 2.48])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "acosh",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def acosh(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.acosh. This method
        simply wraps the function, and so the docstring for startai.acosh also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container whose elements each represent the area of a hyperbolic
            sector. Should have a floating-point data type.
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
            a container containing the inverse hyperbolic cosine of each element in
            ``self``. The returned container must have a floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., 2., 3, 4]),
        ...                   b=startai.array([1., 3., 10.0, 6]))
        >>> y = x.acosh()
        >>> print(y)
        {
            a: startai.array([0., 1.32, 1.76, 2.06]),
            b: startai.array([0., 1.76, 2.99, 2.48])
        }
        """
        return self._static_acosh(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_acos(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.acos. This method simply
        wraps the function, and so the docstring for startai.acos also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the inverse cosine of each element in ``x``.
            The returned container must have a floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., -1, 1]), b=startai.array([1., 0., -1.]))
        >>> y = startai.Container.static_acos(x)
        >>> print(y)
        {
            a: startai.array([1.57, 3.14, 0.]),
            b: startai.array([0., 1.57, 3.14])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "acos",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_add(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        x2: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        alpha: Optional[Union[int, float, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.add. This method simply
        wraps the function, and so the docstring for startai.add also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            first input array or container. Should have a numeric data type.
        x2
            second input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`). Should have a numeric data type.
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
        alpha
            scalar multiplier for ``x2``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the element-wise sums.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.array([[1.1, 2.3, -3.6]])
        >>> y = startai.Container(a=startai.array([[4.], [5.], [6.]]),
        ...                   b=startai.array([[5.], [6.], [7.]]))
        >>> z = startai.Container.static_add(x, y)
        >>> print(z)
        {
            a: startai.array([[5.1, 6.3, 0.4],
                          [6.1, 7.3, 1.4],
                          [7.1, 8.3, 2.4]]),
            b: startai.array([[6.1, 7.3, 1.4],
                          [7.1, 8.3, 2.4],
                          [8.1, 9.3, 3.4]])
        }

        With multiple :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = startai.Container.static_add(x, y)
        >>> print(z)
        {
            a: startai.array([5, 7, 9]),
            b: startai.array([7, 9, 11])
        }

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = startai.Container.static_add(x, y, alpha=2)
        >>> print(z)
        {
            a: startai.array([9, 12, 15]),
            b: startai.array([12, 15, 18])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "add",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            alpha=alpha,
            out=out,
        )

    def acos(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.acos. This method
        simply wraps the function, and so the docstring for startai.acos also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the inverse cosine of each element in ``self``.
            The returned container must have a floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., -1, 1]), b=startai.array([1., 0., -1.]))
        >>> y = x.acos()
        >>> print(y)
        {
            a: startai.array([1.57, 3.14, 0.]),
            b: startai.array([0., 1.57, 3.14])
        }
        """
        return self._static_acos(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def add(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        alpha: Optional[Union[int, float, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.add. This method simply
        wraps the function, and so the docstring for startai.add also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input container. Should have a numeric data type.
        x2
            second input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.
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
        alpha
            scalar multiplier for ``x2``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the element-wise sums.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([5, 6, 7]))

        >>> z = x.add(y)
        >>> print(z)
        {
            a: startai.array([5, 7, 9]),
            b: startai.array([7, 9, 11])
        }

        >>> z = x.add(y, alpha=3)
        >>> print(z)
        {
            a: startai.array([13, 17, 21]),
            b: startai.array([17, 21, 25])
        }
        """
        return self._static_add(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            alpha=alpha,
            out=out,
        )

    @staticmethod
    def _static_asin(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.asin. This method simply
        wraps the function, and so the docstring for startai.asin also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the inverse sine of each element in ``x``.
            The returned container must have a floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., -0.5, -1.]),
        ...                   b=startai.array([0.1, 0.8, 2.]))
        >>> y = startai.Container.static_asin()
        >>> print(y)
        {
            a: startai.array([0., -0.524, -1.57]),
            b: startai.array([0.1, 0.927, nan])
        }

        >>> x = startai.Container(a=startai.array([0.4, 0.9, -0.9]),
        ...                   b=startai.array([[4, -3, -0.2]))
        >>> y = startai.Container(a=startai.zeros(3), b=startai.zeros(3))
        >>> startai.Container.static_asin(out=y)
        >>> print(y)
        {
            a: startai.array([0.412, 1.12, -1.12]),
            b: startai.array([nan, nan, -0.201])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "asin",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def asin(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.asin. This method
        simply wraps the function, and so the docstring for startai.asin also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the inverse sine of each element in ``self``.
            The returned container must have a floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 0.5, 1.]),
        ...                   b=startai.array([-4., 0.8, 2.]))
        >>> y = x.asin()
        >>> print(y)
        {
            a: startai.array([0., 0.524, 1.57]),
            b: startai.array([nan, 0.927, nan])
        }

        >>> x = startai.Container(a=startai.array([12., 1.5, 0.]),
        ...                   b=startai.array([-0.85, 0.6, 0.3]))
        >>> y = startai.Container(a=startai.zeros(3), b=startai.zeros(3))
        >>> x.asin(out=y)
        >>> print(y)
        {
            a: startai.array([nan, nan, 0.]),
            b: startai.array([-1.02, 0.644, 0.305])
        }
        """
        return self._static_asin(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_asinh(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.asinh. This method simply
        wraps the function, and so the docstring for startai.asinh also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container whose elements each represent the area of a hyperbolic
            sector. Should have a floating-point data type.
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
            a container containing the inverse hyperbolic sine of each element
            in ``x``. The returned container must have a floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.5, 0., -3.5]),
        ...                   b=startai.array([3.4, -5.3, -0, -2.8]))
        >>> y = startai.Container.static_asinh(x)
        >>> print(y)
        {
            a: startai.array([1.19, 0., -1.97]),
            b: startai.array([1.94, -2.37, 0., -1.75])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "asinh",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def asinh(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.asinh. This method
        simply wraps the function, and so the docstring for startai.asinh also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container whose elements each represent the area of a hyperbolic
            sector. Should have a floating-point data type.
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
            a container containing the inverse hyperbolic sine of each element in
            ``self``. The returned container must have a floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1, 3.7, -5.1]),
        ...                   b=startai.array([4.5, -2.4, -1.5]))
        >>> y = x.asinh()
        >>> print(y)
        {
            a: startai.array([-0.881, 2.02, -2.33]),
            b: startai.array([2.21, -1.61, -1.19])
        }
        """
        return self._static_asinh(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_atan(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.atan. This method simply
        wraps the function, and so the docstring for startai.atan also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the inverse tangent of each element in ``x``.
            The returned container must have a floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., -1, 1]), b=startai.array([1., 0., -6]))
        >>> y = startai.Container.static_atan(x)
        >>> print(y)
        {
            a: startai.array([0., -0.785, 0.785]),
            b: startai.array([0.785, 0., -1.41])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "atan",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def atan(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.atan. This method
        simply wraps the function, and so the docstring for startai.atan also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the inverse tangent of each element in ``x``.
            The returned container must have a floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., -1, 1]), b=startai.array([1., 0., -6]))
        >>> y = x.atan()
        >>> print(y)
        {
            a: startai.array([0., -0.785, 0.785]),
            b: startai.array([0.785, 0., -1.41])
        }
        """
        return self._static_atan(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_atan2(
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
        """startai.Container static method variant of startai.atan2. This method simply
        wraps the function, and so the docstring for startai.atan2 also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            first input array or container corresponding to the y-coordinates.
            Should have a real-valued floating-point data type.
        x2
            second input array or container corresponding to the x-coordinates.
            Must be compatible with ``x1``
            (see :ref:`broadcasting`). Should have a real-valued
            floating-point data type.
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
            a container containing the inverse tangent of the quotient ``x1/x2``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 2.6, -3.5]),
        ...                   b=startai.array([4.5, -5.3, -0]))
        >>> y = startai.array([3.0, 2.0, 1.0])
        >>> startai.Container.static_atan2(x, y)
        {
            a: startai.array([0., 0.915, -1.29]),
            b: startai.array([0.983, -1.21, 0.])
        }

        >>> x = startai.Container(a=startai.array([0., 2.6, -3.5]),
        ...                   b=startai.array([4.5, -5.3, -0, -2.3]))
        >>> y = startai.Container(a=startai.array([-2.5, 1.75, 3.5]),
        ...                   b=startai.array([2.45, 6.35, 0, 1.5]))
        >>> z = startai.Container.static_atan2(x, y)
        >>> print(z)
        {
            a: startai.array([3.14, 0.978, -0.785]),
            b: startai.array([1.07, -0.696, 0., -0.993])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "atan2",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def atan2(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.atan2. This method
        simply wraps the function, and so the docstring for startai.atan2 also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array or container corresponding to the y-coordinates.
            Should have a real-valued floating-point data type.
        x2
            second input array or container corresponding to the x-coordinates.
            Must be compatible with ``self`` (see :ref:`broadcasting`).
            Should have a real-valued floating-point data type.
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
            a container containing the inverse tangent of the quotient ``self/x2``.
            The returned array must have a real-valued floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 2.6, -3.5]),
        ...                   b=startai.array([4.5, -5.3, -0]))
        >>> y = startai.array([3.0, 2.0, 1.0])
        >>> x.atan2(y)
        {
            a: startai.array([0., 0.915, -1.29]),
            b: startai.array([0.983, -1.21, 0.])
        }

        >>> x = startai.Container(a=startai.array([0., 2.6, -3.5]),
        ...                   b=startai.array([4.5, -5.3, -0, -2.3]))
        >>> y = startai.Container(a=startai.array([-2.5, 1.75, 3.5]),
        ...                   b=startai.array([2.45, 6.35, 0, 1.5]))
        >>> z = x.atan2(y)
        >>> print(z)
        {
            a: startai.array([3.14, 0.978, -0.785]),
            b: startai.array([1.07, -0.696, 0., -0.993])
        }
        """
        return self._static_atan2(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_atanh(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.atanh. This method simply
        wraps the function, and so the docstring for startai.atanh also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container whose elements each represent the area of a hyperbolic
            sector. Should have a floating-point data type.
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
            a container containing the inverse hyperbolic tangent of each
            element in ``x``. The returned container must have a floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, 0.5, -0.5]), b=startai.array([0., 0.2, 0.9]))
        >>> y = startai.Container.static_atanh(x)
        >>> print(y)
        {
            a: startai.array([0., 0.549, -0.549]),
            b: startai.array([0., 0.203, 1.47])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "atanh",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def atanh(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.atanh. This method
        simply wraps the function, and so the docstring for startai.atanh also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container whose elements each represent the area of a
            hyperbolic sector. Should have a floating-point data type.
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
            a container containing the inverse hyperbolic tangent of each element
            in ``self``. The returned container must have a floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, 0.5, -0.5]), b=startai.array([0., 0.2, 0.9]))
        >>> y = x.atanh()
        >>> print(y)
        {
            a: startai.array([0., 0.549, -0.549]),
            b: startai.array([0., 0.203, 1.47])
        }
        """
        return self._static_atanh(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_bitwise_and(
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
        """startai.Container static method variant of startai.bitwise_and. This method
        simply wraps the function, and so the docstring for startai.bitwise_and
        also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            first input array or container. Should have an integer or boolean
            data type.
        x2
            second input array or container Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.array([1, 2, 3])
        >>> y = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = startai.Container.static_bitwise_and(x, y)
        >>> print(z)
        {
                a: startai.array([0, 0, 2]),
                b: startai.array([1, 2, 3])
        }

        With multiple :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = startai.Container.static_bitwise_and(x, y)
        >>> print(z)
        {
                a: startai.array([0, 0, 2]),
                b: startai.array([0, 2, 4])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "bitwise_and",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def bitwise_and(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.bitwise_and. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_and also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array or container. Should have an integer or boolean
            data type.
        x2
            second input array or container Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([True, True]), b=startai.array([False, True]))
        >>> y = startai.Container(a=startai.array([False, True]), b=startai.array([False, True]))
        >>> x.bitwise_and(y, out=y)
        >>> print(y)
        {
            a: startai.array([False, True]),
            b: startai.array([False, True])
        }
        """
        return self._static_bitwise_and(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_bitwise_left_shift(
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
        """startai.Container static method variant of startai.bitwise_left_shift. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_left_shift also applies to this method with minimal
        changes.

        Parameters
        ----------
        x1
            first input array or container. Should have an integer or boolean
            data type.
        x2
            second input array or container Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined by
            :ref:`type-promotion`.
        """
        return ContainerBase.cont_multi_map_in_function(
            "bitwise_left_shift",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def bitwise_left_shift(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.bitwise_left_shift.
        This method simply wraps the function, and so the docstring for
        startai.bitwise_left_shift also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            first input array or container. Should have an integer or boolean
            data type.
        x2
            second input array or container Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
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
            a container containing the element-wise results. The returned container
            must have a data type determined by :ref:`type-promotion`.
        """
        return self._static_bitwise_left_shift(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_bitwise_invert(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.bitwise_invert. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_invert also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned array must have the same data type as ``x``.

        Examples
        --------
        >>> x = startai.Container(a=[False, True, False], b=[True, True, False])
        >>> y = startai.Container.static_bitwise_invert(x)
        >>> print(y)
        {
            a: startai.array([True, False, True]),
            b: startai.array([False, False, True])
        }

        >>> x = startai.Container(a=[1, 2, 3], b=[4, 5, 6])
        >>> y = startai.Container.static_bitwise_invert(x)
        >>> print(y)
        {
            a: startai.array([-2, -3, -4]),
            b: startai.array([-5, -6, -7])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "bitwise_invert",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def bitwise_invert(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.bitwise_invert. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_invert also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.Container(a = startai.array([False, True, False]),
        ...                   b = startai.array([True, True, False]))
        >>> y = x.bitwise_invert()
        >>> print(y)
        {
            a: startai.array([True, False, True]),
            b: startai.array([False, False, True])
        }

        >>> x = startai.Container(a = startai.array([1, 2, 3]),
        ...                   b = startai.array([4, 5, 6]))
        >>> y = x.bitwise_invert()
        >>> print(y)
        {
            a: startai.array([-2, -3, -4]),
            b: startai.array([-5, -6, -7])
        }
        """
        return self._static_bitwise_invert(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_cos(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.cos. This method simply
        wraps the function, and so the docstring for startai.cos also applies to
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
            a container containing the cosine of each element in ``x``. The returned
            container must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., -1, 1]), b=startai.array([1., 0., -6]))
        >>> y = startai.Container.static_cos(x)
        >>> print(y)
        {
            a: startai.array([1., 0.54, 0.54]),
            b: startai.array([0.54, 1., 0.96])
        }
        """
        return startai.ContainerBase.cont_multi_map_in_function(
            "cos",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def cos(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.cos. This method simply
        wraps the function, and so the docstring for startai.cos also applies to
        this method with minimal changes.

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
            a container containing the cosine of each element in ``self``.
            The returned container must have a floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., -1, 1]), b=startai.array([1., 0., -6]))
        >>> y = x.cos()
        >>> print(y)
        {
            a: startai.array([1., 0.54, 0.54]),
            b: startai.array([0.54, 1., 0.96])
        }
        """
        return self._static_cos(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_bitwise_or(
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
        """startai.Container static method variant of startai.bitwise_or. This method
        simply wraps the function, and so the docstring for startai.bitwise_or also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned array must have the same data type as ``x``.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> y = startai.array([1, 2, 3])
        >>> x = startai.Container(a=startai.array([4, 5, 6]))
        >>> z = startai.Container.static_bitwise_or(x, y)
        >>> print(z)
        {
            a: startai.array([5, 7, 7]),
        }

        With multiple :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = startai.Container.static_bitwise_or(x, y)
        >>> print(z)
        {
            a: startai.array([5, 7, 7]),
            b: startai.array([7, 7, 7])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "bitwise_or",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def bitwise_or(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.bitwise_or. This method
        simply wraps the function, and so the docstring for startai.bitwise_or also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        Using :class:`startai.Container` instance method:

        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = x.bitwise_or(y)
        >>> print(z)
        {
            a: startai.array([5, 7, 7]),
            b: startai.array([7, 7, 7])
        }
        """
        return self._static_bitwise_or(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_bitwise_right_shift(
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
        """startai.Container static method variant of startai.bitwise_right_shift. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_right_shift also applies to this method with minimal
        changes.

        Parameters
        ----------
        x1
            first input array or container. Should have an integer or boolean data type.
        x2
            second input array or container Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> a = startai.Container(a = startai.array([2, 3, 4]), b = startai.array([5, 10, 64]))
        >>> b = startai.array([0, 1, 2])
        >>> y = startai.Container.static_bitwise_right_shift(a, b)
        >>> print(y)
        {
            a: startai.array([2, 1, 1]),
            b: startai.array([5, 5, 16])
        }

        With multiple :class:`startai.Container` inputs:

        >>> a = startai.Container(a = startai.array([2, 3, 4]), b = startai.array([5, 10, 64]))
        >>> b = startai.Container(a = startai.array([0, 1, 2]), b = startai.array([2]))
        >>> y = startai.Container.static_bitwise_right_shift(a, b)
        >>> print(y)
        {
            a: startai.array([2, 1, 1]),
            b: startai.array([1, 2, 16])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "bitwise_right_shift",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def bitwise_right_shift(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.bitwise_right_shift.
        This method simply wraps the function, and so the docstring for
        startai.bitwise_right_shift also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            first input array or container. Should have an integer or boolean data type.
        x2
            second input array or container Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
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
            a container containing the element-wise results. The returned container
            must have a data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> a = startai.Container(a = startai.array([2, 3, 4]), b = startai.array([5, 10, 64]))
        >>> b = startai.Container(a = startai.array([0, 1, 2]), b = startai.array([2]))
        >>> y = a.bitwise_right_shift(b)
        >>> print(y)
        {
            a: startai.array([2, 1, 1]),
            b: startai.array([1, 2, 16])
        }
        """
        return self._static_bitwise_right_shift(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_bitwise_xor(
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
        """startai.Container static method variant of startai.bitwise_xor. This method
        simply wraps the function, and so the docstring for startai.bitwise_xor
        also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            first input array or container. Should have an integer or boolean
            data type.
        x2
            second input array or container Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a = startai.array([89]), b = startai.array([3]))
        >>> y = startai.Container(a = startai.array([12]), b = startai.array([5]))
        >>> z = startai.Container.static_bitwise_xor(x, y)
        >>> print(z)
        {
            a: startai.array([85]),
            b: startai.array([6])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "bitwise_xor",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def bitwise_xor(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.bitwise_xor. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_xor also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array or container. Should have an integer or
            boolean data type.
        x2
            second input array or container Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a = startai.array([89]), b = startai.array([3]))
        >>> y = startai.Container(a = startai.array([12]), b = startai.array([5]))
        >>> z = x.bitwise_xor(y)
        >>> print(z)
        {
            a: startai.array([85]),
            b: startai.array([6])
        }
        """
        return self._static_bitwise_xor(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_ceil(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.ceil. This method simply
        wraps the function, and so the docstring for startai.ceil also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a numeric data type.
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
            an container containing the rounded result for each element in ``x``.
            The returned array must have the same data type as ``x``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.5, 0.5, -1.4]),
        ...                   b=startai.array([5.4, -3.2, 5.2]))
        >>> y = startai.Container.static_ceil(x)
        >>> print(y)
        {
            a: startai.array([3., 1., -1.]),
            b: startai.array([6., -3., 6.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "ceil",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def ceil(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.ceil. This method
        simply wraps the function, and so the docstring for startai.ceil also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a numeric data type.
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
            an container containing the rounded result for each element in ``self``.
            The returned container must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.5, 0.5, -1.4]),
        ...                   b=startai.array([5.4, -3.2, 5.2]))
        >>> y = x.ceil()
        >>> print(y)
        {
            a: startai.array([3., 1., -1.]),
            b: startai.array([6., -3., 6.])
        }
        """
        return self._static_ceil(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_cosh(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.cosh. This method simply
        wraps the function, and so the docstring for startai.cosh also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container whose elements each represent a hyperbolic angle. Should
            have a floating-point data type.
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
            an container containing the hyperbolic cosine of each element in ``x``. The
            returned container must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([-1, 0.23, 1.12]), b=startai.array([1, -2, 0.76]))
        >>> y = startai.Container.static_cosh(x)
        >>> print(y)
        {
            a: startai.array([1.54, 1.03, 1.7]),
            b: startai.array([1.54, 3.76, 1.3])
        }

        >>> x = startai.Container(a=startai.array([-3, 0.34, 2.]),
        ...                   b=startai.array([0.67, -0.98, -3]))
        >>> y = startai.Container(a=startai.zeros(1), b=startai.zeros(1))
        >>> startai.Container.static_cosh(x, out=y)
        >>> print(y)
        {
            a: startai.array([10.1, 1.06, 3.76]),
            b: startai.array([1.23, 1.52, 10.1])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "cosh",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def cosh(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.cosh. This method
        simply wraps the function, and so the docstring for startai.cosh also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container whose elements each represent a hyperbolic angle. Should
            have a floating-point data type.
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
            an container containing the hyperbolic cosine of each element in ``self``.
            The returned container must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([-1, 0.23, 1.12]), b=startai.array([1, -2, 0.76]))
        >>> y = x.cosh()
        >>> print(y)
        {
            a: startai.array([1.54, 1.03, 1.7]),
            b: startai.array([1.54, 3.76, 1.3])
        }

        >>> x = startai.Container(a=startai.array([-3, 0.34, 2.]),
        ...                   b=startai.array([0.67, -0.98, -3]))
        >>> y = startai.Container(a=startai.zeros(3), b=startai.zeros(3))
        >>> x.cosh(out=y)
        >>> print(y)
        {
            a: startai.array([10.1, 1.06, 3.76]),
            b: startai.array([1.23, 1.52, 10.1])
        }
        """
        return self._static_cosh(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_divide(
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
        """startai.Container static method variant of startai.divide. This method
        simply wraps the function, and so the docstring for startai.divide also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            dividend input array or container. Should have a real-valued data type.
        x2
            divisor input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([12., 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> x2 = startai.Container(a=startai.array([1., 2.3, 3]), b=startai.array([2.4, 3., 2.]))
        >>> y = startai.Container.static_divide(x1, x2)
        >>> print(y)
        {
            a: startai.array([12., 1.52, 2.1]),
            b: startai.array([1.25, 0.333, 0.45])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "divide",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def divide(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.divide. This method
        simply wraps the function, and so the docstring for startai.divide also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array or container. Should have a real-valued
            data type.
        x2
            divisor input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([12., 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> x2 = startai.Container(a=startai.array([1., 2.3, 3]), b=startai.array([2.4, 3., 2.]))
        >>> y = x1.divide(x2)
        >>> print(y)
        {
            a: startai.array([12., 1.52, 2.1]),
            b: startai.array([1.25, 0.333, 0.45])
        }

        With :code:`Number` instances at the leaves:

        >>> x = startai.Container(a=1, b=2)
        >>> y = startai.Container(a=5, b=4)
        >>> z = x.divide(y)
        >>> print(z)
        {
            a: 0.2,
            b: 0.5
        }
        """
        return self._static_divide(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_equal(
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
        """startai.Container static method variant of startai.equal. This method simply
        wraps the function, and so the docstring for startai.equal also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. May have any data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            May have any data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([12, 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> x2 = startai.Container(a=startai.array([12, 2.3, 3]), b=startai.array([2.4, 3., 2.]))
        >>> y = startai.Container.static_equal(x1, x2)
        >>> print(y)
        {
            a: startai.array([True, False, False]),
            b: startai.array([False, False, False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "equal",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def equal(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.equal. This method
        simply wraps the function, and so the docstring for startai.equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. May have any data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            May have any data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([12, 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> x2 = startai.Container(a=startai.array([12, 2.3, 3]), b=startai.array([2.4, 3., 2.]))
        >>> y = x1.equal(x2)
        >>> print(y)
        {
            a: startai.array([True, False, False]),
            b: startai.array([False, False, False])
        }

        With mixed :class:`startai.Container` and :class:`startai.Array` inputs:

        >>> x1 = startai.Container(a=startai.array([12., 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> x2 = startai.array([3., 1., 0.9])
        >>> y = x1.equal(x2)
        >>> print(y)
        {
            a: startai.array([False, False, False]),
            b: startai.array([True, True, True])
        }
        """
        return self._static_equal(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_nan_to_num(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        copy: Union[bool, startai.Container] = True,
        nan: Union[float, int, startai.Container] = 0.0,
        posinf: Optional[Union[float, int, startai.Container]] = None,
        neginf: Optional[Union[float, int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.nan_to_num. This method
        simply wraps the function, and so the docstring for startai.nan_to_num also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input container with array items.
        copy
            Whether to create a copy of x (True) or to replace values in-place (False).
            The in-place operation only occurs if casting to an array does not require
            a copy. Default is True.
        nan
            Value to be used to fill NaN values. If no value is passed then NaN values
            will be replaced with 0.0.
        posinf
            Value to be used to fill positive infinity values. If no value is passed
            then positive infinity values will be replaced with a very large number.
        neginf
            Value to be used to fill negative infinity values.
            If no value is passed then negative infinity values
            will be replaced with a very small (or negative) number.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with replaced non-finite elements.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 3, nan]),\
                               b=startai.array([1, 2, 3, inf]))
        >>> startai.Container.static_nan_to_num(x, posinf=5e+100)
        {
            a: startai.array([1.,  1.,  3.,  0.0])
            b: startai.array([1., 2., 1.,  5e+100])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "nan_to_num",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            copy=copy,
            nan=nan,
            posinf=posinf,
            neginf=neginf,
            out=out,
        )

    def nan_to_num(
        self: startai.Container,
        /,
        *,
        copy: Union[bool, startai.Container] = True,
        nan: Union[float, int, startai.Container] = 0.0,
        posinf: Optional[Union[float, int, startai.Container]] = None,
        neginf: Optional[Union[float, int, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.nan_to_num. This method
        simply wraps the function, and so the docstring for startai.nan_to_num also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container with array items.
        copy
            Whether to create a copy of x (True) or to replace values in-place (False).
            The in-place operation only occurs if casting to an array does not require
            a copy. Default is True.
        nan
            Value to be used to fill NaN values. If no value is passed then NaN values
            will be replaced with 0.0.
        posinf
            Value to be used to fill positive infinity values. If no value is passed
            then positive infinity values will be replaced with a very large number.
        neginf
            Value to be used to fill negative infinity values.
            If no value is passed then negative infinity values
            will be replaced with a very small (or negative) number.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with replaced non-finite elements.

        Examples
        --------
        >>> a = startai.array([1., 2, 3, startai.nan], dtype="float64")
        >>> b = startai.array([1., 2, 3, startai.inf], dtype="float64")
        >>> x = startai.Container(a=a, b=b)
        >>> ret = x.nan_to_num(posinf=5e+100)
        >>> print(ret)
        {
            a: startai.array([1., 2., 3., 0.]),
            b: startai.array([1.e+000, 2.e+000, 3.e+000, 5.e+100])
        }
        """
        return self.static_nan_to_num(
            self, copy=copy, nan=nan, posinf=posinf, neginf=neginf, out=out
        )

    @staticmethod
    def static_imag(
        val: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.imag. This method simply
        wraps the function, and so the docstring for startai.imag also applies to
        this method with minimal changes.

        Parameters
        ----------
        val
            Array-like input.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Returns an Container including arrays with the imaginary part
            of complex numbers.

        Examples
        --------
        >>> x = startai.Container(a=startai.array(np.array([1+2j, 3+4j, 5+6j])),
                                b=startai.array(np.array([-2.25 + 4.75j, 3.25 + 5.75j])))
        >>> x
        {
            a: startai.array([1.+2.j, 3.+4.j, 5.+6.j]),
            b: startai.array([-2.25+4.75j, 3.25+5.75j])
        }
        >>> startai.Container.static_imag(x)
        {
            a: startai.array([2., 4., 6.]),
            b: startai.array([4.75, 5.75])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "imag",
            val,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def imag(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.imag. This method
        simply wraps the function, and so the docstring for startai.imag also
        applies to this method with minimal changes.

        Parameters
        ----------
        val
            Array-like input.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Returns an Container including arrays with the imaginary part
            of complex numbers.

        Examples
        --------
        >>> x = startai.Container(a=startai.array(np.array([1+2j, 3+4j, 5+6j])),
                                b=startai.array(np.array([-2.25 + 4.75j, 3.25 + 5.75j])))
        >>> x
        {
            a: startai.array([1.+2.j, 3.+4.j, 5.+6.j]),
            b: startai.array([-2.25+4.75j, 3.25+5.75j])
        }
        >>> x.imag()
        {
            a: startai.array([2., 4., 6.]),
            b: startai.array([4.75, 5.75])
        }
        """
        return self.static_imag(self, out=out)

    @staticmethod
    def static_angle(
        z: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        deg: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.angle. This method simply
        wraps the function, and so the docstring for startai.angle also applies to
        this method with minimal changes.

        Parameters
        ----------
        z
            Array-like input.
        deg
            optional bool.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Returns an array of angles for each complex number in the input.
            If def is False(default), angle is calculated in radian and if
            def is True, then angle is calculated in degrees.

        Examples
        --------
        >>> startai.set_backend('tensorflow')
        >>> x = startai.Container(a=startai.array([-2.25 + 4.75j, 3.25 + 5.75j]),
                                b=startai.array([-2.25 + 4.75j, 3.25 + 5.75j]))
        >>> x
        {
            a: startai.array([-2.25+4.75j, 3.25+5.75j]),
            b: startai.array([-2.25+4.75j, 3.25+5.75j])
        }
        >>> startai.Container.static_angle(x)
        {
            a: startai.array([2.01317055, 1.05634501]),
            b: startai.array([2.01317055, 1.05634501])
        }
        >>> startai.set_backend('numpy')
        >>> startai.Container.static_angle(x,deg=True)
        {
            a: startai.array([115.3461759, 60.524111]),
            b: startai.array([115.3461759, 60.524111])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "angle",
            z,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            deg=deg,
            out=out,
        )

    def angle(
        self: startai.Container,
        /,
        *,
        deg: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.angle. This method
        simply wraps the function, and so the docstring for startai.angle also
        applies to this method with minimal changes.

        Parameters
        ----------
        z
            Array-like input.
        deg
            optional bool.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Returns an array of angles for each complex number in the input.
            If def is False(default), angle is calculated in radian and if
            def is True, then angle is calculated in degrees.

        Examples
        --------
        >>> startai.set_backend('tensorflow')
        >>> x = startai.Container(a=startai.array([-2.25 + 4.75j, 3.25 + 5.75j]),
                                b=startai.array([-2.25 + 4.75j, 3.25 + 5.75j]))
        >>> x
        {
            a: startai.array([-2.25+4.75j, 3.25+5.75j]),
            b: startai.array([-2.25+4.75j, 3.25+5.75j])
        }
        >>> x.angle()
        {
            a: startai.array([2.01317055, 1.05634501]),
            b: startai.array([2.01317055, 1.05634501])
        }
        >>> startai.set_backend('numpy')
        >>> x.angle(deg=True)
        {
            a: startai.array([115.3461759, 60.524111]),
            b: startai.array([115.3461759, 60.524111])
        }
        """
        return self.static_angle(self, deg=deg, out=out)

    @staticmethod
    def static_gcd(
        x1: Union[startai.Array, startai.NativeArray, startai.Container, int, list, tuple],
        x2: Union[startai.Array, startai.NativeArray, startai.Container, int, list, tuple],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.gcd. This method simply
        wraps the function, and so the docstring for startai.gcd also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            first input container with array-like items.
        x2
            second input container with array-like items.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise gcd of input arrays.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1, 2, 3]),\
                               b=startai.array([1, 2, 3]))
        >>> x2 = startai.Container(a=startai.array([5, 6, 7]),\
                               b=10)
        >>> startai.Container.static_gcd(x1, x2)
        {
            a: startai.array([1.,  1.,  3.])
            b: startai.array([1., 2., 1.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "gcd",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def gcd(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.gcd. This method simply
        wraps the function, and so the docstring for startai.gcd also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input container with array-like items.
        x2
            second input container with array-like items.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise gcd of input arrays.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1, 2, 3]),\
                               b=startai.array([1, 2, 3]))
        >>> x2 = startai.Container(a=startai.array([5, 6, 7]),\
                               b=10)
        >>> x1.gcd(x2)
        {
            a: startai.array([1.,  1.,  3.])
            b: startai.array([1., 2., 1.])
        }
        """
        return self.static_gcd(self, x2, out=out)

    @staticmethod
    def static_exp2(
        x: Union[startai.Array, startai.NativeArray, startai.Container, float, list, tuple],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.exp2. This method simply
        wraps the function, and so the docstring for startai.exp2 also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            container with the base input arrays.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise 2 to the power
            of input arrays elements.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 3]),\
                               b=[5, 6, 7])
        >>> startai.Container.static_exp2(x)
        {
            a: startai.array([2.,  4.,  8.])
            b: startai.array([32., 64., 128.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "exp2",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def exp2(
        self: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.exp2. This method
        simply wraps the function, and so the docstring for startai.exp2 also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            container with the base input arrays.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise 2 to the power
            of input array elements.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 3]),\
                               b=[5, 6, 7])
        >>> x.exp2()
        {
            a: startai.array([2.,  4.,  8.])
            b: startai.array([32., 64., 128.])
        }
        """
        return self.static_exp2(self, out=out)

    @staticmethod
    def _static_exp(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.exp. This method simply
        wraps the function, and so the docstring for startai.exp also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a floating-point data type.
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
            a container containing the evaluated result for each element in ``x``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., 2.,]), b=startai.array([4., 5.]))
        >>> y = startai.Container.static_exp(x)
        >>> print(y)
        {
            a: startai.array([2.71828198, 7.38905573]),
            b: startai.array([54.59814835, 148.4131622])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "exp",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def exp(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.exp. This method simply
        wraps the function, and so the docstring for startai.exp also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a floating-point data type.
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
            a container containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., 2., 3.]), b=startai.array([4., 5., 6.]))
        >>> y = x.exp()
        >>> print(y)
        {
            a: startai.array([2.71828198, 7.38905573, 20.08553696]),
            b: startai.array([54.59814835, 148.4131622, 403.428772])
        }
        """
        return self._static_exp(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_expm1(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.expm1. This method simply
        wraps thefunction, and so the docstring for startai.expm1 also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a floating-point data type.
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
            a container containing the evaluated result for each element in ``x``.
            The returned array must have areal-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` static method:

        >>> x = startai.Container(a=startai.array([1, 2]), b=startai.array([3, 4]))
        >>> print(startai.Container.static_expm1(x))
        {
            a: startai.array([1.71828175, 6.38905621]),
            b: startai.array([19.08553696, 53.59815216])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "expm1",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def expm1(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.expm1. This method
        simply wraps the function, and so the docstring for startai.expm1 also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a floating-point data type.
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
            a container containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.5, 0.5]),
        ...                   b=startai.array([5.4, -3.2]))
        >>> y = x.expm1()
        >>> print(y)
        {
            a: startai.array([11.2, 0.649]),
            b: startai.array([220., -0.959])
        }

        >>> y = startai.Container(a=startai.array([0., 0.]))
        >>> x = startai.Container(a=startai.array([4., -2.]))
        >>> x.expm1(out=y)
        >>> print(y)
        {
            a: startai.array([53.6, -0.865])
        }
        """
        return self._static_expm1(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_floor(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.floor. This method simply
        wraps thefunction, and so the docstring for startai.floor also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a numeric data type.
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
            a container containing the rounded result for each element in ``x``. The
            returned array must have the same data type as ``x``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.5, 0.5, -1.4]),
        ...                   b=startai.array([5.4, -3.2, 5.2]))
        >>> y = startai.Container.static_floor(x)
        >>> print(y)
        {
            a: startai.array([2., 0., -2.]),
            b: startai.array([5., -4., 5.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "floor",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def floor(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.floor. This method
        simply wraps the function, and so the docstring for startai.floor also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a numeric data type.
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
            a container containing the rounded result for each element in ``self``.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2.5, 0.5, -1.4]),
        ...                   b=startai.array([5.4, -3.2, 5.2]))
        >>> y = x.floor()
        >>> print(y)
        {
            a: startai.array([2., 0., -2.]),
            b: startai.array([5., -4., 5.])
        }
        """
        return self._static_floor(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_floor_divide(
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
        """startai.Container static method variant of startai.floor_divide. This method
        simply wraps the function, and so the docstring for startai.floor_divide
        also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            dividend input array or container. Should have a real-valued data type.
        x2
            divisor input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([4., 5., 6.]), b=startai.array([7., 8., 9.]))
        >>> x2 = startai.Container(a=startai.array([5., 4., 2.5]), b=startai.array([2.3, 3.7, 5]))
        >>> y = startai.Container.static_floor_divide(x1, x2)
        >>> print(y)
        {
            a: startai.array([0., 1., 2.]),
            b: startai.array([3., 2., 1.])
        }

        With mixed :class:`startai.Container` and :class:`startai.Array` inputs:

        >>> x1 = startai.Container(a=startai.array([4., 5., 6.]), b=startai.array([7., 8., 9.]))
        >>> x2 = startai.array([2, 3, 4])
        >>> y = startai.Container.static_floor_divide(x1, x2)
        >>> print(y)
        {
            a: startai.array([2., 1., 1.]),
            b: startai.array([3., 2., 2.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "floor_divide",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def floor_divide(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.floor_divide. This
        method simply wraps the function, and so the docstring for
        startai.floor_divide also applies to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array or container. Should have a real-valued
            data type.
        x2
            divisor input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([4., 5., 6.]), b=startai.array([7., 8., 9.]))
        >>> x2 = startai.Container(a=startai.array([5., 4., 2.5]), b=startai.array([2.3, 3.7, 5]))
        >>> y = x1.floor_divide(x2)
        >>> print(y)
        {
            a: startai.array([0., 1., 2.]),
            b: startai.array([3., 2., 1.])
        }

        With mixed :class:`startai.Container` and :class:`startai.Array` inputs:

        >>> x1 = startai.Container(a=startai.array([4., 5., 6.]), b=startai.array([7., 8., 9.]))
        >>> x2 = startai.array([2, 3, 4])
        >>> y = x1.floor_divide(x2)
        >>> print(y)
        {
            a: startai.array([2., 1., 1.]),
            b: startai.array([3., 2., 2.])
        }
        """
        return self._static_floor_divide(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_fmin(
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
        """startai.Container static method variant of startai.fmin. This method simply
        wraps the function, and so the docstring for startai.fmin also applies to
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
            Container including arrays with element-wise minimums.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([2, 3, 4]),\
                               b=startai.array([startai.nan, 0, startai.nan]))
        >>> x2 = startai.Container(a=startai.array([1, 5, 2]),\
                               b=startai.array([0, startai.nan, startai.nan]))
        >>> startai.Container.static_fmin(x1, x2)
        {
            a: startai.array([1, 3, 2]),
            b: startai.array([0., 0., nan])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "fmin",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def fmin(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.fmin. This method
        simply wraps the function, and so the docstring for startai.fmin also
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
            Container including arrays with element-wise minimums.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([2, 3, 4]),\
                               b=startai.array([startai.nan, 0, startai.nan]))
        >>> x2 = startai.Container(a=startai.array([1, 5, 2]),\
                               b=startai.array([0, startai.nan, startai.nan]))
        >>> x1.fmin(x2)
        {
            a: startai.array([1, 3, 2]),
            b: startai.array([0., 0., nan])
        }
        """
        return self.static_fmin(self, x2, out=out)

    @staticmethod
    def _static_greater(
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
        """startai.Container static method variant of startai.greater. This method
        simply wraps the function, and so the docstring for startai.greater also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a real-valued data type.
        x2
            divisor input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned array must
            have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = startai.Container.static_greater(y,x)
        >>> print(z)
        {
            a: startai.array([False, False, False]),
            b: startai.array([True, True, True])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "greater",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def greater(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.greater. This method
        simply wraps the function, and so the docstring for startai.greater also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a real-valued data type.
        x2
            divisor input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned array must
            have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = x.greater(y)
        >>> print(z)
        {
            a: startai.array([True, True, True]),
            b: startai.array([False, False, False])
        }
        """
        return self._static_greater(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_greater_equal(
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
        """startai.Container static method variant of startai.greater_equal. This
        method simply wraps the function, and so the docstring for
        startai.greater_equal also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = startai.Container.static_greater_equal(y)
        >>> print(z)
        {
            a:startai.array([True,True,True]),
            b:startai.array([False,False,False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "greater_equal",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def greater_equal(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.greater_equal. This
        method simply wraps the function, and so the docstring for
        startai.greater_equal also applies to this metho with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = x.greater_equal(y)
        >>> print(z)
        {
            a:startai.array([True,True,True]),
            b:startai.array([False,False,False])
        }
        """
        return self._static_greater_equal(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_isfinite(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.isfinite. This method
        simply wraps the function, and so the docstring for startai.isfinite also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued data type.
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
            a container containing the test result. An element ``out_i`` is ``True``
            if ``x_i`` is finite and ``False`` otherwise.
            The returned array must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 999999999999]),
        ...                   b=startai.array([float('-0'), startai.nan]))
        >>> y = startai.Container.static_isfinite(x)
        >>> print(y)
        {
            a: startai.array([True, True]),
            b: startai.array([True, False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "isfinite",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def isfinite(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.isfinite. This method
        simply wraps the function, and so the docstring for startai.isfinite also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued data type.
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
            a container containing the test result. An element ``out_i`` is ``True``
            if ``self_i`` is finite and ``False`` otherwise.
            The returned array must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 999999999999]),
        ...                   b=startai.array([float('-0'), startai.nan]))
        >>> y = x.isfinite()
        >>> print(y)
        {
            a: startai.array([True, True]),
            b: startai.array([True, False])
        }
        """
        return self._static_isfinite(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_isinf(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        detect_positive: Union[bool, startai.Container] = True,
        detect_negative: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.isinf. This method simply
        wraps the function, and so the docstring for startai.isinf also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued data type.
        detect_positive
            if ``True``, positive infinity is detected.
        detect_negative
            if ``True``, negative infinity is detected.
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
            a container containing the test result. An element ``out_i`` is ``True``
            if ``x_i`` is either positive or negative infinity and ``False``
            otherwise. The returned array must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([-1, -float('inf'), 1.23]),
        ...                   b=startai.array([float('inf'), 3.3, -4.2]))
        >>> z = startai.Container.static_isinf(x)
        >>> print(z)
        {
            a: startai.array([False, True, False]),
            b: startai.array([True, False, False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "isinf",
            x,
            detect_positive=detect_positive,
            detect_negative=detect_negative,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def isinf(
        self: startai.Container,
        *,
        detect_positive: Union[bool, startai.Container] = True,
        detect_negative: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.isinf. This method
        simply wraps the function, and so the docstring for startai.isinf also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued data type.
        detect_positive
            if ``True``, positive infinity is detected.
        detect_negative
            if ``True``, negative infinity is detected.
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
            a container containing the test result. An element ``out_i`` is ``True``
            if ``self_i`` is either positive or negative infinity and ``False``
            otherwise. The returned array must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([-1, -float('inf'), 1.23]),
        ...                   b=startai.array([float('inf'), 3.3, -4.2]))
        >>> z = x.isinf()
        >>> print(z)
        {
            a: startai.array([False, True, False]),
            b: startai.array([True, False, False])
        }
        """
        return self._static_isinf(
            self,
            detect_positive=detect_positive,
            detect_negative=detect_negative,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_isnan(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.isnan. This method simply
        wraps the function, and so the docstring for startai.isnan also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued data type.
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
            a container containing the test result. An element ``out_i`` is ``True``
            if ``x_i`` is ``NaN`` and ``False`` otherwise.
            The returned array should have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([-1, -float('nan'), 1.23]),
        ...                   b=startai.array([float('nan'), 3.3, -4.2]))
        >>> z = startai.Container.static_isnan(x)
        >>> print(z)
        {
            a: startai.array([False, True, False]),
            b: startai.array([True, False, False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "isnan",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def isnan(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.isnan. This method
        simply wraps the function, and so the docstring for startai.isnan also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued data type.
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
            a container containing the test result. An element ``out_i`` is ``True``
            if ``self_i`` is ``NaN`` and ``False`` otherwise.
            The returned array should have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1, -float('nan'), 1.23]),
        ...                   b=startai.array([float('nan'), 3.3, -4.2]))
        >>> y = x.isnan()
        >>> print(y)
        {
            a: startai.array([False, True, False]),
            b: startai.array([True, False, False])
        }
        """
        return self._static_isnan(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_less(
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
        """startai.Container static method variant of startai.less. This method simply
        wraps the function, and so the docstring for startai.less also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = startai.Container.static_less(y,x)
        >>> print(z)
        {
            a: startai.array([True, True, True]),
            b: startai.array([False, False, False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "less",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def less(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.less. This method
        simply wraps the function, and so the docstring for startai.less also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([4, 5, 6]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([5, 6, 7]))
        >>> z = x.less(y)
        >>> print(z)
        {
            a: startai.array([False, False, False]),
            b: startai.array([True, True, True])
        }
        """
        return self._static_less(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_less_equal(
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
        """startai.Container static method variant of startai.less_equal. This method
        simply wraps the function, and so the docstring for startai.less_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        With :code:'startai.Container' inputs:

        >>> x1 = startai.Container(a=startai.array([12, 3.5, 9.2]), b=startai.array([2., 1.1, 5.5]))
        >>> x2 = startai.Container(a=startai.array([12, 2.2, 4.1]), b=startai.array([1, 0.7, 3.8]))
        >>> y = startai.Container.static_less_equal(x1, x2)
        >>> print(y)
        {
            a: startai.array([True, False, False]),
            b: startai.array([False, False, False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "less_equal",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def less_equal(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.less_equal. This method
        simply wraps the function, and so the docstring for startai.less_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        With :code:'startai.Container' inputs:

        >>> x1 = startai.Container(a=startai.array([12, 3.5, 9.2]), b=startai.array([2., 1.1, 5.5]))
        >>> x2 = startai.Container(a=startai.array([12, 2.2, 4.1]), b=startai.array([1, 0.7, 3.8]))
        >>> y = x1.less_equal(x2)
        >>> print(y)
        {
            a: startai.array([True, False, False]),
            b: startai.array([False, False, False])
        }

        With mixed :code:'startai.Container' and :code:'startai.Array' inputs:

        >>> x1 = startai.Container(a=startai.array([12., 3.5, 9.2]), b=startai.array([2., 1., 5.5]))
        >>> x2 = startai.array([2., 1.1, 5.5])
        >>> y = x1.less_equal(x2)
        >>> print(y)
        {
            a: startai.array([False, False, False]),
            b: startai.array([True, True, True])
        }
        """
        return self._static_less_equal(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_log(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.log. This method simply
        wraps the function, and so the docstring for startai.log also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the log for each element in ``x``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0.0, float('nan')]),
        ...                   b=startai.array([-0., -3.9, float('+inf')]),
        ...                   c=startai.array([7.9, 1.1, 1.]))
        >>> y = startai.Container.static_log(x)
        >>> print(y)
        {
            a: startai.array([-inf, nan]),
            b: startai.array([-inf, nan, inf]),
            c: startai.array([2.07, 0.0953, 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "log",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def log(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.log. This method simply
        wraps the function, and so the docstring for startai.log also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the log for each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Container` instance method:

        >>> x = startai.Container(a=startai.array([0.0, float('nan')]),
        ...                   b=startai.array([-0., -3.9, float('+inf')]),
        ...                   c=startai.array([7.9, 1.1, 1.]))
        >>> y = x.log()
        >>> print(y)
        {
            a: startai.array([-inf, nan]),
            b: startai.array([-inf, nan, inf]),
            c: startai.array([2.07, 0.0953, 0.])
        }
        """
        return self._static_log(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_log1p(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.log1p. This method simply
        wraps the function, and so the docstring for startai.log1p also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the evaluated result for each element in ``x``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.1]))
        >>> y = startai.Container.static_log1p(x)
        >>> print(y)
        {
            a: startai.array([0., 0.693, 1.1]),
            b: startai.array([1.39, 1.61, 1.81])
        }

        >>> x = startai.Container(a=startai.array([0., 2.]), b=startai.array([ 4., 5.1]))
        >>> startai.Container.static_log1p(x, out = x)
        >>> print(y)
        {
            a: startai.array([0., 0.693, 1.1]),
            b: startai.array([1.39, 1.61, 1.81])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "log1p",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def log1p(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.log1p. This method
        simply wraps the function, and so the docstring for startai.log1p also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.6, 2.6, 3.5]),
        ...                   b=startai.array([4.5, 5.3, 2.3]))
        >>> y = x.log1p()
        >>> print(y)
        {
            a: startai.array([0.956, 1.28, 1.5]),
            b: startai.array([1.7, 1.84, 1.19])
        }
        """
        return self._static_log1p(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_log2(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.log2. This method simply
        wraps the function, and so the docstring for startai.log2 also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the evaluated base ``2`` logarithm for
            each element in ``x``. The returned array must have a real-valued
            floating-point data type determined by :ref:`type-promotion`.

        Examples
        --------
        Using :code:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0.0, float('nan')]),\
                              b=startai.array([-0., -4.9, float('+inf')]),\
                              c=startai.array([8.9, 2.1, 1.]))
        >>> y = startai.Container.static_log2(x)
        >>> print(y)
        {
            a: startai.array([-inf, nan]),
            b: startai.array([-inf, nan, inf]),
            c: startai.array([3.15, 1.07, 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "log2",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def log2(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.log2. This method
        simply wraps the function, and so the docstring for startai.log2 also
        applies to this metho with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the evaluated base ``2`` logarithm for each
            element in ``self``. The returned array must have a real-valued
            floating-point data type determined by :ref:`type-promotion`.

        Examples
        --------
        Using :code:`startai.Container` instance method:

        >>> x = startai.Container(a=startai.array([0.0, float('nan')]),
        ...                   b=startai.array([-0., -5.9, float('+inf')]),
        ...                   c=startai.array([8.9, 2.1, 1.]))
        >>> y = startai.log2(x)
        >>> print(y)
        {
            a: startai.array([-inf, nan]),
            b: startai.array([-inf, nan, inf]),
            c: startai.array([3.15, 1.07, 0.])
        }
        """
        return self._static_log2(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_log10(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.log10. This method simply
        wraps the function, and so the docstring for startai.log10 also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the evaluated base ``10`` logarithm for each
            element in ``x``. The returned array must have a real-valued
            floating-point data type determined by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0.0, float('nan')]),
        ...                   b=startai.array([-0., -3.9, float('+inf')]),
        ...                   c=startai.array([7.9, 1.1, 1.]))
        >>> y = startai.Container.static_log10(x)
        >>> print(y)
        {
            a: startai.array([-inf, nan]),
            b: startai.array([-inf, nan, inf]),
            c: startai.array([0.898, 0.0414, 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "log10",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def log10(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.log10. This method
        simply wraps the function, and so the docstring for startai.log10 also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the evaluated base ``10`` logarithm for
            each element in ``self``. The returned array must have a real-valued
            floating-point data type determined by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Container` instance method:

        >>> x = startai.Container(a=startai.array([0.0, float('nan')]),
        ...                   b=startai.array([-0., -3.9, float('+inf')]),
        ...                   c=startai.array([7.9, 1.1, 1.]))
        >>> y = x.log10()
        >>> print(y)
        {
            a: startai.array([-inf, nan]),
            b: startai.array([-inf, nan, inf]),
            c: startai.array([0.898, 0.0414, 0.])
        }
        """
        return self._static_log10(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_logaddexp(
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
        """startai.Container static method variant of startai.greater_equal. This
        method simply wraps the function, and so the docstring for
        startai.greater_equal also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a real-valued floating-point data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([4., 5., .]),
        ...                   b=startai.array([2., 3., 4.]))
        >>> y = startai.Container(a=startai.array([1., 2., 3.]),
        ...                   b=startai.array([5., 6., 7.]))
        >>> z = startai.Container.static_logaddexp(y,x)
        >>> print(z)
        {
            a: startai.array([4.05, 5.05, 6.05]),
            b: startai.array([5.05, 6.05, 7.05])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "logaddexp",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def logaddexp(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.greater_equal. This
        method simply wraps the function, and so the docstring for
        startai.greater_equal also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a real-valued floating-point data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([4., 5., 6.]),
        ...                   b=startai.array([2., 3., 4.]))
        >>> y = startai.Container(a=startai.array([1., 2., 3.]),
        ...                   b=startai.array([5., 6., 7.]))
        >>> z = startai.logaddexp(y,x)
        >>> print(z)
        {
            a: startai.array([4.05, 5.05, 6.05]),
            b: startai.array([5.05, 6.05, 7.05])
        }
        """
        return self._static_logaddexp(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_logaddexp2(
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
        """startai.Container static method variant of startai.logaddexp2. This method
        simply wraps the function, and so the docstring for startai.logaddexp2 also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            first input container with array-like items.
        x2
            second input container with array-like items.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise logaddexp2 of input arrays.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1, 2, 3]),\
                               b=startai.array([1, 2, 3]))
        >>> x2 = startai.Container(a=startai.array([4, 5, 6]),\
                               b=5)
        >>> startai.Container.static_logaddexp2(x1, x2)
        {
            a: startai.array([4.169925, 5.169925, 6.169925])
            b: startai.array([5.08746284, 5.169925  , 5.32192809])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "logaddexp2",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def logaddexp2(
        self: startai.Container,
        x2: startai.Container,
        /,
        *,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.logaddexp2. This method
        simply wraps the function, and so the docstring for startai.logaddexp2 also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input container with array-like items.
        x2
            second input container with array-like items.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            Container including arrays with element-wise logaddexp2 of input arrays.

        Examples
        --------
        >>> x1 = startai.Container(a=startai.array([1, 2, 3]),\
                               b=startai.array([1, 2, 3]))
        >>> x2 = startai.Container(a=startai.array([4, 5, 6]),\
                               b=5)
        >>> x1.logaddexp2(x2)
        {
            a: startai.array([4.169925, 5.169925, 6.169925])
            b: startai.array([5.08746284, 5.169925  , 5.32192809])
        }
        """
        return self.static_logaddexp2(self, x2, out=out)

    @staticmethod
    def _static_logical_and(
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
        """startai.Container static method variant of startai.logical_and. This method
        simply wraps the function, and so the docstring for startai.logical_and
        also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a boolean data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        Using 'startai.Container' instance

        >>> a = startai.Container(a=startai.array([True, False, True, False]))
        >>> b = startai.Container(a=startai.array([True, True, False, False]))
        >>> w = startai.Container.static_logical_and(a, b)
        >>> print(w)
        {
            a:startai.array([True,False,False,False])
        }

        >>> j = startai.Container(a=startai.array([True, True, False, False]))
        >>> m = startai.array([False, True, False, True])
        >>> x = startai.Container.static_logical_and(j, m)
        >>> print(x)
        {
            a:startai.array([False,True,False,False])
        }


        >>> k = startai.Container(a=startai.array([True, False, True]),
        ...                   b=startai.array([True, False, False]))
        >>> l = startai.Container(a=startai.array([True, True, True]),
        ...                   b=startai.array([False, False, False]))
        >>> z = startai.Container.static_logical_and(k, l)
        >>> print(z)
        {
            a:startai.array([True,False,True]),
            b:startai.array([False,False,False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "logical_and",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def logical_and(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.logical_and. This
        method simply wraps the function, and so the docstring for
        startai.logical_and also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a boolean data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        Using 'startai.Container' instance

        >>> a = startai.Container(a=startai.array([True, False, True, False]))
        >>> b = startai.Container(a=startai.array([True, True, False, False]))
        >>> w = a.logical_and(b)
        >>> print(w)
        {
            a:startai.array([True,False,False,False])
        }

        >>> j = startai.Container(a=startai.array([True, True, False, False]))
        >>> m = startai.array([False, True, False, True])
        >>> x = j.logical_and(m)
        >>> print(x)
        {
            a:startai.array([False,True,False,False])
        }

        >>> k = startai.Container(a=startai.array([True, False, True]),
        ...                   b=startai.array([True, False, False]))
        >>> l = startai.Container(a=startai.array([True, True, True]),
        ...                   b=startai.array([False, False, False]))
        >>> z = k.logical_and(l)
        >>> print(z)
        {
            a:startai.array([True,False,True]),
            b:startai.array([False,False,False])
        }
        """
        return self._static_logical_and(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_logical_not(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.logical_not. This method
        simply wraps the function, and so the docstring for startai.logical_not
        also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a boolean data type.
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
            a container containing the evaluated result for each element in ``x``.
            The returned container must have a data type of ``bool``.

        Examples
        --------
        Using 'startai.Container' instance

        >>> x=startai.Container(a=startai.array([1,0,0,1]), b=startai.array([3,1,7,0]))
        >>> startai.Container.static_logical_not(x)
        {
            a: startai.array([False, True, True, False]),
            b: startai.array([False, False, False, True])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "logical_not",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def logical_not(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.logical_not. This
        method simply wraps the function, and so the docstring for
        startai.logical_not also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a boolean data type.
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
            a container containing the evaluated result for each element in ``self``.
            The returned container must have a data type of ``bool``.

        Examples
        --------
        Using 'startai.Container' instance

        >>> x=startai.Container(a=startai.array([1,0,0,1]), b=startai.array([3,1,7,0]))
        >>> y = x.logical_not()
        >>> print(y)
        {
            a: startai.array([False, True, True, False]),
            b: startai.array([False, False, False, True])
        }

        >>> x=startai.Container(a=startai.array([1,0,1,0]), b=startai.native_array([5,2,0,3]))
        >>> y = x.logical_not()
        >>> print(y)
        {
            a: startai.array([False, True, False, True]),
            b: startai.array([False, False, True, False])
        }
        """
        return self._static_logical_not(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_logical_or(
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
        """startai.Container static method variant of startai.logical_or. This method
        simply wraps the function, and so the docstring for startai.logical_or also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a boolean data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([False, False, True]),
        ...                   b=startai.array([True, False, True]))
        >>> y = startai.Container(a=startai.array([False, True, False]),
        ...                   b=startai.array([True, True, False]))
        >>> z = startai.Container.static_logical_or(x, y)
        >>> print(z)
        {
            a: startai.array([False, True, True]),
            b: startai.array([True, True, True])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "logical_or",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def logical_or(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.logical_or. This method
        simply wraps the function, and so the docstring for startai.logical_or also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a boolean data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        This function conforms to the `Array API Standard
        <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of
        the `docstring <https://data-apis.org/array-api/latest/
        API_specification/generated/array_api.logical_or.html>`_
        in the standard.

        Both the description and the type hints above assumes an array input for
        simplicity, but this function is *nestable*, and therefore also
        accepts :class:`startai.Container` instances in place of any of the arguments.

        Examples
        --------
        Using :class:`startai.Container` instance method:

        >>> x = startai.Container(a=startai.array([False,True,True]),
        ...                   b=startai.array([3.14, 2.718, 1.618]))
        >>> y = startai.Container(a=startai.array([0, 5.2, 0.8]), b=startai.array([0.2, 0, 0.9]))
        >>> z = x.logical_or(y)
        >>> print(z)
        {
            a: startai.array([False, True, True]),
            b: startai.array([True, True, True])
        }
        """
        return self._static_logical_or(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_logical_xor(
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
        """startai.Container static method variant of startai.logical_xor. This method
        simply wraps the function, and so the docstring for startai.logical_xor
        also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a boolean data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.array([0,0,1,1,0])
        >>> y = startai.Container(a=startai.array([1,0,0,1,0]), b=startai.array([1,0,1,0,0]))
        >>> z = startai.Container.static_logical_xor(x, y)
        >>> print(z)
        {
            a: startai.array([True, False, True, False, False]),
            b: startai.array([True, False, False, True, False])
        }

        With multiple :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([1,0,0,1,0]), b=startai.array([1,0,1,0,0]))
        >>> y = startai.Container(a=startai.array([0,0,1,1,0]), b=startai.array([1,0,1,1,0]))
        >>> z = startai.Container.static_logical_xor(x, y)
        >>> print(z)
        {
            a: startai.array([True, False, True, False, False]),
            b: startai.array([False, False, False, True, False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "logical_xor",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def logical_xor(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.logical_xor. This
        method simply wraps the function, and so the docstring for
        startai.logical_xor also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a boolean data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1,0,0,1,0]), b=startai.array([1,0,1,0,0]))
        >>> y = startai.Container(a=startai.array([0,0,1,1,0]), b=startai.array([1,0,1,1,0]))
        >>> z = x.logical_xor(y)
        >>> print(z)
        {
            a: startai.array([True, False, True, False, False]),
            b: startai.array([False, False, False, True, False])
        }
        """
        return self._static_logical_xor(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_multiply(
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
        """startai.Container static method variant of startai.multiply. This method
        simply wraps the function, and so the docstring for startai.multiply also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :code:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([15., 4.5, 6.5]),\
                               b=startai.array([3.2, 5., 7.5]))
        >>> x2 = startai.Container(a=startai.array([1.7, 2.8, 3.]),\
                               b=startai.array([5.6, 1.2, 4.2]))
        >>> y =startai.Container.static_multiply(x1, x2)
        >>> print(y)
        {
            a: startai.array([25.5, 12.6, 19.5]),
            b: startai.array([17.9, 6., 31.5])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "multiply",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def multiply(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.multiply. This method
        simply wraps the function, and so the docstring for startai.multiply also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array or container. Should have a numeric data type.
        x2
            second input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a nuneric data type.
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
            a container containing the element-wise products.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :code:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([15., 4.5, 6.5]),\
                               b=startai.array([3.2, 5., 7.5]))
        >>> x2 = startai.Container(a=startai.array([1.7, 2.8, 3.]),\
                               b=startai.array([5.6, 1.2, 4.2]))
        >>> y = startai.Container.multiply(x1, x2)
        >>> print(y)
        {
            a: startai.array([25.5, 12.6, 19.5]),
            b: startai.array([17.9, 6., 31.5])
        }

        With mixed :code:`startai.Container` and :code:`startai.Array` inputs:

        >>> x1 = startai.Container(a=startai.array([6.2, 4.8, 2.3]),\
                               b=startai.array([5., 1.7, 0.1]))
        >>> x2 = startai.array([8.3, 3.2, 6.5])
        >>> y = startai.Container.multiply(x1, x2)
        >>> print(y)
        {
            a: startai.array([51.5, 15.4, 14.9]),
            b: startai.array([41.5, 5.44, 0.65])
        }
        """
        return self._static_multiply(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_negative(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.negative. This method
        simply wraps the function, and so the docstring for startai.negative also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a numeric data type.
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
            a container containing the evaluated result for each element in ``x``.
            The returned container must have the same data type as ``x``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., 1., 2.]),
        ...                   b=startai.array([3., 4., -5.]))
        >>> y = startai.Container.static_negative(x)
        >>> print(y)
        {
            a: startai.array([-0., -1., -2.]),
            b: startai.array([-3., -4., 5.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "negative",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def negative(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.negative. This method
        simply wraps the function, and so the docstring for startai.negative also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a numeric data type.
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
            a container containing the evaluated result for each element in ``self``.
            The returned container must have the same data type as ``self``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., 1., 2.]),
        ...                   b=startai.array([3., 4., -5.]))
        >>> y = x.negative()
        >>> print(y)
        {
            a: startai.array([-0., -1., -2.]),
            b: startai.array([-3., -4., 5.])
        }
        """
        return self._static_negative(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_not_equal(
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
        """startai.Container static method variant of startai.not_equal. This method
        simply wraps the function, and so the docstring for startai.not_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. May have any data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            May have any data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([12, 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> x2 = startai.Container(a=startai.array([12, 2.3, 3]), b=startai.array([2.4, 3., 2.]))
        >>> y = startai.Container.static_not_equal(x1, x2)
        >>> print(y)
        {
            a: startai.array([False, True, True]),
            b: startai.array([True, True, True])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "not_equal",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def not_equal(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.not_equal. This method
        simply wraps the function, and so the docstring for startai.not_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. May have any data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            May have any data type.
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
            a container containing the element-wise results. The returned container
            must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([12, 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> x2 = startai.Container(a=startai.array([12, 2.3, 3]), b=startai.array([2.4, 3., 2.]))
        >>> y = x1.not_equal(x2)
        >>> print(y)
        {
            a: startai.array([False, True, True]),
            b: startai.array([True, True, True])
        }

        With mixed :class:`startai.Container` and :class:`startai.Array` inputs:

        >>> x1 = startai.Container(a=startai.array([12., 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> x2 = startai.array([3., 1., 0.9])
        >>> y = x1.not_equal(x2)
        >>> print(y)
        {
            a: startai.array([True, True, True]),
            b: startai.array([False, False, False])
        }
        """
        return self._static_not_equal(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_positive(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.positive. This method
        simply wraps the function, and so the docstring for startai.positive also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a numeric data type.
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
            a container containing the evaluated result for each element in ``x``.
            The returned container must have the same data type as ``x``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., 1., 2.]),
        ...                   b=startai.array([3., 4., -5.]))
        >>> y = startai.Container.static_positive(x)
        >>> print(y)
        {
            a: startai.array([0., 1., 2.]),
            b: startai.array([3., 4., -5.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "positive",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def positive(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.positive. This method
        simply wraps the function, and so the docstring for startai.positive also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a numeric data type.
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
            a container containing the evaluated result for each element in ``self``.
            The returned container must have the same data type as ``self``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., 1., 2.]),
        ...                   b=startai.array([3., 4., -5.]))
        >>> y = startai.positive(x)
        >>> print(y)
        {
            a: startai.array([0., 1., 2.]),
            b: startai.array([3., 4., -5.])
        }
        """
        return self._static_positive(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_pow(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        x2: Union[int, float, startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.pow. This method simply
        wraps the function, and so the docstring for startai.pow also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a data type determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0, 1]), b=startai.array([2, 3]))
        >>> y = startai.Container.static_pow(x, 2)
        >>> print(y)
        {
            a: startai.array([0, 1]),
            b: startai.array([4, 9])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "pow",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def pow(
        self: startai.Container,
        x2: Union[int, float, startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.pow. This method simply
        wraps the function, and so the docstring for startai.pow also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results. The returned container
            must have a data type determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0, 1]), b=startai.array([2, 3]))
        >>> y = x.pow(3)
        >>> print(y)
        {
            a:startai.array([0,1]),
            b:startai.array([8,27])
        }
        """
        return self._static_pow(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_real(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.real. This method simply
        wraps the function, and so the docstring for startai.real also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the test result. An element ``out_i`` is ``out_i``
            if ``x_i`` is real number part only else ``real number part``,
            if it contains real and complex part both.
            The returned array should have a data type of ``float``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1+5j, 0-0j, 1.23j]),
        ...                   b=startai.array([7.9, 0.31+3.3j, -4.2-5.9j]))
        >>> z = startai.Container.static_real(x)
        >>> print(z)
        {
            a: startai.array([-1., 0., 0.]),
            b: startai.array([7.9, 0.31, -4.2])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "real",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def real(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.real. This method
        simply wraps the function, and so the docstring for startai.real also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the test result.
            An element ``out_i`` is ``self_i`` if ``self_i`` is real number
            else ``took real number part only`` if ``self_i``
            contains real number and complex number both.
            The returned array should have a data type of ``float``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1j, 0.335+2.345j, 1.23+7j]),\
                          b=startai.array([0.0, 1.2+3.3j, 1+0j]))
        >>> x.real()
        {
            a: startai.array([0., 0.335, 1.23]),
            b: startai.array([0.0, 1.2, 1.])
        }
        """
        return self.static_real(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_remainder(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        x2: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        modulus: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.remainder. This method
        simply wraps the function, and so the docstring for startai.remainder also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        modulus
            whether to compute the modulus instead of the remainder.
            Default is ``True``.
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
            a container containing the element-wise results. The returned container
            must have the same sign as the respective element ``x2_i``.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([2., 3., 5.]), b=startai.array([2., 2., 4.]))
        >>> x2 = startai.Container(a=startai.array([1., 3., 4.]), b=startai.array([1., 3., 3.]))
        >>> y = startai.Container.static_remainder(x1, x2)
        >>> print(y)
        {
            a: startai.array([0., 0., 1.]),
            b: startai.array([0., 2., 1.])
        }

        With mixed :class:`startai.Container` and `startai.Array` inputs:

        >>> x1 = startai.Container(a=startai.array([2., 3., 5.]), b=startai.array([2., 2., 4.]))
        >>> x2 = startai.array([1., 2., 3.])
        >>> y = startai.Container.static_remainder(x1, x2)
        >>> print(y)
        {
            a: startai.array([0., 1., 2.]),
            b: startai.array([0., 0., 1.])
        }

        With mixed :class:`startai.Container` and `startai.NativeArray` inputs:

        >>> x1 = startai.Container(a=startai.array([2., 3., 5.]), b=startai.array([2., 2., 4.]))
        >>> x2 = startai.native_array([1., 2., 3.])
        >>> y = startai.Container.static_remainder(x1, x2)
        >>> print(y)
        {
            a: startai.array([0., 1., 2.]),
            b: startai.array([0., 0., 1.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "remainder",
            x1,
            x2,
            modulus=modulus,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def remainder(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        modulus: Union[bool, startai.Container] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.remainder. This method
        simply wraps the function, and so the docstring for startai.remainder also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array or container. Should have a real-valued data type.
        x2
            input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        modulus
            whether to compute the modulus instead of the remainder.
            Default is ``True``.
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
            a container containing the element-wise results. The returned container
            must have the same sign as the respective element ``x2_i``.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([2., 3., 5.]), b=startai.array([2., 2., 4.]))
        >>> x2 = startai.Container(a=startai.array([1., 3., 4.]), b=startai.array([1., 3., 3.]))
        >>> y = x1.remainder(x2)
        >>> print(y)
        {
            a: startai.array([0., 0., 1.]),
            b: startai.array([0., 2., 1.])
        }

        With mixed :class:`startai.Container` and `startai.Array` inputs:

        >>> x1 = startai.Container(a=startai.array([2., 3., 5.]), b=startai.array([2., 2., 4.]))
        >>> x2 = startai.array([1., 2., 3.])
        >>> y = x1.remainder(x2)
        >>> print(y)
        {
            a: startai.array([0., 1., 2.]),
            b: startai.array([0., 0., 1.])
        }

        With mixed :class:`startai.Container` and `startai.NativeArray` inputs:

        >>> x1 = startai.Container(a=startai.array([2., 3., 5.]), b=startai.array([2., 2., 4.]))
        >>> x2 = startai.native_array([1., 2., 3.])
        >>> y = x1.remainder(x2)
        >>> print(y)
        {
            a: startai.array([0., 1., 2.]),
            b: startai.array([0., 0., 1.])
        }
        """
        return self._static_remainder(
            self,
            x2,
            modulus=modulus,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_round(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        decimals: Union[int, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.round. This method simply
        wraps thevfunction, and so the docstring for startai.round also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a numeric data type.
        decimals
            number of decimal places to round to. Default is ``0``.
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
            a container containing the rounded result for each element in ``x``.
            The returned container must have the same data type as ``x``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([4.20, 8.6, 6.90, 0.0]),
        ...                   b=startai.array([-300.9, -527.3, 4.5]))
        >>> y = startai.Container.static_round(x)
        >>> print(y)
        {
            a: startai.array([4., 9., 7., 0.]),
            b: startai.array([-301., -527., 4.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "round",
            x,
            decimals=decimals,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def round(
        self: startai.Container,
        *,
        decimals: Union[int, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.round. This method
        simply wraps the function, and so the docstring for startai.round also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a numeric data type.
        decimals
            number of decimal places to round to. Default is ``0``.
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
            a container containing the rounded result for each element in ``self``.
            The returned container must have the same data type as ``self``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([4.20, 8.6, 6.90, 0.0]),
        ...                   b=startai.array([-300.9, -527.3, 4.5]))
        >>> y = x.round()
        >>> print(y)
        {
            a: startai.array([4., 9., 7., 0.]),
            b: startai.array([-301., -527., 4.])
        }
        """
        return self._static_round(
            self,
            decimals=decimals,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_sign(
        x: Union[float, startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        np_variant: Optional[Union[bool, startai.Container]] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.sign. This method simply
        wraps the function, and so the docstring for startai.sign also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a numeric data type.
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
            a container containing the evaluated result for each element in ``x``.
            The returned container must have the same data type as ``x``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, -1., 6.6]),
        ...                   b=startai.array([-14.2, 8.3, 0.1, -0]))
        >>> y = startai.Container.static_sign(x)
        >>> print(y)
        {
            a: startai.array([0., -1., 1.]),
            b: startai.array([-1., 1., 1., 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "sign",
            x,
            np_variant=np_variant,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def sign(
        self: startai.Container,
        *,
        np_variant: Optional[Union[bool, startai.Container]] = True,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.sign. This method
        simply wraps the function, and so the docstring for startai.sign also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a numeric data type.
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
            a container containing the evaluated result for each element in ``self``.
            The returned container must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-6.7, 2.4, -8.5]),
        ...                   b=startai.array([1.5, -0.3, 0]),
        ...                   c=startai.array([-4.7, -5.4, 7.5]))
        >>> y = x.sign()
        >>> print(y)
        {
            a: startai.array([-1., 1., -1.]),
            b: startai.array([1., -1., 0.]),
            c: startai.array([-1., -1., 1.])
        }
        """
        return self._static_sign(
            self,
            np_variant=np_variant,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_sin(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.sin. This method simply
        wraps the function, and so the docstring for startai.sin also applies to
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
            a container containing the sine of each element in ``x``. The returned
            container must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1., -2., -3.]),
        ...                   b=startai.array([4., 5., 6.]))
        >>> y = startai.Container.static_sin(x)
        >>> print(y)
        {
            a: startai.array([-0.841, -0.909, -0.141]),
            b: startai.array([-0.757, -0.959, -0.279])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "sin",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def sin(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.sin. This method simply
        wraps the function, and so the docstring for startai.sin also applies to
        this method with minimal changes.

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
            a container containing the sine of each element in ``self``.
            The returned container must have a floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., 2., 3.]),
        ...                   b=startai.array([-4., -5., -6.]))
        >>> y = x.sin()
        >>> print(y)
        {
            a: startai.array([0.841, 0.909, 0.141]),
            b: startai.array([0.757, 0.959, 0.279])
        }
        """
        return self._static_sin(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_sinh(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.sinh. This method simply
        wraps the function, and so the docstring for startai.sinh also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container whose elements each represent a hyperbolic angle.
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
            an container containing the hyperbolic sine of each element in ``x``.
            The returned container must have a floating-point data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1, 0.23, 1.12]), b=startai.array([1, -2, 0.76]))
        >>> y = startai.Container.static_sinh(x)
        >>> print(y)
        {
            a: startai.array([-1.18, 0.232, 1.37]),
            b: startai.array([1.18, -3.63, 0.835])
        }

        >>> x = startai.Container(a=startai.array([-3, 0.34, 2.]),
        ...                   b=startai.array([0.67, -0.98, -3]))
        >>> y = startai.Container(a=startai.zeros(1), b=startai.zeros(1))
        >>> startai.Container.static_sinh(x, out=y)
        >>> print(y)
        {
            a: startai.array([-10., 0.347, 3.63]),
            b: startai.array([0.721, -1.14, -10.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "sinh",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def sinh(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.sinh. This method
        simply wraps the function, and so the docstring for startai.sinh also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container whose elements each represent a hyperbolic angle.
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
            an container containing the hyperbolic sine of each element in ``self``.
            The returned container must have a floating-point data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1, 0.23, 1.12]), b=startai.array([1, -2, 0.76]))
        >>> y = x.sinh()
        >>> print(y)
        {
            a: startai.array([-1.18, 0.232, 1.37]),
            b: startai.array([1.18, -3.63, 0.835])
        }

        >>> x = startai.Container(a=startai.array([-3, 0.34, 2.]),
        ...                   b=startai.array([0.67, -0.98, -3]))
        >>> y = startai.Container(a=startai.zeros(3), b=startai.zeros(3))
        >>> x.sinh(out=y)
        >>> print(y)
        {
            a: startai.array([-10., 0.347, 3.63]),
            b: startai.array([0.721, -1.14, -10.])
        }
        """
        return self._static_sinh(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_square(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.square. This method
        simply wraps the function, and so the docstring for startai.square also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the square of each element in ``x``.
            The returned container must have a real-valued floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, 1]), b=startai.array([2, 3]))
        >>> y = startai.Container.static_square(x)
        >>> print(y)
        {
            a:startai.array([0,1]),
            b:startai.array([4,9])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "square",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def square(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.square. This method
        simply wraps the function, and so the docstring for startai.square also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the square of each element in ``self``.
            The returned container must have a real-valued floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0, 1]), b=startai.array([2, 3]))
        >>> y = x.square()
        >>> print(y)
        {
            a:startai.array([0,1]),
            b:startai.array([4,9])
        }
        """
        return self._static_square(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_sqrt(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.sqrt. This method simply
        wraps the function, and so the docstring for startai.sqrt also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued floating-point data type.
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
            a container containing the square root of each element in ``x``.
            The returned container must have a real-valued floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        with :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., 100., 27.]),
        ...                   b=startai.native_array([93., 54., 25.]))
        >>> y = startai.Container.static_sqrt(x)
        >>> print(y)
        {
            a: startai.array([0., 10., 5.2]),
            b: startai.array([9.64, 7.35, 5.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "sqrt",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def sqrt(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.sqrt. This method
        simply wraps the function, and so the docstring for startai.sqrt also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued floating-point data type.
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
            a container containing the square root of each element in
            ``self``. The returned container must have a real-valued
            floating-point data type determined by :ref:`type-promotion`.

        Examples
        --------
        with :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([0., 100., 27.]),
        ...                   b=startai.native_array([93., 54., 25.]))
        >>> y = x.sqrt()
        >>> print(y)
        {
            a: startai.array([0., 10., 5.2]),
            b: startai.array([9.64, 7.35, 5.])
        }
        """
        return self._static_sqrt(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_subtract(
        x1: Union[startai.Array, startai.NativeArray, startai.Container],
        x2: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        alpha: Optional[Union[int, float, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.subtract. This method
        simply wraps the function, and so the docstring for startai.subtract also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            first input array or container. Should have a numeric data type.
        x2
            second input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`). Should have a numeric data type.
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
        alpha
            optional scalar multiplier for ``x2``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the element-wise sums.
            The returned container must have a data type determined
            by :ref:`type-promotion`.


        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([4, 1, 3]),
        ...                   b=startai.array([1, -1, 0]))
        >>> z = startai.Container.static_subtract(x, y)
        >>> print(z)
        {
            a: startai.array([-3, 1, 0]),
            b: startai.array([1, 4, 4])
        }

        >>> z = startai.Container.static_subtract(x, y, alpha=3)
        >>> print(z)
        {
            a: startai.array([-11, -1, -6]),
            b: startai.array([-1, 6, 4])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "subtract",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            alpha=alpha,
            out=out,
        )

    def subtract(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        alpha: Optional[Union[int, float, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.subtract. This method
        simply wraps the function, and so the docstring for startai.subtract also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array or container. Should have a numeric data type.
        x2
            second input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.
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
        alpha
            optional scalar multiplier for ``x2``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the element-wise sums.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 3]),
        ...                   b=startai.array([2, 3, 4]))
        >>> y = startai.Container(a=startai.array([4, 1, 3]),
        ...                   b=startai.array([1, -1, 0]))
        >>> z = x.subtract(y)
        >>> print(z)
        {
            a: startai.array([-3, 1, 0]),
            b: startai.array([1, 4, 4])
        }

        >>> z = x.subtract(y, alpha=3)
        >>> print(z)
        {
            a: startai.array([-11, -1, -6]),
            b: startai.array([-1, 6, 4])
        }
        """
        return self._static_subtract(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            alpha=alpha,
            out=out,
        )

    @staticmethod
    def _static_tan(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.tan. This method simply
        wraps the function, and so the docstring for startai.tan also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input array whose elements are expressed in radians. Should have a
            floating-point data type.
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
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the tangent of each element in ``x``.
            The return must have a floating-point data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.]))
        >>> y = startai.Container.static_tan(x)
        >>> print(y)
        {
            a: startai.array([0., 1.56, -2.19]),
            b: startai.array([-0.143, 1.16, -3.38])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "tan",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def tan(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.tan. This method simply
        wraps the function, and so the docstring for startai.tan also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements are expressed in radians. Should have a
            floating-point data type.
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
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            a container containing the tangent of each element in ``self``.
            The return must have a floating-point data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.]))
        >>> y = x.tan()
        >>> print(y)
        {
            a:startai.array([0., 1.56, -2.19]),
            b:startai.array([-0.143, 1.16, -3.38])
        }
        """
        return self._static_tan(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_tanh(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.tanh. This method simply
        wraps the function, and so the docstring for startai.tanh also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container whose elements each represent a hyperbolic angle.
            Should have a real-valued floating-point data type.
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
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the hyperbolic tangent of each element in ``x``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([3., 4., 5.]))
        >>> y = startai.Container.static_tanh(x)
        >>> print(y)
        {
            a: startai.array([0., 0.76, 0.96]),
            b: startai.array([0.995, 0.999, 0.9999])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "tanh",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            complex_mode=complex_mode,
            out=out,
        )

    def tanh(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.tanh. This method
        simply wraps the function, and so the docstring for startai.tanh also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container whose elements each represent a hyperbolic angle.
            Should have a real-valued floating-point data type.
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
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container containing the hyperbolic tangent of each element in
            ``self``. The returned container must have a real-valued floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0., 1., 2.]),
        ...                   b=startai.array([3., 4., 5.]))
        >>> y = x.tanh()
        >>> print(y)
        {
            a:startai.array([0., 0.762, 0.964]),
            b:startai.array([0.995, 0.999, 1.])
        }
        """
        return self._static_tanh(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            complex_mode=complex_mode,
            out=out,
        )

    @staticmethod
    def _static_trunc(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.trunc. This method simply
        wraps the function, and so the docstring for startai.trunc also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued data type.
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
            a container containing the rounded result for each element in ``x``.
            The returned container must have the same data type as ``x``.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x = startai.Container(a=startai.array([-0.25, 4, 1.3]),
        ...                   b=startai.array([12, -3.5, 1.234]))
        >>> y = startai.Container.static_trunc(x)
        >>> print(y)
        {
            a: startai.array([-0., 4., 1.]),
            b: startai.array([12., -3., 1.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "trunc",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def trunc(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.trunc. This method
        simply wraps the function, and so the docstring for startai.trunc also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued data type.
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
            a container containing the rounded result for each element in ``self``.
            The returned container must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-0.25, 4, 1.3]),
        ...                   b=startai.array([12, -3.5, 1.234]))
        >>> y = x.trunc()
        >>> print(y)
        {
            a: startai.array([-0., 4., 1.]),
            b: startai.array([12., -3., 1.])
        }
        """
        return self._static_trunc(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_erf(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.erf. This method simply
        wraps the function, and so the docstring for startai.erf also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container to compute exponential for.
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
            a container containing the Gauss error of ``x``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-0.25, 4, 1.3]),
        ...                   b=startai.array([12, -3.5, 1.234]))
        >>> y = startai.Container.static_erf(x)
        >>> print(y)
        {
            a: startai.array([-0.27632612, 1., 0.934008]),
            b: startai.array([1., -0.99999928, 0.91903949])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "erf",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def erf(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.erf. This method simply
        wraps thefunction, and so the docstring for startai.erf also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container to compute exponential for.
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
            a container containing the Gauss error of ``self``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-0.25, 4, 1.3]),
        ...                   b=startai.array([12, -3.5, 1.234]))
        >>> y = x.erf()
        >>> print(y)
        {
            a: startai.array([-0.27632612, 1., 0.934008]),
            b: startai.array([1., -0.99999928, 0.91903949])
        }
        """
        return self._static_erf(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_minimum(
        x1: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        use_where: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.minimum. This method
        simply wraps the function, and so the docstring for startai.minimum also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            Input array containing elements to minimum threshold.
        x2
            The other container or number to compute the minimum against.
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
        use_where
            Whether to use :func:`where` to calculate the minimum. If ``False``, the
            minimum is calculated using the ``(x + y - |x - y|)/2`` formula. Default is
            ``True``.
        out
            optional output container, for writing the result to. It must have a
            shape that the inputs broadcast to.

        Returns
        -------
            Container object with all sub-arrays having the minimum values computed.

        Examples
        --------
        With multiple :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([1, 3, 1]),
        ...                   b=startai.array([2, 8, 5]))
        >>> y = startai.Container(a=startai.array([1, 5, 6]),
        ...                   b=startai.array([5, 9, 7]))
        >>> z = startai.Container.static_minimum(x, y)
        >>> print(z)
        {
            a: startai.array([1, 3, 1]),
            b: startai.array([2, 8, 5])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "minimum",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            use_where=use_where,
            out=out,
        )

    def minimum(
        self: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        use_where: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.minimum. This method
        simply wraps the function, and so the docstring for startai.minimum also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array containing elements to minimum threshold.
        x2
            The other container or number to compute the minimum against.
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
        use_where
            Whether to use :func:`where` to calculate the minimum. If ``False``, the
            minimum is calculated using the ``(x + y - |x - y|)/2`` formula. Default is
            ``True``.
        out
            optional output container, for writing the result to. It must have a
            shape that the inputs broadcast to.

        Returns
        -------
            Container object with all sub-arrays having the minimum values computed.

        Examples
        --------
        With multiple :class:`startai.Container` inputs:

        >>> x = startai.Container(a=startai.array([1, 3, 1]),
        ...                   b=startai.array([2, 8, 5]))
        >>> y = startai.Container(a=startai.array([1, 5, 6]),
        ...                   b=startai.array([5, 9, 7]))
        >>> z = x.minimum(y)
        >>> print(z)
        {
            a: startai.array([1, 3, 1]),
            b: startai.array([2, 8, 5])
        }
        """
        return self._static_minimum(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            use_where=use_where,
            out=out,
        )

    @staticmethod
    def _static_maximum(
        x1: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        use_where: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.maximum. This method
        simply wraps the function, and so the docstring for startai.maximum also
        applies to this method with minimal changes.

        Parameters
        ----------
        x1
            Input array containing elements to maximum threshold.
        x2
            Tensor containing maximum values, must be broadcastable to x1.
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
        use_where
            Whether to use :func:`where` to calculate the maximum. If ``False``, the
            maximum is calculated using the ``(x + y + |x - y|)/2`` formula. Default is
            ``True``.
        out
            optional output container, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            A container with the elements of x1, but clipped to not be lower than the x2
            values.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.array([[1, 3], [2, 4], [3, 7]])
        >>> y = startai.Container(a=startai.array([1, 0,]),
        ...                   b=startai.array([-5, 9]))
        >>> z = startai.Container.static_maximum(x, y)
        >>> print(z)
        {
            a: startai.array([[1, 3],
                          [2, 4],
                          [3, 7]]),
            b: startai.array([[1, 9],
                          [2, 9],
                          [3, 9]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "maximum",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            use_where=use_where,
            out=out,
        )

    def maximum(
        self: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        use_where: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.maximum. This method
        simply wraps the function, and so the docstring for startai.maximum also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array containing elements to maximum threshold.
        x2
            Tensor containing maximum values, must be broadcastable to x1.
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
        use_where
            Whether to use :func:`where` to calculate the maximum. If ``False``, the
            maximum is calculated using the ``(x + y + |x - y|)/2`` formula. Default is
            ``True``.
        out
            optional output array, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            An container with the elements of x1, but clipped to not be
            lower than the x2 values.

        Examples
        --------
        With one :class:`startai.Container` input:

        >>> x = startai.array([[1, 3], [2, 4], [3, 7]])
        >>> y = startai.Container(a=startai.array([1, 0,]),
        ...                   b=startai.array([-5, 9]))
        >>> z = x.maximum(y)
        >>> print(z)
        {
            a: startai.array([[1, 3],
                          [2, 4],
                          [3, 7]]),
            b: startai.array([[1, 9],
                          [2, 9],
                          [3, 9]])
        }
        """
        return self._static_maximum(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            use_where=use_where,
            out=out,
        )

    @staticmethod
    def _static_reciprocal(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.reciprocal. This method
        simply wraps the function, and so the docstring for startai.reciprocal also
        applies to this method with minimal changes.

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
            a container with the element-wise recirpocal of ``x``

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2]), b=startai.array([4, 5]))
        >>> y = startai.Container.static_reciprocal(x)
        >>> print(y)
        {
            a: startai.array([1, 0.5]),
            b: startai.array([0.25, 0.2])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "reciprocal",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def reciprocal(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.reciprocal. This method
        simply wraps the function, and so the docstring for startai.reciprocal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container to compute the element-wise reciprocal for.
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
            a container with the element-wise recirpocal of ``x``

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2]), b=startai.array([4, 5]))
        >>> y = x.reciprocal()
        >>> print(y)
        {
            a: startai.array([1, 0.5]),
            b: startai.array([0.25, 0.2])
        }
        """
        return self._static_reciprocal(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_deg2rad(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.deg2rad. This method
        simply wraps the function, and so the docstring for startai.deg2rad also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. to be converted from degrees to radians.
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
            a container with each element in ``x`` converted from degrees to radians.

        Examples
        --------
        >>> x=startai.Container(a=startai.array([0,90,180,270,360]),
        ...                 b=startai.native_array([0,-1.5,-50,startai.nan]))
        >>> y=startai.Container.static_deg2rad(x)
        >>> print(y)
        {
            a: startai.array([0., 1.57, 3.14, 4.71, 6.28]),
            b: startai.array([0., -0.0262, -0.873, nan])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "deg2rad",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def deg2rad(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.deg2rad. This method
        simply wraps the function, and so the docstring for startai.deg2rad also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. to be converted from degrees to radians.
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
            a container with each element in ``x`` converted from degrees to radians.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x=startai.Container(a=startai.array([0., 0.351, -0.881, startai.nan]),
        ...                 b=startai.native_array([0,-1.5,-50,startai.nan]))
        >>> y=x.deg2rad()
        >>> print(y)
        {
            a: startai.array([0., 0.00613, -0.0154, nan]),
            b: startai.array([0., -0.0262, -0.873, nan])
        }
        """
        return self._static_deg2rad(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_rad2deg(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.rad2deg. This method
        simply wraps the function, and so the docstring for startai.rad2deg also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. to be converted from radians to degrees.
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
            a container with each element in ``x`` converted from radians to degrees.

        Examples
        --------
        >>> x=startai.Container(a=startai.array([0,90,180,270,360]),
        ...                 b=startai.native_array([0,-1.5,-50,startai.nan]))
        >>> y=startai.Container.static_rad2deg(x)
        >>> print(y)
        {
            a: startai.array([0., 5160., 10300., 15500., 20600.]),
            b: startai.array([0., -85.9, -2860., nan])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "rad2deg",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def rad2deg(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.rad2deg. This method
        simply wraps the function, and so the docstring for startai.rad2deg also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. to be converted from radians to degrees.
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
            a container with each element in ``x`` converted from radians to degrees.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> x=startai.Container(a=startai.array([0., 0.351, -0.881, startai.nan]),
        ...                 b=startai.native_array([0,-1.5,-50,7.2]))
        >>> y=x.rad2deg()
        >>> print(y)
        {
            a: startai.array([0., 20.1, -50.5, nan]),
            b: startai.array([0., -85.9, -2860., 413.])
        }
        """
        return self._static_rad2deg(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_trunc_divide(
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
        """startai.Container static method variant of startai.trunc_divide. This method
        simply wraps the function, and so the docstring for startai.trunc_divide
        also applies to this method with minimal changes.

        Parameters
        ----------
        x1
            dividend input array or container. Should have a real-valued data type.
        x2
            divisor input array or container. Must be compatible with ``x1``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([12., 3.5, 6.3]), b=startai.array([3., 1., 9.]))
        >>> x2 = startai.Container(a=startai.array([1., 2.3, -3]), b=startai.array([2.4, 3., -2.]))
        >>> y = startai.Container.static_divide(x1, x2)
        >>> print(y)
        {
            a: startai.array([12., 1., -2.]),
            b: startai.array([1., 0., -4.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "trunc_divide",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def trunc_divide(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.trunc_divide. This
        method simply wraps the function, and so the docstring for
        startai.trunc_divide also applies to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array or container. Should have a real-valued
            data type.
        x2
            divisor input array or container. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
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
            a container containing the element-wise results.
            The returned container must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Container` inputs:

        >>> x1 = startai.Container(a=startai.array([12., 3.5, 6.3]), b=startai.array([3., 1., 9.]))
        >>> x2 = startai.Container(a=startai.array([1., 2.3, -3]), b=startai.array([2.4, 3., -2.]))
        >>> y = x1.trunc_divide(x2)
        >>> print(y)
        {
            a: startai.array([12., 1., -2.]),
            b: startai.array([1., 0., -4.])
        }
        """
        return self._static_trunc_divide(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_isreal(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.isreal. This method
        simply wraps the function, and so the docstring for startai.isreal also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container. Should have a real-valued data type.
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
            a container containing the test result. An element ``out_i`` is ``True``
            if ``x_i`` is real number and ``False`` otherwise.
            The returned array should have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1+5j, 0-0j, 1.23j]),
        ...                   b=startai.array([7.9, 3.3j, -4.2-5.9j]))
        >>> z = startai.Container.static_isreal(x)
        >>> print(z)
        {
            a: startai.array([False, True, False]),
            b: startai.array([True, False, False])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "isreal",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def isreal(
        self: startai.Container,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.isreal. This method
        simply wraps the function, and so the docstring for startai.isreal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container. Should have a real-valued data type.
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
            a container containing the test result. An element ``out_i`` is ``True``
            if ``self_i`` is real number and ``False`` otherwise.
            The returned array should have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-1j, -np.inf, 1.23+7j]),\
                          b=startai.array([0.0, 3.3j, 1+0j]))
        >>> y = x.isreal()
        >>> print(y)
        {
            a: startai.array([False, True, False]),
            b: startai.array([True, False, True])
        }
        """
        return self._static_isreal(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_trapz(
        y: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        x: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        dx: Union[float, startai.Container] = 1.0,
        axis: Union[int, startai.Container] = -1,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.trapz. This method simply
        wraps the function, and so the docstring for startai.trapz also applies to
        this method with minimal changes.

        Parameters
        ----------
        y
            The container whose arrays should be integrated.
        x
            The sample points corresponding to the input array values.
            If x is None, the sample points are assumed to be evenly spaced
            dx apart. The default is None.
        dx
            The spacing between sample points when x is None. The default is 1.
        axis
            The axis along which to integrate.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including definite integrals of n-dimensional arrays
            as approximated along a single axis by the trapezoidal rule.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> y = startai.Container(a=startai.array((1, 2, 3)), b=startai.array((1, 5, 10)))
        >>> startai.Container.static_trapz(y)
        {
            a: 4.0
            b: 10.5
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "trapz",
            y,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            x=x,
            dx=dx,
            axis=axis,
            out=out,
        )

    def trapz(
        self: startai.Container,
        /,
        *,
        x: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        dx: Union[float, startai.Container] = 1.0,
        axis: Union[int, startai.Container] = -1,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.trapz. This method
        simply wraps the function, and so the docstring for startai.trapz also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The container whose arrays should be integrated.
        x
            The sample points corresponding to the input array values.
            If x is None, the sample points are assumed to be evenly spaced
            dx apart. The default is None.
        dx
            The spacing between sample points when x is None. The default is 1.
        axis
            The axis along which to integrate.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including definite integrals of n-dimensional arrays
            as approximated along a single axis by the trapezoidal rule.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> y = startai.Container(a=startai.array((1, 2, 3)), b=startai.array((1, 5, 10)))
        >>> y.trapz()
        {
            a: 4.0
            b: 10.5
        }
        """
        return self._static_trapz(self, x=x, dx=dx, axis=axis, out=out)

    @staticmethod
    def _static_lcm(
        x1: Union[startai.Container, startai.Array, startai.NativeArray],
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.lcm. This method simply
        wraps the function, and so the docstring for startai.lcm also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            first input container.
        x2
            second input container.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            a container containing the element-wise least common multiples
            of the arrays contained in x1 and x2.

        Examples
        --------
        >>> x1=startai.Container(a=startai.array([2, 3, 4]),
        ...                  b=startai.array([6, 54, 62, 10]))
        >>> x2=startai.Container(a=startai.array([5, 8, 15]),
        ...                  b=startai.array([32, 40, 25, 13]))
        >>> startai.Container.lcm(x1, x2)
        {
            a: startai.array([10, 21, 60]),
            b: startai.array([96, 1080, 1550, 130])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "lcm",
            x1,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def lcm(
        self: startai.Container,
        x2: Union[startai.Container, startai.Array, startai.NativeArray],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.lcm. This method simply
        wraps the function, and so the docstring for startai.lcm also applies to
        this method with minimal changes.

        Parameters
        ----------
        x1
            first input container.
        x2
            second input container.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            a container containing the the element-wise least common multiples
            of the arrays contained in x1 and x2.

        Examples
        --------
        >>> x1=startai.Container(a=startai.array([2, 3, 4]),
        ...                  b=startai.array([6, 54, 62, 10]))
        >>> x2=startai.Container(a=startai.array([5, 8, 15]),
        ...                  b=startai.array([32, 40, 25, 13]))
        >>> x1.lcm(x2)
        {
            a: startai.array([10, 24, 60]),
            b: startai.array([96, 1080, 1550, 130])
        }
        """
        return self._static_lcm(
            self,
            x2,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )
