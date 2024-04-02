# global
import startai
import startai.functional.frontends.torch as torch_frontend
from startai.func_wrapper import with_unsupported_dtypes
from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back

# local
from collections import namedtuple


# --- Helpers --- #
# --------------- #


def _compute_allclose_with_tol(input, other, rtol, atol):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.all(
        startai.less_equal(
            startai.abs(startai.subtract(input, other)),
            startai.add(atol, startai.multiply(rtol, startai.abs(other))),
        )
    )


def _compute_isclose_with_tol(input, other, rtol, atol):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.less_equal(
        startai.abs(startai.subtract(input, other)),
        startai.add(atol, startai.multiply(rtol, startai.abs(other))),
    )


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def allclose(input, other, rtol=1e-05, atol=1e-08, equal_nan=False):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    finite_input = startai.isfinite(input)
    finite_other = startai.isfinite(other)
    if startai.all(finite_input) and startai.all(finite_other):
        ret = _compute_allclose_with_tol(input, other, rtol, atol)
        return startai.all_equal(True, ret)
    else:
        finites = startai.bitwise_and(finite_input, finite_other)
        ret = startai.zeros_like(finites)
        ret_ = ret.astype(int)
        input = input * startai.ones_like(ret_)
        other = other * startai.ones_like(ret_)
        ret[finites] = _compute_allclose_with_tol(
            input[finites], other[finites], rtol, atol
        )
        nans = startai.bitwise_invert(finites)
        ret[nans] = startai.equal(input[nans], other[nans])
        if equal_nan:
            both_nan = startai.bitwise_and(startai.isnan(input), startai.isnan(other))
            ret[both_nan] = both_nan[both_nan]
        return startai.all(ret)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@to_startai_arrays_and_back
def argsort(input, dim=-1, descending=False):
    return startai.argsort(input, axis=dim, descending=descending)


@to_startai_arrays_and_back
def eq(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.equal(input, other, out=out)


@to_startai_arrays_and_back
def equal(input, other):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.all(startai.equal(input, other))


@to_startai_arrays_and_back
def fmax(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.where(
        startai.bitwise_or(startai.greater(input, other), startai.isnan(other)),
        input,
        other,
        out=out,
    )


@to_startai_arrays_and_back
def fmin(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.where(
        startai.bitwise_or(startai.less(input, other), startai.isnan(other)),
        input,
        other,
        out=out,
    )


@with_unsupported_dtypes({"2.2 and below": ("complex64", "complex128")}, "torch")
@to_startai_arrays_and_back
def greater(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.greater(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex64", "complex128")}, "torch")
@to_startai_arrays_and_back
def greater_equal(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.greater_equal(input, other, out=out)


@to_startai_arrays_and_back
def isclose(input, other, rtol=1e-05, atol=1e-08, equal_nan=False):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    finite_input = startai.isfinite(input)
    finite_other = startai.isfinite(other)
    if startai.all(finite_input) and startai.all(finite_other):
        return _compute_isclose_with_tol(input, other, rtol, atol)

    else:
        finites = startai.bitwise_and(finite_input, finite_other)
        ret = startai.zeros_like(finites)
        ret_ = ret.astype(int)
        input = input * startai.ones_like(ret_)
        other = other * startai.ones_like(ret_)
        ret[finites] = _compute_isclose_with_tol(
            input[finites], other[finites], rtol, atol
        )
        nans = startai.bitwise_invert(finites)
        ret[nans] = startai.equal(input[nans], other[nans])
        if equal_nan:
            both_nan = startai.bitwise_and(startai.isnan(input), startai.isnan(other))
            ret[both_nan] = both_nan[both_nan]
        return ret


@to_startai_arrays_and_back
def isfinite(input):
    return startai.isfinite(input)


@with_unsupported_dtypes(
    {"2.2 and below": ("float16", "bfloat16", "complex", "bool")}, "torch"
)
@to_startai_arrays_and_back
def isin(elements, test_elements, *, assume_unique=False, invert=False):
    input_elements_copy = startai.reshape(startai.to_startai(elements), (-1,))
    test_elements_copy = startai.reshape(startai.to_startai(test_elements), (-1,))

    if (
        startai.shape(test_elements_copy)[0]
        < 10 * startai.shape(input_elements_copy)[0] ** 0.145
    ):
        if invert:
            mask = startai.ones(startai.shape(input_elements_copy[0]), dtype=bool)
            for a in test_elements_copy:
                mask &= input_elements_copy != a
        else:
            mask = startai.zeros(startai.shape(input_elements_copy[0]), dtype=bool)
            for a in test_elements_copy:
                mask |= input_elements_copy == a
        return startai.reshape(mask, startai.shape(elements))

    if not assume_unique:
        input_elements_copy, rev_idx = startai.unique_inverse(input_elements_copy)
        test_elements_copy = startai.sort(startai.unique_values(test_elements_copy))

    ar = startai.concat((input_elements_copy, test_elements_copy))

    order = startai.argsort(ar, stable=True)
    sar = ar[order]
    if invert:
        bool_ar = sar[1:] != sar[:-1]
    else:
        bool_ar = sar[1:] == sar[:-1]
    flag = startai.concat((bool_ar, startai.array([invert])))
    ret = startai.empty(startai.shape(ar), dtype=bool)
    ret[order] = flag

    if assume_unique:
        return startai.reshape(
            ret[: startai.shape(input_elements_copy)[0]], startai.shape(elements)
        )
    else:
        return startai.reshape(ret[rev_idx], startai.shape(elements))


@to_startai_arrays_and_back
def isinf(input):
    return startai.isinf(input)


@to_startai_arrays_and_back
def isnan(input):
    return startai.isnan(input)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@to_startai_arrays_and_back
def isneginf(input, *, out=None):
    is_inf = startai.isinf(input)
    neg_sign_bit = startai.less(input, 0)
    return startai.logical_and(is_inf, neg_sign_bit, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@to_startai_arrays_and_back
def isposinf(input, *, out=None):
    is_inf = startai.isinf(input)
    pos_sign_bit = startai.bitwise_invert(startai.less(input, 0))
    return startai.logical_and(is_inf, pos_sign_bit, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bfloat16",)}, "torch")
@to_startai_arrays_and_back
def isreal(input):
    return startai.isreal(input)


@with_unsupported_dtypes(
    {"2.2 and below": ("bfloat16", "float16", "bool", "complex")}, "torch"
)
@to_startai_arrays_and_back
def kthvalue(input, k, dim=-1, keepdim=False, *, out=None):
    sorted_input = startai.sort(input, axis=dim)
    sort_indices = startai.argsort(input, axis=dim)

    values = startai.asarray(
        startai.gather(sorted_input, startai.array(k - 1), axis=dim), dtype=input.dtype
    )
    indices = startai.asarray(
        startai.gather(sort_indices, startai.array(k - 1), axis=dim), dtype="int64"
    )

    if keepdim:
        values = startai.expand_dims(values, axis=dim)
        indices = startai.expand_dims(indices, axis=dim)

    ret = namedtuple("sort", ["values", "indices"])(values, indices)
    if startai.exists(out):
        return startai.inplace_update(out, ret)
    return ret


@with_unsupported_dtypes({"2.2 and below": ("complex64", "complex128")}, "torch")
@to_startai_arrays_and_back
def less(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.less(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex64", "complex128")}, "torch")
@to_startai_arrays_and_back
def less_equal(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.less_equal(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex64", "complex128")}, "torch")
@to_startai_arrays_and_back
def maximum(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.maximum(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex64", "complex128")}, "torch")
@to_startai_arrays_and_back
def minimum(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.minimum(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@to_startai_arrays_and_back
def msort(input, *, out=None):
    return startai.sort(input, axis=0, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
@to_startai_arrays_and_back
def not_equal(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.not_equal(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@to_startai_arrays_and_back
# TODO: the original torch.sort places * right before `out`
def sort(input, *, dim=-1, descending=False, stable=False, out=None):
    values = startai.sort(input, axis=dim, descending=descending, stable=stable, out=out)
    indices = startai.argsort(input, axis=dim, descending=descending)
    return namedtuple("sort", ["values", "indices"])(values, indices)


@with_unsupported_dtypes({"2.2 and below": ("float16", "complex")}, "torch")
@to_startai_arrays_and_back
def topk(input, k, dim=None, largest=True, sorted=True, *, out=None):
    if dim is None:
        dim = -1
    return startai.top_k(input, k, axis=dim, largest=largest, sorted=sorted, out=out)


ge = greater_equal
gt = greater
le = less_equal
lt = less
ne = not_equal
