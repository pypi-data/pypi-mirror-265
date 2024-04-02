# global
import startai

from startai.functional.frontends.numpy import promote_types_of_numpy_inputs
from startai import with_unsupported_dtypes
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    handle_numpy_casting,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
    handle_numpy_out,
)


# --- Helpers --- #
# --------------- #


@handle_numpy_out
@handle_numpy_dtype
@to_startai_arrays_and_back
@handle_numpy_casting
@from_zero_dim_arrays_to_scalar
def _matmul(
    x1, x2, /, out=None, *, casting="same_kind", order="K", dtype=None, subok=True
):
    return startai.matmul(x1, x2, out=out)


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def cross(a, b, *, axisa=-1, axisb=-1, axisc=-1, axis=None):
    return startai.cross(a, b, axisa=axisa, axisb=axisb, axisc=axisc, axis=axis)


@handle_numpy_out
@to_startai_arrays_and_back
def dot(a, b, out=None):
    a, b = promote_types_of_numpy_inputs(a, b)
    return startai.matmul(a, b, out=out)


@handle_numpy_out
@to_startai_arrays_and_back
def einsum(
    subscripts,
    *operands,
    out=None,
    dtype=None,
    order="K",
    casting="safe",
    optimize=False,
):
    return startai.einsum(subscripts, *operands, out=out)


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def inner(a, b, /):
    a, b = promote_types_of_numpy_inputs(a, b)
    return startai.inner(a, b)


@to_startai_arrays_and_back
def kron(a, b):
    a, b = promote_types_of_numpy_inputs(a, b)
    return startai.kron(a, b)


@to_startai_arrays_and_back
def matrix_power(a, n):
    return startai.matrix_power(a, n)


@with_unsupported_dtypes({"2.0.0 and below": ("float16",)}, "torch")
@handle_numpy_out
@to_startai_arrays_and_back
def multi_dot(arrays, *, out=None):
    return startai.multi_dot(arrays, out=out)


@handle_numpy_out
@to_startai_arrays_and_back
def outer(a, b, out=None):
    a, b = promote_types_of_numpy_inputs(a, b)
    return startai.outer(a, b, out=out)


@to_startai_arrays_and_back
def tensordot(a, b, axes=2):
    return startai.tensordot(a, b, axes=axes)


@to_startai_arrays_and_back
def tensorsolve(a, b, axes=2):
    return startai.tensorsolve(a, b, axes=axes)
