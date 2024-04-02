# global
from hypothesis import given, strategies as st
import platform

# local
import startai
import startai_tests.test_startai.helpers as helpers
from startai.functional.frontends.numpy.func_wrapper import (
    inputs_to_startai_arrays,
    outputs_to_frontend_arrays,
    to_startai_arrays_and_back,
    handle_numpy_dtype,
    from_zero_dim_arrays_to_scalar,
)
from startai.functional.frontends.numpy.ndarray import ndarray
import startai.functional.frontends.numpy as np_frontend


# --- Helpers --- #
# --------------- #


@st.composite
def _dtype_helper(draw):
    return draw(
        st.sampled_from(
            [
                draw(st.sampled_from([int, float, bool])),
                startai.as_native_dtype(
                    draw(helpers.get_dtypes("valid", full=False, prune_function=False))[
                        0
                    ]
                ),
                np_frontend.dtype(
                    draw(helpers.get_dtypes("valid", full=False, prune_function=False))[
                        0
                    ]
                ),
                draw(st.sampled_from(list(np_frontend.numpy_scalar_to_dtype.keys()))),
                draw(st.sampled_from(list(np_frontend.numpy_str_to_type_table.keys()))),
            ]
        )
    )


def _fn(*args, check_default=False, dtype=None):
    if (
        check_default
        and any(not (startai.is_array(i) or hasattr(i, "startai_array")) for i in args)
        and not startai.exists(dtype)
    ):
        startai.utils.assertions.check_equal(
            startai.default_float_dtype(), "float64", as_array=False
        )
        if platform.system() != "Windows":
            startai.utils.assertions.check_equal(
                startai.default_int_dtype(), "int64", as_array=False
            )
        else:
            startai.utils.assertions.check_equal(
                startai.default_int_dtype(), "int32", as_array=False
            )
    if not startai.exists(args[0]):
        return dtype
    return args[0]


def _zero_dim_to_scalar_checks(x, ret_x):
    if len(x.shape) > 0:
        assert startai.all(startai.array(ret_x) == startai.array(x))
    else:
        assert issubclass(type(ret_x), np_frontend.generic)
        assert ret_x.startai_array == startai.array(x)


@st.composite
def _zero_dim_to_scalar_helper(draw):
    dtype = draw(
        helpers.get_dtypes("valid", prune_function=False, full=False).filter(
            lambda x: "bfloat16" not in x
        )
    )[0]
    shape = draw(helpers.get_shape())
    return draw(
        st.one_of(
            helpers.array_values(shape=shape, dtype=dtype),
            st.lists(helpers.array_values(shape=shape, dtype=dtype), min_size=1).map(
                tuple
            ),
        )
    )


# --- Main --- #
# ------------ #


@given(
    dtype=_dtype_helper(),
)
def test_handle_numpy_dtype(dtype, backend_fw):
    startai.set_backend(backend_fw)
    ret_dtype = handle_numpy_dtype(_fn)(None, dtype=dtype)
    assert isinstance(ret_dtype, startai.Dtype)
    startai.previous_backend()


@given(x=_zero_dim_to_scalar_helper())
def test_numpy_from_zero_dim_arrays_to_scalar(x, backend_fw):
    startai.set_backend(backend_fw)
    ret_x = from_zero_dim_arrays_to_scalar(_fn)(x)
    if isinstance(x, tuple):
        assert isinstance(ret_x, tuple)
        for x_i, ret_x_i in zip(x, ret_x):
            _zero_dim_to_scalar_checks(x_i, ret_x_i)
    else:
        _zero_dim_to_scalar_checks(x, ret_x)
    startai.previous_backend()


@given(
    dtype_x_shape=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False),
        ret_shape=True,
    ),
)
def test_numpy_inputs_to_startai_arrays(dtype_x_shape, backend_fw):
    startai.set_backend(backend_fw)
    x_dtype, x, shape = dtype_x_shape

    # check for startai array
    input_startai = startai.array(x[0], dtype=x_dtype[0])
    output = inputs_to_startai_arrays(_fn)(input_startai)
    assert isinstance(output, startai.Array)
    assert input_startai.dtype == output.dtype
    assert startai.all(input_startai == output)

    # check for native array
    input_native = startai.native_array(input_startai)
    output = inputs_to_startai_arrays(_fn)(input_native)
    assert isinstance(output, startai.Array)
    assert startai.as_startai_dtype(input_native.dtype) == str(output.dtype)
    assert startai.all(input_native == output.data)

    # check for frontend array
    input_frontend = ndarray(shape)
    input_frontend.startai_array = input_startai
    output = inputs_to_startai_arrays(_fn)(input_frontend)
    assert isinstance(output, startai.Array)
    assert input_frontend.startai_array.dtype == str(output.dtype)
    assert startai.all(input_frontend.startai_array == output)
    startai.previous_backend()


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ),
    dtype=helpers.get_dtypes("valid", none=True, full=False, prune_function=False),
)
def test_numpy_outputs_to_frontend_arrays(dtype_and_x, dtype, backend_fw):
    startai.set_backend(backend_fw)
    x_dtype, x = dtype_and_x

    # check for startai array
    input_startai = startai.array(x[0], dtype=x_dtype[0])
    if not len(input_startai.shape):
        scalar_input_startai = startai.to_scalar(input_startai)
        outputs_to_frontend_arrays(_fn)(
            scalar_input_startai, scalar_input_startai, check_default=True, dtype=dtype
        )
        outputs_to_frontend_arrays(_fn)(
            scalar_input_startai, input_startai, check_default=True, dtype=dtype
        )
    output = outputs_to_frontend_arrays(_fn)(input_startai, check_default=True, dtype=dtype)
    assert isinstance(output, ndarray)
    assert input_startai.dtype == output.startai_array.dtype
    assert startai.all(input_startai == output.startai_array)

    assert startai.default_float_dtype_stack == startai.default_int_dtype_stack == []
    startai.previous_backend()


@given(
    dtype_x_shape=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False),
        ret_shape=True,
    ),
    dtype=helpers.get_dtypes("valid", none=True, full=False, prune_function=False),
)
def test_numpy_to_startai_arrays_and_back(dtype_x_shape, dtype, backend_fw):
    startai.set_backend(backend_fw)
    x_dtype, x, shape = dtype_x_shape

    # check for startai array
    input_startai = startai.array(x[0], dtype=x_dtype[0])
    if not len(input_startai.shape):
        scalar_input_startai = startai.to_scalar(input_startai)
        to_startai_arrays_and_back(_fn)(
            scalar_input_startai, scalar_input_startai, check_default=True, dtype=dtype
        )
        to_startai_arrays_and_back(_fn)(
            scalar_input_startai, input_startai, check_default=True, dtype=dtype
        )
    output = to_startai_arrays_and_back(_fn)(input_startai, check_default=True, dtype=dtype)
    assert isinstance(output, ndarray)
    assert input_startai.dtype == output.startai_array.dtype
    assert startai.all(input_startai == output.startai_array)

    # check for native array
    input_native = startai.native_array(input_startai)
    if not len(input_native.shape):
        scalar_input_native = startai.to_scalar(input_native)
        to_startai_arrays_and_back(_fn)(
            scalar_input_native, scalar_input_native, check_default=True, dtype=dtype
        )
        to_startai_arrays_and_back(_fn)(
            scalar_input_native, input_native, check_default=True, dtype=dtype
        )
    output = to_startai_arrays_and_back(_fn)(input_native, check_default=True, dtype=dtype)
    assert isinstance(output, ndarray)
    assert startai.as_startai_dtype(input_native.dtype) == output.startai_array.dtype
    assert startai.all(input_native == output.startai_array.data)

    # check for frontend array
    input_frontend = ndarray(shape)
    input_frontend.startai_array = input_startai
    if not len(input_frontend.shape):
        scalar_input_front = inputs_to_startai_arrays(startai.to_scalar)(input_frontend)
        to_startai_arrays_and_back(_fn)(
            scalar_input_front, scalar_input_front, check_default=True, dtype=dtype
        )
        to_startai_arrays_and_back(_fn)(
            scalar_input_front, input_frontend, check_default=True, dtype=dtype
        )
    output = to_startai_arrays_and_back(_fn)(
        input_frontend, check_default=True, dtype=dtype
    )
    assert isinstance(output, ndarray)
    assert input_frontend.startai_array.dtype == output.startai_array.dtype
    assert startai.all(input_frontend.startai_array == output.startai_array)

    assert startai.default_float_dtype_stack == startai.default_int_dtype_stack == []
    startai.previous_backend()
