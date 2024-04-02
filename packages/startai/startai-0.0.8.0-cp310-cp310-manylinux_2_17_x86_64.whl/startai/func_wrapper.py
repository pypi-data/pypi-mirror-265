import contextlib
import startai
import functools
import logging
import weakref
import warnings
import copy as python_copy
from types import FunctionType
from typing import Callable, Literal
import inspect
import numpy as np

from startai.utils.exceptions import StartaiValueError


# for wrapping (sequence matters)
FN_DECORATORS = [
    "handle_complex_input",
    "handle_device",
    "infer_dtype",
    "handle_array_function",
    "outputs_to_startai_arrays",
    "outputs_to_startai_shapes",
    "outputs_to_native_arrays",
    "inputs_to_native_arrays",
    "inputs_to_native_shapes",
    "inputs_to_startai_arrays",
    "handle_out_argument",
    "handle_view_indexing",
    "handle_view",
    "handle_array_like_without_promotion",
    "handle_partial_mixed_function",
    "handle_nestable",
    "handle_ragged",
    "handle_backend_invalid",
    "temp_asarray_wrapper",
    "handle_exceptions",
    "handle_nans",
]


# Helpers #
# --------#

# for casting modes, order is the hierarchy
casting_modes_dict = {
    "uint": lambda: startai.valid_uint_dtypes,
    "int": lambda: sorted(
        set(startai.valid_int_dtypes).difference(set(startai.valid_uint_dtypes))
    ),
    "float": lambda: startai.valid_float_dtypes,
    "complex": lambda: startai.valid_complex_dtypes,
}


def caster(dtype, intersect):
    if hasattr(dtype, "dtype"):
        dtype = startai.as_startai_dtype(dtype.dtype)
    else:
        dtype = startai.as_startai_dtype(dtype)
    if str(dtype) in intersect:
        # based on upcasting or downcasting do something
        if startai.cast_dtypes():
            # all casting types is enabled
            # check cross_casting
            ret_dtype = cross_caster(intersect)
            if ret_dtype:
                return ret_dtype
            # check upcasting
            ret_dtype = upcaster(dtype, intersect)
            if ret_dtype:
                return ret_dtype
            # check downcasting
            ret_dtype = downcaster(dtype, intersect)
            if ret_dtype:
                return ret_dtype
        elif startai.crosscast_dtypes:
            # check cross_casting
            ret_dtype = cross_caster(intersect)
            if ret_dtype:
                return ret_dtype
        elif startai.upcast_dtypes:
            # check upcasting
            ret_dtype = upcaster(dtype, intersect)
            if ret_dtype:
                return ret_dtype
        elif startai.downcast_dtypes:
            # check downcasting
            ret_dtype = downcaster(dtype, intersect)
            if ret_dtype:
                return ret_dtype


def cast_helper(arg, dtype, intersect, is_upcast=True):
    step = 1 if is_upcast else -1
    index = casting_modes_dict[arg]().index(dtype) + step
    result = ""
    while 0 <= index < len(casting_modes_dict[arg]()):
        if casting_modes_dict[arg]()[index] not in intersect:
            result = casting_modes_dict[arg]()[index]
            break
        index += step

    return result


def upcaster(dtype, intersect):
    # upcasting is enabled, we upcast to the highest
    if "uint" in str(dtype):
        return cast_helper("uint", dtype, intersect, is_upcast=True)
    if "int" in dtype:
        return cast_helper("int", dtype, intersect, is_upcast=True)
    if "float" in dtype:
        return cast_helper("float", dtype, intersect, is_upcast=True)
    if "complex" in dtype:
        return cast_helper("complex", dtype, intersect, is_upcast=True)


def downcaster(dtype, intersect):
    # downcasting is enabled, we upcast to the highest
    if "uint" in str(dtype):
        return cast_helper("uint", dtype, intersect, is_upcast=False)
    if "int" in dtype:
        return cast_helper("int", dtype, intersect, is_upcast=False)
    if "float" in dtype:
        return cast_helper("float", dtype, intersect, is_upcast=False)
    if "complex" in dtype:
        return cast_helper("complex", dtype, intersect, is_upcast=False)


def cross_caster(intersect):
    # check if this is an integer unsupported case
    # intersect is unordered, sorting it makes a list
    # and remaking it a set messes the order
    # so we stick with making both of these
    # sorted lists
    dtype = ""
    valid_float = sorted(startai.valid_float_dtypes)
    valid_int = sorted(startai.valid_int_dtypes)
    valid_bool = [startai.bool]
    intersect = sorted(intersect)
    if set(valid_int).issubset(intersect):
        # make dtype equal to default float
        dtype = startai.default_float_dtype()
    elif set(valid_float).issubset(intersect) or set(valid_bool).issubset(intersect):
        # make dtype equal to default int
        dtype = startai.default_int_dtype()

    return str(dtype)


def try_array_function_override(func, overloaded_args, types, args, kwargs):
    if not overloaded_args:
        return False, None

    for overloaded_arg in overloaded_args:
        # Note that we're only calling __startai_array_function__ on the *first*
        # occurrence of each argument type. This is necessary for reasonable
        # performance with a possibly long list of overloaded arguments, for
        # which each __startai_array_function__ implementation might reasonably need to
        # check all argument types.
        try:
            result = overloaded_arg.__startai_array_function__(func, types, args, kwargs)
        except Exception:
            raise startai.utils.exceptions.StartaiNotImplementedException

        if result is not NotImplemented:
            return True, result

    raise TypeError(
        f"no implementation found for {func} on types that implement"
        f" __startai_array_function__: {list(map(type, overloaded_args))}"
    )


def _get_first_array(*args, **kwargs):
    # ToDo: make this more efficient, with function startai.nested_nth_index_where
    def array_fn(x):
        return (
            startai.is_array(x)
            if not hasattr(x, "_startai_array")
            else startai.is_array(x.startai_array)
        )

    array_fn = array_fn if "array_fn" not in kwargs else kwargs["array_fn"]
    arr = None
    if args:
        arr_idxs = startai.nested_argwhere(args, array_fn, stop_after_n_found=1)
        if arr_idxs:
            arr = startai.index_nest(args, arr_idxs[0])
        else:
            arr_idxs = startai.nested_argwhere(kwargs, array_fn, stop_after_n_found=1)
            if arr_idxs:
                arr = startai.index_nest(kwargs, arr_idxs[0])
    elif kwargs:
        arr_idxs = startai.nested_argwhere(kwargs, array_fn, stop_after_n_found=1)
        if arr_idxs:
            arr = startai.index_nest(kwargs, arr_idxs[0])
    return arr


def _build_view(original, view, fn, args, kwargs, index=None):
    if startai.exists(original._base):
        base = original._base
        view._manipulation_stack = python_copy.copy(original._manipulation_stack)
    else:
        base = original
    view._base = base
    base._view_refs.append(weakref.ref(view))
    view._manipulation_stack.append((fn, args[1:], kwargs, index))

    # Handle attributes for torch functions without native view functionality
    if startai.exists(original._torch_base):
        view._torch_base = (
            original
            if startai.exists(original._torch_manipulation)
            else original._torch_base
        )
    else:
        view._torch_base = base
    if fn in _torch_non_native_view_functions:
        view._torch_manipulation = (original, (fn, args[1:], kwargs))
        view._torch_base._torch_view_refs.append(weakref.ref(view))
    return view


_torch_non_native_view_functions = ("flip", "flipud", "rot90", "fliplr")


def _check_in_nested_sequence(sequence, value=None, _type=None):
    """Check `sequence` for either a `value` or a value of type `_type`.

    Helper to recursively check if a N-level nested `sequence` contains
    either a `value` or contains a value of type `_type` and return a
    boolean flag.
    """
    if sequence is value or (isinstance(sequence, _type)):
        # Base case - N = 0
        return True
    elif isinstance(sequence, (tuple, list)):
        if any(isinstance(_val, _type) or _val is value for _val in sequence):
            # N = 1
            return True
        else:
            return any(
                _check_in_nested_sequence(sub_sequence, value, _type)
                for sub_sequence in sequence
                if isinstance(sub_sequence, (tuple, list))
            )


def _get_preferred_device(args, kwargs):
    # When new arrays are created, they should be created on the same device as
    # existing array inputs. If a device is specified as a kwarg, create them there.
    # If not, scan for any other inputs which are already arrays and use the device
    # of the first one found (unless we're in soft device mode).
    device = None
    if "device" in kwargs and kwargs["device"] is not None:
        return device
    if not startai.soft_device_mode:
        arr_arg = _get_first_array(*args, **kwargs)
        return startai.default_device(item=arr_arg, as_native=True)
    return startai.default_device(as_native=True)


# Array Handling #
# ---------------#


def handle_array_function(fn):
    """Wrap a function `fn` to be passed to array_function method.

    Wrap a function to extract the relevant argument types to be passed
    to array_function method.
    """

    @functools.wraps(fn)
    def _handle_array_function(*args, **kwargs):
        overloaded_types = []
        overloaded_args = []

        for arg in args + tuple(kwargs.values()):
            if startai.exists(arg):
                if not isinstance(arg, startai.Container) and hasattr(
                    arg, "__startai_array_function__"
                ):
                    if type(arg) not in overloaded_types:
                        overloaded_types.append(type(arg))
                        if (
                            arg.__startai_array_function__
                            is not startai.Array.__startai_array_function__
                            and not isinstance(arg, (startai.Array, startai.NativeArray))
                        ):
                            index = len(overloaded_args)
                            for i, old_arg in enumerate(overloaded_args):
                                if issubclass(type(arg), type(old_arg)):
                                    index = i
                                    break
                            overloaded_args.insert(index, arg)
                elif isinstance(arg, startai.Container):
                    arg = startai.Container.cont_flatten_key_chains(arg)
                    indices = startai.nested_argwhere(
                        arg, lambda x: hasattr(x, "__startai_array_function__")
                    )
                    for a in indices:
                        if type(getattr(arg, a[0])) not in overloaded_types:
                            overloaded_types.append(type(getattr(arg, a[0])))

                            if getattr(
                                arg, a[0]
                            ).__startai_array_function__ is not startai.Array.__startai_array_function__ and not isinstance(  # noqa: E501
                                getattr(arg, a[0]), (startai.Array, startai.NativeArray)
                            ):
                                index = len(overloaded_args)
                                for i, old_arg in enumerate(overloaded_args):
                                    if issubclass(
                                        type(getattr(arg, a[0])), type(old_arg)
                                    ):
                                        index = i
                                        break
                                overloaded_args.insert(index, arg)

        success, value = try_array_function_override(
            startai.__dict__[fn.__name__], overloaded_args, overloaded_types, args, kwargs
        )
        if success:
            return value
        return fn(*args, **kwargs)

    _handle_array_function.handle_array_function = True
    return _handle_array_function


def handle_array_like_without_promotion(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_array_like_without_promotion(*args, **kwargs):
        args = list(args)
        num_args = len(args)
        try:
            type_hints = inspect.signature(fn).parameters
        except (TypeError, ValueError):
            return fn(*args, **kwargs)
        parameters = list(type_hints.keys())
        annotations = [param.annotation for param in type_hints.values()]

        device = _get_preferred_device(args, kwargs)

        for i, (annotation, parameter, arg) in enumerate(
            zip(annotations, parameters, args)
        ):
            annotation_str = str(annotation)
            if (
                ("rray" in annotation_str or "Tensor" in annotation_str)
                and parameter != "out"
                and all(
                    sq not in annotation_str
                    for sq in ["Sequence", "List", "Tuple", "float", "int", "bool"]
                )
            ):
                if i < num_args:
                    # Fix for ellipsis, slices for numpy's __getitem__
                    # No need to try and convert them into arrays
                    # since asarray throws unpredictable bugs
                    if _check_in_nested_sequence(arg, value=Ellipsis, _type=slice):
                        continue
                    if not startai.is_array(arg):
                        args[i] = startai.array(arg, device=device)
                elif parameters in kwargs:
                    kwarg = kwargs[parameter]
                    if not startai.is_array(kwarg):
                        kwargs[parameter] = startai.array(kwarg, device=device)

        return fn(*args, **kwargs)

    _handle_array_like_without_promotion.handle_array_like_without_promotion = True
    return _handle_array_like_without_promotion


def inputs_to_native_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _inputs_to_native_arrays(*args, **kwargs):
        """Convert all `startai.Array` instances in both the positional and keyword
        arguments into `startai.NativeArray` instances, and then calls the function
        with the updated arguments.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with native arrays passed in the arguments.
        """
        if not startai.array_mode:
            return fn(*args, **kwargs)
        # check if kwargs contains an out argument, and if so, remove it
        has_out = False
        out = None
        if "out" in kwargs:
            out = kwargs["out"]
            del kwargs["out"]
            has_out = True
        # convert all arrays in the inputs to startai.NativeArray instances
        new_args, new_kwargs = startai.args_to_native(*args, **kwargs)
        # add the original out argument back to the keyword arguments
        if has_out:
            new_kwargs["out"] = out
        return fn(*new_args, **new_kwargs)

    _inputs_to_native_arrays.inputs_to_native_arrays = True
    return _inputs_to_native_arrays


def inputs_to_startai_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _inputs_to_startai_arrays(*args, **kwargs):
        """Convert all `startai.NativeArray` instances in both the positional and
        keyword arguments into `startai.Array` instances, and then calls the
        function with the updated arguments.

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
        if not startai.array_mode:
            warnings.warn(
                "In the case of Compositional function, operators might cause"
                " inconsistent behavior when array_mode is set to False"
            )
            return fn(*args, **kwargs)

        has_out = False
        if "out" in kwargs:
            out = kwargs["out"]
            has_out = True
        # convert all arrays in the inputs to startai.Array instances
        startai_args, startai_kwargs = startai.args_to_startai(
            *args, **kwargs, include_derived={"tuple": True}
        )
        if has_out:
            startai_kwargs["out"] = out
        return fn(*startai_args, **startai_kwargs)

    _inputs_to_startai_arrays.inputs_to_startai_arrays = True
    return _inputs_to_startai_arrays


def inputs_to_native_shapes(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _inputs_to_native_shapes(*args, **kwargs):
        args, kwargs = startai.nested_map(
            lambda x: (x.shape if isinstance(x, startai.Shape) and startai.array_mode else x),
            [args, kwargs],
        )
        return fn(*args, **kwargs)

    _inputs_to_native_shapes.inputs_to_native_shapes = True
    return _inputs_to_native_shapes


def outputs_to_startai_shapes(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _outputs_to_startai_shapes(*args, **kwargs):
        args, kwargs = startai.nested_map(
            lambda x: (x.shape if isinstance(x, startai.Shape) and startai.array_mode else x),
            [args, kwargs],
        )
        return fn(*args, **kwargs)

    _outputs_to_startai_shapes.outputs_to_startai_shapes = True
    return _outputs_to_startai_shapes


def to_native_shapes_and_back(fn: Callable) -> Callable:
    """Make `fn` receive `startai.NativeShape` and return `startai.Shape`.

    Wrap `fn` so that input shapes are all converted to
    `startai.NativeShape` instances and return shapes are all converted to
    `startai.Shape` instances.
    """
    return outputs_to_startai_shapes(inputs_to_native_shapes(fn))


def outputs_to_startai_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _outputs_to_startai_arrays(*args, **kwargs):
        """Call the function, and then converts all `startai.NativeArray` instances
        in the function return into `startai.Array` instances.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with native arrays as startai arrays.
        """
        # call unmodified function
        ret = fn(*args, **kwargs)
        # convert all arrays in the return to `startai.Array` instances
        return (
            startai.to_startai(ret, nested=True, include_derived={"tuple": True})
            if startai.array_mode
            else ret
        )

    _outputs_to_startai_arrays.outputs_to_startai_arrays = True
    return _outputs_to_startai_arrays


def output_to_native_arrays(fn: Callable) -> Callable:
    """Call the function, and then converts all `startai.Array` instances in the
    function return into `startai.NativeArray` instances.

    Parameters
    ----------
    args
        The arguments to be passed to the function.

    kwargs
        The keyword arguments to be passed to the function.

    Returns
    -------
        The return of the function, with startai arrays as native arrays.
    """

    @functools.wraps(fn)
    def _output_to_native_arrays(*args, **kwargs):
        ret = fn(*args, **kwargs)
        return startai.to_native(ret, nested=True, include_derived={"tuple": True})

    _output_to_native_arrays.outputs_to_native_arrays = True
    return _output_to_native_arrays


def to_startai_arrays_and_back(fn: Callable) -> Callable:
    """Make `fn` receive `startai.Array` and return `startai.NativeArray`.

    Wrap `fn` so that input arrays are all converted to `startai.Array`
    instances and return arrays are all converted to `startai.NativeArray`
    instances.
    """
    return output_to_native_arrays(inputs_to_startai_arrays(fn))


def to_native_arrays_and_back(fn: Callable) -> Callable:
    """Make `fn` receive `startai.NativeArray` and return `startai.Array`.

    Wrap `fn` so that input arrays are all converted to
    `startai.NativeArray` instances and return arrays are all converted to
    `startai.Array` instances.
    """
    return outputs_to_startai_arrays(inputs_to_native_arrays(fn))


def frontend_outputs_to_startai_arrays(fn: Callable) -> Callable:
    """Wrap `fn` and convert all frontend arrays in its return to startai arrays.

    Used in cases when a frontend function receives a callable (frontend
    function) argument. To be able to use that callable in a composition
    of startai functions, its outputs need to be converted to startai arrays.
    """

    @functools.wraps(fn)
    def _outputs_to_startai_arrays(*args, **kwargs):
        ret = fn(*args, **kwargs)
        return startai.nested_map(
            lambda x: x.startai_array if hasattr(x, "startai_array") else x,
            ret,
            shallow=False,
        )

    return _outputs_to_startai_arrays


def handle_view(fn: Callable) -> Callable:
    """Wrap `fn` and performs view handling if copy is False.

    Used for functional backends (Jax and TensorFlow). Checks if the
    first arg is a view or original array by checking if the ._base
    attribute is populated. If it's original it adds the returned array
    to its view references, then the returned array adds the operation
    to its manipulation stack and stores the original as its base. If
    the first arg is a view, then the returned array copies its base and
    manipulation stack, appends the new operation to the manipulation
    stack and appends its reference to the base array's view_refs
    attribute.
    """

    @functools.wraps(fn)
    def _handle_view(*args, **kwargs):
        ret = fn(*args, **kwargs)
        if ("copy" in kwargs and kwargs["copy"]) or not startai.is_startai_array(args[0]):
            return ret
        original = args[0]
        if isinstance(ret, (list, tuple)):
            for i, view in enumerate(ret):
                ret[i] = _build_view(original, view, fn.__name__, args, kwargs, i)
        else:
            ret = _build_view(original, ret, fn.__name__, args, kwargs, None)
        return ret

    _handle_view.handle_view = True
    return _handle_view


def handle_view_indexing(fn: Callable) -> Callable:
    """Wrap `fn` and performs view handling specifically for indexing.

    As with NumPy it returns a copy if advanced indexing is performed.
    Used for functional backends (Jax and TensorFlow). Checks if the
    first arg is a view or original array by checking if the ._base
    attribute is populated. If it's original it adds the returned array
    to its view references, then the returned array adds the operation
    to its manipulation stack and stores the original as its base. If
    the first arg is a view, then the returned array copies its base and
    manipulation stack, appends the new operation to the manipulation
    stack and appends its reference to the base array's view_refs
    attribute.
    """

    @functools.wraps(fn)
    def _handle_view_indexing(*args, **kwargs):
        ret = fn(*args, **kwargs)
        if ("copy" in kwargs and kwargs["copy"]) or not startai.is_startai_array(args[0]):
            return ret
        query = kwargs["query"] if "query" in kwargs else args[1]
        query = query if isinstance(query, tuple) else (query,)
        if [i for i in query if not isinstance(i, (slice, int))]:
            return ret
        original = args[0]
        # ToDo: Remove hard coding of only function with this wrapper
        #  Need general way to convert special method to function found in startai.__dict__
        ret = _build_view(original, ret, "get_item", args, kwargs)
        return ret

    _handle_view_indexing.handle_view_indexing = True
    return _handle_view_indexing


def _convert_numpy_arrays_to_backend_specific(*args):
    if isinstance(args, np.ndarray):
        np_arr_idxs = startai.nested_argwhere(args, lambda x: isinstance(x, np.ndarray))
        np_arr_val = startai.multi_index_nest(args, np_arr_idxs)
        backend_arr_vals = [startai.array(x).to_native() for x in np_arr_val]
        startai.set_nest_at_indices(args, np_arr_idxs, backend_arr_vals)
    return args


def handle_numpy_arrays_in_specific_backend(fn: Callable) -> Callable:
    """Wrap `fn` and converts all `numpy.ndarray` inputs to `torch.Tensor`
    instances.

    Used for functional backends (PyTorch). Converts all `numpy.ndarray`
    inputs to `torch.Tensor` instances.
    """

    @functools.wraps(fn)
    def _handle_numpy_array_in_torch(*args, **kwargs):
        args = _convert_numpy_arrays_to_backend_specific(*args)
        ret = fn(*args, **kwargs)
        return ret

    _handle_numpy_array_in_torch.handle_numpy_arrays_in_specific_backend = True
    return _handle_numpy_array_in_torch


# Data Type Handling #
# -------------------#


def infer_dtype(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _infer_dtype(*args, dtype=None, **kwargs):
        """Determine the correct `dtype`, and then calls the function with the
        `dtype` passed explicitly.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        dtype
            The data type for the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with `dtype` passed explicitly.
        """
        # find the first array argument, if required
        arr = None if startai.exists(dtype) else _get_first_array(*args, **kwargs)
        # infer the correct data type
        dtype = startai.default_dtype(dtype=dtype, item=arr, as_native=True)
        startai.utils.assertions._check_jax_x64_flag(dtype)
        # call the function with dtype provided explicitly
        return fn(*args, dtype=dtype, **kwargs)

    _infer_dtype.infer_dtype = True
    return _infer_dtype


# Device Handling #
# ----------------#


def handle_device(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_device(*args, **kwargs):
        """Move all array inputs of the function to `startai.default_device()`.

        Parameters
        ----------
        args
            The arguments to be passed to the function.
        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function.
        """
        dev = None
        if "device" in kwargs and kwargs["device"] is not None:
            dev = startai.as_native_dev(kwargs["device"])
        if startai.soft_device_mode:
            with startai.DefaultDevice(startai.default_device(dev)):
                return startai.handle_soft_device_variable(*args, fn=fn, **kwargs)
        inputs = args + tuple(kwargs.values())
        devices = tuple(startai.dev(x) for x in inputs if startai.is_array(x))
        unique_devices = set(devices)
        # check if arrays are on the same device
        if len(unique_devices) <= 1:
            # len(unique_devices) == 0 when there are no arrays
            dst_dev = (
                dev
                if dev is not None
                else None if len(unique_devices) == 0 else next(iter(unique_devices))
            )
            with startai.DefaultDevice(startai.default_device(dst_dev)):
                return startai.handle_soft_device_variable(*args, fn=fn, **kwargs)
        # raise when arrays are on different devices
        elif len(unique_devices) > 1:
            raise startai.utils.exceptions.StartaiException(
                "Expected all input arrays to be on the same device, "
                f"but found at least two devices - {devices}, "
                "set `startai.set_soft_device_mode(True)` to handle this problem."
            )
        return fn(*args, **kwargs)

    _handle_device.handle_device = True
    return _handle_device


# Inplace Update Handling #
# ------------------------#


def handle_out_argument(fn: Callable) -> Callable:
    handle_out_in_backend = hasattr(fn, "support_native_out")

    @functools.wraps(fn)
    def _handle_out_argument(*args, out=None, **kwargs):
        """Call `fn` with the `out` argument handled correctly for performing
        an inplace update.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        out
            The array to write the result to.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with `out` handled correctly for
            inplace updates.
        """
        nonlocal handle_out_in_backend
        if out is None:
            return fn(*args, out=out, **kwargs)
        if startai.gradients._is_variable(out):
            handle_out_in_backend = False
        if handle_out_in_backend:
            # extract underlying native array for out
            native_out = startai.to_native(out)
            # compute return, with backend inplace update handled by
            # the backend function
            ret = fn(*args, out=native_out, **kwargs)
            if isinstance(ret, (tuple, list)):
                for i in range(len(ret)):
                    startai.inplace_update(out[i], ret[i])
                    if startai.backend == "torch":
                        _update_torch_views(out[i])
            else:
                startai.inplace_update(out, ret)
                if startai.backend == "torch":
                    _update_torch_views(out)
            return out
        # compute return, and then handle the inplace update explicitly

        ret = fn(*args, **kwargs)
        if not startai.is_array(ret) and not startai.is_startai_container(ret):
            return startai.nested_multi_map(
                lambda x, _: startai.inplace_update(
                    x[0], startai.astype(x[1], startai.dtype(x[0]))
                ),
                [out, ret],
            )
        return startai.inplace_update(out, startai.astype(ret, startai.dtype(out)))
        # return output matches the dtype of the out array to match numpy and torch

    _handle_out_argument.handle_out_argument = True
    return _handle_out_argument


def _update_torch_views(x, visited_view=None):
    if x._torch_view_refs != []:
        _update_torch_references(x, visited_view)
    if startai.exists(x._torch_manipulation):
        parent_tensor, fn_args_kwargs = x._torch_manipulation
        fn, args, kwargs = fn_args_kwargs
        kwargs["copy"] = True
        if fn == "rot90":
            kwargs = kwargs.copy()
            kwargs["k"] = -kwargs["k"]
        parent_tensor.data[()] = startai.__dict__[fn](x, *args, **kwargs).data
    if startai.exists(x._torch_base):
        _update_torch_views(x._torch_base, visited_view=x)


def _update_torch_references(x, visited_view=None):
    for ref in x._torch_view_refs:
        view = ref()
        if startai.exists(view) and view is not visited_view:
            parent_tensor, fn_args_kwargs = view._torch_manipulation
            fn, args, kwargs = fn_args_kwargs
            kwargs["copy"] = True
            view.data[()] = startai.__dict__[fn](parent_tensor, *args, **kwargs).data
            if view._torch_view_refs != []:
                _update_torch_references(view)


# Nestable Handling #
# ------------------#


def handle_nestable(fn: Callable) -> Callable:
    fn_name = fn.__name__

    @functools.wraps(fn)
    def _handle_nestable(*args, **kwargs):
        """Call `fn` with the *nestable* property of the function correctly
        handled. This means mapping the function to the container leaves if any
        containers are passed in the input.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with the nestable property handled correctly.
        """
        # if any of the arguments or keyword arguments passed to the function contains
        # a container, get the container's version of the function and call it using
        # the passed arguments.
        if hasattr(startai.Container, f"_static_{fn_name}"):
            cont_fn = getattr(startai.Container, f"_static_{fn_name}")
        else:

            def cont_fn(*args, **kwargs):
                return startai.Container.cont_multi_map_in_function(fn, *args, **kwargs)

        if startai.nestable_mode and (
            startai.nested_any(args, startai.is_startai_container, check_nests=True)
            or startai.nested_any(kwargs, startai.is_startai_container, check_nests=True)
        ):
            return cont_fn(*args, **kwargs)

        # if the passed arguments does not contain a container, the function using
        # the passed arguments, returning an startai or a native array.
        return fn(*args, **kwargs)

    _handle_nestable.handle_nestable = True
    return _handle_nestable


def handle_ragged(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_ragged(*args, **kwargs):
        """Call `fn` with the *ragged* property of the function correctly
        handled. This means mapping the function to the RaggedArray arrays if
        any RaggedArrays are passed in the input.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with the ragged property handled correctly.
        """

        def nested_fn(*args, **kwargs):
            return startai.NestedArray.ragged_multi_map_in_function(fn, *args, **kwargs)

        if startai.nested_any(
            args, startai.is_startai_nested_array, check_nests=True
        ) or startai.nested_any(kwargs, startai.is_startai_nested_array, check_nests=True):
            return nested_fn(*args, **kwargs)

        # if the passed arguments does not contain a container, the function using
        # the passed arguments, returning an startai or a native array.
        return fn(*args, **kwargs)

    _handle_ragged.handle_ragged = True
    return _handle_ragged


# Partial Mixed Function Handling #


def handle_partial_mixed_function(fn) -> Callable:
    @functools.wraps(fn)
    def _handle_partial_mixed_function(*args, **kwargs):
        handle_mixed_in_backend = False
        if not hasattr(fn, "partial_mixed_handler"):
            handle_mixed_in_backend = True
        else:
            compos = getattr(fn, "compos")
            condition = getattr(fn, "partial_mixed_handler")

        if handle_mixed_in_backend or condition(*args, **kwargs):
            return fn(*args, **kwargs)
        return compos(*args, **kwargs)

    _handle_partial_mixed_function.handle_partial_mixed_function = True
    return _handle_partial_mixed_function


# Temporary asarray wrapper (Please request my review before removing)


def temp_asarray_wrapper(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _temp_asarray_wrapper(*args, **kwargs):
        """Convert `Tensor` into `startai.Array` instances.

        Convert all `Tensor` instances in both the positional and keyword arguments
        into `startai.Array` instances, and then call the function with the updated
        arguments.
        """

        def _to_startai_array(x):
            # if x is a frontend torch Tensor (or any frontend "Tensor" actually) return the wrapped startai array # noqa: E501
            if hasattr(x, "startai_array"):
                return x.startai_array
            # else just return x
            return x

        # convert all input arrays to startai.Array instances
        new_args = startai.nested_map(
            _to_startai_array, args, include_derived={"tuple": True}, shallow=False
        )
        new_kwargs = startai.nested_map(
            _to_startai_array, kwargs, include_derived={"tuple": True}, shallow=False
        )
        return fn(*new_args, **new_kwargs)

    _temp_asarray_wrapper.temp_asarray_wrapper = True
    return _temp_asarray_wrapper


# Download compiled cython wrapper wrapper


def download_cython_wrapper_wrapper(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _download_cython_wrapper_wrapper(*args, **kwargs):
        """Wrap the function to download compiled cython wrapper for the
        function and re- wraps it with the downloaded wrapper.

        Download the compiled cython wrapper by calling
        startai.wrappers.get_wrapper(func_name: str) and then wrap the
        function with the downloaded wrapper.
        """
        startai.wrappers.download_cython_wrapper(fn.__name__)
        startai.wrappers.load_one_wrapper(fn.__name__)
        startai.functional.__dict__[fn.__name__] = getattr(
            startai.wrappers, fn.__name__ + "_wrapper"
        )(fn)
        return startai.functional.__dict__[fn.__name__](*args, **kwargs)

    return _download_cython_wrapper_wrapper


# Functions #


def _wrap_function(
    key: str, to_wrap: Callable, original: Callable, compositional: bool = False
) -> Callable:
    """Apply wrapping to backend implementation `to_wrap` if the original
    implementation `original` is also wrapped, and if `to_wrap` is not already
    wrapped. Attributes `handle_nestable` etc are set during wrapping, hence
    indicate to us whether a certain function has been wrapped or not. Also
    handles wrapping of the `linalg` namespace.

    Parameters
    ----------
    to_wrap
        the new implementation to potentially wrap
    original
        the original implementation of `to_wrap` which tells us which wrappers we need.
    compositional
        indicates whether the function being wrapped is compositional
        (Default Value = ``False``).

    Returns
    -------
    ret
        `to_wrap` appropriately wrapped if `to_wrap` is a function, otherwise just the
        input is returned.
    """
    if key == "linalg":
        for linalg_k, linalg_v in to_wrap.__dict__.items():
            if (
                isinstance(linalg_v, FunctionType)
                and linalg_k.lower() != "namedtuple"
                and linalg_k != "with_unsupported_dtypes"
                and not linalg_k.startswith("_")
            ):
                to_wrap.__dict__[linalg_k] = _wrap_function(
                    linalg_k,
                    linalg_v,
                    startai.__dict__[linalg_k],
                    compositional=compositional,
                )
        return to_wrap
    if isinstance(to_wrap, FunctionType):
        if startai.cython_wrappers_mode and startai.wrappers.wrapper_exists(to_wrap.__name__):
            if to_wrap.__name__ + "_wrapper" in startai.wrappers.__all__:
                to_wrap = getattr(startai.wrappers, to_wrap.__name__ + "_wrapper")(to_wrap)
                return to_wrap
            else:
                return download_cython_wrapper_wrapper(to_wrap)
        # set attributes
        for attr in original.__dict__.keys():
            # private attribute or decorator
            if (
                attr.startswith("_")
                or hasattr(startai, attr)
                or attr == "mixed_backend_wrappers"
            ):
                continue
            setattr(to_wrap, attr, getattr(original, attr))
        # Copy docstring
        docstring_attr = ["__annotations__", "__doc__"]
        for attr in docstring_attr:
            setattr(to_wrap, attr, getattr(original, attr))

        mixed_fn = hasattr(original, "mixed_backend_wrappers") and original != to_wrap
        partial_mixed = (
            mixed_fn
            and hasattr(original, "handle_partial_mixed_function")
            and hasattr(to_wrap, "partial_mixed_handler")
        )
        add_wrappers, skip_wrappers = [], []
        if mixed_fn:
            backend_wrappers = getattr(original, "mixed_backend_wrappers")
            add_wrappers = backend_wrappers.get("to_add")
            skip_wrappers = backend_wrappers.get("to_skip")

        for attr in FN_DECORATORS:
            if hasattr(original, attr) and not hasattr(to_wrap, attr):
                if partial_mixed and attr == "handle_partial_mixed_function":
                    to_wrap.compos = original
                    to_wrap = handle_partial_mixed_function(to_wrap)
                if attr not in skip_wrappers:
                    to_wrap = getattr(startai, attr)(to_wrap)
            if attr in add_wrappers:
                to_wrap = getattr(startai, attr)(to_wrap)

        # we should remove the all the decorators
        # after handle_mixed_fuction in FN_DECORATORS
        # from the compos function because these will
        # be run from the primary implementation.
        if partial_mixed:
            array_spec = to_wrap.compos.__dict__["array_spec"]
            for attr in FN_DECORATORS[
                -1 : FN_DECORATORS.index("handle_partial_mixed_function") : -1
            ]:
                if hasattr(to_wrap.compos, attr):
                    to_wrap.compos = to_wrap.compos.__wrapped__
            to_wrap.compos.__dict__["array_spec"] = array_spec
    return to_wrap


def casting_modes_ops(fn, ret_dtype_target=None):
    @functools.wraps(fn)
    def method(*args, **kwargs):
        # Get the function signature
        signature = inspect.signature(fn)
        # Extract argument names
        arg_names = [param.name for param in signature.parameters.values()]
        # we first check if it has unsupported/supported dtypes uniquely added to it
        intersect = set(startai.function_unsupported_dtypes(fn)).difference(
            set(startai.invalid_dtypes)
        )
        if not intersect:
            # doesn't have unsupported dtypes specified
            # so check if it's one of the device_and_dtype one
            intersect = set(
                startai.function_unsupported_devices_and_dtypes(fn).get(
                    startai.default_device().split(":")[0], {None}
                )
            ).difference(set(startai.invalid_dtypes))
            if not intersect:
                # no unsupported dtype specified
                return fn(*args, **kwargs)

        # specifies which dtype to cast the output to
        to_cast = None
        if "dtype" in kwargs and kwargs["dtype"] is not None:
            to_cast = kwargs["dtype"]
            dtype = caster(kwargs["dtype"], intersect)
            if dtype:
                kwargs["dtype"] = startai.as_native_dtype(dtype)

        def mini_helper(x):
            if not hasattr(x, "dtype"):
                return x
            dtype = caster(x, intersect)
            if dtype:
                x = startai.to_native(startai.astype(x, startai.as_native_dtype(dtype)))
            return x

        args = startai.nested_map(mini_helper, args, include_derived=True)
        kwargs = startai.nested_map(mini_helper, kwargs)

        if not to_cast and ret_dtype_target:
            for arg in ret_dtype_target:
                if arg:
                    to_cast, arg_mod = startai.promote_types_of_inputs(
                        to_cast,
                        (
                            args[arg_names.index(arg)]
                            if arg not in kwargs
                            else kwargs[arg]
                        ),
                    )
                    if arg not in kwargs:
                        args[arg_names.index(arg)] = (
                            arg_mod
                            if not startai.is_array(args[arg_names.index(arg)])
                            else args[arg_names.index(arg)]
                        )
                    else:
                        kwargs[arg] = (
                            arg_mod
                            if not startai.is_array(args[arg_names.index(arg)])
                            else kwargs[arg]
                        )

        return (
            startai.astype(fn(*args, **kwargs), startai.to_native(to_cast))
            if to_cast
            else fn(*args, **kwargs)
        )

    return method


# Gets dtype from a version dictionary
def _dtype_from_version(dic, version):
    # if version is a string, it's a frontend function
    if isinstance(version, str):
        version = startai.functional.frontends.__dict__["versions"][version]
    # if version is a dict, extract the version
    if isinstance(version, dict):
        version = version["version"]

    # If version dict is empty, then there is an error
    if not dic:
        raise ValueError("No version found in the dictionary")

    # If key is already in the dictionary, return the value
    if version in dic:
        return dic[version]

    version_tuple = tuple(map(int, version.split(".")))

    # If key is not in the dictionary, check if it's in any range
    # three formats are supported:
    # 1. x.y.z and above
    # 2. x.y.z and below
    # 3. x.y.z to x.y.z
    for key in dic.keys():
        kl = key.split(" ")
        k1 = tuple(map(int, kl[0].split(".")))
        if "above" in key and k1 <= version_tuple:
            return dic[key]
        if "below" in key and k1 >= version_tuple:
            return dic[key]
        if "to" in key and k1 <= version_tuple <= tuple(map(int, kl[2].split("."))):
            return dic[key]

    # if no version is found, return the last version
    return dic[list(dic.keys())[-1]]


def _versioned_attribute_factory(attribute_function, base):
    class VersionedAttributes(base):
        """Class which add versioned attributes to a class, inheriting from
        `base`.

        Create a class which inherits `base` this way if isinstance is
        called on an instance of the class, it will return True if
        testing for the baseclass, such as isinstance(instance, tuple)
        if `base` is tuple.
        """

        def __init__(self):
            self.attribute_function = attribute_function

        def __get__(self, instance=None, owner=None):
            # version dtypes recalculated every time it's accessed
            return self.attribute_function()

        def __iter__(self):
            # iter allows for iteration over current version that's selected
            return iter(self.__get__())

        def __repr__(self):
            return repr(self.__get__())

        def __bool__(self):
            return bool(self.__get__())

    return VersionedAttributes()


def _dtype_device_wrapper_creator(attrib, t):
    """Create a wrapper for a dtype or device attribute.

    The wrapper returns the correct dtype or device for the current version of the
    backend.

    Parameters
    ----------
    attrib
        The attribute name to be wrapped. for example, "unsupported_dtypes"
    t
        The type of the attribute. for example, "tuple"

    Returns
    -------
    A wrapper function for the attribute.
    """

    def _wrapper_outer(version_dict, version, exclusive=True, ret_dtype_target=None):
        def _wrapped(func):
            val = _versioned_attribute_factory(
                lambda: _dtype_from_version(version_dict, version), t
            )
            if hasattr(func, "override"):
                # we do nothing
                return func
            if not exclusive:
                # exclusive attribute comes into existence
                # only when exclusive is passed as true
                setattr(func, "exclusive", True)
            # set the attribute on the function and return the function as is

            has_attrib = [
                attribute for attribute in attribute_dict if hasattr(func, attribute)
            ] or False
            if has_attrib:
                for attribs in has_attrib:
                    if not (
                        attrib == attribs or (attrib, attribs) in attribute_conflict
                    ):
                        # cases when we encounter two different decorators
                        # applied to the function, but they are not same
                        # and aren't in conflicting dict either
                        setattr(func, attrib, val)
                        setattr(func, "dictionary_info", (version_dict, version))
                    elif hasattr(func, "exclusive"):
                        if attrib == attribs:
                            # we see a higher decorator with exclusivity applied
                            # we use this decorator's dict information
                            # and previous decorator's dict information
                            # to update this
                            old_version_dict = getattr(func, "dictionary_info")[0]
                            old_version_dict.update(version_dict)
                            val = _versioned_attribute_factory(
                                lambda: _dtype_from_version(
                                    version_dict, old_version_dict
                                ),
                                t,
                            )
                            setattr(func, attrib, val)
                        else:
                            # for conflicting ones we do nothing
                            pass
            else:
                if not val and attrib.startswith("supported"):
                    setattr(func, f"un{attrib}", val)
                else:
                    setattr(func, attrib, val)
                setattr(func, "dictionary_info", (version_dict, version))
            if "frontends" in func.__module__:
                # it's a frontend func, no casting modes for this
                return func

            return casting_modes_ops(func, ret_dtype_target=ret_dtype_target)

        return _wrapped

    return _wrapper_outer


# nans Handling #
# --------------#


def _leaf_has_nans(x):
    if isinstance(x, startai.Container):
        return x.has_nans()
    elif startai.is_array(x):
        return startai.isnan(x).any()
    elif np.isnan(x):
        return True
    return False


def _nest_has_nans(x):
    return startai.nested_any(x, _leaf_has_nans)


def handle_nans(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_nans(*args, **kwargs):
        """Check for the existence of nans in all arrays in the `args` and
        `kwargs`.

        The presence of nans is then handled depending on the enabled `nan_policy`.

        Following policies apply:
        raise_exception: raises an exception in case nans are present
        warns: warns a user in case nans are present
        nothing: does nothing

        Parameters
        ----------
        args
            The arguments to be passed to the function.
        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with handling of inputs based
            on the selected `nan_policy`.
        """
        nan_policy = startai.nan_policy
        # skip the check if the current nan policy is `nothing``
        if nan_policy == "nothing":
            return fn(*args, **kwargs)

        # check all args and kwargs for presence of nans
        result = _nest_has_nans(args) or _nest_has_nans(kwargs)

        if result:
            # handle nans based on the selected policy
            if nan_policy == "raise_exception":
                raise startai.utils.exceptions.StartaiException(
                    "Nans are not allowed in `raise_exception` policy."
                )
            elif nan_policy == "warns":
                logging.warning("Nans are present in the input.")

        return fn(*args, **kwargs)

    _handle_nans.handle_nans = True
    return _handle_nans


# Complex number handling #
# ----------------------- #
def handle_complex_input(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_complex_input(
        inp,
        *args,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        **kwargs,
    ):
        """Check whether the first positional argument is an array of complex
        type, and if so handle it according to the provided `complex_mode`.

        The options are:
        `"jax"` (default): emulate the behaviour of the JAX framework. If the function
            has a `jax_like` attribute then this will be used to decide on the
            behaviour (see below) and if not, then the entire array will be passed to
            the function.
        `"split"`: execute the function separately on the real and imaginary parts of
            the input.
        `"magnitude"`: execute the function on the magnitude of the input, and keep the
            angle constant.

        The `jax_like` attribute (which should be added to the function itself, and not
        passed as a parameter) has the following options:
        `"entire"` (default): pass the entire input to the function. This is best used
            for purely mathematical operators which are already well defined on complex
            inputs, as many backends will throw exceptions otherwise.
        `"split"`: as the `"split"` option for `complex_mode`
        `"magnitude"`: as the `"magnitude"` option for `complex_mode`
        A callable function: the function will be called instead of the originally
            decorated function. It will be passed `inp` and `*args` as positional
            arguments, and the original `**kwargs` plus `fn_original` as keyword
            arguments. The latter is the original function, in case the `jax_like`
            function wishes to call it.

        Parameters
        ----------
        inp
            The first positional argument to the function, which is expected to be an
            :class:`startai.Array`.
        args
            The remaining positional arguments to be passed to the function.
        complex_mode
            Optional argument which specifies the method that will be used to handle
            the input, if it is complex.
        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with handling of inputs based
            on the selected `complex_mode`.

        Examples
        --------
        Using the default `jax_like` behaviour

        >>> @handle_complex_input
        >>> def my_func(inp):
        >>>     return startai.ones_like(inp)

        >>> x = startai.array([1+1j, 3+4j, 5+12j])
        >>> my_func(x)  # equivalent to setting complex_mode="jax"
        startai.array([1.+0.j, 1.+0.j, 1.+0.j])

        >>> my_func(x, complex_mode="split")
        startai.array([1.+1.j, 1.+1.j, 1.+1.j])

        >>> my_func(x, complex_mode="magnitude")
        startai.array([0.70710681+0.70710675j, 0.60000001+0.79999999j,
                   0.38461535+0.92307694j])

        Using non-default `jax_like` behaviour

        >>> @handle_complex_input
        >>> def my_func(inp):
        >>>     return startai.ones_like(inp)
        >>> my_func.jax_like = "split"
        >>> my_func(x, complex_mode="jax")
        startai.array([1.+1.j, 1.+1.j, 1.+1.j])

        Using callable `jax_like` behaviour

        >>> def _my_func_jax_like(inp, fn_original=None):
        >>>     return fn_original(inp) * 3j
        >>> @handle_complex_input
        >>> def my_func(inp):
        >>>     return startai.ones_like(inp)
        >>> my_func.jax_like = _my_func_jax_like
        >>> my_func(x, complex_mode="jax")
        startai.array([0.+3.j, 0.+3.j, 0.+3.j])
        """
        if not startai.is_complex_dtype(inp):
            return fn(inp, *args, **kwargs)

        jax_like = fn.jax_like if hasattr(fn, "jax_like") else "entire"

        if complex_mode == "split" or (complex_mode == "jax" and jax_like == "split"):
            real_inp = startai.real(inp).data
            imag_inp = startai.imag(inp).data
            if "out" in kwargs and kwargs["out"] is not None:
                out = kwargs.pop("out")
                real_ret = fn(real_inp, *args, out=startai.real(out), **kwargs)
                imag_ret = fn(imag_inp, *args, out=startai.imag(out), **kwargs)
            else:
                real_ret = fn(real_inp, *args, **kwargs)
                imag_ret = fn(imag_inp, *args, **kwargs)
            return startai.add(
                real_ret,
                startai.multiply(startai.array(1j, dtype=inp.dtype), imag_ret),
            )

        elif complex_mode == "magnitude" or (
            complex_mode == "jax" and jax_like == "magnitude"
        ):
            mag_inp = startai.abs(inp).data
            angle_inp = startai.angle(inp).data
            return startai.multiply(
                fn(mag_inp, *args, **kwargs), startai.exp(startai.multiply(1j, angle_inp))
            )

        elif complex_mode == "jax" and jax_like == "entire":
            return fn(inp, *args, **kwargs)

        elif complex_mode == "jax":
            return jax_like(inp, *args, **kwargs, fn_original=fn)

        else:
            raise StartaiValueError(f"complex_mode '{complex_mode}' is not recognised.")

    _handle_complex_input.handle_complex_input = True
    return _handle_complex_input


def handle_backend_invalid(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def _handle_backend_invalid(*args, **kwargs):
        """Check if any of the arguments (or nested arguments) passed to the
        function are instances of startai.Array or startai.NativeArray. If so, it
        returns the function. If not, it raises an InvalidBackendException.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function if the current
            backend matches the argument backend.
            If not, it raises an InvalidBackendException
        """
        array_indices = startai.nested_argwhere(
            [args, kwargs], lambda x: isinstance(x, startai.Array)
        )
        array_vals = startai.multi_index_nest([args, kwargs], array_indices)

        def func(x):
            target_backend = startai.utils.backend.handler._determine_backend_from_args(x)
            if (
                target_backend is not None
                and startai.backend != ""
                and startai.current_backend_str() != target_backend.backend
            ):
                raise startai.utils.exceptions.StartaiInvalidBackendException(
                    "Operation not allowed. Array was instantiated with backend"
                    f" {target_backend.backend}. But current backend is"
                    f" {startai.backend}. Please set dynamic=True"
                    " for the array if you want to convert it to the target"
                    " backend"
                )
            return x

        startai.nested_map(func, array_vals, include_derived=True)

        return fn(*args, **kwargs)

    _handle_backend_invalid.handle_backend_invalid = True
    return _handle_backend_invalid


attribute_dict = {
    "unsupported_dtypes",
    "supported_dtypes",
    "unsupported_devices",
    "supported_devices",
    "unsupported_device_and_dtype",
    "supported_device_and_dtype",
}


attribute_conflict = {
    ("unsupported_devices", "supported_devices"),
    ("supported_devices", "unsupported_devices"),
    ("unsupported_device_and_dtype", "supported_device_and_dtype"),
    ("supported_device_and_dtype", "unsupported_device_and_dtype"),
}

# TODO see if the globals_getter_func can be hacked to return
# the globals in the module where it is working


def globals_getter_func(x=None):
    # define and assign this function to
    # startai.func_wrapper.globals_getter_func in the module
    # where you want to use the decorators as a context
    # manager
    if not x:
        return globals()
    else:
        globals()[x[0]] = x[1]


class with_unsupported_dtypes(contextlib.ContextDecorator):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.globals = {}

    def __call__(self, func=None):
        if func:
            return (
                _dtype_device_wrapper_creator("unsupported_dtypes", tuple)(
                    *self.args, **self.kwargs
                )
            )(func)

    def __enter__(self):
        self.globals = globals_getter_func().copy()  # global snapshot

    def __exit__(self, *exec):
        new_globals = set(globals_getter_func().keys())
        diff = new_globals.difference(set(self.globals))
        for item in diff:
            if globals_getter_func().get(item, None):
                if isinstance(globals_getter_func()[item], FunctionType):
                    # we need to add the decorator
                    globals_getter_func(
                        [
                            item,
                            (
                                _dtype_device_wrapper_creator(
                                    "unsupported_dtypes", tuple
                                )(*self.args, **self.kwargs)
                            )(globals_getter_func()[item]),
                        ]
                    )


class with_supported_dtypes(contextlib.ContextDecorator):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.globals = {}

    def __call__(self, func=None):
        if func:
            return (
                _dtype_device_wrapper_creator("supported_dtypes", tuple)(
                    *self.args, **self.kwargs
                )
            )(func)

    def __enter__(self):
        self.globals = globals_getter_func().copy()  # global snapshot

    def __exit__(self, *exec):
        new_globals = set(globals_getter_func().keys())
        diff = new_globals.difference(set(self.globals))
        for item in diff:
            if globals_getter_func().get(item, None):
                if isinstance(globals_getter_func()[item], FunctionType):
                    # we need to add the decorator
                    globals_getter_func(
                        [
                            item,
                            (
                                _dtype_device_wrapper_creator(
                                    "supported_dtypes", tuple
                                )(*self.args, **self.kwargs)
                            )(globals_getter_func()[item]),
                        ]
                    )


class with_unsupported_devices(contextlib.ContextDecorator):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.globals = {}

    def __call__(self, func=None):
        if func:
            return (
                _dtype_device_wrapper_creator("unsupported_devices", tuple)(
                    *self.args, **self.kwargs
                )
            )(func)

    def __enter__(self):
        self.globals = globals_getter_func().copy()  # global snapshot

    def __exit__(self, *exec):
        new_globals = set(globals_getter_func().keys())
        diff = new_globals.difference(set(self.globals))
        for item in diff:
            if globals_getter_func().get(item, None):
                if isinstance(globals_getter_func()[item], FunctionType):
                    # we need to add the decorator
                    globals_getter_func(
                        [
                            item,
                            (
                                _dtype_device_wrapper_creator(
                                    "unsupported_devices", tuple
                                )(*self.args, **self.kwargs)
                            )(globals_getter_func()[item]),
                        ]
                    )


class with_supported_devices(contextlib.ContextDecorator):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.globals = {}

    def __call__(self, func=None):
        if func:
            return (
                _dtype_device_wrapper_creator("supported_devices", tuple)(
                    *self.args, **self.kwargs
                )
            )(func)

    def __enter__(self):
        self.globals = globals_getter_func().copy()  # global snapshot

    def __exit__(self, *exec):
        new_globals = set(globals_getter_func().keys())
        diff = new_globals.difference(set(self.globals))
        for item in diff:
            if globals_getter_func().get(item, None):
                if isinstance(globals_getter_func()[item], FunctionType):
                    # we need to add the decorator
                    globals_getter_func(
                        [
                            item,
                            (
                                _dtype_device_wrapper_creator(
                                    "supported_devices", tuple
                                )(*self.args, **self.kwargs)
                            )(globals_getter_func()[item]),
                        ]
                    )


class with_unsupported_device_and_dtypes(contextlib.ContextDecorator):
    def __init__(self, *args, **kwargs):
        # arg inspection
        dicti = args[0]
        self.kwargs = kwargs
        # iterate through the keys
        for key in dicti.keys():
            # maintain a dictionary for nested dictionary
            nested_dic = {}
            for nested_key in dicti[key].keys():
                if nested_key == "all":
                    nested_dic["cpu"] = dicti[key].get("cpu", ()) + tuple(
                        dicti[key]["all"]
                    )
                    nested_dic["tpu"] = dicti[key].get("tpu", ()) + tuple(
                        dicti[key]["all"]
                    )
                    nested_dic["gpu"] = dicti[key].get("gpu", ()) + tuple(
                        dicti[key]["all"]
                    )
                else:
                    nested_dic[nested_key] = tuple(dicti[key][nested_key])
            dicti[key] = nested_dic
        args = (dicti, args[1])

        self.args = args
        self.globals = {}

    def __call__(self, func=None):
        if func:
            return (
                _dtype_device_wrapper_creator("unsupported_device_and_dtype", tuple)(
                    *self.args, **self.kwargs
                )
            )(func)

    def __enter__(self):
        self.globals = globals_getter_func().copy()  # global snapshot

    def __exit__(self, *exec):
        new_globals = set(globals_getter_func().keys())
        diff = new_globals.difference(set(self.globals.keys()))
        for item in diff:
            if globals_getter_func().get(item, None):
                if isinstance(globals_getter_func()[item], FunctionType):
                    # we need to add the decorator
                    globals_getter_func(
                        [
                            item,
                            (
                                _dtype_device_wrapper_creator(
                                    "unsupported_device_and_dtype", tuple
                                )(*self.args, **self.kwargs)
                            )(globals_getter_func()[item]),
                        ]
                    )


class with_supported_device_and_dtypes(contextlib.ContextDecorator):
    def __init__(self, *args, **kwargs):
        # arg inspection
        dicti = args[0]
        self.kwargs = kwargs
        # iterate through the keys
        for key in dicti.keys():
            # maintain a dictionary for nested dictionary
            nested_dic = {}
            for nested_key in dicti[key].keys():
                if nested_key == "all":
                    nested_dic["cpu"] = dicti[key].get("cpu", ()) + tuple(
                        dicti[key]["all"]
                    )
                    nested_dic["tpu"] = dicti[key].get("tpu", ()) + tuple(
                        dicti[key]["all"]
                    )
                    nested_dic["gpu"] = dicti[key].get("gpu", ()) + tuple(
                        dicti[key]["all"]
                    )
                else:
                    nested_dic[nested_key] = tuple(dicti[key][nested_key])
            dicti[key] = nested_dic
        args = (dicti, args[1])

        self.args = args
        self.globals = {}

    def __call__(self, func=None):
        if func:
            return (
                _dtype_device_wrapper_creator("supported_device_and_dtype", tuple)(
                    *self.args, **self.kwargs
                )
            )(func)

    def __enter__(self):
        self.globals = globals_getter_func().copy()  # global snapshot

    def __exit__(self, *exec):
        new_globals = set(globals_getter_func().keys())
        diff = new_globals.difference(set(self.globals))
        for item in diff:
            if globals_getter_func().get(item, None):
                if isinstance(globals_getter_func()[item], FunctionType):
                    # we need to add the decorator
                    globals_getter_func(
                        [
                            item,
                            (
                                _dtype_device_wrapper_creator(
                                    "supported_device_and_dtype", tuple
                                )(*self.args, **self.kwargs)
                            )(globals_getter_func()[item]),
                        ]
                    )


class override(contextlib.ContextDecorator):
    def __call__(self, func=None):
        if func:
            setattr(func, "override", "override")
            return func

    def __enter__(self):
        self.globals = globals_getter_func().copy()  # global snapshot

    def __exit__(self, *exec):
        new_globals = set(globals().keys())
        diff = new_globals.difference(set(self.globals))
        for item in diff:
            if globals_getter_func().get(item, None):
                if isinstance(globals_getter_func()[item], FunctionType):
                    # we need to add the decorator
                    globals_getter_func([item, "override"])
