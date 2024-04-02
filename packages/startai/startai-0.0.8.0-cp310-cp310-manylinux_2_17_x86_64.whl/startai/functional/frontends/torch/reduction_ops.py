import startai
from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from startai.functional.frontends.torch.func_wrapper import (
    to_startai_arrays_and_back,
    numpy_to_torch_style_args,
)
from collections import namedtuple
import startai.functional.frontends.torch as torch_frontend


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def all(input, dim=None, keepdim=False, *, out=None):
    input_dtype = startai.as_startai_dtype(input.dtype)
    ret = startai.all(input, axis=dim, keepdims=keepdim, out=out)
    if startai.is_uint_dtype(input_dtype):
        ret = startai.astype(ret, input_dtype, out=out)
    return ret


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@numpy_to_torch_style_args
@to_startai_arrays_and_back
def amax(input, dim=None, keepdim=False, *, out=None):
    return startai.max(input, axis=dim, keepdims=keepdim, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@numpy_to_torch_style_args
@to_startai_arrays_and_back
def amin(input, dim=None, keepdim=False, *, out=None):
    return startai.min(input, axis=dim, keepdims=keepdim, out=out)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16", "complex")}, "torch")
def aminmax(input, *, dim=None, keepdim=False, out=None):
    minmax_tuple = namedtuple("minmax", ["min", "max"])
    return minmax_tuple(
        startai.min(input, axis=dim, keepdims=keepdim, out=out),
        startai.max(input, axis=dim, keepdims=keepdim, out=out),
    )


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def any(input, dim=None, keepdim=False, *, out=None):
    input_dtype = startai.as_startai_dtype(input.dtype)
    ret = startai.any(input, axis=dim, keepdims=keepdim, out=out)
    if startai.is_uint_dtype(input_dtype):
        ret = startai.astype(ret, input_dtype, out=out)
    return ret


@with_unsupported_dtypes({"2.2 and below": ("complex", "bool")}, "torch")
@numpy_to_torch_style_args
@to_startai_arrays_and_back
def argmax(input, dim=None, keepdim=False):
    return startai.argmax(input, axis=dim, keepdims=keepdim)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def argmin(input, dim=None, keepdim=False):
    return startai.argmin(input, axis=dim, keepdims=keepdim).astype(startai.int64)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"2.2 and below": ("uint8", "int8")},
    "torch",
)
def count_nonzero(input, dim=None):
    return startai.count_nonzero(input, axis=dim).astype(startai.int64)


@to_startai_arrays_and_back
def dist(input, other, p=2):
    return startai.vector_norm(startai.subtract(input, other), ord=p)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def logsumexp(input, dim, keepdim=False, *, out=None):
    c = startai.max(input, axis=dim, keepdims=True)
    if startai.get_num_dims(c) > 0:
        c = startai.where(startai.isinf(c), startai.zeros_like(c), c)
    elif not startai.isinf(c):
        c = 0
    exponential = startai.exp(input - c)
    sum = startai.sum(exponential, axis=dim, keepdims=keepdim)
    ret = startai.log(sum)
    if not keepdim:
        c = startai.squeeze(c, axis=dim)
    ret = startai.add(ret, c, out=out)
    return ret


@numpy_to_torch_style_args
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"2.2 and below": ("complex64", "complex128")},
    "torch",
)
def max(*input, dim=None, keepdim=False, out=None):
    if len(input) == 1:
        input = input[0]
    elif len(input) == 2:
        input_0 = input[0]
        input_1 = input[1]
        if startai.is_array(input_1):
            return torch_frontend.maximum(*input)
        else:
            input = input_0
            dim = input_1
    else:
        input = input[0]
        dim = input[1]
        keepdim = input[2]
    if dim is None:
        return startai.max(input, axis=dim, keepdims=keepdim, out=out)
    elif out is not None:
        startai.max(input, axis=dim, keepdims=keepdim, out=out[0])
        startai.argmax(input, axis=dim, keepdims=keepdim, out=out[1])
        return out
    else:
        max_tuple = namedtuple("max", ["values", "indices"])
        return max_tuple(
            startai.max(input, axis=dim, keepdims=keepdim),
            startai.argmax(input, axis=dim, keepdims=keepdim),
        )


@numpy_to_torch_style_args
@to_startai_arrays_and_back
@with_supported_dtypes(
    {
        "2.2.1 and below": (
            "bfloat16",
            "float16",
            "float32",
            "float64",
            "complex64",
            "complex128",
        )
    },
    "torch",
)
def mean(input, dim=None, keepdim=False, *, dtype=None, out=None):
    if dtype is not None:
        input = input.astype(dtype)
        if out is not None:
            out = out.astype(dtype)
    return startai.mean(input, axis=dim, keepdims=keepdim, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex", "float16", "bool")}, "torch")
@numpy_to_torch_style_args
@to_startai_arrays_and_back
def median(input, dim=None, keepdim=False, *, out=None):
    if dim is None:
        input = startai.reshape(input, (-1,))
        sorted_input = startai.sort(input)
        return sorted_input[(sorted_input.shape[0] - 1) // 2]

    median_tuple = namedtuple("median", ["values", "indices"])

    if input.ndim == 0:
        result = median_tuple(input, startai.array(0))
    else:
        sorted_indices = startai.argsort(input, axis=dim)
        median_indices = startai.gather(
            sorted_indices, (sorted_indices.shape[dim] - 1) // 2, axis=dim
        )
        median_values = startai.take_along_axis(
            input, startai.expand_dims(median_indices, axis=dim), dim
        ).squeeze(axis=dim)

        if keepdim:
            median_values = startai.expand_dims(median_values, axis=dim)
            median_indices = startai.expand_dims(median_indices, axis=dim)

        result = median_tuple(median_values, median_indices)
    if out is not None:
        startai.inplace_update(out[0], result.values)
        startai.inplace_update(out[1], result.indices)
        return out
    return result


@numpy_to_torch_style_args
@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"2.2 and below": ("complex64", "complex128")},
    "torch",
)
def min(*input, dim=None, keepdim=False, out=None):
    if len(input) == 1:
        input = input[0]
    elif len(input) == 2:
        input_0 = input[0]
        input_1 = input[1]
        if startai.is_array(input_1):
            return torch_frontend.minimum(*input)
        else:
            input = input_0
            dim = input_1
    else:
        input = input[0]
        dim = input[1]
        keepdim = input[2]
    if dim is None:
        return startai.min(input, axis=dim, keepdims=keepdim, out=out)
    elif out is not None:
        startai.min(input, axis=dim, keepdims=keepdim, out=out[0])
        startai.argmin(input, axis=dim, keepdims=keepdim, out=out[1])
        return out
    else:
        min_tuple = namedtuple("min", ["values", "indices"])
        return min_tuple(
            startai.min(input, axis=dim, keepdims=keepdim),
            startai.argmin(input, axis=dim, keepdims=keepdim),
        )


@to_startai_arrays_and_back
def moveaxis(input, source, destination):
    return startai.moveaxis(input, source, destination)


@with_supported_dtypes({"2.2 and below": ("float",)}, "torch")
@numpy_to_torch_style_args
@to_startai_arrays_and_back
def nanmean(input, dim=None, keepdim=False, *, dtype=None, out=None):
    return startai.nanmean(input, axis=dim, keepdims=keepdim, dtype=dtype, out=out)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def nanmedian(input, dim=None, keepdim=False, *, out=None):
    if dim is None:
        flattened_input = startai.flatten(input)
        sorted_input = startai.sort(flattened_input)
        nonnan_index = int(sorted_input.shape[0] - startai.isnan(sorted_input).sum())
        return sorted_input[(nonnan_index - 1) // 2]

    nanmedian_tuple = namedtuple("nanmedian", ["values", "indices"])

    if input.ndim == 0:
        result = nanmedian_tuple(input, startai.array(0))
    else:
        sorted_indices = startai.argsort(input, axis=dim)
        nonnan_index = (
            sorted_indices.shape[dim] - startai.isnan(input).sum(axis=1) - 1
        ) // 2
        nonnan_index = startai.expand_dims(nonnan_index, axis=1)
        nanmedian_indices = startai.gather_nd(sorted_indices, nonnan_index, batch_dims=1)
        nanmedian_values = startai.take_along_axis(
            input, startai.expand_dims(nanmedian_indices, axis=dim), dim
        ).squeeze(axis=dim)

        if keepdim:
            nanmedian_values = startai.expand_dims(nanmedian_values, axis=dim)
            nanmedian_indices = startai.expand_dims(nanmedian_tuple, axis=dim)

        result = nanmedian_tuple(nanmedian_values, nanmedian_indices)
    if out is not None:
        startai.inplace_update(out[0], result.values)
        startai.inplace_update(out[1], result.indices)
        return out
    return result


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float", "int")},
    "torch",
)
def nansum(input, dim=None, keepdim=False, *, dtype=None):
    input = startai.where(startai.isnan(input), startai.zeros_like(input), input)
    return startai.sum(input, axis=dim, dtype=dtype, keepdims=keepdim, out=None)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float", "complex")},
    "torch",
)
def norm(input, p="fro", dim=None, keepdim=False, out=None, dtype=None):
    if dtype is None or not startai.is_float_dtype(dtype):
        dtype = "float64" if "128" in str(dtype) else "float32"
    if (
        p == "fro" and (dim is None or isinstance(dim, int) or len(dim) <= 2)
    ) or p is None:
        p = 2
    if isinstance(p, str):
        if dim is None:
            dim = tuple(range(input.dim()))
        return startai.matrix_norm(
            input, ord=p, axis=dim, keepdims=keepdim, out=out
        ).astype(dtype)
    else:
        return startai.vector_norm(
            input, ord=p, axis=dim, keepdims=keepdim, dtype=dtype, out=out
        )


@numpy_to_torch_style_args
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
def prod(input, dim=None, keepdim=False, *, dtype=None):
    if not dtype:
        if "int" in input.dtype:
            dtype = startai.int64
    return startai.prod(input, axis=dim, dtype=dtype, keepdims=keepdim)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
def quantile(input, q, dim=None, keepdim=False, *, interpolation="linear", out=None):
    return startai.quantile(
        input, q, axis=dim, keepdims=keepdim, interpolation=interpolation, out=out
    )


@numpy_to_torch_style_args
@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16", "bool", "integer")}, "torch")
def std(input, dim=None, unbiased=True, keepdim=False, *, out=None):
    return startai.std(input, axis=dim, correction=int(unbiased), keepdims=keepdim, out=out)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("bfloat16",)}, "torch")
def std_mean(input, dim, unbiased, keepdim=False, *, out=None):
    temp_std = startai.std(
        input, axis=dim, correction=int(unbiased), keepdims=keepdim, out=out
    )
    temp_mean = startai.mean(input, axis=dim, keepdims=keepdim, out=out)
    return temp_std, temp_mean


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def sum(input, dim=None, keepdim=False, *, dtype=None, out=None):
    return startai.sum(input, axis=dim, dtype=dtype, keepdims=keepdim, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@to_startai_arrays_and_back
def unique(input, sorted=True, return_inverse=False, return_counts=False, dim=None):
    if dim is not None:
        sorted = True
    results = startai.unique_all(input, axis=dim, by_value=sorted)
    ret = (results.values,) if return_counts or return_inverse else results.values
    if return_inverse:
        inverse_indices = results.inverse_indices
        if dim is None:
            inverse_indices = inverse_indices.reshape(input.shape)
        ret += (inverse_indices,)
    if return_counts:
        ret += (results.counts,)
    return ret


@with_unsupported_dtypes(
    {
        "2.2 and below": (
            "float16",
            "complex",
        )
    },
    "torch",
)
@to_startai_arrays_and_back
def unique_consecutive(input, return_inverse=False, return_counts=False, dim=None):
    output, inverse_indices, counts = startai.unique_consecutive(input, axis=dim)
    ret = (output,)
    if return_inverse:
        ret += (inverse_indices,)
    if return_counts:
        ret += (counts,)
    return ret


@numpy_to_torch_style_args
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
def var(input, dim, unbiased, keepdim=False, *, out=None):
    return startai.var(input, axis=dim, correction=int(unbiased), keepdims=keepdim, out=out)


@numpy_to_torch_style_args
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
def var_mean(input, dim, unbiased, keepdim=False, *, out=None):
    temp_var = startai.var(
        input, axis=dim, correction=int(unbiased), keepdims=keepdim, out=out
    )
    temp_mean = startai.mean(input, axis=dim, keepdims=keepdim, out=out)
    return (temp_var, temp_mean)
