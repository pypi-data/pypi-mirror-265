# local
import startai.functional.frontends.numpy as np_frontend
import startai


def asmatrix(data, dtype=None):
    return np_frontend.matrix(startai.array(data), dtype=dtype, copy=False)


def asscalar(a):
    return a.item()
