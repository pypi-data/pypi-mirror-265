# global
import startai
from startai.functional.frontends.tensorflow.func_wrapper import to_startai_arrays_and_back
from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from startai.functional.frontends.tensorflow import check_tensorflow_casting


# --- Helpers --- #
# --------------- #


def _convolution_broadcast_helper(
    arg, num_spatial_dims, channel_index, name="dilations"
):
    # Helper to broadcast dilations and strides to correct dims
    if arg is None:
        return [1] * num_spatial_dims
    else:
        if isinstance(arg, int):
            arg = [arg]
        else:
            arg = list(arg)
        len_arg = len(arg)

        if len_arg == num_spatial_dims + 2:
            return arg

        # Broadcast to rcorrect dimensions
        if len_arg == 1:
            arg = arg * num_spatial_dims
        elif len_arg != num_spatial_dims:
            raise ValueError(
                f"{name} should be of length 1, "
                f"{num_spatial_dims} or {num_spatial_dims + 2}. "
                f"Received: {name}={arg} of length {len_arg}."
            )

    # Add dimensions for batch and channel
    if channel_index == 1:
        return [1, 1] + arg
    else:
        return [1] + arg + [1]


def _reduce_padding(padding, data_format):
    if not isinstance(padding, str):
        if data_format[1] == "C":
            padding = padding[2:]
        else:
            padding = padding[1:-1]
    return padding


def _reduce_strides_dilations(dim, stride, dilations):
    if not isinstance(stride, int):
        if len(stride) > dim:
            stride = stride[1:-1]
        if len(stride) == 1 and dim != 1:
            stride = stride[0]
    if not isinstance(dilations, int):
        if len(dilations) > dim:
            dilations = dilations[1:-1]
        if len(dilations) == 1 and dim != 1:
            dilations = dilations[0]
    return stride, dilations


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def atrous_conv2d(value, filters, rate, padding):
    return startai.conv2d(value, filters, 1, padding, dilations=[rate] * 2)


@to_startai_arrays_and_back
def atrous_conv2d_transpose(value, filters, output_shape, rate, padding):
    filters = filters.swapaxes(-2, -1)
    return startai.conv2d_transpose(
        value, filters, 1, padding, output_shape=output_shape, dilations=[rate] * 2
    )


@to_startai_arrays_and_back
def avg_pool(input, ksize, strides, padding, data_format="NWC", name=None):
    if len(startai.shape(input)) == 3:
        return startai.avg_pool1d(input, ksize, strides, padding, data_format=data_format)
    elif len(startai.shape(input)) == 4:
        return startai.avg_pool2d(input, ksize, strides, padding, data_format=data_format)
    return startai.avg_pool3d(input, ksize, strides, padding, data_format=data_format)


# avg_pool1d
@to_startai_arrays_and_back
def avg_pool1d(input, ksize, strides, padding, data_format="NWC", name=None):
    return startai.avg_pool1d(input, ksize, strides, padding, data_format=data_format)


# avg_pool2d
@to_startai_arrays_and_back
def avg_pool2d(input, ksize, strides, padding, data_format="NHWC", name=None):
    return startai.avg_pool2d(
        input, ksize, strides, padding, data_format=data_format
    ).astype(input.dtype)


# avg_pool3d
@to_startai_arrays_and_back
def avg_pool3d(input, ksize, strides, padding, data_format="NDHWC", name=None):
    return startai.avg_pool3d(input, ksize, strides, padding, data_format=data_format)


@to_startai_arrays_and_back
def batch_normalization(x, mean, variance, offset, scale, variance_epsilon, name=None):
    xnormalized, _, _ = startai.batch_norm(
        x,
        mean,
        variance,
        offset=offset,
        scale=scale,
        eps=variance_epsilon,
    )
    return xnormalized


@to_startai_arrays_and_back
def bias_add(value, bias, data_format=None, name=None):
    if data_format is None:
        data_format = "N...C"

    channel_index = data_format.find("C")
    if channel_index != 1:
        return startai.add(value, bias)
    else:
        value = startai.swapaxes(value, 1, -1)
        res = startai.add(value, bias)
        return startai.swapaxes(res, 1, -1)


@to_startai_arrays_and_back
def conv1d(
    input, filters, stride, padding, data_format="NWC", dilations=None, name=None
):
    dilations = 1 if dilations is None else dilations
    stride, dilations = _reduce_strides_dilations(1, stride, dilations)
    return startai.conv1d(
        input, filters, stride, padding, data_format=data_format, dilations=dilations
    )


@to_startai_arrays_and_back
def conv1d_transpose(
    input,
    filters,
    output_shape,
    strides,
    padding="SAME",
    data_format="NWC",
    dilations=None,
    name=None,
):
    dilations = 1 if dilations is None else dilations
    strides, dilations = _reduce_strides_dilations(1, strides, dilations)
    return startai.conv1d_transpose(
        input,
        filters,
        strides,
        padding,
        output_shape=output_shape,
        data_format=data_format,
        dilations=dilations,
    )


@to_startai_arrays_and_back
def conv2d(
    input, filters, strides, padding, data_format="NHWC", dilations=None, name=None
):
    dilations = 1 if dilations is None else dilations
    strides, dilations = _reduce_strides_dilations(2, strides, dilations)
    padding = _reduce_padding(padding, data_format)
    return startai.conv2d(
        input, filters, strides, padding, data_format=data_format, dilations=dilations
    )


@to_startai_arrays_and_back
def conv2d_transpose(
    input,
    filters,
    output_shape,
    strides,
    padding="SAME",
    data_format="NHWC",
    dilations=None,
    name=None,
):
    dilations = 1 if dilations is None else dilations
    strides, dilations = _reduce_strides_dilations(2, strides, dilations)
    padding = _reduce_padding(padding, data_format)
    return startai.conv2d_transpose(
        input,
        filters,
        strides,
        padding,
        output_shape=output_shape,
        data_format=data_format,
        dilations=dilations,
    )


@to_startai_arrays_and_back
def conv3d(
    input, filters, strides, padding, data_format="NDHWC", dilations=None, name=None
):
    dilations = 1 if dilations is None else dilations
    strides, dilations = _reduce_strides_dilations(3, strides, dilations)
    return startai.conv3d(
        input, filters, strides, padding, data_format=data_format, dilations=dilations
    )


@with_unsupported_dtypes({"2.15.0 and below": ("bfloat16",)}, "tensorflow")
@to_startai_arrays_and_back
def conv3d_transpose(
    input,
    filters,
    output_shape,
    strides,
    padding="SAME",
    data_format="NDHWC",
    dilations=None,
    name=None,
):
    dilations = 1 if dilations is None else dilations
    strides, dilations = _reduce_strides_dilations(3, strides, dilations)
    return startai.conv3d_transpose(
        input,
        filters,
        strides,
        padding,
        output_shape=output_shape,
        data_format=data_format,
        dilations=dilations,
    )


@to_startai_arrays_and_back
def convolution(
    input,
    filters,
    strides=None,
    padding="VALID",
    data_format=None,
    dilations=None,
    name=None,
):
    num_spatial_dims = input.ndim - 2
    if data_format is None or not data_format.startswith("NC"):
        data_format = "channel_last"
    else:
        data_format = "channel_first"

    channel_index = -1 if data_format == "channel_last" else 1
    input_depth = startai.shape(input)[channel_index]
    filters_depth = startai.shape(filters)[-2]

    feature_group_count = 1
    if input_depth != filters_depth:
        if input_depth % filters_depth != 0:
            raise ValueError(
                "input depth must be evenly divisible by filter depth: "
                f"{input_depth} vs {filters_depth}"
            )
        feature_group_count = input_depth // filters_depth
    return startai.conv_general_dilated(
        input,
        filters,
        strides,
        padding,
        dims=num_spatial_dims,
        data_format=data_format,
        dilations=dilations,
        feature_group_count=feature_group_count,
    )


@to_startai_arrays_and_back
def crelu(features, axis=-1, name=None):
    c = startai.concat([features, -features], axis=axis)
    return startai.relu(c)


# ctc_unique_labels
@to_startai_arrays_and_back
def ctc_unique_labels(labels, name=None):
    ctc_labels = startai.unique_all(labels, by_value=False)
    unique_pad = startai.pad(
        ctc_labels[0], (0, labels.size - ctc_labels[0].size), mode="constant"
    )
    return unique_pad, ctc_labels[2]


@with_unsupported_dtypes({"2.15.0 and below": ("bfloat16",)}, "tensorflow")
@to_startai_arrays_and_back
def depthwise_conv2d(
    input,
    filter,
    strides,
    padding="SAME",
    data_format="NHWC",
    dilations=None,
    name=None,
):
    dilations = 1 if dilations is None else dilations
    strides, dilations = _reduce_strides_dilations(2, strides, dilations)
    fc = filter.shape[-2]
    filter = filter.reshape(
        [*filter.shape[0:2], 1, filter.shape[-2] * filter.shape[-1]]
    )
    return startai.conv_general_dilated(
        input,
        filter,
        strides,
        padding,
        data_format="channel_last" if data_format[-1] == "C" else "channel_first",
        dilations=dilations,
        feature_group_count=fc,
    )


@to_startai_arrays_and_back
def dropout(x, rate, noise_shape=None, seed=None, name=None):
    return startai.dropout(x, rate, noise_shape=noise_shape, training=True, seed=seed)


@with_unsupported_dtypes({"2.11.1 and below": ("complex",)}, "tensorflow")
@to_startai_arrays_and_back
def embedding_lookup(params, ids, max_norm=None, name=None):
    return startai.embedding(params, ids, max_norm=max_norm)


@to_startai_arrays_and_back
def gelu(features, approximate=False, name=None):
    return startai.gelu(features, approximate=approximate)


@with_unsupported_dtypes({"2.15.0 and below": "float16"}, "tensorflow")
@to_startai_arrays_and_back
def leaky_relu(features, alpha=0.2, name=None):
    return startai.leaky_relu(features, alpha=alpha)


@with_supported_dtypes({"2.15.0 and below": ("float32", "float16")}, "tensorflow")
@to_startai_arrays_and_back
def local_response_normalization(
    input, depth_radius=5, bias=1.0, alpha=1.0, beta=0.5, name=None
):
    return startai.local_response_norm(
        input, 2 * depth_radius + 1, bias=bias, alpha=alpha, beta=beta
    )


@to_startai_arrays_and_back
def log_poisson_loss(targets, log_input, compute_full_loss=False, name=None):
    return startai.log_poisson_loss(targets, log_input, compute_full_loss=compute_full_loss)


@to_startai_arrays_and_back
def max_pool1d(input, ksize, strides, padding, data_format="NWC", name=None):
    return startai.max_pool1d(input, ksize, strides, padding, data_format=data_format)


@to_startai_arrays_and_back
def max_pool2d(input, ksize, strides, padding, data_format="NHWC", name=None):
    return startai.max_pool2d(input, ksize, strides, padding, data_format=data_format)


@with_supported_dtypes({"2.15.0 and below": ("float32",)}, "tensorflow")
@to_startai_arrays_and_back
def max_pool3d(input, ksize, strides, padding, data_format="NDHWC", name=None):
    return startai.max_pool3d(input, ksize, strides, padding, data_format=data_format)


@to_startai_arrays_and_back
def moments(x, axes, shift=None, keepdims=False, name=None):
    return startai.mean(x, axis=startai.to_list(axes), keepdims=keepdims), startai.var(
        x, axis=startai.to_list(axes), keepdims=keepdims
    )


@with_unsupported_dtypes(
    {
        "2.15.0 and below": (
            "int8",
            "int16",
            "int32",
            "int64",
            "bool",
        )
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def normalize_moments(counts, mean_ss, variance_ss, shift=None, name=None):
    divisor = startai.reciprocal(counts)
    if shift is not None:
        shifted_mean = startai.multiply(mean_ss, divisor)
        mean = startai.add(shifted_mean, shift)
    else:
        shifted_mean = startai.multiply(mean_ss, divisor)
        mean = shifted_mean

    variance = startai.subtract(
        startai.multiply(variance_ss, divisor), startai.square(shifted_mean)
    )
    return mean, variance


# pool
@to_startai_arrays_and_back
def pool(
    input,
    window_shape,
    pooling_type,
    strides=None,
    padding="VALID",
    data_format=None,
    dilations=None,
    name=None,
):
    return startai.pool(
        input,
        window_shape,
        pooling_type,
        strides=strides,
        padding=padding,
        data_format=data_format,
        dilations=dilations,
    )


@with_unsupported_dtypes({"2.15.0 and below": ("complex",)}, "tensorflow")
@to_startai_arrays_and_back
def relu(features, name=None):
    return startai.relu(features)


@with_unsupported_dtypes({"2.15.0 and below": ("complex",)}, "tensorflow")
@to_startai_arrays_and_back
def relu6(features, name=None):
    return startai.relu6(features)


@with_unsupported_dtypes({"2.15.0 and below": ("bfloat16",)}, "tensorflow")
@to_startai_arrays_and_back
def separable_conv2d(
    input,
    depthwise_filter,
    pointwise_filter,
    strides,
    padding,
    data_format=None,
    dilations=None,
    name=None,
):
    dilations = 1 if dilations is None else dilations
    strides, dilations = _reduce_strides_dilations(2, strides, dilations)
    ret = depthwise_conv2d(
        input,
        depthwise_filter,
        strides=strides,
        padding=padding,
        dilations=dilations,
        data_format=data_format,
    )
    return conv2d(ret, pointwise_filter, 1, "SAME", data_format=data_format)


@with_unsupported_dtypes(
    {
        "2.15.0 and below": (
            "int8",
            "int16",
            "int32",
            "int64",
            "bool",
        )
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def sigmoid_cross_entropy_with_logits(labels=None, logits=None, name=None):
    startai.utils.assertions.check_shape(labels, logits)
    zeros = startai.zeros_like(logits)
    max_logits = startai.where(logits >= zeros, logits, zeros)
    neg_abs_logits = startai.negative(startai.abs(logits))
    neg_multiple = startai.negative(startai.multiply(logits, labels))
    ret_val = startai.add(max_logits, neg_multiple)
    return startai.add(ret_val, startai.log1p(startai.exp(neg_abs_logits)))


@to_startai_arrays_and_back
def silu(features, beta: float = 1.0):
    beta = startai.astype(startai.array(beta), startai.dtype(features))
    return startai.multiply(features, startai.sigmoid(startai.multiply(beta, features)))


@with_unsupported_dtypes({"2.15.0 and below": ("float16",)}, "tensorflow")
@to_startai_arrays_and_back
def softmax(logits, axis=None, name=None):
    return startai.softmax(logits, axis=axis)


# Softsign
@with_unsupported_dtypes(
    {
        "2.15.0 and below": (
            "int8",
            "int16",
            "int32",
            "int64",
        )
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def softsign(x, name=None):
    return startai.softsign(x)


# sufficient_statistics
@to_startai_arrays_and_back
def sufficient_statistics(x, axes, shift=None, keepdims=False, name=None):
    count = 1
    shape = startai.shape(x)
    axes = list(set(axes))
    for a in axes:
        if startai.to_scalar(a) < 0:
            index = x.ndim + startai.to_scalar(a)
        else:
            index = startai.to_scalar(a)
        count *= shape[index]
    count = startai.array(count, dtype=startai.dtype(x))
    if shift is None:
        sum_of_elements = startai.sum(x, axis=axes, keepdims=keepdims)
        sum_of_squares = startai.sum(startai.square(x), axis=axes, keepdims=keepdims)
    else:
        sum_of_elements = startai.sum(
            (startai.subtract(x, shift)), axis=axes, keepdims=keepdims
        )
        sum_of_squares = startai.sum(
            (startai.square(startai.subtract(x, shift))), axis=axes, keepdims=keepdims
        )
        if shift.ndim == 0:
            startai.reshape(shift, ())

    if count.ndim == 0:
        startai.reshape(count, ())
    if sum_of_elements.ndim == 0:
        startai.reshape(sum_of_elements, ())
    if sum_of_squares.ndim == 0:
        startai.reshape(sum_of_squares, ())
    return count, sum_of_elements, sum_of_squares, shift


@with_unsupported_dtypes(
    {
        "2.15.0 and below": (
            "int8",
            "int16",
            "int32",
            "int64",
            "bool",
        )
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def weighted_cross_entropy_with_logits(
    labels=None, logits=None, pos_weight=1.0, name=None
):
    startai.utils.assertions.check_shape(labels, logits)
    ones = startai.ones_like(labels)
    zeros = startai.zeros_like(logits)
    log_weight = startai.add(ones, startai.multiply(pos_weight - 1, labels))
    ones_minus_labels = startai.subtract(ones, labels)
    first_term = startai.multiply(ones_minus_labels, logits)

    max_neg_logits = startai.where(
        startai.negative(logits) >= zeros, startai.negative(logits), zeros
    )
    neg_abs_logits = startai.negative(startai.abs(logits))
    log_neg_abs_logits = startai.log1p(startai.exp(neg_abs_logits))
    second_term = startai.multiply(log_weight, startai.add(log_neg_abs_logits, max_neg_logits))
    return startai.add(first_term, second_term)


# weighted_moments
@to_startai_arrays_and_back
def weighted_moments(x, axes, frequency_weights, keepdims=False, name=None):
    fw_x_prod = frequency_weights * x
    fw_x_prod = startai.array(fw_x_prod)
    weighted_input_sum = startai.sum(fw_x_prod, axis=axes, keepdims=True).astype(
        fw_x_prod.dtype
    )

    broadcasted_weights = frequency_weights + startai.zeros_like(x)
    broadcasted_weights = startai.array(broadcasted_weights)
    sum_of_weights = startai.sum(broadcasted_weights, axis=axes, keepdims=True).astype(
        broadcasted_weights.dtype
    )

    divisor = startai.reciprocal(sum_of_weights)

    weighted_input_sum, divisor = check_tensorflow_casting(weighted_input_sum, divisor)
    weighted_mean = startai.multiply(weighted_input_sum, divisor)

    x, weighted_mean = check_tensorflow_casting(x, weighted_mean)
    squared_difference = startai.square(startai.subtract(x, weighted_mean))
    if isinstance(squared_difference, complex):
        squared_difference = squared_difference.real - squared_difference.imag * 1j

    fw_sq_diff_prod = frequency_weights * squared_difference
    fw_sq_diff_prod = startai.array(fw_sq_diff_prod)
    weighted_distsq = startai.sum(fw_sq_diff_prod, axis=axes, keepdims=True).astype(
        fw_sq_diff_prod.dtype
    )

    weighted_distsq, divisor = check_tensorflow_casting(weighted_distsq, divisor)
    weighted_variance = startai.multiply(weighted_distsq, divisor)

    if not keepdims:
        weighted_mean = startai.squeeze(weighted_mean, axis=axes)
        weighted_variance = startai.squeeze(weighted_variance, axis=axes)
    return weighted_mean, weighted_variance


swish = silu
