# local
import startai
from startai.func_wrapper import inputs_to_native_arrays
from startai.utils.exceptions import handle_exceptions


# helpers
def _verify_coo_components(indices=None, values=None, dense_shape=None):
    startai.utils.assertions.check_all_or_any_fn(
        indices,
        values,
        dense_shape,
        fn=startai.exists,
        type="all",
        message="indices, values and dense_shape must all be specified",
    )
    # coordinates style (COO), must be shaped (x, y)
    startai.utils.assertions.check_equal(
        len(startai.shape(indices)), 2, message="indices must be 2D", as_array=False
    )
    startai.utils.assertions.check_equal(
        len(startai.shape(values)), 1, message="values must be 1D", as_array=False
    )
    startai.utils.assertions.check_equal(
        len(startai.to_startai_shape(dense_shape)),
        startai.shape(indices)[0],
        message="shape and indices shape do not match",
        as_array=False,
    )
    # number of values must match number of coordinates
    startai.utils.assertions.check_equal(
        startai.shape(values)[0],
        startai.shape(indices)[1],
        message="values and indices do not match",
        as_array=False,
    )
    for i in range(startai.shape(indices)[0]):
        startai.utils.assertions.check_less(
            indices[i],
            startai.to_startai_shape(dense_shape)[i],
            message="indices is larger than shape",
        )


def _verify_common_row_format_components(
    crow_indices=None, col_indices=None, values=None, dense_shape=None, format="csr"
):
    startai.utils.assertions.check_all_or_any_fn(
        crow_indices,
        col_indices,
        values,
        dense_shape,
        fn=startai.exists,
        type="all",
        message=(
            "crow_indices, col_indices, values and dense_shape must all be specified."
        ),
    )

    startai.utils.assertions.check_equal(
        len(startai.shape(crow_indices)),
        1,
        message="crow_indices must be 1D.",
        as_array=False,
    )
    startai.utils.assertions.check_equal(
        len(startai.shape(col_indices)),
        1,
        message="col_indices must be 1D.",
        as_array=False,
    )

    startai.utils.assertions.check_equal(
        len(dense_shape),
        2,
        message=f"Only 2D arrays can be converted to {format.upper()} sparse arrays.",
        as_array=False,
    )

    startai.utils.assertions.check_equal(
        startai.shape(col_indices)[0],
        crow_indices[-1],
        message="size of col_indices does not match with last element of crow_indices",
    )

    # number of values must match number of coordinates
    startai.utils.assertions.check_equal(
        startai.shape(col_indices)[0],
        startai.shape(values)[0],
        message="values and col_indices do not match",
        as_array=False,
    )

    # index in crow_indices must not exceed length of col_indices
    startai.utils.assertions.check_less(
        crow_indices,
        startai.shape(col_indices)[0],
        allow_equal=True,
        message="index in crow_indices does not match the number of col_indices",
    )


def _verify_csr_components(
    crow_indices=None, col_indices=None, values=None, dense_shape=None
):
    _verify_common_row_format_components(
        crow_indices=crow_indices,
        col_indices=col_indices,
        values=values,
        dense_shape=dense_shape,
        format="csr",
    )

    startai.utils.assertions.check_equal(
        len(startai.shape(values)), 1, message="values must be 1D.", as_array=False
    )
    # number of intervals must be equal to x in shape (x, y)
    startai.utils.assertions.check_equal(
        startai.shape(crow_indices)[0] - 1, dense_shape[0], as_array=False
    )

    startai.utils.assertions.check_less(
        col_indices,
        dense_shape[1],
        message="index in col_indices does not match shape",
    )


def _verify_bsr_components(
    crow_indices=None, col_indices=None, values=None, dense_shape=None
):
    _verify_common_row_format_components(
        crow_indices=crow_indices,
        col_indices=col_indices,
        values=values,
        dense_shape=dense_shape,
        format="bsr",
    )
    startai.utils.assertions.check_equal(
        len(startai.shape(values)), 3, message="values must be 3D.", as_array=False
    )
    nrowblocks, ncolblocks = startai.shape(values)[-2:]
    startai.utils.assertions.check_equal(
        dense_shape[0] % nrowblocks,
        0,
        message="The number of rows of array must be divisible by that of block.",
        as_array=False,
    )
    startai.utils.assertions.check_equal(
        dense_shape[1] % ncolblocks,
        0,
        message="The number of cols of array must be divisible by that of block.",
        as_array=False,
    )
    startai.utils.assertions.check_equal(
        startai.shape(crow_indices)[0] - 1, dense_shape[0] // nrowblocks, as_array=False
    )
    startai.utils.assertions.check_less(
        col_indices,
        dense_shape[1] // ncolblocks,
        message="index in col_indices does not match shape",
    )


def _verify_common_column_format_components(
    ccol_indices=None, row_indices=None, values=None, dense_shape=None, format="csc"
):
    startai.utils.assertions.check_all_or_any_fn(
        ccol_indices,
        row_indices,
        values,
        dense_shape,
        fn=startai.exists,
        type="all",
        message=(
            "ccol_indices, row_indices, values and dense_shape must all be specified"
        ),
    )
    startai.utils.assertions.check_equal(
        len(startai.shape(ccol_indices)),
        1,
        message="ccol_indices must be 1D",
        as_array=False,
    )
    startai.utils.assertions.check_equal(
        len(startai.shape(row_indices)), 1, message="row_indices must be 1D", as_array=False
    )

    startai.utils.assertions.check_equal(
        len(dense_shape),
        2,
        message=f"only 2D arrays can be converted to {format.upper()} sparse arrays",
        as_array=False,
    )
    # number of values must match number of coordinates
    startai.utils.assertions.check_equal(
        startai.shape(row_indices)[0],
        startai.shape(values)[0],
        message="values and row_indices do not match",
        as_array=False,
    )
    # index in ccol_indices must not exceed length of row_indices
    startai.utils.assertions.check_less(
        ccol_indices,
        startai.shape(row_indices)[0],
        allow_equal=True,
        message="index in ccol_indices does not match the number of row_indices",
    )


def _verify_csc_components(
    ccol_indices=None, row_indices=None, values=None, dense_shape=None
):
    _verify_common_column_format_components(
        ccol_indices=ccol_indices,
        row_indices=row_indices,
        values=values,
        dense_shape=dense_shape,
        format="csc",
    )

    startai.utils.assertions.check_equal(
        len(startai.shape(values)), 1, message="values must be 1D", as_array=False
    )
    # number of intervals must be equal to y in shape (x, y)
    startai.utils.assertions.check_equal(
        startai.shape(ccol_indices)[0] - 1, dense_shape[1], as_array=False
    )
    startai.utils.assertions.check_less(
        row_indices,
        dense_shape[0],
        message="index in row_indices does not match shape",
    )


def _verify_bsc_components(
    ccol_indices=None, row_indices=None, values=None, dense_shape=None
):
    _verify_common_column_format_components(
        ccol_indices=ccol_indices,
        row_indices=row_indices,
        values=values,
        dense_shape=dense_shape,
        format="bsc",
    )
    startai.utils.assertions.check_equal(
        len(startai.shape(values)), 3, message="values must be 3D", as_array=False
    )
    nrowblocks, ncolblocks = startai.shape(values)[-2:]
    startai.utils.assertions.check_equal(
        dense_shape[0] % nrowblocks,
        0,
        message="number of rows of array must be divisible by that of block.",
        as_array=False,
    )
    startai.utils.assertions.check_equal(
        dense_shape[1] % ncolblocks,
        0,
        message="number of cols of array must be divisible by that of block.",
        as_array=False,
    )
    # number of intervals must be equal to y in shape (x, y)
    startai.utils.assertions.check_equal(
        startai.shape(ccol_indices)[0] - 1, dense_shape[1] // ncolblocks, as_array=False
    )
    startai.utils.assertions.check_less(
        row_indices,
        dense_shape[0] // nrowblocks,
        message="index in row_indices does not match shape",
    )


def _is_data_not_indices_values_and_shape(
    data=None,
    coo_indices=None,
    crow_indices=None,
    col_indices=None,
    ccol_indices=None,
    row_indices=None,
    values=None,
    dense_shape=None,
    format=None,
):
    if data is not None:
        startai.utils.assertions.check_all_or_any_fn(
            coo_indices,
            crow_indices,
            col_indices,
            ccol_indices,
            row_indices,
            values,
            dense_shape,
            format,
            fn=startai.exists,
            type="any",
            limit=[0],
            message=(
                "Only specify data, coo_indices for COO format, crow_indices and"
                " col_indices for CSR and BSR, ccol_indices and row_indicesfor CSC and"
                " BSC."
            ),
        )
        return True
    return False


def _is_valid_format(
    coo_indices=None,
    crow_indices=None,
    col_indices=None,
    ccol_indices=None,
    row_indices=None,
    values=None,
    dense_shape=None,
    format="coo",
):
    valid_formats = ["coo", "csr", "csc", "csc", "bsc", "bsr"]

    if not isinstance(format, str) or format.lower() not in valid_formats:
        return False

    if format.endswith("o"):
        # format is coo
        return (
            startai.exists(coo_indices)
            and startai.exists(values)
            and startai.exists(dense_shape)
            and crow_indices is None
            and col_indices is None
            and ccol_indices is None
            and row_indices is None
        )

    if format.endswith("r"):
        # format is either csr or bsr
        return (
            startai.exists(crow_indices)
            and startai.exists(col_indices)
            and startai.exists(values)
            and startai.exists(dense_shape)
            and coo_indices is None
            and ccol_indices is None
            and row_indices is None
        )
    # format is either csc or bsc
    return (
        startai.exists(ccol_indices)
        and startai.exists(row_indices)
        and startai.exists(values)
        and startai.exists(dense_shape)
        and coo_indices is None
        and crow_indices is None
        and col_indices is None
    )


class SparseArray(startai.Array):
    def __init__(
        self,
        data=None,
        *,
        coo_indices=None,
        crow_indices=None,
        col_indices=None,
        ccol_indices=None,
        row_indices=None,
        values=None,
        dense_shape=None,
        format=None,
    ):
        if _is_data_not_indices_values_and_shape(
            data,
            coo_indices,
            crow_indices,
            col_indices,
            ccol_indices,
            row_indices,
            values,
            dense_shape,
        ):
            self._init_data(data)
        elif _is_valid_format(
            coo_indices,
            crow_indices,
            col_indices,
            ccol_indices,
            row_indices,
            values,
            dense_shape,
            format=format,
        ):
            format = format.lower()

            if format == "coo":
                self._init_coo_components(coo_indices, values, dense_shape, format)
            elif format in ["csr", "bsr"]:
                self._init_compressed_row_components(
                    crow_indices, col_indices, values, dense_shape, format
                )
            else:
                print(format)
                self._init_compressed_column_components(
                    ccol_indices, row_indices, values, dense_shape, format
                )

        else:
            print(
                format,
                ccol_indices,
                row_indices,
                values,
                dense_shape,
                crow_indices,
                col_indices,
                values,
            )

            raise startai.utils.exceptions.StartaiException(
                "specify all coo components (coo_indices, values and "
                " dense_shape), all csr components (crow_indices, "
                "col_indices, values and dense_shape), all csc components "
                "(ccol_indices, row_indices, values and dense_shape). all "
                "bsc components (ccol_indices, row_indices, values and "
                "dense_shape), or all bsr components (crow_indices, "
                "col_indices, values and dense_shape)."
            )

        # initialize parent class
        super().__init__(self)

    def _init_data(self, data):
        if startai.is_startai_sparse_array(data):
            self._data = data.data
            self._coo_indices = data.coo_indices
            self._crow_indices = data.crow_indices
            self._col_indices = data.col_indices
            self._ccol_indices = data.ccol_indices
            self._row_indices = data.row_indices
            self._values = data.values
            self._dense_shape = data.dense_shape
            self._format = data.format.lower()
        else:
            startai.utils.assertions.check_true(
                startai.is_native_sparse_array(data), message="not a native sparse array"
            )
            self._data = data
            self._native_sparse_array_to_indices_values_and_shape()

    def _native_sparse_array_to_indices_values_and_shape(self):
        indices, values, shape = startai.native_sparse_array_to_indices_values_and_shape(
            self._data
        )

        if "coo_indices" in indices:
            self._coo_indices = startai.array(indices["coo_indices"], dtype="int64")
            self._crow_indices = None
            self._col_indices = None
            self._ccol_indices = None
            self._row_indices = None

        elif "crow_indices" in indices and "col_indices" in indices:
            self._crow_indices = startai.array(indices["crow_indices"], dtype="int64")
            self._col_indices = startai.array(indices["col_indices"], dtype="int64")
            self._coo_indices = None
            self._ccol_indices = None
            self._row_indices = None

        else:
            self._ccol_indices = startai.array(indices["ccol_indices"], dtype="int64")
            self._row_indices = startai.array(indices["row_indices"], dtype="int64")
            self._coo_indices = None
            self._crow_indices = None
            self._col_indices = None

        self._values = startai.array(values)
        self._dense_shape = startai.Shape(shape)
        self._format = self._data.format.lower()

    def _init_coo_components(self, coo_indices, values, shape, format):
        coo_indices = startai.array(coo_indices, dtype="int64")
        values = startai.array(values)
        shape = startai.Shape(shape)
        self._data = startai.native_sparse_array(
            coo_indices=coo_indices, values=values, dense_shape=shape, format=format
        )
        self._coo_indices = coo_indices
        self._values = values
        self._dense_shape = shape
        self._format = format
        self._crow_indices = None
        self._col_indices = None
        self._ccol_indices = None
        self._row_indices = None

    def _init_compressed_row_components(
        self, crow_indices, col_indices, values, shape, format
    ):
        crow_indices = startai.array(crow_indices, dtype="int64")
        col_indices = startai.array(col_indices, dtype="int64")
        values = startai.array(values)
        shape = startai.Shape(shape)
        self._data = startai.native_sparse_array(
            crow_indices=crow_indices,
            col_indices=col_indices,
            values=values,
            dense_shape=shape,
            format=format,
        )
        self._crow_indices = crow_indices
        self._col_indices = col_indices
        self._values = values
        self._dense_shape = shape
        self._format = format
        self._coo_indices = None
        self._ccol_indices = None
        self._row_indices = None

    def _init_compressed_column_components(
        self, ccol_indices, row_indices, values, shape, format
    ):
        ccol_indices = startai.array(ccol_indices, dtype="int64")
        row_indices = startai.array(row_indices, dtype="int64")
        values = startai.array(values)
        shape = startai.Shape(shape)
        self._data = startai.native_sparse_array(
            ccol_indices=ccol_indices,
            row_indices=row_indices,
            values=values,
            dense_shape=shape,
            format=format,
        )
        self._ccol_indices = ccol_indices
        self._row_indices = row_indices
        self._values = values
        self._dense_shape = shape
        self._format = format
        self._coo_indices = None
        self._crow_indices = None
        self._col_indices = None

    def __repr__(self):
        if self._dev_str is None:
            self._dev_str = startai.as_startai_dev(self.device)
            self._pre_repr = "startai.sparse_array"
            if "gpu" in self._dev_str:
                self._post_repr = f", dev={self._dev_str})"
            else:
                self._post_repr = ")"
        if self._format == "coo":
            repr = (
                f"indices={self._coo_indices}, values={self._values},"
                f" dense_shape={self._dense_shape}"
            )
        elif self._format in ["csr", "bsr"]:
            repr = (
                f"crow_indices={self._crow_indices}, col_indices={self._col_indices},"
                f" values={self._values}, dense_shape={self._dense_shape}"
            )
        else:
            repr = (
                f"ccol_indices={self._ccol_indices}, row_indices={self._row_indices},"
                f" values={self._values}, dense_shape={self._dense_shape}"
            )
        return (
            self._pre_repr
            + "("
            + repr
            + f", format={self._format}"
            + self._post_repr.format(startai.current_backend_str())
        )

    # Properties #
    # -----------#

    @property
    def data(self):
        return self._data

    @property
    def coo_indices(self):
        return self._coo_indices

    @property
    def crow_indices(self):
        return self._crow_indices

    @property
    def col_indices(self):
        return self._col_indices

    @property
    def ccol_indices(self):
        return self._ccol_indices

    @property
    def row_indices(self):
        return self._row_indices

    @property
    def values(self):
        return self._values

    @property
    def dense_shape(self):
        return self._dense_shape

    @property
    def format(self):
        return self._format

    # Setters #
    # --------#

    @data.setter
    def data(self, data):
        self._init_data(data)

    @coo_indices.setter
    def coo_indices(self, indices):
        indices = startai.array(indices, dtype="int64")
        _verify_coo_components(
            indices=indices, values=self._values, dense_shape=self._dense_shape
        )
        self._coo_indices = indices

    @crow_indices.setter
    def crow_indices(self, indices):
        indices = startai.array(indices, dtype="int64")
        if self._format == "csr":
            _verify_csr_components(
                crow_indices=indices,
                col_indices=self._col_indices,
                values=self._values,
                dense_shape=self._dense_shape,
            )
        else:
            _verify_bsr_components(
                crow_indices=indices,
                col_indices=self._col_indices,
                values=self._values,
                dense_shape=self._dense_shape,
            )
        self._crow_indices = indices

    @col_indices.setter
    def col_indices(self, indices):
        indices = startai.array(indices, dtype="int64")
        if self._format == "csr":
            _verify_csr_components(
                crow_indices=indices,
                col_indices=self._col_indices,
                values=self._values,
                dense_shape=self._dense_shape,
            )
        else:
            _verify_bsr_components(
                crow_indices=indices,
                col_indices=self._col_indices,
                values=self._values,
                dense_shape=self._dense_shape,
            )
        self._col_indices = indices

    @ccol_indices.setter
    def ccol_indices(self, indices):
        indices = startai.array(indices, dtype="int64")
        if self._format == "csc":
            _verify_csc_components(
                ccol_indices=indices,
                row_indices=self._row_indices,
                values=self._values,
                dense_shape=self._dense_shape,
            )
        else:
            _verify_bsc_components(
                ccol_indices=indices,
                row_indices=self._row_indices,
                values=self._values,
                dense_shape=self._dense_shape,
            )
        self._ccol_indices = indices

    @row_indices.setter
    def row_indices(self, indices):
        indices = startai.array(indices, dtype="int64")
        if self._format == "csc":
            _verify_csc_components(
                ccol_indices=self._ccol_indices,
                row_indices=indices,
                values=self._values,
                dense_shape=self._dense_shape,
            )
        else:
            _verify_bsc_components(
                ccol_indices=self._ccol_indices,
                row_indices=indices,
                values=self._values,
                dense_shape=self._dense_shape,
            )
        self._row_indices = indices

    @values.setter
    def values(self, values):
        values = startai.array(values)
        _verify_coo_components(
            indices=self._coo_indices, values=values, dense_shape=self._dense_shape
        )
        self._values = values

    @dense_shape.setter
    def dense_shape(self, dense_shape):
        dense_shape = startai.Shape(dense_shape)
        _verify_coo_components(
            indices=self._coo_indices, values=self._values, dense_shape=dense_shape
        )
        self._dense_shape = dense_shape

    @format.setter
    def format(self, format):
        self._format = format

    # Instance Methods #
    # ---------------- #

    def _coo_to_dense_coordinates(self):
        all_coordinates = []
        for i in range(self._values.shape[0]):
            coordinate = startai.gather(self._coo_indices, startai.array([[i]]))
            coordinate = startai.reshape(coordinate, (self._coo_indices.shape[0],))
            all_coordinates.append(coordinate.to_list())
        return all_coordinates

    def _csr_to_dense_coordinates(self):
        all_coordinates = []
        total_rows = self._dense_shape[0]
        all_rows = self._col_indices.to_list()
        all_cols = self._crow_indices.to_list()
        for row in range(total_rows):
            cols = all_rows[all_cols[row] : all_cols[row + 1]]
            for col in cols:
                all_coordinates.append([row, col])
        return all_coordinates

    def _csc_to_dense_coordinates(self):
        # CSC sparse array
        all_coordinates = []
        total_rows = self._dense_shape[1]
        all_cols = self._row_indices.to_list()
        all_rows = self._ccol_indices.to_list()
        for col in range(total_rows):
            rows = all_cols[all_rows[col] : all_rows[col + 1]]
            for row in rows:
                all_coordinates.append([row, col])
        return all_coordinates

    def _bsr_to_dense_coordinates(self):
        all_coordinates = []
        total_rows = self._dense_shape[0]
        all_rows = self._crow_indices.to_list()
        all_cols = self._col_indices.to_list()

        nblockrows, nblockcols = self._values.shape[-2:]

        for row in range(total_rows // nblockrows):
            cols = all_cols[all_rows[row] : all_rows[row + 1]]
            for col in cols:
                for col_index in range(nblockcols):
                    for row_index in range(nblockrows):
                        all_coordinates.append(
                            [
                                nblockrows * row + row_index,
                                nblockcols * col + col_index,
                            ]
                        )
        return all_coordinates

    def _bsc_to_dense_coordinates(self):
        all_coordinates = []
        total_cols = self._dense_shape[1]
        all_rows = self._row_indices.to_list()
        all_cols = self._ccol_indices.to_list()

        nblockrows, nblockcols = self._values.shape[-2:]

        for col in range(total_cols // nblockcols):
            rows = all_rows[all_cols[col] : all_cols[col + 1]]
            for row in rows:
                for col_index in range(nblockcols):
                    for row_index in range(nblockrows):
                        all_coordinates.append(
                            [
                                nblockrows * row + row_index,
                                nblockcols * col + col_index,
                            ]
                        )
        return all_coordinates

    def to_dense_array(self, *, native=False):
        if self._format == "coo":
            all_coordinates = self._coo_to_dense_coordinates()
        elif self._format == "csr":
            all_coordinates = self._csr_to_dense_coordinates()
        elif self._format == "csc":
            all_coordinates = self._csc_to_dense_coordinates()
        elif self._format == "bsc":
            all_coordinates = self._bsc_to_dense_coordinates()
        else:
            all_coordinates = self._bsr_to_dense_coordinates()

        # make dense array
        ret = startai.scatter_nd(
            startai.array(all_coordinates),
            startai.flatten(self._values),
            startai.array(self._dense_shape),
        )
        return ret.to_native() if native else ret


class NativeSparseArray:
    pass


def is_startai_sparse_array(x):
    return isinstance(x, startai.SparseArray)


@handle_exceptions
@inputs_to_native_arrays
def is_native_sparse_array(x):
    return startai.current_backend().is_native_sparse_array(x)


@handle_exceptions
@inputs_to_native_arrays
def native_sparse_array(
    data=None,
    *,
    coo_indices=None,
    crow_indices=None,
    col_indices=None,
    ccol_indices=None,
    row_indices=None,
    values=None,
    dense_shape=None,
    format=None,
):
    return startai.current_backend().native_sparse_array(
        data,
        coo_indices=coo_indices,
        crow_indices=crow_indices,
        col_indices=col_indices,
        ccol_indices=ccol_indices,
        row_indices=row_indices,
        values=values,
        dense_shape=dense_shape,
        format=format,
    )


@handle_exceptions
def native_sparse_array_to_indices_values_and_shape(x):
    return startai.current_backend().native_sparse_array_to_indices_values_and_shape(x)
