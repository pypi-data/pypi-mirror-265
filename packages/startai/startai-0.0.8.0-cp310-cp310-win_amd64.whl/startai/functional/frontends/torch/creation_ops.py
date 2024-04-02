# local
import startai
from startai.functional.frontends.torch.func_wrapper import (
    to_startai_arrays_and_back,
    to_startai_shape,
)
from startai.func_wrapper import (
    with_unsupported_dtypes,
    with_supported_dtypes,
)
import startai.functional.frontends.torch as torch_frontend


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def arange(
    start=0,
    end=None,
    step=1,
    *,
    out=None,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
):
    return startai.arange(start, end, step, dtype=dtype, device=device, out=out)


@to_startai_arrays_and_back
def as_strided(input, size, stride, storage_offset=None):
    ind = startai.array([0], dtype=startai.int64)
    for i, (size_i, stride_i) in enumerate(zip(size, stride)):
        r_size = [1] * len(stride)
        r_size[i] = -1
        ind = ind + startai.reshape(startai.arange(size_i), r_size) * stride_i
    if storage_offset:
        ind = ind + storage_offset
    # in case the input is a non-contiguous native array,
    # the return will differ from torch.as_strided
    if startai.is_startai_array(input) and input.base is not None:
        return startai.gather(startai.flatten(input.base), ind)
    return startai.gather(startai.flatten(input), ind)


@to_startai_arrays_and_back
def as_tensor(
    data,
    *,
    dtype=None,
    device=None,
):
    if dtype is None:
        if isinstance(data, int):
            dtype = startai.int64
        elif isinstance(data, float):
            dtype = torch_frontend.get_default_dtype()
        elif isinstance(data, (list, tuple)):
            if all(isinstance(d, int) for d in data):
                dtype = startai.int64
            else:
                dtype = torch_frontend.get_default_dtype()
    return startai.asarray(data, dtype=dtype, device=device)


@to_startai_arrays_and_back
def asarray(
    obj,
    *,
    dtype=None,
    device=None,
    copy=None,
):
    return startai.asarray(obj, copy=copy, dtype=dtype, device=device)


@with_supported_dtypes({"2.2 and below": ("float32", "float64")}, "torch")
@to_startai_arrays_and_back
def complex(
    real,
    imag,
    *,
    out=None,
):
    assert real.dtype == imag.dtype, TypeError(
        "Expected real and imag to have the same dtype, "
        f" but got real.dtype = {real.dtype} and imag.dtype = {imag.dtype}."
    )

    complex_dtype = startai.complex64 if real.dtype != startai.float64 else startai.complex128
    complex_array = real + imag * 1j
    return complex_array.astype(complex_dtype, out=out)


@to_startai_arrays_and_back
def empty(
    *args,
    size=None,
    out=None,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    pin_memory=False,
    memory_format=None,
):
    if args and size:
        raise TypeError("empty() got multiple values for argument 'shape'")
    if size is None:
        size = (
            args[0]
            if isinstance(args[0], (tuple, list, startai.Shape, startai.NativeShape))
            else args
        )
    if isinstance(size, (tuple, list)):
        size = tuple(s.to_scalar() if startai.is_array(s) else s for s in size)
    return startai.empty(shape=size, dtype=dtype, device=device, out=out)


@to_startai_arrays_and_back
def empty_like(
    input,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    memory_format=None,
):
    ret = startai.empty_like(input, dtype=dtype, device=device)
    return ret


@to_startai_arrays_and_back
def empty_strided(
    size,
    stride,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    pin_memory=False,
):
    max_offsets = [(s - 1) * st for s, st in zip(size, stride)]
    items = sum(max_offsets) + 1
    empty_array = empty(items, dtype=dtype, device=device)
    strided_array = as_strided(empty_array, size, stride)
    return strided_array


@to_startai_arrays_and_back
def eye(
    n, m=None, *, out=None, dtype=None, layout=None, device=None, requires_grad=False
):
    return startai.eye(n, m, dtype=dtype, device=device, out=out)


@to_startai_arrays_and_back
def from_dlpack(ext_tensor):
    return startai.from_dlpack(ext_tensor)


@to_startai_arrays_and_back
def from_numpy(data, /):
    return startai.asarray(data, dtype=startai.dtype(data))


@to_startai_arrays_and_back
def frombuffer(
    buffer,
    *,
    dtype,
    count=-1,
    offset=0,
    requires_grad=False,
):
    return startai.frombuffer(buffer, dtype=dtype, count=count, offset=offset)


@with_unsupported_dtypes({"2.2.0 and below": ("bfloat16",)}, "torch")
@to_startai_arrays_and_back
def full(
    size,
    fill_value,
    *,
    out=None,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=None,
):
    ret = startai.full(size, fill_value, dtype=dtype, device=device, out=out)
    return ret


@to_startai_arrays_and_back
def full_like(
    input,
    fill_value,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    memory_format=None,
):
    fill_value = startai.to_scalar(fill_value)
    return startai.full_like(input, fill_value, dtype=dtype, device=device)


@to_startai_arrays_and_back
def heaviside(input, values, *, out=None):
    return startai.heaviside(input, values, out=out)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def linspace(
    start,
    end,
    steps,
    *,
    out=None,
    dtype=None,
    device=None,
    layout=None,
    requires_grad=False,
):
    dtype = torch_frontend.get_default_dtype() if dtype is None else dtype
    return startai.linspace(start, end, num=steps, dtype=dtype, device=device, out=out)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def logspace(
    start,
    end,
    steps,
    *,
    base=10.0,
    out=None,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
):
    ret = startai.logspace(
        start, end, num=steps, base=base, dtype=dtype, device=device, out=out
    )
    return ret


@to_startai_shape
@to_startai_arrays_and_back
def ones(*args, size=None, out=None, dtype=None, device=None, requires_grad=False):
    if args and size:
        raise TypeError("ones() got multiple values for argument 'shape'")
    if size is None:
        size = (
            args[0]
            if isinstance(args[0], (tuple, list, startai.Shape, startai.NativeShape))
            else args
        )
    return startai.ones(shape=size, dtype=dtype, device=device, out=out)


@to_startai_arrays_and_back
def ones_like_v_0p3p0_to_0p3p1(input, out=None):
    return startai.ones_like(input, out=None)


@to_startai_arrays_and_back
def ones_like_v_0p4p0_and_above(
    input,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    memory_format=None,
):
    ret = startai.ones_like(input, dtype=dtype, device=device)
    return ret


@with_supported_dtypes({"2.2 and below": ("float32", "float64")}, "torch")
@to_startai_arrays_and_back
def polar(
    abs,
    angle,
    *,
    out=None,
):
    return complex(abs * angle.cos(), abs * angle.sin(), out=out)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def range(
    *args,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
):
    if len(args) == 1:
        end = args[0]
        start = 0
        step = 1
    elif len(args) == 2:
        end = args[1]
        start = args[0]
        step = 1
    elif len(args) == 3:
        start, end, step = args
    else:
        startai.utils.assertions.check_true(
            len(args) == 1 or len(args) == 3,
            "only 1 or 3 positional arguments are supported",
        )
    range_vec = []
    elem = start
    while 1:
        range_vec = range_vec + [elem]
        elem += step
        if start == end:
            break
        if start < end:
            if elem > end:
                break
        else:
            if elem < end:
                break
    return startai.array(range_vec, dtype=dtype, device=device)


@to_startai_arrays_and_back
def tensor(
    data,
    *,
    dtype=None,
    device=None,
    requires_grad=False,
    pin_memory=False,
):
    return startai.array(data, dtype=dtype, device=device)


@to_startai_shape
@to_startai_arrays_and_back
def zeros(*args, size=None, out=None, dtype=None, device=None, requires_grad=False):
    if args and size:
        raise TypeError("zeros() got multiple values for argument 'shape'")
    if size is None:
        size = (
            args[0]
            if isinstance(args[0], (tuple, list, startai.Shape, startai.NativeShape))
            else args
        )
    return startai.zeros(shape=size, dtype=dtype, device=device, out=out)


@to_startai_arrays_and_back
def zeros_like(
    input,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    memory_format=None,
):
    ret = startai.zeros_like(input, dtype=dtype, device=device)
    return ret
