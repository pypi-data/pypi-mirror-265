# global
import startai
from startai.func_wrapper import with_supported_dtypes
from startai.functional.frontends.paddle.func_wrapper import (
    to_startai_arrays_and_back,
)


@with_supported_dtypes(
    {"2.6.0 and below": ("complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def fft(x, n=None, axis=-1.0, norm="backward", name=None):
    ret = startai.fft(startai.astype(x, "complex128"), axis, norm=norm, n=n)
    return startai.astype(ret, x.dtype)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def fft2(x, s=None, axes=(-2, -1), norm="backward", name=None):
    if axes is None:
        axes = (-2, -1)
    ret = startai.fft2(x, s=s, dim=axes, norm=norm)
    return ret


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def fftfreq(n, d=1.0, dtype=None, name=None):
    if d * n == 0:
        raise ValueError("d or n should not be 0.")

    if dtype is None:
        dtype = startai.default_dtype()
    val = 1.0 / (n * d)
    pos_max = (n + 1) // 2
    neg_max = n // 2
    indices = startai.arange(-neg_max, pos_max, dtype=dtype)
    indices = startai.roll(indices, -neg_max)
    return startai.multiply(indices, val)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "int32",
            "int64",
            "float32",
            "float64",
            "complex64",
            "complex128",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def fftshift(x, axes=None, name=None):
    shape = x.shape

    if axes is None:
        axes = tuple(range(x.ndim))
        shifts = [(dim // 2) for dim in shape]
    elif isinstance(axes, int):
        shifts = shape[axes] // 2
    else:
        shifts = startai.concat([shape[ax] // 2 for ax in axes])

    roll = startai.roll(x, shifts, axis=axes)

    return roll


@with_supported_dtypes(
    {"2.6.0 and below": ("complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def hfft(x, n=None, axes=-1, norm="backward", name=None):
    """Compute the FFT of a signal that has Hermitian symmetry, resulting in a
    real spectrum."""
    # Determine the input shape and axis length
    input_shape = x.shape
    input_len = input_shape[axes]

    # Calculate n if not provided
    if n is None:
        n = 2 * (input_len - 1)

    # Perform the FFT along the specified axis
    result = startai.fft(x, axes, n=n, norm=norm)

    return startai.real(result)


@with_supported_dtypes(
    {"2.6.0 and below": "complex64"},
    "paddle",
)
@to_startai_arrays_and_back
def hfft2(x, s=None, axis=(-2, -1), norm="backward"):
    # check if the input tensor x is a hermitian complex
    if not startai.allclose(startai.conj(startai.matrix_transpose(x)), x):
        raise ValueError("Input tensor x must be Hermitian complex.")

    fft_result = startai.fft2(x, s=s, dim=axis, norm=norm)

    # Depending on the norm, apply scaling and normalization
    if norm == "forward":
        fft_result /= startai.sqrt(startai.prod(startai.shape(fft_result)))
    elif norm == "ortho":
        fft_result /= startai.sqrt(startai.prod(startai.shape(x)))

    return startai.real(fft_result)  # Return the real part of the result


@with_supported_dtypes(
    {"2.6.0 and below": ("complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def ifft(x, n=None, axis=-1.0, norm="backward", name=None):
    ret = startai.ifft(startai.astype(x, "complex128"), axis, norm=norm, n=n)
    return startai.astype(ret, x.dtype)


@with_supported_dtypes(
    {"2.6.0 and below": ("complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def ifftn(x, s=None, axes=None, norm="backward", name=None):
    ret = startai.ifftn(startai.astype(x, "complex128"), s=s, axes=axes, norm=norm)
    return startai.astype(ret, x.dtype)


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def ifftshift(x, axes=None, name=None):
    shape = x.shape

    if axes is None:
        axes = tuple(range(x.ndim))
        shifts = [-(dim // 2) for dim in shape]
    elif isinstance(axes, int):
        shifts = -(shape[axes] // 2)
    else:
        shifts = startai.concat([-shape[ax] // 2 for ax in axes])

    roll = startai.roll(x, shifts, axis=axes)

    return roll


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def ihfft2(x, s=None, axes=(-2, -1), norm="backward", name=None):
    # check if the input array is two-dimensional and real
    if len(startai.array(x).shape) != 2 or startai.is_complex_dtype(x):
        raise ValueError("input must be a two-dimensional real array")

    # cast the input to the same float64 type so that there are no backend issues
    x_ = startai.astype(x, startai.float64)

    ihfft2_result = 0
    # Compute the complex conjugate of the 2-dimensional discrete Fourier Transform
    if norm == "backward":
        ihfft2_result = startai.conj(startai.rfftn(x_, s=s, axes=axes, norm="forward"))
    if norm == "forward":
        ihfft2_result = startai.conj(startai.rfftn(x_, s=s, axes=axes, norm="backward"))
    if norm == "ortho":
        ihfft2_result = startai.conj(startai.rfftn(x_, s=s, axes=axes, norm="ortho"))

    if x.dtype in [startai.float32, startai.int32, startai.int64]:
        return startai.astype(ihfft2_result, startai.complex64)
    if x.dtype == startai.float64:
        return startai.astype(ihfft2_result, startai.complex128)


@to_startai_arrays_and_back
def ihfftn(x, s=None, axes=None, norm="backward", name=None):
    # cast the input to the same float64 type so that there are no backend issues
    x_ = startai.astype(x, startai.float64)

    ihfftn_result = 0
    # Compute the complex conjugate of the 2-dimensional discrete Fourier Transform
    if norm == "backward":
        ihfftn_result = startai.conj(startai.rfftn(x_, s=s, axes=axes, norm="forward"))
    if norm == "forward":
        ihfftn_result = startai.conj(startai.rfftn(x_, s=s, axes=axes, norm="backward"))
    if norm == "ortho":
        ihfftn_result = startai.conj(startai.rfftn(x_, s=s, axes=axes, norm="ortho"))

    if x.dtype in [startai.float32, startai.int32, startai.int64]:
        return startai.astype(ihfftn_result, startai.complex64)
    if x.dtype == startai.float64:
        return startai.astype(ihfftn_result, startai.complex128)


@with_supported_dtypes(
    {"2.6.0 and below": ("complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def irfft(x, n=None, axis=-1.0, norm="backward", name=None):
    if n is None:
        n = 2 * (x.shape[axis] - 1)

    pos_freq_terms = startai.take_along_axis(x, range(n // 2 + 1), axis)
    neg_freq_terms = startai.conj(pos_freq_terms[1:-1][::-1])
    combined_freq_terms = startai.concat((pos_freq_terms, neg_freq_terms), axis=axis)
    time_domain = startai.ifft(combined_freq_terms, axis, norm=norm, n=n)
    if startai.isreal(x):
        time_domain = startai.real(time_domain)
    return time_domain


@with_supported_dtypes(
    {
        "2.6.0 and below": (
            "int32",
            "int64",
            "float16",
            "float32",
            "float64",
            "complex64",
            "complex128",
        )
    },
    "paddle",
)
@to_startai_arrays_and_back
def irfft2(x, s=None, axes=(-2, -1), norm="backward"):
    # Handle values if None
    if s is None:
        s = x.shape
    if axes is None:
        axes = (-2, -1)

    # Calculate the normalization factor 'n' based on the shape 's'
    n = startai.prod(startai.array(s))

    result = startai.ifftn(x, axes=axes[0], norm=norm)

    # Normalize the result based on the 'norm' parameter
    if norm == "backward":
        result /= n
    elif norm == "forward":
        result *= n
    elif norm == "ortho":
        result /= startai.sqrt(n)
    return result


@with_supported_dtypes(
    {"2.6.0 and below": ("complex64", "complex128")},
    "paddle",
)
@to_startai_arrays_and_back
def irfftn(x, s=None, axes=None, norm="backward", name=None):
    x = startai.array(x)

    if axes is None:
        axes = list(range(len(x.shape)))

    include_last_axis = len(x.shape) - 1 in axes

    if s is None:
        s = [
            x.shape[axis] if axis != (len(x.shape) - 1) else 2 * (x.shape[axis] - 1)
            for axis in axes
        ]

    real_result = x
    remaining_axes = [axis for axis in axes if axis != (len(x.shape) - 1)]

    if remaining_axes:
        real_result = startai.ifftn(
            x,
            s=[s[axes.index(axis)] for axis in remaining_axes],
            axes=remaining_axes,
            norm=norm,
        )

    if include_last_axis:
        axis = len(x.shape) - 1
        size = s[axes.index(axis)]
        freq_domain = startai.moveaxis(real_result, axis, -1)
        slices = [slice(None)] * startai.get_num_dims(freq_domain)
        slices[-1] = slice(0, size // 2 + 1)
        pos_freq_terms = freq_domain[tuple(slices)]
        slices[-1] = slice(1, -1)
        neg_freq_terms = startai.conj(pos_freq_terms[tuple(slices)][..., ::-1])
        combined_freq_terms = startai.concat((pos_freq_terms, neg_freq_terms), axis=-1)
        real_result = startai.ifftn(combined_freq_terms, s=[size], axes=[-1], norm=norm)
        real_result = startai.moveaxis(real_result, -1, axis)

    if startai.is_complex_dtype(x.dtype):
        output_dtype = "float32" if x.dtype == "complex64" else "float64"
    else:
        output_dtype = "float32"

    result_t = startai.astype(real_result, output_dtype)
    return result_t


@with_supported_dtypes({"2.6.0 and below": ("float32", "float64")}, "paddle")
@to_startai_arrays_and_back
def rfft(x, n=None, axis=-1, norm="backward", name=None):
    return startai.dft(x, axis=axis, inverse=False, onesided=True, dft_length=n, norm=norm)


@to_startai_arrays_and_back
def rfftfreq(n, d=1.0, dtype=None, name=None):
    dtype = startai.default_dtype()
    val = 1.0 / (n * d)
    pos_max = n // 2 + 1
    indices = startai.arange(0, pos_max, dtype=dtype)
    return indices * val
