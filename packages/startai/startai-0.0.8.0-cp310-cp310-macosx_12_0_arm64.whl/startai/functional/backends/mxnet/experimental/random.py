from typing import Union, Optional, Sequence
import mxnet as mx

import startai
from startai.utils.exceptions import StartaiNotImplementedException


def dirichlet(
    alpha: Union[(None, mx.ndarray.NDArray, float, Sequence[float])],
    /,
    *,
    size: Optional[Union[(startai.NativeShape, Sequence[int])]] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
    seed: Optional[int] = None,
    dtype: Optional[None] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def beta(
    alpha: Union[(float, None, mx.ndarray.NDArray)],
    beta: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    shape: Optional[Union[(startai.NativeShape, Sequence[int])]] = None,
    device: Optional[str] = None,
    dtype: Optional[Union[(None, startai.Dtype)]] = None,
    seed: Optional[int] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def gamma(
    alpha: Union[(float, None, mx.ndarray.NDArray)],
    beta: Union[(float, None, mx.ndarray.NDArray)],
    /,
    *,
    shape: Optional[Union[(startai.NativeShape, Sequence[int])]] = None,
    device: Optional[str] = None,
    dtype: Optional[Union[(None, startai.Dtype)]] = None,
    seed: Optional[int] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def poisson(
    lam: Union[(float, None, mx.ndarray.NDArray)],
    *,
    shape: Optional[Union[(startai.NativeShape, Sequence[int])]] = None,
    device: str,
    dtype: None,
    seed: Optional[int] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()


def bernoulli(
    probs: Union[(float, None, mx.ndarray.NDArray)],
    *,
    logits: Union[(float, None, mx.ndarray.NDArray)] = None,
    shape: Optional[Union[(startai.NativeShape, Sequence[int])]] = None,
    device: str,
    dtype: None,
    seed: Optional[int] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise StartaiNotImplementedException()
