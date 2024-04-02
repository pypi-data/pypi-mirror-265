# global

# local
import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back

from startai.func_wrapper import with_unsupported_dtypes
from startai.functional.frontends.numpy import promote_types_of_numpy_inputs
from startai.functional.frontends.numpy.linalg.norms_and_other_numbers import matrix_rank


# inv
@with_unsupported_dtypes({"1.26.3 and below": ("float16",)}, "numpy")
@to_startai_arrays_and_back
def inv(a):
    return startai.inv(a)


# TODO: replace this with function from API
# As the compositon provides unstable results
@to_startai_arrays_and_back
@with_unsupported_dtypes({"1.26.3 and below": ("float16",)}, "numpy")
def lstsq(a, b, rcond="warn"):
    solution = startai.matmul(
        startai.pinv(a, rtol=1e-15).astype(startai.float64), b.astype(startai.float64)
    )
    svd = startai.svd(a, compute_uv=False)
    rank = matrix_rank(a).astype(startai.int32)
    residuals = startai.sum((b - startai.matmul(a, solution)) ** 2).astype(startai.float64)
    return (solution, residuals, rank, svd[0])


# pinv
# TODO: add hermitian functionality
@with_unsupported_dtypes({"1.26.3 and below": ("float16",)}, "numpy")
@to_startai_arrays_and_back
def pinv(a, rcond=1e-15, hermitian=False):
    return startai.pinv(a, rtol=rcond)


# solve
@with_unsupported_dtypes({"1.26.3 and below": ("float16",)}, "numpy")
@to_startai_arrays_and_back
def solve(a, b):
    a, b = promote_types_of_numpy_inputs(a, b)
    return startai.solve(a, b)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"1.26.3 and below": ("float16", "blfloat16")}, "numpy")
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
    return startai.reshape(ia, shape=new_shape)
