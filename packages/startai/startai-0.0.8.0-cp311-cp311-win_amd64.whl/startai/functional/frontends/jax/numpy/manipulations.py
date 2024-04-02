# local
import startai
from startai.functional.frontends.jax.func_wrapper import (
    to_startai_arrays_and_back,
    handle_jax_dtype,
)
from startai.functional.frontends.jax.numpy import promote_types_of_jax_inputs


@to_startai_arrays_and_back
def append(arr, values, axis=None):
    if axis is None:
        return startai.concat((startai.flatten(arr), startai.flatten(values)), axis=0)
    else:
        return startai.concat((arr, values), axis=axis)


@to_startai_arrays_and_back
def array_split(ary, indices_or_sections, axis=0):
    return startai.split(
        ary, num_or_size_splits=indices_or_sections, axis=axis, with_remainder=True
    )


@to_startai_arrays_and_back
def atleast_1d(*arys):
    return startai.atleast_1d(*arys)


@to_startai_arrays_and_back
def atleast_2d(*arys):
    return startai.atleast_2d(*arys)


@to_startai_arrays_and_back
def atleast_3d(*arys):
    return startai.atleast_3d(*arys)


@to_startai_arrays_and_back
def bartlett(M):
    if M < 1:
        return startai.array([])
    if M == 1:
        return startai.ones(M, dtype=startai.float64)
    res = startai.arange(0, M)
    res = startai.where(
        startai.less_equal(res, (M - 1) / 2.0),
        2.0 * res / (M - 1),
        2.0 - 2.0 * res / (M - 1),
    )
    return res


@to_startai_arrays_and_back
def blackman(M):
    if M < 1:
        return startai.array([])
    if M == 1:
        return startai.ones((1,))
    n = startai.arange(0, M)
    alpha = 0.16
    a0 = (1 - alpha) / 2
    a1 = 1 / 2
    a2 = alpha / 2
    ret = (
        a0
        - a1 * startai.cos(2 * startai.pi * n / (M - 1))
        + a2 * startai.cos(4 * startai.pi * n / (M - 1))
    )
    return ret


@to_startai_arrays_and_back
def block(arr):
    # TODO: reimplement block
    raise startai.utils.exceptions.StartaiNotImplementedError()


@to_startai_arrays_and_back
def broadcast_arrays(*args):
    return startai.broadcast_arrays(*args)


@to_startai_arrays_and_back
def broadcast_shapes(*shapes):
    return startai.broadcast_shapes(*shapes)


@to_startai_arrays_and_back
def broadcast_to(array, shape):
    return startai.broadcast_to(array, shape)


@to_startai_arrays_and_back
def clip(a, a_min=None, a_max=None, out=None):
    startai.utils.assertions.check_all_or_any_fn(
        a_min,
        a_max,
        fn=startai.exists,
        type="any",
        limit=[1, 2],
        message="at most one of a_min or a_max can be None",
    )
    a = startai.array(a)
    if a_min is None:
        a, a_max = promote_types_of_jax_inputs(a, a_max)
        return startai.minimum(a, a_max, out=out)
    if a_max is None:
        a, a_min = promote_types_of_jax_inputs(a, a_min)
        return startai.maximum(a, a_min, out=out)
    return startai.clip(a, a_min, a_max, out=out)


@to_startai_arrays_and_back
def column_stack(tup):
    if len(startai.shape(tup[0])) == 1:
        ys = []
        for t in tup:
            ys += [startai.reshape(t, (startai.shape(t)[0], 1))]
        return startai.concat(ys, axis=1)
    return startai.concat(tup, axis=1)


@handle_jax_dtype
@to_startai_arrays_and_back
def concatenate(arrays, axis=0, dtype=None):
    ret = startai.concat(arrays, axis=axis)
    if dtype:
        ret = startai.array(ret, dtype=dtype)
    return ret


@to_startai_arrays_and_back
def diagflat(v, k=0):
    ret = startai.diagflat(v, offset=k)
    while len(startai.shape(ret)) < 2:
        ret = ret.expand_dims(axis=0)
    return ret


@to_startai_arrays_and_back
def dsplit(ary, indices_or_sections):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[2]])
            .astype(startai.int8)
            .to_list()
        )
    return startai.dsplit(ary, indices_or_sections)


@to_startai_arrays_and_back
def dstack(tup, dtype=None):
    return startai.dstack(tup)


@to_startai_arrays_and_back
def expand_dims(a, axis):
    return startai.expand_dims(a, axis=axis)


@to_startai_arrays_and_back
def flip(m, axis=None):
    return startai.flip(m, axis=axis)


@to_startai_arrays_and_back
def fliplr(m):
    return startai.fliplr(m)


@to_startai_arrays_and_back
def flipud(m):
    return startai.flipud(m, out=None)


def hamming(M):
    if M <= 1:
        return startai.ones([M], dtype=startai.float64)
    n = startai.arange(M)
    ret = 0.54 - 0.46 * startai.cos(2.0 * startai.pi * n / (M - 1))
    return ret


@to_startai_arrays_and_back
def hanning(M):
    if M <= 1:
        return startai.ones([M], dtype=startai.float64)
    n = startai.arange(M)
    ret = 0.5 * (1 - startai.cos(2.0 * startai.pi * n / (M - 1)))
    return ret


@to_startai_arrays_and_back
def hsplit(ary, indices_or_sections):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        if ary.ndim == 1:
            indices_or_sections = (
                startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[0]])
                .astype(startai.int8)
                .to_list()
            )
        else:
            indices_or_sections = (
                startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[1]])
                .astype(startai.int8)
                .to_list()
            )
    return startai.hsplit(ary, indices_or_sections)


@to_startai_arrays_and_back
def kaiser(M, beta):
    if M <= 1:
        return startai.ones([M], dtype=startai.float64)
    n = startai.arange(M)
    alpha = 0.5 * (M - 1)
    ret = startai.i0(beta * startai.sqrt(1 - ((n - alpha) / alpha) ** 2)) / startai.i0(beta)
    return ret


@to_startai_arrays_and_back
def moveaxis(a, source, destination):
    return startai.moveaxis(a, source, destination)


@to_startai_arrays_and_back
def pad(array, pad_width, mode="constant", **kwargs):
    return startai.pad(array, pad_width, mode=mode, **kwargs)


@to_startai_arrays_and_back
def ravel(a, order="C"):
    return startai.reshape(a, shape=(-1,), order=order)


@to_startai_arrays_and_back
def repeat(a, repeats, axis=None, *, total_repeat_length=None):
    return startai.repeat(a, repeats, axis=axis)


@to_startai_arrays_and_back
def reshape(a, newshape, order="C"):
    return startai.reshape(a, shape=newshape, order=order)


@to_startai_arrays_and_back
def resize(a, new_shape):
    a = startai.array(a)
    resized_a = startai.reshape(a, new_shape)
    return resized_a


@to_startai_arrays_and_back
def roll(a, shift, axis=None):
    return startai.roll(a, shift, axis=axis)


@to_startai_arrays_and_back
def rot90(m, k=1, axes=(0, 1)):
    return startai.rot90(m, k=k, axes=axes)


@to_startai_arrays_and_back
def row_stack(tup):
    if len(startai.shape(tup[0])) == 1:
        xs = []
        for t in tup:
            xs += [startai.reshape(t, (1, startai.shape(t)[0]))]
        return startai.concat(xs, axis=0)
    return startai.concat(tup, axis=0)


@to_startai_arrays_and_back
def split(ary, indices_or_sections, axis=0):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[axis]])
            .astype(startai.int8)
            .to_list()
        )
    return startai.split(
        ary, num_or_size_splits=indices_or_sections, axis=axis, with_remainder=False
    )


@to_startai_arrays_and_back
def squeeze(a, axis=None):
    return startai.squeeze(a, axis=axis)


@to_startai_arrays_and_back
def stack(arrays, axis=0, out=None, dtype=None):
    if dtype:
        return startai.astype(
            startai.stack(arrays, axis=axis, out=out), startai.as_startai_dtype(dtype)
        )
    return startai.stack(arrays, axis=axis, out=out)


@to_startai_arrays_and_back
def swapaxes(a, axis1, axis2):
    return startai.swapaxes(a, axis1, axis2)


@to_startai_arrays_and_back
def take(
    a,
    indices,
    axis=None,
    out=None,
    mode=None,
    unique_indices=False,
    indices_are_sorted=False,
    fill_value=None,
):
    return startai.gather(a, indices, axis=axis, out=out)


@to_startai_arrays_and_back
def tile(A, reps):
    return startai.tile(A, reps)


@to_startai_arrays_and_back
def transpose(a, axes=None):
    if startai.isscalar(a):
        return startai.array(a)
    elif a.ndim == 1:
        return a
    if not axes:
        axes = list(range(len(a.shape)))[::-1]
    if isinstance(axes, int):
        axes = [axes]
    if (len(a.shape) == 0 and not axes) or (len(a.shape) == 1 and axes[0] == 0):
        return a
    return startai.permute_dims(a, axes, out=None)


@handle_jax_dtype
@to_startai_arrays_and_back
def tri(N, M=None, k=0, dtype="float64"):
    if M is None:
        M = N
    ones = startai.ones((N, M), dtype=dtype)
    return startai.tril(ones, k=k)


@to_startai_arrays_and_back
def tril(m, k=0):
    return startai.tril(m, k=k)


@to_startai_arrays_and_back
def trim_zeros(flit, trim="fb"):
    start_index = 0
    end_index = startai.shape(flit)[0]
    trim = trim.lower()
    if "f" in trim:
        for item in flit:
            if item == 0:
                start_index += 1
            else:
                break
    if "b" in trim:
        for item in flit[::-1]:
            if item == 0:
                end_index -= 1
            else:
                break
    return flit[start_index:end_index]


@to_startai_arrays_and_back
def vsplit(ary, indices_or_sections):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[0]])
            .astype(startai.int8)
            .to_list()
        )
    return startai.vsplit(ary, indices_or_sections)
