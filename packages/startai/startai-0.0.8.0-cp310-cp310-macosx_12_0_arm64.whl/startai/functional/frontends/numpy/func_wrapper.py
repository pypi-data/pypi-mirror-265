# global
import functools
from typing import Callable, Any
import inspect
import platform

# local
import startai
import startai.functional.frontends.numpy as np_frontend


# --- Helpers --- #
# --------------- #


# general casting
def _assert_array(args, dtype, scalar_check=False, casting="safe"):
    if args and dtype:
        if not scalar_check:
            startai.utils.assertions.check_all_or_any_fn(
                *args,
                fn=lambda x: np_frontend.can_cast(
                    x, startai.as_startai_dtype(dtype), casting=casting
                ),
                type="all",
                message=f"type of input is incompatible with dtype: {dtype}",
            )
        else:
            assert_fn = None if casting == "safe" else startai.exists
            if startai.is_bool_dtype(dtype):
                assert_fn = startai.is_bool_dtype
            if startai.is_int_dtype(dtype):

                def assert_fn(x):  # noqa F811
                    return not startai.is_float_dtype(x)

            if assert_fn:
                startai.utils.assertions.check_all_or_any_fn(
                    *args,
                    fn=lambda x: (
                        assert_fn(x)
                        if startai.shape(x) == ()
                        else np_frontend.can_cast(
                            x, startai.as_startai_dtype(dtype), casting=casting
                        )
                    ),
                    type="all",
                    message=f"type of input is incompatible with dtype: {dtype}",
                )


# no casting
def _assert_no_array(args, dtype, scalar_check=False, none=False):
    if args:
        first_arg = args[0]
        fn_func = startai.as_startai_dtype(dtype) if startai.exists(dtype) else startai.dtype(first_arg)

        def assert_fn(x):
            return startai.dtype(x) == fn_func

        if scalar_check:

            def assert_fn(x):  # noqa F811
                return (
                    startai.dtype(x) == fn_func
                    if startai.shape(x) != ()
                    else _casting_no_special_case(startai.dtype(x), fn_func, none)
                )

        startai.utils.assertions.check_all_or_any_fn(
            *args,
            fn=assert_fn,
            type="all",
            message=f"type of input is incompatible with dtype: {dtype}",
        )


def _assert_no_scalar(args, dtype, none=False):
    if args:
        first_arg = args[0]
        startai.utils.assertions.check_all_or_any_fn(
            *args,
            fn=lambda x: type(x) == type(first_arg),  # noqa: E721
            type="all",
            message=f"type of input is incompatible with dtype: {dtype}",
        )
        if dtype:
            if startai.is_int_dtype(dtype):
                check_dtype = int
            elif startai.is_float_dtype(dtype):
                check_dtype = float
            else:
                check_dtype = bool
            startai.utils.assertions.check_equal(
                type(args[0]),
                check_dtype,
                message=f"type of input is incompatible with dtype: {dtype}",
                as_array=False,
            )
            if startai.as_startai_dtype(dtype) not in ["float64", "int8", "int64", "uint8"]:
                if isinstance(args[0], int):
                    startai.utils.assertions.check_elem_in_list(
                        dtype,
                        ["int16", "int32", "uint16", "uint32", "uint64"],
                        inverse=True,
                    )
                elif isinstance(args[0], float):
                    startai.utils.assertions.check_equal(
                        dtype, "float32", inverse=True, as_array=False
                    )


def _assert_scalar(args, dtype):
    if args and dtype:
        assert_fn = None
        if startai.is_int_dtype(dtype):

            def assert_fn(x):  # noqa F811
                return not isinstance(x, float)

        elif startai.is_bool_dtype(dtype):

            def assert_fn(x):
                return isinstance(x, bool)

        if assert_fn:
            startai.utils.assertions.check_all_or_any_fn(
                *args,
                fn=assert_fn,
                type="all",
                message=f"type of input is incompatible with dtype: {dtype}",
            )


def _casting_no_special_case(dtype1, dtype, none=False):
    if dtype == "float16":
        allowed_dtypes = ["float32", "float64"]
        if not none:
            allowed_dtypes += ["float16"]
        return dtype1 in allowed_dtypes
    if dtype in ["int8", "uint8"]:
        if none:
            return startai.is_int_dtype(dtype1) and dtype1 not in ["int8", "uint8"]
        return startai.is_int_dtype(dtype1)
    return dtype1 == dtype


def _check_C_order(x):
    if isinstance(x, startai.Array):
        return True
    elif isinstance(x, np_frontend.ndarray):
        if x._f_contiguous:
            return False
        else:
            return True
    else:
        return None


def _count_operands(subscript):
    if "->" in subscript:
        input_subscript, output_index = subscript.split("->")
    else:
        input_subscript = subscript
    return len(input_subscript.split(","))


def _startai_to_numpy(x: Any) -> Any:
    if isinstance(x, startai.Array) or startai.is_native_array(x):
        a = np_frontend.ndarray(x, _init_overload=True)
        return a
    else:
        return x


def _startai_to_numpy_order_F(x: Any) -> Any:
    if isinstance(x, startai.Array) or startai.is_native_array(x):
        a = np_frontend.ndarray(
            0, order="F"
        )  # TODO Find better initialisation workaround
        a.startai_array = x
        return a
    else:
        return x


def _native_to_startai_array(x):
    if isinstance(x, startai.NativeArray):
        return startai.array(x)
    return x


def _numpy_frontend_to_startai(x: Any) -> Any:
    if hasattr(x, "startai_array"):
        return x.startai_array
    else:
        return x


def _set_order(args, order):
    startai.utils.assertions.check_elem_in_list(
        order,
        ["C", "F", "A", "K", None],
        message="order must be one of 'C', 'F', 'A', or 'K'",
    )
    if order in ["K", "A", None]:
        check_order = startai.nested_map(
            _check_C_order, args, include_derived={"tuple": True}, shallow=False
        )
        if all(v is None for v in check_order) or any(
            startai.multi_index_nest(check_order, startai.all_nested_indices(check_order))
        ):
            order = "C"
        else:
            order = "F"
    return order


def _to_startai_array(x):
    return _numpy_frontend_to_startai(_native_to_startai_array(x))


# --- Main --- #
# ------------ #


def from_zero_dim_arrays_to_scalar(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _from_zero_dim_arrays_to_scalar(*args, **kwargs):
        """Call the function, and then convert all 0 dimensional array
        instances in the function to float numbers if out argument is not
        provided.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with 0 dimensional arrays as float numbers.
        """
        # call unmodified function
        ret = fn(*args, **kwargs)

        if ("out" in kwargs and kwargs["out"] is None) or "out" not in kwargs:
            if isinstance(ret, tuple):
                # converting every scalar element of the tuple to float
                data = tuple(startai.native_array(i) for i in ret)
                data = startai.copy_nest(data, to_mutable=True)
                ret_idx = startai.nested_argwhere(data, lambda x: x.shape == ())
                try:
                    startai.map_nest_at_indices(
                        data,
                        ret_idx,
                        lambda x: np_frontend.numpy_dtype_to_scalar[startai.dtype(x)](x),
                    )
                except KeyError as e:
                    raise startai.utils.exceptions.StartaiException(
                        "Casting to specified type is unsupported"
                    ) from e
                return tuple(data)
            else:
                # converting the scalar to float
                data = startai.native_array(ret)
                if data.shape == ():
                    try:
                        return np_frontend.numpy_dtype_to_scalar[startai.dtype(data)](data)
                    except KeyError as e:
                        raise startai.utils.exceptions.StartaiException(
                            f"Casting to {startai.dtype(data)} is unsupported"
                        ) from e
        return ret

    _from_zero_dim_arrays_to_scalar.from_zero_dim_arrays_to_scalar = True
    return _from_zero_dim_arrays_to_scalar


def handle_numpy_casting(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_numpy_casting(*args, casting="same_kind", dtype=None, **kwargs):
        """Check numpy casting type.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, or raise StartaiException if error is thrown.
        """
        startai.utils.assertions.check_elem_in_list(
            casting,
            ["no", "equiv", "safe", "same_kind", "unsafe"],
            message="casting must be one of [no, equiv, safe, same_kind, unsafe]",
        )
        args = list(args)
        args_scalar_idxs = startai.nested_argwhere(
            args, lambda x: isinstance(x, (int, float, bool))
        )
        args_scalar_to_check = startai.multi_index_nest(args, args_scalar_idxs)
        args_idxs = startai.nested_argwhere(args, startai.is_array)
        args_to_check = startai.multi_index_nest(args, args_idxs)

        if casting in ["no", "equiv"]:
            none = not dtype
            if none:
                dtype = args_to_check[0].dtype if args_to_check else None
            _assert_no_array(
                args_to_check,
                dtype,
                scalar_check=(args_to_check and args_scalar_to_check),
                none=none,
            )
            _assert_no_scalar(args_scalar_to_check, dtype, none=none)
        elif casting in ["same_kind", "safe"]:
            _assert_array(
                args_to_check,
                dtype,
                scalar_check=(args_to_check and args_scalar_to_check),
                casting=casting,
            )
            _assert_scalar(args_scalar_to_check, dtype)

        if startai.exists(dtype):
            startai.map_nest_at_indices(
                args, args_idxs, lambda x: startai.astype(x, startai.as_startai_dtype(dtype))
            )

        return fn(*args, **kwargs)

    _handle_numpy_casting.handle_numpy_casting = True
    return _handle_numpy_casting


def handle_numpy_casting_special(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_numpy_casting_special(*args, casting="same_kind", dtype=None, **kwargs):
        """Check numpy casting type for special cases where output must be type
        bool.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, or raise StartaiException if error is thrown.
        """
        startai.utils.assertions.check_elem_in_list(
            casting,
            ["no", "equiv", "safe", "same_kind", "unsafe"],
            message="casting must be one of [no, equiv, safe, same_kind, unsafe]",
        )
        if startai.exists(dtype):
            startai.utils.assertions.check_equal(
                startai.as_startai_dtype(dtype),
                "bool",
                message="output is compatible with bool only",
                as_array=False,
            )

        return fn(*args, **kwargs)

    _handle_numpy_casting_special.handle_numpy_casting_special = True
    return _handle_numpy_casting_special


def handle_numpy_dtype(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_numpy_dtype(*args, dtype=None, **kwargs):
        if len(args) > (dtype_pos + 1):
            dtype = args[dtype_pos]
            kwargs = {
                **dict(
                    zip(
                        list(inspect.signature(fn).parameters.keys())[
                            dtype_pos + 1 : len(args)
                        ],
                        args[dtype_pos + 1 :],
                    )
                ),
                **kwargs,
            }
            args = args[:dtype_pos]
        elif len(args) == (dtype_pos + 1):
            dtype = args[dtype_pos]
            args = args[:-1]
        return fn(*args, dtype=np_frontend.to_startai_dtype(dtype), **kwargs)

    dtype_pos = list(inspect.signature(fn).parameters).index("dtype")
    _handle_numpy_dtype.handle_numpy_dtype = True
    return _handle_numpy_dtype


def handle_numpy_out(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_numpy_out(*args, **kwargs):
        if "out" not in kwargs:
            keys = list(inspect.signature(fn).parameters.keys())
            if fn.__name__ == "einsum":
                out_pos = 1 + _count_operands(args[0])
            else:
                out_pos = keys.index("out")
            kwargs = {
                **dict(
                    zip(
                        keys[keys.index("out") :],
                        args[out_pos:],
                    )
                ),
                **kwargs,
            }
            args = args[:out_pos]
        return fn(*args, **kwargs)

    _handle_numpy_out.handle_numpy_out = True
    return _handle_numpy_out


def inputs_to_startai_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _inputs_to_startai_arrays_np(*args, **kwargs):
        """Convert all `ndarray` instances in both the positional and keyword
        arguments into `startai.Array` instances, and then call the function with
        the updated arguments.

        Parameters
        ----------
        args
            The arguments to be passed to the function.
        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with startai arrays passed in the arguments.
        """
        # convert all arrays in the inputs to startai.Array instances
        startai_args = startai.nested_map(_to_startai_array, args, include_derived={"tuple": True})
        startai_kwargs = startai.nested_map(
            _to_startai_array, kwargs, include_derived={"tuple": True}
        )
        return fn(*startai_args, **startai_kwargs)

    _inputs_to_startai_arrays_np.inputs_to_startai_arrays_numpy = True
    return _inputs_to_startai_arrays_np


def outputs_to_frontend_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _outputs_to_frontend_arrays(*args, order="K", **kwargs):
        """Call the function, and then convert all `startai.Array` instances
        returned by the function into `ndarray` instances.

        Returns
        -------
            The return of the function, with startai arrays as numpy arrays.
        """
        # handle order and call unmodified function
        # ToDo: Remove this default dtype setting
        #  once frontend specific backend setting is added
        set_default_dtype = False
        if not ("dtype" in kwargs and startai.exists(kwargs["dtype"])) and any(
            not (startai.is_array(i) or hasattr(i, "startai_array")) for i in args
        ):
            if startai.current_backend_str() == "jax":
                import jax

                jax.config.update("jax_enable_x64", True)
            (
                startai.set_default_int_dtype("int64")
                if platform.system() != "Windows"
                else startai.set_default_int_dtype("int32")
            )
            startai.set_default_float_dtype("float64")
            set_default_dtype = True
        if contains_order:
            if len(args) >= (order_pos + 1):
                order = args[order_pos]
                args = args[:-1]
            order = _set_order(args, order)
            try:
                ret = fn(*args, order=order, **kwargs)
            finally:
                if set_default_dtype:
                    startai.unset_default_int_dtype()
                    startai.unset_default_float_dtype()
        else:
            try:
                ret = fn(*args, **kwargs)
            finally:
                if set_default_dtype:
                    startai.unset_default_int_dtype()
                    startai.unset_default_float_dtype()
        if not startai.array_mode:
            return ret
        # convert all returned arrays to `ndarray` instances
        if order == "F":
            return startai.nested_map(
                _startai_to_numpy_order_F, ret, include_derived={"tuple": True}
            )
        else:
            return startai.nested_map(_startai_to_numpy, ret, include_derived={"tuple": True})

    if "order" in list(inspect.signature(fn).parameters.keys()):
        contains_order = True
        order_pos = list(inspect.signature(fn).parameters).index("order")
    else:
        contains_order = False
    _outputs_to_frontend_arrays.outputs_to_frontend_arrays_numpy = True
    return _outputs_to_frontend_arrays


def to_startai_arrays_and_back(fn: Callable) -> Callable:
    """Wrap `fn` so it receives and returns `startai.Array` instances.

    Wrap `fn` so that input arrays are all converted to `startai.Array` instances and
    return arrays are all converted to `ndarray` instances.
    """
    return outputs_to_frontend_arrays(inputs_to_startai_arrays(fn))
