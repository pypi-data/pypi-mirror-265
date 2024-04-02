# local
import startai
import startai.functional.frontends.tensorflow as tf_frontend
import startai.functional.frontends.numpy as np_frontend
from startai.functional.frontends.tensorflow.func_wrapper import (
    to_startai_arrays_and_back,
    handle_tf_dtype,
)


class DType:
    def __init__(self, dtype_int):
        self._startai_dtype = tf_frontend.tensorflow_enum_to_type[dtype_int]

    def __repr__(self):
        return "startai.frontends.tensorflow." + self._startai_dtype

    @property
    def startai_dtype(self):
        return self._startai_dtype

    @property
    def as_datatype_enum(self):
        return tf_frontend.tensorflow_type_to_enum[self._startai_dtype]

    @property
    def as_numpy_dtype(self):
        return np_frontend.dtype(self._startai_dtype)

    @property
    def base_dtype(self):
        return self

    @property
    def is_bool(self):
        return self._startai_dtype.is_bool_dtype

    @property
    def is_complex(self):
        return "complex" in self._startai_dtype

    @property
    def is_floating(self):
        return self._startai_dtype.is_float_dtype

    @property
    def is_integer(self):
        return self._startai_dtype.is_int_dtype

    @property
    def is_numpy_compatible(self):
        return self._startai_dtype in np_frontend.numpy_type_to_str_and_num_table

    @property
    def is_unsigned(self):
        return self._startai_dtype.is_uint_dtype

    @property
    def limits(self):
        if self._startai_dtype is startai.bool:
            return False, True
        if self._startai_dtype.is_int_dtype:
            return 0, self._startai_dtype.info.max
        if self._startai_dtype.is_float_dtype:
            return 0, 1
        else:
            raise startai.utils.exceptions.StartaiException(
                f"{self._startai_dtype} does not have defined limits"
            )

    @property
    def max(self):
        if self._startai_dtype in (startai.bool, startai.complex128, startai.complex64):
            raise startai.utils.exceptions.StartaiException(
                f"Cannot find maximum value of {self._startai_dtype}"
            )
        if self._startai_dtype is startai.bfloat16:
            return float.fromhex("0x1.FEp127")
        return self._startai_dtype.info.max

    @property
    def min(self):
        if self._startai_dtype in (startai.bool, startai.complex128, startai.complex64):
            raise startai.utils.exceptions.StartaiException(
                f"Cannot find maximum value of {self._startai_dtype}"
            )
        if self._startai_dtype is startai.bfloat16:
            return float.fromhex("-0x1.FEp127")
        return self._startai_dtype.info.min

    @property
    def real_dtype(self):
        if self._startai_dtype is startai.complex64:
            return DType(1)
        if self._startai_dtype is startai.complex128:
            return DType(2)
        else:
            return self

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, DType):
            try:
                other = as_dtype(other)
            except startai.utils.exceptions.StartaiException:
                return False

        return self._startai_dtype == other._startai_dtype

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(repr(self))


def as_dtype(type_value):
    if isinstance(type_value, DType):
        return type_value
    if startai.is_native_dtype(type_value):
        return DType(tf_frontend.tensorflow_type_to_enum[startai.as_startai_dtype(type_value)])
    if type_value in tf_frontend.tensorflow_enum_to_type:
        return DType(type_value)
    if type_value in tf_frontend.tensorflow_type_to_enum:
        return DType(tf_frontend.tensorflow_type_to_enum[type_value])
    if type_value is float:
        return DType(1)
    if type_value is bool:
        return DType(10)
    if isinstance(type_value, np_frontend.dtype):
        return DType(tf_frontend.tensorflow_type_to_enum[type_value.startai_dtype])
    if issubclass(type_value, np_frontend.generic):
        return DType(
            tf_frontend.tensorflow_type_to_enum[
                np_frontend.numpy_scalar_to_dtype[type_value]
            ]
        )
    raise startai.utils.exceptions.StartaiException(
        f"Cannot convert the argument 'type_value': {type_value!r} "
        "to a TensorFlow Dtype"
    )


@handle_tf_dtype
@to_startai_arrays_and_back
def cast(x, dtype, name=None):
    return startai.astype(x, dtype, copy=False)
