# global
from builtins import slice as py_slice, range as py_range

# local
import startai
from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from startai.functional.frontends.tensorflow.func_wrapper import (
    to_startai_arrays_and_back,
    handle_tf_dtype,
    to_startai_dtype,
)
from startai.functional.frontends.tensorflow.tensor import EagerTensor
import startai.functional.frontends.tensorflow as tf_frontend
from startai.functional.frontends.tensorflow import check_tensorflow_casting
import functools


# --- Helpers --- #
# --------------- #


def _num_to_bit_list(value, num_dims):
    return list(map(int, f"{value:0{num_dims}b}"))[::-1]


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def argsort(values, axis=-1, direction="ASCENDING", stable=False, name=None):
    if direction == "DESCENDING":
        descending = True
    else:
        descending = False
    return startai.argsort(values, axis=axis, descending=descending, stable=stable).astype(
        "int32"
    )


@to_startai_arrays_and_back
def boolean_mask(tensor, mask, axis=None, name=None):
    if axis is None or axis == 0:
        return startai.get_item(tensor, mask)
    else:
        n = startai.get_num_dims(tensor)
        k = startai.get_num_dims(mask)
        if axis < 0:
            axis = n + axis
        startai.utils.assertions.check_less(
            k + axis,
            n,
            allow_equal=True,
            message="Value of axis must be such that axis + dim(mask) <= dim(tensor)",
            as_array=False,
        )
        tensor_shape = startai.shape(tensor)
        range_array = startai.arange(axis - 1, -1, -1)
        for i in startai.to_list(range_array):
            mask = startai.expand_dims(mask, axis=0)
            mask = startai.repeat(mask, tensor_shape[i], axis=0)
        return startai.get_item(tensor, mask)


@with_supported_dtypes({"2.15.0 and below": ("float32",)}, "tensorflow")
@to_startai_arrays_and_back
def clip_by_global_norm(t_list, clip_norm, use_norm=None):
    if use_norm is not None:
        global_norm = use_norm
    else:
        global_norm = startai.sqrt(startai.sum([startai.vector_norm(t) ** 2 for t in t_list]))

    max_clip_ratio = startai.maximum(clip_norm, global_norm)
    return [
        startai.multiply(t, startai.divide(clip_norm, max_clip_ratio)) for t in t_list
    ], global_norm


@with_supported_dtypes({"2.15.0 and below": ("float", "complex")}, "tensorflow")
@to_startai_arrays_and_back
def clip_by_norm(t, clip_norm, axes=None):
    t, clip_norm = check_tensorflow_casting(t, clip_norm)
    l2sum = startai.sum(t * t, axis=axes, keepdims=True)
    pred = l2sum > 0

    l2sum_safe = startai.where(pred, l2sum, startai.ones_like(l2sum))
    l2norm = startai.where(pred, startai.sqrt(l2sum_safe), l2sum)
    intermediate = t * clip_norm
    assert (
        t.shape == intermediate.shape
    ), f"Dimensions {t.shape} and {intermediate.shape} are not compatible"
    t_clip = intermediate / startai.maximum(l2norm, clip_norm)
    return t_clip


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.15.0 and below": ("float16",)}, "tensorflow")
def clip_by_value(t, clip_value_min, clip_value_max):
    startai.utils.assertions.check_all_or_any_fn(
        clip_value_min,
        clip_value_max,
        fn=startai.exists,
        type="all",
        message="clip_value_min and clip_value_max must exist",
    )
    t = startai.array(t)
    return startai.clip(t, clip_value_min, clip_value_max)


@to_startai_arrays_and_back
def concat(values, axis, name=None):
    return startai.concat(values, axis=axis)


@to_startai_arrays_and_back
def cond(pred, true_fn=None, false_fn=None, name=None):
    if true_fn is None:
        raise TypeError("cond(): 'true_fn' argument required")
    if false_fn is None:
        raise TypeError("cond(): 'false_fn' argument required")

    if not callable(true_fn):
        raise TypeError("'true_fn' must be callable.")
    if not callable(false_fn):
        raise TypeError("'false_fn' must be callable.")

    if pred:
        return true_fn()

    if not pred:
        return false_fn()


@handle_tf_dtype
def constant(value, dtype=None, shape=None, name=None):
    if shape is not None:
        value = startai.reshape(value, shape=shape)
    if dtype is not None:
        return EagerTensor(startai.astype(value, dtype))
    return EagerTensor(value)


@handle_tf_dtype
def convert_to_tensor(value, dtype=None, dtype_hint=None, name=None):
    if dtype:
        return tf_frontend.cast(value, dtype)
    elif dtype_hint:
        return tf_frontend.cast(value, dtype_hint)
    if hasattr(value, "startai_array"):
        return EagerTensor(value.startai_array)
    return EagerTensor(value)


@to_startai_arrays_and_back
def einsum(equation, *inputs, **kwargs):
    return startai.einsum(equation, *inputs)


@to_startai_arrays_and_back
def ensure_shape(x, shape, name=None):
    x = EagerTensor(x)
    x.set_shape(shape)

    return x


@to_startai_arrays_and_back
def expand_dims(input, axis, name=None):
    return startai.expand_dims(input, axis=axis)


@with_unsupported_dtypes({"2.15.0 and below": ("float16", "bfloat16")}, "tensorflow")
@handle_tf_dtype
@to_startai_arrays_and_back
def eye(num_rows, num_columns=None, batch_shape=None, dtype=startai.float32, name=None):
    return startai.eye(num_rows, num_columns, batch_shape=batch_shape, dtype=dtype)


@to_startai_arrays_and_back
def fill(dims, value, name=None):
    return startai.full(dims, value)


@to_startai_arrays_and_back
def foldl(
    fn,
    elems,
    initializer=None,
    parallel_iterations=10,
    swap_memory=False,
    name=None,
):
    startai.utils.assertions.check_isinstance(
        elems, (list, startai.Array), "elems must be an iterable object"
    )
    startai.utils.assertions.check_true(
        callable(fn), f"{fn.__name__} must be a callable function"
    )
    if len(startai.shape(elems)) == 0 or startai.get_num_dims(elems) == 0:
        raise startai.utils.exceptions.StartaiValueError(
            "elems must be a non-empty iterable object with at least one dimension"
        )
    if initializer is not None:
        result = functools.reduce(fn, elems, initializer)
    elif initializer is None and startai.shape(elems)[0] > 0:
        result = functools.reduce(fn, elems[1:], elems[0])
    else:
        result = elems
    if all(startai.get_num_dims(e) == 0 for e in elems):
        result = startai.to_scalar(result)

    return result


@with_unsupported_dtypes({"2.6.0 and below": ("float16", "bfloat16")}, "paddle")
@to_startai_arrays_and_back
def foldr(
    fn,
    elems,
    initializer=None,
    parallel_iterations=10,
    back_prop=True,
    swap_memory=False,
    name=None,
):
    startai.utils.assertions.check_isinstance(
        elems, (list, startai.Array), "elems must be an iterable object"
    )
    startai.utils.assertions.check_true(
        callable(fn), f"{fn.__name__} must be a callable function"
    )
    if len(startai.shape(elems)) == 0 or startai.get_num_dims(elems) == 0:
        raise startai.utils.exceptions.StartaiValueError(
            "elems must be a non-empty iterable object with at least one dimension"
        )

    elems = startai.flip(elems)

    if initializer is not None:
        result = functools.reduce(fn, elems, initializer)
    elif initializer is None and startai.shape(elems)[0] > 0:
        result = functools.reduce(fn, elems[1:], elems[0])
    else:
        result = elems
    if all(startai.get_num_dims(e) == 0 for e in elems):
        result = startai.to_scalar(result)
    result = startai.flip(result)
    return result


@to_startai_arrays_and_back
def gather(params, indices, validate_indices=None, axis=None, batch_dims=0, name=None):
    if axis is None:
        axis = batch_dims
    else:
        axis = axis % len(params.shape)
    axis = max(axis, batch_dims)
    return startai.gather(params, indices, axis=axis, batch_dims=batch_dims)


@to_startai_arrays_and_back
def gather_nd(params, indices, batch_dims=0, name=None):
    return startai.gather_nd(params, indices, batch_dims=batch_dims)


@to_startai_arrays_and_back
def identity(input, name=None):
    return startai.copy_array(input)


@to_startai_arrays_and_back
def identity_n(input, name=None):
    return [startai.copy_array(x) for x in input]


@to_startai_arrays_and_back
def is_tensor(x, name=None):
    return startai.is_array(x)


@to_startai_arrays_and_back
def linspace(start, stop, num, name=None, axis=0):
    return startai.linspace(start, stop, num, axis=axis)


@to_startai_arrays_and_back
def meshgrid(*args, **kwargs):
    sparse = False
    indexing = "xy"
    if "indexing" in kwargs:
        indexing = kwargs["indexing"]

    return startai.meshgrid(*args, sparse=sparse, indexing=indexing)


@to_startai_arrays_and_back
def no_op(name=None):
    return


@with_supported_dtypes({"2.15.0 and below": ("float32", "float64")}, "tensorflow")
@to_startai_arrays_and_back
def norm(tensor, ord="euclidean", axis=None, keepdims=None, name=None):
    return tf_frontend.linalg.norm(
        tensor, ord=ord, axis=axis, keepdims=keepdims, name=name
    )


@to_startai_arrays_and_back
def one_hot(
    indices: startai.Array,
    depth: int,
    on_value=None,
    off_value=None,
    axis=None,
    dtype=None,
    device=None,
    out=None,
):
    return startai.one_hot(indices, depth)


@with_unsupported_dtypes({"2.15.0 and below": ("float16", "bfloat16")}, "tensorflow")
@handle_tf_dtype
@to_startai_arrays_and_back
def ones(shape, dtype=startai.float32, name=None):
    return startai.ones(shape, dtype=dtype)


@handle_tf_dtype
@to_startai_arrays_and_back
def ones_like(input, dtype=None, name=None):
    return startai.ones_like(input, dtype=dtype)


@to_startai_arrays_and_back
def pad(tensor, paddings, mode="CONSTANT", constant_values=0, name=None):
    paddings = paddings.to_list() if startai.is_array(paddings) else paddings
    return startai.pad(tensor, paddings, mode=mode.lower(), constant_values=constant_values)


@with_unsupported_dtypes({"2.15.0 and below": ("float16", "bfloat16")}, "tensorflow")
@handle_tf_dtype
@to_startai_arrays_and_back
def range(start, limit=None, delta=1, dtype=None, name=None):
    return startai.arange(start, limit, delta, dtype=dtype)


@to_startai_arrays_and_back
def rank(input, **kwargs):
    return startai.astype(startai.array(input.ndim), startai.int32)


@with_unsupported_dtypes({"2.15.0 and below": ("unsigned", "integer")}, "tensorflow")
@to_startai_arrays_and_back
def realdiv(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.divide(x, y)


@to_startai_arrays_and_back
def repeat(
    input,
    repeats,
    axis=None,
    name=None,
):
    return startai.repeat(input, repeats, axis=axis)


@to_startai_arrays_and_back
def reshape(tensor, shape, name=None):
    shape = shape.to_list() if startai.is_array(shape) else shape
    return startai.reshape(tensor, shape=shape)


@to_startai_arrays_and_back
def reverse(tensor, axis, name=None):
    return startai.flip(tensor, axis=axis)


@to_startai_arrays_and_back
def roll(input, shift, axis, name=None):
    return startai.roll(input, shift, axis=axis)


@to_startai_arrays_and_back
def scan(
    fn,
    elems,
    initializer=None,
    parallel_iterations=10,
    back_prop=True,
    swap_memory=False,
    infer_shape=True,
    reverse=False,
    name=None,
):
    elems = startai.asarray(elems)
    return startai.associative_scan(elems, fn, reverse=reverse)


@to_startai_arrays_and_back
def searchsorted(sorted_sequence, values, side="left", out_type="int32"):
    out_type = to_startai_dtype(out_type)
    if out_type not in ["int32", "int64"]:
        out_type = "int64"
    return startai.searchsorted(sorted_sequence, values, side=side, ret_dtype=out_type)


@with_supported_dtypes(
    {"2.15.0 and below": ("int8", "int16", "int32", "int64")}, "tensorflow"
)
@to_startai_arrays_and_back
def sequence_mask(lengths, maxlen=None, dtype=startai.bool, name=None):
    if maxlen is None:
        maxlen = startai.maximum(
            startai.max(lengths), startai.max(startai.arange(startai.get_num_dims(lengths)))
        )
        maxlen = startai.maximum(0, maxlen)
    else:
        maxlen = startai.array(maxlen)
    if startai.get_num_dims(maxlen) is not None and startai.get_num_dims(maxlen) != 0:
        raise ValueError(
            "Argument `maxlen` must be scalar for sequence_mask, "
            f"received `maxlen` = {maxlen} "
            f"with shape '{maxlen.get_shape()}' instead"
        )

    row_vector = startai.arange(0, int(maxlen), 1)
    matrix = startai.expand_dims(lengths, axis=-1)
    result = row_vector < matrix
    if dtype is None:
        return result
    else:
        return startai.astype(result, dtype)


@to_startai_arrays_and_back
def shape(input, out_type=startai.int32, name=None):
    out_type = to_startai_dtype(out_type)
    if out_type in ["int32", "int64"]:
        return startai.array(startai.shape(input), dtype=out_type)
    else:
        return startai.array(startai.shape(input), dtype="int64")


@to_startai_arrays_and_back
def shape_n(input, out_type=startai.int32, name=None):
    out_type = to_startai_dtype(out_type)
    if out_type in ["int32", "int64"]:
        return [startai.array(startai.shape(i), dtype=out_type) for i in input]
    else:
        return [startai.array(startai.shape(i), dtype="int64") for i in input]


@to_startai_arrays_and_back
def size(input, out_type=startai.int32, name=None):
    out_type = to_startai_dtype(out_type)
    shape = startai.shape(input, as_array=True)
    return startai.astype(startai.prod(shape), out_type, copy=False)


@to_startai_arrays_and_back
def slice(input_, begin, size, name=None):
    return strided_slice(input_, begin, begin + size)


@to_startai_arrays_and_back
def sort(values, axis=-1, direction="ASCENDING", name=None):
    descending = True
    if direction == "ASCENDING":
        descending = False
    else:
        startai.utils.assertions.check_equal(
            direction,
            "DESCENDING",
            message="Argument `direction` should be one of 'ASCENDING' or 'DESCENDING'",
            as_array=False,
        )
    return startai.sort(values, axis=axis, descending=descending)


@with_unsupported_dtypes(
    {"2.15.0 and below": ("uint8", "uint16", "uint32", "uint64", "int16")}, "tensorflow"
)
@to_startai_arrays_and_back
def split(value, num_or_size_splits, axis=0, num=None, name=None):
    return startai.split(
        value, num_or_size_splits=num_or_size_splits, axis=axis, with_remainder=True
    )


@to_startai_arrays_and_back
def squeeze(input, axis=None, name=None):
    return startai.squeeze(input, axis=axis)


@to_startai_arrays_and_back
def stack(values, axis=0, name="stack"):
    return startai.stack(values, axis=axis)


@to_startai_arrays_and_back
def stop_gradient(input, name=None):
    return startai.stop_gradient(input)


# ToDo: find a way around for negative indexing, which torch does not support
@to_startai_arrays_and_back
def strided_slice(
    input_,
    begin,
    end,
    strides=None,
    begin_mask=0,
    end_mask=0,
    ellipsis_mask=0,
    new_axis_mask=0,
    shrink_axis_mask=0,
    var=None,
    name=None,
):
    input_shape = list(input_.shape)
    input_rank = len(input_shape)
    begin_mask, end_mask, ellipsis_mask, new_axis_mask, shrink_axis_mask = list(
        map(
            _num_to_bit_list,
            [begin_mask, end_mask, ellipsis_mask, new_axis_mask, shrink_axis_mask],
            [input_rank] * 5,
        )
    )
    begin, end, strides = map(
        lambda x: startai.array(x) if isinstance(x, int) else x, [begin, end, strides]
    )
    num_defined = len(begin)
    strides = startai.repeat(startai.array(1), num_defined) if strides is None else strides
    startai.assertions.check_true(
        num_defined == len(end) == len(strides),
        message="`begin`, `end`, and `strides` are expected to have the same length",
    )
    begin, end, strides = map(
        lambda x: [startai.to_scalar(i) for i in x] if startai.is_startai_array(x) else x,
        [begin, end, strides],
    )
    for i, v in enumerate(shrink_axis_mask):
        if v == 1:
            begin_mask[i] = 0
    ellipsis_indices = [i for i, v in enumerate(ellipsis_mask) if v]
    if len(ellipsis_indices) > 1:
        raise ValueError("Multiple ellipses are not allowed.")
    elif len(ellipsis_indices) == 1:
        ellipsis_index = ellipsis_indices[0]
        num_missing = input_rank - len(begin)
        if num_missing == 0:
            begin_mask[ellipsis_index] = 1
            end_mask[ellipsis_index] = 1
            shrink_axis_mask[ellipsis_index] = 0
            new_axis_mask[ellipsis_index] = 0
        else:
            for i in py_range(ellipsis_index, ellipsis_index + num_missing + 1, 1):
                if i < input_rank:
                    shrink_axis_mask[i] = 0
                    new_axis_mask[i] = 0
                else:
                    break
            if ellipsis_index >= len(begin):
                begin = begin + [None] * num_missing
                end = end + [None] * num_missing
                strides = strides + [1] * num_missing
            else:
                begin = (
                    begin[:ellipsis_index]
                    + [None] * (num_missing + 1)
                    + begin[ellipsis_index + 1 :]
                )
                end = (
                    end[:ellipsis_index]
                    + [None] * (num_missing + 1)
                    + end[ellipsis_index + 1 :]
                )
                strides = (
                    strides[:ellipsis_index]
                    + [1] * (num_missing + 1)
                    + strides[ellipsis_index + 1 :]
                )
    full_slice = ()
    for i, _ in enumerate(begin):
        if new_axis_mask[i]:
            full_slice += (startai.newaxis,)
        else:
            b = None if begin_mask[i] else begin[i]
            e = None if end_mask[i] else end[i]
            s = strides[i]
            if b is None and e is None:
                s = 1 if ellipsis_mask[i] else s
            elif shrink_axis_mask[i]:
                if b is not None:
                    e = b + 1 if s > 0 else b - 1
                else:
                    e = 1 if s > 0 else input_shape[i] - 2
            full_slice += (py_slice(b, e, s),)
    if all(i is None for i in full_slice):
        full_slice += (...,)
    ret = input_[full_slice]
    shrink_indices = [
        i
        for i, v in enumerate(shrink_axis_mask)
        if v and i < len(ret.shape) and ret.shape[i] == 1
    ]
    ret = startai.squeeze(ret, axis=shrink_indices)
    return ret


@to_startai_arrays_and_back
def tensor_scatter_nd_add(tensor, indices, updates, name=None):
    zero_tensor = startai.zeros_like(tensor)
    scatter_tensor = startai.scatter_nd(indices, updates, zero_tensor.shape)
    return startai.add(tensor, scatter_tensor)


@with_unsupported_dtypes({"2.15.0 and below": ("uint16",)}, "tensorflow")
@to_startai_arrays_and_back
def tile(input, multiples, name=None):
    return startai.tile(input, multiples)


@to_startai_arrays_and_back
def transpose(a, perm=None, conjugate=False, name="transpose"):
    # handle conjugate when startai supports complex numbers
    if perm is not None:
        return startai.permute_dims(a, axes=perm)
    n = a.ndim
    perm = startai.arange(n - 1, -1, -1)
    return startai.permute_dims(a, axes=perm)


@with_unsupported_dtypes({"2.15.0 and below": ("float16", "bfloat16")}, "tensorflow")
@to_startai_arrays_and_back
def truncatediv(x, y, name=None):
    return x.trunc_divide(y)


@with_unsupported_dtypes(
    {"2.15.0 and below": ("int16", "int8", "uint8", " uint16")}, "tensorflow"
)
@to_startai_arrays_and_back
def truncatemod(x, y):
    x = startai.broadcast_to(x, startai.shape(y))
    y = startai.broadcast_to(y, startai.shape(x))
    return startai.trunc(x / y) * y + (x % y)


@to_startai_arrays_and_back
def unique(x, out_idx=startai.int32, name=None):
    ret = startai.unique_all(x, by_value=False)
    y = ret[0]
    idx = startai.astype(ret[2], out_idx)
    return y, idx


@to_startai_arrays_and_back
def unique_with_counts(x, out_idx="int32", name=None):
    x = x.to_list() if startai.is_array(x) else x

    startai.utils.assertions.check_equal(
        startai.array(x).ndim,
        1,
        message="unique_with_counts expects a 1D vector.",
    )
    startai.utils.assertions.check_elem_in_list(
        out_idx,
        ["int32", "int64"],
        message=(
            f"Value for attr 'out_idx' of {out_idx} is not in the list of allowed"
            " values: [int32, int64]"
        ),
    )

    values = []
    indices = []
    counts = []

    for element in x:
        if element not in values:
            values.append(element)
            indices.append(len(values) - 1)
            counts.append(1)
        else:
            index = values.index(element)
            counts[index] += 1
            indices.append(index)

    return (
        startai.array(values),
        startai.array(indices, dtype=out_idx),
        startai.array(counts, dtype=out_idx),
    )


@to_startai_arrays_and_back
def unravel_index(indices, dims, out=None, name=None):
    return startai.unravel_index(indices, dims, out=out)


@with_unsupported_dtypes({"2.15.0 and below": ("float16", "bfloat16")}, "tensorflow")
@to_startai_arrays_and_back
def unstack(value: startai.Array, axis=0, num=None, name=None):
    return startai.unstack(value, axis=axis)


@to_startai_arrays_and_back
def where(condition: startai.Array, x=None, y=None, name=None):
    if x is None and y is None:
        return startai.argwhere(condition)
    else:
        return startai.where(condition, x, y)


@to_startai_arrays_and_back
def while_loop(
    cond,
    body,
    loop_vars,
    shape_invariants=None,
    parallel_iterations=10,
    back_prop=True,
    swap_memory=False,
    maximum_iterations=None,
    name=None,
):
    return startai.while_loop(test_fn=cond, body_fn=body, vars=loop_vars)


@handle_tf_dtype
@to_startai_arrays_and_back
def zeros(shape, dtype=startai.float32, name=None):
    return startai.zeros(shape=shape, dtype=dtype)


@with_unsupported_dtypes({"2.15.0 and below": ("float16", "bfloat16")}, "tensorflow")
@to_startai_arrays_and_back
def zeros_initializer(shape, dtype=None, name=None):
    # todo internal: fix behaviour
    if dtype is None:
        dtype = startai.default_dtype()
    return startai.zeros(shape, dtype=dtype)


@handle_tf_dtype
@to_startai_arrays_and_back
def zeros_like(input, dtype=None, name=None):
    return startai.zeros_like(input, dtype=dtype)
