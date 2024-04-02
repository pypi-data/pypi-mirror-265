# local
import startai
from startai.functional.frontends.jax.func_wrapper import (
    to_startai_arrays_and_back,
)
from startai.functional.frontends.jax.numpy import (
    promote_types_of_jax_inputs as promote_jax_arrays,
)
from startai.utils.exceptions import StartaiNotImplementedException
from startai.func_wrapper import with_unsupported_dtypes


# --- Helpers --- #
# --------------- #


def _packbits_nested_list_padding(arr, pad_length):
    if arr.ndim > 1:
        nested_list = []
        for sub_arr in arr:
            nested_list.append(_packbits_nested_list_padding(sub_arr, pad_length))
        return nested_list
    else:
        return arr.zero_pad(pad_width=[[0, pad_length]])


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def all(a, axis=None, out=None, keepdims=False, *, where=False):
    return startai.all(a, axis=axis, keepdims=keepdims, out=out)


@to_startai_arrays_and_back
def allclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
    a, b = promote_jax_arrays(a, b)
    return startai.allclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)


@to_startai_arrays_and_back
def any(a, axis=None, out=None, keepdims=False, *, where=None):
    # TODO: Out not supported
    ret = startai.any(a, axis=axis, keepdims=keepdims)
    if startai.is_array(where):
        where = startai.array(where, dtype=startai.bool)
        ret = startai.where(where, ret, startai.default(None, startai.zeros_like(ret)))
    return ret


@to_startai_arrays_and_back
def array_equal(a1, a2, equal_nan: bool) -> bool:
    a1, a2 = promote_jax_arrays(a1, a2)
    if startai.shape(a1) != startai.shape(a2):
        return False
    eq = startai.asarray(a1 == a2)
    if equal_nan:
        eq = startai.logical_or(eq, startai.logical_and(startai.isnan(a1), startai.isnan(a2)))
    return startai.all(eq)


@to_startai_arrays_and_back
def array_equiv(a1, a2) -> bool:
    a1, a2 = promote_jax_arrays(a1, a2)
    try:
        eq = startai.equal(a1, a2)
    except ValueError:
        # shapes are not broadcastable
        return False
    return startai.all(eq)


@to_startai_arrays_and_back
def bitwise_and(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.bitwise_and(x1, x2)


@to_startai_arrays_and_back
def bitwise_not(x, /):
    return startai.bitwise_invert(x)


@to_startai_arrays_and_back
def bitwise_or(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.bitwise_or(x1, x2)


@to_startai_arrays_and_back
def bitwise_xor(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.bitwise_xor(x1, x2)


@to_startai_arrays_and_back
def equal(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.equal(x1, x2)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"0.4.24 and below": ("bfloat16",)}, "jax")
def fromfunction(function, shape, *, dtype=float, **kwargs):
    def canonicalize_shape(shape, context="shape argument"):
        if isinstance(shape, int):
            return (shape,)
        elif isinstance(shape, list):
            return tuple(shape)
        elif isinstance(shape, tuple):
            return shape
        else:
            msg = f"{context} must be an int, list, or tuple, but got {type(shape)}."
            raise TypeError(msg)

    arr = startai.zeros(shape, dtype=dtype)
    shape = canonicalize_shape(shape)
    # Iterate over the indices of the array
    for indices in startai.ndindex(shape):
        f_indices = indices
        startai.set_nest_at_index(
            arr, f_indices, startai.asarray(function(*indices, **kwargs), dtype=dtype)
        )
    return arr


@to_startai_arrays_and_back
def greater(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.greater(x1, x2)


@to_startai_arrays_and_back
def greater_equal(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.greater_equal(x1, x2)


@to_startai_arrays_and_back
def invert(x, /):
    return startai.bitwise_invert(x)


@to_startai_arrays_and_back
def isclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
    a, b = promote_jax_arrays(a, b)
    return startai.isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)


@to_startai_arrays_and_back
def iscomplex(x: any):
    return startai.bitwise_invert(startai.isreal(x))


@to_startai_arrays_and_back
def iscomplexobj(x):
    return startai.is_complex_dtype(startai.dtype(x))


@to_startai_arrays_and_back
def isfinite(x, /):
    return startai.isfinite(x)


@to_startai_arrays_and_back
def isin(element, test_elements, assume_unique=False, invert=False):
    return startai.isin(element, test_elements, assume_unique=assume_unique, invert=invert)


@to_startai_arrays_and_back
def isinf(x, /):
    return startai.isinf(x)


@to_startai_arrays_and_back
def isnan(x, /):
    return startai.isnan(x)


@to_startai_arrays_and_back
def isneginf(x, /, out=None):
    return startai.isinf(x, detect_positive=False, out=out)


@to_startai_arrays_and_back
def isposinf(x, /, out=None):
    return startai.isinf(x, detect_negative=False, out=out)


@to_startai_arrays_and_back
def isreal(x, out=None):
    return startai.isreal(x, out=out)


@to_startai_arrays_and_back
def isrealobj(x: any):
    return not startai.is_complex_dtype(startai.dtype(x))


@to_startai_arrays_and_back
def isscalar(x, /):
    return startai.isscalar(x)


@to_startai_arrays_and_back
def left_shift(x1, x2):
    # TODO: implement
    raise StartaiNotImplementedException()


@to_startai_arrays_and_back
def less(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.less(x1, x2)


@to_startai_arrays_and_back
def less_equal(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.less_equal(x1, x2)


@to_startai_arrays_and_back
# known issue in jnp's documentation of arguments
# https://github.com/google/jax/issues/9119
def logical_and(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    if x1.dtype == "complex128" or x2.dtype == "complex128":
        x1 = startai.astype(x1, startai.complex128)
        x2 = startai.astype(x2, startai.complex128)
    else:
        x1, x2 = promote_jax_arrays(x1, x2)
    return startai.logical_and(x1, x2)


@to_startai_arrays_and_back
def logical_not(x, /):
    return startai.logical_not(x)


@to_startai_arrays_and_back
def logical_or(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.logical_or(x1, x2)


@to_startai_arrays_and_back
def logical_xor(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.logical_xor(x1, x2)


@to_startai_arrays_and_back
def not_equal(x1, x2, /):
    x1, x2 = promote_jax_arrays(x1, x2)
    return startai.not_equal(x1, x2)


@to_startai_arrays_and_back
def packbits(x, /, *, axis=None, bitorder="big"):
    x = startai.greater(x, startai.zeros_like(x)).astype("uint8")
    bits = startai.arange(8, dtype="uint8")
    if bitorder == "big":
        bits = bits[::-1]
    if axis is None:
        x = startai.flatten(x)
        axis = 0
    x = startai.swapaxes(x, axis, -1)

    remainder = x.shape[-1] % 8
    if remainder:
        x = _packbits_nested_list_padding(x, 8 - remainder)
        x = startai.array(x)

    x = startai.reshape(x, list(x.shape[:-1]) + [x.shape[-1] // 8, 8])
    bits = startai.expand_dims(bits, axis=tuple(range(x.ndim - 1)))
    packed = (x << bits).sum(axis=-1).astype("uint8")
    return startai.swapaxes(packed, axis, -1)


@to_startai_arrays_and_back
def right_shift(x1, x2, /):
    return startai.bitwise_right_shift(x1, x2)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"0.4.24 and below": ("bfloat16", "bool")}, "jax")
def setxor1d(ar1, ar2, assume_unique=False):
    common_dtype = startai.promote_types(startai.dtype(ar1), startai.dtype(ar2))
    ar1 = startai.asarray(ar1, dtype=common_dtype)
    ar2 = startai.asarray(ar2, dtype=common_dtype)
    if not assume_unique:
        ar1 = startai.unique_values(ar1)
        ar2 = startai.unique_values(ar2)
    ar1 = startai.reshape(ar1, (-1,))
    ar2 = startai.reshape(ar2, (-1,))
    aux = startai.concat([ar1, ar2], axis=0)
    if aux.size == 0:
        return aux
    aux = startai.sort(aux)
    flag = startai.concat(
        (startai.array([True]), startai.not_equal(aux[1:], aux[:-1]), startai.array([True])), axis=0
    )
    mask = flag[1:] & flag[:-1]
    if startai.all(startai.logical_not(mask)):
        ret = startai.asarray([], dtype=common_dtype)
    else:
        ret = aux[mask]
    return ret


alltrue = all
sometrue = any
