"""Collection of tests for utility functions."""

# global
from hypothesis import strategies as st

# local
import startai_tests.test_startai.helpers as helpers
from startai_tests.test_startai.helpers import handle_test


# all
@handle_test(
    fn_tree="functional.startai.all",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        valid_axis=True,
        max_axes_size=1,
    ),
    keepdims=st.booleans(),
    test_gradients=st.just(False),
)
def test_all(dtype_x_axis, keepdims, test_flags, backend_fw, fn_name, on_device):
    input_dtype, x, axis = dtype_x_axis
    axis = axis if axis is None or isinstance(axis, int) else axis[0]
    helpers.test_function(
        input_dtypes=input_dtype,
        test_flags=test_flags,
        backend_to_test=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        x=x[0],
        axis=axis,
        keepdims=keepdims,
    )


# any
@handle_test(
    fn_tree="functional.startai.any",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid", full=True),
        valid_axis=True,
        max_axes_size=1,
    ),
    keepdims=st.booleans(),
    test_gradients=st.just(False),
)
def test_any(dtype_x_axis, keepdims, test_flags, backend_fw, fn_name, on_device):
    input_dtype, x, axis = dtype_x_axis
    axis = axis if axis is None or isinstance(axis, int) else axis[0]
    helpers.test_function(
        input_dtypes=input_dtype,
        test_flags=test_flags,
        backend_to_test=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        x=x[0],
        axis=axis,
        keepdims=keepdims,
    )
