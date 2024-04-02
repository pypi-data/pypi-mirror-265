import startai
from startai.func_wrapper import with_supported_dtypes, with_unsupported_dtypes
from startai.functional.frontends.torch.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def bartlett_window(
    window_length,
    periodic=True,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False
):
    # this implementation is based on scipy.signal.windows.bartlett
    # https://github.com/scipy/scipy/blob/v1.11.2/scipy/signal/windows/_windows.py#L625-L721
    if int(window_length) != window_length or window_length < 0:
        raise ValueError("Window length must be a non-negative integer")
    elif window_length == 1:
        return startai.ones(window_length)
    else:
        N = window_length + 1 if periodic else window_length

        res = startai.arange(0, N, dtype=dtype)
        res = startai.where(
            startai.less_equal(res, (N - 1) / 2.0),
            2.0 * res / (N - 1),
            2.0 - 2.0 * res / (N - 1),
        )

        return res[:-1] if periodic else res


@to_startai_arrays_and_back
@with_supported_dtypes({"2.51.0 and below": ("float32", "float64")}, "torch")
def blackman_window(
    window_length,
    periodic=True,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False
):
    return startai.blackman_window(window_length, periodic=periodic, dtype=dtype)


@to_startai_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def hamming_window(
    window_length,
    periodic=True,
    alpha=0.54,
    beta=0.46,
):
    return startai.hamming_window(
        window_length,
        periodic=periodic,
        alpha=alpha,
        beta=beta,
    )


@to_startai_arrays_and_back
@with_supported_dtypes({"2.51.0 and below": ("float32", "float64")}, "torch")
def kaiser_window(
    window_length,
    periodic=True,
    beta=12.0,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False
):
    return startai.kaiser_window(window_length, periodic=periodic, beta=beta, dtype=dtype)
