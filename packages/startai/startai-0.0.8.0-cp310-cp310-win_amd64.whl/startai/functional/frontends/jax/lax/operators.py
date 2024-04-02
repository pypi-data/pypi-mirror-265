# global
from typing import Any
import itertools
import string
import builtins

# local
import startai
from startai.func_wrapper import with_supported_dtypes
from startai.functional.frontends.jax.func_wrapper import to_startai_arrays_and_back
from startai.func_wrapper import with_unsupported_dtypes, frontend_outputs_to_startai_arrays

_slice = builtins.slice


# --- Helpers --- #
# --------------- #


def _argsort_tuple(the_tuple):
    return tuple(i for i, _ in sorted(enumerate(the_tuple), key=lambda x: x[1]))


def _conv_transpose_padding(k, s, padding):
    if padding == "SAME":
        pad_len = k + s - 2
        if s > k - 1:
            pad_a = k - 1
        else:
            pad_a = int(startai.to_scalar(startai.ceil(pad_len / 2)))
    elif padding == "VALID":
        pad_len = k + s - 2 + startai.to_scalar(startai.maximum(k - s, 0))
        pad_a = k - 1
    else:
        raise ValueError("Padding mode must be `SAME` or `VALID`.")
    pad_b = pad_len - pad_a
    return pad_a, pad_b


def _dimension_numbers(dimension_numbers, lhs_len, transp=False):
    if dimension_numbers is None:
        if transp:
            iota = (0, lhs_len - 1, *range(1, lhs_len - 1))
            iotb = (lhs_len - 1, lhs_len - 2, *range(0, lhs_len - 2))
            return iota, iotb, iota
        else:
            iota = tuple(range(lhs_len))
            return iota, iota, iota
    elif isinstance(dimension_numbers[0], (tuple, list)):
        return dimension_numbers
    else:
        lhs_spec, rhs_spec, out_spec = dimension_numbers

        def getperm(spec, charpair):
            spatial = (i for i, c in enumerate(spec) if c not in charpair)
            if spec is not rhs_spec:
                spatial = sorted(spatial, key=lambda i: rhs_spec.index(spec[i]))
            return (spec.index(charpair[0]), spec.index(charpair[1])) + tuple(spatial)

        charpairs = ("N", "C"), ("O", "I"), ("N", "C")
        lhs_spec, rhs_spec, out_spec = map(getperm, dimension_numbers, charpairs)
        return lhs_spec, rhs_spec, out_spec


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def abs(x):
    return startai.abs(x)


@to_startai_arrays_and_back
def acos(x):
    return startai.acos(x)


@to_startai_arrays_and_back
def add(x, y):
    return startai.add(x, y)


@to_startai_arrays_and_back
def argmax(operand, axis, index_dtype):
    return startai.astype(startai.argmax(operand, axis=axis), index_dtype)


@to_startai_arrays_and_back
def argmin(operand, axis, index_dtype):
    return startai.astype(startai.argmin(operand, axis=axis), index_dtype)


@to_startai_arrays_and_back
def asin(x):
    return startai.asin(x)


@to_startai_arrays_and_back
def asinh(x):
    return startai.asinh(x)


@to_startai_arrays_and_back
def atan(x):
    return startai.atan(x)


@to_startai_arrays_and_back
def atan2(x, y):
    return startai.atan2(x, y)


@to_startai_arrays_and_back
def atanh(x):
    return startai.atanh(x)


@to_startai_arrays_and_back
def batch_matmul(lhs, rhs, precision=None):
    if lhs.ndim < 2 or rhs.ndim < 2:
        raise ValueError(
            f"Arguments to batch_matmul must be at least 2D, got {lhs.ndim}, {rhs.ndim}"
        )
    if lhs.ndim != rhs.ndim:
        raise ValueError(
            f"Arguments to batch_matmul must have same ndim, got {lhs.ndim}, {rhs.ndim}"
        )
    return startai.matmul(lhs, rhs).astype(lhs.dtype)


@to_startai_arrays_and_back
def bitwise_and(x, y):
    return startai.bitwise_and(x, y)


@to_startai_arrays_and_back
def bitwise_not(x):
    return startai.bitwise_invert(x)


@to_startai_arrays_and_back
def bitwise_or(x, y):
    return startai.bitwise_or(x, y)


@to_startai_arrays_and_back
def bitwise_xor(x, y):
    return startai.bitwise_xor(x, y)


@to_startai_arrays_and_back
def broadcast(operand, sizes):
    ret = startai.zeros(tuple(sizes) + tuple(startai.shape(operand)), dtype=startai.dtype(operand))
    return ret + operand


@with_supported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "float32",
            "float64",
        )
    },
    "jax",
)
@to_startai_arrays_and_back
def cbrt(x):
    return startai.pow(x, 1 / 3)


@to_startai_arrays_and_back
def ceil(x):
    return startai.ceil(x)


@to_startai_arrays_and_back
def clamp(min, x, max):
    return startai.clip(x, min, max)


@to_startai_arrays_and_back
def complex(x, y):
    return startai.complex(x, y)


@to_startai_arrays_and_back
def concatenate(operands, dimension):
    return startai.concat(operands, axis=dimension)


@to_startai_arrays_and_back
def conj(x):
    return startai.conj(x)


@to_startai_arrays_and_back
def conv(
    lhs, rhs, window_strides, padding, precision=None, preferred_element_type=None
):
    if preferred_element_type:
        lhs = startai.astype(lhs, preferred_element_type)
        rhs = startai.astype(rhs, preferred_element_type)
    dims = len(lhs.shape) - 2
    return startai.conv_general_dilated(
        lhs,
        rhs,
        window_strides,
        padding,
        dims=dims,
        data_format="channel_first",
        filter_format="channel_first",
    )


@to_startai_arrays_and_back
def conv_general_dilated(
    lhs,
    rhs,
    window_strides,
    padding,
    lhs_dilation=None,
    rhs_dilation=None,
    dimension_numbers=None,
    feature_group_count=1,
    batch_group_count=1,
    precision=None,
    preferred_element_type=None,
):
    # TODO: add support for batch_group_count
    if preferred_element_type:
        lhs = startai.astype(lhs, preferred_element_type)
        rhs = startai.astype(rhs, preferred_element_type)
    dims = len(lhs.shape) - 2
    dim_nums = _dimension_numbers(dimension_numbers, dims + 2)
    rhs_spec = tuple(dim_nums[1][i] for i in (*range(2, dims + 2), 1, 0))
    return startai.permute_dims(
        startai.conv_general_dilated(
            startai.permute_dims(lhs, axes=dim_nums[0]),
            startai.permute_dims(rhs, axes=rhs_spec),
            window_strides,
            padding,
            dims=dims,
            data_format="channel_first",
            x_dilations=1 if lhs_dilation is None else lhs_dilation,
            dilations=1 if rhs_dilation is None else rhs_dilation,
            feature_group_count=feature_group_count,
        ),
        axes=_argsort_tuple(dim_nums[2]),
    )


@to_startai_arrays_and_back
def conv_transpose(
    lhs,
    rhs,
    strides,
    padding,
    rhs_dilation=None,
    dimension_numbers=None,
    transpose_kernel=False,
    precision=None,
    preferred_element_type=None,
):
    # TODO: add support for transpose_kernel
    if preferred_element_type:
        lhs = startai.astype(lhs, preferred_element_type)
        rhs = startai.astype(rhs, preferred_element_type)
    dims = len(lhs.shape) - 2
    dim_nums = _dimension_numbers(dimension_numbers, dims + 2, transp=True)
    rhs_spec = tuple(dim_nums[1][i] for i in (*range(2, dims + 2), 1, 0))
    rhs_dilation = 1 if rhs_dilation is None else rhs_dilation
    if isinstance(padding, str):
        k_sdims = [rhs.shape[i] for i in rhs_spec[:-2]]
        effective_k_size = map(lambda k, r: (k - 1) * r + 1, k_sdims, rhs_dilation)
        padding = [
            _conv_transpose_padding(k, s, padding)
            for k, s in zip(effective_k_size, strides)
        ]
    return startai.permute_dims(
        startai.conv_general_dilated(
            startai.permute_dims(lhs, axes=dim_nums[0]),
            startai.permute_dims(rhs, axes=rhs_spec),
            1,
            padding,
            dilations=rhs_dilation,
            x_dilations=strides,
            dims=dims,
            data_format="channel_first",
        ),
        axes=_argsort_tuple(dim_nums[2]),
    )


@to_startai_arrays_and_back
def convert_element_type(operand, new_dtype):
    return startai.astype(operand, new_dtype, copy=False)


@to_startai_arrays_and_back
def cos(x):
    return startai.cos(x)


@to_startai_arrays_and_back
def cosh(x):
    return startai.cosh(x)


@with_unsupported_dtypes(
    {"0.4.24 and below": ("bfloat16", "float16", "bool", "complex64", "complex128")},
    "jax",
)
@to_startai_arrays_and_back
def cummin(operand, axis=0, reverse=False):
    return startai.cummin(operand, axis=axis, reverse=reverse, dtype=operand.dtype)


@to_startai_arrays_and_back
def cumprod(operand, axis=None, reverse=False):
    dtype = startai.dtype(operand)
    return startai.cumprod(operand, axis=axis, reverse=reverse).astype(dtype)


@to_startai_arrays_and_back
def cumsum(operand, axis=None, reverse=False):
    if reverse:
        return startai.flip(startai.cumsum(startai.flip(operand), axis=axis, dtype=operand.dtype))
    return startai.cumsum(operand, axis=axis, dtype=operand.dtype)


@to_startai_arrays_and_back
def div(x, y):
    return startai.astype(startai.divide(x, y), x.dtype)


@to_startai_arrays_and_back
def dot(lhs, rhs, precision=None, preferred_element_type=None):
    ret = startai.matmul(lhs, rhs)
    if preferred_element_type:
        ret = startai.astype(ret, preferred_element_type, copy=False)
    return ret


@with_unsupported_dtypes({"0.4.5 and below": ("bool",)}, "jax")
@to_startai_arrays_and_back
def dot_general(
    lhs, rhs, dimension_numbers, precision=None, preferred_element_type=None
):
    (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers
    startai.utils.assertions.check_less(
        len(lhs.shape),
        52,
        "number of dimensions greater than 52 is not supported",
        as_array=False,
    )
    new_id = itertools.count()
    lhs_axis_ids = [next(new_id) for _ in lhs.shape]
    rhs_axis_ids = [next(new_id) for _ in rhs.shape]
    lhs_out_axis_ids = lhs_axis_ids[:]
    rhs_out_axis_ids = rhs_axis_ids[:]
    for lhs_axis, rhs_axis in zip(lhs_contracting, rhs_contracting):
        shared_id = next(new_id)
        lhs_axis_ids[lhs_axis] = shared_id
        rhs_axis_ids[rhs_axis] = shared_id
        lhs_out_axis_ids[lhs_axis] = None
        rhs_out_axis_ids[rhs_axis] = None
    batch_ids = []
    for lhs_axis, rhs_axis in zip(lhs_batch, rhs_batch):
        shared_id = next(new_id)
        lhs_axis_ids[lhs_axis] = shared_id
        rhs_axis_ids[rhs_axis] = shared_id
        lhs_out_axis_ids[lhs_axis] = None
        rhs_out_axis_ids[rhs_axis] = None
        batch_ids.append(shared_id)
    out_axis_ids = list(
        filter(lambda x: x is not None, batch_ids + lhs_out_axis_ids + rhs_out_axis_ids)
    )
    char_list = [*string.ascii_letters]
    lhs_axis_ids = "".join(str(char_list[i]) for i in lhs_axis_ids)
    rhs_axis_ids = "".join(str(char_list[i]) for i in rhs_axis_ids)
    out_axis_ids = "".join(str(char_list[i]) for i in out_axis_ids)
    equ_str = f"{lhs_axis_ids},{rhs_axis_ids}->{out_axis_ids}"
    ret = startai.einsum(equ_str, lhs, rhs)
    if preferred_element_type:
        ret = startai.astype(ret, preferred_element_type, copy=False)
    return ret


@to_startai_arrays_and_back
def eq(x, y):
    return startai.equal(x, y)


@to_startai_arrays_and_back
def erf(x):
    return startai.erf(x)


@with_supported_dtypes(
    {
        "0.4.24 and below": (
            "float16",
            "float32",
            "float64",
        )
    },
    "jax",
)
@to_startai_arrays_and_back
def erfc(x):
    value = startai.erf(x)
    value = (1.0 - value) if value is not None else None
    return value


@to_startai_arrays_and_back
def exp(x):
    return startai.exp(x)


@to_startai_arrays_and_back
def expand_dims(array, dimensions):
    return startai.expand_dims(array, axis=dimensions)


@to_startai_arrays_and_back
def expm1(x):
    return startai.expm1(x)


@to_startai_arrays_and_back
def full(shape, fill_value, dtype=None):
    return startai.full(shape, fill_value, dtype=dtype)


@to_startai_arrays_and_back
def full_like(x, fill_value, dtype=None, shape=None):
    if shape is None:
        return startai.full_like(x, fill_value, dtype=dtype)
    return startai.full(shape, fill_value, dtype=dtype)


@with_unsupported_dtypes({"0.4.5 and below": ("complex",)}, "jax")
@to_startai_arrays_and_back
def ge(x, y):
    return startai.greater_equal(x, y)


@with_unsupported_dtypes({"0.4.5 and below": ("complex",)}, "jax")
@to_startai_arrays_and_back
def gt(x, y):
    return startai.greater(x, y)


@to_startai_arrays_and_back
def igamma(a, x):
    return startai.igamma(a, x=x)


@to_startai_arrays_and_back
def imag(x):
    return startai.imag(x)


@with_unsupported_dtypes(
    {"0.4.24 and below": ("bool", "bfloat16")},
    "jax",
)
@to_startai_arrays_and_back
def iota(dtype, size):
    return startai.arange(0, size, dtype=dtype)


@to_startai_arrays_and_back
def is_finite(x):
    return startai.isfinite(x)


@with_unsupported_dtypes({"0.4.5 and below": ("complex",)}, "jax")
@to_startai_arrays_and_back
def le(x, y):
    return startai.less_equal(x, y)


@to_startai_arrays_and_back
def log(x):
    return startai.log(x)


@to_startai_arrays_and_back
def log1p(x):
    return startai.log1p(x)


@to_startai_arrays_and_back
def lt(x, y):
    return startai.less(x, y)


@to_startai_arrays_and_back
def max(x: Any, y: Any):
    return startai.maximum(x, y)


@to_startai_arrays_and_back
def min(x, y):
    return startai.minimum(x, y)


@to_startai_arrays_and_back
def mul(x, y):
    return startai.multiply(x, y)


@to_startai_arrays_and_back
def ne(x, y):
    return startai.not_equal(x, y)


@to_startai_arrays_and_back
def neg(x):
    return startai.negative(x)


@to_startai_arrays_and_back
def nextafter(x1, x2):
    return startai.nextafter(x1, x2)


@to_startai_arrays_and_back
def pad(operand, padding_value, padding_config):
    return startai.pad(
        operand, padding_config, mode="dilated", constant_values=padding_value
    )


@to_startai_arrays_and_back
def pow(x, y):
    return startai.pow(x, y)


@to_startai_arrays_and_back
def real(x):
    return startai.real(x)


@to_startai_arrays_and_back
def reciprocal(x):
    return startai.reciprocal(x)


@to_startai_arrays_and_back
def reduce_window(
    operand,
    init_value,
    computation,
    window_dimensions,
    window_strides,
    padding,
    base_dilation=None,
    window_dilation=None,
):
    computation = frontend_outputs_to_startai_arrays(computation)
    return startai.reduce_window(
        operand,
        init_value,
        computation,
        window_dimensions,
        window_strides=window_strides,
        padding=padding,
        base_dilation=base_dilation,
        window_dilation=window_dilation,
    )


@to_startai_arrays_and_back
def rem(x, y):
    return startai.remainder(startai.abs(x), startai.abs(y)) * startai.sign(x)


@to_startai_arrays_and_back
def reshape(operand, new_sizes, dimensions=None):
    if dimensions:
        operand = startai.permute_dims(operand, dimensions)
    return startai.reshape(operand, new_sizes)


@to_startai_arrays_and_back
def rev(operand, dimensions):
    return startai.flip(operand, axis=dimensions)


@to_startai_arrays_and_back
def round(x, rounding_method=1):
    if rounding_method == 0:
        ret = startai.where(
            startai.less(x, 0),
            startai.ceil(x) - (startai.ceil(x) - startai.floor(x)),
            startai.ceil(x),
        )
    elif rounding_method == 1:
        ret = startai.ceil(x)
        ret = startai.where(startai.remainder(ret, 2) == 0, ret, ret - 1)
    return startai.where(startai.abs(x - startai.floor(x) - 0.5) < 1e-7, ret, startai.round(x))


@to_startai_arrays_and_back
def rsqrt(x):
    return startai.reciprocal(startai.sqrt(x))


@to_startai_arrays_and_back
def select(pred, on_true, on_false):
    return startai.where(pred, on_true, on_false)


@to_startai_arrays_and_back
def shift_left(x, y):
    return startai.bitwise_left_shift(x, y)


@to_startai_arrays_and_back
def shift_right_logical(x, y):
    return startai.bitwise_right_shift(x, y)


@to_startai_arrays_and_back
def sign(x):
    return startai.sign(x, np_variant=False)


@to_startai_arrays_and_back
def sin(x):
    return startai.sin(x)


@to_startai_arrays_and_back
def sinh(x):
    return startai.sinh(x)


@to_startai_arrays_and_back
def slice(operand, start_indices, limit_indices, strides=None):
    strides = [1] * len(operand.shape) if strides is None else strides

    full_slice = ()
    for i, _ in enumerate(operand.shape):
        strides_i = int(strides[i])
        start_i = int(start_indices[i])
        limit_i = int(limit_indices[i])
        full_slice += (_slice(start_i, limit_i, strides_i),)
    return operand[full_slice]


@to_startai_arrays_and_back
def slice_in_dim(operand, start_index, limit_index, stride=1, axis=0):
    start_indices = [0] * operand.ndim
    limit_indices = list(operand.shape)
    strides = [1] * operand.ndim

    len_axis = operand.shape[axis]
    start_index_int = start_index if start_index is not None else 0
    limit_index_int = limit_index if limit_index is not None else len_axis

    if start_index_int < 0:
        start_index_int = start_index_int + len_axis
    if limit_index_int < 0:
        limit_index_int = limit_index_int + len_axis

    axis = int(axis)
    start_indices[axis] = start_index_int
    limit_indices[axis] = limit_index_int
    strides[axis] = int(stride)
    return slice(operand, start_indices, limit_indices, strides)


@to_startai_arrays_and_back
def sort(operand, dimension=-1, is_stable=True, num_keys=1):
    return startai.sort(operand, axis=dimension, stable=is_stable)


@to_startai_arrays_and_back
def sqrt(x):
    return startai.sqrt(x)


@to_startai_arrays_and_back
def square(x):
    return startai.square(x)


@to_startai_arrays_and_back
def squeeze(array, dimensions):
    return startai.squeeze(array, axis=dimensions)


@to_startai_arrays_and_back
def sub(x, y):
    return startai.subtract(x, y)


@to_startai_arrays_and_back
def tan(x):
    return startai.tan(x)


@to_startai_arrays_and_back
def tie_in(x, y):
    return y


# top_k
@to_startai_arrays_and_back
def top_k(operand, k):
    values, indices = startai.top_k(operand, k, axis=-1)
    indices = startai.astype(indices, startai.int32, copy=False)
    return [values, indices]


@to_startai_arrays_and_back
def transpose(operand, permutation):
    return startai.permute_dims(operand, permutation)
