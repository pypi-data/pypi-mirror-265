import startai
import startai.functional.frontends.tensorflow as tf_frontend
from startai.functional.frontends.tensorflow.func_wrapper import to_startai_arrays_and_back
from startai import with_supported_dtypes, with_unsupported_dtypes


ACTIVATION_FUNCTIONS = [
    "gelu",
    "leaky_relu",
    "log_softmax",
    "relu",
    "sigmoid",
    "silu",
    "softmax",
    "softplus",
]


# --- Helpers --- #
# --------------- #


# note: defined to avoid AST call extraction of
# 'tf_frontend.keras.activations.__dict__.items()
# or 'tf_frontend.keras.activations.__dict__.values()'
def _get_tf_keras_activations():
    return tf_frontend.keras.activations.__dict__.items()


# --- Main --- #
# ------------ #


@with_supported_dtypes(
    {"2.15.0 and below": ("float16", "float32", "float64")},
    "tensorflow",
)
def deserialize(name, custom_objects=None):
    if name is None:
        return None

    elif isinstance(name, str):
        if custom_objects and name in custom_objects:
            return custom_objects.get(name)

        # To replicate tensorflow framework
        elif (
            startai.current_backend().__name__.split(".")[-1] == "tensorflow"
            and name in tf_frontend.keras.activations.__dict__
        ):  # noqa
            return tf_frontend.keras.activations.__dict__[name]

        # On other backends, query the function from global startai dict
        elif name in ACTIVATION_FUNCTIONS:
            return startai.__dict__[name]

        else:
            raise ValueError(f"Unknown activation function: {name}.")

    else:
        raise ValueError(f"Could not interpret activation function: {name}")


@with_supported_dtypes(
    {"2.15.0 and below": ("bfloat16", "float16", "float32", "float64")},
    "tensorflow",
)
@to_startai_arrays_and_back
def elu(x, alpha=1.0):
    zeros = startai.zeros_like(x, dtype=startai.dtype(x))
    ones = startai.ones_like(x, dtype=startai.dtype(x))
    alpha = startai.astype(startai.array(alpha), startai.dtype(x))
    ret_val = startai.where(
        x > zeros, x, startai.multiply(alpha, startai.subtract(startai.exp(x), ones))
    )
    return ret_val


@to_startai_arrays_and_back
def gelu(x, approximate=False):
    return startai.gelu(x, approximate=approximate)


def get(identifier):
    if identifier is None:
        return tf_frontend.keras.activations.linear

    elif isinstance(identifier, str):
        return tf_frontend.keras.activations.deserialize(identifier)

    elif callable(identifier):
        return identifier

    else:
        raise ValueError(f"Could not interpret function identifier: {identifier}")


@to_startai_arrays_and_back
def hard_sigmoid(x):
    dtype_in = x.dtype
    point_two = startai.full(x.shape, 0.2)
    point_five = startai.full(x.shape, 0.5)
    x = startai.multiply(x, point_two)
    x = startai.add(x, point_five)
    x = startai.clip(x, 0.0, 1.0)
    x = startai.asarray(x, dtype=dtype_in)
    return x


@to_startai_arrays_and_back
def linear(x):
    return startai.array(x)


@with_unsupported_dtypes(
    {"2.15.0 and below": ("complex",)},
    "tensorflow",
)
@to_startai_arrays_and_back
def relu(x, alpha=0.0, max_value=None, threshold=0.0):
    return startai.relu(x)


@with_supported_dtypes(
    {"2.15.0 and below": ("float16", "float32", "float64")},
    "tensorflow",
)
@to_startai_arrays_and_back
def selu(x):
    return startai.selu(x)


@with_supported_dtypes(
    {"2.15.0 and below": ("float16", "float32", "float64")},
    "tensorflow",
)
def serialize(activation, use_legacy_format=False, custom_objects=None):
    # If the activation function is None, return None
    if activation is None:
        return None

    # If the activation function is already a string, return it
    elif isinstance(activation, str):
        return activation

    # If the activation function is callable (a function), get its name
    elif callable(activation):
        # Check if the function is in the custom_objects dictionary
        if custom_objects:
            for name, custom_func in custom_objects.items():
                if custom_func == activation:
                    return name

        tf_keras_frontend_activations = _get_tf_keras_activations()

        # Check if the function is in the ACTIVATION_FUNCTIONS list
        if activation.__name__ in ACTIVATION_FUNCTIONS:
            return activation.__name__

        # Check if the function is in the TensorFlow frontend activations
        elif activation in [fn for name, fn in tf_keras_frontend_activations]:
            for name, tf_func in tf_keras_frontend_activations:
                if tf_func == activation:
                    return name

        else:
            raise ValueError(f"Unknown activation function: {activation}.")

    else:
        raise ValueError(f"Could not interpret activation function: {activation}")


@to_startai_arrays_and_back
def sigmoid(x):
    return startai.sigmoid(x)


@to_startai_arrays_and_back
def softmax(x, axis=-1):
    return startai.softmax(x, axis=axis)


@to_startai_arrays_and_back
def softplus(x):
    return startai.softplus(x)


@to_startai_arrays_and_back
def softsign(x):
    return startai.divide(x, startai.add(1, startai.abs(x)))


@to_startai_arrays_and_back
def swish(x):
    return startai.multiply(x, startai.sigmoid(x))


@to_startai_arrays_and_back
def tanh(x):
    return startai.tanh(x)
