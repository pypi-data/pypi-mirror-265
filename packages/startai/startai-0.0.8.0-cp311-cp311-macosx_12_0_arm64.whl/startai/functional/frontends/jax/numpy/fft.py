# local
import startai
from startai.functional.frontends.jax.func_wrapper import to_startai_arrays_and_back
from startai.func_wrapper import with_unsupported_dtypes


@to_startai_arrays_and_back
def fft(a, n=None, axis=-1, norm=None):
    if norm is None:
        norm = "backward"
    return startai.fft(a, axis, norm=norm, n=n)


@to_startai_arrays_and_back
def fft2(a, s=None, axes=(-2, -1), norm=None):
    if norm is None:
        norm = "backward"
    return startai.array(startai.fft2(a, s=s, dim=axes, norm=norm), dtype=startai.dtype(a))


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.6.0 and below": ("float16", "bfloat16")}, "paddle")
def fftfreq(n, d=1.0, *, dtype=None):
    if not isinstance(
        n, (int, type(startai.int8), type(startai.int16), type(startai.int32), type(startai.int64))
    ):
        raise TypeError("n should be an integer")

    dtype = startai.float64 if dtype is None else startai.as_startai_dtype(dtype)

    N = (n - 1) // 2 + 1
    val = 1.0 / (n * d)

    results = startai.zeros((n,), dtype=dtype)
    results[:N] = startai.arange(0, N, dtype=dtype)
    results[N:] = startai.arange(-(n // 2), 0, dtype=dtype)

    return results * val


@to_startai_arrays_and_back
@with_unsupported_dtypes({"2.4.2 and below": ("float16", "bfloat16")}, "paddle")
def fftshift(x, axes=None, name=None):
    shape = x.shape

    if axes is None:
        axes = tuple(range(x.ndim))
        shifts = [(dim // 2) for dim in shape]
    elif isinstance(axes, int):
        shifts = shape[axes] // 2
    else:
        shifts = [shape[ax] // 2 for ax in axes]

    roll = startai.roll(x, shifts, axis=axes)

    return roll


@to_startai_arrays_and_back
def ifft(a, n=None, axis=-1, norm=None):
    if norm is None:
        norm = "backward"
    return startai.ifft(a, axis, norm=norm, n=n)


@to_startai_arrays_and_back
def ifft2(a, s=None, axes=(-2, -1), norm=None):
    if norm is None:
        norm = "backward"
    return startai.array(startai.ifft2(a, s=s, dim=axes, norm=norm), dtype=startai.dtype(a))


@with_unsupported_dtypes({"1.24.3 and below": ("complex64", "bfloat16")}, "numpy")
@to_startai_arrays_and_back
def ifftn(a, s=None, axes=None, norm=None):
    a = startai.asarray(a, dtype=startai.complex128)
    a = startai.ifftn(a, s=s, axes=axes, norm=norm)
    return a


@to_startai_arrays_and_back
@with_unsupported_dtypes({"1.25.2 and below": ("float16", "bfloat16")}, "numpy")
def rfft(a, n=None, axis=-1, norm=None):
    if n is None:
        n = a.shape[axis]
    if norm is None:
        norm = "backward"
    result = startai.dft(
        a, axis=axis, inverse=False, onesided=False, dft_length=n, norm=norm
    )
    slices = [slice(0, a) for a in result.shape]
    slices[axis] = slice(0, int(startai.shape(result, as_array=True)[axis] // 2 + 1))
    result = result[tuple(slices)]
    return result
