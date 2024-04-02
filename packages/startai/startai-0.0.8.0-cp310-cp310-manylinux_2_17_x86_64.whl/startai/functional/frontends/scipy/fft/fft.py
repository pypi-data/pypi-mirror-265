# global
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back

import startai


# dct
@to_startai_arrays_and_back
def dct(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False, orthogonalize=None):
    return startai.dct(x, type=type, n=n, axis=axis, norm=norm)


# fft
@to_startai_arrays_and_back
def fft(x, n=None, axis=-1, norm="backward", overwrite_x=False):
    return startai.fft(x, axis, norm=norm, n=n)


@to_startai_arrays_and_back
def fft2(x, s=None, axes=(-2, -1), norm=None, overwrite_x=False):
    return startai.fft2(x, s=s, dim=axes, norm=norm)


# idct
@to_startai_arrays_and_back
def idct(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False, orthogonalize=None):
    inverse_type = {1: 1, 2: 3, 3: 2, 4: 4}[type]
    return startai.dct(x, type=inverse_type, n=n, axis=axis, norm=norm)


# ifft
@to_startai_arrays_and_back
def ifft(x, n=None, axis=-1, norm=None, overwrite_x=False):
    return startai.ifft(x, axis, norm=norm, n=n)


@to_startai_arrays_and_back
def ifftn(
    x, s=None, axes=None, norm=None, overwrite_x=False, workers=None, *, plan=None
):
    return startai.ifftn(x, s=s, axes=axes, norm=norm)


@to_startai_arrays_and_back
def rfftn(
    x, s=None, axes=None, norm=None, overwrite_x=False, workers=None, *, plan=None
):
    return startai.rfftn(x, s=s, axes=axes, norm=norm)
