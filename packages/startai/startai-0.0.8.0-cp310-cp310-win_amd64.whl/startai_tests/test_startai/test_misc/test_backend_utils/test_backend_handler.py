# global
from packaging import version
import pytest
import importlib
import types
import numpy as np

# local
import startai
from startai.utils.backend.handler import _backend_dict

# TODO fix due to refactor
from startai_tests.test_startai.helpers.available_frameworks import _available_frameworks


try:
    import tensorflow as tf
except ImportError:
    tf = types.SimpleNamespace()
    tf.constant = lambda x: x
try:
    import torch
except ImportError:
    torch = types.SimpleNamespace()
    torch.tensor = lambda x: x
try:
    import jax.numpy as jnp
    import jax
except ImportError:
    jnp = types.SimpleNamespace()
    jnp.array = lambda x: x
    jax = types.SimpleNamespace()
try:
    import paddle
except ImportError:
    paddle = types.SimpleNamespace()
    paddle.Tensor = lambda x: x

available_array_types_class = [
    ("numpy", "<class 'numpy.ndarray'>"),
]
available_array_types_input = [
    ("numpy", np.array(3.0)),
]
available_frameworks_with_none = _available_frameworks()[:]
# Dynamic Backend

backends = list(_backend_dict.keys())


@pytest.mark.parametrize("excluded", available_frameworks_with_none)
def test_choose_random_backend(excluded):
    backend = startai.choose_random_backend(excluded=excluded)
    if excluded is None:
        assert backend in list(_backend_dict.keys())
    else:
        backends_list = list(_backend_dict.keys())
        backends_list.remove(excluded)
        assert backend in backends_list


@pytest.mark.parametrize(
    ("backend", "array_type"),
    available_array_types_input,
)
def test_current_backend(backend, array_type):
    # test backend inference from arguments when stack clear
    startai.unset_backend()
    assert startai.current_backend(array_type) is importlib.import_module(
        _backend_dict[backend]
    )

    # global_backend > argument's backend.
    if "torch" in _available_frameworks():
        startai.set_backend("torch")
        startai.utils.assertions.check_equal(
            startai.current_backend(array_type),
            importlib.import_module(_backend_dict["torch"]),
            as_array=False,
        )
    else:
        startai.set_backend("numpy")
        startai.utils.assertions.check_equal(
            startai.current_backend(array_type),
            importlib.import_module(_backend_dict["numpy"]),
            as_array=False,
        )


@pytest.mark.parametrize(
    ("middle_backend", "end_backend"),
    [(a, b) for a in backends for b in backends if (a != b and "mxnet" not in [a, b])],
)
def test_dynamic_backend_all_combos(middle_backend, end_backend):
    # create an startai array, container and native container
    a = startai.array([1, 2, 3])
    b = startai.array([4, 5, 6])
    startai_cont = startai.Container({"w": a, "b": b})

    # clear the backend stack after initialization of inputs
    startai.unset_backend()

    # set dynamic_backend to false for all objects
    startai_cont.dynamic_backend = False
    a.dynamic_backend = False
    b.dynamic_backend = False

    # set the middle backend
    startai.set_backend(middle_backend, dynamic=True)
    var_cont = startai.Container(
        {
            "w": startai.gradients._variable(startai.array([10, 20, 30])),
            "b": startai.gradients._variable(startai.array([40, 50, 60])),
        }
    )
    # set dynamic_backend to true for all objects
    startai_cont.dynamic_backend = True
    a.dynamic_backend = True
    b.dynamic_backend = True

    # set the final backend
    startai.set_backend(end_backend, dynamic=True)

    # add the necessary asserts to check if the data
    # of the objects are in the correct format

    assert isinstance(a.data, startai.NativeArray)
    assert isinstance(startai_cont["b"].data, startai.NativeArray)

    if {"numpy", "jax"}.intersection([middle_backend, end_backend]):
        # these frameworks don't support native variables
        assert isinstance(var_cont["b"].data, startai.NativeArray)
    else:
        assert startai.gradients._is_variable(var_cont["b"])


def test_dynamic_backend_context_manager():
    with startai.dynamic_backend_as(True):
        a = startai.array([0.0, 1.0])
        b = startai.array([2.0, 3.0])

    with startai.dynamic_backend_as(False):
        c = startai.array([4.0, 5.0])
        d = startai.array([6.0, 7.0])

    assert a.dynamic_backend is True
    assert b.dynamic_backend is True
    assert c.dynamic_backend is False
    assert d.dynamic_backend is False


def test_dynamic_backend_setter():
    a = startai.array([1, 2, 3])
    type_a = type(a.data)
    a.dynamic_backend = False

    # clear the backend stack after initialization of inputs
    startai.unset_backend()

    startai.set_backend("tensorflow", dynamic=True)
    assert type(a.data) == type_a  # noqa: E721

    a.dynamic_backend = True
    assert isinstance(a.data, tf.Tensor)

    startai.set_backend("torch", dynamic=True)
    assert isinstance(a.data, torch.Tensor)


@pytest.mark.parametrize("backend", _available_frameworks())
def test_previous_backend(backend):
    if not startai.backend_stack:
        assert startai.previous_backend() is None

    startai.set_backend(backend)
    stack_before_unset = []
    func_address_before_unset = id(startai.sum)
    stack_before_unset.extend(startai.backend_stack)

    previous_backend = startai.previous_backend()
    stack_after_unset = startai.backend_stack
    # check that the function id has changed as inverse=True.
    startai.utils.assertions.check_equal(
        func_address_before_unset, id(startai.sum), inverse=True, as_array=False
    )
    startai.utils.assertions.check_equal(
        previous_backend,
        importlib.import_module(_backend_dict[backend]),
        as_array=False,
    )
    startai.utils.assertions.check_greater(
        len(stack_before_unset), len(stack_after_unset), as_array=False
    )

    # checking a previously set backend is still set
    startai.set_backend(backend)
    startai.set_backend("numpy")
    startai.previous_backend()
    startai.utils.assertions.check_equal(startai.current_backend_str(), backend, as_array=False)


@pytest.mark.parametrize(
    (
        "backend",
        "array_type",
    ),
    available_array_types_class,
)
def test_set_backend(backend, array_type):
    # recording data before backend change
    stack_before = []
    func_address_before = id(startai.sum)
    stack_before.extend(startai.backend_stack)

    startai.set_backend(backend)
    stack_after = startai.backend_stack
    # check that the function id has changed as inverse=True.
    startai.utils.assertions.check_equal(
        func_address_before, id(startai.sum), inverse=True, as_array=False
    )
    # using startai assertions to ensure the desired backend is set
    startai.utils.assertions.check_less(len(stack_before), len(stack_after), as_array=False)
    startai.utils.assertions.check_equal(startai.current_backend_str(), backend, as_array=False)
    backend = importlib.import_module(_backend_dict[backend])
    startai.utils.assertions.check_equal(stack_after[-1], backend, as_array=False)
    x = startai.array([1, 2, 3])
    startai.utils.assertions.check_equal(
        str(type(startai.to_native(x))), array_type, as_array=False
    )


@pytest.mark.parametrize("backend", ["torch", "numpy"])
def test_set_backend_no_warning_when_inplace_update_supported(backend):
    with pytest.warns(None):
        startai.set_backend(backend)


def test_set_backend_throw_warning_only_once_when_inplace_update_not_supported(
    backend_fw,
):
    def _assert_number_of_inplace_warnings_is(n):
        inplace_update_warning_counter = 0
        for item in record:
            if "inplace update" in str(item.message):
                inplace_update_warning_counter += 1
        assert inplace_update_warning_counter == n

    if backend_fw in ["tensorflow", "paddle", "jax"]:
        with pytest.warns(UserWarning) as record:
            startai.set_backend(backend_fw)
            startai.set_backend(backend_fw)
        _assert_number_of_inplace_warnings_is(1)


def test_unset_backend():
    for backend_str in _available_frameworks():
        startai.set_backend(backend_str)

    startai.unset_backend()
    startai.utils.assertions.check_equal(startai.backend_stack, [], as_array=False)


def test_variables():
    # clear the backend stack
    startai.unset_backend()

    startai.set_backend("tensorflow", dynamic=True)

    a = tf.Variable(0)
    b = tf.Variable(1)

    dyn_cont = startai.Container({"w": a, "b": b})
    stat_cont = startai.Container({"w": a, "b": b})
    stat_cont.dynamic_backend = False

    startai.set_backend("torch", dynamic=True)
    assert startai.current_backend().gradients.is_variable(dyn_cont["w"].data)

    startai.set_backend("paddle", dynamic=True)
    assert startai.current_backend().gradients.is_variable(dyn_cont["w"].data)

    assert isinstance(stat_cont["w"], tf.Variable)


available_frameworks_with_none.append(None)

if "tensorflow" in _available_frameworks():
    available_array_types_input.append(("tensorflow", tf.constant([3.0])))
    available_array_types_class.append(
        ("tensorflow", "<class 'tensorflow.python.framework.ops.EagerTensor'>")
    )

if "jax" in _available_frameworks():
    available_array_types_input.append(("jax", jnp.array(3.0)))
    if version.parse(jax.__version__) >= version.parse("0.4.1"):
        available_array_types_class.append(
            ("jax", "<class 'jaxlib.xla_extension.ArrayImpl'>")
        )
    else:
        available_array_types_class.append(
            ("jax", "<class 'jaxlib.xla_extension.DeviceArray'>")
        )


if "torch" in _available_frameworks():
    available_array_types_input.append(("torch", torch.tensor([3.0])))
    available_array_types_class.append(("torch", "<class 'torch.Tensor'>"))

if "paddle" in _available_frameworks():
    available_array_types_input.append(("paddle", paddle.to_tensor([3.0])))
    available_array_types_class.append(("paddle", "<class 'paddle.Tensor'>"))
