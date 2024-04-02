import startai
from startai.functional.frontends.jax.func_wrapper import to_startai_arrays_and_back
from startai.func_wrapper import with_supported_dtypes


# --- Helpers --- #
# --------------- #


def _batch_promotion(*args, default_dtype="float64"):
    # Promote all types
    promote_types = set()

    for arg in args:
        if args is None:
            continue
        if isinstance(arg, (float, int)):
            continue
        promote_types.add(startai.dtype(arg))

    if "float64" in promote_types:
        return "float64"

    if "float32" in promote_types:
        return "float32"

    if "float16" in promote_types:
        return "float32" if "bfloat16" in promote_types else "float16"

    if "bfloat16" in promote_types:
        return "bfloat16"

    if "int64" in promote_types or "uint64" in promote_types:
        return "float64"

    ints = ["int8", "int16", "int32"]
    if "uint32" in promote_types and any(d in promote_types for d in ints):
        return "float64"

    return default_dtype


def _canonicalize_axis(axis, ndim):
    if not -ndim <= axis < ndim:
        raise startai.utils.exceptions.StartaiException(
            f"axis {axis} is out of bounds for array of dimension {ndim}"
        )
    if axis < 0:
        axis = axis + ndim
    return axis


def _len(x):
    shape = startai.shape(x)
    return 0 if len(shape) == 0 else shape[0]


def _mean(x, axis=None, keepdims=False, where=None):
    # Mean with support for where
    if where is None:
        return startai.mean(x, axis=axis, keepdims=keepdims)

    filtered_x = startai.where(where, startai.array(x), startai.zeros_like(x))
    counter_x = startai.where(where, startai.ones_like(x), startai.zeros_like(x))

    sums = startai.sum(filtered_x, axis=axis, keepdims=keepdims)
    counts = startai.sum(counter_x, axis=axis, keepdims=keepdims)

    return startai.divide(sums, counts)


def _reduction_dims(a, axis):
    ndims = len(startai.shape(a))
    if axis is None:
        return (tuple(range(ndims)),) * 2
    if not isinstance(axis, (tuple, list)):
        axis = (axis,)
    canon_axis = tuple(_canonicalize_axis(ax, ndims) for ax in axis)
    startai.utils.assertions.check_equal(
        len(canon_axis),
        len(set(canon_axis)),
        message=f"duplicate value in 'axis': {axis}",
        as_array=False,
    )

    # TODO: deal with named axis

    canon_pos_axis = tuple(x for x in canon_axis if isinstance(x, int))

    if len(canon_pos_axis) != len(canon_axis):
        return canon_pos_axis, canon_axis
    else:
        return canon_axis, canon_axis


def _type_conversion(x):
    # Does type conversion, floats maps to float,
    # complex maps to complex,
    # 64bit dtype to float64, everything else to float32
    x = startai.asarray(x)
    dtype = startai.as_startai_dtype(x.dtype)
    if not ("float" in dtype or "complex" in dtype):
        dtype = "float64" if "64" in dtype[-2:] else "float32"
    return startai.astype(x, dtype)


def _type_conversion_64(x):
    # Does type conversion, floats maps to float,
    # complex maps to complex, everything else to float64
    x = startai.asarray(x)
    dtype = startai.as_startai_dtype(x.dtype)
    if not ("float" in dtype or "complex" in dtype):
        dtype = "float64"
    return startai.astype(x, dtype)


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def celu(x, alpha=1.0):
    return startai.celu(x, alpha=alpha)


@to_startai_arrays_and_back
def elu(x, alpha=1.0):
    ret = startai.where(x > 0, x, alpha * startai.expm1(x))
    dtype = _batch_promotion(x, alpha, default_dtype="float64")
    return startai.asarray(ret, dtype=dtype)


@to_startai_arrays_and_back
def gelu(x, approximate=True):
    return startai.gelu(x, approximate=approximate, complex_mode="jax")


@to_startai_arrays_and_back
def glu(x, axis=-1):
    size = x.shape[axis]
    startai.utils.assertions.check_equal(
        size % 2, 0, message="axis size must be divisible by 2", as_array=False
    )
    x1, x2 = startai.split(x, num_or_size_splits=2, axis=axis)
    return startai.multiply(x1, startai.sigmoid(x2))


@to_startai_arrays_and_back
def hard_sigmoid(x):
    dtype = _batch_promotion(x, default_dtype="float64")
    return startai.divide(startai.minimum(startai.maximum(startai.add(x, 3), 0), 6), 6).astype(dtype)


@to_startai_arrays_and_back
def hard_silu(x):
    dtype = _batch_promotion(x, default_dtype="float64")
    sig = startai.divide(startai.minimum(startai.maximum(startai.add(x, 3), 0), 6), 6)
    return startai.multiply(x, sig).astype(dtype)


@to_startai_arrays_and_back
def hard_swish(x):
    res = (x * startai.minimum(startai.maximum(x + 3, 0.0), 6.0)) / 6
    return startai.asarray(res, dtype=x.dtype)


@to_startai_arrays_and_back
def hard_tanh(x):
    n1 = -1
    if "uint" in str(x.dtype):
        dtype = x.dtype
        # tensorflow can't use -1 for uint
        n1 = startai.asarray((1 << startai.dtype_bits(dtype)) - 1, dtype=dtype)

    return startai.where(x > 1, 1, startai.where(x < n1, n1, x)).astype(x.dtype)


@to_startai_arrays_and_back
def leaky_relu(x, negative_slope=0.01):
    x = _type_conversion_64(x)
    return startai.leaky_relu(x, alpha=negative_slope, complex_mode="jax")


@to_startai_arrays_and_back
def log_sigmoid(x):
    x = _type_conversion(x)
    return startai.logsigmoid(x, complex_mode="jax").astype(x.dtype)


@to_startai_arrays_and_back
def log_softmax(x, axis=-1):
    return startai.log_softmax(x, axis=axis)


@to_startai_arrays_and_back
def logsumexp(a, axis=None, b=None, keepdims=False, return_sign=False):
    a = startai.asarray(a)
    if b is not None:
        dtype = _batch_promotion(a, b, default_dtype="float32")
        a = startai.astype(a, dtype)
        b = startai.asarray(b, dtype=dtype)
        a = startai.where(b != 0, a, -startai.inf)
        a = startai.astype(a, dtype)
    out_dtype = _batch_promotion(a, b, default_dtype="float32")
    pos_dims, dims = _reduction_dims(a, axis)

    amax = startai.max(a, axis=pos_dims, keepdims=keepdims)
    notinf = startai.asarray(not startai.isinf(amax))
    amax = startai.stop_gradient(startai.where(notinf, amax, startai.zeros_like(amax)))
    amax_with_dims = amax if keepdims else startai.expand_dims(amax, axis=pos_dims)

    # fast path for non-negative result
    if b is None:
        out = startai.add(
            startai.log(
                startai.sum(
                    startai.exp(startai.subtract(a, amax_with_dims)),
                    axis=dims,
                    keepdims=keepdims,
                )
            ),
            amax,
        )
        sign = startai.where(startai.isnan(out), out, 1.0)
        sign = startai.where(startai.isinf(-out), 0.0, sign).astype(out.dtype)
    else:
        expsub = startai.exp(startai.subtract(a, amax_with_dims))
        if b is not None:
            expsub = startai.multiply(expsub, b)
        sumexp = startai.sum(expsub, axis=dims, keepdims=keepdims)
        sign = startai.stop_gradient(startai.sign(sumexp))
        out = startai.add(startai.log(startai.abs(sumexp)), amax)
    if return_sign:
        return out, sign

    if b is not None:
        out = startai.where(sign < 0, startai.array(startai.nan, dtype=out.dtype), out)

    return out.astype(out_dtype)


@to_startai_arrays_and_back
def normalize(x, axis=-1, mean=None, variance=None, epsilon=1e-5, where=None):
    default = "float64" if mean is not None and variance is not None else "float32"

    x_typed = _type_conversion(x)
    if mean is None:
        mean = _mean(x_typed, axis=axis, keepdims=True, where=where)
    if variance is None:
        variance = _mean(
            startai.square(x).astype(x_typed.dtype), axis=axis, keepdims=True, where=where
        ) - startai.square(mean)

    res = (x - mean) / startai.sqrt(variance + startai.asarray(epsilon, dtype=x_typed.dtype))

    out_type = _batch_promotion(x, mean, variance, default_dtype=default)

    return startai.asarray(res, dtype=out_type)


@to_startai_arrays_and_back
def one_hot(x, num_classes, *, dtype=None, axis=-1):
    dtype = startai.float64 if dtype is None else startai.as_startai_dtype(dtype)
    return startai.one_hot(x, num_classes, axis=axis, dtype=dtype)


@to_startai_arrays_and_back
def relu(x):
    return startai.relu(x, complex_mode="jax")


@to_startai_arrays_and_back
def relu6(x):
    res = startai.relu6(x, complex_mode="jax")
    return _type_conversion_64(res)


@to_startai_arrays_and_back
def selu(x):
    x = _type_conversion_64(x)
    return startai.selu(x)


@to_startai_arrays_and_back
def sigmoid(x):
    x = _type_conversion(x)
    ret = startai.sigmoid(x, complex_mode="jax")
    return startai.astype(ret, x.dtype)


@with_supported_dtypes(
    {"0.4.24 and below": ("complex", "float")},
    "jax",
)
@to_startai_arrays_and_back
def silu(x):
    x = _type_conversion(x)
    return startai.multiply(x, startai.sigmoid(x))


@to_startai_arrays_and_back
def soft_sign(x):
    dtype = _type_conversion(x).dtype
    ret = x / (startai.abs(x) + 1)
    return ret.astype(dtype)


@to_startai_arrays_and_back
def softmax(x, axis=-1, where=None, initial=None):
    return startai.softmax(x, axis=axis)


@to_startai_arrays_and_back
def softplus(x):
    x = _type_conversion(x)
    return startai.softplus(x, complex_mode="jax").astype(x.dtype)


@to_startai_arrays_and_back
def swish(x):
    ret = x / (1 + startai.exp(-x))
    return startai.asarray(ret, dtype=x.dtype)
