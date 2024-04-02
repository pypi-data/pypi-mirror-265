# global
import startai
from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from startai.functional.frontends.paddle import promote_types_of_paddle_inputs
from startai.functional.frontends.paddle.func_wrapper import (
    to_startai_arrays_and_back,
)


@with_supported_dtypes({"2.4.1 and above": ("int64",)}, "paddle")
@to_startai_arrays_and_back
def bincount(x, weights=None, minlength=0, name=None):
    return startai.bincount(x, weights=weights, minlength=minlength)


# bmm
@with_unsupported_dtypes({"2.6.0 and below": ("float16", "bfloat16")}, "paddle")
@to_startai_arrays_and_back
def bmm(x, y, transpose_x=False, transpose_y=False, name=None):
    if len(startai.shape(x)) != 3 or len(startai.shape(y)) != 3:
        raise RuntimeError("input must be 3D matrices")
    x, y = promote_types_of_paddle_inputs(x, y)
    return startai.matmul(x, y, transpose_a=transpose_x, transpose_b=transpose_y)


# cholesky
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def cholesky(x, /, *, upper=False, name=None):
    return startai.cholesky(x, upper=upper)


# cholesky_solve
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def cholesky_solve(x, y, /, *, upper=False, name=None):
    if upper:
        y = startai.matrix_transpose(y)
    Y = startai.solve(y, x)
    return startai.solve(startai.matrix_transpose(y), Y)


# cond
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def cond(x, p=None, name=None):
    ret = startai.cond(x, p=p, out=name)
    if ret.shape == ():
        ret = ret.reshape((1,))
    return ret


@with_supported_dtypes(
    {"2.6.0 and below": ("float32", "float64", "int32", "int64")}, "paddle"
)
@to_startai_arrays_and_back
def cross(x, y, /, *, axis=9, name=None):
    x, y = promote_types_of_paddle_inputs(x, y)
    return startai.cross(x, y, axis=axis)


# diagonal
@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "int32",
            "int64",
            "float64",
            "complex128",
            "float32",
            "complex64",
            "bool",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def diagonal(x, offset=0, axis1=0, axis2=1, name=None):
    return startai.diagonal(x, offset=offset, axis1=axis1, axis2=axis2)


@with_supported_dtypes({"2.4.1 and above": ("float64", "float32")}, "paddle")
@to_startai_arrays_and_back
def dist(x, y, p=2):
    ret = startai.vector_norm(startai.subtract(x, y), ord=p)
    return startai.reshape(ret, (1,))


# dot
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def dot(x, y, name=None):
    x, y = promote_types_of_paddle_inputs(x, y)
    out = startai.multiply(x, y)
    return startai.sum(out, axis=startai.get_num_dims(x) - 1, keepdims=False)


# eig
@to_startai_arrays_and_back
def eig(x, name=None):
    return startai.eig(x)


# eigh
@to_startai_arrays_and_back
def eigh(x, UPLO="L", name=None):
    return startai.eigh(x, UPLO=UPLO)


# eigvals
@to_startai_arrays_and_back
def eigvals(x, name=None):
    return startai.eigvals(x)


# eigvalsh
@to_startai_arrays_and_back
def eigvalsh(x, UPLO="L", name=None):
    return startai.eigvalsh(x, UPLO=UPLO)


@to_startai_arrays_and_back
def lu_unpack(lu_data, lu_pivots, unpack_datas=True, unpack_pivots=True, *, out=None):
    A = lu_data
    n = A.shape
    m = len(lu_pivots)
    pivot_matrix = startai.eye(m)
    L = startai.tril(A)
    L.fill_diagonal(1.000)
    U = startai.triu(A)
    for i in range(m):
        if i != lu_pivots[i] - 1:
            pivot_matrix[[i, lu_pivots[i] - 1]] = pivot_matrix[[lu_pivots[i] - 1, i]]
        P = pivot_matrix
    if not unpack_datas:
        L = startai.zeros(n)
        U = startai.zeros(n)
        if not unpack_pivots:
            P = startai.zeros(n)
        else:
            P = pivot_matrix
        result = f"P={P}\n" + f"L={L}\n" + f"U={U}"
        return result
    elif not unpack_pivots:
        P = startai.zeros(n)
        result = f"P={P}\n" + f"L={L}\n" + f"U={U}"
        return result
    else:
        result = f"P={P}\n" + f"L={L}\n" + f"U={U}"
        return result


# matmul
@with_unsupported_dtypes({"2.6.0 and below": ("float16", "bfloat16")}, "paddle")
@to_startai_arrays_and_back
def matmul(x, y, transpose_x=False, transpose_y=False, name=None):
    x, y = promote_types_of_paddle_inputs(x, y)
    return startai.matmul(x, y, transpose_a=transpose_x, transpose_b=transpose_y)


# matrix_power
@with_unsupported_dtypes({"2.6.0 and below": ("float16", "bfloat16")}, "paddle")
@to_startai_arrays_and_back
def matrix_power(x, n, name=None):
    return startai.matrix_power(x, n)


# mv
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def mv(x, vec, name=None):
    return startai.dot(x, vec)


# norm
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def norm(x, p="fro", axis=None, keepdim=False, name=None):
    if axis is None and p is not None:
        if p == "fro":
            p = 2
        ret = startai.vector_norm(x.flatten(), ord=p, axis=-1)
        if keepdim:
            ret = ret.reshape([1] * len(x.shape))
        return ret

    if isinstance(axis, tuple):
        axis = list(axis)
    if isinstance(axis, list) and len(axis) == 1:
        axis = axis[0]

    if isinstance(axis, int):
        if p == "fro":
            p = 2
        if p in [0, 1, 2, startai.inf, -startai.inf]:
            ret = startai.vector_norm(x, ord=p, axis=axis, keepdims=keepdim)
        elif isinstance(p, (int, float)):
            ret = startai.pow(
                startai.sum(startai.pow(startai.abs(x), p), axis=axis, keepdims=keepdim),
                float(1.0 / p),
            )

    elif isinstance(axis, list) and len(axis) == 2:
        if p == 0:
            raise ValueError
        elif p == 1:
            ret = startai.sum(startai.abs(x), axis=axis, keepdims=keepdim)
        elif p in [2, "fro"]:
            ret = startai.matrix_norm(x, ord="fro", axis=axis, keepdims=keepdim)
        elif p == startai.inf:
            ret = startai.max(startai.abs(x), axis=axis, keepdims=keepdim)
        elif p == -startai.inf:
            ret = startai.min(startai.abs(x), axis=axis, keepdims=keepdim)
        elif isinstance(p, (int, float)) and p > 0:
            ret = startai.pow(
                startai.sum(startai.pow(startai.abs(x), p), axis=axis, keepdims=keepdim),
                float(1.0 / p),
            )
        else:
            raise ValueError

    else:
        raise ValueError

    return ret


# pinv
@with_unsupported_dtypes({"2.6.0 and below": ("float16", "bfloat16")}, "paddle")
@to_startai_arrays_and_back
def pinv(x, rcond=1e-15, hermitian=False, name=None):
    # TODO: Add hermitian functionality
    return startai.pinv(x, rtol=rcond)


# qr
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def qr(x, mode="reduced", name=None):
    return startai.qr(x, mode=mode)


# solve
@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def solve(x, y, name=None):
    return startai.solve(x, y)


# transpose
@with_unsupported_dtypes({"2.6.0 and below": ("uint8", "int8", "int16")}, "paddle")
@to_startai_arrays_and_back
def transpose(x, perm, name=None):
    return startai.permute_dims(x, axes=perm)
