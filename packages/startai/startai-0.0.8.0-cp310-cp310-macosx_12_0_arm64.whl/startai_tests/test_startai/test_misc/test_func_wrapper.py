import numpy as np

import startai
import pytest
from unittest.mock import patch
from startai.func_wrapper import handle_array_like_without_promotion
from typing import Union, Tuple, List, Sequence


# --- Helpers --- #
# --------------- #


def _fn1(x: Union[startai.Array, Tuple[int, int]]):
    return x


def _fn2(x: Union[startai.Array, startai.NativeArray]):
    return x


def _fn3(x: List[startai.Array]):
    return x


def _fn4(x: Union[Sequence[startai.Array], startai.Array]):
    return x


def _fn5(x):
    # Test input was converted to native array
    assert isinstance(x, startai.NativeArray)


def _fn6(x):
    # Assert input was converted to Startai Array
    assert isinstance(x, startai.Array)


def _fn7(x):
    # Assert input was converted to native array
    assert isinstance(x, startai.NativeArray)
    return x


def _fn8(x):
    return startai.ones_like(x)


def _jl(x, *args, fn_original, **kwargs):
    return fn_original(x) * 3j


# --- Main --- #
# ------------ #


@pytest.mark.parametrize(
    ("fn", "x", "expected_type"),
    [
        (_fn1, (1, 2), tuple),
        (_fn2, (1, 2), startai.Array),
        (_fn2, [1, 2], startai.Array),
        (_fn3, [1, 2], list),
        (_fn4, [1, 2], list),
    ],
)
def test_handle_array_like_without_promotion(fn, x, expected_type, backend_fw):
    startai.set_backend(backend_fw)
    assert isinstance(handle_array_like_without_promotion(fn)(x), expected_type)
    startai.previous_backend()


@pytest.mark.parametrize(
    ("x", "mode", "jax_like", "expected"),
    [
        ([3.0, 7.0, -5.0], None, None, [1.0, 1.0, 1.0]),
        ([3 + 4j, 7 - 6j, -5 - 2j], None, None, [1 + 0j, 1 + 0j, 1 + 0j]),
        ([3 + 4j, 7 - 6j, -5 - 2j], "split", None, [1 + 1j, 1 + 1j, 1 + 1j]),
        (
            [3 + 4j, 7 - 6j, -5 - 2j],
            "magnitude",
            None,
            [0.6 + 0.8j, 0.75926 - 0.65079j, -0.92848 - 0.37139j],
        ),
        ([3 + 4j, 7 - 6j, -5 - 2j], "jax", None, [1 + 0j, 1 + 0j, 1 + 0j]),
        ([3 + 4j, 7 - 6j, -5 - 2j], "jax", "entire", [1 + 0j, 1 + 0j, 1 + 0j]),
        ([3 + 4j, 7 - 6j, -5 - 2j], "jax", "split", [1 + 1j, 1 + 1j, 1 + 1j]),
        (
            [3 + 4j, 7 - 6j, -5 - 2j],
            "jax",
            "magnitude",
            [0.6 + 0.8j, 0.75926 - 0.65079j, -0.92848 - 0.37139j],
        ),
        ([3 + 4j, 7 - 6j, -5 - 2j], "jax", _jl, [3j, 3j, 3j]),
    ],
)
def test_handle_complex_input(x, mode, jax_like, expected, backend_fw):
    startai.set_backend(backend_fw)
    x = startai.array(x)
    expected = startai.array(expected)
    if jax_like is not None:
        _fn8.jax_like = jax_like
    elif hasattr(_fn8, "jax_like"):
        # _fn8 might have the jax_like attribute still attached from previous tests
        delattr(_fn8, "jax_like")
    test_fn = startai.handle_complex_input(_fn8)
    out = test_fn(x) if mode is None else test_fn(x, complex_mode=mode)
    if "float" in x.dtype:
        assert startai.all(out == expected)
    else:
        assert startai.all(
            startai.logical_or(
                startai.real(out) > startai.real(expected) - 1e-4,
                startai.real(out) < startai.real(expected) + 1e-4,
            )
        )
        assert startai.all(
            startai.logical_or(
                startai.imag(out) > startai.imag(expected) - 1e-4,
                startai.imag(out) < startai.imag(expected) + 1e-4,
            )
        )
    startai.previous_backend()


@pytest.mark.parametrize(
    ("x", "weight", "expected"),
    [
        ([[1, 1], [1, 1]], [[1, 1], [1, 1], [1, 1]], True),
        (
            [[1, 1], [1, 1]],
            [
                [[1, 1], [1, 1], [1, 1]],
                [[1, 1], [1, 1], [1, 1]],
                [[1, 1], [1, 1], [1, 1]],
            ],
            False,
        ),
    ],
)
def test_handle_partial_mixed_function(x, weight, expected, backend_fw):
    startai.set_backend(backend_fw)
    test_fn = "torch.nn.functional.linear"
    if startai.current_backend_str() != "torch":
        # startai.matmul is used inside the compositional implementation
        test_fn = "startai.matmul"
        expected = True
    with patch(test_fn) as test_mock_function:
        startai.linear(startai.array(x), startai.array(weight))
        assert test_mock_function.called == expected
    startai.previous_backend()


def test_inputs_to_startai_arrays(backend_fw):
    startai.set_backend(backend_fw)
    startai.inputs_to_startai_arrays(_fn6)(startai.native_array(1))
    startai.previous_backend()


def test_inputs_to_native_arrays(backend_fw):
    startai.set_backend(backend_fw)
    startai.inputs_to_native_arrays(_fn5)(startai.array(1))
    startai.previous_backend()


def test_outputs_to_startai_arrays(backend_fw):
    startai.set_backend(backend_fw)
    assert isinstance(
        startai.outputs_to_startai_arrays(_fn1)(startai.to_native(startai.array([2.0]))), startai.Array
    )
    assert startai.outputs_to_startai_arrays(_fn1)(startai.array(1)) == startai.array(1)
    startai.previous_backend()


def test_to_native_arrays_and_back(backend_fw):
    startai.set_backend(backend_fw)
    x = startai.array(1.0)
    res = startai.func_wrapper.to_native_arrays_and_back(_fn7)(x)
    assert isinstance(res, startai.Array)
    startai.previous_backend()


@pytest.mark.parametrize(
    "array_to_update",
    [0, 1, 2, 3, 4],
)
def test_views(array_to_update, backend_fw):
    startai.set_backend(backend_fw)
    a = startai.random.random_normal(shape=(6,))
    a_copy = startai.copy_array(a)
    b = a.reshape((2, 3))
    b_copy = startai.copy_array(b)
    c = startai.flip(b)
    c_copy = startai.copy_array(c)
    d = startai.rot90(c, k=3)
    d_copy = startai.copy_array(d)
    e = startai.split(d)
    e_copy = startai.copy_array(e[0])
    array = (a, b, c, d, e)[array_to_update]
    if array_to_update == 4:
        for arr in array:
            arr += 1
    else:
        array += 1
    assert np.allclose(a, a_copy + 1)
    assert np.allclose(b, b_copy + 1)
    assert np.allclose(c, c_copy + 1)
    assert np.allclose(d, d_copy + 1)
    assert np.allclose(e[0], e_copy + 1)
    startai.previous_backend()
