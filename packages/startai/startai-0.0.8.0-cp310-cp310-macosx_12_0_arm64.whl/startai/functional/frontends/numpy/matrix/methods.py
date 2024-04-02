# global
import startai

# local
from startai.functional.frontends.numpy import (
    argmax,
    any,
    ndarray,
)


class matrix:
    def __init__(self, data, dtype=None, copy=True):
        self._init_data(data, dtype, copy)

    def _init_data(self, data, dtype, copy):
        if isinstance(data, str):
            self._process_str_data(data, dtype)
        elif isinstance(data, (list, ndarray)) or startai.is_array(data):
            if isinstance(data, ndarray):
                data = data.startai_array
            if startai.is_array(data) and dtype is None:
                dtype = data.dtype
            data = startai.array(data, dtype=dtype, copy=copy)
            self._data = data
        elif startai.isscalar(data):
            self._data = startai.asarray(data, dtype=dtype)
        else:
            raise startai.utils.exceptions.StartaiException(
                "data must be an array, list, or scalar"
            )
        if self._data.ndim < 2:
            self._data = self._data.reshape((1, -1))
        elif self._data.ndim > 2:
            newshape = tuple(x for x in self._data.shape if x > 1)
            ndim = len(newshape)
            if ndim == 2:
                self._data = self._data.reshape(newshape)
            else:
                raise ValueError("shape too large to be a matrix.")
        self._dtype = self._data.dtype
        self._shape = startai.shape(self._data)

    def _process_str_data(self, data, dtype):
        is_float = "." in data or "e" in data
        is_complex = "j" in data
        data = data.replace(",", " ")
        data = " ".join(data.split())
        data = data.split(";")
        for i, row in enumerate(data):
            row = row.strip().split(" ")
            data[i] = row
            for j, elem in enumerate(row):
                if is_complex:
                    data[i][j] = complex(elem)
                else:
                    data[i][j] = float(elem) if is_float else int(elem)
        if dtype is None:
            if is_complex:
                dtype = startai.complex128
            else:
                dtype = startai.float64 if is_float else startai.int64
        self._data = startai.array(data, dtype=dtype)

    # Properties #
    # ---------- #

    @property
    def A(self):
        return self._data

    @property
    def A1(self):
        return startai.reshape(self._data, (self.size,))

    # flake8: noqa: E743, E741
    @property
    def I(self):
        if startai.is_int_dtype(self._data):
            return startai.inv(self._data.astype(startai.float64))
        return startai.inv(self._data)

    @property
    def T(self):
        return startai.matrix_transpose(self._data)

    @property
    def data(self):
        return memoryview(startai.to_numpy(self._data).tobytes())

    @property
    def dtype(self):
        return self._dtype

    @property
    def ndim(self):
        return len(self._shape)

    @property
    def shape(self):
        return self._shape

    @property
    def size(self):
        return self._shape[0] * self._shape[1]

    # Setters #
    # ------- #

    @dtype.setter
    def dtype(self, dtype):
        self._data = startai.astype(self._data, dtype)
        self._dtype = self._data.dtype

    # Built-ins #
    # --------- #

    def __repr__(self):
        return "startai.matrix(" + str(self._data.to_list()) + ")"

    # Instance Methods #
    # ---------------- #

    def argmax(self, axis=None, out=None):
        if startai.exists(axis):
            return argmax(self.A, axis=axis, keepdims=True, out=out)
        return argmax(self.A, axis=axis, out=out)

    def any(self, axis=None, out=None):
        if startai.exists(axis):
            return any(self.A, axis=axis, keepdims=True, out=out)
        return any(self.A, axis=axis, out=out)
