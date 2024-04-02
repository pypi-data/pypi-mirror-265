# global
import startai
from startai import (
    with_supported_dtypes,
    with_unsupported_dtypes,
    with_supported_device_and_dtypes,
)
from startai.functional.frontends.tensorflow import check_tensorflow_casting
from startai.functional.frontends.tensorflow.func_wrapper import (
    to_startai_arrays_and_back,
    handle_tf_dtype,
    to_startai_dtype,
)


# --- Helpers --- #
# --------------- #


def _chbevl(x, coef, N):
    """Evaluates the series.

            N-1
             - '
      y  =   >   coef[i] T (x/2)
             -            i
            i=0

    of Chebyshev polynomials Ti at argument x/2.

    Coefficients are stored in reverse order, i.e. the zero
    order term is last in the array.  Note N is the number of
    coefficients, not the order.

    If coefficients are for the interval a to b, x must
    have been transformed to x -> 2(2x - b - a)/(b-a) before
    entering the routine.  This maps x from (a, b) to (-1, 1),
    over which the Chebyshev polynomials are defined.

    If the coefficients are for the inverted interval, in
    which (a, b) is mapped to (1/b, 1/a), the transformation
    required is x -> 2(2ab/x - b - a)/(b-a).  If b is infinity,
    this becomes x -> 4a/x - 1.
    """
    b0 = coef[0:1]
    b1 = startai.zeros_like(x)
    i = N - 1
    p = 1

    while i > 0:
        b2 = b1
        b1 = b0
        with startai.PreciseMode(True):
            b0 = x * b1 - b2 + coef[p : p + 1]
        p += 1
        i -= 1

    return 0.5 * (b0 - b2)


def _get_chebyshev_coefficients_for_exp_i1():
    """Chebyshev coefficients for exp(-x) I1(x) / x in the interval [0,8].

    lim(x->0){ exp(-x) I1(x) / x } = 1/2.

    Returns list of 29 float elements
    -------
    """
    return startai.array(
        [
            2.77791411276104639959e-18,
            -2.11142121435816608115e-17,
            1.55363195773620046921e-16,
            -1.10559694773538630805e-15,
            7.60068429473540693410e-15,
            -5.04218550472791168711e-14,
            3.22379336594557470981e-13,
            -1.98397439776494371520e-12,
            1.17361862988909016308e-11,
            -6.66348972350202774223e-11,
            3.62559028155211703701e-10,
            -1.88724975172282928790e-9,
            9.38153738649577178388e-9,
            -4.44505912879632808065e-8,
            2.00329475355213526229e-7,
            -8.56872026469545474066e-7,
            3.47025130813767847674e-6,
            -1.32731636560394358279e-5,
            4.78156510755005422638e-5,
            -1.61760815825896745588e-4,
            5.12285956168575772895e-4,
            -1.51357245063125314899e-3,
            4.15642294431288815669e-3,
            -1.05640848946261981558e-2,
            2.47264490306265168283e-2,
            -5.29459812080949914269e-2,
            1.02643658689847095384e-1,
            -1.76416518357834055153e-1,
            2.52587186443633654823e-1,
        ]
    )


def _get_chebyshev_coefficients_for_exp_sqrt_i1():
    """Chebyshev coefficients for exp(-x) sqrt(x) I1(x) in the inverted
    interval [8,infinity].

    lim(x->inf){ exp(-x) sqrt(x) I1(x) } = 1/sqrt(2pi).

    Returns a list of 25 elements containing float
    -------
    """
    return startai.array(
        [
            7.51729631084210481353e-18,
            4.41434832307170791151e-18,
            -4.65030536848935832153e-17,
            -3.20952592199342395980e-17,
            2.96262899764595013876e-16,
            3.30820231092092828324e-16,
            -1.88035477551078244854e-15,
            -3.81440307243700780478e-15,
            1.04202769841288027642e-14,
            4.27244001671195135429e-14,
            -2.10154184277266431302e-14,
            -4.08355111109219731823e-13,
            -7.19855177624590851209e-13,
            2.03562854414708950722e-12,
            1.41258074366137813316e-11,
            3.25260358301548823856e-11,
            -1.89749581235054123450e-11,
            -5.58974346219658380687e-10,
            -3.83538038596423702205e-9,
            -2.63146884688951950684e-8,
            -2.51223623787020892529e-7,
            -3.88256480887769039346e-6,
            -1.10588938762623716291e-4,
            -9.76109749136146840777e-3,
            7.78576235018280120474e-1,
        ]
    )


# --- Main --- #
# ------------ #


@with_unsupported_dtypes(
    {
        "1.2.0": ("float16", "complex64", "complex128"),
        "1.8.0 and below": ("float16",),
        "2.15.0 and below": ("int8", "int16", "uint8", "uint16", "uint32", "uint64"),
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def abs(x, name=None):
    dtype = startai.dtype(x)
    if dtype in ["complex64", "complex128"]:
        return startai.sqrt(startai.square(startai.real(x)) + startai.square(startai.imag(x)))
    return startai.abs(x)


@to_startai_arrays_and_back
def accumulate_n(inputs, shape=None, tensor_dtype=None, name=None):
    return startai.sum(inputs, axis=0)


@to_startai_arrays_and_back
def acos(x, name="acos"):
    return startai.acos(x)


@to_startai_arrays_and_back
def acosh(x, name="acosh"):
    return startai.acosh(x)


@to_startai_arrays_and_back
def add(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.add(x, y)


@to_startai_arrays_and_back
def add_n(inputs, name=None):
    inputs = startai.array(inputs)
    return startai.sum(inputs, dtype=inputs.dtype, axis=0)


@to_startai_arrays_and_back
def angle(input, name=None):
    return startai.angle(input)


@with_unsupported_dtypes(
    {"2.15.0 and below": ("complex",)},
    "tensorflow",
)
@to_startai_arrays_and_back
def argmax(input, axis, output_type=None, name=None):
    output_type = to_startai_dtype(output_type)
    if output_type in ["int32", "int64"]:
        return startai.astype(startai.argmax(input, axis=axis), output_type)
    else:
        return startai.astype(startai.argmax(input, axis=axis), "int64")


@with_unsupported_dtypes(
    {"2.15.0 and below": ("complex",)},
    "tensorflow",
)
@to_startai_arrays_and_back
def argmin(input, axis=None, output_type="int64", name=None):
    output_type = to_startai_dtype(output_type)
    if output_type in ["int32", "int64"]:
        return startai.astype(startai.argmin(input, axis=axis), output_type)
    else:
        return startai.astype(startai.argmin(input, axis=axis), "int64")


@to_startai_arrays_and_back
def asin(x, name=None):
    return startai.asin(x)


@to_startai_arrays_and_back
def asinh(x, name="asinh"):
    return startai.asinh(x)


@to_startai_arrays_and_back
def atan(x, name=None):
    return startai.atan(x)


@to_startai_arrays_and_back
def atan2(y, x, name=None):
    return startai.atan2(y, x)


@to_startai_arrays_and_back
def atanh(x, name="atanh"):
    return startai.atanh(x)


@with_supported_dtypes(
    {"2.15.0 and below": ("float16", "float32", "float64")}, "tensorflow"
)
@to_startai_arrays_and_back
def bessel_i1(x, name=None):
    z = startai.abs(x)
    result = startai.zeros_like(z)

    mask1 = z <= 8.0

    if startai.any(mask1) > 0:
        y = (z[mask1] / startai.array([2.0])) - startai.array([2.0])
        result[mask1] = (
            _chbevl(y, _get_chebyshev_coefficients_for_exp_i1(), 29)
            * z[mask1]
            * startai.exp(z[mask1])
        )

    mask2 = ~mask1
    if startai.any(mask2) > 0:
        result[mask2] = (
            startai.exp(z[mask2])
            * _chbevl(
                startai.array([32.0]) / z[mask2] - startai.array([2.0]),
                _get_chebyshev_coefficients_for_exp_sqrt_i1(),
                25,
            )
            / startai.sqrt(z[mask2])
        )

    result[x < 0.0] = -result[x < 0.0]

    return result


@with_supported_dtypes(
    {"2.15.0 and below": ("int32",)},
    "tensorflow",
)
@to_startai_arrays_and_back
def bincount(
    arr,
    weights=None,
    minlength=None,
    maxlength=None,
    dtype=startai.int32,
    name=None,
    axis=None,
    binary_output=False,
):
    return startai.bincount(arr, weights=weights, minlength=minlength)


@to_startai_arrays_and_back
def ceil(x, name=None):
    return startai.ceil(x)


@handle_tf_dtype
@to_startai_arrays_and_back
def confusion_matrix(
    labels, predictions, num_classes=None, weights=None, dtype=startai.int32, name=None
):
    labels = startai.astype(
        startai.squeeze(startai.array(labels), axis=None), startai.int64, copy=False
    )
    predictions = startai.astype(
        startai.squeeze(startai.array(predictions), axis=None), startai.int64, copy=False
    )
    # failsafe for (1,) array will be squeeze to 0-dim
    labels = startai.expand_dims(labels, axis=-1) if labels.ndim == 0 else labels
    predictions = (
        startai.expand_dims(predictions, axis=-1) if predictions.ndim == 0 else predictions
    )

    # Sanity check (potential optimization)
    startai.utils.assertions.check_greater(
        labels, 0, allow_equal=True, message="labels contains negative values"
    )
    startai.utils.assertions.check_greater(
        predictions, 0, allow_equal=True, message="predictions contains negative values"
    )

    if num_classes is None:
        num_classes = max(startai.max(labels), startai.max(predictions)) + 1
    else:
        num_classes_int64 = startai.astype(startai.array(num_classes), startai.int64, copy=False)
        startai.utils.assertions.check_less(
            labels, num_classes_int64, message="labels out of bound"
        )
        startai.utils.assertions.check_less(
            predictions, num_classes_int64, message="predictions out of bound"
        )

    if weights is not None:
        weights = startai.array(weights)
        startai.utils.assertions.check_equal(
            startai.shape(predictions),
            startai.shape(weights),
            message="weights shape do not match predictions",
            as_array=False,
        )
        weights = startai.astype(weights, dtype, copy=False)

    shape = startai.stack([num_classes, num_classes])
    indices = startai.stack([labels, predictions], axis=1)
    values = startai.ones_like(predictions, dtype=dtype) if weights is None else weights
    return startai.scatter_nd(indices, values, shape=shape)


@to_startai_arrays_and_back
def conj(x, name=None):
    return startai.conj(x)


@to_startai_arrays_and_back
def cos(x, name=None):
    return startai.cos(x)


@to_startai_arrays_and_back
def cosh(x, name=None):
    return startai.cosh(x)


@handle_tf_dtype
@to_startai_arrays_and_back
def count_nonzero(input, axis=None, keepdims=None, dtype=startai.int64, name=None):
    x = startai.array(input)
    if keepdims is None:
        keepdims = False
    zero = startai.zeros(startai.shape(x), dtype=x.dtype)
    return startai.astype(
        startai.sum(
            startai.astype(startai.not_equal(x, zero), startai.int64),
            axis=axis,
            keepdims=keepdims,
        ),
        dtype,
        copy=False,
    )


@to_startai_arrays_and_back
def cumprod(x, axis, exclusive=False, reverse=False, name=None):
    return startai.astype(
        startai.cumprod(x, axis=axis, exclusive=exclusive, reverse=reverse), x.dtype
    )


@to_startai_arrays_and_back
def cumsum(x, axis, exclusive=False, reverse=False, name=None):
    return startai.astype(
        startai.cumsum(x, axis=axis, exclusive=exclusive, reverse=reverse), x.dtype
    )


@to_startai_arrays_and_back
def digamma(x, name=None):
    return startai.digamma(x)


@to_startai_arrays_and_back
def divide(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.divide(x, y)


@to_startai_arrays_and_back
def divide_no_nan(x, y, name="divide_no_nan"):
    x, y = check_tensorflow_casting(x, y)
    return startai.where(
        y == 0,
        startai.array(0.0, dtype=startai.promote_types(x.dtype, y.dtype)),
        x / y,
    )


@to_startai_arrays_and_back
def equal(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.equal(x, y)


@to_startai_arrays_and_back
def erfcinv(x, name="erfcinv"):
    return 1 / (1 - startai.erf(x))


@to_startai_arrays_and_back
def exp(x, name=None):
    return startai.exp(x)


@to_startai_arrays_and_back
def expm1(x, name=None):
    return startai.expm1(x)


@to_startai_arrays_and_back
def floor(x, name=None):
    return startai.floor(x)


@to_startai_arrays_and_back
def floordiv(x, y, name=None):
    return startai.floor_divide(x, y)


@to_startai_arrays_and_back
def floormod(x, y, name=None):
    return startai.remainder(x, y)


@to_startai_arrays_and_back
def greater(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.greater(x, y)


@with_unsupported_dtypes(
    {"2.15.0 and below": ("complex64", "complex128")}, "tensorflow"
)
@to_startai_arrays_and_back
def greater_equal(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.greater_equal(x, y)


@with_supported_device_and_dtypes(
    {
        "2.15.0 and below": {
            "cpu": ("float32", "float64"),
            "gpu": ("bfloat16", "float16", "float32", "float64"),
        }
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def igamma(a, x, name=None):
    return startai.igamma(a, x=x)


@with_supported_dtypes(
    {"2.15.0 and below": ("float16", "float32", "float64", "complex64", "complex128")},
    "tensorflow",
)
@to_startai_arrays_and_back
def imag(input, name=None):
    return startai.imag(input)


@to_startai_arrays_and_back
def in_top_k(target, pred, k, name=None):
    top_k = startai.top_k(target, k)
    return startai.array([val in top_k.values for val in target])


@with_supported_dtypes(
    {
        "2.15.0 and below": ("int32", "int64"),
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def invert_permutation(x, name=None):
    return startai.invert_permutation(x)


@with_supported_dtypes(
    {
        "2.15.0 and below": ("bfloat16", "half", "float32", "float64"),
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def is_finite(x, name=None):
    return startai.isfinite(x)


@to_startai_arrays_and_back
def is_inf(x, name=None):
    return startai.isinf(x)


@to_startai_arrays_and_back
def is_nan(x, name=None):
    return startai.isnan(x)


@to_startai_arrays_and_back
def is_non_decreasing(x, name="is_non_decreasing"):
    if startai.array(x).size < 2:
        return startai.array(True)
    if startai.array(x).size == 2:
        return startai.array([x[0] <= x[1]])
    return startai.all(startai.less_equal(x, startai.roll(x, -1)))


@to_startai_arrays_and_back
def is_strictly_increasing(x, name="is_strictly_increasing"):
    if startai.array(x).size < 2:
        return startai.array(True)
    x = startai.flatten(x)
    res = startai.less(x, startai.roll(x, -1))
    if res.size >= 2:
        res[res.size - 1] = True  # The last comparison must be set to true.
    return startai.all(res)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.15.0 and below": ("float32", "float64")}, "tensorflow")
def l2_normalize(x, axis=None, epsilon=1e-12, name=None):
    square_sum = startai.sum(startai.square(x), axis=axis, keepdims=True)
    x_inv_norm = startai.reciprocal(startai.sqrt(startai.maximum(square_sum, epsilon)))
    return startai.multiply(x, x_inv_norm)


@to_startai_arrays_and_back
@with_unsupported_dtypes(
    {"2.15.0 and below": ("complex64", "complex128")}, "tensorflow"
)
def less(x, y, name="None"):
    x, y = check_tensorflow_casting(x, y)
    return startai.less(x, y)


@to_startai_arrays_and_back
def less_equal(x, y, name="LessEqual"):
    x, y = check_tensorflow_casting(x, y)
    return startai.less_equal(x, y)


# lgamma
@to_startai_arrays_and_back
@with_supported_dtypes({"2.15.0 and below": ("float32", "float64")}, "tensorflow")
def lgamma(x, name=None):
    return startai.lgamma(x)


@to_startai_arrays_and_back
def log(x, name=None):
    return startai.log(x)


@to_startai_arrays_and_back
def log1p(x, name=None):
    return startai.log1p(x)


@to_startai_arrays_and_back
def log_sigmoid(x, name=None):
    return -startai.softplus(-x)


@to_startai_arrays_and_back
def log_softmax(logits, axis=None):
    if axis is None:
        axis = -1
    return startai.log_softmax(logits, axis=axis)


@to_startai_arrays_and_back
def logical_and(x, y, name="LogicalAnd"):
    return startai.logical_and(x, y)


@to_startai_arrays_and_back
def logical_not(x, name="logical_not"):
    return startai.logical_not(x)


@to_startai_arrays_and_back
def logical_or(x, y, name="logical_or"):
    return startai.logical_or(x, y)


@to_startai_arrays_and_back
def logical_xor(x, y, name="LogicalXor"):
    return startai.logical_xor(x, y)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.15.0 and below": ("complex",)}, "tensorflow")
def maximum(x, y, name=None):
    return startai.maximum(x, y)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.15.0 and below": ("complex",)}, "tensorflow")
def minimum(x, y, name=None):
    return startai.minimum(x, y)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.6.0 and below": ("bfloat16",)}, "paddle")
def mod(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.remainder(x, y)


@to_startai_arrays_and_back
def multiply(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.multiply(x, y)


@to_startai_arrays_and_back
def multiply_no_nan(x, y, name="multiply_no_nan"):
    x, y = check_tensorflow_casting(x, y)
    return startai.where(
        y == 0,
        startai.array(0.0, dtype=startai.promote_types(x.dtype, y.dtype)),
        x * y,
    )


@to_startai_arrays_and_back
def negative(x, name=None):
    return startai.negative(x)


@to_startai_arrays_and_back
def nextafter(x1, x2, name=None):
    return startai.nextafter(x1, x2)


@to_startai_arrays_and_back
def not_equal(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.not_equal(x, y)


@to_startai_arrays_and_back
def polyval(coeffs, x, name=None):
    startai.utils.assertions.check_isinstance(coeffs, list)
    x = startai.array(x)
    if len(coeffs) < 1:
        return startai.zeros_like(x, dtype=x.dtype)
    coeffs = [startai.array(_) for _ in coeffs]
    p = coeffs[0]
    for c in coeffs[1:]:
        p = c + p * x
    return p


@to_startai_arrays_and_back
def pow(x, y, name="pow"):
    x, y = check_tensorflow_casting(x, y)
    return startai.pow(x, y)


@to_startai_arrays_and_back
def real(input, name=None):
    return startai.real(input)


@to_startai_arrays_and_back
def reciprocal(x, name="reciprocal"):
    return startai.reciprocal(x)


@to_startai_arrays_and_back
def reciprocal_no_nan(x, name="reciprocal_no_nan"):
    return startai.where(
        x == 0,
        startai.array(0.0, dtype=x.dtype),
        startai.ones_like(x, dtype=x.dtype) / x,
    )


@to_startai_arrays_and_back
def reduce_all(input_tensor, axis=None, keepdims=False, name="reduce_all"):
    return startai.all(input_tensor, axis=axis, keepdims=keepdims)


@to_startai_arrays_and_back
def reduce_any(input_tensor, axis=None, keepdims=False, name="reduce_any"):
    return startai.any(input_tensor, axis=axis, keepdims=keepdims)


@to_startai_arrays_and_back
def reduce_euclidean_norm(
    input_tensor, axis=None, keepdims=False, name="reduce_euclidean_norm"
):
    return startai.vector_norm(
        input_tensor, axis=axis, keepdims=keepdims, ord=2
    )  # ord = '2' is the euclidean norm


@to_startai_arrays_and_back
def reduce_logsumexp(input_tensor, axis=None, keepdims=False, name="reduce_logsumexp"):
    # stable logsumexp trick
    max_input_tensor = startai.max(input_tensor, axis=axis, keepdims=False)
    return (
        startai.log(
            startai.sum(
                startai.exp(input_tensor - max_input_tensor),
                axis=axis,
                keepdims=keepdims,
            )
        )
        + max_input_tensor
    ).astype(input_tensor.dtype)


@to_startai_arrays_and_back
def reduce_max(input_tensor, axis=None, keepdims=False, name="reduce_max"):
    return startai.max(input_tensor, axis=axis, keepdims=keepdims)


@to_startai_arrays_and_back
def reduce_mean(input_tensor, axis=None, keepdims=False, name="reduce_mean"):
    if startai.exists(axis):
        axis = startai.to_list(axis)
    return startai.mean(input_tensor, axis=axis, keepdims=keepdims)


@to_startai_arrays_and_back
def reduce_min(input_tensor, axis=None, keepdims=False, name="reduce_min"):
    return startai.min(input_tensor, axis=axis, keepdims=keepdims)


@to_startai_arrays_and_back
def reduce_prod(input_tensor, axis=None, keepdims=False, name="reduce_prod"):
    return startai.prod(input_tensor, axis=axis, keepdims=keepdims).astype(
        input_tensor.dtype
    )


@to_startai_arrays_and_back
def reduce_std(input_tensor, axis=None, keepdims=False, name="reduce_std"):
    return startai.std(input_tensor, axis=axis, keepdims=keepdims)


@to_startai_arrays_and_back
def reduce_sum(input_tensor, axis=None, keepdims=False, name="reduce_sum"):
    input_tensor = startai.array(input_tensor)
    return startai.sum(input_tensor, axis=axis, keepdims=keepdims).astype(
        input_tensor.dtype
    )


@to_startai_arrays_and_back
def reduce_variance(input_tensor, axis=None, keepdims=False, name="reduce_variance"):
    return startai.var(input_tensor, axis=axis, keepdims=keepdims)


@with_supported_device_and_dtypes(
    {
        "2.15.0 and below": {
            "cpu": ("float32", "float64"),
            "gpu": ("bfloat16", "float16", "float32", "float64"),
        }
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def rint(x, name=None):
    return startai.round(x)


@to_startai_arrays_and_back
def round(x, name=None):
    return startai.round(x)


@to_startai_arrays_and_back
def rsqrt(x, name=None):
    return startai.reciprocal(startai.sqrt(x))


@to_startai_arrays_and_back
def scalar_mul(scalar, x, name="scalar_mul"):
    scalar, x = check_tensorflow_casting(scalar, x)
    return startai.multiply(x, scalar).astype(x.dtype)


@with_unsupported_dtypes(
    {"2.15.0 and below": ("float16", "bool", "int16", "int8")},
    "tensorflow",
)
@to_startai_arrays_and_back
def segment_sum(data, segment_ids, name="segment_sum"):
    data = startai.array(data)
    segment_ids = startai.array(segment_ids)
    startai.utils.assertions.check_equal(
        list(segment_ids.shape), [list(data.shape)[0]], as_array=False
    )
    sum_array = startai.zeros(
        tuple([int(segment_ids[-1] + 1)] + (list(data.shape))[1:]), dtype=data.dtype
    )
    for i in range((segment_ids).shape[0]):
        sum_array[segment_ids[i]] = sum_array[segment_ids[i]] + data[i]
    return sum_array


@to_startai_arrays_and_back
def sigmoid(x, name=None):
    return startai.sigmoid(x)


@with_supported_dtypes(
    {
        "2.15.0 and below": (
            "bfloat16",
            "float16",
            "float32",
            "float64",
            "complex64",
            "complex128",
        )
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def sin(x, name=None):
    return startai.sin(x)


@to_startai_arrays_and_back
def sinh(x, name=None):
    return startai.sinh(x)


@to_startai_arrays_and_back
def softmax(logits, axis=None, name=None):
    return startai.softmax(logits, axis=axis)


@to_startai_arrays_and_back
def softplus(features, name=None):
    return startai.softplus(features)


@with_supported_dtypes(
    {"2.15.0 and below": ("bfloat32", "float32", "float64")}, "tensorflow"
)
@to_startai_arrays_and_back
def softsign(features, name=None):
    return startai.divide(features, startai.abs(features) + 1)


@to_startai_arrays_and_back
def sqrt(x, name=None):
    return startai.sqrt(x)


@to_startai_arrays_and_back
def square(x, name=None):
    return startai.square(x)


@with_supported_dtypes(
    {
        "2.15.0 and below": (
            "bfloat16",
            "float16",
            "float32",
            "float64",
            "int32",
            "int64",
            "complex64",
            "complex128",
        )
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def squared_difference(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    res = startai.square(startai.subtract(x, y))
    if isinstance(res, complex):
        res = res.real - res.imag * 1j  # Changing the sign of the imaginary part
        return res
    return res


@to_startai_arrays_and_back
def subtract(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return startai.subtract(x, y)


@to_startai_arrays_and_back
def tan(x, name=None):
    return startai.tan(x)


@with_supported_dtypes(
    {"2.15.0 and below": ("float16", "float32", "float64", "complex64", "complex128")},
    "tensorflow",
)
@to_startai_arrays_and_back
def tanh(x, name=None):
    return startai.tanh(x)


@to_startai_arrays_and_back
def top_k(input, k=1, sorted=True, name=None):
    return startai.top_k(input, k, sorted=sorted)


@to_startai_arrays_and_back
def truediv(x, y, name="truediv"):
    x, y = check_tensorflow_casting(x, y)
    x_dtype = startai.dtype(x)
    if x_dtype in ["int8", "uint8", "int16", "uint16"]:
        return startai.divide(startai.astype(x, startai.float32), startai.astype(y, startai.float32))
    elif x_dtype in ["int32", "uint32", "int64", "uint64"]:
        return startai.divide(startai.astype(x, startai.float64), startai.astype(y, startai.float64))
    return startai.divide(x, y)


@to_startai_arrays_and_back
def unsorted_segment_mean(
    data, segment_ids, num_segments, name="unsorted_segment_mean"
):
    startai.utils.assertions.check_equal(
        list(segment_ids.shape), [list(data.shape)[0]], as_array=False
    )
    x = startai.zeros(tuple([num_segments] + (list(data.shape))[1:]))
    count = startai.zeros((num_segments,))
    for i in range((segment_ids).shape[0]):
        x[segment_ids[i]] = x[segment_ids[i]] + data[i]
        count[segment_ids[i]] += 1
    for j in range(num_segments):
        x[j] = startai.divide(x[j], count[j])
    return x


@to_startai_arrays_and_back
def unsorted_segment_min(data, segment_ids, num_segments, name="unsorted_segment_min"):
    data = startai.array(data)
    segment_ids = startai.array(segment_ids)

    startai.utils.assertions.check_equal(
        list(segment_ids.shape), [list(data.shape)[0]], as_array=False
    )
    min_array = startai.zeros(
        tuple([num_segments.item()] + (list(data.shape))[1:]), dtype=startai.int32
    )
    for i in range((segment_ids).shape[0]):
        min_array[segment_ids[i]] = startai.minimum(min_array[segment_ids[i]], data[i])
    return min_array


@to_startai_arrays_and_back
def unsorted_segment_sqrt_n(
    data, segment_ids, num_segments, name="unsorted_segement_sqrt_n"
):
    startai.utils.assertions.check_equal(
        list(segment_ids.shape), [list(data.shape)[0]], as_array=False
    )
    x = startai.zeros(tuple([num_segments] + (list(data.shape))[1:]))
    count = startai.zeros((num_segments,))
    for i in range((segment_ids).shape[0]):
        x[segment_ids[i]] = x[segment_ids[i]] + data[i]
        count[segment_ids[i]] += 1
    for j in range(num_segments):
        x[j] = startai.divide(x[j], startai.sqrt(count[j]))
    return x


@to_startai_arrays_and_back
def unsorted_segment_sum(data, segment_ids, num_segments, name="unsorted_segment_sum"):
    data = startai.array(data)
    segment_ids = startai.array(segment_ids)
    startai.utils.assertions.check_equal(
        list(segment_ids.shape), [list(data.shape)[0]], as_array=False
    )
    sum_array = startai.zeros(
        tuple([num_segments.item()] + (list(data.shape))[1:]), dtype=startai.int32
    )
    for i in range((segment_ids).shape[0]):
        sum_array[segment_ids[i]] = sum_array[segment_ids[i]] + data[i]
    return sum_array


@with_supported_dtypes(
    {"2.15.0 and below": ("float32", "float64", "complex64", "complex128")},
    "tensorflow",
)
@to_startai_arrays_and_back
def xdstartai(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    if (x == 0).all():
        return 0.0
    return startai.divide(x, y)


@to_startai_arrays_and_back
@with_supported_dtypes({"2.15.0 and below": ("float32", "float64")}, "tensorflow")
def xlog1py(x, y, name=None):
    x, y = check_tensorflow_casting(x, y)
    return x * startai.log1p(y)


@to_startai_arrays_and_back
def xlogy(x, y, name=None):
    return startai.xlogy(x, y)


@to_startai_arrays_and_back
def zero_fraction(value, name="zero_fraction"):
    zero = startai.zeros(tuple(value.shape), dtype=startai.float32)
    x = startai.array(value, dtype=startai.float32)
    count_zero = startai.sum(startai.equal(x, zero), dtype=startai.float32)
    count_nonzero = startai.sum(startai.not_equal(x, zero), dtype=startai.float32)
    return startai.divide(count_zero, startai.add(count_zero, count_nonzero))


@to_startai_arrays_and_back
@with_supported_dtypes(
    {
        "2.15.0 and below": ("float32", "float64"),
    },
    "tensorflow",
)
def zeta(x, q, name=None):
    return startai.zeta(x, q)
