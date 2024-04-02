# global
from typing import Union, Optional, List, Dict, Literal

# local
import startai
from startai.data_classes.container.base import ContainerBase


class _ContainerWithActivationExperimental(ContainerBase):
    @staticmethod
    def static_logit(
        x: Union[float, int, startai.Container],
        /,
        *,
        eps: Optional[Union[float, startai.Container]] = None,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.logit. This method simply
        wraps the function, and so the docstring for startai.logit  also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            Input container.
        eps
            When eps is None the function outputs NaN where x < 0 or x > 1.
            and inf or -inf where x = 1 or x = 0, respectively.
            Otherwise if eps is defined, x is clamped to [eps, 1 - eps]
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            Optional output Container.

        Returns
        -------
        ret
            Container with logits of the leaves.

        Examples
        --------
        >>> a = startai.array([1, 0, 0.9])
        >>> b = startai.array([0.1, 2, -0.9])
        >>> x = startai.Container(a=a, b=b)
        >>> z = startai.Container.static_logit(x)
        >>> print(z)
        {
            a: startai.array([inf, -inf, 2.19722438]),
            b: startai.array([-2.19722462, nan, nan])
        }

        >>> a = startai.array([0.3, 2, 0.9])
        >>> b = startai.array([0.1, 1.2, -0.9])
        >>> x = startai.Container(a=a, b=b)
        >>> z = startai.Container.static_logit(x, eps=0.2)
        >>> print(z)
        {
            a: startai.array([-0.84729779, 1.38629448, 1.38629448]),
            b: startai.array([-1.38629436, 1.38629448, -1.38629436])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "logit",
            x,
            eps=eps,
            complex_mode=complex_mode,
            out=out,
        )

    def logit(
        self: Union[float, int, startai.Container],
        /,
        *,
        eps: Optional[Union[float, startai.Container]] = None,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.logit. This method
        simply wraps the function, and so the docstring for startai.logit  also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container.
        eps
            When eps is None the function outputs NaN where x < 0 or x > 1.
            and inf or -inf where x = 1 or x = 0, respectively.
            Otherwise if eps is defined, x is clamped to [eps, 1 - eps]
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            Optional output Container.

        Returns
        -------
        ret
            Container with logits of the leaves.

        Examples
        --------
        >>> a = startai.array([1, 0, 0.9])
        >>> b = startai.array([0.1, 2, -0.9])
        >>> x = startai.Container(a=a, b=b)
        >>> z = x.logit()
        >>> print(z)
        {
            a: startai.array([inf, -inf, 2.19722438]),
            b: startai.array([-2.19722462, nan, nan])
        }

        >>> a = startai.array([0.3, 2, 0.9])
        >>> b = startai.array([0.1, 1.2, -0.9])
        >>> x = startai.Container(a=a, b=b)
        >>> z = x.logit(eps=0.2)
        >>> print(z)
        {
            a: startai.array([-0.84729779, 1.38629448, 1.38629448]),
            b: startai.array([-1.38629436, 1.38629448, -1.38629436])
        }
        """
        return self.static_logit(self, eps=eps, complex_mode=complex_mode, out=out)

    @staticmethod
    def static_thresholded_relu(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        threshold: Union[int, float, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.thresholded_relu. This
        method simply wraps the function, and so the docstring for
        startai.thresholded_relu also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        threshold
            threshold value above which the activation is linear. Default: ``0``.
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
            a container with the rectified linear activation unit function
            applied element-wise with custom threshold.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = startai.Container.static_thresholded_relu(x, threshold=0.5)
        >>> print(y)
        {
            a: startai.array([1., 0.]),
            b: startai.array([0., 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "thresholded_relu",
            x,
            threshold=threshold,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def thresholded_relu(
        self: startai.Container,
        /,
        *,
        threshold: Union[int, float, startai.Container] = 0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.thresholded_relu. This
        method simply wraps the function, and so the docstring for
        startai.thresholded_relu also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        threshold
            threshold value above which the activation is linear. Default: ``0``.
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
            a container with the rectified linear activation unit function
            applied element-wise with custom threshold.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = x.thresholded_relu(threshold=0.5)
        >>> print(y)
        {
            a: startai.array([1., 0.]),
            b: startai.array([0., 0.])
        }
        """
        return self.static_thresholded_relu(
            self,
            threshold=threshold,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_prelu(
        x: Union[startai.NativeArray, startai.Array, startai.Container],
        slope: Union[float, startai.NativeArray, startai.Array, startai.Container],
        /,
        *,
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
        slope
        key_chains
        to_apply
        prune_unapplied
        map_sequences
        out
        """
        return ContainerBase.cont_multi_map_in_function(
            "prelu",
            x,
            slope,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def prelu(
        self: startai.Container,
        slope: Union[float, startai.NativeArray, startai.Array, startai.Container],
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """

        Parameters
        ----------
        slope
        key_chains
        to_apply
        prune_unapplied
        map_sequences
        out
        """
        return self.static_prelu(
            self,
            slope,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_relu6(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.relu6. This method simply
        wraps the function, and so the docstring for startai.relu6 also applies to
        this method with minimal changes.

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
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container with the rectified linear 6 activation unit function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a = startai.array([-3., -2., -1., 0., 1., 2., 3., 4., 5.]),
        ...                   b = startai.array([1., 2., 3., 4., 5., 6., 7., 8., 9.]))
        >>> y = startai.Container.static_relu6(x)
        >>> print(y)
        {
            a: startai.array([0., 0., 0., 0., 1., 2., 3., 4., 5.]),
            b: startai.array([1., 2., 3., 4., 5., 6., 6., 6., 6.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "relu6",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            complex_mode=complex_mode,
            out=out,
        )

    def relu6(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.relu6. This method
        simply wraps the function, and so the docstring for startai.relu6 also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
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
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container with the rectified linear 6 activation unit function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a = startai.array([-3., -2., -1., 0., 1., 2., 3., 4., 5.]),
        ...                   b= startai.array([1., 2., 3., 4., 5., 6., 7., 8., 9.]))
        >>> y = x.relu()
        >>> print(y)
        {
            a: startai.array([0., 0., 0., 0., 1., 2., 3., 4., 5.]),
            b: startai.array([1., 2., 3., 4., 5., 6., 7., 8., 9.])
        }
        """
        return self.static_relu6(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            complex_mode=complex_mode,
            out=out,
        )

    @staticmethod
    def static_logsigmoid(
        input: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    ) -> startai.Container:
        """startai.Container static method variant of startai.logsigmoid. This method
        simply wraps the function, and so the docstring for startai.logsigmoid also
        applies to this method with minimal changes.

        Parameters
        ----------
        input
            Input container.
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

        Returns
        -------
            Container with Log-sigmoid applied to the leaves.

        Examples
        --------
        >>> a = startai.array([1, 0, 0.9])
        >>> b = startai.array([0.1, 2, -0.9])
        >>> x = startai.Container(a=a, b=b)
        >>> z = startai.Container.static_logsigmoid(x)
        >>> print(z)
        {
            a: startai.array([-0.31326169, -0.69314718, -0.34115386]),
            b: startai.array([-0.64439666, -0.126928, -1.24115384])
        }

        >>> a = startai.array([0.3, 2.5, 4.9])
        >>> b = startai.array([0.1, 1.2, -9.])
        >>> x = startai.Container(a=a, b=b)
        >>> z = startai.Container.static_logsigmoid(x)
        >>> print(z)
        {
            a: startai.array([-0.55435526, -0.07888974, -0.00741899]),
            b: startai.array([-0.64439666, -0.26328245, -9.00012302])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "logsigmoid",
            input,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            complex_mode=complex_mode,
        )

    def logsigmoid(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    ) -> startai.Container:
        """Apply element-wise Log-sigmoid of x i.e. log(1 / (1 + exp(-x)).

        Parameters
        ----------
        self
            Input container.
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.

        Returns
        -------
        ret
            Container with Log-sigmoid applied to the leaves.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = x.logsigmoid()
        >>> print(y)
        {
            a: startai.array([-0.31326163, -1.46328258]),
            b: startai.array([-0.51301527, -0.79813886])
        }
        """
        return self.static_logsigmoid(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            complex_mode=complex_mode,
        )

    @staticmethod
    def static_selu(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.selu. This method simply
        wraps the function, and so the docstring for startai.selu also applies to
        this method with minimal changes.

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
            a container with the scaled exponential linear unit activation function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = startai.Container.static_selu(x)
        >>> print(y)
        {
            a: startai.array([1.05070102, -1.22856998]),
            b: startai.array([0.42028043, -0.31868932])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "selu",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def selu(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.selu. This method
        simply wraps the function, and so the docstring for startai.selu also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
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
            a container with the scaled exponential linear unit activation function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = x.selu()
        >>> print(y)
        {
            a: startai.array([1.05070102, -1.22856998]),
            b: startai.array([0.42028043, -0.31868932])
        }
        """
        return self.static_selu(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_silu(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.silu. This method simply
        wraps the function, and so the docstring for startai.silu also applies to
        this method with minimal changes.

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
            a container with the rectified linear activation unit function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = startai.Container.static_silu(x)
        >>> print(y)
        {
            a: startai.array([0.73105854, -0.27777028]),
            b: startai.array([0.23947507, -0.0900332])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "silu",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def silu(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.silu. This method
        simply wraps the function, and so the docstring for startai.silu also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
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
            a container with the rectified linear activation unit function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = x.silu()
        >>> print(y)
        {
            a: startai.array([0.73105854, -0.27777028]),
            b: startai.array([0.23947507, -0.0900332])
        }
        """
        return self._static_silu(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_elu(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        alpha: startai.Container = 1.0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.elu. This method simply
        wraps the function, and so the docstring for startai.elu also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        alpha
            scaler for controlling the slope of the function for x <= 0 Default: 1.0
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
             a container with the elu unit function applied element-wise.

        Examples
        --------
        >>> x = x = startai.Container(a=startai.array([0.39, -0.85]), b=startai.array([1., -0.2]))
        >>> y = startai.Container.static_elu(x)
        >>> print(y)
        {
            a: startai.array([0.38999999, -0.57]),
            b: startai.array([1., -0.18])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "elu",
            x,
            alpha=alpha,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def elu(
        self: startai.Container,
        /,
        *,
        alpha: startai.Container = 1.0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.elu. This method simply
        wraps the function, and so the docstring for startai.elu also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        alpha
            scaler for controlling the slope of the function for x <= 0 Default: 1.0
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
           a container with the elu unit function applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0.39, -0.85]), b=startai.array([1., -0.2]))
        >>> y = x.elu()
        >>> print(y)
        {
            a: startai.array([0.38999999, -0.57]),
            b: startai.array([1., -0.18])
        }
        """
        return self._static_elu(
            self,
            alpha=alpha,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_hardtanh(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        min_val: startai.Container = -1.0,
        max_val: startai.Container = 1.0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.hardtanh.This method
        simply wrap the function,the docstring for startai.hardtanh also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        min_val
             minimum value of the linear region range. Default: -1.
        max_val
            maximum value of the linear region range. Default: 1.
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
             a container with the hardtanh unit function applied element-wise.

        Examples
        --------
        >>> x = x = startai.Container(a=startai.array([0.39, -2.0]), b=startai.array([2., -0.2]))
        >>> y = startai.Container._static_hardtanh(x)
        >>> print(y)
        {
            a: startai.array([0.3899, -1.]),
            b: startai.array([1., -0.2])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "hardtanh",
            x,
            min_val=min_val,
            max_val=max_val,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def hardtanh(
        self: startai.Container,
        /,
        *,
        min_val: startai.Container = -1.0,
        max_val: startai.Container = 1.0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.hardtanh.This method
        simply wraps the function, so the docstring for startai.elu also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        min_val
             minimum value of the linear region range. Default: -1.
        max_val
            maximum value of the linear region range. Default: 1.
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
           a container with the hardtanh unit function applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0.39, -2.0]), b=startai.array([2., -0.2]))
        >>> y = startai.Container.hardtanh(x)
        >>> print(y)
        {
            a: startai.array([0.389999, -1.]),
            b: startai.array([1., -0.2])
        }
        """
        return self._static_hardtanh(
            self,
            max_val=max_val,
            min_val=min_val,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_tanhshrink(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.tanhshrink. This method
        simply wraps the function, and so the docstring for startai.tanhshrink also
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
            a container with the tanhshrink activation unit function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = startai.Container._static_tanhshrink(x)
        >>> print(y)
        {
            a: startai.array([0.23840582, -0.36634541]),
            b: startai.array([0.02005103, -0.00262468])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "tanhshrink",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def tanhshrink(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.tanhshrink. This method
        simply wraps the function, and so the docstring for startai.tanhshrink also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
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
            a container with the tanhshrink activation unit function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = x.tanhshrink()
        >>> print(y)
        {
            a: startai.array([0.23840582, -0.36634541]),
            b: startai.array([0.02005103, -0.00262468])
        }
        """
        return self._static_tanhshrink(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_threshold(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        threshold: startai.Container,
        value: startai.Container,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.threshold. This method
        simply wraps the function, and so the docstring for startai.threshold also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        threshold
            threshold value for thresholding operation.
        value
            value to replace with if thresholding condition is not met.
        key_chains
            The key-chains to apply or not apply the method to.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container with the threshold activation unit function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = x._static_threshold(threshold=0.5, value=0.0)
        >>> print(y)
        {
            a: startai.array([1., 0.]),
            b: startai.array([0., 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "threshold",
            x,
            threshold=threshold,
            value=value,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def threshold(
        self: startai.Container,
        /,
        *,
        threshold: startai.Container,
        value: startai.Container,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.threshold. This method
        simply wraps the function, and so the docstring for startai.threshold also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        threshold
            threshold value for thresholding operation.
        value
            value to replace with if thresholding condition is not met.
        key_chains
            The key-chains to apply or not apply the method to.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            a container with the threshold activation unit function
            applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1.0, -1.2]), b=startai.array([0.4, -0.2]))
        >>> y = x.threshold(threshold=0.5, value=0.0)
        >>> print(y)
        {
            a: startai.array([1., 0.]),
            b: startai.array([0., 0.])
        }
        """
        return self._static_threshold(
            self,
            threshold=threshold,
            value=value,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_softshrink(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        lambd: startai.Container = 0.5,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = False,
        prune_unapplied: Union[bool, startai.Container] = True,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.softshrink. This method
        simply wraps the function, and so the docstring for startai.softshrink also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        lambd
            Lambda value for soft shrinkage calculation.
        key_chains
            The key-chains to apply or not apply the method to.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container with soft shrinkage applied to the leaves.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., -2.]), b=startai.array([0.4, -0.2]))
        >>> y = startai.Container._static_softshrink(x)
        >>> print(y)
        {
            a: startai.array([0.5, -1.5]),
            b: startai.array([0., 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "softshrink",
            x,
            lambd=lambd,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def softshrink(
        self: startai.Container,
        /,
        *,
        lambd: startai.Container = 0.5,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = False,
        prune_unapplied: Union[bool, startai.Container] = True,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """Apply the soft shrinkage function element-wise.

        Parameters
        ----------
        self
            Input container.
        lambd
            Lambda value for soft shrinkage calculation.
        key_chains
            The key-chains to apply or not apply the method to.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container with soft shrinkage applied to the leaves.

        Examples
        --------
        >>> import startai.numpy as np
        >>> x = startai.Container(a=np.array([1., -2.]), b=np.array([0.4, -0.2]))
        >>> y = startai.Container.softshrink(x)
        >>> print(y)
        {
            a: startai.array([0.5, -1.5]),
            b: startai.array([0., 0.])
        }
        """
        return self._static_softshrink(
            self,
            lambd=lambd,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_celu(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        alpha: startai.Container = 1.0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.celu. This method simply
        wraps the function, and so the docstring for startai.celu also applies to
        this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        alpha
            array or scalar specifying the alpha value for CELU formlation.
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
             a container with the celu unit function applied element-wise.

        Examples
        --------
        >>> x = x = startai.Container(a=startai.array([0.39, -0.85]), b=startai.array([1., -0.2]))
        >>> y = startai.Container.static_celu(x)
        >>> print(y)
        {
            a: startai.array([0.38999999, -0.17]),
            b: startai.array([1., -0.04])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "celu",
            x,
            alpha=alpha,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            complex_mode=complex_mode,
            out=out,
        )

    def celu(
        self: startai.Container,
        /,
        *,
        alpha: startai.Container = 1.0,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.leaky_relu. This method
        simply wraps the function, and so the docstring for startai.leaky_relu also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        alpha
            array or scalar specifying alpha (negative slope) value for CELU
            formulation.
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
           a container with the celu unit function applied element-wise.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([0.39, -0.85]), b=startai.array([1., -0.2]))
        >>> y = x.celu()
        >>> print(y)
        {
            a: startai.array([0.38999999, -0.57]),
            b: startai.array([1., -0.18])
        }
        """
        return self._static_celu(
            self,
            alpha=alpha,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            complex_mode=complex_mode,
            out=out,
        )

    @staticmethod
    def _static_scaled_tanh(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        alpha: Union[float, startai.Container] = 1.7159,
        beta: Union[float, startai.Container] = 0.67,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.scaled_tanh. This method
        simply wraps the function, and so the docstring for startai.scaled_tanh
        also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        alpha
            The scaling parameter for the output.
            Determines the amplitude of the tanh function.
            Default: 1.7159
        beta
            The scaling parameter for the input.
            Determines the slope of the tanh function.
            Default: 0.67
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
             a container with the scaled_tanh function applied.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([8.931, -0.85]), b=startai.array([1., -0.2])))
        >>> y = startai.Container._static_scaled_tanh(x)
        >>> y
        {
            a: startai.array([1.71587813, -0.88367474]),
            b: startai.array([1.00376701, -0.2285642])
        }

        >>> x = startai.Container(a=startai.array([8.9, -8.9]), b=startai.array([3., 33.2]))
        >>> y = startai.Container._static_scaled_tanh(x, alpha=2, beta=2.5)
        >>> y
        {
            a: startai.array([2., -2.]),
            b: startai.array([1.99999881, 2.])
        }

        >>> x = startai.Container(a=startai.array([0.3, -0.3]), b=startai.array([33.0, -33.0]))
        >>> y = startai.Container._static_scaled_tanh(x, alpha=1.5, beta=25)
        >>> y
        {
            a: startai.array([1.49999905, -1.49999905]),
            b: startai.array([1.5, -1.5])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "scaled_tanh",
            x,
            alpha=alpha,
            beta=beta,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def scaled_tanh(
        self: startai.Container,
        /,
        *,
        alpha: Union[float, startai.Container] = 1.7159,
        beta: Union[float, startai.Container] = 0.67,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.scaled_tanh. This
        method simplywraps the function, and so the docstring for
        startai.scaled_tanh also applies to this method with minimal changes.

        Parameters
        ----------
        x
           input container.
        alpha
           The scaling parameter for the output.
           Determines the amplitude of the tanh function.
           Default: 1.7159
        beta
            The scaling parameter for the input.
            Determines the slope of the tanh function.
            Default: 0.67
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
             a container with the scaled_tanh function applied.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([2., 3.]), b=startai.array([1., 2.]))
        >>> x.scaled_tanh()
        {
            a: startai.array([1.49570239, 1.65537548]),
            b: startai.array([1.00376701, 1.49570239])
        }

        >>> x = startai.Container(a=startai.array([1., 1.]), b=startai.array([1., 1.]))
        >>> x.scaled_tanh(alpha=30)
        {
            a: startai.array([17.54939651, 17.54939651]),
            b: startai.array([17.54939651, 17.54939651])
        }

        >>> x = startai.Container(a=startai.array([20., 21.]), b=startai.array([3., 1.]))
        >>> x.scaled_tanh(alpha=0.1, beta=-0.4)
        {
            a: startai.array([-0.09999998, -0.09999999]),
            b: startai.array([-0.08336546, -0.0379949])
        }
        """
        return self._static_scaled_tanh(
            self,
            alpha=alpha,
            beta=beta,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_hardshrink(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        lambd: startai.Container = 0.5,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = False,
        prune_unapplied: Union[bool, startai.Container] = True,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.hardshrink. This method
        simply wraps the function, and so the docstring for startai.hardshrink also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input container.
        lambd
            Lambda value for hard shrinkage calculation.
        key_chains
            The key-chains to apply or not apply the method to.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
        map_sequences
            Whether to also map method to sequences (lists, tuples).

        Returns
        -------
        ret
            Container with hard shrinkage applied to the leaves.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., -2.]), b=startai.array([0.4, -0.2]))
        >>> y = startai.Container._static_hardshrink(x)
        >>> print(y)
        {
            a: startai.array([1., -2.]),
            b: startai.array([0., 0.])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "hardshrink",
            x,
            lambd=lambd,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def hardshrink(
        self: startai.Container,
        /,
        *,
        lambd: startai.Container = 0.5,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = False,
        prune_unapplied: Union[bool, startai.Container] = True,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """Apply the hard shrinkage function element-wise.

        Parameters
        ----------
        self
            Input container.
        lambd
            Lambda value for hard shrinkage calculation.
        key_chains
            The key-chains to apply or not apply the method to.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            Container with hard shrinkage applied to the leaves.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1., -2.]), b=startai.array([0.4, -0.2]))
        >>> y = startai.Container.hardshrink(x)
        >>> print(y)
        {
            a: startai.array([1., -2.]),
            b: startai.array([0., 0.])
        }
        """
        return self._static_hardshrink(
            self,
            lambd=lambd,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_hardsilu(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method which acts as a wrapper for
        startai.hardsilu.

        Parameters
        ----------
        x
            input container
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
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        a container containing the output of the hardsilu/hardswish function applied
        to each element in ``x``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-0.5, -1, 0]), b=startai.array([0.5, 1., 2]))
        >>> y = startai.Container._static_hardsilu(x)
        >>> print(y)
        {
            a: startai.array([-0.20833333, -0.33333334, 0.]),
            b: startai.array([0.29166666, 0.66666669, 1.66666663])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "hardsilu",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def hardsilu(
        self,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method which acts as a wrapper for
        startai.hardsilu.

        Parameters
        ----------
        self
            input container
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
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        a container containing the output of the hardsilu/hardswish function applied
        to each element in the input container.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([-0.5, -1, 0]), b=startai.array([0.5, 1., 2]))
        >>> y = x.hardsilu()
        >>> print(y)
        {
            a: startai.array([-0.20833333, -0.33333334, 0.]),
            b: startai.array([0.29166666, 0.66666669, 1.66666663])
        }
        """
        return self._static_hardsilu(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )
