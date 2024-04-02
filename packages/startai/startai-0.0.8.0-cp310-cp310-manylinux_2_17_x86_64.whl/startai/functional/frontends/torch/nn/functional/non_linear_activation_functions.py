# local
import startai
from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "2.2 and below": (
            "complex",
            "float16",
        )
    },
    "torch",
)
def celu(input, alpha=1.0, inplace=False):
    return startai.celu(input, alpha=alpha)


def celu_(input, alpha=1.0):
    return celu(input, alpha=alpha, inplace=True)


@to_startai_arrays_and_back
def elu(input, alpha=1.0, inplace=False):
    prod = startai.multiply(
        alpha,
        startai.subtract(startai.exp(input), 1),
    )
    return startai.where(startai.greater(input, 0), input, prod)


def elu_(input, alpha=1.0):
    return elu(input, alpha=alpha, inplace=True)


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
def gelu(input, *, approximate="none"):
    if approximate == "none":
        return startai.gelu(input, approximate=False)
    elif approximate == "tanh":
        return startai.gelu(input, approximate=True)
    else:
        raise startai.utils.exceptions.StartaiException(
            "`approximate` argument must be either 'none' or 'tanh'."
        )


@to_startai_arrays_and_back
def glu(input, dim=-1):
    a, b = startai.split(input, num_or_size_splits=2, axis=dim)
    return startai.multiply(a, startai.sigmoid(b))


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def gumbel_softmax(logits, tau=1, hard=False, eps=1e-10, dim=-1):
    gumbels = -startai.empty_like(logits).exponential().log()
    gumbels = (logits + gumbels) / tau
    y_soft = startai.softmax(gumbels, axis=dim)

    if hard:
        indices = y_soft.max(axis=dim, keepdims=True)[1]
        y_hard = startai.zeros_like(logits)
        updates = startai.ones_like(indices)
        y_hard = startai.scatter_nd(indices, updates, reduction="replace", out=y_hard)

        ret = y_hard - y_soft.stop_gradient(preserve_type=True) + y_soft
    else:
        ret = y_soft

    return ret


@to_startai_arrays_and_back
def hardshrink(input, lambd=0.5):
    mask = startai.logical_or(startai.greater(input, lambd), startai.less(input, -lambd))
    return startai.where(mask, input, 0.0)


@to_startai_arrays_and_back
def hardsigmoid(input, inplace=False):
    return startai.divide(startai.minimum(startai.maximum(startai.add(input, 3), 0), 6), 6)


@to_startai_arrays_and_back
def hardswish(input, inplace=False):
    relu6_val = startai.relu6(startai.add(input, 3))
    return startai.multiply(input, startai.divide(relu6_val, 6))


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def hardtanh(input, min_val=-1.0, max_val=1.0, inplace=False):
    less = startai.where(startai.less(input, min_val), min_val, input)
    return startai.where(startai.greater(input, max_val), max_val, less).astype(input.dtype)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def hardtanh_(input, min_val=-1.0, max_val=1.0):
    return hardtanh(input, min_val=min_val, max_val=max_val, inplace=True)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def leaky_relu(input, negative_slope=0.01, inplace=False):
    return startai.leaky_relu(input, alpha=negative_slope)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def leaky_relu_(input, negative_slope=0.01):
    return leaky_relu(input, negative_slope=negative_slope, inplace=True)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.2 and below": ("float",)}, "torch")
def local_response_norm(input, size, alpha=0.0001, beta=0.75, k=1.0):
    non_batched = input.ndim == 3
    if non_batched:
        input = startai.expand_dims(input, axis=2)
    ret = startai.local_response_norm(
        input, size, bias=k, alpha=alpha, beta=beta, average=True, data_format="NCHW"
    )
    if non_batched:
        ret = startai.squeeze(ret, axis=2)
    return ret


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def log_softmax(input, dim=None, _stacklevel=3, dtype=None):
    if dtype:
        input = startai.astype(startai.array(input), startai.as_startai_dtype(dtype))
    if dim is None:
        dim = -1
    return startai.log_softmax(input, axis=dim)


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
def logsigmoid(input):
    return startai.logsigmoid(input)


@to_startai_arrays_and_back
def mish(input, inplace=False):
    return startai.multiply(
        input,
        startai.tanh(startai.softplus(input)),
    )


@to_startai_arrays_and_back
def normalize(input, p=2.0, dim=1, eps=1e-12, out=None):
    abs_square = startai.pow(startai.abs(input), p)
    sum_ = startai.sum(abs_square, axis=dim, keepdims=True)
    pnorm_res = startai.pow(sum_, 1.0 / p)
    max_ = startai.maximum(pnorm_res, eps)
    return startai.divide(input, max_, out=out)


@to_startai_arrays_and_back
def prelu(input, weight):
    return startai.add(startai.maximum(0, input), startai.multiply(weight, startai.minimum(0, input)))


@to_startai_arrays_and_back
def relu(input, inplace=False):
    return startai.relu(input)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
def relu6(input, inplace=False):
    return startai.relu6(input)


@to_startai_arrays_and_back
def relu_(input):
    return relu(input, inplace=True)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def rrelu(input, lower=1.0 / 8, upper=1.0 / 3, training=False, inplace=False):
    if training:
        # alpha = startai.random_uniform(low=lower, high=upper)
        # ToDo implement alpha correctly after fixing startai.random_uniform
        pass
    else:
        alpha = (lower + upper) / 2
    return startai.subtract(
        startai.relu(input), startai.multiply(alpha, startai.relu(startai.negative(input)))
    )


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def rrelu_(input, lower=1.0 / 8, upper=1.0 / 3, training=False):
    return rrelu(input, lower=lower, upper=upper, training=training, inplace=True)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.2 and below": ("float32", "float64")}, "torch")
def scaled_dot_product_attention(
    query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None
):
    return startai.scaled_dot_product_attention(
        query,
        key,
        value,
        scale=scale,
        mask=attn_mask,
        dropout_p=dropout_p,
        is_causal=is_causal,
    )


@to_startai_arrays_and_back
def selu(input, inplace=False):
    return startai.selu(input)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def sigmoid(input):
    return startai.sigmoid(input)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def silu(input, inplace=False):
    return startai.multiply(input, startai.sigmoid(input))


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def softmax(input, dim=None, _stacklevel=3, dtype=None):
    if dtype:
        input = startai.astype(startai.array(input), startai.as_startai_dtype(dtype))
    return startai.softmax(input, axis=dim)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def softmin(input, dim=None, dtype=None):
    if dtype:
        input = startai.astype(startai.array(input), startai.as_startai_dtype(dtype))
    return startai.softmax(-input, axis=dim)


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
def softplus(input, beta=1, threshold=20):
    return startai.softplus(input, beta=beta, threshold=threshold)


@to_startai_arrays_and_back
def softshrink(input, lambd=0.5):
    low = startai.where(startai.less(input, -lambd), startai.add(input, lambd), 0)
    up = startai.where(startai.greater(input, lambd), startai.subtract(input, lambd), 0)
    return startai.add(low, up)


@to_startai_arrays_and_back
def softsign(input):
    return startai.divide(input, startai.add(1, startai.abs(input)))


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def tanh(input):
    return startai.tanh(input)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def tanhshrink(input):
    return startai.subtract(input, startai.tanh(input))


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def threshold(input, threshold, value, inplace=False):
    return startai.where(startai.greater(input, threshold), input, value)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def threshold_(input, threshold, value):
    return threshold(input, threshold, value, inplace=True)
