# local
import math
import startai
import startai.functional.frontends.torch as torch_frontend
from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back
from startai.func_wrapper import with_supported_dtypes, with_unsupported_dtypes
from collections import namedtuple


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def cholesky(input, *, upper=False, out=None):
    return startai.cholesky(input, upper=upper, out=out)


@to_startai_arrays_and_back
def cholesky_ex(input, *, upper=False, check_errors=False, out=None):
    try:
        matrix = startai.cholesky(input, upper=upper, out=out)
        info = startai.zeros(input.shape[:-2], dtype=startai.int32)
        return matrix, info
    except RuntimeError as e:
        if check_errors:
            raise RuntimeError(e) from e
        else:
            matrix = input * math.nan
            info = startai.ones(input.shape[:-2], dtype=startai.int32)
            return matrix, info


@to_startai_arrays_and_back
@with_supported_dtypes({"2.2 and below": ("float32", "float64", "complex")}, "torch")
def cond(input, p=None, *, out=None):
    return startai.cond(input, p=p, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def cross(input, other, *, dim=None, out=None):
    return torch_frontend.miscellaneous_ops.cross(input, other, dim=dim, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def det(A, *, out=None):
    return startai.det(A, out=out)


@to_startai_arrays_and_back
def diagonal(A, *, offset=0, dim1=-2, dim2=-1):
    return torch_frontend.diagonal(A, offset=offset, dim1=dim1, dim2=dim2)


@to_startai_arrays_and_back
def divide(input, other, *, rounding_mode=None, out=None):
    return startai.divide(input, other, out=out)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("bfloat16", "float16")}, "torch")
def eig(input, *, out=None):
    return startai.eig(input, out=out)


@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64", "complex128")},
    "torch",
)
def eigh(A, UPLO="L", *, out=None):
    return startai.eigh(A, UPLO=UPLO, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def eigvals(input, *, out=None):
    ret = startai.eigvals(input)
    if startai.exists(out):
        return startai.inplace_update(out, ret)
    return ret


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def eigvalsh(input, UPLO="L", *, out=None):
    ret = startai.eigvalsh(input, UPLO=UPLO, out=out)
    if "complex64" in startai.as_startai_dtype(ret.dtype):
        ret = startai.astype(ret, startai.float32)
    elif "complex128" in startai.as_startai_dtype(ret.dtype):
        ret = startai.astype(ret, startai.float64)
    return ret


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def inv(A, *, out=None):
    return startai.inv(A, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def inv_ex(A, *, check_errors=False, out=None):
    if startai.any(startai.det(A) == 0):
        if check_errors:
            raise RuntimeError("Singular Matrix")
        else:
            inv = A * math.nan
            # TODO: info should return an array containing the diagonal element of the
            # LU decomposition of the input matrix that is exactly zero
            info = startai.ones(A.shape[:-2], dtype=startai.int32)
    else:
        inv = startai.inv(A, out=out)
        info = startai.zeros(A.shape[:-2], dtype=startai.int32)
    return inv, info


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def lu_factor(A, *, pivot=True, out=None):
    return startai.lu_factor(A, pivot=pivot, out=out)


@to_startai_arrays_and_back
def lu_factor_ex(A, *, pivot=True, check_errors=False, out=None):
    try:
        LU = startai.lu_factor(A, pivot=pivot, out=out)
        info = startai.zeros(A.shape[:-2], dtype=startai.int32)
        return LU, info
    except RuntimeError as e:
        if check_errors:
            raise RuntimeError(e) from e
        else:
            matrix = A * math.nan
            info = startai.ones(A.shape[:-2], dtype=startai.int32)
            return matrix, info


def lu_solve(LU, pivots, B, *, left=True, adjoint=False, out=None):
    return startai.lu_solve(LU, pivots, B, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def matmul(input, other, *, out=None):
    return startai.matmul(input, other, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.2 and below": ("float32", "float64", "complex")}, "torch")
def matrix_exp(A):
    return startai.matrix_exp(A)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def matrix_norm(input, ord="fro", dim=(-2, -1), keepdim=False, *, dtype=None, out=None):
    return startai.matrix_norm(
        input, ord=ord, axis=dim, keepdims=keepdim, dtype=dtype, out=out
    )


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def matrix_power(A, n, *, out=None):
    return startai.matrix_power(A, n, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def matrix_rank(input, *, atol=None, rtol=None, hermitian=False, out=None):
    return startai.matrix_rank(input, atol=atol, rtol=rtol, hermitian=hermitian, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def multi_dot(tensors, *, out=None):
    return startai.multi_dot(tensors, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex64", "complex128")}, "torch"
)
def norm(input, ord=None, dim=None, keepdim=False, *, dtype=None, out=None):
    if dim is None and (ord is not None):
        if input.ndim == 1:
            ret = startai.vector_norm(input, axis=dim, keepdims=keepdim, ord=ord)
        else:
            ret = startai.matrix_norm(input, keepdims=keepdim, ord=ord)
    elif dim is None and ord is None:
        input = startai.flatten(input)
        ret = startai.vector_norm(input, axis=0, keepdims=keepdim, ord=2)
    elif isinstance(dim, int):
        ret = startai.vector_norm(input, axis=dim, keepdims=keepdim, ord=ord)
    elif isinstance(dim, tuple) and len(dim) <= 2:
        ret = startai.matrix_norm(input, axis=dim, keepdims=keepdim, ord=ord)
    elif isinstance(dim, tuple) and len(dim) > 2:
        raise RuntimeError(
            f"linalg.norm: If dim is specified, it must be of length 1 or 2. Got {dim}"
        )
    return ret


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def pinv(input, *, atol=None, rtol=None, hermitian=False, out=None):
    # TODO: add handling for hermitian
    if atol is None:
        return startai.pinv(input, rtol=rtol, out=out)
    else:
        sigma = startai.svdvals(input)[0]
        if rtol is None:
            rtol = atol / sigma
        else:
            if atol > rtol * sigma:
                rtol = atol / sigma

    return startai.pinv(input, rtol=rtol, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def qr(A, mode="reduced", *, out=None):
    if mode == "reduced":
        ret = startai.qr(A, mode="reduced")
    elif mode == "r":
        Q, R = startai.qr(A, mode="r")
        Q = []
        ret = Q, R
    elif mode == "complete":
        ret = startai.qr(A, mode="complete")
    if startai.exists(out):
        return startai.inplace_update(out, ret)
    return ret


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def slogdet(A, *, out=None):
    sign, logabsdet = startai.slogdet(A)
    if "complex64" in startai.as_startai_dtype(logabsdet.dtype):
        logabsdet = startai.astype(logabsdet, startai.float32)
    if "complex128" in startai.as_startai_dtype(logabsdet.dtype):
        logabsdet = startai.astype(logabsdet, startai.float64)
    ret = namedtuple("slogdet", ["sign", "logabsdet"])(sign, logabsdet)
    if startai.exists(out):
        return startai.inplace_update(out, ret, keep_input_dtype=True)
    return ret


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def solve(A, B, *, left=True, out=None):
    if left:
        return startai.solve(A, B, out=out)

    A_t = startai.linalg.matrix_transpose(A)
    B_t = startai.linalg.matrix_transpose(B if B.ndim > 1 else startai.reshape(B, (-1, 1)))
    X_t = startai.solve(A_t, B_t)
    return startai.linalg.matrix_transpose(X_t, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def solve_ex(A, B, *, left=True, check_errors=False, out=None):
    try:
        if left:
            result = startai.solve(A, B, out=out)
        else:
            A_t = startai.linalg.matrix_transpose(A)
            B_t = startai.linalg.matrix_transpose(
                B if B.ndim > 1 else startai.reshape(B, (-1, 1))
            )
            X_t = startai.solve(A_t, B_t)
            result = startai.linalg.matrix_transpose(X_t, out=out)

        info = startai.zeros(A.shape[:-2], dtype=startai.int32)
        return result, info
    except RuntimeError as e:
        if check_errors:
            raise RuntimeError(e) from e
        else:
            result = A * math.nan
            info = startai.ones(A.shape[:-2], dtype=startai.int32)

            return result, info


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def svd(A, /, *, full_matrices=True, driver=None, out=None):
    # TODO: add handling for driver and out
    return startai.svd(A, compute_uv=True, full_matrices=full_matrices)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def svdvals(A, *, driver=None, out=None):
    if driver in ["gesvd", "gesvdj", "gesvda", None]:
        return startai.svdvals(A, driver=driver, out=out)
    else:
        raise ValueError("Unsupported SVD driver")


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def tensorinv(input, ind=2, *, out=None):
    not_invertible = "Reshaped tensor is not invertible"
    prod_cond = "Tensor shape must satisfy prod(A.shape[:ind]) == prod(A.shape[ind:])"
    positive_ind_cond = "Expected a strictly positive integer for 'ind'"
    input_shape = startai.shape(input)
    assert ind > 0, f"{positive_ind_cond}"
    shape_ind_end = input_shape[:ind]
    shape_ind_start = input_shape[ind:]
    prod_ind_end = 1
    prod_ind_start = 1
    for i in shape_ind_start:
        prod_ind_start *= i
    for j in shape_ind_end:
        prod_ind_end *= j
    assert prod_ind_end == prod_ind_start, f"{prod_cond}."
    inverse_shape = shape_ind_start + shape_ind_end
    input = startai.reshape(input, shape=(prod_ind_end, -1))
    inverse_shape_tuple = (*inverse_shape,)
    assert inv_ex(input, check_errors=True), f"{not_invertible}."
    inverse_tensor = startai.inv(input)
    return startai.reshape(inverse_tensor, shape=inverse_shape_tuple, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def tensorsolve(A, B, dims=None, *, out=None):
    return startai.tensorsolve(A, B, axes=dims, out=out)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.2 and below": ("integer", "float", "complex")}, "torch")
def vander(x, N=None):
    if len(x.shape) < 1:
        raise RuntimeError("Input dim must be greater than or equal to 1.")

    # pytorch always return int64 for integers
    if "int" in x.dtype:
        x = startai.astype(x, startai.int64)

    if len(x.shape) == 1:
        # torch always returns the powers in ascending order
        return startai.vander(x, N=N, increasing=True)

    # support multi-dimensional array
    original_shape = x.shape
    if N is None:
        N = x.shape[-1]

    # store the vander output
    x = startai.reshape(x, (-1, x.shape[-1]))
    output = []

    for i in range(x.shape[0]):
        output.append(startai.vander(x[i], N=N, increasing=True))

    output = startai.stack(output)
    output = startai.reshape(output, (*original_shape, N))
    output = startai.astype(output, x.dtype)
    return output


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def vecdot(x, y, *, dim=-1, out=None):
    if "complex" in startai.as_startai_dtype(x.dtype):
        x = startai.conj(x)
    return startai.sum(startai.multiply(x, y), axis=dim)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"2.2 and below": ("float32", "float64", "complex32", "complex64")}, "torch"
)
def vector_norm(input, ord=2, dim=None, keepdim=False, *, dtype=None, out=None):
    return startai.vector_norm(
        input, axis=dim, keepdims=keepdim, ord=ord, out=out, dtype=dtype
    )
