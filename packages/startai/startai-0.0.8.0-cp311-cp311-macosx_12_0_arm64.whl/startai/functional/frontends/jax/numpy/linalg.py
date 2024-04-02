# local
import startai
from startai.functional.frontends.jax import Array
from startai.functional.frontends.jax.func_wrapper import to_startai_arrays_and_back
from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from startai.functional.frontends.jax.numpy import promote_types_of_jax_inputs
from startai.functional.frontends.numpy.linalg import lstsq as numpy_lstsq


@to_startai_arrays_and_back
def cholesky(a):
    return startai.cholesky(a)


@to_startai_arrays_and_back
def cond(x, p=None):
    return startai.cond(x, p=p)


@to_startai_arrays_and_back
def det(a):
    return startai.det(a)


@to_startai_arrays_and_back
def eig(a):
    return startai.eig(a)


@to_startai_arrays_and_back
def eigh(a, UPLO="L", symmetrize_input=True):
    def symmetrize(x):
        # TODO : Take Hermitian transpose after complex numbers added
        return (x + startai.swapaxes(x, -1, -2)) / 2

    if symmetrize_input:
        a = symmetrize(a)

    return startai.eigh(a, UPLO=UPLO)


@to_startai_arrays_and_back
def eigvals(a):
    return startai.eigvals(a)


@to_startai_arrays_and_back
def eigvalsh(a, UPLO="L"):
    return startai.eigvalsh(a, UPLO=UPLO)


@to_startai_arrays_and_back
def inv(a):
    return startai.inv(a)


# TODO: replace this with function from API
# As the composition provides numerically unstable results
@to_startai_arrays_and_back
def lstsq(a, b, rcond=None, *, numpy_resid=False):
    if numpy_resid:
        return numpy_lstsq(a, b, rcond=rcond)
    least_squares_solution = startai.matmul(
        startai.pinv(a, rtol=1e-15).astype(startai.float64), b.astype(startai.float64)
    )
    residuals = startai.sum((b - startai.matmul(a, least_squares_solution)) ** 2).astype(
        startai.float64
    )
    svd_values = startai.svd(a, compute_uv=False)
    rank = startai.matrix_rank(a).astype(startai.int32)
    return (least_squares_solution, residuals, rank, svd_values[0])


@to_startai_arrays_and_back
def matrix_power(a, n):
    return startai.matrix_power(a, n)


@to_startai_arrays_and_back
def matrix_rank(M, tol=None):
    return startai.matrix_rank(M, atol=tol)


@to_startai_arrays_and_back
def multi_dot(arrays, *, precision=None):
    return startai.multi_dot(arrays)


@to_startai_arrays_and_back
@with_supported_dtypes(
    {"0.4.24 and below": ("float32", "float64")},
    "jax",
)
def norm(x, ord=None, axis=None, keepdims=False):
    if ord is None:
        ord = 2
    if type(axis) in [list, tuple] and len(axis) == 2:
        return Array(startai.matrix_norm(x, ord=ord, axis=axis, keepdims=keepdims))
    return Array(startai.vector_norm(x, ord=ord, axis=axis, keepdims=keepdims))


@to_startai_arrays_and_back
def pinv(a, rcond=None):
    return startai.pinv(a, rtol=rcond)


@to_startai_arrays_and_back
def qr(a, mode="reduced"):
    return startai.qr(a, mode=mode)


@to_startai_arrays_and_back
def slogdet(a, method=None):
    return startai.slogdet(a)


@to_startai_arrays_and_back
def solve(a, b):
    return startai.solve(a, b)


@to_startai_arrays_and_back
def svd(a, /, *, full_matrices=True, compute_uv=True, hermitian=None):
    if not compute_uv:
        return startai.svdvals(a)
    return startai.svd(a, full_matrices=full_matrices)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"0.4.24 and below": ("float16", "bfloat16")}, "jax")
def tensorinv(a, ind=2):
    old_shape = startai.shape(a)
    prod = 1
    if ind > 0:
        invshape = old_shape[ind:] + old_shape[:ind]
        for k in old_shape[ind:]:
            prod *= k
    else:
        raise ValueError("Invalid ind argument.")
    a = startai.reshape(a, shape=(prod, -1))
    ia = startai.inv(a)
    new_shape = (*invshape,)
    return Array(startai.reshape(ia, shape=new_shape))


@to_startai_arrays_and_back
def tensorsolve(a, b, axes=None):
    a, b = promote_types_of_jax_inputs(a, b)
    return startai.tensorsolve(a, b, axes=axes)
