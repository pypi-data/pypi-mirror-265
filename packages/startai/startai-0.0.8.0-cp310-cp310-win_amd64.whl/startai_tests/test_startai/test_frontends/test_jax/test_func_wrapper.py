# global
from hypothesis import given

# local
import startai
import startai_tests.test_startai.helpers as helpers
from startai.functional.frontends.jax.func_wrapper import (
    inputs_to_startai_arrays,
    outputs_to_frontend_arrays,
    to_startai_arrays_and_back,
)
from startai.functional.frontends.jax.array import Array
import startai.functional.frontends.jax as jax_frontend


# --- Helpers --- #
# --------------- #


def _fn(x, check_default=False):
    if check_default and jax_frontend.config.jax_enable_x64:
        startai.utils.assertions.check_equal(
            startai.default_float_dtype(), "float64", as_array=False
        )
        startai.utils.assertions.check_equal(
            startai.default_int_dtype(), "int64", as_array=False
        )
    return x


# --- Main --- #
# ------------ #


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ),
)
def test_jax_inputs_to_startai_arrays(dtype_and_x, backend_fw):
    startai.set_backend(backend_fw)
    x_dtype, x = dtype_and_x

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
    assert startai.as_startai_dtype(input_native.dtype) == output.dtype
    assert startai.all(startai.equal(input_native, output.data))

    # check for frontend array
    input_frontend = Array(x[0])
    output = inputs_to_startai_arrays(_fn)(input_frontend)
    assert isinstance(output, startai.Array)
    assert input_frontend.dtype == output.dtype
    assert startai.all(input_frontend.startai_array == output)
    startai.previous_backend()


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ),
)
def test_jax_outputs_to_frontend_arrays(dtype_and_x, backend_fw):
    startai.set_backend(backend_fw)
    x_dtype, x = dtype_and_x

    # check for startai array
    input_startai = startai.array(x[0], dtype=x_dtype[0])
    output = outputs_to_frontend_arrays(_fn)(input_startai, check_default=True)
    assert isinstance(output, Array)
    assert input_startai.dtype == output.dtype
    assert startai.all(input_startai == output.startai_array)

    assert startai.default_float_dtype_stack == startai.default_int_dtype_stack == []
    startai.previous_backend()


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ),
)
def test_jax_to_startai_arrays_and_back(dtype_and_x, backend_fw):
    startai.set_backend(backend_fw)
    x_dtype, x = dtype_and_x

    # check for startai array
    input_startai = startai.array(x[0], dtype=x_dtype[0])
    output = to_startai_arrays_and_back(_fn)(input_startai, check_default=True)
    assert isinstance(output, Array)
    assert input_startai.dtype == output.dtype
    assert startai.all(input_startai == output.startai_array)

    # check for native array
    input_native = startai.native_array(input_startai)
    output = to_startai_arrays_and_back(_fn)(input_native, check_default=True)
    assert isinstance(output, Array)
    assert startai.as_startai_dtype(input_native.dtype) == output.dtype
    assert startai.all(startai.equal(input_native, output.startai_array.data))

    # check for frontend array
    input_frontend = Array(x[0])
    output = to_startai_arrays_and_back(_fn)(input_frontend, check_default=True)
    assert isinstance(output, Array)
    assert str(input_frontend.dtype) == str(output.dtype)
    assert startai.all(input_frontend.startai_array == output.startai_array)

    assert startai.default_float_dtype_stack == startai.default_int_dtype_stack == []
    startai.previous_backend()
