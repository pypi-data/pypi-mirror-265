import startai
from startai.func_wrapper import with_unsupported_dtypes
from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back


@with_unsupported_dtypes(
    {
        "2.2 and below": (
            "bfloat16",
            "float16",
        )
    },
    "torch",
)
@to_startai_arrays_and_back
def batch_norm(
    input,
    running_mean,
    running_var,
    weight=None,
    bias=None,
    training=False,
    momentum=0.1,
    eps=1e-5,
):
    normalized, mean, var = startai.batch_norm(
        input,
        running_mean,
        running_var,
        offset=bias,
        scale=weight,
        training=training,
        eps=eps,
        momentum=momentum,
        data_format="NCS",
    )
    if training:
        startai.inplace_update(running_mean, mean)
        startai.inplace_update(running_var, var)
    return normalized


@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "2.2 and below": (
            "float16",
            "bfloat16",
        )
    },
    "torch",
)
def group_norm(input, num_groups, weight=None, bias=None, eps=1e-05):
    return startai.group_norm(
        input, num_groups, scale=weight, offset=bias, data_format="NCS", eps=eps
    )


@with_unsupported_dtypes(
    {
        "2.2 and below": (
            "bfloat16",
            "float16",
        )
    },
    "torch",
)
@to_startai_arrays_and_back
def instance_norm(
    input,
    running_mean,
    running_var,
    weight=None,
    bias=None,
    use_input_stats=False,
    momentum=0.1,
    eps=1e-5,
):
    normalized, mean, var = startai.instance_norm(
        input,
        running_mean,
        running_var,
        offset=bias,
        scale=weight,
        training=use_input_stats,
        eps=eps,
        momentum=momentum,
        data_format="NCS",
    )
    startai.inplace_update(running_mean, mean)
    startai.inplace_update(running_var, var)
    return normalized


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
def layer_norm(input, normalized_shape, weight=None, bias=None, eps=1e-05):
    shape = startai.shape(input)
    if isinstance(normalized_shape, int) and normalized_shape == shape[-1]:
        axis = [-1]
    else:
        assert startai.all(startai.equal(normalized_shape, shape[-len(normalized_shape) :]))
        axis = list(range(len(shape) - len(normalized_shape), len(shape)))
    return startai.layer_norm(input, axis, scale=weight, offset=bias, eps=eps)
