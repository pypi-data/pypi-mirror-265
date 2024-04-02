# global
import operator

# local
import startai
from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from startai.functional.frontends.jax.func_wrapper import (
    to_startai_arrays_and_back,
    handle_jax_dtype,
)


# --- Helpers --- #
# --------------- #


def _get_seed(key):
    if "PRNGKeyArray" in repr(key):
        key = key._base_array
    key1, key2 = int(key[0]), int(key[1])
    return startai.to_scalar(int("".join(map(str, [key1, key2]))))


def _remove_axis(shape, axis):
    return shape[:axis] + shape[axis + 1 :]


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def PRNGKey(seed):
    return startai.array([0, seed % 4294967295 - (seed // 4294967295)], dtype=startai.int64)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_supported_dtypes(
    {
        "0.4.24 and below": (
            "float32",
            "float64",
        )
    },
    "jax",
)
def ball(key, d, p=2.0, shape=(), dtype="float64"):
    seed = _get_seed(key)
    d = operator.index(d)

    g = startai.gamma(1 / p, 1.0, shape=shape, dtype=dtype, seed=seed)
    b = startai.bernoulli(startai.array([0.5]), shape=shape, dtype=dtype, seed=seed)
    r = 2 * b - 1
    gn = r * g ** (1 / p)

    uniform = startai.random_uniform(seed=seed, shape=shape, dtype=dtype)
    exp = -startai.log(1 - uniform)

    return gn / (((startai.abs(gn) ** p).sum(axis=-1) + exp) ** (1 / p))[..., None]


@to_startai_arrays_and_back
def bernoulli(key, p=0.5, shape=None):
    seed = _get_seed(key)
    return startai.bernoulli(p, shape=shape, seed=seed)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def beta(key, a, b, shape=None, dtype=None):
    seed = _get_seed(key)
    return startai.beta(a, b, shape=shape, dtype=dtype, seed=seed)


@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def categorical(key, logits, axis, shape=None):
    logits_arr = startai.asarray(logits)

    if axis >= 0:
        axis -= len(logits_arr.shape)
    batch_shape = tuple(_remove_axis(logits_arr.shape, axis))

    if shape is None:
        shape = batch_shape
    else:
        shape = tuple(shape)
        if shape != batch_shape:
            raise ValueError(
                +f"Shape {shape} is not compatible with reference shape {batch_shape}"
            )

    logits_shape = list(shape[len(shape) - len(batch_shape) :])
    logits_shape.insert(axis % len(logits_arr.shape), logits_arr.shape[axis])

    gumbel_noise = gumbel(key, startai.array(logits_shape), logits_arr.dtype)
    expanded_logits = startai.expand_dims(logits_arr, axis=axis)
    noisy_logits = gumbel_noise + expanded_logits

    # Use Startai's argmax to get indices
    indices = startai.argmax(noisy_logits, axis=axis)

    return indices


@handle_jax_dtype
@to_startai_arrays_and_back
def cauchy(key, shape=(), dtype="float64"):
    seed = _get_seed(key)
    u = startai.random_uniform(low=0.0, high=1.0, shape=shape, dtype=dtype, seed=seed)
    return startai.tan(startai.pi * (u - 0.5))


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def dirichlet(key, alpha, shape=None, dtype="float32"):
    seed = _get_seed(key)
    alpha = startai.astype(alpha, dtype)
    return startai.dirichlet(alpha, size=shape, dtype=dtype, seed=seed)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"0.4.24 and below": "uint32"},
    "jax",
)
def double_sided_maxwell(key, loc, scale, shape=(), dtype="float64"):
    params_shapes = startai.broadcast_shapes(startai.shape(loc), startai.shape(scale))
    if not shape:
        shape = params_shapes

    shape = shape + params_shapes
    maxwell_rvs = maxwell(key, shape=shape, dtype=dtype)
    random_sign = rademacher(key, shape=shape, dtype=dtype)

    return random_sign * maxwell_rvs * scale + loc


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def exponential(key, shape=(), dtype="float64"):
    seed = _get_seed(key)
    uniform = startai.random_uniform(seed=seed, shape=shape, dtype=dtype)
    exp = -startai.log(1 - uniform)
    return exp


@to_startai_arrays_and_back
def fold_in(key, data):
    if "PRNGKeyArray" in repr(key):
        key = key._base_array
    s = startai.bitwise_left_shift(
        startai.asarray(data, dtype=startai.uint32), startai.array(32, dtype=startai.uint32)
    )
    return startai.bitwise_xor(key, s)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def gamma(key, a, shape=None, dtype="float64"):
    seed = _get_seed(key)
    return startai.gamma(a, 1.0, shape=shape, dtype=dtype, seed=seed)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def generalized_normal(key, p, shape=(), dtype="float64"):
    seed = _get_seed(key)
    g = startai.gamma(1 / p, 1.0, shape=shape, dtype=dtype, seed=seed)
    b = startai.bernoulli(startai.array([0.5]), shape=shape, dtype=dtype, seed=seed)
    r = 2 * b - 1
    return r * g ** (1 / p)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def gumbel(key, shape=(), dtype="float64"):
    seed = _get_seed(key)
    uniform_x = startai.random_uniform(
        low=0.0,
        high=1.0,
        shape=shape,
        dtype=dtype,
        seed=seed,
    )
    return -startai.log(-startai.log(uniform_x))


# loggamma
@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def loggamma(key, a, shape=None, dtype="float64"):
    seed = _get_seed(key)
    return startai.log(startai.gamma(a, 1.0, shape=shape, dtype=dtype, seed=seed))


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"0.4.24 and below": ("float16", "bfloat16")},
    "jax",
)
def logistic(key, shape=(), dtype="float64"):
    seed = _get_seed(key)
    uniform_x = startai.random_uniform(seed=seed, shape=shape, dtype=dtype)
    return startai.log(startai.divide(uniform_x, startai.subtract(1.0, uniform_x)))


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.3.14 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def maxwell(key, shape, dtype="float64"):
    seed = _get_seed(key)
    shape = shape + (3,)
    random_normal = startai.random_normal(seed=seed, shape=shape, dtype=dtype)
    return startai.vector_norm(random_normal, axis=-1)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def multivariate_normal(key, mean, cov, shape=None, dtype="float64", method="cholesky"):
    if shape is None:
        shape = startai.broadcast_shapes(mean.shape[:-1], cov.shape[:-2])
    if method == "cholesky":
        cov_factor = startai.cholesky(cov)
    elif method == "eigh":
        (w, v) = startai.eigh(cov)
        cov_factor = v * startai.sqrt(w[..., None, :])
    elif method == "svd":
        (u, s, _) = startai.svd(cov)
        cov_factor = u * startai.sqrt(s[..., None, :])

    rand_normal = normal(key=key, shape=shape + mean.shape[-1:], dtype=dtype)
    result = mean + startai.einsum("...ij,...j->...i", cov_factor, rand_normal.startai_array)

    return result


@handle_jax_dtype
@to_startai_arrays_and_back
def normal(key, shape=(), dtype=None):
    seed = _get_seed(key)
    return startai.random_normal(shape=shape, dtype=dtype, seed=seed)


@handle_jax_dtype
@to_startai_arrays_and_back
def orthogonal(key, n, shape=(), dtype=None):
    seed = _get_seed(key)
    flat_shape = (n, n)
    if shape:
        flat_shape = shape + flat_shape

    # Generate a random matrix with the given shape and dtype
    random_matrix = startai.random_uniform(seed=seed, shape=flat_shape, dtype=dtype)

    # Compute the QR decomposition of the random matrix
    q, _ = startai.linalg.qr(random_matrix)

    # Reshape the resulting orthogonal matrix to the desired shape
    if shape:
        q = startai.reshape(q, shape + (n, n))

    return q


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "bfloat16",
        )
    },
    "jax",
)
def pareto(key, b, shape=None, dtype="float64"):
    seed = _get_seed(key)
    if shape is None:
        shape = b.shape
    # Draw samples from exponential distribution
    uniform = startai.random_uniform(seed=seed, shape=shape, dtype=dtype)
    e = -startai.log(1 - uniform)

    return startai.exp(e / b)


@to_startai_arrays_and_back
def permutation(key, x, axis=0, independent=False):
    x = startai.array(x)
    seed = _get_seed(key)
    if not startai.get_num_dims(x):
        r = int(x)
        return startai.shuffle(startai.arange(r), axis, seed=seed)
    if independent:
        return startai.shuffle(x, axis, seed=seed)
    rand = startai.arange(x.shape[axis])
    ind = startai.shuffle(rand, 0, seed=seed)
    return startai.gather(x, ind, axis=axis)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"0.4.24 and below": ("unsigned", "int8", "int16")},
    "jax",
)
def poisson(key, lam, shape=None, dtype=None):
    seed = _get_seed(key)
    return startai.poisson(lam, shape=shape, dtype=dtype, seed=seed, fill_value=-1)


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"0.4.24 and below": ("unsigned", "int8", "int16")},
    "jax",
)
def rademacher(key, shape, dtype="int64"):
    seed = _get_seed(key)
    prob = startai.full(shape, 0.5, dtype="float32")
    b = startai.bernoulli(prob, shape=shape, dtype="float32", seed=seed)
    b = startai.astype(b, dtype)
    return 2 * b - 1


@handle_jax_dtype
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"0.4.24 and below": ("unsigned", "int8", "int16")},
    "jax",
)
def randint(key, shape, minval, maxval, dtype="int64"):
    seed = _get_seed(key)
    return startai.randint(minval, maxval, shape=shape, dtype=dtype, seed=seed)


@to_startai_arrays_and_back
def shuffle(key, x, axis=0):
    seed = _get_seed(key)
    x = startai.flip(x, axis=axis)
    return startai.shuffle(x, seed=seed)


@handle_jax_dtype
@to_startai_arrays_and_back
def t(key, df, shape=(), dtype="float64"):
    seed = _get_seed(key)
    n = startai.random_normal(shape=shape, dtype=dtype, seed=seed)
    half_df = df / 2.0
    g = startai.gamma(half_df, 1.0, shape=shape, dtype=dtype, seed=seed)
    return n * startai.sqrt(startai.divide(half_df, g))


@handle_jax_dtype
@to_startai_arrays_and_back
def uniform(key, shape=(), dtype=None, minval=0.0, maxval=1.0):
    seed = _get_seed(key)
    return startai.random_uniform(
        low=minval, high=maxval, shape=shape, dtype=dtype, seed=seed
    )


@handle_jax_dtype
@to_startai_arrays_and_back
def weibull_min(key, scale, concentration, shape=(), dtype="float64"):
    seed = _get_seed(key)
    uniform_x = startai.random_uniform(seed=seed, shape=shape, dtype=dtype)
    x = 1 - uniform_x
    weibull = x ** (concentration - 1) * -startai.log(x / scale)
    return weibull
