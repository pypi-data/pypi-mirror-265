# local
import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def cholesky(a):
    return startai.cholesky(a)


@to_startai_arrays_and_back
def qr(a, mode="reduced"):
    return startai.qr(a, mode=mode)


@to_startai_arrays_and_back
def svd(a, full_matrices=True, compute_uv=True, hermitian=False):
    # Todo: conpute_uv and hermitian handling
    return startai.svd(a, full_matrices=full_matrices, compute_uv=compute_uv)
