# global
import startai
from startai.func_wrapper import with_supported_dtypes
from startai.func_wrapper import with_supported_device_and_dtypes, with_unsupported_dtypes
from startai.functional.frontends.paddle.func_wrapper import (
    to_startai_arrays_and_back,
)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64")},
    "paddle",
)
@to_startai_arrays_and_back
def multinomial(x, num_samples=1, replacement=False, name=None):
    n = num_samples + 1
    return startai.multinomial(n, num_samples, probs=x, replace=replacement)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64")},
    "paddle",
)
@to_startai_arrays_and_back
def normal(mean=0.0, std=1.0, shape=None, name=None):
    return startai.random_normal(mean=mean, std=std, shape=shape)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64")},
    "paddle",
)
@to_startai_arrays_and_back
def poisson(x, name=None):
    return startai.poisson(x, shape=None, device=None, dtype=None, seed=None, out=None)


@with_supported_device_and_dtypes(
    {
        "2.6.0 and above": {
            "cpu": (
                "bfloat16",
                "float32",
                "float64",
            ),
            "gpu": (
                "bfloat16",
                "float16",
                "float32",
                "float64",
            ),
        },
        "2.4.2 and below": {
            "cpu": (
                "float32",
                "float64",
            ),
            "gpu": (
                "float16",
                "float32",
                "float64",
            ),
        },
    },
    "paddle",
)
@to_startai_arrays_and_back
def rand(shape, dtype=None, name=None):
    return startai.random_uniform(low=0.0, high=1.0, shape=shape, dtype=dtype, seed=None)


@to_startai_arrays_and_back
def randint(low=0, high=None, shape=[1], dtype=None, name=None):
    return startai.randint(low, high, shape=shape, dtype=dtype)


@with_unsupported_dtypes(
    {"2.6.0 and below": ("int16", "float16", "bfloat16", "uint8")},
    "paddle",
)
@to_startai_arrays_and_back
def randint_like(x, low=0, high=None, dtype=None, name=None):
    if high is None:
        high = low
        low = 0
        if high <= 0:
            raise startai.exceptions.StartaiError(
                "If high is None, low must be greater than 0, but received low = 0."
            )
    return startai.randint(low, high, shape=x.shape, dtype=dtype, seed=None)


def randn(shape, dtype=None, name=None):
    if dtype not in ["float32", "float64"]:
        raise startai.exceptions.StartaiError(
            "Unsupported dtype for randn, only float32 and float64 are supported, "
        )
    return startai.random_normal(shape=shape, dtype=dtype, seed=None)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64")},
    "paddle",
)
@to_startai_arrays_and_back
def standard_normal(shape, dtype=None, name=None):
    return startai.random_normal(mean=0, std=1, shape=shape, dtype=dtype)


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64")},
    "paddle",
)
@to_startai_arrays_and_back
def uniform(shape, dtype=None, min=-1.0, max=1.0, seed=0, name=None):
    return startai.random_uniform(low=min, high=max, shape=shape, dtype=dtype, seed=seed)
