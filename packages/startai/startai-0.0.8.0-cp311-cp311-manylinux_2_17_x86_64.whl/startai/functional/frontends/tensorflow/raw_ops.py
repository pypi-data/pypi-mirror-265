# global
import startai
import startai.functional.frontends.tensorflow as tf_frontend
from startai.functional.frontends.tensorflow import check_tensorflow_casting
from startai.functional.frontends.tensorflow.func_wrapper import (
    to_startai_arrays_and_back,
    map_raw_ops_alias,
    to_startai_dtype,
)

from startai.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
from startai.utils.exceptions import StartaiNotImplementedException


Acos = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.acos))
Acosh = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.acosh))
Add = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.add))
AddN = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.add_n))
AddV2 = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.add))
ArgMax = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {"2.15.0 and below": ("complex",)},
        "tensorflow",
    )(
        map_raw_ops_alias(
            tf_frontend.math.argmax, kwargs_to_update={"dimension": "axis"}
        )
    )
)
ArgMin = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {"2.15.0 and below": ("complex",)},
        "tensorflow",
    )(
        map_raw_ops_alias(
            tf_frontend.math.argmin, kwargs_to_update={"dimension": "axis"}
        )
    )
)
Asin = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.asin))
Atan = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.atan))
Atan2 = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {"2.15.0 and below": "float16"},
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.math.atan2))
)
ConcatV2 = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.concat))
Conj = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.13.0 and below": ("complex64", "complex128", "variant"),
        },
        "tensorflow",
    )(
        map_raw_ops_alias(
            tf_frontend.math.conj,
            kwargs_to_update={
                "input": "x",
            },
        )
    )
)
Cos = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.cos))
Cosh = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.cosh))
Cumprod = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.cumprod))
Cumsum = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.cumsum))
Digamma = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.digamma))
Div = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.divide))
Einsum = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.15.0 and below": (
                "bfloat16",
                "complex128 ",
                "complex64",
                "float64",
                "float32",
                "float16",
                "int64",
                "int32",
            ),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.general_functions.einsum))
)
Identity = to_startai_arrays_and_back(
    map_raw_ops_alias(tf_frontend.general_functions.identity)
)
IdentityN = to_startai_arrays_and_back(
    map_raw_ops_alias(tf_frontend.general_functions.identity_n)
)
Igamma = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.15.0 and below": (
                "float64",
                "float32",
                "half",
            ),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.math.igamma))
)
LeakyRelu = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.15.0 and below": ("bfloat16", "float16", "float32", "float64"),
        },
        "tensorflow",
    )(
        map_raw_ops_alias(
            tf_frontend.nn.leaky_relu,
        )
    )
)
LessEqual = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {
            "2.15.0 and below": ("complex",),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.math.less_equal))
)
Log1p = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.log1p))
LogSoftmax = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.15.0 and below": (
                "bfloat16",
                "float32",
                "float64",
            ),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.math.log_softmax))
)
LogicalOr = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.logical_or))
MatrixDeterminant = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.linalg.det))
Max = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {
            "2.15.0 and below": ("complex",),
        },
        "tensorflow",
    )(
        map_raw_ops_alias(
            tf_frontend.math.reduce_max,
            kwargs_to_update={
                "input": "input_tensor",
                "keep_dims": "keepdims",
            },
        )
    )
)
MaxPool3D = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.15.0 and below": ("float32",),
        },
        "tensorflow",
    )(
        map_raw_ops_alias(
            tf_frontend.nn.max_pool3d,
        )
    )
)
Maximum = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {
            "2.15.0 and below": ("complex",),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.math.maximum))
)
Mean = to_startai_arrays_and_back(
    map_raw_ops_alias(
        tf_frontend.math.reduce_mean,
        kwargs_to_update={
            "input": "input_tensor",
            "keep_dims": "keepdims",
        },
    )
)
Min = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {
            "2.15.0 and below": ("complex",),
        },
        "tensorflow",
    )(
        map_raw_ops_alias(
            tf_frontend.math.reduce_min,
            kwargs_to_update={
                "input": "input_tensor",
                "keep_dims": "keepdims",
            },
        )
    )
)
Mod = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.mod))
Mul = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.multiply))
Neg = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.negative))
Pow = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.pow))
RealDiv = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.15.0 and below": (
                "complex",
                "bfloat16",
                "float16",
                "float64",
                "float32",
            ),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.general_functions.realdiv))
)
Reciprocal = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.reciprocal))
Relu = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {
            "2.15.0 and below": ("complex", "float16"),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.nn.relu))
)
Relu6 = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {
            "2.15.0 and below": ("complex", "float16"),
        },
        "tensorflow",
    )(
        map_raw_ops_alias(
            tf_frontend.nn.relu6,
        )
    )
)
Reshape = to_startai_arrays_and_back(
    map_raw_ops_alias(tf_frontend.general_functions.reshape)
)
Roll = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.roll))
ShapeN = to_startai_arrays_and_back(
    map_raw_ops_alias(tf_frontend.general_functions.shape_n)
)
Sigmoid = to_startai_arrays_and_back(
    map_raw_ops_alias(tf_frontend.keras.activations.sigmoid)
)
Sin = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.sin))
Size = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.general_functions.size))
Slice = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.slice))
Softmax = to_startai_arrays_and_back(
    with_unsupported_dtypes(
        {
            "2.15.0 and below": ("float16",),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.nn.softmax))
)
Split = to_startai_arrays_and_back(
    map_raw_ops_alias(
        tf_frontend.split, kwargs_to_update={"num_split": "num_or_size_splits"}
    )
)
SquaredDifference = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.15.0 and below": (
                "complex",
                "bfloat16",
                "float16",
                "float64",
                "float32",
                "int32",
                "int64",
            ),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.math.squared_difference))
)
Squeeze = to_startai_arrays_and_back(
    map_raw_ops_alias(tf_frontend.general_functions.squeeze)
)
Sub = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.subtract))
Tan = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.tan))
Tanh = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.tanh))
Tile = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.general_functions.tile))
Xlogy = to_startai_arrays_and_back(map_raw_ops_alias(tf_frontend.math.xlogy))
Zeta = to_startai_arrays_and_back(
    with_supported_dtypes(
        {
            "2.15.0 and below": ("float32", "float64"),
        },
        "tensorflow",
    )(map_raw_ops_alias(tf_frontend.math.zeta))
)


# --- Helpers --- #
# --------------- #


def _tf_to_startai_startai_arguments_for_conv(
    padding, ex_pading, strides, dilations, data_format
):
    if data_format.find("C") == 1:
        strides = strides[2:]
        dilations = dilations[2:]
        data_format = "channel_first"
        pad_index = [4, 8]
    else:
        strides = strides[1:-1]
        dilations = dilations[1:-1]
        data_format = "channel_last"
        pad_index = [2, 6]
    if padding == "EXPLICIT":
        padding = [
            (ex_pading[i], ex_pading[i + 1])
            for i in range(pad_index[0], pad_index[1], 2)
        ]
    return padding, strides, dilations, data_format


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def AccumulateNV2(inputs, shape, name="AccumulateNV2"):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def Angle(
    *,
    input,
    Tout=startai.float32,
    name="Angle",
):
    Tout = startai.as_startai_dtype(Tout) if Tout is not None else startai.float32
    return startai.astype(startai.angle(input), Tout)


@with_unsupported_dtypes(
    {
        "2.15.0 and below": (
            "float16",
            "bool",
            "bfloat16",
        )
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def ApproximateEqual(
    *,
    x,
    y,
    tolerance=1e-05,
    name="ApproximateEqual",
):
    x, y = check_tensorflow_casting(x, y)
    return startai.abs(x - y) < tolerance


@to_startai_arrays_and_back
def Atanh(*, x, name="Atanh"):
    return startai.atanh(x)


@to_startai_arrays_and_back
def BandedTriangularSolve(
    matrix,
    rhs,
    lower=True,
    adjoint=False,
    name="BandedTriangularSolve",
):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def BatchMatMul(x, y, adj_x=False, adj_y=False, name="BatchMatMul"):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def BatchMatMulV2(x, y, adj_x=False, adj_y=False, name="BatchMatMulV2"):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def BatchMatMulV3(x, y, Tout=startai.Dtype, adj_x=False, adj_y=False, name="BatchMatMulV3"):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def BitwiseAnd(*, x, y, name="BitwiseAnd"):
    x, y = check_tensorflow_casting(x, y)
    return startai.bitwise_and(x, y)


@to_startai_arrays_and_back
def BitwiseOr(*, x, y, name="BitwiseOr"):
    x, y = check_tensorflow_casting(x, y)
    return startai.bitwise_or(x, y)


@to_startai_arrays_and_back
def BitwiseXor(*, x, y, name="BitwiseXor"):
    x, y = check_tensorflow_casting(x, y)
    return startai.bitwise_xor(x, y)


@to_startai_arrays_and_back
def BroadcastTo(*, input, shape, name="BroadcastTo"):
    return startai.broadcast_to(input, shape=shape)


@to_startai_arrays_and_back
def Ceil(*, x, name=None):
    return startai.ceil(x)


@to_startai_arrays_and_back
def Cholesky(*, input, name="Cholesky"):
    return startai.astype(startai.cholesky(input), input.dtype)


@to_startai_arrays_and_back
def Complex(real, imag, Tout=startai.complex64, name="Complex"):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def Concat(*, concat_dim, values, name="Concat"):
    return startai.concat(values, axis=concat_dim)


@to_startai_arrays_and_back
def Conv2D(
    *,
    input,
    filter,
    strides,
    padding,
    use_cudnn_on_gpu,
    explicit_paddings,
    data_format="NHWC",
    dilations=[1, 1, 1, 1],
    name="Conv2D",
):
    padding, strides, dilations, data_format = _tf_to_startai_startai_arguments_for_conv(
        padding, explicit_paddings, strides, dilations, data_format
    )
    return startai.conv_general_dilated(
        input,
        filter,
        strides,
        padding,
        data_format=data_format,
        dilations=dilations,
        dims=2,
    )


@to_startai_arrays_and_back
def Conv3D(
    *,
    input,
    filter,
    strides,
    padding,
    data_format="NDHWC",
    dilations=[1, 1, 1, 1, 1],
    name="Conv3D",
):
    # startai.backends.tensorflow expects strides and dilations to be
    # a single integer value or a list of 3 values whereas the raw op
    # expects a list of 5 values
    if data_format == "NDHWC":
        strides = strides[1:-1]
        dilations = dilations[1:-1]
    elif data_format == "NCDHW":
        strides = strides[2:]
        dilations = dilations[2:]

    return tf_frontend.nn.conv3d(
        input,
        filter,
        strides,
        padding,
        data_format=data_format,
        dilations=dilations,
        name=name,
    )


@to_startai_arrays_and_back
def Cross(*, a, b, name="Cross"):
    a, b = check_tensorflow_casting(a, b)
    return startai.cross(a, b)


@to_startai_arrays_and_back
def CumulativeLogsumexp(
    x, axis, exclusive=False, reverse=False, name="CumulativeLogsumexp"
):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def DebugGradientIdentity(input, name="DebugGradientIdentity"):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def Diag(*, diagonal, name="Diag"):
    return startai.astype(startai.diag(diagonal), diagonal.dtype)


@with_supported_dtypes(
    {"2.15.0 and below": ("bfloat16", "float16", "float32", "float64")},
    "tensorflow",
)
@to_startai_arrays_and_back
def Elu(features, name=None):
    zeros = startai.zeros_like(features, dtype=startai.dtype(features))
    ones = startai.ones_like(features, dtype=startai.dtype(features))
    ret_val = startai.where(
        # if x > 0 => x; else e^x - 1
        features > zeros,
        features,
        startai.subtract(startai.exp(features), ones),
    )
    return ret_val


@to_startai_arrays_and_back
def Equal(*, x, y, incompatible_shape_error=True, name="Equal"):
    x, y = check_tensorflow_casting(x, y)
    if incompatible_shape_error:
        return startai.equal(x, y)

    try:
        return startai.equal(x, y)
    except (startai.utils.exceptions.StartaiError, startai.utils.exceptions.StartaiBackendException):
        return startai.array(False)


@to_startai_arrays_and_back
def EuclideanNorm(*, input, axis, keep_dims=False, name="EuclideanNorm"):
    return startai.astype(
        startai.vector_norm(input, axis=axis, keepdims=keep_dims), input.dtype
    )


@to_startai_arrays_and_back
def Exp(*, x, name="Exp"):
    return startai.exp(x)


@to_startai_arrays_and_back
def Expm1(*, x, name="Expm1"):
    return startai.expm1(x)


@to_startai_arrays_and_back
def FFT(*, input, name="FFT"):
    return startai.astype(startai.fft(input, -1), input.dtype)


@to_startai_arrays_and_back
def FFT2D(*, input, name="FFT2D"):
    return startai.astype(startai.fft2(input, dim=(-2, -1)), input.dtype)


@to_startai_arrays_and_back
def FFT3D(*, input, name="FFT3D"):
    fft_result = startai.fft(input, -1)
    fft_result = startai.fft(fft_result, -2)
    fft_result = startai.fft(fft_result, -3)
    return startai.astype(fft_result, input.dtype)


@to_startai_arrays_and_back
def Fill(*, dims, value, name="Full"):
    return startai.full(dims, value)


@to_startai_arrays_and_back
def Floor(*, x, name="Floor"):
    return startai.floor(x)


@to_startai_arrays_and_back
def FloorDiv(*, x, y, name="FloorDiv"):
    x, y = check_tensorflow_casting(x, y)
    return startai.floor_divide(x, y)


@to_startai_arrays_and_back
def FloorMod(*, x, y, name="FloorMod"):
    x, y = check_tensorflow_casting(x, y)
    return startai.remainder(x, y)


@to_startai_arrays_and_back
def Gather(*, params, indices, validate_indices=None, name="Gather"):
    return startai.gather(params, indices, axis=0, batch_dims=0)


@with_supported_dtypes(
    {"2.15.0 and below": ("int32", "int64", "float32", "float64")},
    "tensorflow",
)
@to_startai_arrays_and_back
def GatherNd(*, params, indices, name=None):
    return startai.gather_nd(params, indices, batch_dims=0)


@to_startai_arrays_and_back
def Greater(*, x, y, name="Greater"):
    x, y = check_tensorflow_casting(x, y)
    return startai.greater(x, y)


@to_startai_arrays_and_back
def GreaterEqual(*, x, y, name="GreaterEqual"):
    x, y = check_tensorflow_casting(x, y)
    return startai.greater_equal(x, y)


@to_startai_arrays_and_back
def Imag(
    *,
    input,
    Tout=startai.float32,
    name="Imag",
):
    Tout = startai.as_startai_dtype(Tout) if Tout is not None else startai.float32
    return startai.astype(startai.imag(input), Tout)


@to_startai_arrays_and_back
def Inv(*, x, name="Inv"):
    return startai.astype(startai.reciprocal(x), x.dtype)


@to_startai_arrays_and_back
def InvGrad(*, y, dy, name="InvGrad"):
    return startai.multiply(startai.negative(dy), startai.multiply(y, y))


@to_startai_arrays_and_back
def Invert(*, x, name="Invert"):
    return startai.bitwise_invert(x)


@to_startai_arrays_and_back
def LeftShift(*, x, y, name="LeftShift"):
    return startai.bitwise_left_shift(x, y)


@to_startai_arrays_and_back
def Less(*, x, y, name="Less"):
    x, y = check_tensorflow_casting(x, y)
    return startai.less(x, y)


@to_startai_arrays_and_back
def LinSpace(*, start, stop, num, name=None):
    return startai.linspace(start, stop, num)


@to_startai_arrays_and_back
def Log(*, x, name="Log"):
    return startai.log(x)


@to_startai_arrays_and_back
def LogicalNot(*, x, name="LogicalNot"):
    return startai.logical_not(x)


@to_startai_arrays_and_back
def MatMul(*, a, b, transpose_a=False, transpose_b=False, name="MatMul"):
    a, b = check_tensorflow_casting(a, b)
    return startai.matmul(a, b, transpose_a=transpose_a, transpose_b=transpose_b)


@to_startai_arrays_and_back
def MatrixInverse(*, input, adjoint=False, name="MatrixInverse"):
    return startai.inv(input, adjoint=adjoint)


@to_startai_arrays_and_back
def Minimum(*, x, y, name="Minimum"):
    return startai.minimum(x, y)


@to_startai_arrays_and_back
def NotEqual(*, x, y, incompatible_shape_error=True, name="NotEqual"):
    x, y = check_tensorflow_casting(x, y)
    if incompatible_shape_error:
        return startai.not_equal(x, y)

    try:
        return startai.not_equal(x, y)
    except (startai.utils.exceptions.StartaiError, startai.utils.exceptions.StartaiBackendException):
        return startai.array(True)


@to_startai_arrays_and_back
def NthElement(*, input, n, reverse=False, name="NthElement"):
    return startai.astype(startai.sort(input, descending=reverse)[..., n], input.dtype)


@to_startai_arrays_and_back
def OnesLike(*, x, name="OnesLike"):
    return startai.ones_like(x)


@to_startai_arrays_and_back
def Pack(*, values, axis=0, name="Pack"):
    return startai.stack(values, axis=axis)


@to_startai_arrays_and_back
def Pad(*, input, paddings, name="Pad"):
    return startai.constant_pad(input, paddings.to_list())


@to_startai_arrays_and_back
def PadV2(*, input, paddings, constant_values, name="PadV2"):
    return startai.constant_pad(input, paddings.to_list(), value=constant_values)


@to_startai_arrays_and_back
def Prod(*, input, axis, keep_dims=False, name="Prod"):
    return startai.astype(startai.prod(input, axis=axis, keepdims=keep_dims), input.dtype)


@to_startai_arrays_and_back
def Real(input, Tout=startai.float32, name="Real"):
    # TODO
    raise StartaiNotImplementedException


@to_startai_arrays_and_back
def Reverse(*, tensor, dims, name="Reverse"):
    ret = tensor
    for dim in enumerate(dims):
        if dim[1]:
            ret = startai.flip(ret, axis=dim[0])
    return ret


@to_startai_arrays_and_back
def RightShift(*, x, y, name="RightShift"):
    return startai.bitwise_right_shift(x, y)


@to_startai_arrays_and_back
def Round(*, x, name="Round"):
    return startai.round(x)


@to_startai_arrays_and_back
def Rsqrt(*, x, name="Rsqrt"):
    return startai.sqrt(startai.reciprocal(x))


@to_startai_arrays_and_back
def Shape(*, input, output_type=startai.int32, name="Shape"):
    output_type = to_startai_dtype(output_type)
    return startai.astype(startai.shape(input, as_array=True), output_type, copy=False)


@with_unsupported_dtypes(
    {"2.15.0 and below": ("unsigned",)},
    "tensorflow",
)
@to_startai_arrays_and_back
def Sign(*, x, name="Sign"):
    return startai.sign(x, np_variant=False)


@to_startai_arrays_and_back
def Sinh(*, x, name="Sinh"):
    return startai.sinh(x)


@to_startai_arrays_and_back
def Softplus(*, features, name="Softplus"):
    return startai.softplus(features)


# Softsign
@to_startai_arrays_and_back
def Softsign(*, features, name="Softsign"):
    return startai.softsign(features)


@to_startai_arrays_and_back
def SplitV(*, value, size_splits, axis, num_split, name="SplitV"):
    return startai.split(value, num_or_size_splits=size_splits, axis=axis)


@to_startai_arrays_and_back
def Sqrt(*, x, name="Sqrt"):
    return startai.sqrt(x)


@to_startai_arrays_and_back
def Square(*, x, name="Square"):
    return startai.square(x)


@to_startai_arrays_and_back
def Sum(*, input, axis, keep_dims=False, name="Sum"):
    return startai.astype(startai.sum(input, axis=axis, keepdims=keep_dims), input.dtype)


@with_supported_dtypes(
    {"2.15.0 and below": ("float64", "float128", "halfcomplex64", "complex128")},
    "tensorflow",
)
@to_startai_arrays_and_back
def Svd(*, input, full_matrices=False, compute_uv=True, name=None):
    return startai.svd(input, compute_uv=compute_uv, full_matrices=full_matrices)


@to_startai_arrays_and_back
def TanhGrad(*, y, dy, name="TanhGrad"):
    return startai.multiply(dy, startai.subtract(1, startai.multiply(y, y)))


@to_startai_arrays_and_back
def Transpose(*, x, perm, name="Transpose"):
    ret = startai.permute_dims(x, axes=perm)
    return ret


@to_startai_arrays_and_back
def TruncateDiv(*, x, y, name="TruncateDiv"):
    return startai.astype(startai.trunc_divide(x, y), x.dtype)


@with_unsupported_dtypes({"2.15.0 and below": ("float16", "bfloat16")}, "tensorflow")
@to_startai_arrays_and_back
def Unpack(*, value, num, axis=0, name="Unpack"):
    return startai.unstack(value, axis=axis)[:num]


@with_supported_dtypes(
    {
        "2.15.0 and below": (
            "int8",
            "int16",
            "int32",
            "int64",
            "float32",
            "float64",
            "complex64",
            "complex128",
        )
    },
    "tensorflow",
)
@to_startai_arrays_and_back
def UnsortedSegmentProd(*, data, segment_ids, num_segments, name=None):
    data = startai.array(data)
    segment_ids = startai.array(segment_ids)

    startai.utils.assertions.check_equal(
        list(segment_ids.shape), [list(data.shape)[0]], as_array=False
    )
    startai.utils.assertions.check_greater(int(num_segments), int(startai.max(segment_ids)))

    shape = list(startai.shape(data))
    shape[0] = int(num_segments)
    x = startai.ones(shape, dtype=data.dtype)
    for i in range((segment_ids).shape[0]):
        x[segment_ids[i]] = startai.multiply(x[segment_ids[i]], data[i])
    return x


@to_startai_arrays_and_back
def Xdstartai(*, x, y, name="Xdstartai"):
    if (x == 0).all():
        return 0.0
    return startai.divide(x, y)


@with_unsupported_dtypes({"2.15.0 and below": ("bfloat16",)}, "tensorflow")
@to_startai_arrays_and_back
def Xlog1py(*, x, y, name="Xlog1py"):
    if (x == 0).all():
        return 0.0
    return startai.multiply(x, startai.log1p(y))


@to_startai_arrays_and_back
def ZerosLike(*, x, name="ZerosLike"):
    return startai.zeros_like(x)
