"""Collection of tests for unified device functions."""

# global
import io
import multiprocessing
import os
import re
import shutil
import sys
import warnings

import numpy as np
import psutil
import subprocess
from hypothesis import strategies as st, assume

# nvidia-ml-py (pynvml) is not installed in CPU Dockerfile.

# local
import startai
import startai_tests.test_startai.helpers as helpers
import startai_tests.test_startai.helpers.globals as test_globals
from startai_tests.test_startai.helpers import handle_test, BackendHandler

try:
    import pynvml
except ImportError:
    warnings.warn(
        "pynvml installation was not found in the environment, functionalities"
        " of the Startai's device module will be limited. Please install pynvml if"
        " you wish to use GPUs with Startai."
    )


# --- Helpers --- #
# --------------- #


# Function Splitting #


@st.composite
def _axis(draw):
    max_val = draw(st.shared(helpers.ints(), key="num_dims"))
    return draw(helpers.ints(min_value=0, max_value=max_val - 1))


def _composition_1(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        return startai_backend.relu().argmax()


def _composition_2(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        return startai_backend.ceil() or startai_backend.floor()


def _empty_dir(path, recreate=False):
    # Delete the directory if it exists and create it again if recreate is True
    if os.path.exists(path):
        shutil.rmtree(path)
    if recreate:
        os.makedirs(path)


def _get_possible_devices():
    # Return all the possible usable devices
    with BackendHandler.update_backend(test_globals.CURRENT_BACKEND) as startai_backend:
        devices = ["cpu"]
        if startai_backend.gpu_is_available():
            for i in range(startai_backend.num_gpus()):
                devices.append("gpu:" + str(i))

        # Return a list of startai devices
        return list(map(startai_backend.Device, devices))


def _ram_array_and_clear_test(metric_fn, device, size=10000000):
    # This function checks if the memory usage changes before, during and after

    # Measure usage before creating array
    before = metric_fn()
    # Create an array of floats, by default with 10 million elements (40 MB)
    arr = startai.random_normal(shape=(size,), dtype="float32", device=device)
    during = metric_fn()
    # Check that the memory usage has increased
    assert before < during

    # Delete the array
    del arr
    # Measure the memory usage after the array is deleted
    after = metric_fn()
    # Check that the memory usage has decreased
    assert during > after


# --- Main --- #
# ------------ #


def get_cpu_percent():
    output = str(subprocess.check_output(["top", "-bn1"]))
    cpu_percent = float(re.search(r"%Cpu\(s\):\s+([\d.]+)\s+us", output).group(1))
    return cpu_percent


def get_gpu_mem_usage(backend, device="gpu:0"):
    handle = backend.startai.functional.startai.device._get_nvml_gpu_handle(device)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return (info.used / info.total) * 100


# as_startai_dev
@handle_test(
    fn_tree="functional.startai.as_startai_dev",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
    ),
)
def test_as_startai_dev(*, dtype_and_x, test_flags, backend_fw):
    dtype, x = dtype_and_x
    dtype = dtype[0]
    x = x[0]

    with BackendHandler.update_backend(backend_fw) as startai_backend:
        for device in _get_possible_devices():
            x = startai_backend.array(x, device=device)
            if test_flags.as_variable and startai_backend.is_float_dtype(dtype):
                x = startai_backend.functional.startai.gradients._variable(x)

            native_device = startai_backend.dev(x, as_native=True)
            ret = startai_backend.as_startai_dev(native_device)

            # Type test
            assert isinstance(ret, str)
            # Value test
            assert ret == device


# as_native_dev
@handle_test(
    fn_tree="functional.startai.as_native_dev",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
    ),
)
def test_as_native_dev(*, dtype_and_x, test_flags, on_device, backend_fw):
    dtype, x = dtype_and_x
    dtype = dtype[0]
    x = x[0]

    with BackendHandler.update_backend(backend_fw) as startai_backend:
        for device in _get_possible_devices():
            x = startai_backend.asarray(x, device=on_device)
            if test_flags.as_variable:
                x = startai_backend.functional.startai.gradients._variable(x)

            device = startai_backend.as_native_dev(on_device)
            ret = startai_backend.as_native_dev(startai_backend.dev(x))
            # value test
            if backend_fw == "tensorflow":
                assert "/" + ":".join(ret[1:].split(":")[-2:]) == "/" + ":".join(
                    device[1:].split(":")[-2:]
                )
            elif backend_fw == "torch":
                assert ret.type == device.type
            elif backend_fw == "paddle":
                assert ret._equals(device)
            else:
                assert ret == device


@handle_test(fn_tree="clear_cached_mem_on_dev")
def test_clear_cached_mem_on_dev(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        devices = _get_possible_devices()
        for device in devices:
            # Testing on only GPU since clearing cache mem is relevant
            # for only CUDA devices
            if "gpu" in device:
                arr = startai_backend.random_normal(  # noqa: F841
                    shape=(10000, 1000), dtype="float32", device=device
                )
                del arr
                before = get_gpu_mem_usage(device)
                startai_backend.clear_cached_mem_on_dev(device)
                after = get_gpu_mem_usage(device)
                assert before > after


# Device Allocation #
# default_device
@handle_test(fn_tree="functional.startai.default_device")
def test_default_device(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        # setting and unsetting
        orig_len = len(startai_backend.default_device_stack)
        startai_backend.set_default_device("cpu")
        assert len(startai_backend.default_device_stack) == orig_len + 1
        startai_backend.set_default_device("cpu")
        assert len(startai_backend.default_device_stack) == orig_len + 2
        startai_backend.unset_default_device()
        assert len(startai_backend.default_device_stack) == orig_len + 1
        startai_backend.unset_default_device()
        assert len(startai_backend.default_device_stack) == orig_len

        # with
        assert len(startai_backend.default_device_stack) == orig_len
        with startai_backend.DefaultDevice("cpu"):
            assert len(startai_backend.default_device_stack) == orig_len + 1
            with startai_backend.DefaultDevice("cpu"):
                assert len(startai_backend.default_device_stack) == orig_len + 2
            assert len(startai_backend.default_device_stack) == orig_len + 1
        assert len(startai_backend.default_device_stack) == orig_len


# Tests #
# ------#

# Device Queries #


# dev
@handle_test(
    fn_tree="functional.startai.dev",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
    ),
)
def test_dev(*, dtype_and_x, test_flags, backend_fw):
    dtype, x = dtype_and_x
    dtype = dtype[0]
    x = x[0]

    with BackendHandler.update_backend(backend_fw) as startai_backend:
        for device in _get_possible_devices():
            x = startai_backend.array(x, device=device)
            if test_flags.as_variable and startai_backend.is_float_dtype(dtype):
                x = startai_backend.functional.startai.gradients._variable(x)

            ret = startai_backend.dev(x)
            # type test
            assert isinstance(ret, str)
            # value test
            assert ret == device
            # array instance test
            assert x.dev() == device
            # container instance test
            container_x = startai_backend.Container({"a": x})
            assert container_x.dev() == device
            # container static test
            assert startai_backend.Container.static_dev(container_x) == device


@handle_test(fn_tree="dev_util")
def test_dev_util(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        devices = _get_possible_devices()
        for device in devices:
            # The internally called psutil.cpu_percent() has a unique behavior where it
            # returns 0 as usage when run the second time in same line so simple
            # assert psutil.cpu_percent() == startai.dev_util(device) isn't possible
            if "cpu" in device:
                assert 100 >= startai_backend.dev_util(device) >= 0
                # Comparing CPU utilization using top. Two percentiles won't be directly
                # equal but absolute difference should be below a safe threshold
                assert abs(get_cpu_percent() - startai_backend.dev_util(device)) < 10
            elif "gpu" in device:
                handle = startai_backend.functional.startai.device._get_nvml_gpu_handle(device)
                assert (
                    startai_backend.dev_util(device)
                    == pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
                )


# function_unsupported_devices
@handle_test(
    fn_tree="functional.startai.function_supported_devices",
    func=st.sampled_from([_composition_1, _composition_2]),
    expected=st.just(["cpu"]),
)
def test_function_supported_devices(
    *,
    func,
    expected,
    backend_fw,
):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        res = startai_backend.function_supported_devices(func)
        exp = set(expected)

        assert sorted(exp) == sorted(res)


# function_unsupported_devices
@handle_test(
    fn_tree="functional.startai.function_supported_devices",
    func=st.sampled_from([_composition_1, _composition_2]),
    expected=st.just(["gpu", "tpu"]),
)
def test_function_unsupported_devices(
    *,
    func,
    expected,
    backend_fw,
):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        res = startai_backend.function_unsupported_devices(func)
        exp = set(expected)

        assert sorted(exp) == sorted(res)


@handle_test(
    fn_tree="functional.startai.get_all_startai_arrays_on_dev",
    num=helpers.ints(min_value=0, max_value=5),
)
def test_get_all_startai_arrays_on_dev(
    *,
    num,
    on_device,
    backend_fw,
):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        arrays = [startai_backend.array(np.random.uniform(size=2)) for _ in range(num)]
        arr_ids_on_dev = [
            id(a) for a in startai_backend.get_all_startai_arrays_on_dev(on_device).values()
        ]
        for a in arrays:
            assert id(a) in arr_ids_on_dev


@handle_test(fn_tree="gpu_is_available")
def test_gpu_is_available(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        # If gpu is available but cannot be initialised it will fail the test
        if startai_backend.gpu_is_available():
            try:
                pynvml.nvmlInit()
            except pynvml.NVMLError:
                assert False


# handle_soft_device_variable
@handle_test(
    fn_tree="functional.startai.handle_soft_device_variable",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
    ),
)
def test_handle_soft_device_variable(*, dtype_and_x, backend_fw):
    dtype, x = dtype_and_x
    dtype = dtype[0]
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        x = startai_backend.to_device(x[0], "cpu")

        def fn(x, y):
            return startai_backend.add(x, y)

        for device in _get_possible_devices():
            startai_backend.set_default_device(device)
            out = startai_backend.handle_soft_device_variable(x, fn=fn, y=x)

            # check if device shifting is successful
            assert out.device == startai_backend.default_device()


@handle_test(fn_tree="num_cpu_cores")
def test_num_cpu_cores(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        # using multiprocessing module too because startai uses psutil as basis.
        p_cpu_cores = psutil.cpu_count()
        m_cpu_cores = multiprocessing.cpu_count()
        assert isinstance(startai_backend.num_cpu_cores(), int)
        assert startai_backend.num_cpu_cores() == p_cpu_cores
        assert startai_backend.num_cpu_cores() == m_cpu_cores


@handle_test(
    fn_tree="functional.startai.num_startai_arrays_on_dev",
    num=helpers.ints(min_value=0, max_value=5),
)
def test_num_startai_arrays_on_dev(
    *,
    num,
    on_device,
    backend_fw,
):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        arrays = [
            startai_backend.array(np.random.uniform(size=2).tolist(), device=on_device)
            for _ in range(num)
        ]
        assert startai_backend.num_startai_arrays_on_dev(on_device) == num
        for item in arrays:
            del item


@handle_test(fn_tree="percent_used_mem_on_dev")
def test_percent_used_mem_on_dev(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        devices = _get_possible_devices()

        for device in devices:
            used = startai_backend.percent_used_mem_on_dev(startai_backend.Device(device))
            assert 0 <= used <= 100

            # Same as test_used_mem_on_dev, but using percent of total memory as metric
            # function
            _ram_array_and_clear_test(
                lambda: startai_backend.percent_used_mem_on_dev(
                    device, process_specific=True
                ),
                device=device,
            )


@handle_test(
    fn_tree="functional.startai.print_all_startai_arrays_on_dev",
    num=helpers.ints(min_value=0, max_value=2),
    attr_only=st.booleans(),
)
def test_print_all_startai_arrays_on_dev(
    *,
    num,
    attr_only,
    on_device,
    backend_fw,
):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        arr = [startai_backend.array(np.random.uniform(size=2)) for _ in range(num)]

        # Flush to avoid artifact
        sys.stdout.flush()
        # temporarily redirect output to a buffer
        captured_output = io.StringIO()
        sys.stdout = captured_output

        startai_backend.print_all_startai_arrays_on_dev(device=on_device, attr_only=attr_only)
        # Flush again to make sure all data is printed
        sys.stdout.flush()
        written = captured_output.getvalue().splitlines()
        # restore stdout
        sys.stdout = sys.__stdout__

        # Should have written same number of lines as the number of array in device
        assert len(written) == num

        if attr_only:
            # Check that the attribute are printed are in the format of
            # (startai.Shape(dim,...), type)
            regex = r"^\(startai.Shape\((\d+,(\d,\d*)*)\), \'\w*\'\)$"
        else:
            # Check that the arrays are printed are in the format of startai.array(...)
            regex = r"^startai\.array\(\[.*\]\)$"

        # Clear the array from device
        for item in arr:
            del item

        # Apply the regex search
        assert all(re.match(regex, line) for line in written)


# profiler
@handle_test(
    fn_tree="functional.startai.Profiler",
)
def test_profiler(*, backend_fw):
    # ToDo: find way to prevent this test from hanging when run
    #  alongside other tests in parallel

    # log dir, each framework uses their own folder,
    # so we can run this test in parallel
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        this_dir = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(this_dir, "../log")
        fw_log_dir = os.path.join(log_dir, backend_fw)

        # Remove old content and recreate log dir
        _empty_dir(fw_log_dir, True)

        # with statement
        with startai_backend.Profiler(fw_log_dir):
            a = startai_backend.ones([10])
            b = startai_backend.zeros([10])
            _ = a + b

        # Should have content in folder
        assert len(os.listdir(fw_log_dir)) != 0, "Profiler did not log anything"

        # Remove old content and recreate log dir
        _empty_dir(fw_log_dir, True)

        # Profiler should stop log
        assert (
            len(os.listdir(fw_log_dir)) == 0
        ), "Profiler logged something while stopped"

        # start and stop methods
        profiler = startai_backend.Profiler(fw_log_dir)
        profiler.start()
        a = startai_backend.ones([10])
        b = startai_backend.zeros([10])
        _ = a + b
        profiler.stop()

        # Should have content in folder
        assert len(os.listdir(fw_log_dir)) != 0, "Profiler did not log anything"

        # Remove old content including the logging folder
        _empty_dir(fw_log_dir, False)

        assert not os.path.exists(fw_log_dir), "Profiler recreated logging folder"


@handle_test(
    fn_tree="functional.startai.split_func_call",
    array_shape=helpers.lists(
        x=helpers.ints(min_value=1, max_value=3),
        min_size="num_dims",
        max_size="num_dims",
        size_bounds=[1, 3],
    ),
    dtype=helpers.get_dtypes("numeric", full=False),
    chunk_size=helpers.ints(min_value=1, max_value=3),
    axis=_axis(),
)
def test_split_func_call(
    *,
    array_shape,
    dtype,
    chunk_size,
    axis,
    test_flags,
    backend_fw,
):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        # inputs
        shape = tuple(array_shape)
        x1 = np.random.uniform(size=shape).astype(dtype[0])
        x2 = np.random.uniform(size=shape).astype(dtype[0])
        x1 = startai_backend.asarray(x1)
        x2 = startai_backend.asarray(x2)
        if test_flags.as_variable and startai_backend.is_float_dtype(dtype[0]):
            x1 = startai_backend.functional.startai.gradients._variable(x1)
            x2 = startai_backend.functional.startai.gradients._variable(x2)

        # function
        def func(t0, t1):
            return t0 * t1, t0 - t1, t1 - t0

        # predictions
        a, b, c = startai_backend.split_func_call(
            func, [x1, x2], "concat", chunk_size=chunk_size, input_axes=axis
        )

        # true
        a_true, b_true, c_true = func(x1, x2)

        # value test
        helpers.assert_all_close(
            startai_backend.to_numpy(a), startai_backend.to_numpy(a_true), backend=backend_fw
        )
        helpers.assert_all_close(
            startai_backend.to_numpy(b), startai_backend.to_numpy(b_true), backend=backend_fw
        )
        helpers.assert_all_close(
            startai_backend.to_numpy(c), startai_backend.to_numpy(c_true), backend=backend_fw
        )


@handle_test(
    fn_tree="functional.startai.split_func_call",
    array_shape=helpers.lists(
        x=helpers.ints(min_value=2, max_value=3),
        min_size="num_dims",
        max_size="num_dims",
        size_bounds=[2, 3],
    ),
    dtype=helpers.get_dtypes("numeric", full=False),
    chunk_size=helpers.ints(min_value=1, max_value=3),
    axis=helpers.ints(min_value=0, max_value=1),
)
def test_split_func_call_with_cont_input(
    *,
    array_shape,
    test_flags,
    dtype,
    chunk_size,
    axis,
    on_device,
    backend_fw,
):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        shape = tuple(array_shape)
        x1 = np.random.uniform(size=shape).astype(dtype[0])
        x2 = np.random.uniform(size=shape).astype(dtype[0])
        x1 = startai_backend.asarray(x1, device=on_device)
        x2 = startai_backend.asarray(x2, device=on_device)
        # inputs

        if test_flags.as_variable and startai_backend.is_float_dtype(dtype[0]):
            _variable_fn = startai_backend.functional.startai.gradients._variable
            in0 = startai_backend.Container(cont_key=_variable_fn(x1))
            in1 = startai_backend.Container(cont_key=_variable_fn(x2))
        else:
            in0 = startai_backend.Container(cont_key=x1)
            in1 = startai_backend.Container(cont_key=x2)

        # function
        def func(t0, t1):
            return t0 * t1, t0 - t1, t1 - t0

        # predictions
        a, b, c = startai.split_func_call(
            func, [in0, in1], "concat", chunk_size=chunk_size, input_axes=axis
        )

        # true
        a_true, b_true, c_true = func(in0, in1)

        # value test
        helpers.assert_all_close(
            startai_backend.to_numpy(a.cont_key),
            startai_backend.to_numpy(a_true.cont_key),
            backend=backend_fw,
        )
        helpers.assert_all_close(
            startai_backend.to_numpy(b.cont_key),
            startai_backend.to_numpy(b_true.cont_key),
            backend=backend_fw,
        )
        helpers.assert_all_close(
            startai_backend.to_numpy(c.cont_key),
            startai_backend.to_numpy(c_true.cont_key),
            backend=backend_fw,
        )


# to_dev
@handle_test(
    fn_tree="functional.startai.to_device",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
    ),
    stream=helpers.ints(min_value=0, max_value=50),
)
def test_to_device(
    *,
    dtype_and_x,
    stream,
    test_flags,
    backend_fw,
    on_device,
):
    dtype, x = dtype_and_x
    dtype = dtype[0]
    x = x[0]

    with BackendHandler.update_backend(backend_fw) as startai_backend:
        x = startai_backend.asarray(x)
        if test_flags.as_variable and startai_backend.is_float_dtype(dtype):
            x = startai_backend.functional.startai.gradients._variable(x)

        # create a dummy array for out that is broadcastable to x
        out = (
            startai_backend.zeros(startai_backend.shape(x), device=on_device, dtype=dtype)
            if test_flags.with_out
            else None
        )

        device = startai_backend.dev(x)
        x_on_dev = startai_backend.to_device(x, on_device, stream=stream, out=out)
        dev_from_new_x = startai_backend.dev(x_on_dev)

        if test_flags.with_out:
            # should be the same array test
            assert x_on_dev is out

            # should be the same device
            if backend_fw != "paddle":
                assert startai_backend.dev(x_on_dev, as_native=True) == startai_backend.dev(
                    out, as_native=True
                )
            else:
                assert startai_backend.dev(x_on_dev, as_native=False) == startai_backend.dev(
                    out, as_native=False
                )

            # check if native arrays are the same
            # these backends do not support native inplace updates
            assume(backend_fw not in ["tensorflow", "jax"])

            assert x_on_dev.data is out.data

        # value test
        if backend_fw == "tensorflow":
            assert "/" + ":".join(dev_from_new_x[1:].split(":")[-2:]) == "/" + ":".join(
                device[1:].split(":")[-2:]
            )
        elif backend_fw == "torch":
            assert type(dev_from_new_x) == type(device)  # noqa: E721
        else:
            assert dev_from_new_x == device

        # array instance test
        assert x.to_device(device).dev() == device
        # container instance test
        container_x = startai_backend.Container({"x": x})
        assert container_x.to_device(device).dev() == device
        # container static test
        assert startai_backend.Container.to_device(container_x, device).dev() == device


@handle_test(fn_tree="total_mem_on_dev")
def test_total_mem_on_dev(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        devices = _get_possible_devices()
        for device in devices:
            if "cpu" in device:
                assert (
                    startai_backend.total_mem_on_dev(device)
                    == psutil.virtual_memory().total / 1e9
                )
            elif "gpu" in device:
                handle = startai_backend.functional.startai.device._get_nvml_gpu_handle(device)
                gpu_mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                assert startai_backend.total_mem_on_dev(device) == gpu_mem.total / 1e9


@handle_test(fn_tree="tpu_is_available")
def test_tpu_is_available(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        import tensorflow as tf

        try:
            resolver = tf.distribute.cluster_resolver.TPUClusterResolver()
            tf.config.experimental_connect_to_cluster(resolver)
            tf.tpu.experimental.initialize_tpu_system(resolver)
            tf.config.list_logical_devices("TPU")
            tf.distribute.experimental.TPUStrategy(resolver)
            ground_truth = True
        except ValueError:
            ground_truth = False

        assert startai_backend.tpu_is_available() == ground_truth


@handle_test(fn_tree="used_mem_on_dev")
def test_used_mem_on_dev(backend_fw):
    with BackendHandler.update_backend(backend_fw) as startai_backend:
        devices = _get_possible_devices()

        # Check that there not all memory is used
        for device in devices:
            assert startai_backend.used_mem_on_dev(device) > 0
            assert startai_backend.used_mem_on_dev(device) < startai_backend.total_mem_on_dev(
                device
            )

            _ram_array_and_clear_test(
                lambda: startai_backend.used_mem_on_dev(device, process_specific=True),
                device=device,
            )
