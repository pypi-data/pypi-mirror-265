# local
import startai
from startai.functional.frontends.numpy.func_wrapper import (
    to_startai_arrays_and_back,
    from_zero_dim_arrays_to_scalar,
)


@to_startai_arrays_and_back
def eig(a):
    return startai.eig(a)


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def eigh(a, /, UPLO="L"):
    return startai.eigh(a, UPLO=UPLO)


@to_startai_arrays_and_back
def eigvals(a):
    return startai.eig(a)[0]


@to_startai_arrays_and_back
@from_zero_dim_arrays_to_scalar
def eigvalsh(a, /, UPLO="L"):
    return startai.eigvalsh(a, UPLO=UPLO)
