# global
import startai
from startai.func_wrapper import (
    with_unsupported_dtypes,
    with_supported_dtypes,
)
import startai.functional.frontends.torch as torch_frontend
from startai.functional.frontends.torch.func_wrapper import (
    to_startai_arrays_and_back,
)


erfc = torch_frontend.special.erfc


@to_startai_arrays_and_back
def abs(input, *, out=None):
    return startai.abs(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def acos(input, *, out=None):
    return startai.acos(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def acosh(input, *, out=None):
    return startai.acosh(input, out=out)


@with_supported_dtypes(
    {"1.12.0 and below": ("float32", "float64", "int32", "int64")}, "jax"
)
@to_startai_arrays_and_back
def add(input, other, *, alpha=1, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.add(input, other, alpha=alpha, out=out)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
def addcdiv(input, tensor1, tensor2, *, value=1, out=None):
    return startai.add(input, startai.multiply(value, startai.divide(tensor1, tensor2)), out=out)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
def addcmul(input, tensor1, tensor2, *, value=1, out=None):
    return startai.add(input, startai.multiply(value, startai.multiply(tensor1, tensor2)), out=out)


@to_startai_arrays_and_back
def angle(input, *, out=None):
    return startai.angle(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def asin(input, *, out=None):
    return startai.asin(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def asinh(input, *, out=None):
    return startai.asinh(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def atan(input, *, out=None):
    return startai.atan(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
@to_startai_arrays_and_back
def atan2(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.atan2(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def atanh(input, *, out=None):
    return startai.atanh(input, out=out)


@to_startai_arrays_and_back
def bitwise_and(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.bitwise_and(input, other, out=out)


@to_startai_arrays_and_back
def bitwise_left_shift(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.bitwise_left_shift(input, other, out=out)


@to_startai_arrays_and_back
def bitwise_not(input, *, out=None):
    return startai.bitwise_invert(input, out=out)


@to_startai_arrays_and_back
def bitwise_or(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.bitwise_or(input, other, out=out)


@to_startai_arrays_and_back
def bitwise_right_shift(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.bitwise_right_shift(input, other, out=out)


@to_startai_arrays_and_back
def bitwise_xor(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.bitwise_xor(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def ceil(input, *, out=None):
    return startai.ceil(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16", "complex")}, "torch")
@to_startai_arrays_and_back
def clamp(input, min=None, max=None, *, out=None):
    startai.utils.assertions.check_all_or_any_fn(
        min,
        max,
        fn=startai.exists,
        type="any",
        limit=[1, 2],
        message="at most one of min or max can be None",
    )
    if min is None:
        return startai.minimum(input, max, out=out)
    if max is None:
        return startai.maximum(input, min, out=out)
    return startai.clip(input, min, max, out=out)


@to_startai_arrays_and_back
def conj_physical(input, *, out=None):
    return startai.conj(input, out=out)


@with_unsupported_dtypes({"1.12.0 and below": ("float16",)}, "jax")
@to_startai_arrays_and_back
def copysign(input, other, *, out=None):
    return startai.copysign(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def cos(input, *, out=None):
    return startai.cos(input, out=out)


@to_startai_arrays_and_back
def cosh(input, *, out=None):
    return startai.cosh(input, out=out)


@to_startai_arrays_and_back
def deg2rad(input, *, out=None):
    return startai.array(input * startai.pi / 180, out=out)


@to_startai_arrays_and_back
def div(input, other, *, rounding_mode=None, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    if rounding_mode is not None:
        promoted = input.dtype
        if rounding_mode == "trunc":
            return startai.astype(startai.trunc_divide(input, other, out=out), promoted)
        else:
            return startai.astype(startai.floor_divide(input, other, out=out), promoted)
    else:
        return startai.divide(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16", "complex")}, "torch")
@to_startai_arrays_and_back
def erf(input, *, out=None):
    return startai.erf(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def exp(input, *, out=None):
    return startai.exp(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def exp2(input, out=None):
    return startai.exp2(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def expm1(input, out=None):
    return startai.expm1(input, out=out)


@to_startai_arrays_and_back
def flipud(input):
    return startai.flipud(input)


@with_unsupported_dtypes({"1.12.0 and below": ("bfloat16", "float16")}, "jax")
@to_startai_arrays_and_back
def float_power(input, exponent, *, out=None):
    input, exponent = torch_frontend.promote_types_of_torch_inputs(input, exponent)
    return startai.float_power(input, exponent, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def floor(input, *, out=None):
    return startai.floor(input, out=out)


@to_startai_arrays_and_back
def floor_divide(input, other, *, out=None):
    return startai.floor_divide(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
@to_startai_arrays_and_back
def fmod(x1, x2, out=None):
    return startai.fmod(x1, x2, out=out)


@to_startai_arrays_and_back
def frac(input, *, out=None):
    return input - startai.sign(input) * startai.floor(startai.abs(input))


@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
@to_startai_arrays_and_back
def frexp(input, *, out=None):
    return startai.frexp(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bfloat16",)}, "torch")
@to_startai_arrays_and_back
def gradient(input, *, spacing=1, dim=None, edge_order=1):
    return startai.gradient(input, spacing=spacing, edge_order=edge_order, axis=dim)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def hypot(input, other, *, out=None):
    return startai.hypot(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def i0(input, *, out=None):
    return startai.i0(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bfloat16",)}, "torch")
@to_startai_arrays_and_back
def igamma(input, other, *, out=None):
    return startai.igamma(input, x=other, out=out)


@to_startai_arrays_and_back
def imag(input):
    return startai.imag(input)


@with_supported_dtypes({"2.2 and below": ("float16", "float32", "float64")}, "torch")
@to_startai_arrays_and_back
def ldexp(input, other, *, out=None):
    value = startai.pow(2, other, out=out)
    value = startai.multiply(input, value, out=out)
    return value


@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
@to_startai_arrays_and_back
def lerp(input, end, weight, *, out=None):
    return startai.lerp(input, end, weight, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def lgamma(input, *, out=None):
    return startai.lgamma(input, out=out)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def log(input, *, out=None):
    return startai.log(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def log10(input, *, out=None):
    return startai.log10(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def log1p(input, *, out=None):
    return startai.log1p(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def log2(input, *, out=None):
    return startai.log2(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def logaddexp(x1, x2, out=None):
    return startai.logaddexp(x1, x2, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def logaddexp2(x1, x2, out=None):
    return startai.logaddexp2(x1, x2, out=out)


@to_startai_arrays_and_back
def logical_and(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.logical_and(input, other, out=out)


@to_startai_arrays_and_back
def logical_not(input, *, out=None):
    return startai.logical_not(input, out=out)


@to_startai_arrays_and_back
def logical_or(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.logical_or(input, other, out=out)


@to_startai_arrays_and_back
def logical_xor(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.logical_xor(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16", "bfloat16")}, "torch")
@to_startai_arrays_and_back
def logit(input, eps=None, *, out=None):
    return startai.logit(input, eps=eps, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bfloat16",)}, "torch")
@to_startai_arrays_and_back
def masked_fill(input, mask, value):
    return startai.where(mask, value, input, out=input)


@to_startai_arrays_and_back
def mul(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.multiply(input, other, out=out)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
def mvlgamma(input, p, *, out=None):
    startai.assertions.check_greater(
        p, 1, allow_equal=True, message="p has to be greater than or equal to 1"
    )
    c = 0.25 * p * (p - 1) * startai.log(startai.pi, out=out)
    b = 0.5 * startai.arange((1 - p), 1, 1, dtype=input.dtype, device=input.device, out=out)
    return (
        startai.sum(
            startai.lgamma(startai.expand_dims(input, axis=-1) + b, out=out), axis=-1, out=out
        )
        + c
    )


@with_unsupported_dtypes({"2.2 and below": ("bfloat16",)}, "tensorflow")
@to_startai_arrays_and_back
def nan_to_num(input, nan=0.0, posinf=None, neginf=None, *, out=None):
    return startai.nan_to_num(input, nan=nan, posinf=posinf, neginf=neginf, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bool",)}, "torch")
@to_startai_arrays_and_back
def negative(input, *, out=None):
    return startai.negative(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bfloat16", "float16")}, "torch")
@to_startai_arrays_and_back
def nextafter(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.nextafter(input, other, out=out)


@to_startai_arrays_and_back
def positive(input, *, out=None):
    return startai.positive(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bool",)}, "torch")
@to_startai_arrays_and_back
def pow(input, exponent, *, out=None):
    if not startai.is_array(exponent):
        if (
            any(dtype in str(input.dtype) for dtype in ["int8", "int16"])
            and isinstance(exponent, int)
        ) or ("float16" in str(input.dtype) and isinstance(exponent, float)):
            exponent = startai.array(exponent, dtype=input.dtype)
        else:
            exponent = torch_frontend.as_tensor(exponent).startai_array
    input, exponent = torch_frontend.promote_types_of_torch_inputs(input, exponent)
    ret_dtype = input.dtype
    if not startai.is_int_dtype(exponent) and startai.is_int_dtype(ret_dtype):
        ret_dtype = exponent.dtype
    ret = startai.pow(input, exponent)
    if startai.any(input == 0) and startai.is_int_dtype(exponent):
        ret = startai.where(startai.bitwise_and(input == 0, exponent < 0), 0, ret, out=out)
    return ret.astype(ret_dtype)


@to_startai_arrays_and_back
def rad2deg(input, *, out=None):
    return startai.rad2deg(input, out=out)


@to_startai_arrays_and_back
def real(input):
    return startai.real(input)


@to_startai_arrays_and_back
def reciprocal(input, *, out=None):
    return startai.reciprocal(input)


@to_startai_arrays_and_back
def remainder(input, other, *, out=None):
    if startai.is_array(input) and startai.isscalar(other):
        other = startai.full(input.shape, other)
    return startai.remainder(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bfloat16",)}, "torch")
@to_startai_arrays_and_back
def round(input, *, decimals=0, out=None):
    m = startai.full(input.shape, 10.0**decimals)
    upscale = startai.multiply(input, m)
    rounded = startai.round(upscale)
    return startai.divide(rounded, m, out=out).astype(input.dtype)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def rsqrt(input, *, out=None):
    return startai.reciprocal(startai.sqrt(input), out=out)


@to_startai_arrays_and_back
def sgn(input, *, out=None):
    if startai.is_complex_dtype(input.dtype):
        input_abs = startai.abs(input, out=out)
        # TODO wrap this in Where function after solve it's errors
        if input_abs == 0:
            return 0
        else:
            return startai.divide(input, input_abs, out=out)
    else:
        return startai.sign(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def sigmoid(input, *, out=None):
    return startai.sigmoid(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@to_startai_arrays_and_back
def sign(input, *, out=None):
    return startai.sign(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("complex",)}, "torch")
@to_startai_arrays_and_back
def signbit(input, *, out=None):
    return startai.signbit(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def sin(input, *, out=None):
    return startai.sin(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def sinc(input, *, out=None):
    return startai.sinc(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def sinh(input, *, out=None):
    return startai.sinh(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def sqrt(input, *, out=None):
    return startai.sqrt(input, out=out)


@to_startai_arrays_and_back
def square(input, *, out=None):
    return startai.square(input, out=out)


@to_startai_arrays_and_back
def subtract(input, other, *, alpha=1, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.subtract(input, other * alpha, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def tan(input, *, out=None):
    return startai.tan(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def tanh(input, *, out=None):
    return startai.tanh(input, out=out)


@to_startai_arrays_and_back
def true_divide(input, other, *, out=None):
    input, other = torch_frontend.promote_types_of_torch_inputs(input, other)
    return startai.divide(input, other, out=out)


@with_unsupported_dtypes({"2.2 and below": ("float16",)}, "torch")
@to_startai_arrays_and_back
def trunc(input, *, out=None):
    return startai.trunc(input, out=out)


@with_unsupported_dtypes({"2.2 and below": ("bfloat16",)}, "tensorflow")
@to_startai_arrays_and_back
def xlogy(input, other, *, out=None):
    return startai.xlogy(input, other, out=out)


absolute = abs
arccos = acos
arccosh = acosh
arcsin = asin
arcsinh = asinh
arctan = atan
arctan2 = atan2
arctanh = atanh
clip = clamp
divide = div
fix = trunc
multiply = mul
sub = subtract
