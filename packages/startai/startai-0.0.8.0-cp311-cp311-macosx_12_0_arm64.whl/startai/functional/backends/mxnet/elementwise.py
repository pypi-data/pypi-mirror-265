import mxnet as mx
from typing import Union, Optional
from startai.func_wrapper import with_supported_dtypes
from . import backend_version
from startai.utils.exceptions import StartaiNotImplementedException
import startai


def abs(
    x: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.abs(x)


def acos(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.arccos(x)


def acosh(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.arccosh(x)


def add(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    alpha: Optional[Union[(int, float)]] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    if alpha is None or alpha == 1.0:
        return mx.nd.add(x1, x2)
    return mx.nd.add(mx.nd.multiply(x1, alpha), x2)


def asin(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.arcsin(x)


def asinh(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.arcsinh(x)


def atan(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.arctan(x)


def atan2(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.arctan2(x1, x2)


def atanh(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.arctanh(x)


def bitwise_and(
    x1: Union[(int, None, mx.ndarray.NDArray)],
    x2: Union[(int, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def bitwise_invert(
    x: Union[(int, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def bitwise_left_shift(
    x1: Union[(int, None, mx.ndarray.NDArray)],
    x2: Union[(int, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def bitwise_or(
    x1: Union[(int, None, mx.ndarray.NDArray)],
    x2: Union[(int, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def bitwise_right_shift(
    x1: Union[(int, None, mx.ndarray.NDArray)],
    x2: Union[(int, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def bitwise_xor(
    x1: Union[(int, None, mx.ndarray.NDArray)],
    x2: Union[(int, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def ceil(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.ceil(x)


def cos(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.cos(x)


def cosh(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.cosh(x)


def divide(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    ret = mx.nd.divide(x1, x2)
    if startai.is_float_dtype(x1.dtype) or startai.is_complex_dtype(x1.dtype):
        ret = mx.nd.array(ret, dtype=x1.dtype)
    else:
        ret = mx.nd.array(ret, dtype=startai.default_float_dtype(as_native=True))
    return ret


def equal(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def exp(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.exp(x)


def expm1(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return (mx.nd.exp(x) - 1).astype(x.dtype)


def floor(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.floor(x)


def floor_divide(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.floor(mx.nd.divide(x1, x2))


def fmin(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def greater(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.greater(x1, x2)


def greater_equal(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.greater_equal(x1, x2)


def isfinite(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def isinf(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    detect_positive: bool = True,
    detect_negative: bool = True,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def isnan(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def lcm(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def less(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.less(x1, x2)


def less_equal(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.less_equal(x1, x2)


def log(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.log(x)


def log10(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def log1p(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.log1p(x)


def log2(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.log2(x)


def logaddexp(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.logaddexp(x1, x2)


def logaddexp2(
    x1: Union[(None, mx.ndarray.NDArray, float, list, tuple)],
    x2: Union[(None, mx.ndarray.NDArray, float, list, tuple)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def logical_and(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.logical_and(x1, x2)


def logical_not(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.logical_not(x)


def logical_or(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.logical_or(x1, x2)


def logical_xor(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.logical_xor(x1, x2)


def multiply(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.multiply(x1, x2)


def negative(
    x: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.negative(x)


def not_equal(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def positive(
    x: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def pow(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(int, float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.power(x1, x2)


def remainder(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    modulus: bool = True,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def round(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    decimals: int = 0,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def sign(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


@with_supported_dtypes(
    {"1.9.1 and below": ("float",)},
    backend_version,
)
def sin(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    x_dtype = x.dtype
    # have to handle zero dim array separately from dtype
    zero_dim = False
    if x.shape == ():
        ret = mx.nd.sin(mx.nd.array([x.asscalar()]))
        zero_dim = True
    else:
        ret = mx.nd.sin(x)

    if "int" in str(x_dtype):
        ret = ret.astype("float32")
    else:
        ret = ret.astype(x_dtype)

    if zero_dim:
        return ret.reshape(())
    return ret


def sinh(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.sinh(x)


def sqrt(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.sqrt(x)


def square(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.square(x)


def subtract(
    x1: Union[(float, None, mx.ndarray.NDArray)],
    x2: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    alpha: Optional[Union[(int, float)]] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    if alpha not in (1, None):
        startai.set_array_mode(False)
        x2 = multiply(x2, alpha)
        startai.unset_array_mode()
    return mx.nd.subtract(x1, x2)


def trapz(
    y: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    x: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
    dx: float = 1.0,
    axis: int = (-1),
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def tan(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.tan(x)


def tanh(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    complex_mode="jax",
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.tanh(x)


def trunc(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def imag(
    val: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def angle(
    input: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    deg: Optional[bool] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def exp2(
    x: Union[(None, mx.ndarray.NDArray, float, list, tuple)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def erf(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def maximum(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    use_where: bool = True,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def minimum(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    use_where: bool = True,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def reciprocal(
    x: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    return mx.nd.reciprocal(x)


def deg2rad(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def rad2deg(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def isreal(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def fmod(
    x1: Union[(None, mx.ndarray.NDArray)],
    x2: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def real(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()
