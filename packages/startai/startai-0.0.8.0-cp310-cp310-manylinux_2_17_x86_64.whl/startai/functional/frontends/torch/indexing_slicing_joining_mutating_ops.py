# local
import startai
from startai.func_wrapper import with_unsupported_dtypes
from startai.functional.frontends.torch.func_wrapper import (
    to_startai_arrays_and_back,
    numpy_to_torch_style_args,
    to_startai_shape,
)
import startai.functional.frontends.torch as torch_frontend


@to_startai_arrays_and_back
def adjoint(input):
    return startai.adjoint(input)


@to_startai_arrays_and_back
def argwhere(input):
    return startai.argwhere(input)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def cat(tensors, dim=0, *, out=None):
    return startai.concat(tensors, axis=dim, out=out)


@to_startai_arrays_and_back
def chunk(input, chunks, dim=0):
    if startai.shape(input) == ():
        return [input]
    else:
        dim_size = startai.shape(input)[dim]
        chunk_size = dim_size // chunks
        if chunk_size == 0:
            return startai.split(input, num_or_size_splits=dim_size, axis=dim)
        else:
            remainder = dim_size % chunks
            if remainder == 0:
                return startai.split(input, num_or_size_splits=chunks, axis=dim)
            else:
                return startai.split(
                    input,
                    num_or_size_splits=tuple(
                        [chunk_size + remainder] + [chunk_size] * (chunks - 1)
                    ),
                    axis=dim,
                )


@to_startai_arrays_and_back
def column_stack(tensors, *, out=None):
    reshaped_tensors = []
    for t in tensors:
        dim_num = startai.get_num_dims(t, as_array=False)
        if dim_num <= 1:
            reshaped_tensor = startai.reshape(t, (-1, 1))
        else:
            reshaped_tensor = t
        reshaped_tensors.append(reshaped_tensor)
    return startai.hstack(reshaped_tensors, out=out)


@to_startai_arrays_and_back
def concat(tensors, dim=0, *, out=None):
    return startai.concat(tensors, axis=dim, out=out)


@to_startai_arrays_and_back
def conj(input):
    return startai.conj(input)


# diagonal_scatter
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
def diagonal_scatter(input, src, offset=0, dim1=0, dim2=1):
    input = startai.copy_array(input)
    input_shape = input.shape
    indices = startai.arange(0, input.size)
    diagonal_indices = startai.diagonal(
        indices.reshape(input.shape), offset=offset, axis1=dim1, axis2=dim2
    )
    if src.shape != diagonal_indices.shape:
        raise startai.utils.exceptions.StartaiException(
            "src must have shape equal to specified diagonal of input. src size ="
            f" {src.shape}, diagonal size = {diagonal_indices.shape}"
        )
    input = input.reshape((-1,))
    input[diagonal_indices.reshape((-1,))] = src.reshape((-1,))
    input = input.reshape(input_shape)
    return input


@to_startai_arrays_and_back
def dsplit(input, indices_or_sections, /):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[input.shape[2]])
            .astype(startai.int8)
            .to_list()
        )
    return tuple(startai.dsplit(input, indices_or_sections))


@to_startai_arrays_and_back
def dstack(tensors, *, out=None):
    return startai.dstack(tensors, out=out)


@to_startai_arrays_and_back
def gather(input, dim, index, *, sparse_grad=False, out=None):
    if sparse_grad:
        raise startai.utils.exceptions.StartaiException(
            "Gather does not yet support the sparse grad functionality"
        )

    dim = dim % len(input.shape)
    all_indices = startai.argwhere(startai.full(index.shape, True))
    gather_locations = startai.reshape(index, [startai.prod(startai.array(index.shape))])

    gather_indices = []
    for axis in range(len(index.shape)):
        if axis == dim:
            gather_indices.append(startai.array(gather_locations, dtype=index.dtype))
        else:
            gather_indices.append(startai.array(all_indices[:, axis], dtype=index.dtype))

    gather_indices = startai.stack(gather_indices, axis=-1)
    gathered = startai.gather_nd(input, gather_indices)
    reshaped = startai.reshape(gathered, index.shape)
    return reshaped


@to_startai_arrays_and_back
def hsplit(input, indices_or_sections=None, /):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        if input.ndim == 1:
            indices_or_sections = (
                startai.diff(indices_or_sections, prepend=[0], append=[input.shape[0]])
                .astype(startai.int8)
                .to_list()
            )
        else:
            indices_or_sections = (
                startai.diff(indices_or_sections, prepend=[0], append=[input.shape[1]])
                .astype(startai.int8)
                .to_list()
            )
    return tuple(startai.hsplit(input, indices_or_sections))


@to_startai_arrays_and_back
def hstack(tensors, *, out=None):
    return startai.hstack(tensors, out=out)


@to_startai_arrays_and_back
def index_add(input, dim, index, source, *, alpha=1, out=None):
    input = startai.swapaxes(input, dim, 0)
    source = startai.swapaxes(source, dim, 0)
    _to_adds = []
    index = sorted(zip(startai.to_list(index), range(len(index))), key=(lambda x: x[0]))
    while index:
        _curr_idx = index[0][0]
        while len(_to_adds) < _curr_idx:
            _to_adds.append(startai.zeros_like(source[0]))
        _to_add_cum = startai.get_item(source, index[0][1])
        while (len(index) > 1) and (index[0][0] == index[1][0]):
            _to_add_cum = _to_add_cum + startai.get_item(source, index.pop(1)[1])
        index.pop(0)
        _to_adds.append(_to_add_cum)
    while len(_to_adds) < input.shape[0]:
        _to_adds.append(startai.zeros_like(source[0]))
    _to_adds = startai.stack(_to_adds)
    if len(input.shape) < 2:
        # Added this line due to the paddle backend treating scalars as 1-d arrays
        _to_adds = startai.flatten(_to_adds)

    ret = startai.add(input, _to_adds, alpha=alpha)
    ret = startai.swapaxes(ret, 0, dim, out=out)
    return ret


@to_startai_arrays_and_back
def index_copy(input, dim, index, source, *, out=None):
    input = startai.swapaxes(input, dim, 0)
    source = startai.swapaxes(source, dim, 0)
    index = sorted(zip(startai.to_list(index), range(len(index))), key=(lambda x: x[0]))
    res = []
    while index:
        _curr_idx = index[0][0]
        for i in range(len(res), _curr_idx):
            res.append(startai.get_item(input, i))
        while (len(index) > 1) and (index[0][0] == index[1][0]):
            index.pop(0)
        res.append(startai.get_item(source, index[0][1]))
        index.pop(0)
    for i in range(len(res), input.shape[0]):
        res.append(startai.get_item(input, i))
    res = startai.stack(res)
    if len(input.shape) < 2:
        res = startai.flatten(res)

    return startai.swapaxes(res, 0, dim, out=out)


@with_unsupported_dtypes(
    {
        "2.2 and below": (
            "uint16",
            "uint32",
            "uint64",
            "bfloat16",
            "complex128",
            "complex64",
        )
    },
    "torch",
)
@to_startai_arrays_and_back
def index_reduce(input, dim, index, source, reduce, *, include_self=True, out=None):
    result = startai.copy_array(input)
    counts = (
        startai.ones_like(result, dtype=result.dtype)
        if include_self
        else startai.zeros_like(result, dtype=result.dtype)
    )

    index = index.astype(startai.int64)

    def init_val(reduce):
        if reduce == "prod":
            return 1
        elif reduce == "amax":
            return -startai.inf
        elif reduce == "amin":
            return startai.inf
        else:
            return 0

    if not include_self:
        result[index, ...] = init_val(reduce)

    numel = index.size
    index_contig = startai.copy_array(index)

    def update_counts(reduce, counts, dim, input_index):
        if reduce == "mean":
            counts_slice = [slice(None)] * counts.ndim
            counts_slice[dim] = input_index
            counts[tuple(counts_slice)] += 1
        return counts

    def update_result(result, reduce, input_data, source_data):
        if reduce == "prod":
            return input_data * source_data
        elif reduce == "amin":
            return startai.minimum(input_data, source_data)
        elif reduce == "amax":
            return startai.maximum(input_data, source_data)
        else:
            return input_data + source_data

    if result.ndim > 1:
        for i in range(numel):
            input_index = index_contig[i]
            if not (0 <= input_index < result.shape[dim]):
                raise IndexError("Index out of range in self")

            input_data = startai.gather(result, [input_index], axis=dim)
            source_data = startai.gather(source, [i], axis=dim)

            result_slice = [slice(None)] * result.ndim
            result_slice[dim] = input_index

            update_data = update_result(result, reduce, input_data, source_data)
            slide_shape = result[tuple(result_slice)].shape
            result[tuple(result_slice)] = startai.reshape(update_data, slide_shape)

            counts = update_counts(reduce, counts, dim, input_index)

    elif result.ndim == 1:
        for i in range(numel):
            input_index = index_contig[i]
            if not (0 <= input_index < result.size):
                raise IndexError("Index out of range in self")

            input_data = startai.flatten(result)[input_index]
            source_data = startai.flatten(source)[i]

            result[input_index] = update_result(result, reduce, input_data, source_data)
            counts[input_index] += 1

    if reduce == "mean":
        if startai.any(counts == startai.array(0)):
            counts[counts == startai.array(0)] = startai.array(1)
        result /= counts

        if not input.is_float_dtype():
            result = startai.floor(result)
            result = result.astype(input.dtype)

    return result


@to_startai_arrays_and_back
def index_select(input, dim, index, *, out=None):
    return startai.gather(input, index, axis=dim, out=out)


@to_startai_arrays_and_back
def masked_select(input, mask, out=None):
    return startai.flatten(input[mask], out=out)


@to_startai_arrays_and_back
def moveaxis(input, source, destination):
    return startai.moveaxis(input, source, destination)


@to_startai_arrays_and_back
def movedim(input, source, destination):
    return startai.moveaxis(input, source, destination)


@to_startai_arrays_and_back
def narrow(input, dim, start, length):
    num_dims = startai.get_num_dims(input)
    slices = [slice(None)] * num_dims
    slices[dim] = slice(start, start + length)
    return input[tuple(slices)]


@to_startai_arrays_and_back
def nonzero(input, *, out=None, as_tuple=False):
    if as_tuple:
        return startai.nonzero(input, as_tuple=as_tuple)
    return startai.argwhere(input != 0, out=out)


@to_startai_arrays_and_back
def permute(input, dims):
    return startai.permute_dims(input, axes=dims, copy=False)


@to_startai_shape
@to_startai_arrays_and_back
def reshape(input, shape):
    return startai.reshape(input, shape)


@to_startai_arrays_and_back
def row_stack(tensors, *, out=None):
    return startai.vstack(tensors, out=out)


@to_startai_arrays_and_back
def select(input, dim, index):
    num_dims = startai.get_num_dims(input)
    slices = [slice(None)] * num_dims
    slices[dim] = index
    return input[tuple(slices)]


@to_startai_arrays_and_back
def split(tensor, split_size_or_sections, dim=0):
    if isinstance(split_size_or_sections, int):
        split_size = split_size_or_sections
        split_size_or_sections = [split_size] * (tensor.shape[dim] // split_size)
        if tensor.shape[dim] % split_size:
            split_size_or_sections.append(tensor.shape[dim] % split_size)
    return tuple(
        startai.split(
            tensor,
            num_or_size_splits=split_size_or_sections,
            axis=dim,
            with_remainder=True,
        )
    )


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def squeeze(input, dim=None):
    if isinstance(dim, int) and input.ndim > 0:
        if input.shape[dim] > 1:
            return input
    return startai.squeeze(input, axis=dim)


@numpy_to_torch_style_args
@to_startai_arrays_and_back
def stack(tensors, dim=0, *, out=None):
    return startai.stack(tensors, axis=dim, out=out)


@to_startai_arrays_and_back
def swapaxes(input, axis0, axis1):
    return startai.swapaxes(input, axis0, axis1)


@to_startai_arrays_and_back
def swapdims(input, dim0, dim1):
    return startai.swapaxes(input, dim0, dim1)


@to_startai_arrays_and_back
def t(input):
    if input.ndim > 2:
        raise startai.utils.exceptions.StartaiException(
            f"t(input) expects a tensor with <= 2 dimensions, but self is {input.ndim}D"
        )
    if input.ndim == 2:
        return startai.swapaxes(input, 0, 1)
    else:
        return input


@to_startai_arrays_and_back
def take(input, index):
    input = startai.reshape(input, (-1,))
    return startai.gather(input, index, axis=0)


@to_startai_arrays_and_back
def take_along_dim(input, indices, dim, *, out=None):
    return startai.take_along_axis(input, indices, dim, out=out)


@to_startai_arrays_and_back
def tensor_split(input, indices_or_sections, dim=0):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[input.shape[dim]])
            .astype(startai.int8)
            .to_list()
        )
    return startai.split(
        input, num_or_size_splits=indices_or_sections, axis=dim, with_remainder=True
    )


@to_startai_arrays_and_back
def tile(input, dims):
    try:
        tup = tuple(dims)
    except TypeError:
        tup = (dims,)
    d = len(tup)
    res = 0
    if len(input.shape) > len([dims]) - 1:
        res = input
    if d < input.ndim:
        tup = (1,) * (input.ndim - d) + tup
        res = startai.tile(input, tup)

    else:
        res = startai.tile(input, repeats=dims, out=None)
    return res


@to_startai_arrays_and_back
def transpose(input, dim0, dim1):
    return startai.swapaxes(input, dim0, dim1)


@to_startai_arrays_and_back
def unbind(input, dim=0):
    shape = list(input.shape)
    shape.pop(dim)
    return tuple([x.reshape(tuple(shape)) for x in split(input, 1, dim=dim)])


@to_startai_arrays_and_back
def unsqueeze(input, dim=0):
    return startai.expand_dims(input, axis=dim)


@to_startai_arrays_and_back
def vsplit(input, indices_or_sections=None, /):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[input.shape[0]])
            .astype(startai.int8)
            .to_list()
        )
    return tuple(startai.vsplit(input, indices_or_sections))


@to_startai_arrays_and_back
def vstack(tensors, *, out=None):
    return startai.vstack(tensors, out=out)


@to_startai_arrays_and_back
def where(condition, input=None, other=None):
    if not startai.exists(input) and not startai.exists(other):
        return nonzero(condition, as_tuple=True)
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.where(condition, input, other)
