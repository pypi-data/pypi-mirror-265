# local
import startai
from startai.func_wrapper import with_unsupported_dtypes

from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back


# ToDo: this function will be simplified once startai.alpha_dropout is implemented
@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@with_unsupported_dtypes({"2.6.0 and below": ("float16", "bfloat16")}, "paddle")
def alpha_dropout(input, p=0.5, training=False, inplace=False):
    if p == 0.0 or not training or input.shape == () or input.shape == (0,):
        return input
    neg_saturation = startai.log1p(startai.exp(-startai.square(input)))
    mask = startai.where(
        startai.random_uniform(shape=input.shape, device=startai.dev(input)) < p,
        0.0,
        1.0,
    )
    if inplace:
        startai.inplace_update(input, mask * input + (1 - mask) * neg_saturation)
        startai.inplace_update(input, input / startai.sqrt(1 - p / (1 - p + 1e-5)))
        return input
    else:
        masked = mask * input + (1 - mask) * neg_saturation
        return masked / startai.sqrt(1 - p / (1 - p + 1e-5))


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def dropout(input, p=0.5, training=True, inplace=False):
    return startai.dropout(input, p, scale=True, training=training)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def dropout1d(input, p=0.5, training=True, inplace=False):
    if inplace:
        return startai.dropout1d(input, p, training=training, data_format="NCW", out=input)
    return startai.dropout1d(input, p, training=training, data_format="NCW")


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def dropout2d(input, p=0.5, training=True, inplace=False):
    if input.ndim < 2:
        raise ValueError("Feature dropout requires at least 2 dimensions in the input")

    ret = startai.dropout2d(input, p, training=training, data_format="NCHW")
    if inplace:
        startai.inplace_update(input, ret)
        return input
    return ret


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
def dropout3d(input, p=0.5, training=True, inplace=False):
    if inplace:
        return startai.dropout3d(
            input, p, training=training, data_format="NDHWC", out=input
        )
    return startai.dropout3d(input, p, training=training, data_format="NDHWC")
