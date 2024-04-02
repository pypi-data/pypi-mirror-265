from typing import Union, Optional, Sequence
import mxnet as mx
from numbers import Number

# local
from startai.utils.exceptions import StartaiNotImplementedException
import startai


def min(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def max(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def mean(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def prod(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    dtype: Optional[None] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    dtype = startai.as_native_dtype(dtype)
    if dtype is None:
        dtype = x.dtype
    if dtype != x.dtype and not startai.is_bool_dtype(x):
        x = x.astype(dtype)
    if axis is None:
        num_dims = len(x.shape)
        axis = tuple(range(num_dims))
    elif isinstance(axis, Number):
        axis = (axis,)
    elif isinstance(axis, list):
        axis = tuple(axis)
    return mx.nd.prod(x, axis=axis, keepdims=keepdims).astype(dtype)


def std(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    correction: Union[(int, float)] = 0.0,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def sum(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    dtype: Optional[None] = None,
    keepdims: Optional[bool] = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    dtype = startai.as_native_dtype(dtype)
    if dtype is None:
        dtype = x.dtype
    if dtype != x.dtype and not startai.is_bool_dtype(x):
        x = x.astype(dtype)
    if axis is None:
        num_dims = len(x.shape)
        axis = tuple(range(num_dims))
    elif isinstance(axis, Number):
        axis = (axis,)
    elif isinstance(axis, list):
        axis = tuple(axis)
    return mx.nd.sum(x, axis=axis, keepdims=keepdims).astype(dtype)


def var(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    correction: Union[(int, float)] = 0.0,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def cumprod(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: int = 0,
    exclusive: bool = False,
    reverse: bool = False,
    dtype: Optional[None] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def cumsum(
    x: Union[(None, mx.ndarray.NDArray)],
    axis: int = 0,
    exclusive: bool = False,
    reverse: bool = False,
    *,
    dtype: Optional[None] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def einsum(
    equation: str,
    *operands: Union[(None, mx.ndarray.NDArray)],
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()
