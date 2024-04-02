# global

# local
import startai
import startai.functional.frontends.tensorflow as tf_frontend


class Variable:
    def __init__(self, array, trainable=True, name=None, dtype=None):
        self._startai_array = (
            startai.array(array) if not isinstance(array, startai.Array) else array
        )
        self._startai_array = (
            startai.astype(self._startai_array, dtype) if dtype is not None else self._startai_array
        )
        self.trainable = trainable

    def __repr__(self):
        return (
            repr(self._startai_array).replace(
                "startai.array", "startai.frontends.tensorflow.Variable"
            )[:-1]
            + ", shape="
            + str(self._startai_array.shape)
            + ", dtype="
            + str(self._startai_array.dtype)
            + ")"
        )

    # Properties #
    # ---------- #

    @property
    def startai_array(self):
        return self._startai_array

    @property
    def device(self):
        return self._startai_array.device

    @property
    def dtype(self):
        return tf_frontend.DType(
            tf_frontend.tensorflow_type_to_enum[self._startai_array.dtype]
        )

    @property
    def shape(self):
        return self._startai_array.shape

    # Instance Methods #
    # ---------------- #

    def assign(self, value, use_locking=None, name=None, read_value=True):
        startai.utils.assertions.check_equal(
            value.startai_array.shape if hasattr(value, "startai_array") else startai.shape(value),
            self.shape,
            as_array=False,
        )
        self._startai_array = value._startai_array
        return self

    def assign_add(self, delta, use_locking=None, name=None, read_value=True):
        startai.utils.assertions.check_equal(
            delta.startai_array.shape if hasattr(delta, "startai_array") else startai.shape(delta),
            self.shape,
            as_array=False,
        )
        self._startai_array = startai.add(self._startai_array, delta._startai_array)
        return self

    def assign_sub(self, delta, use_locking=None, name=None, read_value=True):
        startai.utils.assertions.check_equal(
            delta.startai_array.shape if hasattr(delta, "startai_array") else startai.shape(delta),
            self.shape,
            as_array=False,
        )
        self._startai_array = startai.subtract(self._startai_array, delta._startai_array)
        return self

    def batch_scatter_update(
        self, sparse_delta, use_locking=None, name=None, read_value=True
    ):
        pass

    def gather_nd(self, indices, name=None):
        return tf_frontend.gather_nd(params=self._startai_array, indices=indices)

    def read_value(self):
        return tf_frontend.Tensor(self._startai_array)

    def scatter_add(self, sparse_delta, use_locking=None, name=None, read_value=True):
        pass

    def scatter_div(self, sparse_delta, use_locking=None, name=None, read_value=True):
        pass

    def scatter_max(self, sparse_delta, use_locking=None, name=None, read_value=True):
        pass

    def scatter_min(self, sparse_delta, use_locking=None, name=None, read_value=True):
        pass

    def scatter_mul(self, sparse_delta, use_locking=None, name=None, read_value=True):
        pass

    def scatter_nd_add(self, indices, updates, use_locking=None, name=None):
        pass

    def scatter_nd_sub(self, indices, updates, use_locking=None, name=None):
        pass

    def scatter_nd_update(self, indices, updates, use_locking=None, name=None):
        pass

    def scatter_sub(self, sparse_delta, use_locking=None, name=None, read_value=True):
        pass

    def scatter_update(
        self, sparse_delta, use_locking=None, name=None, read_value=True
    ):
        pass

    def set_shape(self, shape):
        if shape is None:
            return

        x_shape = self._startai_array.shape
        if len(x_shape) != len(shape):
            raise ValueError(
                f"Tensor's shape {x_shape} is not compatible with supplied shape "
                f"{shape}."
            )
        for i, v in enumerate(x_shape):
            if v != shape[i] and (shape[i] is not None):
                raise ValueError(
                    f"Tensor's shape {x_shape} is not compatible with supplied shape "
                    f"{shape}."
                )

    def get_shape(self):
        return self._startai_array.shape

    def sparse_read(self, indices, name=None):
        pass

    def __add__(self, y, name="add"):
        return self.__radd__(y)

    def __div__(self, x, name="div"):
        return tf_frontend.math.divide(x, self._startai_array, name=name)

    def __and__(self, y, name="and"):
        return y.__rand__(self._startai_array)

    def __eq__(self, other):
        return tf_frontend.raw_ops.Equal(
            x=self._startai_array, y=other, incompatible_shape_error=False
        )

    def __floordiv__(self, y, name="floordiv"):
        return y.__rfloordiv__(self._startai_array)

    def __ge__(self, y, name="ge"):
        return tf_frontend.raw_ops.GreaterEqual(
            x=self._startai_array, y=y._startai_array, name=name
        )

    def __getitem__(self, slice_spec, var=None, name="getitem"):
        ret = startai.get_item(self._startai_array, slice_spec)
        return Variable(startai.array(ret, dtype=startai.dtype(ret), copy=False))

    def __gt__(self, y, name="gt"):
        return tf_frontend.raw_ops.Greater(x=self._startai_array, y=y._startai_array, name=name)

    def __invert__(self, name="invert"):
        return tf_frontend.raw_ops.Invert(x=self._startai_array, name=name)

    def __le__(self, y, name="le"):
        return tf_frontend.raw_ops.LessEqual(
            x=self._startai_array, y=y._startai_array, name=name
        )

    def __lt__(self, y, name="lt"):
        return tf_frontend.raw_ops.Less(x=self._startai_array, y=y._startai_array, name=name)

    def __matmul__(self, y, name="matmul"):
        return y.__rmatmul__(self._startai_array)

    def __mul__(self, x, name="mul"):
        return tf_frontend.math.multiply(x, self._startai_array, name=name)

    def __mod__(self, x, name="mod"):
        return tf_frontend.math.mod(x, self._startai_array, name=name)

    def __ne__(self, other):
        return tf_frontend.raw_ops.NotEqual(
            x=self._startai_array, y=other._startai_array, incompatible_shape_error=False
        )

    def __neg__(self, name="neg"):
        return tf_frontend.raw_ops.Neg(x=self._startai_array, name=name)

    def __or__(self, y, name="or"):
        return y.__ror__(self._startai_array)

    def __pow__(self, y, name="pow"):
        return tf_frontend.math.pow(x=self, y=y, name=name)

    def __radd__(self, x, name="radd"):
        return tf_frontend.math.add(x, self._startai_array, name=name)

    def __rand__(self, x, name="rand"):
        return tf_frontend.math.logical_and(x, self._startai_array, name=name)

    def __rfloordiv__(self, x, name="rfloordiv"):
        return tf_frontend.raw_ops.FloorDiv(x=x, y=self._startai_array, name=name)

    def __rmatmul__(self, x, name="rmatmul"):
        return tf_frontend.raw_ops.MatMul(a=x, b=self._startai_array, name=name)

    def __rmul__(self, x, name="rmul"):
        return tf_frontend.raw_ops.Mul(x=x, y=self._startai_array, name=name)

    def __ror__(self, x, name="ror"):
        return tf_frontend.raw_ops.LogicalOr(x=x, y=self._startai_array, name=name)

    def __rpow__(self, x, name="rpow"):
        return tf_frontend.raw_ops.Pow(x=x, y=self._startai_array, name=name)

    def __rsub__(self, x, name="rsub"):
        return tf_frontend.math.subtract(x, self._startai_array, name=name)

    def __rtruediv__(self, x, name="rtruediv"):
        return tf_frontend.math.truediv(x, self._startai_array, name=name)

    def __rxor__(self, x, name="rxor"):
        return tf_frontend.math.logical_xor(x, self._startai_array, name=name)

    def __sub__(self, y, name="sub"):
        return y.__rsub__(self._startai_array)

    def __truediv__(self, y, name="truediv"):
        dtype = startai.dtype(self._startai_array)
        if dtype in [startai.uint8, startai.int8, startai.uint16, startai.int16]:
            return startai.astype(y, startai.float32).__rtruediv__(
                startai.astype(self._startai_array, startai.float32)
            )
        if dtype in [startai.uint32, startai.int32, startai.uint64, startai.int64]:
            return startai.astype(y, startai.float64).__rtruediv__(
                startai.astype(self._startai_array, startai.float64)
            )
        return y.__rtruediv__(self._startai_array)

    def __xor__(self, y, name="xor"):
        return y.__rxor__(self._startai_array)

    def __setitem__(self, key, value):
        raise startai.utils.exceptions.StartaiException(
            "startai.functional.frontends.tensorflow.Variable object "
            "doesn't support assignment"
        )


class IndexedSlices:
    def __init__(self, values, indices, dense_shape=None):
        self._values = values
        self._indices = indices
        self._dense_shape = dense_shape

    @property
    def values(self):
        """A `Tensor` containing the values of the slices."""
        return self._values

    @property
    def indices(self):
        """A 1-D `Tensor` containing the indices of the slices."""
        return self._indices

    @property
    def dense_shape(self):
        """A 1-D `Tensor` containing the shape of the corresponding dense
        tensor."""
        return self._dense_shape

    @property
    def device(self):
        """The name of the device on which `values` will be produced, or
        `None`."""
        return self.values.device

    @property
    def dtype(self):
        """The `DType` of elements in this tensor."""
        return self.values.dtype

    def __repr__(self):
        return "IndexedSlices(\nindices=%s,\nvalues=%s%s\n)" % (
            self._indices,
            self._values,
            (
                f", dense_shape={self._dense_shape}"
                if self._dense_shape is not None
                else ""
            ),
        )

    def __neg__(self):
        return IndexedSlices(-self._values, self._indices, self._dense_shape)
