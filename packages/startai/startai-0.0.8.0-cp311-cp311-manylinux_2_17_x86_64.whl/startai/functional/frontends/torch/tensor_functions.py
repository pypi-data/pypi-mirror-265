# local
import startai
from startai.func_wrapper import with_supported_dtypes
from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def broadcast_tensors(*tensors):
    return startai.broadcast_arrays(*tensors)


@to_startai_arrays_and_back
def is_complex(input):
    return startai.is_complex_dtype(input)


@to_startai_arrays_and_back
def is_floating_point(input):
    return startai.is_float_dtype(input)


@to_startai_arrays_and_back
def is_nonzero(input):
    return startai.nonzero(input)[0].size != 0


@to_startai_arrays_and_back
def is_tensor(obj):
    return startai.is_array(obj)


@to_startai_arrays_and_back
def numel(input):
    return startai.astype(startai.array(input.size), startai.int64)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "int32", "int64")}, "torch"
)
def scatter(input, dim, index, src):
    return startai.put_along_axis(input, index, src, dim, mode="replace")


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "int32", "int64")}, "torch"
)
def scatter_add(input, dim, index, src):
    return startai.put_along_axis(input, index, src, dim, mode="sum")


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "int32", "int64")}, "torch"
)
def scatter_reduce(input, dim, index, src, reduce, *, include_self=True):
    mode_mappings = {
        "sum": "sum",
        "amin": "min",
        "amax": "max",
        "prod": "mul",
        "replace": "replace",
    }
    reduce = mode_mappings.get(reduce, reduce)
    return startai.put_along_axis(input, index, src, dim, mode=reduce)
