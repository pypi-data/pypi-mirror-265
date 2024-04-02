"""Startai wrapping functions for conversions.

Collection of Startai functions for wrapping functions to accept and return
startai.Array instances.
"""

# global
import numpy as np
from typing import Any, Union, Tuple, Dict, Iterable, Optional

# local
import startai


# Helpers #
# --------#


ARRAY_TO_BACKEND = {
    "ndarray": "numpy",
    "Tensor": ["torch", "paddle"],
    "Parameter": "torch",
    "EagerTensor": "tensorflow",
    "ResourceVariable": "tensorflow",
    "DeviceArray": "jax",
    "Array": "jax",
    "ArrayImpl": "jax",
    "EagerParamBase": "paddle",
}


def _array_to_new_backend(
    x: Union[startai.Array, startai.NativeArray], native: bool = False
) -> Union[startai.Array, startai.NativeArray]:
    # Frontend instances
    if hasattr(x, "_startai_array"):
        return x

    # startai.Array instances
    native_x = x.data if isinstance(x, startai.Array) else x
    native_x_type = type(native_x).__name__

    # Modify native_type here since @tf.function converts tf.EagerTensor into
    # tf.Tensor when running @tf.function enclosed function
    if startai.backend == "tensorflow":
        import tensorflow as tf

        native_x_type = (
            "EagerTensor"
            if not tf.executing_eagerly() and isinstance(native_x, tf.Tensor)
            else native_x_type
        )

    if native_x_type not in ARRAY_TO_BACKEND:
        return x

    # Check if the other possible backends match with the native data type
    native_x_backend = ARRAY_TO_BACKEND[native_x_type]

    # Handle the `Tensor` name clash in paddle and torch
    if not isinstance(native_x_backend, str):
        native_x_backend = "torch" if "torch" in str(native_x.__class__) else "paddle"

    # If the current backend and the backend for the given array match,
    # simply return the array as is
    if startai.backend == native_x_backend:
        if native:
            return native_x
        np_intermediary = startai.to_numpy(native_x)
        return startai.array(np_intermediary)

    # Otherwise, convert to the new backend
    else:
        native_x_backend = startai.with_backend(native_x_backend)
        # Handle native variable instances here
        if native_x_backend.gradients._is_variable(native_x):
            x_data = native_x_backend.gradients._variable_data(native_x)
            # x_data = _array_to_new_backend(x_data, native=True)
            from startai.functional.startai.gradients import _variable

            return _variable(x_data).data if native else _variable(x_data)

        np_intermediary = native_x_backend.to_numpy(native_x)
        ret = startai.array(np_intermediary)
        return ret.data if native else ret


def _to_new_backend(
    x: Any,
    native: bool = False,
    inplace: bool = False,
    to_ignore: tuple = (),
) -> Any:
    if isinstance(x, startai.Container):
        to_ignore = startai.default(to_ignore, ())
        return x.cont_map(
            lambda x_, _: _to_new_backend(
                x_, native=native, inplace=inplace, to_ignore=to_ignore
            ),
            inplace=inplace,
        )
    return _array_to_new_backend(x, native=native)


def _to_native(x: Any, inplace: bool = False, to_ignore: tuple = ()) -> Any:
    to_ignore = startai.default(to_ignore, ())
    if isinstance(x, to_ignore):
        return x
    if isinstance(x, startai.Array):
        return x.data
    # to prevent the graph from breaking for the time being
    elif type(x) is startai.Shape:
        return x.shape
    elif isinstance(x, startai.Container):
        return x.cont_map(
            lambda x_, _: _to_native(x_, inplace=inplace, to_ignore=to_ignore),
            inplace=inplace,
        )
    return x


def _to_startai(x: Any) -> Any:
    if isinstance(x, startai.Array):
        return x
    elif isinstance(x, startai.NativeShape):
        return startai.Shape(x)
    elif isinstance(x, startai.Container):
        return x.to_startai()
    if startai.is_native_array(x) or isinstance(x, np.ndarray):
        return startai.Array(x)
    return x


# Wrapped #
# --------#


def to_startai(
    x: Union[startai.Array, startai.NativeArray, Iterable],
    nested: bool = False,
    include_derived: Optional[Dict[str, bool]] = None,
) -> Union[startai.Array, startai.NativeArray, Iterable]:
    """Return the input array converted to an startai.Array instance if it is a
    native array type, otherwise the input is returned unchanged. If nested is
    set, the check is applied to all nested leafs of tuples, lists and dicts
    contained within x.

    Parameters
    ----------
    x
        The input to be converted.
    nested
        Whether to apply the conversion on arguments in a nested manner. If so, all
        dicts, lists and tuples will be traversed to their lowest leaves in search of
        startai.Array instances. Default is ``False``.
    include_derived
        Whether to also recursive for classes derived from tuple, list and dict. Default
        is False.

    Returns
    -------
    ret
        the input in its native framework form in the case of startai.Array or instances.
    """
    if nested:
        return startai.nested_map(_to_startai, x, include_derived, shallow=False)
    return _to_startai(x)


def args_to_startai(
    *args: Iterable[Any],
    include_derived: Optional[Dict[str, bool]] = None,
    **kwargs: Dict[str, Any],
) -> Tuple[Iterable[Any], Dict[str, Any]]:
    """Return args and keyword args in their startai.Array or form for all nested
    instances, otherwise the arguments are returned unchanged.

    Parameters
    ----------
    args
        The positional arguments to check
    include_derived
        Whether to also recursive for classes derived from tuple, list and dict.
        Default is ``False``.
    kwargs
        The key-word arguments to check

    Returns
    -------
     ret
        the same arguments, with any nested arrays converted to startai.Array or
        instances.
    """
    native_args = startai.nested_map(_to_startai, args, include_derived, shallow=False)
    native_kwargs = startai.nested_map(_to_startai, kwargs, include_derived, shallow=False)
    return native_args, native_kwargs


def to_native(
    x: Union[startai.Array, startai.NativeArray, Iterable],
    nested: bool = False,
    include_derived: Optional[Dict[str, bool]] = None,
    cont_inplace: bool = False,
    to_ignore: Optional[Union[type, Tuple[type]]] = None,
) -> Union[startai.Array, startai.NativeArray, Iterable]:
    """Return the input item in its native backend framework form if it is an
    startai.Array instance, otherwise the input is returned unchanged. If nested is
    set, the check is applied to all nested leaves of tuples, lists and dicts
    contained within ``x``.

    Parameters
    ----------
    x
        The input to maybe convert.
    nested
        Whether to apply the conversion on arguments in a nested manner. If so, all
        dicts, lists and tuples will be traversed to their lowest leaves in search of
        startai.Array instances. Default is ``False``.
    include_derived
        Whether to also recursive for classes derived from tuple, list and dict.
        Default is ``False``.
    cont_inplace
        Whether to update containers in place. Default is ``False``
    to_ignore
        Types to ignore when deciding whether to go deeper into the nest or not

    Returns
    -------
     ret
        the input in its native framework form in the case of startai.Array instances.
    """
    if nested:
        return startai.nested_map(
            lambda x: _to_native(x, inplace=cont_inplace, to_ignore=to_ignore),
            x,
            include_derived,
            shallow=False,
        )
    return _to_native(x, inplace=cont_inplace, to_ignore=to_ignore)


def args_to_native(
    *args: Iterable[Any],
    include_derived: Optional[Dict[str, bool]] = None,
    cont_inplace: bool = False,
    to_ignore: Optional[Union[type, Tuple[type]]] = None,
    **kwargs: Dict[str, Any],
) -> Tuple[Iterable[Any], Dict[str, Any]]:
    """Return args and keyword args in their native backend framework form for
    all nested startai.Array instances, otherwise the arguments are returned
    unchanged.

    Parameters
    ----------
    args
        The positional arguments to check
    include_derived
        Whether to also recursive for classes derived from tuple, list and dict.
        Default is ``False``.
    cont_inplace
        Whether to update containers in place.
        Default is ``False``
    to_ignore
        Types to ignore when deciding whether to go deeper into the nest or not
    kwargs
        The key-word arguments to check

    Returns
    -------
     ret
        the same arguments, with any nested startai.Array or instances converted to their
        native form.
    """
    native_args = startai.nested_map(
        lambda x: _to_native(x, inplace=cont_inplace, to_ignore=to_ignore),
        args,
        include_derived,
        shallow=False,
    )
    native_kwargs = startai.nested_map(
        lambda x: _to_native(x, inplace=cont_inplace, to_ignore=to_ignore),
        kwargs,
        include_derived,
        shallow=False,
    )
    return native_args, native_kwargs


def to_new_backend(
    x: Union[startai.Array, startai.NativeArray, Iterable],
    native: bool = True,
    nested: bool = False,
    include_derived: Optional[Dict[str, bool]] = None,
    cont_inplace: bool = False,
    to_ignore: Optional[Union[type, Tuple[type]]] = None,
) -> Union[startai.Array, startai.NativeArray, Iterable]:
    """Return the input array converted to new backend framework form if it is
    an `startai.Array`, `startai.NativeArray` or NativeVariable instance. If nested is
    set, the check is applied to all nested leaves of tuples, lists and dicts
    contained within ``x``.

    Parameters
    ----------
    x
        The input to maybe convert.
    native
        Whether to return the new array as a `startai.NativeArray`, NativeVariable
        or an `startai.Array`. Default is ``True``.
    nested
        Whether to apply the conversion on arguments in a nested manner. If so, all
        dicts, lists and tuples will be traversed to their lowest leaves in search of
        startai.Array instances. Default is ``False``.
    include_derived
        Whether to also recursive for classes derived from tuple, list and dict.
        Default is ``False``.
    cont_inplace
        Whether to update containers in place. Default is ``False``
    to_ignore
        Types to ignore when deciding whether to go deeper into the nest or not

    Returns
    -------
     ret
        the input in the new backend framework form in the case of array instances.
    """
    if nested:
        return startai.nested_map(
            lambda x: _to_new_backend(
                x, native=native, inplace=cont_inplace, to_ignore=to_ignore
            ),
            x,
            include_derived,
            shallow=False,
        )
    return _to_new_backend(x, native=native, inplace=cont_inplace, to_ignore=to_ignore)


def args_to_new_backend(
    *args: Iterable[Any],
    native: bool = True,
    shallow: bool = True,
    include_derived: Optional[Dict[str, bool]] = None,
    cont_inplace: bool = False,
    to_ignore: Optional[Union[type, Tuple[type]]] = None,
    **kwargs: Dict[str, Any],
) -> Tuple[Iterable[Any], Dict[str, Any]]:
    """Return args and keyword args in the new current backend framework for
    all nested startai.Array, startai.NativeArray or NativeVariable instances.

    Parameters
    ----------
    args
        The positional arguments to check
    native
        Whether to return the new array as a startai.NativeArray, NativeVariable
        or an startai.Array. Default is ``True``.
    include_derived
        Whether to also recursive for classes derived from tuple, list and dict.
        Default is ``False``.
    cont_inplace
        Whether to update containers in place.
        Default is ``False``
    to_ignore
        Types to ignore when deciding whether to go deeper into the nest or not
    shallow
        Whether to inplace update the input nest or not
        Only works if nest is a mutable type. Default is ``True``.
    kwargs
        The key-word arguments to check

    Returns
    -------
    ret
        The same arguments, with any nested array instances converted
        to the new backend.
    """
    new_args = startai.nested_map(
        lambda x: _to_new_backend(
            x, native=native, inplace=cont_inplace, to_ignore=to_ignore
        ),
        args,
        include_derived,
        shallow=shallow,
    )
    new_kwargs = startai.nested_map(
        lambda x: _to_new_backend(
            x, native=native, inplace=cont_inplace, to_ignore=to_ignore
        ),
        kwargs,
        include_derived,
        shallow=shallow,
    )
    return new_args, new_kwargs
