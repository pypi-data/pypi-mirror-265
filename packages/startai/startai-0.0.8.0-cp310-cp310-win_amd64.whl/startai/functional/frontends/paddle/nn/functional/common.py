# local
import startai
from startai.func_wrapper import with_supported_dtypes
from startai.functional.frontends.paddle.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
def cosine_similarity(x1, x2, *, axis=1, eps=1e-08):
    if len(x1.shape) == len(x2.shape) and len(x2.shape) >= 2:
        numerator = startai.sum(x1 * x2, axis=axis)
        x1_squared_norm = startai.sum(startai.square(x1), axis=axis)
        x2_squared_norm = startai.sum(startai.square(x2), axis=axis)
    else:
        numerator = startai.sum(x1 * x2)
        x1_squared_norm = startai.sum(startai.square(x1))
        x2_squared_norm = startai.sum(startai.square(x2))

    x1_norm = startai.sqrt(x1_squared_norm)
    x2_norm = startai.sqrt(x2_squared_norm)
    norm_mm = x1_norm * x2_norm
    denominator = startai.maximum(norm_mm, eps)

    cosine = numerator / denominator
    return cosine


@to_startai_arrays_and_back
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
def dropout(x, p=0.5, axis=None, training=True, mode="upscale_in_train", name=None):
    if axis is not None and axis > 1:
        raise ValueError("Axis value can only be 0 or 1 or None.")
    elif axis is None or (isinstance(axis, list) and len(axis) == 2):
        mask = get_mask(shape=x.shape, device=startai.dev(x), prob=p, seed=None)
    elif axis == 0:
        mask = get_mask(shape=(x.shape[0], 1), device=startai.dev(x), prob=p)
        mask = startai.broadcast_to(mask, x.shape)
    elif axis == 1:
        mask = get_mask(shape=(1, x.shape[1]), device=startai.dev(x), prob=p)
        mask = startai.broadcast_to(mask, x.shape)
    if mode == "upscale_in_train":
        if training:
            out = startai.multiply(x, mask)
            ret = startai.multiply(out, 1.0 / (1.0 - p))
        else:
            ret = x
    else:
        if training:
            ret = startai.multiply(x, mask)
        else:
            ret = startai.multiply(x, (1.0 - p))
    return ret


@to_startai_arrays_and_back
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
def dropout2d(x, *, p=0.5, training=True, data_format="NCHW", name=None):
    return startai.dropout2d(x, p, training=training, data_format=data_format)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
def dropout3d(x, p=0.5, training=True, data_format="NCDHW", name=None):
    return startai.dropout3d(x, p, training=training, data_format=data_format)


def get_mask(shape, device, prob, seed=None):
    mask = startai.where(
        startai.random_uniform(shape=shape, device=device, seed=seed) < prob,
        0.0,
        1.0,
    )
    return mask


@to_startai_arrays_and_back
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
def interpolate(
    x,
    size=None,
    scale_factor=None,
    mode="nearest",
    align_corners=False,
    align_mode=0,
    data_format="NCHW",
    name=None,
):
    return startai.interpolate(
        x, size, mode=mode, scale_factor=scale_factor, align_corners=align_corners
    )


@to_startai_arrays_and_back
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
def linear(x, weight, bias=None, name=None):
    weight = startai.swapaxes(weight, -1, -2)
    return startai.linear(x, weight, bias=bias)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
def unfold(x, kernel_sizes, strides=1, paddings=0, dilations=1, name=None):
    # Input checking
    if isinstance(kernel_sizes, int):
        kernel_sizes = [kernel_sizes, kernel_sizes]
    elif not isinstance(kernel_sizes, (list, tuple)):
        raise startai.exceptions.StartaiError(
            "Expected kernel size input as type int, tuple or list but got"
            f" {type(kernel_sizes)}"
        )

    if isinstance(strides, int):
        strides = [strides, strides]
    elif not isinstance(strides, (list, tuple)):
        raise startai.exceptions.StartaiError(
            f"Expected strides input as type int, tuple or list but got {type(strides)}"
        )

    if isinstance(dilations, int):
        dilations = [dilations, dilations]
    elif not isinstance(dilations, (list, tuple)):
        raise startai.exceptions.StartaiError(
            "Expected dilations input as type int, tuple or list but got"
            f" {type(dilations)}"
        )

    if isinstance(paddings, int):
        paddings = [paddings, paddings]
    elif not isinstance(paddings, (list, tuple)):
        raise startai.exceptions.StartaiError(
            "Expected paddings, input as type int, tuple or list but got"
            f" {type(paddings)}"
        )

    n, c, h, w = x.shape
    # Padding
    if paddings[0] >= 0 or paddings[1] >= 0:
        padding_tup = [(0, 0) for i in range(2)] + [
            (paddings[0], paddings[0]),
            (paddings[1], paddings[1]),
        ]
        x = startai.pad(x, padding_tup, mode="constant", constant_values=0.0)
    else:
        raise startai.exceptions.StartaiError(
            f"Expected padding size larger than 0 but got {paddings[0]}/{paddings[1]}"
        )

    # Expected input shape
    h_steps = int(
        (h + (paddings[0] * 2) - dilations[0] * (kernel_sizes[0] - 1) - 1) / strides[0]
        + 1
    )

    w_steps = int(
        (w + (paddings[1] * 2) - dilations[1] * (kernel_sizes[1] - 1) - 1) / strides[1]
        + 1
    )

    if h_steps < 1 or w_steps < 1:
        raise startai.exceptions.StartaiError(
            "Expected at least one for height and width, but got expected output shape"
            f" H:{h_steps} W:{w_steps}]"
        )

    # sliding windows
    folder = []
    for i in range(0, h_steps * strides[0], strides[0]):
        for j in range(0, w_steps * strides[1], strides[1]):
            window = x[
                :,
                :,
                i : i + dilations[0] * (kernel_sizes[0] - 1) + 1 : dilations[0],
                j : j + dilations[1] * (kernel_sizes[1] - 1) + 1 : dilations[1],
            ]
            window = startai.flatten(window, start_dim=1)
            folder.append(window)
    return startai.stack(folder, axis=2)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
def zeropad2d(x, padding, data_format="NCHW", name=None):
    if startai.is_array(padding):
        padding = padding.to_list()
    if isinstance(padding, int):
        padding = [padding, padding, padding, padding]
    if len(padding) != 4:
        raise ValueError("Padding length should be 4.")
    if x.ndim != 4:
        raise ValueError("Input x must be 4-dimensional.")
    if data_format == "NCHW":
        padding = ((0, 0), (0, 0), (padding[2], padding[3]), (padding[0], padding[1]))
    elif data_format == "NHWC":
        padding = ((0, 0), (padding[2], padding[3]), (padding[0], padding[1]), (0, 0))
    else:
        raise ValueError(f"Unknown data_format: {data_format}")
    return startai.pad(x, padding, mode="constant", constant_values=0.0)
