"""Collection of MXNet gradient functions, wrapped to fit Startai syntax and
signature."""

# global
from typing import Sequence, Union
import mxnet as mx

# local
from startai.utils.exceptions import StartaiNotImplementedException


def variable(x, /):
    return x


def is_variable(x, /, *, exclusive=False):
    return isinstance(x, mx.ndarray.NDArray)


def variable_data(x, /):
    raise StartaiNotImplementedException()


def execute_with_gradients(
    func,
    xs,
    /,
    *,
    retain_grads: bool = False,
    xs_grad_idxs: Sequence[Sequence[Union[str, int]]] = ((0,),),
    ret_grad_idxs: Sequence[Sequence[Union[str, int]]] = ((0,),),
):
    raise StartaiNotImplementedException()


def value_and_grad(func):
    raise StartaiNotImplementedException()


def jac(func):
    raise StartaiNotImplementedException()


def grad(func, argnums=0):
    raise StartaiNotImplementedException()


def stop_gradient(x, /, *, preserve_type=True, out=None):
    raise StartaiNotImplementedException()
