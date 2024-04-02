# global
import startai
from startai.func_wrapper import with_unsupported_dtypes
import startai.functional.frontends.torch as torch_frontend
from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def addbmm(input, batch1, batch2, *, beta=1, alpha=1, out=None):
    if len(startai.shape(batch1)) != 3 or len(startai.shape(batch2)) != 3:
        raise RuntimeError("input must be 3D matrices")
    batch1, batch2 = torch_frontend.promote_types_of_torch_inputs(batch1, batch2)
    ret = startai.matmul(batch1, batch2, out=out)
    ret = startai.sum(ret, axis=0, keepdims=False, dtype=startai.dtype(ret), out=out)
    alpha, ret = torch_frontend.promote_types_of_torch_inputs(alpha, ret)
    ret = startai.multiply(alpha, ret, out=out)
    beta, input = torch_frontend.promote_types_of_torch_inputs(beta, input)
    beta_input = startai.multiply(beta, input, out=out)
    beta_input, ret = torch_frontend.promote_types_of_torch_inputs(beta_input, ret)
    return startai.add(beta_input, ret, out=out)


@to_startai_arrays_and_back
def addmm(input, mat1, mat2, *, beta=1, alpha=1, out=None):
    if len(startai.shape(mat1)) != 2 or len(startai.shape(mat2)) != 2:
        raise RuntimeError("input must be 2D matrices")
    mat1, mat2 = torch_frontend.promote_types_of_torch_inputs(mat1, mat2)
    ret = startai.matmul(mat1, mat2, out=out)
    alpha, ret = torch_frontend.promote_types_of_torch_inputs(alpha, ret)
    ret = startai.multiply(alpha, ret, out=out)
    beta, input = torch_frontend.promote_types_of_torch_inputs(beta, input)
    beta_input = startai.multiply(beta, input, out=out)
    beta_input, ret = torch_frontend.promote_types_of_torch_inputs(beta_input, ret)
    return startai.add(beta_input, ret, out=out)


@to_startai_arrays_and_back
def addmv(input, mat, vec, *, beta=1, alpha=1, out=None):
    if len(startai.shape(mat)) != 2 or len(startai.shape(vec)) != 1:
        raise RuntimeError("input must be 2D matrix and 1D vector")
    mat, vec = torch_frontend.promote_types_of_torch_inputs(mat, vec)
    ret = startai.matmul(mat, vec, out=out)
    alpha, ret = torch_frontend.promote_types_of_torch_inputs(alpha, ret)
    ret = startai.multiply(alpha, ret, out=out)
    beta, input = torch_frontend.promote_types_of_torch_inputs(beta, input)
    beta_input = startai.multiply(beta, input, out=out)
    beta_input, ret = torch_frontend.promote_types_of_torch_inputs(beta_input, ret)
    return startai.add(beta_input, ret, out=out)


@to_startai_arrays_and_back
def addr(input, vec1, vec2, *, beta=1, alpha=1, out=None):
    if len(startai.shape(vec1)) != 1 or len(startai.shape(vec2)) != 1:
        raise RuntimeError("input must be 1D vectors")
    vec1, vec2 = torch_frontend.promote_types_of_torch_inputs(vec1, vec2)
    ret = startai.outer(vec1, vec2, out=out)
    alpha, ret = torch_frontend.promote_types_of_torch_inputs(alpha, ret)
    ret = startai.multiply(alpha, ret, out=out)
    beta, input = torch_frontend.promote_types_of_torch_inputs(beta, input)
    beta_input = startai.multiply(beta, input, out=out)
    beta_input, ret = torch_frontend.promote_types_of_torch_inputs(beta_input, ret)
    return startai.add(beta_input, ret, out=out)


@to_startai_arrays_and_back
def baddbmm(input, batch1, batch2, *, beta=1, alpha=1, out=None):
    if len(startai.shape(batch1)) != 3 or len(startai.shape(batch2)) != 3:
        raise RuntimeError("input must be batched 2D matrices")
    batch1, batch2 = torch_frontend.promote_types_of_torch_inputs(batch1, batch2)
    ret = startai.matmul(batch1, batch2, out=out)
    alpha, ret = torch_frontend.promote_types_of_torch_inputs(alpha, ret)
    ret = startai.multiply(alpha, ret, out=out)
    beta, input = torch_frontend.promote_types_of_torch_inputs(beta, input)
    beta_input = startai.multiply(beta, input, out=out)
    beta_input, ret = torch_frontend.promote_types_of_torch_inputs(beta_input, ret)
    return startai.add(beta_input, ret, out=out)


@to_startai_arrays_and_back
def bmm(input, mat2, *, out=None):
    if len(startai.shape(input)) != 3 or len(startai.shape(mat2)) != 3:
        raise RuntimeError("input must be 3D matrices")
    input, mat2 = torch_frontend.promote_types_of_torch_inputs(input, mat2)
    return startai.matmul(input, mat2, out=out)


@to_startai_arrays_and_back
def chain_matmul(*matrices, out=None):
    return startai.multi_dot(matrices, out=out)


@to_startai_arrays_and_back
def cholesky(input, upper=False, *, out=None):
    return startai.cholesky(input, upper=upper, out=out)


@to_startai_arrays_and_back
def det(input):
    return torch_frontend.linalg.det(input)


@to_startai_arrays_and_back
def dot(input, other, *, out=None):
    if len(input.shape) == 1 and len(other.shape) == 1:
        input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
        return startai.matmul(input, other, out=out)
    else:
        raise RuntimeError("input must be 1D vectors")


@to_startai_arrays_and_back
def ger(input, vec2, *, out=None):
    input, vec2 = torch_frontend.promote_types_of_torch_inputs(input, vec2)
    return startai.outer(input, vec2, out=out)


@to_startai_arrays_and_back
def inner(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.inner(input, other, out=out)


@to_startai_arrays_and_back
def inverse(input, *, out=None):
    return torch_frontend.linalg.inv(input, out=out)


@to_startai_arrays_and_back
def logdet(input):
    return startai.det(input).log()


@to_startai_arrays_and_back
def matmul(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.matmul(input, other, out=out)


@to_startai_arrays_and_back
def matrix_power(A, n, *, out=None):
    return torch_frontend.linalg.matrix_power(A, n, out=out)


@to_startai_arrays_and_back
def matrix_rank(input, tol=None, symmetric=False, *, out=None):
    return startai.matrix_rank(input, atol=tol, hermitian=symmetric, out=out)


@to_startai_arrays_and_back
def mm(input, mat2, *, out=None):
    if len(startai.shape(input)) != 2 or len(startai.shape(mat2)) != 2:
        raise RuntimeError("input must be 2D matrices")
    input, mat2 = torch_frontend.promote_types_of_torch_inputs(input, mat2)
    return startai.matmul(input, mat2, out=out)


@to_startai_arrays_and_back
def mv(input, vec, *, out=None):
    if len(startai.shape(input)) != 2 or len(startai.shape(vec)) != 1:
        raise RuntimeError("input must be 2D matrix and 1D vector")
    input, vec = torch_frontend.promote_types_of_torch_inputs(input, vec)
    return startai.matmul(input, vec, out=out)


@to_startai_arrays_and_back
def outer(input, vec2, *, out=None):
    input, vec2 = torch_frontend.promote_types_of_torch_inputs(input, vec2)
    return startai.outer(input, vec2, out=out)


@to_startai_arrays_and_back
def pinverse(input, rcond=1e-15):
    return startai.pinv(input, rtol=rcond)


@to_startai_arrays_and_back
def qr(input, some=True, *, out=None):
    if some:
        ret = startai.qr(input, mode="reduced")
    else:
        ret = startai.qr(input, mode="complete")
    if startai.exists(out):
        return startai.inplace_update(out, ret)
    return ret


@to_startai_arrays_and_back
def slogdet(A, *, out=None):
    return torch_frontend.linalg.slogdet(A, out=out)


@to_startai_arrays_and_back
def svd(input, some=True, compute_uv=True, *, out=None):
    # TODO: add compute_uv
    if some:
        ret = startai.svd(input, full_matrices=False)
    else:
        ret = startai.svd(input, full_matrices=True)
    if startai.exists(out):
        return startai.inplace_update(out, ret)
    return ret


@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
@to_startai_arrays_and_back
def trapezoid(y, x=None, *, dx=None, dim=-1):
    if x is not None:
        y, x = torch_frontend.promote_types_of_torch_inputs(y, x)
    return startai.trapz(y, x=x, dx=dx, axis=dim)


@to_startai_arrays_and_back
def vdot(input, other, *, out=None):
    if len(input.shape) != 1 or len(other.shape) != 1:
        raise RuntimeError("input must be 1D vectors")
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    ret = startai.vecdot(input, other, out=out)
    return ret.squeeze(0) if ret.ndim == 1 else ret


# alias to fix mm transpilation issue as mm() gets mapped to spmm() after transpilation
spmm = mm
