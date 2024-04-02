"""Collection of Startai neural network layers in functional form."""

# global
from typing import Optional, Tuple, Union, Sequence

# local
import startai
from startai.utils.backend import current_backend
from startai.func_wrapper import (
    handle_array_function,
    handle_partial_mixed_function,
    inputs_to_startai_arrays,
    to_native_arrays_and_back,
    inputs_to_native_shapes,
    handle_out_argument,
    handle_nestable,
    handle_array_like_without_promotion,
    handle_device,
    handle_backend_invalid,
)
from startai.utils.exceptions import handle_exceptions

# Extra #
# ------#


def _get_embed_dim(
    in_proj_weights, q_proj_weights, k_proj_weights, v_proj_weights, query
):
    pre_embed_dim = query.shape[-1]
    if startai.exists(in_proj_weights):
        embed_dim = in_proj_weights.shape[0] / 3
    elif all(startai.exists(x) for x in [q_proj_weights, k_proj_weights, v_proj_weights]):
        embed_dim = q_proj_weights.shape[0]
    else:
        embed_dim = None
    return pre_embed_dim, embed_dim


def _in_projection(
    q,
    k,
    v,
    w,
    b=None,
):
    """Projects query, key and value efficiently, depending on whether we are
    doing self- attention (query is key is value) or cross-attention (key is
    value) or an attention where query, key and value are all different.

    it is only used in
    multi_head_attention layer.
    This helper function is a modified version of https://github.com/pytorch/pytorch/b
    lob/5293dee9208cc0e1e7db2ebdcbaef64908c087c6/torch/nn/functional.py#L4762.
    """
    E = q.shape[-1]
    if k is v:
        if q is k:
            # self-attention
            proj = startai.linear(q, w, bias=b)
            proj = proj.split(num_or_size_splits=3, axis=-1)
            return proj[0], proj[1], proj[2]
        else:
            # encoder-decoder attention
            w_q, w_kv = w.split(num_or_size_splits=[E, E * 2])
            if b is None:
                b_q = b_kv = None
            else:
                b_q, b_kv = b.split([E, E * 2])
            q_proj = startai.linear(q, w_q, bias=b_q)
            kv_proj = startai.linear(k, w_kv, bias=b_kv)
            kv_proj = kv_proj.split(num_or_size_splits=2, axis=-1)
            return (q_proj, kv_proj[0], kv_proj[1])
    else:
        w_q, w_k, w_v = w.split(num_or_size_splits=3)
        if b is None:
            b_q = b_k = b_v = None
        else:
            b_q, b_k, b_v = b.split(num_or_size_splits=3)
        return (
            startai.linear(q, w_q, bias=b_q),
            startai.linear(k, w_k, bias=b_k),
            startai.linear(v, w_v, bias=b_v),
        )


# Linear #
@handle_exceptions
@handle_nestable
@handle_partial_mixed_function
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def linear(
    x: Union[startai.Array, startai.NativeArray],
    weight: Union[startai.Array, startai.NativeArray],
    /,
    *,
    bias: Optional[Union[startai.Array, startai.NativeArray]] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply a linear transformation to the incoming data: y = x * t(weight) + bias.
    The operation also supports batching of the weight matrices. This is useful if a
    batch of different network parameters are to be represented.

    Parameters
    ----------
    x
        The input x to compute linear transformation on.
        *[outer_batch_shape,inner_batch_shape,in_features]*
    weight
        The weight matrix. *[outer_batch_shape,out_features,in_features]*
    bias
        The bias vector, default is ``None``. *[outer_batch_shape,out_features]*
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        Result array of the linear transformation.
        *[outer_batch_shape,inner_batch_shape,out_features]*

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([1., 2., 3.])
    >>> w = startai.array([[1., 0., 0.]])
    >>> y = startai.linear(x, w)
    >>> print(y)
    startai.array([1.])

    >>> x = startai.array([[0.666, -0.4269, 1.911]])
    >>> w = startai.array([[1., 0., 0.], [0., 0., 1.]])
    >>> y = startai.zeros((1, 2))
    >>> startai.linear(x, w, out=y)
    >>> print(y)
    startai.array([[0.666, 1.91 ]])

    >>> x = startai.array([[1.546, 5.234, 6.487],
    ...                [0.157, 5.753, 4.52],
    ...                [5.165, 3.159, 7.101]])
    >>> w = startai.array([[1.545, 2.547, 3.124],
    ...                [5.852, 8.753, 6.963]])
    >>> b = startai.array([-1., 1.])
    >>> y = startai.zeros((3, 2))
    >>> startai.linear(x, w, bias=b, out=y)
    >>> print(y)
    startai.array([[ 34.98495483, 101.0293808 ],
           [ 28.0159359 ,  83.74752808],
           [ 37.20942307, 108.3205719 ]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[1., 2., 3.],
    ...                                [4., 5., 6.]]),
    ...                   b=startai.array([1.1, 2.2, 3.3]))
    >>> w = startai.Container(a=startai.array([[1., 2., 3.],
    ...                                [-1., 1., 2.]]),
    ...                   b=startai.array([[0., -1., 1.],
    ...                                [0., 1., 1.]]))
    >>> b = startai.Container(a=startai.array([1., -1.]), b=startai.array([1., 1.]))
    >>> y = startai.linear(x, w, bias=b)
    >>> print(y)
    {
        a: startai.array([[15., 6.],
                      [33., 12.]]),
        b: startai.array([2.1, 6.5])
    }

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([[1.1, 2.2, 3.3],
    ...                                [11., 22., 33.]]),
    ...                   b=startai.array([[1.245, 0.278, 4.105],
    ...                                [7., 13., 17.]]))
    >>> w = startai.array([[1., 2., 3.],
    ...                [4., 5., 6.],
    ...                [7., 8., 9.]])
    >>> b = startai.Container(a=startai.array([1., 0., -1.]),
    ...                   b=startai.array([1., 1., 0.]))
    >>> startai.linear(x, w, bias=b, out=x)
    >>> print(x)
    {
        a: startai.array([[16.4, 35.2, 54.],
                      [155., 352., 549.]]),
        b: startai.array([[15.1, 32., 47.9],
                      [85., 196., 306.]])
    }

    """
    outer_batch_shape = list(weight.shape[:-2])
    num_outer_batch_dims = len(outer_batch_shape)
    inner_batch_shape = list(x.shape[num_outer_batch_dims:-1])
    num_inner_batch_dims = len(inner_batch_shape)
    num_out_feats, num_in_feats = list(weight.shape[-2:])

    # OBS x IBS x OF
    y = startai.matmul(
        x,
        startai.swapaxes(
            startai.reshape(
                weight,
                outer_batch_shape
                + [1] * max(num_inner_batch_dims - 1, 0)
                + [num_out_feats, num_in_feats],
            ),
            -1,
            -2,
        ),
    )

    if startai.exists(bias):
        # OBS x [1]*len(IBS) x OF
        bias_broadcast = startai.reshape(
            bias, outer_batch_shape + [1] * num_inner_batch_dims + [num_out_feats]
        )

        # OBS x IBS x OF
        y = y + bias_broadcast

    if startai.exists(out):
        return startai.inplace_update(out, y)
    return y


linear.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "handle_out_argument",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays", "handle_partial_mixed_function"),
}


# Dropout #


@handle_exceptions
@handle_nestable
@handle_partial_mixed_function
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def dropout(
    x: Union[startai.Array, startai.NativeArray],
    prob: float,
    /,
    *,
    scale: bool = True,
    dtype: Optional[Union[startai.Dtype, startai.NativeDtype]] = None,
    training: bool = True,
    seed: Optional[int] = None,
    noise_shape: Optional[Sequence[int]] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Randomly setting a fraction of input tensor to zeroes with probability.

    `prob` at each update during training time to prevent possible overfitting.
    The inputs not set to 0 are scaled up `1 / (1 - prob)` by default, so that
    overall sum is unchanged at training time and inference time.

    Parameters
    ----------
    x
        The input array x to perform dropout on.
    prob
        The probability of zeroing out each array element, float between 0 and 1.
    scale
        Whether to scale the output by `1/(1-prob)`. Default is ``True``.
    dtype
        output array data type. If dtype is None, the output array data type
        must be inferred from x. Default is ``None``.
    training
        Turn on dropout if training, turn off otherwise. Default is ``True``.
    seed
        Set a default seed for random number generating (for reproducibility). Default
        is ``None``.
    noise_shape
        a sequence representing the shape of the binary dropout mask that will be
        multiplied with the input. A shape dimension set to None means that a different
        mask value will be applied to each element of the input across that dimension. A
        dimension set to 1 means the same mask value will be applied to all elements of
        the input across that dimension.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        Result array after dropout is performed.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[1., 2., 3.],
    ...                [4., 5., 6.],
    ...                [7., 8., 9.],
    ...                [10., 11., 12.]])
    >>> y = startai.dropout(x,0.3)
    >>> print(y)
    startai.array([[ 1.42857146,  2.85714293,  4.28571415],
           [ 0.        ,  7.14285755,  8.5714283 ],
           [10.        , 11.4285717 ,  0.        ],
           [14.2857151 ,  0.        , 17.1428566 ]])


    >>> x = startai.array([[1.5, 2.6],
    ...                [4.9, 6.6],
    ...                [7.2, 8.7]])
    >>> y = startai.dropout(x,0.5)
    >>> print(y)
    startai.array([[ 0.        ,  5.19999981],
               [ 0.        ,  0.        ],
               [ 0.        , 17.39999962]])

    >>> x = startai.array([[1., 2., 3.],
    ...                [4., 5., 6.],
    ...                [7., 8., 9.],
    ...                [10., 11., 12.]])
    >>> y = startai.dropout(x,0.3,scale=False)
    >>> print(y)
    startai.array([[ 1.,  2., 3.],
               [ 4.,  5., 0.],
               [ 7.,  0., 9.],
               [10., 11., 0.]])

    >>> x = startai.array([[1.5, 2.6],
    ...                [4.9, 6.6],
    ...                [7.2, 8.7]])
    >>> y = startai.dropout(x,0.5,scale=False)
    >>> print(y)
    startai.array([[0., 2.6],
               [0., 0. ],
               [0., 8.7]])

    With :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[1., 2., 3.], [4., 5., 6.]]),
    ...                   b=startai.array([7., 8., 9.]))
    >>> y = startai.dropout(x,0.3)
    >>> print(y)
    {
    a: startai.array([[0., 0., 4.28571415],
                  [5.71428585, 7.14285755, 0.]]),
    b: startai.array([0., 11.4285717, 12.8571434])
    }

    >>> x = startai.Container(a=startai.array([[1.1, 2.2, 3.3], [11., 22., 33.]]),
    ...                   b=startai.array([[1.245, 0.278, 4.105], [7., 13., 17.]]))
    >>> y = startai.dropout(x,0.5)
    >>> print(y)
    {
        a: startai.array([[0., 4.4000001, 6.5999999],
                      [22., 44., 0.]]),
        b: startai.array([[2.49000001, 0.55599999, 8.21000004],
                      [14., 0., 0.]])
    }

    >>> x = startai.Container(a=startai.array([[1., 2., 3.], [4., 5., 6.]]),
    ...                   b=startai.array([7., 8., 9.]))
    >>> y = startai.dropout(x,0.3)
    >>> print(y)
    {
        a: startai.array([[0., 0., 3.],
                      [4., 5., 0.]]),
        b: startai.array([0., 8., 9.])
    }

    >>> x = startai.Container(a=startai.array([[1.1, 2.2, 3.3], [11., 22., 33.]]),
    ...                   b=startai.array([[1.245, 0.278, 4.105], [7., 13., 17.]]))
    >>> y = startai.dropout(x,0.5)
    >>> print(y)
    {
        a: startai.array([[0., 2.2, 3.3],
                      [11., 22., 0.]]),
        b: startai.array([[1.245, 0.278, 4.105],
                      [7., 0., 0.]])
    }
    """
    if prob == 0 or not training:
        if dtype is not None and x.dtype != dtype:
            x = startai.astype(x, dtype)
        return startai.inplace_update(out, x) if startai.exists(out) else x
    if noise_shape is None:
        noise_shape = x.shape
    else:
        noise_shape = list(noise_shape)
        for i, v in enumerate(noise_shape):
            if v is None:
                noise_shape[i] = x.shape[i]
    mask = startai.where(
        startai.random_uniform(shape=noise_shape, device=startai.dev(x), dtype=dtype, seed=seed)
        < prob,
        0.0,
        1.0,
    )
    x = x * mask
    if scale:
        x = startai.multiply(x, 1.0 / (1.0 - prob), out=out)
    return startai.inplace_update(out, x) if startai.exists(out) else x


dropout.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "handle_out_argument",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays", "handle_partial_mixed_function"),
}


# Attention #


@handle_exceptions
@handle_array_like_without_promotion
@handle_array_function
def scaled_dot_product_attention(
    query: Union[startai.Array, startai.NativeArray],
    key: Union[startai.Array, startai.NativeArray],
    value: Union[startai.Array, startai.NativeArray],
    /,
    *,
    scale: Optional[float] = None,
    mask: Optional[Union[startai.Array, startai.NativeArray]] = None,
    dropout_p: Optional[float] = 0.0,
    is_causal: Optional[bool] = False,
    training: Optional[bool] = False,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Apply scaled dot product attention to inputs x using optional mask.

    Parameters
    ----------
    query
        The queries input array. The shape of queries input array should be in
        *[batch_shape,num_queries,feat_dim]*. The queries input array should have the
        same size as keys and values.
    key
        The keys input array. The shape of keys input array should be in
        *[batch_shape,num_keys,feat_dim]*. The keys input array should have the same
        size as queries and values.
    value
        The values input array. The shape of values input should be in
        *[batch_shape,num_keys,feat_dim]*. The values input array should have the same
        size as queries and keys.
    scale
        The scale float value.
        The scale float value is used to scale the query-key pairs before softmax.
    mask
        The mask input array. The mask to apply to the query-key values. Default is
        None. The shape of mask input should be in *[batch_shape,num_queries,num_keys]*.
    dropout_p
        Specifies the dropout probability, if greater than 0.0, dropout is applied
    is_causal
        If true, assumes causal attention masking
        and errors if both `mask` and `is_causal` are set.
    training
        If True, dropout is used, otherwise dropout is not activated.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The output following application of scaled dot-product attention.
        The output array is the weighted sum produced by the attention score and value.
        The shape of output array is *[batch_shape,num_queries,feat_dim]* .

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> q = startai.array([[[0.2, 1.], [2.2, 3.],[4.4, 5.6]]])
    >>> k = startai.array([[[0.6, 1.5], [2.4, 3.3],[4.2, 5.1]]])
    >>> v = startai.array([[[0.4, 1.3], [2.2, 3.1],[4.3, 5.3]]])
    >>> result = startai.scaled_dot_product_attention(q,
    ...                                           k,
    ...                                           v,
    ...                                           scale=1,
    ...                                           dropout_p=0.1,
    ...                                           is_causal=True,
    ...                                           training=True)
    >>> print(result)

    startai.array([[[0.40000001, 1.29999995],
    ...         [2.19994521, 3.09994531],
    ...         [4.30000019, 5.30000019]]])

    >>> q = startai.array([[[0.2, 1.], [2.2, 3.],[4.4, 5.6]]])
    >>> k = startai.array([[[0.6, 1.5], [2.4, 3.3],[4.2, 5.1]]])
    >>> v = startai.array([[[0.4, 1.3], [2.2, 3.1],[4.3, 5.3]]])
    >>> mask = startai.array([[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]])
    >>> result = startai.scaled_dot_product_attention(q,k,v,scale=1,mask=mask)
    >>> print(result)

    startai.array([[[2.30000019, 3.23333359],
        [2.30000019, 3.23333359],
        [2.30000019, 3.23333359]]])

    >>> q = startai.array([[[0.2, 1.], [2.2, 3.], [4.4, 5.6]]])
    >>> k = startai.array([[[0.6, 1.5], [2.4, 3.3], [4.2, 5.1]]])
    >>> v = startai.array([[[0.4, 1.3], [2.2, 3.1], [4.3, 5.3]]])
    >>> out = startai.zeros(shape=(1, 3, 2))
    >>> startai.scaled_dot_product_attention(q,
    ...                                  k,
    ...                                  v,
    ...                                  scale=1,
    ...                                  dropout_p=0.1,
    ...                                  is_causal=True,
    ...                                  training=True,
    ...                                  out=out)
    >>> print(out)

    startai.array([[[0.40000001, 1.29999995],
    ...         [2.19994521, 3.09994531],
    ...         [4.30000019, 5.30000019]]])

    >>> q = startai.native_array([[[0.2, 1.], [2.2, 3.],[4.4, 5.6]]])
    >>> k = startai.native_array([[[0.6, 1.5], [2.4, 3.3],[4.2, 5.1]]])
    >>> v = startai.native_array([[[0.4, 1.3], [2.2, 3.1],[4.3, 5.3]]])
    >>> mask = startai.native_array([[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]])
    >>> result = startai.scaled_dot_product_attention(q,k,v,scale=1,mask=mask)
    >>> print(result)

    startai.array([[[2.30000019, 3.23333359],
    ...         [2.30000019, 3.23333359],
    ...         [2.30000019, 3.23333359]]])

    >>> q = startai.native_array([[[0.2, 1.], [2.2, 3.], [4.4, 5.6]]])
    >>> k = startai.native_array([[[0.6, 1.5], [2.4, 3.3], [4.2, 5.1]]])
    >>> v = startai.native_array([[[0.4, 1.3], [2.2, 3.1], [4.3, 5.3]]])
    >>> out = startai.zeros(shape=(1, 3, 2))
    >>> startai.scaled_dot_product_attention(q,
    ...                                  k,
    ...                                  v,
    ...                                  scale=1,
    ...                                  dropout_p=0.1,
    ...                                  is_causal=True,
    ...                                  training=True,
    ...                                  out=out)
    >>> print(out)

    startai.array([[[0.40000001, 1.29999995],
    ...         [2.19994521, 3.09994531],
    ...         [4.30000019, 5.30000019]]])

    With :class:`startai.Container` input:

    >>> q = startai.Container(a=startai.array([[[0.2, 1.], [2.7, 3.], [4.4, 5.6]]]),
    ...                   b=startai.array([[[1.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
    >>> k = startai.Container(a=startai.array([[[4.2, 1.], [2.2, 3.3], [4.4, 5.6]]]),
    ...                   b=startai.array([[[3.2, 1.], [2.2, 3.6], [4.0, 5.6]]]))
    >>> v = startai.Container(a=startai.array([[[5.2, 1.], [2.1, 3.], [4.4, 5.6]]]),
    ...                   b=startai.array([[[0.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
    >>> result = startai.scaled_dot_product_attention(q,
    ...                                           k,
    ...                                           v,
    ...                                           scale=1,
    ...                                           dropout_p=0.1,
    ...                                           is_causal=True,
    ...                                           training=True)
    >>> print(result)
    {
        a: startai.array([[[5.19999981, 1.],
        ...            [2.59249449, 2.68226194],
        ...            [4.4000001, 5.5999999]]]),
        b: startai.array([[[0.2, 1.],
        ...            [2.19603825, 2.9960382],
        ...            [4.4000001, 5.5999999]]])
    }

    >>> q = startai.Container(a=startai.array([[[0.2, 1.], [2.7, 3.], [4.4, 5.6]]]),
    ...                   b=startai.array([[[1.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
    >>> k = startai.Container(a=startai.array([[[4.2, 1.], [2.2, 3.3], [4.4, 5.6]]]),
    ...                   b=startai.array([[[3.2, 1.], [2.2, 3.6], [4.0, 5.6]]]))
    >>> v = startai.Container(a=startai.array([[[5.2, 1.], [2.1, 3.], [4.4, 5.6]]]),
    ...                   b=startai.array([[[0.2, 1.], [2.2, 3.], [4.4, 5.6]]]))
    >>> mask = startai.Container(
    ...     a=startai.array([[[1.0, 1.0, 1.0],[1.0, 1.0, 1.0],[1.0, 1.0, 1.0]]]),
    ...     b=startai.array([[[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0,1.0]]])
    ... )
    >>> result = startai.scaled_dot_product_attention(q,k,v,scale=1,mask=mask)
    >>> print(result)
    {
        a: startai.array([[[4.26894283, 5.40236187],
        ...            [4.39999437, 5.59999037],
        ...            [4.4000001, 5.5999999]]]),
        b: startai.array([[[4.35046196, 5.54282808],
        ...            [4.39989519, 5.5998764],
        ...            [4.4000001, 5.5999999]]])
    }

    With a mix of :class:`startai.Array` and :class:`startai.NativeArray` inputs:

    >>> q = startai.array([[[0.2, 1.], [2.2, 3.],[4.4, 5.6]]])
    >>> k = startai.native_array([[[0.6, 1.5], [2.4, 3.3],[4.2, 5.1]]])
    >>> v = startai.native_array([[[0.4, 1.3], [2.2, 3.1],[4.3, 5.3]]])
    >>> result = startai.scaled_dot_product_attention(q,
    ...                                            k,
    ...                                            v,
    ...                                            scale=1,
    ...                                            dropout_p=0.1,
    ...                                            is_causal=True,
    ...                                            training=True)
    >>> print(result)

    startai.array([[[0.40000001, 1.29999995],
    ...         [2.19994521, 3.09994531],
    ...         [4.30000019, 5.30000019]]])

    >>> q = startai.array([[[0.2, 1.], [2.2, 3.], [4.4, 5.6]]])
    >>> k = startai.native_array([[[0.6, 1.5], [2.4, 3.3], [4.2, 5.1]]])
    >>> v = startai.native_array([[[0.4, 1.3], [2.2, 3.1], [4.3, 5.3]]])
    >>> out = startai.zeros(shape=(1, 3, 2))
    >>> startai.scaled_dot_product_attention(q,k,v,scale=1,out=out)
    >>> print(out)
    startai.array([[[4.03946018, 5.0280633 ],
    ...         [4.29981947, 5.29981089],
    ...         [4.30000019, 5.30000019]]])

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> q = startai.array([[[0.2, 1.], [2.2, 3.],[4.4, 5.6]]])
    >>> k = startai.Container(a=startai.array([[[4.2, 1.], [2.2, 3.3], [4.4, 5.6]]]),
    ...                   b=startai.array([[[3.2, 1.], [2.2, 3.6], [4.0, 5.6]]]))
    >>> v = startai.array([[[0.4, 1.3], [2.2, 3.1], [4.3, 5.3]]])
    >>> result = startai.scaled_dot_product_attention(q,k,v,scale=1,is_causal=True)
    >>> print(result)
    {
        a: startai.array([[[0.40000001, 1.29999995],
        ...            [2.06345534, 2.9634552],
        ...            [4.30000019, 5.30000019]]]),
        b: startai.array([[[0.40000001, 1.29999995],
        ...            [2.19336844, 3.09336829],
        ...            [4.30000019, 5.30000019]]])
    }
    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> q = startai.array([[[0.2, 1.], [2.2, 3.],[4.4, 5.6]]])
    >>> k = startai.Container(a=startai.array([[[4.2, 1.], [2.2, 3.3],[4.4, 5.6]]]),
    ...                   b=startai.array([[[3.2, 1.], [2.2, 3.6],[4.0, 5.6]]]))
    >>> v = startai.array([[[0.4, 1.3], [2.2, 3.1],[4.3, 5.3]]])
    >>> mask = startai.native_array([[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]])
    >>> result = startai.scaled_dot_product_attention(q,
    ...                                           k,
    ...                                           v,
    ...                                           scale=1,
    ...                                           mask=mask,
    ...                                           dropout_p=0.1,
    ...                                           training=True)
    >>> print(result)
    {
        a: startai.array([[[2.30000019, 3.23333359],
        ...            [2.30000019, 3.23333359],
        ...            [2.30000019, 3.23333359]]]),
        b: startai.array([[[2.30000019, 3.23333359],
        ...            [2.30000019, 3.23333359],
        ...            [2.30000019, 3.23333359]]])
    }
    """
    startai.assertions.check_all(
        (not is_causal) or (is_causal and mask is None),
        "is_causal and attn_mask cannot be set at the same time",
    )
    embed_dim = query.shape[-1]
    scale = scale if scale else 1 / (embed_dim**0.5)
    sim = startai.einsum("... q f, ... k f -> ... q k", query, key) * scale
    sim = startai.dropout(sim, dropout_p, training=training)
    if startai.exists(mask):
        sim = startai.where(
            startai.logical_not(mask),
            -startai.ones_like(sim) * startai.finfo(startai.dtype(sim)).max,
            sim,
        )
    elif is_causal:
        L = query.shape[-2]  # Source sequence length
        S = key.shape[-2]  # Target sequence length
        mask = startai.tril(startai.ones((L, S)), k=0)
        mask = startai.astype(mask, startai.bool)
        sim = startai.where(
            startai.logical_not(mask),
            -startai.ones_like(sim) * startai.finfo(startai.dtype(sim)).max,
            sim,
        )
    attn = startai.softmax(sim, axis=-1)
    result = startai.einsum("... qk, ...kf -> ...qf", attn, value)
    return startai.inplace_update(out, result) if startai.exists(out) else result


@handle_exceptions
@handle_nestable
@handle_out_argument
@handle_partial_mixed_function
@inputs_to_startai_arrays
@handle_array_function
def multi_head_attention(
    query: Union[startai.Array, startai.NativeArray],
    /,
    *,
    key: Optional[Union[startai.Array, startai.NativeArray]] = None,
    value: Optional[Union[startai.Array, startai.NativeArray]] = None,
    batch_first: bool = True,
    num_heads: int = 8,
    scale: Optional[float] = None,
    attention_mask: Optional[Union[startai.Array, startai.NativeArray]] = None,
    in_proj_weights: Optional[Union[startai.Array, startai.NativeArray]] = None,
    q_proj_weights: Optional[Union[startai.Array, startai.NativeArray]] = None,
    k_proj_weights: Optional[Union[startai.Array, startai.NativeArray]] = None,
    v_proj_weights: Optional[Union[startai.Array, startai.NativeArray]] = None,
    out_proj_weights: Optional[Union[startai.Array, startai.NativeArray]] = None,
    in_proj_bias: Optional[Union[startai.Array, startai.NativeArray]] = None,
    out_proj_bias: Optional[Union[startai.Array, startai.NativeArray]] = None,
    is_causal: bool = False,
    key_padding_mask: Optional[Union[startai.Array, startai.NativeArray]] = None,
    bias_k: Optional[Union[startai.Array, startai.NativeArray]] = None,
    bias_v: Optional[Union[startai.Array, startai.NativeArray]] = None,
    static_k: Optional[Union[startai.Array, startai.NativeArray]] = None,
    static_v: Optional[Union[startai.Array, startai.NativeArray]] = None,
    add_zero_attn: bool = False,
    return_attention_weights: bool = False,
    average_attention_weights: bool = True,
    dropout: float = 0.0,
    training: bool = False,
    out: Optional[startai.Array] = None,
) -> Union[startai.Array, startai.NativeArray]:
    """Apply multi-head attention to inputs x. This is an implementation of
    multi-headed attention as described in the paper "Attention is all you
    Need" (Vaswani et al., 2017). If `query`, `key`, `value` are the same, then
    this is self-attention. Each timestep in `query` attends to the
    corresponding sequence in `key`, and returns a fixed-width vector. This
    layer first projects `query`, `key` and `value`. These are (effectively) a
    list of tensors of length `num_attention_heads`, where the corresponding
    shapes are `(batch_size, <query dimensions>, key_dim)`, `(batch_size,
    <key/value dimensions>, key_dim)`, `(batch_size, <key/value dimensions>,
    value_dim)`. Then, the query and key tensors are dot-producted and scaled.
    These are softmaxed to obtain attention probabilities. The value tensors
    are then interpolated by these probabilities, then concatenated back to a
    single tensor. Finally, the result tensor with the last dimension as
    value_dim can take a linear projection and return.

    Parameters
    ----------
    query
        The query embeddings. Shape: `(L, Q)` or `(N, L, Q)`, where L is the number of
        queries, N is the batch size, Q is the query embedding dimension.
    key
        The key embeddings. Shape: `(S, K)` or `(N, S, K)`, where S is the number of
        keys, N is the batch size, K is the key embedding dimension.
    value
        The value embeddings. Shape `(S, V)` or `(N, S, V)`, where S is the number of
        keys, N is the batch size, V is the value embedding dimension.
    batch_first
        If False, `query`, `key` and `value` will have shapes `(L, N, Q)`, `(S, N, K)`
        and `(S, N, V)` respectively (if batched).
    num_heads
        The number of attention heads to use.
    scale
        The value by which to scale the query-key similarity measure before softmax.
    attention_mask
        The mask to apply to the query-key values. Shape: `(L, S)` or
        `(N*num_heads, L, S)`.
    in_proj_weights
        The weights used to project query, key and value. Shape: `(3*E, E')`,  where E
        is the new embedding dimension and E' is the input embedding dimension, i.e.
        `E' = Q = K = V`.
    q_proj_weights
        The weights used to project query if `in_proj_weights` is None. Shape: `(E, Q)`.
    k_proj_weights
        The weights used to project key if `in_proj_weights` is None. Shape: `(E, K)`.
    v_proj_weights
        The weights used to project value if `in_proj_weights` is None. Shape: `(E, V)`.
    out_proj_weights
        The weights used to project the attention output. Shape: `(O, E)`, where O is
        the output embedding dimension.
    in_proj_bias
        The bias used when projecting query, key and value. Shape: `(3*E,)`.
    out_proj_bias
        The bias used when projecting the output. Shape: `(O,)`.
    is_causal
        If True, use a causal attention mask and ignore the provided `attention_mask`.
    key_padding_mask
        A binary mask to apply to the key sequence. Shape: `(S,)` or `(N, S)`.
    bias_k
        An additional bias added to the key sequence. Shape: `(E,)`.
    bias_v
        An additional bias added to the value sequence. Shape: `(E,)`.
    static_k
        A static key to be used in the attention operators.
        Shape: `(N*num_heads, S, E//num_heads)`.
    static_v
        A static value to be used in the attention operators.
        Shape: `(N*num_heads, S, E//num_heads)`.
    add_zero_attn
        A boolean flag indicating whether to add a batch of zeros to key and value.
    return_attention_weights
        If True, return the attention weights alongside the attention output.
    average_attention_weights
        If True, the returned attention weights will be averaged across heads.
        Otherwise, the attention weights will be provided separately per head.
        Note that this flag only has an effect when `return_attention_weights=True`.
    dropout
        Specifies the dropout probability. Dropout is applied on the attention weights.
    training
        If True, dropout is used, otherwise dropout is not activated.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The output following the application of multi-head attention. Either `output`
        or `(output, attention_weights)`. `output` will have shape `(L, E)` if the
        inputs were unbatched or `(N, L, E)` otherwise, and `attention_weights` will
        have shape `(L, S)` or `(N, L, S)` respectively. If `batch_first` is False and
        the inputs were batched, the `output` will have shape `(L, N, E)`.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.
    """
    num_dims = query.ndim
    startai.assertions.check_all(
        num_dims > 1 and num_dims < 4,
        "Number of dimensions should be 2 (for unbatched input) or 3 (for batched"
        f" input), got {num_dims}",
    )
    if key is None and value is None:
        key = value = query
    if num_dims == 2:
        query, key, value = (startai.expand_dims(x, axis=0) for x in [query, key, value])
    elif not batch_first:
        query, key, value = (startai.swapaxes(x, 0, 1) for x in [query, key, value])

    # project query, key and value
    if startai.exists(in_proj_weights):
        q, k, v = _in_projection(query, key, value, w=in_proj_weights, b=in_proj_bias)
        emb_dim = int(in_proj_weights.shape[0] / 3)
    elif all(startai.exists(x) for x in [q_proj_weights, k_proj_weights, v_proj_weights]):
        if startai.exists(in_proj_bias):
            b_q, b_k, b_v = startai.split(in_proj_bias, num_or_size_splits=3)
        else:
            b_q = b_k = b_v = None
        q, k, v = (
            startai.linear(query, q_proj_weights, bias=b_q),
            startai.linear(key, k_proj_weights, bias=b_k),
            startai.linear(value, v_proj_weights, bias=b_v),
        )
        emb_dim = q_proj_weights.shape[0]
    else:
        q, k, v = query, key, value
        if startai.exists(out_proj_weights):
            emb_dim = out_proj_weights.shape[-1]
        else:
            emb_dim = q.shape[-1]

    num_batches, num_queries = query.shape[:2]
    startai.assertions.check_true(
        emb_dim % num_heads == 0, "features must be divisible by number of heads"
    )
    head_dim = emb_dim // num_heads

    # apply extra bias
    if bias_k is not None and bias_v is not None:
        startai.assertions.check_true(
            not (startai.exists(static_k) or startai.exists(static_v)),
            "bias cannot be added to static key or value",
        )
        k = startai.concat([k, startai.tile(bias_k, (num_batches, 1, 1))], axis=1)
        v = startai.concat([v, startai.tile(bias_v, (num_batches, 1, 1))], axis=1)

    num_keys = k.shape[1]

    # reshape q, k, v for efficient matrix multiplication
    q = startai.swapaxes(q.reshape((num_queries, num_batches * num_heads, head_dim)), 0, 1)
    if static_k is None:
        k = startai.swapaxes(k.reshape((num_keys, num_batches * num_heads, head_dim)), 0, 1)
    else:
        k = static_k
    if static_v is None:
        v = startai.swapaxes(v.reshape((num_keys, num_batches * num_heads, head_dim)), 0, 1)
    else:
        v = static_v

    # add extra batch of zeros to k, v
    if add_zero_attn:
        zero_attn_shape = (num_batches * num_heads, 1, head_dim)
        k = startai.concat([k, startai.zeros(zero_attn_shape, dtype=k.dtype)], axis=1)
        v = startai.concat([v, startai.zeros(zero_attn_shape, dtype=v.dtype)], axis=1)
        num_keys = k.shape[1]

    # get attention scores
    attn_scores = startai.matmul(q, startai.swapaxes(k, 1, 2))
    scale = scale if scale else 1 / (head_dim**0.5)
    attn_scores *= scale

    # mask the attention scores
    if startai.exists(attention_mask):
        assert attention_mask.dtype in [query.dtype, startai.bool], (
            "was expecting attention_mask of type bool or the same as the input's, but"
            f" got {attention_mask.dtype}"
        )
        if is_causal:
            mask = startai.triu(startai.ones((num_queries, num_keys)), k=1)
            attention_mask = startai.where(mask, float("-inf"), 0)
        elif startai.is_bool_dtype(attention_mask):
            attention_mask = startai.where(attention_mask, float("-inf"), 0)
        if attention_mask.ndim == 2:
            attention_mask = startai.tile(attention_mask, (num_batches * num_heads, 1, 1))
    if key_padding_mask is not None:
        assert startai.is_bool_dtype(key_padding_mask), (
            "was expecting key_padding_mask of type bool, but got"
            f" {key_padding_mask.dtype}"
        )
        key_padding_mask = startai.where(key_padding_mask, float("-inf"), 0)
        if num_dims == 2:
            key_padding_mask = startai.expand_dims(key_padding_mask, axis=0)
        key_padding_mask = startai.tile(
            key_padding_mask, (num_batches * num_heads, num_queries, 1)
        )
        if attention_mask is None:
            attention_mask = key_padding_mask
        else:
            attention_mask += key_padding_mask
    if startai.exists(attention_mask):
        if bias_k is not None and bias_v is not None and not is_causal:
            attention_mask = startai.pad(attention_mask, [(0, 0), (0, 0), (0, 1)])
        if add_zero_attn and not is_causal:
            attention_mask = startai.pad(attention_mask, [(0, 0), (0, 0), (0, 1)])
        attn_scores += attention_mask.astype(query.dtype)

    # get attention weights
    attn_weights = startai.softmax(attn_scores, axis=-1)
    attn_weights = startai.dropout(attn_weights, dropout, training=training)

    # get attention output
    attention_out = startai.matmul(attn_weights, v)
    attention_out = startai.swapaxes(attention_out, 0, 1).reshape(
        (num_batches, num_queries, emb_dim)
    )
    if startai.exists(out_proj_weights):
        attention_out = startai.linear(attention_out, out_proj_weights, bias=out_proj_bias)

    if num_dims == 2:
        attention_out = attention_out.squeeze(axis=0)
    elif not batch_first:
        attention_out = attention_out.swapaxes(0, 1)
    if return_attention_weights:
        attn_weights = attn_weights.reshape(
            (num_batches, num_heads, num_queries, num_keys)
        )
        if average_attention_weights:
            attn_weights = attn_weights.mean(axis=1)
        if num_dims == 2:
            attn_weights = attn_weights.squeeze(axis=0)
        return attention_out, attn_weights
    else:
        return attention_out


multi_head_attention.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "handle_out_argument",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device_shifting",
    ),
    "to_skip": ("inputs_to_startai_arrays", "handle_partial_mixed_function"),
}


# Convolutions #


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def conv1d(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int]],
    padding: Union[str, int, Sequence[Tuple[int, int]]],
    /,
    *,
    data_format: str = "NWC",
    filter_format: str = "channel_last",
    x_dilations: Union[int, Tuple[int]] = 1,
    dilations: Union[int, Tuple[int]] = 1,
    bias: Optional[startai.Array] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 1-D convolution given 3-D input x and filters arrays.

    Parameters
    ----------
    x
        Input image *[batch_size,w,d_in]* or *[batch_size,d_in,w]*.
    filters
        Convolution filters *[fw,d_in,d_out]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
        padding), or a sequence of n (low, high) integer pairs that give the padding to
        apply before and after each spatial dimension.
    data_format
        The ordering of the dimensions in the input, one of "NWC" or "NCW". "NWC"
        corresponds to input with shape (batch_size, width, channels), while "NCW"
        corresponds to input with shape (batch_size, channels, width).
    filter_format
        Either "channel_first" or "channel_last". "channel_first" corresponds to "OIW",
         input data formats, while "channel_last" corresponds to "WIO", "HWIO", "DHWIO".
     x_dilations
        The dilation factor for each dimension of input. (Default value = 1)
    dilations
        The dilation factor for each dimension of input. (Default value = 1)
    bias
        Bias array of shape *[d_out]*.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the convolution operation.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.asarray([[[0.], [3.], [0.]]]) #NWC
    >>> filters = startai.array([[[0.]], [[1.]], [[0.]]]) #WIO
    >>> result = startai.conv1d(x, filters, (1,), 'SAME', data_format='NWC',dilations= (1,))
    >>> print(result)
    startai.array([[[0.], [3.], [0.]]])

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array([[[1., 3.], [2., 4.], [5., 7]]])
    >>> filters = startai.native_array([[[0., 1.], [1., 0.]]])
    >>> result = startai.conv1d(x, filters, (2,),'VALID')
    >>> print(result)
    startai.array([[[3., 1.],
    ...         [7., 5.]]])

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.Container(a=startai.array([[[1.2, 3.1, 4.8], [5.9, 2.2, 3.3],
    ...                                 [10.8, 7.6, 4.9], [6.1, 2.2, 9.5]]]),
    ...                   b=startai.array([[[8.8, 7.7, 6.6], [1.1, 2.2, 3.5]]]))
    >>> filters = startai.array([[[1., 0., 1.], [0., 1., 0.], [1., 1., 0.]]])
    >>> result  = startai.conv1d(x, filters, 3, 'VALID')
    >>> print(result)
    {
            a: startai.array([[[6., 7.9, 1.2],
    ...                    [15.6, 11.7, 6.1]]]),
    ...     b: startai.array([[[15.4, 14.3, 8.8]]])
    }
    """
    return current_backend(x).conv1d(
        x,
        filters,
        strides,
        padding,
        data_format=data_format,
        filter_format=filter_format,
        x_dilations=x_dilations,
        dilations=dilations,
        bias=bias,
        out=out,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@inputs_to_native_shapes
@to_native_arrays_and_back
@handle_array_function
@handle_device
def conv1d_transpose(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int]],
    padding: str,
    /,
    *,
    output_shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
    filter_format: str = "channel_last",
    data_format: str = "NWC",
    dilations: Union[int, Tuple[int]] = 1,
    bias: Optional[startai.Array] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 1-D transpose convolution given 3-D input x and filters
    arrays.

    Parameters
    ----------
    x
        Input image *[batch_size,w,d_in]* or *[batch_size,d_in,w]*.
    filters
        Convolution filters *[fw,d_out,d_in]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        Either ‘SAME’ (padding so that the output's shape is the same as the
        input's), or ‘VALID’ (padding so that the output's shape is `output_shape`).
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
    bias
        Bias array of shape *[d_out]*.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the transpose convolution operation.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 28, 3])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 6, 3])
    >>> y = startai.conv1d_transpose(x, filters, 2, 'SAME')
    >>> print(y.shape)
    startai.Shape(1, 56, 6)

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 128, 64])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[1, 64, 64])
    >>> startai.conv1d_transpose(x, filters, 1, 'VALID', out=x)
    >>> print(x.shape)
    startai.Shape(1, 128, 64)

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 256, 64])
    >>> y = startai.zeros((1, 258, 32))
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 32, 64])
    >>> startai.conv1d_transpose(x, filters, 1, 'VALID', out=y)
    >>> print(y.shape)
    startai.Shape(1, 258, 32)

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array(
    ...         startai.random_normal(mean=0, std=1, shape=[1, 256, 128]))
    >>> filters = startai.native_array(
    ...         startai.random_normal(mean=0, std=1, shape=[3, 32, 128]))
    >>> y = startai.conv1d_transpose(x, filters, 2, 'SAME')
    >>> print(y.shape)
    startai.Shape(1, 512, 32)

    With one :class:`startai.Container` input:

    >>> x = startai.full((1, 6, 1), 2.7)
    >>> a = startai.random_normal(mean=0, std=1, shape=[3, 1, 1])
    >>> b = startai.random_normal(mean=0, std=1, shape=[3, 1, 1])
    >>> filters = startai.Container(a=a, b=b)
    >>> y = startai.conv1d_transpose(x, filters, 1, 'VALID', dilations=2)
    >>> print(y.shape)
    {
        a: startai.Shape(1, 10, 1),
        b: startai.Shape(1, 10, 1)
    }

    With multiple :class:`startai.Container` inputs:

    >>> a = startai.random_normal(mean=0, std=1, shape=[1, 14, 3])
    >>> b = startai.random_normal(mean=0, std=1, shape=[1, 28, 3])
    >>> c = startai.random_normal(mean=0, std=1, shape=[6, 3, 3])
    >>> d = startai.random_normal(mean=0, std=1, shape=[6, 3, 3])
    >>> x = startai.Container(a=a, b=b)
    >>> filters = startai.Container(c=c, d=d)
    >>> y = startai.conv1d_transpose(x, filters, 2, 'SAME')
    >>> print(y.shape)
    {
        a: {
            c: startai.Shape(1, 28, 3),
            d: startai.Shape(1, 28, 3)
        },
        b: {
            c: startai.Shape(1, 56, 3),
            d: startai.Shape(1, 56, 3)
        },
        c: {
            c: startai.Shape(6, 6, 3),
            d: startai.Shape(6, 6, 3)
        },
        d: {
            c: startai.Shape(6, 6, 3),
            d: startai.Shape(6, 6, 3)
        }
    }
    """
    return current_backend(x).conv1d_transpose(
        x,
        filters,
        strides,
        padding,
        output_shape=output_shape,
        filter_format=filter_format,
        data_format=data_format,
        dilations=dilations,
        bias=bias,
        out=out,
    )


@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def conv2d(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int, int]],
    padding: Union[str, int, Sequence[Tuple[int, int]]],
    /,
    *,
    data_format: str = "NHWC",
    filter_format: str = "channel_last",
    x_dilations: Union[int, Tuple[int, int]] = 1,
    dilations: Union[int, Tuple[int, int]] = 1,
    bias: Optional[startai.Array] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 2-D convolution given 4-D input x and filters arrays.

    Parameters
    ----------
    x
        Input image *[batch_size,h,w,d_in]* or *[batch_size,d_in,h,w]*.
    filters
        Convolution filters *[fh,fw,d_in,d_out]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
        padding), or a sequence of n (low, high) integer pairs that give the padding to
        apply before and after each spatial dimension.
    data_format
        The ordering of the dimensions in the input, one of "NHWC" or "NCHW". "NHWC"
        corresponds to inputs with shape (batch_size, height, width, channels), while
        "NCHW" corresponds to input with shape (batch_size, channels, height, width).
    filter_format
        Either "channel_first" or "channel_last". "channel_first" corresponds to "OIHW",
         input data formats, while "channel_last" corresponds to "HWIO".
     x_dilations
        The dilation factor for each dimension of input. (Default value = 1)
    dilations
        The dilation factor for each dimension of input. (Default value = 1)
    bias
        Bias array of shape *[d_out]*.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the convolution operation.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[[[1.], [2.0],[3.]],
    ...                 [[1.], [2.0],[3.]],
    ...                 [[1.], [2.0],[3.]]]])
    >>> filters = startai.array([[[[0.]],[[1.]],[[0.]]],
    ...                      [[[0.]],[[1.]], [[0.]]],
    ...                      [[[0.]],[[1.]], [[0.]]]])
    >>> result = startai.conv2d(x, filters, 1, 'SAME', data_format='NHWC', dilations=1)
    >>> print(result)
    startai.array([[
              [[2.],[4.],[6.]],
              [[3.],[6.],[9.]],
              [[2.],[4.],[6.]]
              ]])

    With one :class:`startai.Container` input:

    >>> x = startai.Container(a=startai.array([[[[1.], [2.0],[3.]],
    ...                                 [[1.], [2.0],[3.]],
    ...                                 [[1.], [2.0],[3.]]]]))
    >>> filters = startai.eye(3, 3).reshape((3, 3, 1, 1)).astype(startai.float32)
    >>> result = startai.conv2d(x, filters, 2, 'SAME', data_format='NHWC', dilations= 1)
    >>> print(result)
    {
        a:startai.array([[[[3.], [3.]], [[1.], [5.]]]])
    }

    With multiple :class:`startai.Container` inputs:

    >>> x = startai.Container(a = startai.eye(3, 3).reshape((1, 3, 3, 1)),
    ...                   b = startai.eye(4, 4).reshape((1, 4, 4, 1)),
    ...                   c = startai.eye(5, 5).reshape((1, 5, 5, 1)))
    >>> filters = startai.array([[1, 1, 1],
    ...                      [0, 1, 1],
    ...                      [0, 0, 1]], dtype = startai.float32).reshape((3, 3, 1, 1))
    >>> result = startai.conv2d(x, filters, 2, 'SAME')
    >>> print(result)
    {
        a:startai.array([[[[2.], [0.]], [[1.], [2.]]]]),
        b:startai.array([[[[3.], [0.]], [[1.], [2.]]]]),
        c:startai.array([[[[2.], [0.], [0.]],
                      [[1.], [3.], [0.]],
                      [[0.], [1.], [2.]]
                    ]])
    }

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.Container(a = startai.eye(3, 3).reshape((1, 3, 3, 1)),
    ...                   b = startai.eye(5, 5).reshape((1, 5, 5, 1)))
    >>> filters = startai.array([[2, 0, 1],
    ...                      [1, 3, 1],
    ...                      [0, 1, 1]], dtype = startai.float32).reshape((3, 3, 1, 1))
    >>> result = startai.conv2d(x, filters, 2, 'SAME')
    >>> print(result)
    {
        a:startai.array([[[[4.],[0.]],[[1.],[5.]]]]),
        b:startai.array([[[[4.],[0.],[0.]],[[1.],[6.],[0.]],[[0.],[1.],[5.]]]])
    }
    """
    return current_backend(x).conv2d(
        x,
        filters,
        strides,
        padding,
        data_format=data_format,
        filter_format=filter_format,
        x_dilations=x_dilations,
        dilations=dilations,
        bias=bias,
        out=out,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@inputs_to_native_shapes
@to_native_arrays_and_back
@handle_array_function
@handle_device
def conv2d_transpose(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int, int]],
    padding: str,
    /,
    *,
    output_shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
    filter_format: str = "channel_last",
    data_format: str = "NHWC",
    dilations: Union[int, Tuple[int, int]] = 1,
    bias: Optional[startai.Array] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 2-D transpose convolution given 4-D input x and filters
    arrays.

    Parameters
    ----------
    x
        Input image *[batch_size,h,w,d_in]* or *[batch_size,d_in,h,w]*.
    filters
        Convolution filters *[fh,fw,d_out,d_in]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        Either ‘SAME’ (padding so that the output's shape is the same as the
        input's), or ‘VALID’ (padding so that the output's shape is `output_shape`).
    output_shape
        Shape of the output (Default value = None)
    data_format
        The ordering of the dimensions in the input, one of "NHWC" or "NCHW". "NHWC"
        corresponds to inputs with shape (batch_size, height, width, channels), while
        "NCHW" corresponds to input with shape (batch_size, channels, height, width).
    filter_format
        Either "channel_first" or "channel_last". "channel_first" corresponds
        to "IOHW",input data formats, while "channel_last" corresponds to "HWOI".
    x_dilations
        The dilation factor for each dimension of input. (Default value = 1)
    dilations
        The dilation factor for each dimension of input. (Default value = 1)
    bias
        Bias array of shape *[d_out]*.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the transpose convolution operation.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:
    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 28, 28, 3])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 6, 3])
    >>> y = startai.conv2d_transpose(x,filters,2,'SAME')
    >>> print(y.shape)
    startai.Shape(1, 56, 56, 6)

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 128, 128, 64])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[1, 1, 64, 64])
    >>> startai.conv2d_transpose(x,filters,1,'VALID',out=x)
    >>> print(x.shape)
    startai.Shape(1, 128, 128, 64)

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 256, 256, 64])
    >>> y = startai.zeros((1, 258, 258, 32))
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 32, 64])
    >>> startai.conv2d_transpose(x,filters,[1, 1, 1],'VALID',out=y)
    >>> print(y.shape)
    startai.Shape(1, 258, 258, 32)

    With one :class:`startai.Container` inputs:
    >>> x = startai.full((1, 6, 6, 1), 2.7)
    >>> a = startai.random_normal(mean=0, std=1, shape=[3, 3, 1, 1])
    >>> b = startai.random_normal(mean=0, std=1, shape=[3, 3, 1, 1])
    >>> filters = startai.Container(a=a, b=b)
    >>> y = startai.conv2d_transpose(x,filters,1,'VALID',dilations=2)
    >>> print(y.shape)
    {
        a: startai.Shape(1, 10, 10, 1),
        b: startai.Shape(1, 10, 10, 1)
    }

    With multiple :class:`startai.Container` inputs:
    >>> a = startai.random_normal(mean=0, std=1, shape=[1, 14, 14, 3])
    >>> b = startai.random_normal(mean=0, std=1, shape=[1, 28, 28, 3])
    >>> c = startai.random_normal(mean=0, std=1, shape=[6, 3, 3, 3])
    >>> d = startai.random_normal(mean=0, std=1, shape=[6, 3, 3, 3])
    >>> x = startai.Container(a=a, b=b)
    >>> filters = startai.Container(c=c, d=d)
    >>> y = startai.conv2d_transpose(x,filters,2,'SAME')
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
    return current_backend(x).conv2d_transpose(
        x,
        filters,
        strides,
        padding,
        output_shape=output_shape,
        filter_format=filter_format,
        data_format=data_format,
        dilations=dilations,
        bias=bias,
        out=out,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def depthwise_conv2d(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int, int]],
    padding: Union[str, Sequence[Tuple[int, int]]],
    /,
    *,
    data_format: str = "NHWC",
    dilations: Union[int, Tuple[int, int]] = 1,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 2-D depthwise convolution given 4-D input ``x`` and filters
    arrays.

    Parameters
    ----------
    x
        Input image *[batch_size,h,w,d_in]* or *[batch_size,d_in,h,w]*.
    filters
        Convolution filters *[fh,fw,d_in]*. (d_in must be the same as d from x)
    strides
        The stride of the sliding window for each dimension of input.
    padding
        either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
        padding), or a sequence of n (low, high) integer pairs that give the padding to
        apply before and after each spatial dimension.
    data_format
        The ordering of the dimensions in the input, one of "NHWC" or "NCHW". "NHWC"
        corresponds to inputs with shape (batch_size, height, width, channels), while
        "NCHW" corresponds to input with shape (batch_size, channels, height, width).
    dilations
        The dilation factor for each dimension of input. (Default value = 1)
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the convolution operation.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 28, 28, 3])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 3])
    >>> y = startai.depthwise_conv2d(x, filters, (1, 1), 'VALID')
    >>> print(y.shape)
    startai.Shape(1, 26, 26, 3)

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 32, 32, 3])
    >>> y = startai.zeros((1, 16, 16, 3))
    >>> filters = startai.random_normal(mean=0, std=1, shape=[5, 5, 3])
    >>> startai.depthwise_conv2d(x, filters, [2, 2], 'SAME', out=y)
    >>> print(y.shape)
    startai.Shape(1, 16, 16, 3)

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 64, 64, 32])
    >>> y = startai.zeros((1, 61, 61, 32))
    >>> filters = startai.random_normal(mean=0, std=1, shape=[4, 4, 32])
    >>> startai.depthwise_conv2d(x, filters, [1, 1], 'VALID', out=y)
    >>> print(x.shape)
    startai.Shape(1, 64, 64, 32)

    With :class:`startai.NativeArray` input:

    >>> x = startai.native_array(startai.random_normal(mean=0, std=1, shape=[1, 7, 7, 64]))
    >>> filters = startai.native_array(startai.random_normal(mean=0, std=1, shape=[3, 3, 64]))
    >>> y = startai.depthwise_conv2d(x, filters, [1, 1], 'SAME')
    >>> print(y.shape)
    startai.Shape(1, 7, 7, 64)

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.eye(6, 6).reshape((1, 6, 6, 1)) #NHWC
    >>> a = startai.array([[1., 1., 1.], [1., -8., 1.], [1., 1., 1.]]).expand_dims(axis=-1)
    >>> b = startai.array([[1., 1., 1.],
    ...                [1., 1., 1.],
    ...                [1., 1., 1.]]).expand_dims(axis=-1) / 9.0
    >>> filters = startai.Container(a = a, b = b)
    >>> y = startai.depthwise_conv2d(x, filters, 1, 'VALID', dilations=2)
    >>> print(y)
    {
        a: startai.array([[[[-6.],
                        [0.]],
                       [[0.],
                        [-6.]]]]),
        b: startai.array([[[[0.33333334],
                        [0.]],
                       [[0.],
                        [0.33333334]]]])
    }

    With a mix of :class:`startai.Array`, code:`startai.NativeArray`
    and :class:`startai.Container` inputs:

    >>> x = startai.eye(6, 6).reshape((1, 6, 6, 1)) #NHWC
    >>> y = startai.native_array(startai.eye(6, 6).reshape((1, 6, 6, 1)))
    >>> inp = startai.Container(x = x, y = y)
    >>> filter = startai.array([[1., 1., 1.],
    ...                     [1., -8., 1.],
    ...                     [1., 1., 1.]]).expand_dims(axis=-1)
    >>> y = startai.depthwise_conv2d(inp, filter, 1, 'VALID', dilations=2)
    >>> print(y)
    {
        x: startai.array([[[[-6.],
                        [0.]],
                       [[0.],
                        [-6.]]]]),
        y: startai.array([[[[-6.],
                        [0.]],
                       [[0.],
                        [-6.]]]])
    }
    """
    return current_backend(x).depthwise_conv2d(
        x,
        filters,
        strides,
        padding,
        data_format=data_format,
        dilations=dilations,
        out=out,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def conv3d(
    x: Union[startai.Array, startai.NativeArray, startai.Container],
    filters: Union[startai.Array, startai.NativeArray, startai.Container],
    strides: Union[int, Tuple[int, int, int]],
    padding: Union[str, int, Sequence[Tuple[int, int]]],
    /,
    *,
    data_format: str = "NDHWC",
    filter_format: str = "channel_last",
    x_dilations: Union[int, Tuple[int, int, int]] = 1,
    dilations: Union[int, Tuple[int, int, int]] = 1,
    bias: Optional[startai.Array] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 3-D convolution given 5-D input x and filters arrays.

    Parameters
    ----------
    x
        Input volume *[batch_size,d,h,w,d_in]* or *[batch_size,d_in,d,h,w]*.
    filters
        Convolution filters *[fd,fh,fw,d_in,d_out]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
        padding), or a sequence of n (low, high) integer pairs that give the padding to
        apply before and after each spatial dimension.
    data_format
        The ordering of the dimensions in the input, one of "NDHWC" or "NCDHW". "NDHWC"
        corresponds to inputs with shape (batch_size, depth, height, width, channels),
        while "NCDHW" corresponds to input with shape (batch_size, channels, depth,
        height, width).
    filter_format
        Either "channel_first" or "channel_last". "channel_first" corresponds
        to "OIDHW",input data formats, while "channel_last" corresponds to "DHWIO".
     x_dilations
        The dilation factor for each dimension of input. (Default value = 1)
    dilations
        The dilation factor for each dimension of input. (Default value = 1)
    bias
        Bias array of shape *[d_out]*
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the convolution operation.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`startai.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.array([[[1., 2. ,1.], [1., 2. ,1.], [1., 2. ,1.]],
    ...         [[1., 2. ,1.], [1., 2. ,1.], [1., 2. ,1.]],
    ...         [[1., 2. ,1.], [1., 2. ,1.], [1., 2. ,1.]]]).reshape((1, 3, 3, 3, 1))
    >>> filters = startai.array([[[0.,1.,0.],
    ...                       [0.,1.,0.],
    ...                       [0.,1.,0.]]]).reshape((1,3,3,1,1))
    >>> result = startai.conv3d(x, filters, 1, 'SAME', data_format='NDHWC', dilations=1)
    >>> print(result)
    startai.array([[[[[2.],[4.],[2.]],[[3.],[6.],[3.]],[[2.],[4.],[2.]]],
                [[[2.],[4.],[2.]],[[3.],[6.],[3.]],[[2.],[4.],[2.]]],
                [[[2.],[4.],[2.]],[[3.],[6.],[3.]],[[2.],[4.],[2.]]]]])

    With one :class:`startai.Container` input:

    >>> x = startai.Container(a = startai.ones((1, 3, 3, 3, 1)).astype(startai.float32))
    >>> filters = startai.ones((3, 3, 3, 1, 1)).astype(startai.float32)
    >>> result = startai.conv3d(x, filters, 2, 'SAME')
    >>> print(result)
    {
        a: startai.array([[[[[8.],[8.]],[[8.],[8.]]],[[[8.],[8.]],[[8.],[8.]]]]])
    }

    With multiple :class:`startai.Container` input:

    >>> x = startai.Container( a = startai.random_normal(mean = 0, std = 1,
    ...                        shape = [1, 3, 5, 5, 1]),
    ...                    b = startai.random_normal(mean = 0, std = 1,
    ...                        shape = [1, 5, 32 ,32, 1]),
    ...                    c = startai.random_normal(mean = 0, std = 1,
    ...                        shape = [1, 32, 32, 32, 1]))
    >>> filters = startai.ones((3, 5, 5, 1, 3)).astype(startai.float32)
    >>> result = startai.conv3d(x, filters, 1, 'SAME')
    >>> print(result.cont_shapes)
    {
        a: startai.Shape(1, 3, 5, 5, 3),
        b: startai.Shape(1, 5, 32, 32, 3),
        c: startai.Shape(1, 32, 32, 32, 3)
    }
    """
    return current_backend(x).conv3d(
        x,
        filters,
        strides,
        padding,
        data_format=data_format,
        filter_format=filter_format,
        x_dilations=x_dilations,
        dilations=dilations,
        bias=bias,
        out=out,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@inputs_to_native_shapes
@to_native_arrays_and_back
@handle_array_function
@handle_device
def conv3d_transpose(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int, int, int]],
    padding: str,
    /,
    *,
    output_shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
    filter_format: str = "channel_last",
    data_format: str = "NDHWC",
    dilations: Union[int, Tuple[int, int, int]] = 1,
    bias: Optional[startai.Array] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 3-D transpose convolution given 5-D input x and filters
    arrays.

    Parameters
    ----------
    x
        Input volume *[batch_size,d,h,w,d_in]* or *[batch_size,d_in,d,h,w]*.
    filters
        Convolution filters *[fd,fh,fw,d_out,d_in]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        Either ‘SAME’ (padding so that the output's shape is the same as the
        input's), or ‘VALID’ (padding so that the output's shape is `output_shape`).
    output_shape
        Shape of the output (Default value = None)
    filter_format
        Either "channel_first" or "channel_last". "channel_first" corresponds
        to "IODHW",input data formats, while "channel_last" corresponds to "DHWOI".
    data_format
        The ordering of the dimensions in the input, one of "NDHWC" or "NCDHW". "NDHWC"
        corresponds to inputs with shape (batch_size, depth, height, width, channels),
        while "NCDHW" corresponds to input with shape (batch_size, channels, depth,
        height, width).
    dilations
        The dilation factor for each dimension of input. (Default value = 1)
    bias
        Bias array of shape *[d_out]*
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the transpose convolution operation.

    Examples
    --------
    With :class:`startai.Array` input:

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 3, 28, 28, 3])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 6, 3])
    >>> y = startai.conv3d_transpose(x, filters, [2, 2, 2], 'SAME')
    >>> print(y.shape)
    startai.Shape(1, 6, 56, 56, 6)

    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 3, 64, 64, 3])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 6, 3])
    >>> y = startai.conv3d_transpose(x, filters, [2, 2, 2], 'VALID', dilations=[1, 1, 1])
    >>> print(y.shape)
    startai.Shape(1, 7, 129, 129, 6)

    With :class:`startai.Container` inputs:

    >>> a = startai.random_normal(mean=0, std=1, shape=[1, 3, 14, 14, 3])
    >>> b = startai.random_normal(mean=0, std=1, shape=[1, 3, 28, 28, 3])
    >>> c = startai.random_normal(mean=0, std=1, shape=[6, 3, 3, 3, 3])
    >>> d = startai.random_normal(mean=0, std=1, shape=[6, 3, 3, 3, 3])
    >>> x = startai.Container(a=a, b=b)
    >>> filters = startai.Container(c=c, d=d)
    >>> y = startai.conv3d_transpose(x, filters, [2, 2, 2], 'SAME')
    >>> print(y.shape)
    {
        a: {
            c: startai.Shape(1, 6, 28, 28, 3),
            d: startai.Shape(1, 6, 28, 28, 3)
        },
        b: {
            c: startai.Shape(1, 6, 56, 56, 3),
            d: startai.Shape(1, 6, 56, 56, 3)
        },
        c: {
            c: startai.Shape(6, 6, 6, 6, 3),
            d: startai.Shape(6, 6, 6, 6, 3)
        },
        d: {
            c: startai.Shape(6, 6, 6, 6, 3),
            d: startai.Shape(6, 6, 6, 6, 3)
        }
    }

    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:

    >>> x = startai.full((1, 6, 6, 6, 1), 2.7)
    >>> a = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 1, 1])
    >>> b = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 1, 1])
    >>> filters = startai.Container(a=a, b=b)
    >>> y = startai.conv3d_transpose(x, filters, [1, 1, 1], 'VALID', dilations=[1, 1, 1])
    >>> print(y.shape)
    {
        a: startai.Shape(1, 8, 8, 8, 1),
        b: startai.Shape(1, 8, 8, 8, 1)
    }

    >>> x = startai.full((1, 6, 6, 6, 1), 1.23)
    >>> a = startai.array(startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 1, 1]))
    >>> b = startai.array(startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 1, 1]))
    >>> filters = startai.Container(a=a, b=b)
    >>> y = startai.conv3d_transpose(x, filters, [1, 1, 1], 'VALID', dilations=[1, 1, 1])
    >>> print(y.shape)
    {
        a: startai.Shape(1, 8, 8, 8, 1),
        b: startai.Shape(1, 8, 8, 8, 1)
    }
    """
    return current_backend(x).conv3d_transpose(
        x,
        filters,
        strides,
        padding,
        output_shape=output_shape,
        filter_format=filter_format,
        data_format=data_format,
        dilations=dilations,
        bias=bias,
        out=out,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@to_native_arrays_and_back
@handle_array_function
@handle_device
def conv_general_dilated(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]],
    padding: Union[str, int, Sequence[Tuple[int, int]]],
    /,
    *,
    dims: int = 2,
    data_format: str = "channel_last",
    filter_format: str = "channel_last",
    feature_group_count: int = 1,
    x_dilations: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]] = 1,
    dilations: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]] = 1,
    bias: Optional[Union[startai.Array, startai.NativeArray]] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 1-D, 2-D, and 3-D convolution given 3-D, 4-D and 5-D input x
    respectively and filters arrays.

    Parameters
    ----------
    x
        Input image *[batch_size,d,h,w,d_in]* or *[batch_size,d_in,d,h,w]*.
    filters
        Convolution filters *[fd,fh,fw,d_in/feature_group_count,d_out]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
        padding), or a sequence of n (low, high) integer pairs that give the padding to
        apply before and after each spatial dimension.
    dims
        Either 1, 2, or 3 corresponding to 1-D, 2-D, and 3-D convolution.
    data_format
        Either "channel_first" or "channel_last". "channel_first" corresponds to "NCW",
        "NCHW", "NCDHW" input data formatS for 1-D, 2-D, 3-D convolution respectively,
        while "channel_last" corresponds to "NWC", "NHWC", "NDHWC" respectively.
    filter_format
        Either "channel_first" or "channel_last". "channel_first" corresponds to "OIW",
        "OIHW", "OIDHW" input data formats for 1-D, 2-D, 3-D convolution respectively,
        while "channel_last" corresponds to "WIO", "HWIO", "DHWIO" respectively.
    feature_group_count
         split input into groups, d_in should be divisible by the number of groups.
         (Default value = 1)
    x_dilations
        The dilation factor for each dimension of input. (Default value = 1)
    dilations
        The dilation factor for each dimension of filter. (Default value = 1)
    bias
        Bias array of shape *[d_out]*.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the transpose convolution operation.
    """
    return current_backend(x).conv_general_dilated(
        x,
        filters,
        strides,
        padding,
        dims=dims,
        data_format=data_format,
        filter_format=filter_format,
        feature_group_count=feature_group_count,
        x_dilations=x_dilations,
        dilations=dilations,
        bias=bias,
        out=out,
    )


@handle_exceptions
@handle_backend_invalid
@handle_nestable
@handle_array_like_without_promotion
@handle_out_argument
@inputs_to_native_shapes
@to_native_arrays_and_back
@handle_array_function
@handle_device
def conv_general_transpose(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]],
    padding: str,
    /,
    *,
    dims: int = 2,
    output_shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
    filter_format: str = "channel_last",
    data_format: str = "channel_last",
    dilations: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]] = 1,
    feature_group_count: int = 1,
    bias: Optional[Union[startai.Array, startai.NativeArray]] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 1-D, 2-D, and 3-D transpose convolution given 3-D, 4-D and 5-D
    input x respectively and filters arrays.

    Parameters
    ----------
    x
        Input image *[batch_size,d,h,w,d_in]* or *[batch_size,d_in,d,h,w]*.
    filters
        Convolution filters *[fd,fh,fw,d_out,d_in]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        Either ‘SAME’ (padding so that the output's shape is the same as the
        input's), or ‘VALID’ (padding so that the output's shape is `output_shape`).
    dims
        Either 1, 2, or 3 corresponding to 1-D, 2-D, and 3-D convolution.
    output_shape
        Shape of the output.
    filter_format
        Either "channel_first" or "channel_last". "channel_first" corresponds
        to "IODHW",input data formats, while "channel_last" corresponds to "DHWOI".
    data_format
        Either "channel_first" or "channel_last". "channel_first" corresponds to "NCW",
        "NCHW", "NCDHW" input data formatS for 1-D, 2-D, 3-D convolution respectively,
        while "channel_last" corresponds to "NWC", "NHWC", "NDHWC" respectively.
    dilations
        The dilation factor for each dimension of input. (Default value = 1)
    feature_group_count
         split input into groups, d_in should be divisible by the number of groups.
    bias
        Bias array of shape *[d_out]*.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the transpose convolution operation.

    Examples
    --------
    With :class:`startai.Array` input:
    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 3, 28, 28, 3])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 6, 3])
    >>> y = startai.conv3d_transpose(x, filters, [2, 2, 2], 'SAME')
    >>> print(y.shape)
    startai.Shape(1, 6, 56, 56, 6)
    >>> x = startai.random_normal(mean=0, std=1, shape=[1, 3, 64, 64, 3])
    >>> filters = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 6, 3])
    >>> y = startai.conv3d_transpose(x, filters, [2, 2, 2], 'VALID', dilations=[1, 1, 1])
    >>> print(y.shape)
    startai.Shape(1, 7, 129, 129, 6)
    With :class: 'startai.Container' inputs:
    >>> a = startai.random_normal(mean=0, std=1, shape=[1, 3, 14, 14, 3])
    >>> b = startai.random_normal(mean=0, std=1, shape=[1, 3, 28, 28, 3])
    >>> c = startai.random_normal(mean=0, std=1, shape=[6, 3, 3, 3, 3])
    >>> d = startai.random_normal(mean=0, std=1, shape=[6, 3, 3, 3, 3])
    >>> x = startai.Container(a=a, b=b)
    >>> filters = startai.Container(c=c, d=d)
    >>> y = startai.conv3d_transpose(x, filters, [2, 2, 2], 'SAME')
    >>> print(y.shape)
    {
        a: {
            c: startai.Shape(1, 6, 28, 28, 3),
            d: startai.Shape(1, 6, 28, 28, 3)
        },
        b: {
            c: startai.Shape(1, 6, 56, 56, 3),
            d: startai.Shape(1, 6, 56, 56, 3)
        },
        c: {
            c: startai.Shape(6, 6, 6, 6, 3),
            d: startai.Shape(6, 6, 6, 6, 3)
        },
        d: {
            c: startai.Shape(6, 6, 6, 6, 3),
            d: startai.Shape(6, 6, 6, 6, 3)
        }
    }
    With a mix of :class:`startai.Array` and :class:`startai.Container` inputs:
    >>> x = startai.full((1, 6, 6, 6, 1), 2.7)
    >>> a = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 1, 1])
    >>> b = startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 1, 1])
    >>> filters = startai.Container(a=a, b=b)
    >>> y = startai.conv3d_transpose(x, filters, [1, 1, 1], 'VALID', dilations=[1, 1, 1])
    >>> print(y.shape)
    {
        a: startai.Shape(1, 8, 8, 8, 1),
        b: startai.Shape(1, 8, 8, 8, 1)
    }
    >>> x = startai.full((1, 6, 6, 6, 1), 1.23)
    >>> a = startai.array(startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 1, 1]))
    >>> b = startai.array(startai.random_normal(mean=0, std=1, shape=[3, 3, 3, 1, 1]))
    >>> filters = startai.Container(a=a, b=b)
    >>> y = startai.conv3d_transpose(x, filters, [1, 1, 1], 'VALID', dilations=[1, 1, 1])
    >>> print(y.shape)
    {
        a: startai.Shape(1, 8, 8, 8, 1),
        b: startai.Shape(1, 8, 8, 8, 1)
    }
    """
    return current_backend(x).conv_general_transpose(
        x,
        filters,
        strides,
        padding,
        dims=dims,
        output_shape=output_shape,
        filter_format=filter_format,
        data_format=data_format,
        dilations=dilations,
        feature_group_count=feature_group_count,
        bias=bias,
        out=out,
    )


@handle_exceptions
@handle_array_like_without_promotion
@handle_out_argument
@inputs_to_native_shapes
@handle_array_function
def conv(
    x: Union[startai.Array, startai.NativeArray],
    filters: Union[startai.Array, startai.NativeArray],
    strides: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]],
    padding: Union[str, Sequence[Tuple[int, int]]],
    /,
    *,
    transpose: bool = False,
    dims: int = 2,
    output_shape: Optional[Union[startai.Shape, startai.NativeShape]] = None,
    data_format: str = "channel_last",
    filter_format: str = "channel_last",
    feature_group_count: int = 1,
    x_dilations: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]] = 1,
    dilations: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]] = 1,
    bias: Optional[Union[startai.Array, startai.NativeArray]] = None,
    out: Optional[startai.Array] = None,
) -> startai.Array:
    """Compute a 1-D, 2-D, and 3-D transpose or dilated convolution given 3-D,
    4-D and 5-D input x respectively and filters arrays.

    Parameters
    ----------
    x
        Input image *[batch_size,d,h,w,d_in]* or *[batch_size,d_in,d,h,w]*.
    filters
        Convolution filters *[fd,fh,fw,d_in/feature_group_count,d_out]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        either the string ‘SAME’ (padding with zeros evenly), the string ‘VALID’ (no
        padding), or a sequence of n (low, high) integer pairs that give the padding to
        apply before and after each spatial dimension.
    transpose
        True for computing transpose convolution, and False for dilated convolution.
        When True, `x_dilations` must be 1 (the default).
    dims
        Either 1, 2, or 3 corresponding to 1-D, 2-D, and 3-D convolution.
    output_shape
        Shape of the output (Default value = None)
    data_format
        Either "channel_first" or "channel_last". "channel_first" corresponds to "NCW",
        "NCHW", "NCDHW" input data formatS for 1-D, 2-D, 3-D convolution respectively,
        while "channel_last" corresponds to "NWC", "NHWC", "NDHWC" respectively.
    filter_format
        Either "channel_first" or "channel_last". "channel_first" corresponds to "OIW",
        "OIHW", "OIDHW" input data formats for 1-D, 2-D, 3-D convolution respectively,
        while "channel_last" corresponds to "WIO", "HWIO", "DHWIO" respectively.
    feature_group_count
         split input into groups, d_in should be divisible by the number of groups.
         (Default value = 1)
    x_dilations
        The dilation factor for each dimension of input. (Default value = 1)
    dilations
        The dilation factor for each dimension of input. (Default value = 1)
    bias
        Bias array of shape *[d_out]*.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The result of the transpose or dilated convolution operation.
    """
    if transpose:
        return conv_general_transpose(
            x,
            filters,
            strides,
            padding,
            dims=dims,
            output_shape=output_shape,
            data_format=data_format,
            dilations=dilations,
            feature_group_count=feature_group_count,
            bias=bias,
            out=out,
        )
    else:
        return conv_general_dilated(
            x,
            filters,
            strides,
            padding,
            dims=dims,
            data_format=data_format,
            filter_format=filter_format,
            feature_group_count=feature_group_count,
            x_dilations=x_dilations,
            dilations=dilations,
            bias=bias,
            out=out,
        )


# LSTM #


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def lstm_update(
    x: Union[startai.Array, startai.NativeArray],
    init_h: Union[startai.Array, startai.NativeArray],
    init_c: Union[startai.Array, startai.NativeArray],
    kernel: Union[startai.Array, startai.NativeArray],
    recurrent_kernel: Union[startai.Array, startai.NativeArray],
    /,
    *,
    bias: Optional[Union[startai.Array, startai.NativeArray]] = None,
    recurrent_bias: Optional[Union[startai.Array, startai.NativeArray]] = None,
    time_major: bool = False,
) -> Tuple[startai.Array, Tuple[startai.Array, startai.Array]]:
    """Perform long-short term memory update by unrolling time dimension of
    input array.

    Parameters
    ----------
    x
        input tensor of LSTM layer *[batch_shape, t, in]* if time_major=False,
        else *[t, batch_shape, in]*.
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
    time_major
        whether or not the input tensor `x` has the time dimension before batch dim.

    Returns
    -------
    ret
        hidden state for all timesteps of shape *[batch_shape,t,out]* if time_major
        is False, else *[t, batch_shape, out]*, and a tuple containing the final cell
        states, both of shape *[batch_shape,out]*.
    """
    # ToDo: test_lstm_update needs to be fixed
    if time_major:
        x = startai.swapaxes(x, 0, 1)
    # get shapes
    x_shape = list(x.shape)
    batch_shape = x_shape[:-2]
    timesteps = x_shape[-2]
    input_channels = x_shape[-1]
    x_flat = startai.reshape(x, (-1, input_channels))

    # input kernel
    Wi = kernel
    Wi_x = startai.reshape(
        startai.matmul(x_flat, Wi) + (bias if bias is not None else 0),
        batch_shape + [timesteps, -1],
    )
    Wii_x, Wif_x, Wig_x, Wio_x = startai.split(Wi_x, num_or_size_splits=4, axis=-1)

    # recurrent kernel
    Wh = recurrent_kernel

    # lstm states
    ht = init_h
    ct = init_c

    # lstm outputs
    hts_list = []

    # unrolled time dimension with lstm steps
    for Wii_xt, Wif_xt, Wig_xt, Wio_xt in zip(
        startai.unstack(Wii_x, axis=-2),
        startai.unstack(Wif_x, axis=-2),
        startai.unstack(Wig_x, axis=-2),
        startai.unstack(Wio_x, axis=-2),
    ):
        htm1 = ht
        ctm1 = ct

        Wh_htm1 = startai.matmul(htm1, Wh) + (
            recurrent_bias if recurrent_bias is not None else 0
        )
        Whi_htm1, Whf_htm1, Whg_htm1, Who_htm1 = startai.split(
            Wh_htm1, num_or_size_splits=4, axis=-1
        )

        it = startai.sigmoid(Wii_xt + Whi_htm1)
        ft = startai.sigmoid(Wif_xt + Whf_htm1)
        gt = startai.tanh(Wig_xt + Whg_htm1)
        ot = startai.sigmoid(Wio_xt + Who_htm1)
        ct = ft * ctm1 + it * gt
        ht = ot * startai.tanh(ct)

        hts_list.append(startai.expand_dims(ht, axis=-2))

    ret = startai.concat(hts_list, axis=-2)
    if time_major:
        ret = startai.swapaxes(ret, 0, 1)

    return ret, (ht, ct)


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def lstm(
    input: startai.Array,
    initial_states: Tuple[startai.Array],
    all_weights: Tuple[startai.Array],
    num_layers: int,
    dropout: float,
    train: bool,
    bidirectional: bool,
    batch_first: bool = False,
    batch_sizes: Sequence = None,
    weights_transposed: bool = False,
    has_ih_bias: bool = True,
    has_hh_bias: bool = True,
):
    """Applies a multi-layer long-short term memory to an input sequence.

    Parameters
    ----------
    input
        input array of shape (seq_len, batch, input_size) when `batch_first` is False
        or (batch, seq_len, input_size) when `batch_first` is True
    initial_states
        tuple of two arrays (h_0, c_0) where h_0 is the initial hidden state of shape
        (num_layers * num_directions, batch, hidden_size) and c_0 is the initial cell
        state of shape (num_layers * num_directions, batch, hidden_size)

        (num_directions being 2 when `bidirectional`, otherwise 1)
    all_weights
        tuple of arrays representing the learnable weights of the lstm, with each
        layer having up to four arrays (w_ih, w_hh, b_ih, b_hh) representing the weights
        and biases (if biases are being used)

        w_ih: weight of shape (4 * hidden_size, input_size)
        w_hh: weight of shape (4 * hidden_size, hidden_size)
        b_ih: bias of shape (4 * hidden_size,)
        b_hh: bias of shape (4 * hidden_size,)
    num_layers
        number of layers for the lstm to use
    dropout
        dropout rate
    train
        whether to run the lstm in train mode or eval mode
    bidirectional
        whether the lstm is bidirectional or unidirectional
    batch_first
        defines the data format of the input and output arrays
    batch_sizes
        specifies the batch size at each timestep, when the input is a packed sequence
    weights_transposed
        whether the weights are transposed compared to the format
        in which they are expected (input_size, 4 * hidden_size)
        rather than (4 * hidden_size, input_size)
    has_ih_bias
        whether the `all_weights` argument includes a input-hidden bias
    has_hh_bias
        whether the `all_weights` argument includes a hidden-hidden bias

    Returns
    -------
    output
        output array of shape (seq_len, batch, num_directions * hidden_size) or
        (batch, seq_len, num_directions * hidden_size), depending on `batch_first`
    h_outs
        final hidden state of shape (num_layers * num_directions, batch, hidden_size)
    c_outs
        final cell state of shape (num_layers * num_directions, batch, hidden_size)
    """
    # TODO: the test for this function needs to be fixed -
    # see startai_tests/test_startai/test_functional/test_nn/test_layers.py::test_lstm

    if weights_transposed:
        # transpose the weights if they are in the wrong format
        all_weights = [
            startai.swapaxes(weight, 1, 0) if weight.dim() == 2 else weight
            for weight in all_weights
        ]
    else:
        all_weights = list(all_weights)

    if (has_ih_bias and not has_hh_bias) or (has_hh_bias and not has_ih_bias):
        # insert zero biases into the weights where one set of biases is not used
        shapes = []
        for i in range(2, len(all_weights), 3):
            shapes.append(tuple(all_weights[i].shape))
        for i, shape in enumerate(shapes):
            idx = (i + 1) * 4 - (1 if has_ih_bias else 2)
            all_weights.insert(idx, startai.zeros(shape))
        has_ih_bias = True
        has_hh_bias = True

    weights_per_layer = 2
    if has_ih_bias:
        weights_per_layer += 1
    if has_hh_bias:
        weights_per_layer += 1

    assert len(all_weights) == num_layers * weights_per_layer * (1 + bidirectional)
    layer_weights = [
        all_weights[i : i + weights_per_layer]
        for i in range(0, len(all_weights), weights_per_layer)
    ]

    if batch_sizes is not None:
        input, batch_sizes = _pad_packed_sequence(input, batch_sizes)

    if batch_first:
        input = startai.swapaxes(input, 0, 1)

    if dropout and train:
        raise startai.utils.exceptions.StartaiNotImplementedException()

    unidirectional = not bidirectional

    h0, c0 = initial_states
    h_outs, c_outs = [], []

    output = input
    for i in range(num_layers):
        if unidirectional:
            if weights_per_layer == 4:
                weight_ih, weight_hh, (bias_i, bias_h) = _transform_weights(
                    layer_weights, i
                )
            else:
                weight_ih, weight_hh = _transform_weights_no_bias(layer_weights, i)
                bias_i = bias_h = None

            state_indices = i, i + 1
        else:
            if weights_per_layer == 4:
                weight_ih_f, weight_hh_f, (bias_i_f, bias_h_f) = _transform_weights(
                    layer_weights, 2 * i
                )
                weight_ih_b, weight_hh_b, (bias_i_b, bias_h_b) = _transform_weights(
                    layer_weights, 2 * i + 1
                )
            else:
                weight_ih_f, weight_hh_f = _transform_weights_no_bias(
                    layer_weights, 2 * i
                )
                weight_ih_b, weight_hh_b = _transform_weights_no_bias(
                    layer_weights, 2 * i + 1
                )
                bias_i_f = bias_h_f = bias_i_b = bias_h_b = None

            weight_ih = weight_ih_f, weight_ih_b
            weight_hh = weight_hh_f, weight_hh_b
            bias_i = bias_i_f, bias_i_b
            bias_h = bias_h_f, bias_h_b

            state_indices = 2 * i, 2 * i + 2

        output, (h_out, c_out) = _lstm_layer(
            output,
            (
                _retrieve_state(h0, *state_indices, num_layers),
                _retrieve_state(c0, *state_indices, num_layers),
            ),
            (weight_ih, weight_hh),
            (bias_i, bias_h),
            bidirectional,
            batch_first=False,
            batch_sizes=batch_sizes,
        )
        h_outs.append(h_out)
        c_outs.append(c_out)

    if batch_first:
        output = startai.swapaxes(output, 0, 1)

    h_outs = h_out if num_layers == 1 else startai.concat(h_outs, axis=0)
    c_outs = c_out if num_layers == 1 else startai.concat(c_outs, axis=0)

    if batch_sizes is not None:
        output = _pack_padded_sequence(output, batch_sizes)[0]

    return output[:, -1], output, (h_outs, c_outs)


# Helpers #


def _handle_padding(x, strides, filters, padding):
    if isinstance(padding, str) and padding.upper() == "SAME":
        if x % strides == 0:
            pad = max(filters - strides, 0)
        else:
            pad = max(filters - (x % strides), 0)
    else:
        pad = 0
    return pad


def _validate_max_pool_params(
    kernel, strides, padding, dilation, ceil_mode, dims, data_format
):
    if isinstance(kernel, int):
        kernel = (kernel,) * dims
    elif len(kernel) == 1:
        kernel = (kernel[0],) * dims
    elif len(kernel) not in [dims, dims + 2]:
        raise ValueError(
            "The kernel should be an integer, or a tuple of length"
            f" {list({1, dims, dims + 2})}"
        )

    if isinstance(strides, int):
        strides = (strides,) * dims
    elif len(strides) == 1:
        strides = (strides[0],) * dims
    elif len(strides) not in [dims, dims + 2]:
        raise ValueError(
            "The stride should be an integer, or a tuple of length"
            f" {list({1, dims, dims + 2})}"
        )

    if isinstance(padding, int):
        padding = [(padding,) * 2] * dims
    elif isinstance(padding, tuple) and len(padding) == 1:
        padding = [(padding[0],) * 2] * dims
    elif isinstance(padding, tuple) and len(padding) == dims:
        padding = [(padding[i],) * 2 for i in range(dims)]
    elif isinstance(padding, list) and len(padding) == dims:
        if not all(isinstance(p, tuple) and len(p) == 2 for p in padding):
            raise ValueError("Explicit padding must be a list of tuple of two integers")
    if isinstance(padding, str) and padding.upper() not in ["VALID", "SAME"]:
        raise ValueError(
            f"Invalid padding arg {padding}Must be one of: 'VALID' or 'SAME'"
        )

    if isinstance(dilation, int):
        dilation = (dilation,) * dims
    elif len(dilation) == 1:
        dilation = (dilation[0],) * dims
    elif len(dilation) != dims:
        raise ValueError(
            f"Dilation must be an integer or a tuple of length {list({1, dims})}"
        )
    if min(dilation) < 1:
        raise ValueError("All values of `dilation` must be positive")

    # Other errors
    if isinstance(padding, str) and (padding.upper() == "VALID") and ceil_mode:
        raise ValueError("When 'padding' is 'VALID', 'ceil_mode' must be False")
    assert len(kernel) == len(strides), f"len({kernel}) must equal len({strides})"

    ret = kernel, strides, padding, dilation

    # Account for dilation when padding > kernel/2. Not the case in torch by default.
    if len(dilation) < len(kernel):
        if data_format[:2] == "NC":
            dilation = [1, 1, *dilation]
        else:
            dilation = [1, *dilation, 1]
    elif len(dilation) > len(kernel):
        if data_format[:2] == "NC":
            kernel = [1, 1, *kernel]
        else:
            kernel = [1, *kernel, 1]
    new_kernel = tuple(dilation[i] * (kernel[i] - 1) + 1 for i in range(1, len(kernel)))
    if isinstance(padding, list) and len(padding) == len(new_kernel):
        startai.utils.assertions.check_kernel_padding_size(new_kernel, padding)

    return ret


def _depth_max_pooling_helper(
    x_shape, kernel, strides, dims, data_format="channel_last"
):
    # Determine depth pooling.
    # We assume that the kernel and the data have the same data_format.
    depth_pooling = False
    CHANNEL_LAST = "channel_last"
    channel_idx = -1 if data_format == CHANNEL_LAST else 1
    if len(kernel) == dims + 2:
        spatial_kernel = kernel[1:-1] if data_format == CHANNEL_LAST else kernel[2:]
        if kernel[channel_idx] != 1:
            depth_pooling = True
            if any(i != 1 for i in spatial_kernel):
                raise NotImplementedError(
                    "MaxPooling supports exactly one of pooling across"
                    " depth or pooling across width/height."
                )
            if len(strides) != dims + 2 or strides[channel_idx] != kernel[channel_idx]:
                raise NotImplementedError(
                    "Depthwise max pooling requires the depth window to equal the depth"
                    " stride"
                )
            if x_shape[channel_idx] % kernel[channel_idx] != 0:
                raise NotImplementedError(
                    "Depthwise max pooling requires the depth window to evenly divide"
                    " the input depth"
                )
            kernel = [kernel[channel_idx], *[1] * (dims - 1)]
            strides = [strides[channel_idx], *[1] * (dims - 1)]
        else:
            kernel = spatial_kernel
            if len(strides) == dims + 2:
                strides = strides[1:-1] if data_format == CHANNEL_LAST else strides[2:]
    return kernel, strides, depth_pooling


def _deconv_length(dim_size, stride_size, kernel_size, padding, dilation=1):
    kernel_size = kernel_size + (kernel_size - 1) * (dilation - 1)
    if padding == "SAME":
        dim_size = dim_size * stride_size
    else:
        dim_size = dim_size * stride_size + max(kernel_size - stride_size, 0)
    return dim_size


def _get_x_data_format(dims: int = 2, data_format: str = "channel_first"):
    if dims == 1:
        if data_format == "channel_first":
            return "NCW"
        else:
            return "NWC"
    if dims == 2:
        if data_format == "channel_first":
            return "NCHW"
        else:
            return "NHWC"
    elif dims == 3:
        if data_format == "channel_first":
            return "NCDHW"
        else:
            return "NDHWC"


def _get_num_padded_values(i, p, n, k, s):
    """Get number of padded values in a specific window.

    Parameters
    ----------
    i window index
    p total amount of padding
    n input size
    k kernel size
    s stride

    Returns
    -------
        number of padded values in a particular window represented by i
    """
    current_index = s * i
    left_padding = p // 2
    return max(0, left_padding - current_index) + max(
        0, current_index + k - n - left_padding
    )


# TODO : integrate logic for adaptive sampling points in startai.interpolate
def _bilinear_interpolate(
    input,  # [N, C, H, W]
    roi_batch_ind,  # [K]
    y,  # [K, PH, IY]
    x,  # [K, PW, IX]
    ymask,  # [K, IY]
    xmask,  # [K, IX]
):
    _, channels, height, width = input.shape

    # deal with inverse element out of feature map boundary
    y = y.clip(0, None)
    x = x.clip(0, None)
    y_low = y.astype(startai.int32)
    x_low = x.astype(startai.int32)
    y_high = startai.where(y_low >= height - 1, height - 1, y_low + 1)
    y_low = startai.where(y_low >= height - 1, height - 1, y_low)
    y = startai.where(y_low >= height - 1, y.astype(input.dtype), y)

    x_high = startai.where(x_low >= width - 1, width - 1, x_low + 1)
    x_low = startai.where(x_low >= width - 1, width - 1, x_low)
    x = startai.where(x_low >= width - 1, x.astype(input.dtype), x)

    ly = y - y_low
    lx = x - x_low
    hy = 1.0 - ly
    hx = 1.0 - lx

    def masked_index(
        y,  # [K, PH, IY]
        x,  # [K, PW, IX]
    ):
        if ymask is not None:
            assert xmask is not None
            y = startai.where(ymask[:, None, :], y, 0)
            x = startai.where(xmask[:, None, :], x, 0)
        return input[
            roi_batch_ind[:, None, None, None, None, None],
            startai.arange(channels, device=input.device)[None, :, None, None, None, None],
            y[:, None, :, None, :, None],  # prev [K, PH, IY]
            x[:, None, None, :, None, :],  # prev [K, PW, IX]
        ]  # [K, C, PH, PW, IY, IX]

    v1 = masked_index(y_low, x_low)
    v2 = masked_index(y_low, x_high)
    v3 = masked_index(y_high, x_low)
    v4 = masked_index(y_high, x_high)

    # all ws preemptively [K, C, PH, PW, IY, IX]
    def outer_prod(y, x):
        return y[:, None, :, None, :, None] * x[:, None, None, :, None, :]

    w1 = outer_prod(hy, hx)
    w2 = outer_prod(hy, lx)
    w3 = outer_prod(ly, hx)
    w4 = outer_prod(ly, lx)

    val = w1 * v1 + w2 * v2 + w3 * v3 + w4 * v4
    return val


def _convert_boxes_to_roi_format(boxes):
    concat_boxes = startai.concat(boxes, axis=0)
    temp = []
    for i, b in enumerate(boxes):
        temp.append(startai.full_like(b[:, :1], i))
    ids = startai.concat(temp, axis=0)
    rois = startai.concat([ids, concat_boxes], axis=1)
    return rois


def _lstm_cell(
    x,
    init_h,
    init_c,
    kernel,
    recurrent_kernel,
    bias,
    recurrent_bias,
    batch_first,
    batch_sizes=None,
):
    init_h = startai.squeeze(init_h, axis=0)
    init_c = startai.squeeze(init_c, axis=0)
    out, states = startai.lstm_update(
        x,
        init_h,
        init_c,
        kernel,
        recurrent_kernel,
        bias=bias,
        recurrent_bias=recurrent_bias,
        time_major=not batch_first,
    )
    h, c = states
    h = startai.expand_dims(h) if len(h.shape) == 2 else h
    c = startai.expand_dims(c) if len(c.shape) == 2 else c
    return out, (h, c)


def _lstm_layer(
    x, hidden, weights, biases, bidirectional, batch_first, batch_sizes=None
):
    if not bidirectional:
        result, (h, c) = _lstm_cell(
            x,
            *hidden,
            *weights,
            *biases,
            batch_first=batch_first,
            batch_sizes=batch_sizes,
        )
    else:
        result_fw, (h_fw, c_fw) = _lstm_cell(
            x,
            hidden[0][:1],
            hidden[1][:1],
            weights[0][0],
            weights[1][0],
            biases[0][0],
            biases[1][0],
            batch_first=batch_first,
            batch_sizes=batch_sizes,
        )
        x_reversed = startai.flip(x, axis=0)
        result_bw, (h_bw, c_bw) = _lstm_cell(
            x_reversed,
            hidden[0][1:],
            hidden[1][1:],
            weights[0][1],
            weights[1][1],
            biases[0][1],
            biases[1][1],
            batch_first=batch_first,
            batch_sizes=batch_sizes,
        )
        result_bw = startai.flip(result_bw, axis=0)
        result = startai.concat([result_fw, result_bw], axis=len(result_fw.shape) - 1)
        c = startai.concat([c_fw, c_bw], axis=0)
        h = startai.concat([h_fw, h_bw], axis=0)
    return result, (h, c)


def _pack_padded_sequence(input, lengths):
    input = startai.swapaxes(input, 0, 1)
    data = []
    batch_sizes = []
    for i in range(int(max(lengths))):
        valid_data_mask = startai.array(lengths) > i
        data.append(input[valid_data_mask, i])
        batch_sizes.append(int(sum(valid_data_mask)))
    data = startai.concat(data)
    batch_sizes = startai.array(batch_sizes, dtype=startai.int64)
    return data, batch_sizes


def _pad_packed_sequence(data, batch_sizes):
    padded_data = startai.full(
        (len(batch_sizes), int(max(batch_sizes)), *data.shape[1:]),
        0,
        dtype=data.dtype,
        device=data.device,
    )
    data_offset = 0
    for i, batch_size in enumerate(batch_sizes):
        batch_size = int(batch_size)
        padded_data[i, :batch_size] = data[data_offset : data_offset + batch_size]
        data_offset += batch_size
    lengths = startai.sum(
        startai.arange(1, int(max(batch_sizes)) + 1)[:, startai.newaxis] <= batch_sizes,
        axis=1,
        dtype=startai.int64,
    )
    return padded_data, lengths


def _retrieve_state(x, start, end, num_layers):
    return x if num_layers == 1 else _slice_along_axis(x, start=start, stop=end, axis=0)


def _transform_weights(layer_weights, layer_index):
    weights = layer_weights[layer_index]
    weight_ih, weight_hh, bias_ih, bias_hh = weights
    return (
        startai.swapaxes(weight_ih, 0, 1),
        startai.swapaxes(weight_hh, 0, 1),
        (bias_ih, bias_hh),
    )


def _transform_weights_no_bias(layer_weights, layer_index):
    weights = layer_weights[layer_index]
    weight_ih, weight_hh = weights
    return startai.swapaxes(weight_ih, 0, 1), startai.swapaxes(weight_hh, 0, 1)


def _slice_along_axis(x, start=0, stop=None, stride=1, axis=0):
    if axis >= 0:
        slices = [slice(None)] * axis + [slice(start, stop, stride)]
    else:
        slices = [Ellipsis, slice(start, stop, stride)] + [slice(None)] * (-1 - axis)
    return x[tuple(slices)]


@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def roi_align(
    input, boxes, output_size, spatial_scale=1.0, sampling_ratio=-1, aligned=False
):
    pooled_height, pooled_width = (
        (output_size, output_size) if isinstance(output_size, int) else output_size
    )

    if not isinstance(boxes, startai.Array):
        boxes = _convert_boxes_to_roi_format(boxes)
    orig_dtype = input.dtype

    _, _, height, width = input.shape

    ph = startai.arange(pooled_height, device=input.device)  # [PH]
    pw = startai.arange(pooled_width, device=input.device)  # [PW]

    # input: [N, C, H, W]
    # boxes: [K, 5]

    roi_batch_ind = boxes[:, 0].astype(startai.int32)  # [K]
    offset = 0.5 if aligned else 0.0
    roi_start_w = boxes[:, 1] * spatial_scale - offset  # [K]
    roi_start_h = boxes[:, 2] * spatial_scale - offset  # [K]
    roi_end_w = boxes[:, 3] * spatial_scale - offset  # [K]
    roi_end_h = boxes[:, 4] * spatial_scale - offset  # [K]

    roi_width = roi_end_w - roi_start_w  # [K]
    roi_height = roi_end_h - roi_start_h  # [K]
    if not aligned:
        roi_width = startai.clip(roi_width, 1.0, None)  # [K]
        roi_height = startai.clip(roi_height, 1.0, None)  # [K]

    bin_size_h = roi_height / pooled_height  # [K]
    bin_size_w = roi_width / pooled_width  # [K]

    exact_sampling = sampling_ratio > 0

    roi_bin_grid_h = (
        sampling_ratio if exact_sampling else startai.ceil(roi_height / pooled_height)
    )  # scalar or [K]
    roi_bin_grid_w = (
        sampling_ratio if exact_sampling else startai.ceil(roi_width / pooled_width)
    )  # scalar or [K]
    """Iy, ix = dims(2)"""

    if exact_sampling:
        count = max(roi_bin_grid_h * roi_bin_grid_w, 1)  # scalar
        iy = startai.arange(roi_bin_grid_h, device=input.device)  # [IY]
        ix = startai.arange(roi_bin_grid_w, device=input.device)  # [IX]
        ymask = None
        xmask = None
    else:
        count = startai.clip(roi_bin_grid_h * roi_bin_grid_w, 1, None)  # [K]
        iy = startai.arange(height, device=input.device)  # [IY]
        ix = startai.arange(width, device=input.device)  # [IX]
        ymask = iy[None, :] < roi_bin_grid_h[:, None]  # [K, IY]
        xmask = ix[None, :] < roi_bin_grid_w[:, None]  # [K, IX]

    def from_K(t):
        return t[:, None, None]

    y = (
        from_K(roi_start_h)
        + ph[None, :, None] * from_K(bin_size_h)
        + (iy[None, None, :] + 0.5).astype(input.dtype)
        * from_K(bin_size_h / roi_bin_grid_h)
    )  # [K, PH, IY]
    x = (
        from_K(roi_start_w)
        + pw[None, :, None] * from_K(bin_size_w)
        + (ix[None, None, :] + 0.5).astype(input.dtype)
        * from_K(bin_size_w / roi_bin_grid_w)
    )  # [K, PW, IX]
    val = _bilinear_interpolate(
        input, roi_batch_ind, y, x, ymask, xmask
    )  # [K, C, PH, PW, IY, IX]

    # Mask out samples that weren't actually adaptively needed
    if not exact_sampling:
        val = startai.where(ymask[:, None, None, None, :, None], val, 0)
        val = startai.where(xmask[:, None, None, None, None, :], val, 0)

    output = val.sum(axis=(-1, -2))  # remove IY, IX ~> [K, C, PH, PW]
    if isinstance(count, startai.Array):
        output /= count[:, None, None, None]
    else:
        output /= count

    output = output.astype(orig_dtype)

    return output


# TODO add paddle backend implementation back,
#  once paddle.argsort uses a stable algorithm
#  https://github.com/PaddlePaddle/Paddle/issues/57508
@handle_exceptions
@handle_nestable
@handle_array_like_without_promotion
@inputs_to_startai_arrays
@handle_array_function
def nms(
    boxes,
    scores=None,
    iou_threshold=0.5,
    max_output_size=None,
    score_threshold=float("-inf"),
):
    change_id = False
    if score_threshold is not float("-inf") and scores is not None:
        keep_idx = scores > score_threshold
        boxes = boxes[keep_idx]
        scores = scores[keep_idx]
        change_id = True
        nonzero = startai.nonzero(keep_idx)[0].flatten()
    if scores is None:
        scores = startai.ones((boxes.shape[0],), dtype=boxes.dtype)

    if len(boxes) < 2:
        if len(boxes) == 1:
            ret = startai.array([0], dtype=startai.int64)
        else:
            ret = startai.array([], dtype=startai.int64)
    else:
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1) * (y2 - y1)
        order = startai.argsort(
            (-1 * scores), stable=True
        )  # get boxes with more ious first
        keep = []

        while order.size > 0:
            i = order[0]  # pick maxmum iou box
            keep.append(i)
            xx1 = startai.maximum(x1[i], x1[order[1:]])
            yy1 = startai.maximum(y1[i], y1[order[1:]])
            xx2 = startai.minimum(x2[i], x2[order[1:]])
            yy2 = startai.minimum(y2[i], y2[order[1:]])

            w = startai.maximum(0.0, xx2 - xx1)  # maximum width
            h = startai.maximum(0.0, yy2 - yy1)  # maximum height
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = startai.nonzero(ovr <= iou_threshold)[0]

            order = order[inds + 1]

        ret = startai.array(keep)

    if len(ret) > 1 and scores is not None:
        ret = sorted(
            ret.flatten().tolist(), reverse=True, key=lambda x: (scores[x], -x)
        )
        ret = startai.array(ret, dtype=startai.int64).flatten()

    if change_id and len(ret) > 0:
        ret = startai.array(nonzero[ret], dtype=startai.int64).flatten()

    return ret.flatten()[:max_output_size]


nms.mixed_backend_wrappers = {
    "to_add": (
        "handle_backend_invalid",
        "inputs_to_native_arrays",
        "outputs_to_startai_arrays",
        "handle_device",
    ),
    "to_skip": ("inputs_to_startai_arrays",),
}
