# global
import functools
from typing import Callable

# local
import startai
import startai.functional.frontends.torch as torch_frontend


numpy_compatible_args = {
    "axis": "dim",
    "keepdims": "keepdim",
    "x": "input",
    "a": "input",
    "x1": "input",
    "x2": "other",
}


class AccumulateGrad:
    def __init__(self) -> None:
        self.next_functions = ()
        self.__name__ = "AccumulateGrad"

    def __repr__(self):
        return self.__name__

    def __eq__(self, __value: object) -> bool:
        return self.__name__ == __value

    def __call__(self, grads):
        self.__self__._grads = grads
        return None


class GradFn:
    def __init__(self, fn, args, kwargs) -> None:
        self._inputs = []
        self._fns = []
        self.next_functions = []
        for idx, input in [*enumerate(args), *kwargs.items()]:
            if isinstance(input, torch_frontend.Tensor) and input.requires_grad:
                self._inputs.append(input.detach())

                def wrap_fn(idx):
                    def d_fn(x):
                        if idx in kwargs:
                            return fn(
                                *args,
                                **{
                                    key: value
                                    for key, value in kwargs.items()
                                    if key != idx
                                },
                                idx=x,
                            )
                        return fn(*args[:idx], x, *args[idx + 1 :], **kwargs)

                    return d_fn

                self._fns.append(to_startai_arrays_and_back(startai.jac(wrap_fn(idx))))
                if input.grad_fn is not None:
                    self.next_functions.append(input.grad_fn)
                elif input.is_leaf:
                    acc_grad = AccumulateGrad()
                    acc_grad.__self__ = input
                    self.next_functions.append(acc_grad)
        self.__name__ = fn.__name__.capitalize() + "Backward"

    def __call__(self, prev_grads):
        result = []
        for input_tensor, jac_fn in zip(self._inputs, self._fns):
            jacobian = jac_fn(input_tensor)
            dims = list(range(jacobian.dim()))
            permuted_dims = dims[input_tensor.dim() :] + dims[: input_tensor.dim()]
            result.append(
                (
                    jacobian.permute(dims=permuted_dims).reshape(
                        shape=(*input_tensor.shape, -1)
                    )
                    * prev_grads.ravel()
                ).sum(-1)
            )
        return result

    def __repr__(self):
        return self.__name__

    def __eq__(self, __value: object) -> bool:
        return self.__name__ == __value


# --- Helpers --- #
# --------------- #


def _from_startai_array_to_torch_frontend_tensor(
    x, nested=False, include_derived=None, requires_grad=False
):
    if nested:
        return startai.nested_map(
            functools.partial(
                _from_startai_array_to_torch_frontend_tensor, requires_grad=requires_grad
            ),
            x,
            include_derived,
            shallow=False,
        )
    elif isinstance(x, startai.Array) or startai.is_native_array(x):
        a = torch_frontend.Tensor(x, _init_overload=True, requires_grad=requires_grad)
        return a
    return x


def _to_startai_array(x):
    # if x is a native array return it as an startai array
    if isinstance(x, startai.NativeArray):
        return startai.array(x)

    # else if x is a frontend torch Tensor (or any frontend "Tensor" actually) return the wrapped startai array # noqa: E501
    elif hasattr(x, "startai_array"):
        return x.startai_array
    # else just return x
    return x


# --- Main --- #
# ------------ #


def inputs_to_startai_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _inputs_to_startai_arrays_torch(*args, **kwargs):
        """Convert `Tensor` into `startai.Array` instances.

        Convert all `Tensor` instances in both the positional and keyword arguments
        into `startai.Array` instances, and then call the function with the updated
        arguments.
        """
        # convert all input arrays to startai.Array instances
        new_args = startai.nested_map(
            _to_startai_array, args, include_derived={"tuple": True}, shallow=False
        )
        new_kwargs = startai.nested_map(
            _to_startai_array, kwargs, include_derived={"tuple": True}, shallow=False
        )
        return fn(*new_args, **new_kwargs)

    _inputs_to_startai_arrays_torch.inputs_to_startai_arrays_torch = True
    return _inputs_to_startai_arrays_torch


# noqa: F811
def numpy_to_torch_style_args(func):  # noqa
    """Convert argument names from NumPy style to PyTorch style."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_kwargs = {
            numpy_compatible_args.get(key, key): value for key, value in kwargs.items()
        }
        return func(*args, **new_kwargs)

    wrapper.numpy_to_torch_style_args = True
    return wrapper


def outputs_to_frontend_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def outputs_to_frontend_arrays_torch(*args, **kwargs):
        """Convert `startai.Array` into `Tensor` instances.

        Call the function, and then convert all `startai.Array` instances returned by the
        function into `Tensor` instances.
        """
        # call unmodified function
        # ToDo: Remove this default dtype setting
        #  once frontend specific backend setting is added
        set_default_dtype = False
        if not ("dtype" in kwargs and startai.exists(kwargs["dtype"])) and all(
            not (startai.is_array(i) or hasattr(i, "startai_array")) for i in args
        ):
            if startai.current_backend_str() == "jax":
                import jax

                jax.config.update("jax_enable_x64", True)
            startai.set_default_int_dtype("int64")
            startai.set_default_float_dtype(torch_frontend.get_default_dtype())
            set_default_dtype = True
        try:
            ret = fn(*args, **kwargs)
        finally:
            if set_default_dtype:
                startai.unset_default_int_dtype()
                startai.unset_default_float_dtype()
        # convert all arrays in the return to `torch_frontend.Tensor` instances
        ret = _from_startai_array_to_torch_frontend_tensor(
            ret,
            nested=True,
            include_derived={"tuple": True},
            requires_grad=kwargs.get(
                "requires_grad",
                any(
                    isinstance(i, torch_frontend.Tensor) and i.requires_grad
                    for i in args
                ),
            ),
        )

        def array_fn(x):
            return startai.is_array(x) or hasattr(x, "startai_array")

        if "inplace" in kwargs and kwargs["inplace"]:
            first_array = startai.func_wrapper._get_first_array(
                *args, array_fn=array_fn, **kwargs
            )
            native_ret_data = ret.startai_array.data
            if startai.is_startai_array(first_array):
                first_array.data = native_ret_data
            elif startai.is_native_array(first_array):
                startai.inplace_update(first_array, native_ret_data)
                ret = torch_frontend.Tensor(first_array, _init_overload=True)
            else:
                first_array.startai_array.data = native_ret_data
                ret = first_array

        # logic for setting is_leaf
        if ret is not None and isinstance(ret, torch_frontend.Tensor):
            if fn.__name__ in dir(torch_frontend.creation_ops):
                ret.is_leaf = True
            elif all(
                not isinstance(i, torch_frontend.Tensor)
                or (not i.requires_grad and not i.grad_fn)
                for i in args
            ):
                ret.is_leaf = True
            else:
                ret.is_leaf = False
        # set grad_fn
        if any(
            isinstance(i, torch_frontend.Tensor) and i.requires_grad
            for i in [*args, *kwargs.values()]
        ):
            # ToDo: Implement for unbind
            grad_fn = GradFn(fn, args, kwargs)
            grad_fn.__self__ = ret
            ret.grad_fn = grad_fn

        return ret

    outputs_to_frontend_arrays_torch.outputs_to_frontend_arrays_torch = True
    return outputs_to_frontend_arrays_torch


def outputs_to_native_arrays(fn: Callable):
    @functools.wraps(fn)
    def outputs_to_native_arrays_torch(*args, **kwargs):
        ret = fn(*args, **kwargs)
        if isinstance(ret, torch_frontend.Tensor):
            ret = ret.startai_array.data
        return ret

    outputs_to_native_arrays_torch.outputs_to_native_arrays_torch = True
    return outputs_to_native_arrays_torch


def to_startai_arrays_and_back(fn: Callable) -> Callable:
    """Wrap `fn` so it receives and returns `startai.Array` instances.

    Wrap `fn` so that input arrays are all converted to `startai.Array` instances and
    return arrays are all converted to `Tensor` instances.
    """
    return outputs_to_frontend_arrays(inputs_to_startai_arrays(fn))


def to_startai_shape(fn: Callable) -> Callable:
    """Wrap `fn` so it receives `startai.Shape` instances.

    Wrap `fn` so that any `torch_frontend.Size` arguments are converted to
    `startai.Shape` instances.
    """

    @functools.wraps(fn)
    def to_startai_shape_torch(*args, **kwargs):
        new_kwargs = {
            key: (
                value.startai_shape
                if key in ["shape", "size"]
                and isinstance(value, startai.functional.frontends.torch.Size)
                else value
            )
            for key, value in kwargs.items()
        }
        # if any of the args are instance of torch_frontend.Size,
        # convert them to startai.Shape.
        new_args = startai.nested_map(
            lambda x: (
                x.startai_shape if isinstance(x, startai.functional.frontends.torch.Size) else x
            ),
            args,
            shallow=False,
        )
        return fn(*new_args, **new_kwargs)

    to_startai_shape_torch.to_startai_shape_torch = True
    return to_startai_shape_torch
