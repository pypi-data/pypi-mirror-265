# global
from typing import Optional, Tuple, Union, List, Callable, Dict, Sequence

# local
from startai.data_classes.container.base import ContainerBase
import startai


# ToDo: implement all methods here as public instance methods

# ToDo: update docstrings and typehints according to startai\layers


# noinspection PyMissingConstructor
class _ContainerWithLayers(ContainerBase):
    @staticmethod
    def _static_linear(
        x: startai.Container,
        weight: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        bias: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.linear. This method
        simply wraps the function, and so the docstring for startai.linear also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            The input x to compute linear transformation on.
            *[outer_batch_shape,inner_batch_shape,in_features]*
        weight
            The weight matrix. *[outer_batch_shape,out_features,in_features]*
        bias
            The bias vector, default is ``None``. *[outer_batch_shape,out_features]*
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
            Result array of the linear transformation.
            *[outer_batch_shape,inner_batch_shape,out_features]*

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[1.1, 2.2, 3.3], \
                                           [11., 22., 33.]]), \
                              b=startai.array([[1.245, 0.278, 4.105], \
                                           [7., 13., 17.]]))
        >>> w = startai.array([[1., 2., 3.], \
                           [4., 5., 6.], \
                           [7., 8., 9.]])
        >>> b = startai.array([1., 0., -1.])
        >>> y = startai.Container.static_linear(x, w, bias=b)
        >>> print(y)
        {
            a: startai.array([[16.4, 35.2, 54.],
                          [155., 352., 549.]]),
            b: startai.array([[15.1, 31., 46.9],
                          [85., 195., 305.]])
        }

        >>> x = startai.Container(a=startai.array([[1.1, 2.2, 3.3], \
                                           [.0, .1, .2]]), \
                              b=startai.array([[1.245, 0.278, 4.105], \
                                           [.7, .8, .9]]))
        >>> w = startai.Container(a=startai.array([[1., 2., 3.]]), \
                              b=startai.array([[.1, .2, .3]]))
        >>> b = startai.Container(a=startai.array([1.]), b=startai.array([-1.]))
        >>> y = startai.Container.static_linear(x, w, bias=b)
        >>> print(y)
        {
            a: startai.array([[16.4],
                          [1.8]]),
            b: startai.array([[0.412],
                          [-0.5]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "linear",
            x,
            weight,
            bias=bias,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def linear(
        self: startai.Container,
        weight: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        bias: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.linear. This method
        simply wraps the function, and so the docstring for startai.linear also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input container to compute linear transformation on.
            *[outer_batch_shape,inner_batch_shape,in_features]*
        weight
            The weight matrix. *[outer_batch_shape,out_features,in_features]*
        bias
            The bias vector, default is ``None``. *[outer_batch_shape,out_features]*
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
            Result array of the linear transformation.
            *[outer_batch_shape,inner_batch_shape,out_features]*

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[1.1, 2.2, 3.3],
        ...                                [11., 22., 33.]]),
        ...                   b=startai.array([[1.245, 0.278, 4.105],
        ...                                [7., 13., 17.]]))
        >>> w = startai.array([[1., 2., 3.],
        ...                [4., 5., 6.],
        ...                [7., 8., 9.]])
        >>> b = startai.Container(a=startai.array([1., 0., -1.]),
        ...                   b=startai.array([1., 1., 0.]))
        >>> y = x.linear(w, bias=b, out=x)
        >>> print(y)
        {
            a: startai.array([[16.39999962, 35.19999695, 54.],
                          [155., 352., 549.]]),
            b: startai.array([[15.11600018, 32., 47.88399887],
                          [85., 196., 306.]])
        }
        """
        return self._static_linear(
            self,
            weight,
            bias=bias,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_dropout(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        prob: Union[float, startai.Container],
        /,
        *,
        scale: Union[bool, startai.Container] = True,
        dtype: Optional[Union[startai.Dtype, startai.Container]] = None,
        training: Union[bool, startai.Container] = True,
        seed: Optional[Union[int, startai.Container]] = None,
        noise_shape: Optional[Union[Sequence[int], startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.dropout. This method
        simply wraps the function, and so the docstring for startai.dropout also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            The input container x to perform dropout on.
        prob
            The probability of zeroing out each array element, float between 0 and 1.
        scale
            Whether to scale the output by `1/(1-prob)`, default is ``True``.
        dtype
            Output array data type. If dtype is None, the output array data type
            must be inferred from x. Default: ``None``.
        training
            Turn on dropout if training, turn off otherwise. Default is ``True``.
        seed
            Set a default seed for random number generating (for reproducibility).
            Default is ``None``.
        noise_shape
            a sequence representing the shape of the binary dropout mask that will be
            multiplied with the input.
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
            Result array of the output after dropout is performed.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[1., 2., 3.], [4., 5., 6.]]),
        ...                   b=startai.array([7., 8., 9.]))
        >>> y = startai.Container.static_dropout(x, 0.3)
        >>> print(y)
        {
            a: startai.array([[0., 0., 4.28571415],
                          [5.71428585, 7.14285755, 0.]]),
            b: startai.array([0., 11.4285717, 12.8571434])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "dropout",
            x,
            prob,
            scale=scale,
            dtype=dtype,
            training=training,
            seed=seed,
            noise_shape=noise_shape,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def dropout(
        self: startai.Container,
        prob: Union[float, startai.Container],
        /,
        *,
        scale: Union[bool, startai.Container] = True,
        dtype: Optional[Union[startai.Dtype, startai.Container]] = None,
        training: Union[bool, startai.Container] = True,
        seed: Optional[Union[int, startai.Container]] = None,
        noise_shape: Optional[Union[Sequence[int], startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.dropout. This method
        simply wraps the function, and so the docstring for startai.dropout also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input container to perform dropout on.
        prob
            The probability of zeroing out each array element, float between 0 and 1.
        scale
            Whether to scale the output by `1/(1-prob)`, default is ``True``.
        dtype
            output array data type. If dtype is None, the output array data type
            must be inferred from x. Default: ``None``.
        training
            Turn on dropout if training, turn off otherwise. Default is ``True``.
        seed
            Set a default seed for random number generating (for reproducibility).
            Default is ``None``.
        noise_shape
            a sequence representing the shape of the binary dropout mask that will be
            multiplied with the input.
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
            Result array of the output after dropout is performed.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[1., 2., 3.], [4., 5., 6.]]),
        ...                   b=startai.array([7., 8., 9.]))
        >>> y = x.dropout(0.3)
        >>> print(y)
        {
            a: startai.array([[0., 0., 4.28571415],
                          [5.71428585, 7.14285755, 0.]]),
            b: startai.array([0., 11.4285717, 12.8571434])
        }
        """
        return self._static_dropout(
            self,
            prob,
            scale=scale,
            dtype=dtype,
            training=training,
            seed=seed,
            noise_shape=noise_shape,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_dropout1d(
        x: startai.Container,
        prob: Union[float, startai.Container],
        /,
        *,
        training: Union[bool, startai.Container] = True,
        data_format: Union[str, startai.Container] = "NWC",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.dropout1d. This method
        simply wraps the function, and so the docstring for startai.dropout1d also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            The input container to perform dropout on.
        prob
            The probability of zeroing out each array element, float between 0 and 1.
        training
            Turn on dropout if training, turn off otherwise. Default is ``True``.
        data_format
            "NWC" or "NCW". Default is ``"NCW"``.
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
            Result container of the output after dropout is performed.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 3]).reshape([1, 1, 3]),
        ...                   b=startai.array([4, 5, 6]).reshape([1, 1, 3]))
        >>> y = startai.Container.static_dropout1d(x, 0.5)
        >>> print(y)
        {
            a: startai.array([[[0., 4., 0.]]]),
            b: startai.array([[[0., 0., 12.]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "dropout1d",
            x,
            prob,
            training=training,
            data_format=data_format,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def dropout1d(
        self: startai.Container,
        prob: Union[float, startai.Container],
        /,
        *,
        training: Union[bool, startai.Container] = True,
        data_format: Union[str, startai.Container] = "NWC",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.dropout1d. This method
        simply wraps the function, and so the docstring for startai.dropout1d also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input container to perform dropout on.
        prob
            The probability of zeroing out each array element, float between 0 and 1.
        training
            Turn on dropout if training, turn off otherwise. Default is ``True``.
        data_format
            "NWC" or "NCW". Default is ``"NCW"``.
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
            Result container of the output after dropout is performed.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([1, 2, 3]).reshape([1, 1, 3]),
        ...                   b=startai.array([4, 5, 6]).reshape([1, 1, 3]))
        >>> y = x.dropout1d(x, 0.5)
        >>> print(y)
        {
            a: startai.array([[[0., 4., 0.]]]),
            b: startai.array([[[0., 0., 12.]]])
        }
        """
        return self._static_dropout1d(
            self,
            prob,
            training=training,
            data_format=data_format,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_dropout2d(
        x: startai.Container,
        prob: Union[float, startai.Container],
        /,
        *,
        training: Union[bool, startai.Container] = True,
        data_format: Union[str, startai.Container] = "NHWC",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.dropout2d. This method
        simply wraps the function, and so the docstring for startai.dropout2d also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            The input container to perform dropout on.
        prob
            The probability of zeroing out each array element, float between 0 and 1.
        training
            Turn on dropout if training, turn off otherwise. Default is ``True``.
        data_format
            "NHWC" or "NCHW". Default is ``"NHWC"``.
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
            Result container of the output after dropout is performed.
        """
        return ContainerBase.cont_multi_map_in_function(
            "dropout2d",
            x,
            prob,
            training=training,
            data_format=data_format,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def dropout2d(
        self: startai.Container,
        prob: Union[float, startai.Container],
        /,
        *,
        training: Union[bool, startai.Container] = True,
        data_format: Union[str, startai.Container] = "NHWC",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.dropout2d. This method
        simply wraps the function, and so the docstring for startai.dropout2d also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input container to perform dropout on.
        prob
            The probability of zeroing out each array element, float between 0 and 1.
        training
            Turn on dropout if training, turn off otherwise. Default is ``True``.
        data_format
            "NHWC" or "NCHW". Default is ``"NHWC"``.
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
            Result container of the output after dropout is performed.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[100, 200, 300]]),
        ...                   b=startai.array([[400, 500, 600]]))
        >>> y = x.dropout2d(0.5)
        >>> print(y)
        {
            a: startai.array([[200., 0., 600.]]),
            b: startai.array([[0., 0., 0.]])
        }
        """
        return self._static_dropout2d(
            self,
            prob,
            training=training,
            data_format=data_format,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_dropout3d(
        x: startai.Container,
        prob: Union[float, startai.Container],
        /,
        *,
        training: Union[bool, startai.Container] = True,
        data_format: Union[str, startai.Container] = "NDHWC",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.dropout3d. This method
        simply wraps the function, and so the docstring for startai.dropout3d also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            The input container to perform dropout on.
        prob
            The probability of zeroing out each array element, float between 0 and 1.
        training
            Turn on dropout if training, turn off otherwise. Default is ``True``.
        data_format
            "NDHWC" or "NCDHW". Default is ``"NDHWC"``.
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
            Result container of the output after dropout is performed.
        """
        return ContainerBase.cont_multi_map_in_function(
            "dropout3d",
            x,
            prob,
            training=training,
            data_format=data_format,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def dropout3d(
        self: startai.Container,
        prob: Union[float, startai.Container],
        /,
        *,
        training: Union[bool, startai.Container] = True,
        data_format: Union[str, startai.Container] = "NDHWC",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.dropout3d. This method
        simply wraps the function, and so the docstring for startai.dropout3d also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            The input container to perform dropout on.
        prob
            The probability of zeroing out each array element, float between 0 and 1.
        training
            Turn on dropout if training, turn off otherwise. Default is ``True``.
        data_format
            "NDHWC" or "NCDHW". Default is ``"NDHWC"``.
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
            Result container of the output after dropout is performed.
        """
        return self._static_dropout3d(
            self,
            prob,
            training=training,
            data_format=data_format,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_scaled_dot_product_attention(
        query: Union[startai.Array, startai.NativeArray, startai.Container],
        key: Union[startai.Array, startai.NativeArray, startai.Container],
        value: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        scale: Union[float, startai.Container],
        mask: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        dropout_p: Optional[float] = 0.0,
        is_causal: Optional[bool] = False,
        training: Optional[bool] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of
        startai.scaled_dot_product_attention. This method simply wraps the
        function, and so the docstring for startai.scaled_dot_product_attention
        also applies to this method with minimal changes.

        Parameters
        ----------
        query
            The queries input container. The shape of queries input array leaves should
            be in *[batch_shape,num_queries,feat_dim]*. The queries input array leaves
            should have the same size as keys and values.
        key
            The keys input array container. The shape of keys input array leaves
            should be in *[batch_shape,num_keys,feat_dim]*. The keys input array
            leaves should have the same size as queries and values.
        value
            The values input array container. The shape of values input array
            leaves should be in *[batch_shape,num_keys,feat_dim]*. The values
            input array leaves should have the same size as queries and keys.
        scale
            The scale float value.
            The scale float value is used to scale the query-key pairs before softmax.
        mask
            The mask input array/container. The mask to apply to the query-key values.
            Default is None. The shape of mask input array leaves should be in
            *[batch_shape,num_queries,num_keys]*.
        dropout_p
            Specifies the dropout probability, if greater than 0.0, dropout is applied
        is_causal
            If true, assumes causal attention masking and errors if both `mask` and
            `is_causal` are set.
        training
            If True, dropout is used, otherwise dropout is not activated.
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
            The output container following applications of scaled dot-product
            attention. The output array is the weighted sum produced by the
            attention score and value. The shape of output array is
            *[batch_shape,num_queries,feat_dim]* .

        Examples
        --------
        With :class:`startai.Container` input:

        >>> q = startai.Container(a=startai.array([[[0.2, 1.], [2.7, 3.], [4.4, 5.6]]]),
        ...                   b=startai.array([[[1.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
        >>> k = startai.Container(a=startai.array([[[4.2, 1.], [2.2, 3.3],[4.4, 5.6]]]),
        ...                   b=startai.array([[[3.2, 1.], [2.2, 3.6], [4.0, 5.6]]]))
        >>> v = startai.Container(a=startai.array([[[5.2, 1.], [2.1, 3.],[4.4, 5.6]]]),
        ...                   b=startai.array([[[0.2, 1.], [2.2, 3.],[4.4, 5.6]]]))
        >>> mask =
        ... startai.Container(a=startai.array([[[1.0, 1.0, 1.0],
        ...                             [1.0, 1.0, 1.0],
        ...                             [1.0, 1.0,1.0]]]),
        ...               b=startai.array([[[1.0, 1.0, 1.0],
        ...                             [1.0, 1.0, 1.0],
        ...                             [1.0, 1.0,1.0]]]))
        >>> result = startai.Container.static_scaled_dot_product_attention(q,
        ...                                                            k,
        ...                                                            v,
        ...                                                            1,
        ...                                                            mask=mask)
        >>> print(result)
        {
            a: startai.array([[[4.27, 5.4],
                        [4.4, 5.6],
                        [4.4, 5.6]]]),
            b: startai.array([[[4.35, 5.54],
                        [4.4, 5.6],
                        [4.4, 5.6]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "scaled_dot_product_attention",
            query,
            key,
            value,
            scale=scale,
            mask=mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            training=training,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def scaled_dot_product_attention(
        self: startai.Container,
        key: Union[startai.Array, startai.NativeArray, startai.Container],
        value: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        scale: Union[float, startai.Container],
        mask: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        dropout_p: Optional[float] = 0.0,
        is_causal: Optional[bool] = False,
        training: Optional[bool] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of
        startai.scaled_dot_product_attention. This method simply wraps the
        function, and so the docstring for startai.scaled_dot_product_attention
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            The queries input container. The shape of queries input array leaves should
            be in *[batch_shape,num_queries,feat_dim]*. The queries input array leaves
            should have the same size as keys and values.
        key
            The keys input array container. The shape of keys input array leaves
            should be in *[batch_shape,num_keys,feat_dim]*. The keys input array
            leaves should have the same size as queries and values.
        value
            The values input array container. The shape of values input array
            leaves should be in *[batch_shape,num_keys,feat_dim]*. The values
            input array leaves should have the same size as queries and keys.
        scale
            The scale float value.
            The scale float value is used to scale the query-key pairs before softmax.
        mask
            The mask input array/container. The mask to apply to the query-key values.
            Default is None. The shape of mask input array leaves should be in
            *[batch_shape,num_queries,num_keys]*.
        dropout_p
            Specifies the dropout probability, if greater than 0.0, dropout is applied
        is_causal
            If true, assumes causal attention masking and errors if both `mask` and
            `is_causal` are set.
        training
            If True, dropout is used, otherwise dropout is not activated.
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
            The output container following applications of scaled dot-product
            attention. The output array is the weighted sum produced by the
            attention score and value. The shape of output array is
            *[batch_shape,num_queries,feat_dim]* .

        Examples
        --------
        With :class:`startai.Container` input:

        >>> q = startai.Container(a=startai.array([[[0.2, 1.], [2.7, 3.], [4.4, 5.6]]]),
        ...                   b=startai.array([[[1.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
        >>> k = startai.Container(a=startai.array([[[4.2, 1.], [2.2, 3.3], [4.4, 5.6]]]),
        ...                   b=startai.array([[[3.2, 1.], [2.2, 3.6], [4.0, 5.6]]]))

        >>> v = startai.Container(a=startai.array([[[5.2, 1.], [2.1, 3.], [4.4, 5.6]]]),
        ...                   b=startai.array([[[0.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
        >>> result = startai.scaled_dot_product_attention(q, k, v, scale=1, dropout_p=0.1,
        ...                                           is_causal=True, training=True)
        >>> print(result)
        {
            a: startai.array([[[5.19999981, 1.],
                           [2.59249449, 2.68226194],
                           [4.4000001, 5.5999999]]]),
            b: startai.array([[[0.2, 1.],
                           [2.19603825, 2.9960382],
                           [4.4000001, 5.5999999]]])
        }

        >>> q = startai.Container(a=startai.array([[[0.2, 1.], [2.7, 3.], [4.4, 5.6]]]),
        ...                   b=startai.array([[[1.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
        >>> k = startai.Container(a=startai.array([[[4.2, 1.], [2.2, 3.3], [4.4, 5.6]]]),
        ...                   b=startai.array([[[3.2, 1.], [2.2, 3.6], [4.0, 5.6]]]))
        >>> v = startai.Container(a=startai.array([[[5.2, 1.], [2.1, 3.], [4.4, 5.6]]]),
        ...                   b=startai.array([[[0.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
        >>> mask =
        ... startai.Container(a=startai.array([[[1.0, 1.0, 1.0],
        ...                             [1.0, 1.0, 1.0],
        ...                             [1.0, 1.0, 1.0]]]),
        ...               b=startai.array([[[1.0, 1.0, 1.0],
        ...                             [1.0, 1.0, 1.0],
        ...                             [1.0, 1.0,1.0]]]))
        >>> result = startai.scaled_dot_product_attention(q,k,v,scale=1,mask=mask)
        >>> print(result)
        {
            a: startai.array([[[4.26894283, 5.40236187],
                           [4.39999437, 5.59999037],
                           [4.4000001, 5.5999999]]]),
            b: startai.array([[[4.35046196, 5.54282808],
                           [4.39989519, 5.5998764],
                           [4.4000001, 5.5999999]]])

        }
        """
        return self._static_scaled_dot_product_attention(
            self,
            key,
            value,
            scale=scale,
            mask=mask,
            dropout_p=dropout_p,
            is_causal=is_causal,
            training=training,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_multi_head_attention(
        query: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        value: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        num_heads: Union[int, startai.Container] = 8,
        scale: Optional[Union[float, startai.Container]] = None,
        attention_mask: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        in_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        q_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        k_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        v_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        out_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        in_proj_bias: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        out_proj_bias: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        is_causal: Union[bool, startai.Container] = False,
        key_padding_mask: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        bias_k: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        bias_v: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        static_k: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        static_v: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        add_zero_attn: Union[bool, startai.Container] = False,
        return_attention_weights: Union[bool, startai.Container] = False,
        average_attention_weights: Union[bool, startai.Container] = True,
        dropout: Union[float, startai.Container] = 0.0,
        training: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        return ContainerBase.cont_multi_map_in_function(
            "multi_head_attention",
            query,
            key=key,
            value=value,
            num_heads=num_heads,
            scale=scale,
            attention_mask=attention_mask,
            in_proj_weights=in_proj_weights,
            q_proj_weights=q_proj_weights,
            k_proj_weights=k_proj_weights,
            v_proj_weights=v_proj_weights,
            out_proj_weights=out_proj_weights,
            in_proj_bias=in_proj_bias,
            out_proj_bias=out_proj_bias,
            is_causal=is_causal,
            key_padding_mask=key_padding_mask,
            bias_k=bias_k,
            bias_v=bias_v,
            static_k=static_k,
            static_v=static_v,
            add_zero_attn=add_zero_attn,
            return_attention_weights=return_attention_weights,
            average_attention_weights=average_attention_weights,
            dropout=dropout,
            training=training,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def multi_head_attention(
        self: startai.Container,
        /,
        *,
        key: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        value: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        num_heads: Union[int, startai.Container] = 8,
        scale: Optional[Union[float, startai.Container]] = None,
        attention_mask: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        in_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        q_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        k_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        v_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        out_proj_weights: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        in_proj_bias: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        out_proj_bias: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        is_causal: Union[bool, startai.Container] = False,
        key_padding_mask: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        bias_k: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        bias_v: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        static_k: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        static_v: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        add_zero_attn: Union[bool, startai.Container] = False,
        return_attention_weights: Union[bool, startai.Container] = False,
        average_attention_weights: Union[bool, startai.Container] = True,
        dropout: Union[float, startai.Container] = 0.0,
        training: Union[bool, startai.Container] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        return self._static_multi_head_attention(
            self,
            key=key,
            value=value,
            num_heads=num_heads,
            scale=scale,
            attention_mask=attention_mask,
            in_proj_weights=in_proj_weights,
            q_proj_weights=q_proj_weights,
            k_proj_weights=k_proj_weights,
            v_proj_weights=v_proj_weights,
            out_proj_weights=out_proj_weights,
            in_proj_bias=in_proj_bias,
            out_proj_bias=out_proj_bias,
            is_causal=is_causal,
            key_padding_mask=key_padding_mask,
            bias_k=bias_k,
            bias_v=bias_v,
            static_k=static_k,
            static_v=static_v,
            add_zero_attn=add_zero_attn,
            return_attention_weights=return_attention_weights,
            average_attention_weights=average_attention_weights,
            dropout=dropout,
            training=training,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_conv1d(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        data_format: str = "NWC",
        filter_format: str = "channel_last",
        x_dilations: Union[int, Tuple[int]] = 1,
        dilations: Union[int, Tuple[int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.conv1d. This method
        simply wraps the function, and so the docstring for startai.conv1d also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input image *[batch_size,w, d_in]*.
        filters
            Convolution filters *[fw,d_in, d_out]*. (d_in must be the same as d from x)
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating the
            per-dimension paddings.
        data_format
            "NWC" or "NCW". Defaults to "NWC".
        filter_format
            Either "channel_first" or "channel_last". Defaults to "channel_last".
        x_dilations
            The dilation factor for each dimension of input. (Default value = 1)
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
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
        bias
        Bias array of shape *[d_out]*.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the convolution operation.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[[2., 3., 4.], [5., 6., 7.]]]),
        ...                   b=startai.array([[[7., 8., 9.], [10., 11., 12]]]))
        >>> filters = startai.array([[[0., 0.5, 1.], [0.25, 0.5, 0.75], [-0.5, 0., 0.5 ]]])
        >>> result= startai.Container.static_conv1d(x,filters,(1,),'VALID')
        >>> print(result)
        {
            ... a: startai.array([[[-1.25, 2.5, 6.25],
            ...                [-2., 5.5, 13.]]]),
            ... b: startai.array([[[-2.5, 7.5, 17.5],
            ...                [-3.25, 10.5, 24.2]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "conv1d",
            x,
            filters,
            strides,
            padding,
            data_format=data_format,
            filter_format=filter_format,
            x_dilations=x_dilations,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    def conv1d(
        self: startai.Container,
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        data_format: str = "NWC",
        filter_format: str = "channel_last",
        x_dilations: Union[int, Tuple[int]] = 1,
        dilations: Union[int, Tuple[int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.conv1d. This method
        simply wraps the function, and so the docstring for startai.conv1d also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input image *[batch_size,w, d_in]*.
        filters
            Convolution filters *[fw,d_in, d_out]*. (d_in must be the same as d from x)
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating the
            per-dimension paddings.
        data_format
            "NWC" or "NCW". Defaults to "NWC".
        filter_format
            Either "channel_first" or "channel_last". Defaults to "channel_last".
        x_dilations
            The dilation factor for each dimension of input. (Default value = 1)
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
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
        bias
            Bias array of shape *[d_out]*.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the convolution operation.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[[2., 3., 4.], [5., 6., 7.]]]),
        ...                   b=startai.array([[[7., 8., 9.], [10., 11., 12]]]))
        >>> filters = startai.array([[[0., 0.5, 1.], [0.25, 0.5, 0.75], [-0.5, 0., 0.5 ]]])
        >>> result= x.conv1d(filters, (1,), 'VALID')
        >>> print(result)
        {
            ... a: startai.array([[[-1.25, 2.5, 6.25],
            ...                [-2., 5.5, 13.]]]),
            ... b: startai.array([[[-2.5, 7.5, 17.5],
            ...                [-3.25, 10.5, 24.2]]])
        }
        """
        return self._static_conv1d(
            self,
            filters,
            strides,
            padding,
            data_format=data_format,
            filter_format=filter_format,
            x_dilations=x_dilations,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    @staticmethod
    def _static_conv2d(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int, int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        data_format: str = "NHWC",
        filter_format: str = "channel_last",
        x_dilations: Union[int, Tuple[int, int]] = 1,
        dilations: Union[int, Tuple[int, int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.conv2d. This method
        simply wraps the function, and so the docstring for startai.conv2d also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input image *[batch_size,h,w,d_in]*.
        filters
            Convolution filters *[fh,fw,d_in,d_out]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating
            the per-dimension paddings.
        data_format
            "NHWC" or "NCHW". Defaults to "NHWC".
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
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
            The result of the convolution operation.

        Examples
        --------
        >>> x = startai.Container(a = startai.eye(3, 3).reshape((1, 3, 3, 1)),
        ...                   b = startai.eye(5, 5).reshape((1, 5, 5, 1)))
        >>> filters = startai.array([[2., 0., 1.],
        ...                      [1., 3., 1.],
        ...                      [0., 1., 1.]]).reshape((3, 3, 1, 1))
        >>> result = startai.Container.static_conv2d(x, filters, (2,), 'SAME')
        >>> print(result)
        {
            a:startai.array([[[[4.],[0.]],[[1.],[5.]]]]),
            b:startai.array([[[[4.],[0.],[0.]],[[1.],[6.],[0.]],[[0.],[1.],[5.]]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "conv2d",
            x,
            filters,
            strides,
            padding,
            data_format=data_format,
            filter_format=filter_format,
            x_dilations=x_dilations,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    def conv2d(
        self: startai.Container,
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int, int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        data_format: str = "NHWC",
        filter_format: str = "channel_last",
        x_dilations: Union[int, Tuple[int, int]] = 1,
        dilations: Union[int, Tuple[int, int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of `startai.conv2d`. This method
        simply wraps the function, and so the docstring for `startai.conv2d` also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input image *[batch_size,h,w,d_in]*.
        filters
            Convolution filters *[fh,fw,d_in,d_out]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating
            the per-dimension paddings.
        data_format
            "NHWC" or "NCHW". Defaults to "NHWC".
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
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
            The result of the convolution operation.

        Examples
        --------
        >>> x = startai.Container(a = startai.eye(3, 3).reshape((1, 3, 3, 1)),
        ...                   b = startai.eye(5, 5).reshape((1, 5, 5, 1)))
        >>> filters = startai.array([[2, 0, 1],
        ...                      [1, 3, 1],
        ...                      [0, 1, 1]], dtype=startai.float32).reshape((3, 3, 1, 1))
        >>> result = x.conv2d(filters, 2, 'SAME')
        >>> print(result)
        {
            a:startai.array([[[[4.],[0.]],[[1.],[5.]]]]),
            b:startai.array([[[[4.],[0.],[0.]],[[1.],[6.],[0.]],[[0.],[1.],[5.]]]])
        }
        """
        return self._static_conv2d(
            self,
            filters,
            strides,
            padding,
            data_format=data_format,
            dilations=dilations,
            filter_format=filter_format,
            x_dilations=x_dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    @staticmethod
    def _static_conv1d_transpose(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        output_shape: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        filter_format: str = "channel_last",
        data_format: str = "NWC",
        dilations: Union[int, Tuple[int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.conv1d_transpose. This
        method simply wraps the function, and so the docstring for
        startai.conv1d_transpose also applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input image *[batch_size,w,d_in]* or *[batch_size,d_in,w]*.
        filters
            Convolution filters *[fw,d_out,d_in]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
            padding), or a sequence of n (low, high) integer pairs that give the padding
            to apply before and after each spatial dimension.
        output_shape
            Shape of the output (Default value = None)
        filter_format
            Either "channel_first" or "channel_last". "channel_first" corresponds
            to "IOW",input data formats, while "channel_last" corresponds to "WOI".
        data_format
            The ordering of the dimensions in the input, one of "NWC" or "NCW". "NWC"
            corresponds to input with shape (batch_size, width, channels), while "NCW"
            corresponds to input with shape (batch_size, channels, width).
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
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
        bias
            Bias array of shape *[d_out]*.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the transpose convolution operation.

        Examples
        --------
        >>> x = startai.Container(a=startai.random_normal(mean=0, std=1, shape=[1, 28, 3]),
        ...                   b=startai.random_normal(mean=0, std=1, shape=[1, 56, 3]))
        >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 6, 3])
        >>> y = startai.Container.static_conv1d_transpose(x, filters, 2, 'SAME')
        >>> print(y.shape)
        {
            a: [1,56,6],
            b: [1,112,6]
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "conv1d_transpose",
            x,
            filters,
            strides,
            padding,
            output_shape=output_shape,
            filter_format=filter_format,
            data_format=data_format,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    def conv1d_transpose(
        self: startai.Container,
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        output_shape: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        filter_format: str = "channel_last",
        data_format: str = "NWC",
        dilations: int = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> Union[startai.Array, startai.NativeArray, startai.Container]:
        """startai.Container instance method variant of startai.conv1d_transpose. This
        method simply wraps the function, and so the docstring for
        startai.conv1d_transpose also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input image *[batch_size,w,d_in]* or *[batch_size,d_in,w]*.
        filters
            Convolution filters *[fw,d_out,d_in]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
            padding), or a sequence of n (low, high) integer pairs that give the padding
            to apply before and after each spatial dimension.
        output_shape
            Shape of the output (Default value = None)
        filter_format
            Either "channel_first" or "channel_last". "channel_first" corresponds
            to "IOW",input data formats, while "channel_last" corresponds to "WOI".
        data_format
            The ordering of the dimensions in the input, one of "NWC" or "NCW". "NWC"
            corresponds to input with shape (batch_size, width, channels), while "NCW"
            corresponds to input with shape (batch_size, channels, width).
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
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
        bias
            Bias array of shape *[d_out]*.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the transpose convolution operation.

        Examples
        --------
        >>> x = startai.Container(a=startai.random_normal(mean=0, std=1, shape=[1, 28, 3]),
        ...                   b=startai.random_normal(mean=0, std=1, shape=[1, 56, 3]))
        >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 6, 3])
        >>> y = x.conv1d_transpose(filters, 2, 'SAME')
        >>> print(y.shape)
        {
            a: startai.Shape(1, 56, 6),
            b: startai.Shape(1, 112, 6)
        }
        """
        return self._static_conv1d_transpose(
            self,
            filters,
            strides,
            padding,
            output_shape=output_shape,
            filter_format=filter_format,
            data_format=data_format,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    @staticmethod
    def _static_conv2d_transpose(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int, int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        output_shape: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        filter_format: str = "channel_last",
        data_format: str = "NHWC",
        dilations: Union[int, Tuple[int, int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.conv2d_transpose. This
        method simply wraps the function, and so the docstring for startai.conv2d
        also applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input image *[batch_size,h,w,d_in]*.
        filters
            Convolution filters *[fh,fw,d_out,d_in]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating
            the per-dimension paddings.
        output_shape
            Shape of the output (Default value = None)
        filter_format
            Either "channel_first" or "channel_last". "channel_first" corresponds
            to "IOHW",input data formats, while "channel_last" corresponds to "HWOI".
        data_format
            "NHWC" or "NCHW". Defaults to "NHWC".
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
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
        bias
            Bias array of shape *[d_out]*.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the convolution operation.

        Examples
        --------
        >>> a = startai.random_normal(mean=0, std=1, shape=[1, 14, 14, 3])
        >>> b = startai.random_normal(mean=0, std=1, shape=[1, 28, 28, 3])
        >>> c = startai.random_normal(mean=0, std=1, shape=[3, 3, 6, 3])
        >>> d = startai.random_normal(mean=0, std=1, shape=[3, 3, 6, 3])
        >>> x = startai.Container(a=a, b=b)
        >>> filters = startai.Container(c=c, d=d)
        >>> y = startai.Container.static_conv2d_transpose(x, filters, 2, 'SAME')
        >>> print(y.shape)
        {
            a: {
                c: [1,28,28,6],
                d: [1,28,28,6]
            },
            b: {
                c: [1,56,56,6],
                d: [1,56,56,6]
            }
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "conv2d_transpose",
            x,
            filters,
            strides,
            padding,
            output_shape=output_shape,
            filter_format=filter_format,
            data_format=data_format,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    def conv2d_transpose(
        self: startai.Container,
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int, int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        output_shape: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        filter_format: str = "channel_last",
        data_format: str = "NHWC",
        dilations: Union[int, Tuple[int, int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.conv2d_transpose. This
        method simply wraps the function, and so the docstring for startai.conv2d
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input image *[batch_size,h,w,d_in]*.
        filters
            Convolution filters *[fh,fw,d_out,d_in]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating
            the per-dimension paddings.
        output_shape
            Shape of the output (Default value = None)
        filter_format
            Either "channel_first" or "channel_last". "channel_first" corresponds
            to "IOHW",input data formats, while "channel_last" corresponds to "HWOI".
        data_format
            "NHWC" or "NCHW". Defaults to "NHWC".
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
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
        bias
            Bias array of shape *[d_out]*.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the convolution operation.

        Examples
        --------
        >>> a = startai.random_normal(mean=0, std=1, shape=[1, 14, 14, 3])
        >>> b = startai.random_normal(mean=0, std=1, shape=[1, 28, 28, 3])
        >>> c = startai.random_normal(mean=0, std=1, shape=[6, 3, 3, 3])
        >>> d = startai.random_normal(mean=0, std=1, shape=[6, 3, 3, 3])
        >>> x = startai.Container(a=a, b=b)
        >>> filters = startai.Container(c=c, d=d)
        >>> y = x.conv2d_transpose(filters,2,'SAME')
        >>> print(y.shape)
        {
            a: {
                c: startai.Shape(1, 28, 28, 3),
                d: startai.Shape(1, 28, 28, 3)
            },
            b: {
                c: startai.Shape(1, 56, 56, 3),
                d: startai.Shape(1, 56, 56, 3)
            },
            c: {
                c: startai.Shape(6, 6, 6, 3),
                d: startai.Shape(6, 6, 6, 3)
            },
            d: {
                c: startai.Shape(6, 6, 6, 3),
                d: startai.Shape(6, 6, 6, 3)
            }
        }
        """
        return self._static_conv2d_transpose(
            self,
            filters,
            strides,
            padding,
            output_shape=output_shape,
            filter_format=filter_format,
            data_format=data_format,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    @staticmethod
    def _static_depthwise_conv2d(
        x: startai.Container,
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int], Tuple[int, int], startai.Container],
        padding: Union[str, List[int], startai.Container],
        /,
        *,
        data_format: Union[str, startai.Container] = "NHWC",
        dilations: Union[int, Tuple[int], Tuple[int, int], startai.Container] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.depthwise_conv2d. This
        method simply wraps the function, and so the docstring for
        startai.depthwise_conv2d also applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input image *[batch_size,h,w,d]*.
        filters
            Convolution filters *[fh,fw,d_in]*. (d_in must be the same as d from x)
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating the
            per-dimension paddings.
        data_format
            "NHWC" or "NCHW". Defaults to "NHWC".
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the convolution operation.

        Examples
        --------
        >>> a = startai.randint(0, 255, shape=(1, 128, 128, 3)).astype(startai.float32) / 255.0
        >>> b = startai.randint(0, 255, shape=(1, 128, 128, 3)).astype(startai.float32) / 255.0
        >>> inp = startai.Container(a=a, b=b)
        >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 3])
        >>> y = startai.Container.static_depthwise_conv2d(
        ...                                            inp,
        ...                                            filters,
        ...                                            strides=2,
        ...                                            padding='SAME')
        >>> print(y.shape)
        [1, 64, 64, 3]
        """
        return ContainerBase.cont_multi_map_in_function(
            "depthwise_conv2d",
            x,
            filters,
            strides,
            padding,
            data_format=data_format,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def depthwise_conv2d(
        self: startai.Container,
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int], Tuple[int, int], startai.Container],
        padding: Union[str, List[int], startai.Container],
        /,
        *,
        data_format: Union[str, startai.Container] = "NHWC",
        dilations: Union[int, Tuple[int], Tuple[int, int], startai.Container] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.depthwise_conv2d. This
        method simply wraps the function, and so the docstring for
        startai.depthwise_conv2d also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input image *[batch_size,h,w,d]*.
        filters
            Convolution filters *[fh,fw,d_in]*. (d_in must be the same as d from self)
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating the
            per-dimension paddings.
        data_format
            "NHWC" or "NCHW". Defaults to "NHWC".
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the convolution operation.

        Examples
        --------
        >>> a = startai.randint(0, 255, shape=(1, 128, 128, 3)).astype(startai.float32) / 255.0
        >>> b = startai.randint(0, 255, shape=(1, 128, 128, 3)).astype(startai.float32) / 255.0
        >>> inp = startai.Container(a=a, b=b)
        >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 3])
        >>> y = inp.depthwise_conv2d(filters, 2, 'SAME')
        >>> print(y.shape)
        [1, 64, 64, 3]
        """
        return self._static_depthwise_conv2d(
            self,
            filters,
            strides,
            padding,
            data_format=data_format,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_conv3d(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int, int, int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        data_format: str = "NDHWC",
        filter_format: str = "channel_last",
        x_dilations: Union[int, Tuple[int, int, int]] = 1,
        dilations: Union[int, Tuple[int, int, int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.conv3d. This method
        simply wraps the function, and so the docstring for startai.conv3d also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input volume *[batch_size,d,h,w,d_in]*.
        filters
            Convolution filters *[fdfh,fw,d_in,d_out]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating
            the per-dimension paddings.
        data_format
            "NDHWC" or "NCDHW". Defaults to "NDHWC".
        filter_format
            Either "channel_first" or "channel_last". Defaults to "channel_last".
        x_dilations
            The dilation factor for each dimension of input. (Default value = 1)
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
        bias
            Bias array of shape *[d_out]*.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the convolution operation.

        Examples
        --------
        >>> x = startai.Container(a = startai.full((1, 2, 3, 3, 1),0.5),\
                              b = startai.full((1, 2, 5, 5, 1),1.))

        >>> filters = startai.ones((3, 3, 3, 1, 1))

        >>> result = startai.Container.static_conv3d(x, filters, 2, 'SAME')
        >>> print(result)
        {
            a: startai.array([[[[[4.],[4.]],[[4.],[4.]]]]]),
            b: startai.array([[[[[8.],[12.],[8.]],[[12.],[18.],[12.]],[[8.],[12.],[8.]]]]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "conv3d",
            x,
            filters,
            strides,
            padding,
            data_format=data_format,
            filter_format=filter_format,
            x_dilations=x_dilations,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    def conv3d(
        self: startai.Container,
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[int, Tuple[int, int, int], startai.Container],
        padding: Union[str, startai.Container],
        /,
        *,
        data_format: str = "NDHWC",
        filter_format: str = "channel_last",
        x_dilations: Union[int, Tuple[int, int, int]] = 1,
        dilations: Union[int, Tuple[int, int, int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.conv3d. This method
        simply wraps the function, and so the docstring for startai.conv3d also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input volume *[batch_size,d,h,w,d_in]*.
        filters
            Convolution filters *[fdfh,fw,d_in,d_out]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating
            the per-dimension paddings.
        data_format
            "NDHWC" or "NCDHW". Defaults to "NDHWC".
        filter_format
            Either "channel_first" or "channel_last". Defaults to "channel_last".
        x_dilations
            The dilation factor for each dimension of input. (Default value = 1)
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
        bias
            Bias array of shape *[d_out]*.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the convolution operation.

        Examples
        --------
        >>> x = startai.Container(a = startai.full((1, 2, 3, 3, 1),0.5),\
                              b = startai.full((1, 2, 5, 5, 1),1.))

        >>> filters = startai.ones((3, 3, 3, 1, 1))

        >>> result = x.conv3d(filters, 2, 'SAME')
        >>> print(result)
        {
            a: startai.array([[[[[4.],[4.]],[[4.],[4.]]]]]),
            b: startai.array([[[[[8.],[12.],[8.]],[[12.],[18.],[12.]],[[8.],[12.],[8.]]]]])
        }
        """
        return self._static_conv3d(
            self,
            filters,
            strides,
            padding,
            data_format=data_format,
            filter_format=filter_format,
            x_dilations=x_dilations,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    @staticmethod
    def _static_conv3d_transpose(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[
            int, Tuple[int], Tuple[int, int], Tuple[int, int, int], startai.Container
        ],
        padding: Union[str, List[int], startai.Container],
        /,
        *,
        output_shape: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        filter_format: str = "channel_last",
        data_format: str = "NDHWC",
        dilations: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.conv3d_transpose. This
        method simply wraps the function, and so the docstring for
        startai.conv3d_transpose also applies to this method with minimal changes.

        Parameters
        ----------
        x
            Input container with leaves of volume *[batch_size,d,h,w,d_in]*
            or *[batch_size,d_in,d,h,w]*.
        filters
            Convolution filters *[fd,fh,fw,d_out,d_in]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating
            the per-dimension paddings.
        output_shape
            Shape of the output (Default value = None)
        filter_format
            Either "channel_first" or "channel_last". "channel_first" corresponds
            to "IODHW",input data formats, while "channel_last" corresponds to "DHWOI".
        data_format
            The ordering of the dimensions in the input, one of "NDHWC" or
            "NCDHW". "NDHWC" corresponds to inputs with shape (batch_size,
             depth, height, width, channels), while "NCDHW" corresponds
             to input with shape (batch_size, channels, depth, height,
             width).
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
        bias
            Bias array of shape *[d_out]*.
        out
            optional output container, for writing the result to. It must
            have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the transpose convolution operation in a container.

        >>> a = startai.random_normal(mean=0, std=1, shape=[1, 3, 14, 14, 3])
        >>> b = startai.random_normal(mean=0, std=1, shape=[1, 3, 28, 28, 3]))
        >>> c = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 6, 3])
        >>> d = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 6, 3]))
        >>> x = startai.Container(a=a, b=b)
        >>> filters = startai.Container(c=c, d=d)
        >>> y = startai.Container.static_conv3d_transpose(x, filters, 2, 'SAME')
        >>> print(y.shape)
        {
            a: {
                c: [1, 6, 28, 28, 6],
                d: [1, 6, 28, 28, 6]
            },
            b: {
                c: [1, 6, 56, 56, 6],
                d: [1, 6, 56, 56, 6]
            }
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "conv3d_transpose",
            x,
            filters,
            strides,
            padding,
            output_shape=output_shape,
            filter_format=filter_format,
            data_format=data_format,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    def conv3d_transpose(
        self: startai.Container,
        filters: Union[startai.Array, startai.NativeArray, startai.Container],
        strides: Union[
            int, Tuple[int], Tuple[int, int], Tuple[int, int, int], startai.Container
        ],
        padding: Union[str, List[int], startai.Container],
        /,
        *,
        output_shape: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        filter_format: str = "channel_last",
        data_format: str = "NDHWC",
        dilations: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str]]] = None,
        to_apply: bool = True,
        prune_unapplied: bool = False,
        map_sequences: bool = False,
        bias: Optional[startai.Container] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.conv3d_transpose. This
        method simply wraps the function, and so the docstring for
        startai.conv3d_transpose also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container with leaves of volume *[batch_size,d,h,w,d_in]*
            or *[batch_size,d_in,d,h,w]*.
        filters
            Convolution filters *[fd,fh,fw,d_out,d_in]*.
        strides
            The stride of the sliding window for each dimension of input.
        padding
            "SAME" or "VALID" indicating the algorithm, or list indicating
            the per-dimension paddings.
        output_shape
            Shape of the output (Default value = None)
        filter_format
            Either "channel_first" or "channel_last". "channel_first" corresponds
            to "IODHW",input data formats, while "channel_last" corresponds to "DHWOI".
        data_format
            The ordering of the dimensions in the input, one of "NDHWC" or
            "NCDHW". "NDHWC" corresponds to inputs with shape (batch_size,
             depth, height, width, channels), while "NCDHW" corresponds
             to input with shape (batch_size, channels, depth, height,
             width).
        dilations
            The dilation factor for each dimension of input. (Default value = 1)
        bias
            Bias array of shape *[d_out]*.
        out
            optional output container, for writing the result to. It must
            have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            The result of the transpose convolution operation in a container.

        Examples
        --------
        >>> x = startai.Container(a = startai.ones((1, 3, 3, 3, 1)).astype(startai.float32) )
        >>> filters = startai.ones((3, 3, 3, 1, 1)).astype(startai.float32)
        >>> result = x.conv3d(filters, 2, 'SAME')
        >>> print(result)
        {
            a: startai.array([[[[[8.],
                             [8.]],
                            [[8.],
                             [8.]]],
                          [[[8.],
                             [8.]],
                            [[8.],
                             [8.]]]]])
        }
        """
        return self._static_conv3d_transpose(
            self,
            filters,
            strides,
            padding,
            output_shape=output_shape,
            filter_format=filter_format,
            data_format=data_format,
            dilations=dilations,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            bias=bias,
            out=out,
        )

    @staticmethod
    def _static_lstm_update(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        init_h: Union[startai.Array, startai.NativeArray, startai.Container],
        init_c: Union[startai.Array, startai.NativeArray, startai.Container],
        kernel: Union[startai.Array, startai.NativeArray, startai.Container],
        recurrent_kernel: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        bias: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        recurrent_bias: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, startai.Container]:
        return ContainerBase.cont_multi_map_in_function(
            "lstm_update",
            x,
            init_h,
            init_c,
            kernel,
            recurrent_kernel,
            bias=bias,
            recurrent_bias=recurrent_bias,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def lstm_update(
        self: startai.Container,
        init_h: Union[startai.Array, startai.NativeArray, startai.Container],
        init_c: Union[startai.Array, startai.NativeArray, startai.Container],
        kernel: Union[startai.Array, startai.NativeArray, startai.Container],
        recurrent_kernel: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        bias: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        recurrent_bias: Optional[
            Union[startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, startai.Container]:
        """startai.Container instance method variant of startai.lstm_update. This
        method simply wraps the function, and so the docstring for
        startai.lstm_update also applies to this method with minimal changes.

        Parameters
        ----------
        init_h
            initial state tensor for the cell output *[batch_shape, out]*.
        init_c
            initial state tensor for the cell hidden state *[batch_shape, out]*.
        kernel
            weights for cell kernel *[in, 4 x out]*.
        recurrent_kernel
            weights for cell recurrent kernel *[out, 4 x out]*.
        bias
            bias for cell kernel *[4 x out]*. (Default value = None)
        recurrent_bias
            bias for cell recurrent kernel *[4 x out]*. (Default value = None)

        Returns
        -------
        ret
            hidden state for all timesteps *[batch_shape,t,out]* and cell state for last
            timestep *[batch_shape,out]*

        Examples
        --------
        >>> x = startai.Container(
        ...     a=startai.random_normal(shape=(5, 20, 3)),
        ...     b=startai.random_normal(shape=(5, 20, 3))
        ... )
        >>> h_i = startai.random_normal(shape=(5, 6))
        >>> c_i = startai.random_normal(shape=(5, 6))

        >>> kernel = startai.random_normal(shape=(3, 4 * 6))
        >>> rc = startai.random_normal(shape=(6, 4 * 6))
        >>> x.lstm_update(h_i, c_i, kernel, rc)
        {
            a: (tuple(2), <class startai.array.array.Array>, shape=[5, 20, 6]),
            b: (tuple(2), <class startai.array.array.Array>, shape=[5, 20, 6])
        }
        """
        return self._static_lstm_update(
            self,
            init_h,
            init_c,
            kernel,
            recurrent_kernel,
            bias=bias,
            recurrent_bias=recurrent_bias,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def _static_reduce_window(
        operand: Union[startai.Array, startai.NativeArray, startai.Container],
        init_value: Union[int, float, startai.Container],
        computation: Union[Callable, startai.Container],
        window_dimensions: Union[int, Sequence[int], startai.Container],
        /,
        *,
        window_strides: Union[int, Sequence[int], startai.Container] = 1,
        padding: Union[str, int, Sequence[Tuple[int, int]], startai.Container] = "VALID",
        base_dilation: Union[int, Sequence[int], startai.Container] = 1,
        window_dilation: Union[int, Sequence[int], startai.Container] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        return ContainerBase.cont_multi_map_in_function(
            "reduce_window",
            operand,
            init_value,
            computation,
            window_dimensions,
            window_strides=window_strides,
            padding=padding,
            base_dilation=base_dilation,
            window_dilation=window_dilation,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def reduce_window(
        self: startai.Container,
        init_value: Union[int, float, startai.Container],
        computation: Union[Callable, startai.Container],
        window_dimensions: Union[int, Sequence[int], startai.Container],
        /,
        *,
        window_strides: Union[int, Sequence[int], startai.Container] = 1,
        padding: Union[str, int, Sequence[Tuple[int, int]], startai.Container] = "VALID",
        base_dilation: Union[int, Sequence[int], startai.Container] = 1,
        window_dilation: Union[int, Sequence[int], startai.Container] = 1,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.reduce_window. This
        method simply wraps the function, and so the docstring for
        startai.reduce_window also applies to this method with minimal changes.

        Parameters
        ----------
        self
            A container representing the base areas on which the window is going to
            slide over.
        init_value
            The starting value for the reduction.
        computation
            The reduction function to apply to elements in each window.
        window_dimensions
            A sequence containing the window dimensions.
        window_strides
            A sequence containing the window strides.
        padding
            Either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
            padding), or a sequence of n (low, high) integer pairs that give the padding
            to apply before and after each spatial dimension.
        base_dilation
            A sequence containing the base dilation values.
        window_dilation
            A sequence containing the window dilation values.

        Returns
        -------
        ret
            The result of the pooling-like operation.

        Examples
        --------
        >>> x = startai.Container(
        ...     a=startai.array([[1, 2, 3, 4],
        ...                  [5, 6, 7, 8],
        ...                  [9, 10, 11, 12]]),
        ...     b=startai.array([[13, 14, 15, 16],
        ...                  [17, 18, 19, 20],
        ...                  [21, 22, 23, 24]])
        ... )
        >>> x.reduce_window(0, startai.sum, (2, 2))
        {
            a: startai.array([[21 25 29]
                          [33 37 41]
                          [45 49 53]]),
            b: startai.array([[63 67 71]
                          [75 79 83]
                          [87 91 95]])
        }
        """
        return self._static_reduce_window(
            self,
            init_value,
            computation,
            window_dimensions,
            window_strides=window_strides,
            padding=padding,
            base_dilation=base_dilation,
            window_dilation=window_dilation,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )
