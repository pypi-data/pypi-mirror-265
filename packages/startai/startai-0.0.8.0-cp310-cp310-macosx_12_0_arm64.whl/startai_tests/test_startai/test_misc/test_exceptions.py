import sys
import os
import contextlib
import pytest
import startai


@pytest.mark.parametrize("trace_mode", ["full", "startai", "frontend"])
def test_get_trace_mode(trace_mode, backend_fw):
    startai.set_backend(backend_fw)
    startai.set_exception_trace_mode(trace_mode)
    startai.set_exception_trace_mode("startai")
    startai.utils.assertions.check_equal(startai.exception_trace_mode, "startai", as_array=False)
    startai.previous_backend()


@pytest.mark.parametrize("trace_mode", ["full", "startai", "frontend"])
def test_set_trace_mode(trace_mode, backend_fw):
    startai.set_backend(backend_fw)
    startai.set_exception_trace_mode(trace_mode)
    startai.utils.assertions.check_equal(
        startai.exception_trace_mode, trace_mode, as_array=False
    )
    startai.previous_backend()


@pytest.mark.parametrize("trace_mode", ["full", "startai", "frontend"])
@pytest.mark.parametrize("show_func_wrapper", [True, False])
def test_trace_modes(backend_fw, trace_mode, show_func_wrapper):
    startai.set_backend(backend_fw)
    filename = "excep_out.txt"
    orig_stdout = sys.stdout
    with open(filename, "w") as f:
        sys.stdout = f
        startai.set_exception_trace_mode(trace_mode)
        startai.set_show_func_wrapper_trace_mode(show_func_wrapper)
        x = startai.array([])
        y = startai.array([1.0, 3.0, 4.0])
        lines = ""
        try:
            startai.divide(x, y)
        except Exception as e:
            print(e)
        sys.stdout = orig_stdout
    with open(filename) as f:
        lines += f.read()

    if trace_mode == "full" and not show_func_wrapper:
        assert "/func_wrapper.py" not in lines
        assert "/startai/functional/backends" in lines
        if backend_fw.current_backend_str() not in ["torch", "numpy"]:
            assert "/dist-packages" in lines

    if trace_mode == "full" and show_func_wrapper:
        assert "/func_wrapper.py" in lines
        assert "/startai/functional/backends" in lines
        if backend_fw.current_backend_str() not in ["torch", "numpy"]:
            assert "/dist-packages" in lines

    if trace_mode in ["startai", "frontend"]:
        if not show_func_wrapper:
            assert "/func_wrapper.py" not in lines
            assert "/dist-packages" not in lines

        if show_func_wrapper:
            if trace_mode == "frontend":
                assert "/startai/functional/backends" not in lines
            else:
                assert "/func_wrapper.py" in lines
            assert "/dist-packages" not in lines

    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)
    startai.previous_backend()


@pytest.mark.parametrize("trace_mode", ["full", "startai", "frontend"])
def test_unset_trace_mode(trace_mode, backend_fw):
    startai.set_backend(backend_fw)
    startai.set_exception_trace_mode(trace_mode)
    startai.set_exception_trace_mode("startai")
    startai.utils.assertions.check_equal(startai.exception_trace_mode, "startai", as_array=False)
    startai.unset_exception_trace_mode()
    startai.utils.assertions.check_equal(
        startai.exception_trace_mode, trace_mode, as_array=False
    )
    startai.previous_backend()
