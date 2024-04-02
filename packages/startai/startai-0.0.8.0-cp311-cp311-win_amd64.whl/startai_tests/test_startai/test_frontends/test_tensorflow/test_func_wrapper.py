# global
from hypothesis import given, strategies as st

# local
import startai
import startai_tests.test_startai.helpers as helpers
from startai_tests.test_startai.helpers import BackendHandler
from startai.functional.frontends.tensorflow.func_wrapper import (
    outputs_to_frontend_arrays,
    to_startai_arrays_and_back,
    handle_tf_dtype,
)
from startai.functional.frontends.tensorflow.tensor import EagerTensor
import startai.functional.frontends.tensorflow as tf_frontend
import startai.functional.frontends.numpy as np_frontend


# --- Helpers --- #
# --------------- #


@st.composite
def _dtype_helper(draw):
    return draw(
        st.sampled_from(
            [
                draw(helpers.get_dtypes("valid", prune_function=False, full=False))[0],
                startai.as_native_dtype(
                    draw(helpers.get_dtypes("valid", prune_function=False, full=False))[
                        0
                    ]
                ),
                draw(
                    st.sampled_from(list(tf_frontend.tensorflow_enum_to_type.values()))
                ),
                draw(st.sampled_from(list(tf_frontend.tensorflow_enum_to_type.keys()))),
                np_frontend.dtype(
                    draw(helpers.get_dtypes("valid", prune_function=False, full=False))[
                        0
                    ]
                ),
                draw(st.sampled_from(list(np_frontend.numpy_scalar_to_dtype.keys()))),
            ]
        )
    )


def _fn(x=None, dtype=None):
    if startai.exists(dtype):
        return dtype
    return x


# --- Main --- #
# ------------ #


@given(
    dtype=_dtype_helper(),
)
def test_tensorflow_handle_tf_dtype(dtype):
    ret_dtype = handle_tf_dtype(_fn)(dtype=dtype)
    assert isinstance(ret_dtype, startai.Dtype)


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ),
)
def test_tensorflow_inputs_to_startai_arrays(dtype_and_x, backend_fw):
    x_dtype, x = dtype_and_x

    with BackendHandler.update_backend(backend_fw) as startai_backend:
        _import_fn = startai_backend.utils.dynamic_import.import_module
        _import_fn("startai.functional.frontends.tensorflow.func_wrapper")
        _tensor_module = _import_fn("startai.functional.frontends.tensorflow.tensor")

        # check for startai array
        input_startai = startai_backend.array(x[0], dtype=x_dtype[0])
        output = startai_backend.inputs_to_startai_arrays(_fn)(input_startai)
        assert isinstance(output, startai_backend.Array)
        assert input_startai.dtype == output.dtype
        assert startai_backend.all(input_startai == output)

        # check for native array
        input_native = startai_backend.native_array(input_startai)
        output = startai_backend.inputs_to_startai_arrays(_fn)(input_native)
        assert isinstance(output, startai_backend.Array)
        assert startai_backend.as_startai_dtype(input_native.dtype) == output.dtype
        assert startai_backend.all(input_native == output.data)

        # check for frontend array
        input_frontend = _tensor_module.EagerTensor(x[0])
        output = startai_backend.inputs_to_startai_arrays(_fn)(input_frontend)
        assert isinstance(output, startai_backend.Array)
        assert input_frontend.dtype.startai_dtype == output.dtype
        assert startai_backend.all(input_frontend.startai_array == output)


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ),
)
def test_tensorflow_outputs_to_frontend_arrays(dtype_and_x):
    x_dtype, x = dtype_and_x

    # check for startai array
    input_startai = startai.array(x[0], dtype=x_dtype[0])
    output = outputs_to_frontend_arrays(_fn)(input_startai)
    assert isinstance(output, EagerTensor)
    assert input_startai.dtype == output.dtype.startai_dtype
    assert startai.all(input_startai == output.startai_array)


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ),
)
def test_tensorflow_to_startai_arrays_and_back(dtype_and_x):
    x_dtype, x = dtype_and_x

    # check for startai array
    input_startai = startai.array(x[0], dtype=x_dtype[0])
    output = to_startai_arrays_and_back(_fn)(input_startai)
    assert isinstance(output, EagerTensor)
    assert input_startai.dtype == output.dtype.startai_dtype
    assert startai.all(input_startai == output.startai_array)

    # check for native array
    input_native = startai.native_array(input_startai)
    output = to_startai_arrays_and_back(_fn)(input_native)
    assert isinstance(output, EagerTensor)
    assert startai.as_startai_dtype(input_native.dtype) == output.dtype.startai_dtype
    assert startai.all(input_native == output.startai_array.data)

    # check for frontend array
    input_frontend = EagerTensor(x[0])
    output = to_startai_arrays_and_back(_fn)(input_frontend)
    assert isinstance(output, EagerTensor)
    assert input_frontend.dtype == output.dtype
    assert startai.all(input_frontend.startai_array == output.startai_array)
