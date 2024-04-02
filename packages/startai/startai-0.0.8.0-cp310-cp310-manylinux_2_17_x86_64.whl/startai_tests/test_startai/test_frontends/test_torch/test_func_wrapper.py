# global
from hypothesis import given, strategies as st

# local
import startai
import startai_tests.test_startai.helpers as helpers
from startai.functional.frontends.torch.func_wrapper import (
    inputs_to_startai_arrays,
    outputs_to_frontend_arrays,
    to_startai_arrays_and_back,
    numpy_to_torch_style_args,
)
from startai.functional.frontends.torch.tensor import Tensor
import startai.functional.frontends.torch as torch_frontend


# --- Helpers --- #
# --------------- #


def _fn(*args, dtype=None, check_default=False, inplace=False):
    if (
        check_default
        and all(not (startai.is_array(i) or hasattr(i, "startai_array")) for i in args)
        and not startai.exists(dtype)
    ):
        startai.utils.assertions.check_equal(
            startai.default_float_dtype(),
            torch_frontend.get_default_dtype(),
            as_array=False,
        )
        startai.utils.assertions.check_equal(
            startai.default_int_dtype(), "int64", as_array=False
        )
    return args[0]


# --- Main --- #
# ------------ #


@numpy_to_torch_style_args
def mocked_func(dim=None, keepdim=None, input=None, other=None):
    return dim, keepdim, input, other


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ).filter(lambda x: "bfloat16" not in x[0])
)
def test_torch_inputs_to_startai_arrays(dtype_and_x, backend_fw):
    x_dtype, x = dtype_and_x

    startai.set_backend(backend=backend_fw)

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
    input_frontend = Tensor(x[0])
    input_frontend.startai_array = input_startai
    output = inputs_to_startai_arrays(_fn)(input_frontend)
    assert isinstance(output, startai.Array)
    assert str(input_frontend.dtype) == str(output.dtype)
    assert startai.all(input_frontend.startai_array == output)

    startai.previous_backend()


@given(
    dim=st.integers(),
    keepdim=st.booleans(),
    input=st.lists(st.integers()),
    other=st.integers(),
)
def test_torch_numpy_to_torch_style_args(dim, keepdim, input, other):
    # PyTorch-style keyword arguments
    assert (dim, keepdim, input, other) == mocked_func(
        dim=dim, keepdim=keepdim, input=input, other=other
    )

    # NumPy-style keyword arguments
    assert (dim, keepdim, input, other) == mocked_func(
        axis=dim, keepdims=keepdim, x=input, x2=other
    )

    # Mixed-style keyword arguments
    assert (dim, keepdim, input, other) == mocked_func(
        axis=dim, keepdim=keepdim, input=input, x2=other
    )


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ).filter(lambda x: "bfloat16" not in x[0]),
    dtype=helpers.get_dtypes("valid", none=True, full=False, prune_function=False),
    generate_type=st.sampled_from(["frontend", "startai", "native"]),
    inplace=st.booleans(),
)
def test_torch_outputs_to_frontend_arrays(
    dtype_and_x,
    dtype,
    generate_type,
    inplace,
    backend_fw,
):
    x_dtype, x = dtype_and_x

    startai.set_backend(backend_fw)

    x = startai.array(x[0], dtype=x_dtype[0])
    if generate_type == "frontend":
        x = Tensor(x)
    elif generate_type == "native":
        x = x.data

    if not len(x.shape):
        scalar_x = startai.to_scalar(x.startai_array if isinstance(x, Tensor) else x)
        outputs_to_frontend_arrays(_fn)(
            scalar_x, scalar_x, check_default=True, dtype=dtype
        )
        outputs_to_frontend_arrays(_fn)(scalar_x, x, check_default=True, dtype=dtype)
    output = outputs_to_frontend_arrays(_fn)(
        x, check_default=True, dtype=dtype, inplace=inplace
    )
    assert isinstance(output, Tensor)
    if inplace:
        if generate_type == "frontend":
            assert x is output
        elif generate_type == "native":
            assert x is output.startai_array.data
        else:
            assert x is output.startai_array
    else:
        assert startai.as_startai_dtype(x.dtype) == startai.as_startai_dtype(output.dtype)
        if generate_type == "frontend":
            assert startai.all(x.startai_array == output.startai_array)
        elif generate_type == "native":
            assert startai.all(x == output.startai_array.data)
        else:
            assert startai.all(x == output.startai_array)

    assert startai.default_float_dtype_stack == startai.default_int_dtype_stack == []

    startai.previous_backend()


@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid", prune_function=False)
    ).filter(lambda x: "bfloat16" not in x[0]),
    dtype=helpers.get_dtypes("valid", none=True, full=False, prune_function=False),
)
def test_torch_to_startai_arrays_and_back(dtype_and_x, dtype, backend_fw):
    x_dtype, x = dtype_and_x

    startai.set_backend(backend_fw)

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
    assert isinstance(output, Tensor)
    assert str(input_startai.dtype) == str(output.dtype)
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
    assert isinstance(output, Tensor)
    assert startai.as_startai_dtype(input_native.dtype) == str(output.dtype)
    assert startai.all(input_native == output.startai_array.data)

    # check for frontend array
    input_frontend = Tensor(x[0])
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
    assert isinstance(output, Tensor)
    assert input_frontend.dtype == output.dtype
    assert startai.all(input_frontend.startai_array == output.startai_array)

    assert startai.default_float_dtype_stack == startai.default_int_dtype_stack == []

    startai.previous_backend()
