# local
import startai
from startai.functional.frontends.jax.func_wrapper import to_startai_arrays_and_back
from startai.functional.frontends.jax.numpy import (
    jax_numpy_casting_table,
    promote_types_jax,
)
from startai.functional.frontends.numpy import dtype as np_dtype
from startai import with_supported_dtypes


@to_startai_arrays_and_back
def astype(x, dtype, /, *, copy=True):
    if not copy and dtype == x.dtype:
        return x
    return startai.astype(x, dtype, copy=copy)


@to_startai_arrays_and_back
def can_cast(from_, to, casting="safe"):
    startai.utils.assertions.check_elem_in_list(
        casting,
        ["no", "equiv", "safe", "same_kind", "unsafe"],
        message="casting must be one of [no, equiv, safe, same_kind, unsafe]",
    )

    if startai.is_array(from_):
        from_ = startai.as_startai_dtype(from_.dtype)
    elif isinstance(from_, (str, type)):
        from_ = startai.as_startai_dtype(from_)
    elif isinstance(from_, np_dtype):
        from_ = from_._startai_dtype
    else:
        raise startai.utils.exceptions.StartaiException(
            "from_ must be one of dtype, dtype specifier, scalar type, or array, "
        )

    if isinstance(to, (str, type)):
        to = startai.as_startai_dtype(to)
    elif isinstance(to, np_dtype):
        to = to._startai_dtype
    else:
        raise startai.utils.exceptions.StartaiException(
            "to must be one of dtype, or dtype specifier"
        )

    if casting in ["no", "equiv"]:
        return from_ == to

    if casting == "safe":
        return to in jax_numpy_casting_table[from_]

    if casting == "same_kind":
        if from_ == to or "bool" in from_:
            return True
        elif startai.is_int_dtype(from_) and ("float" in to or "complex" in to):
            return True
        elif startai.is_float_dtype(from_) and ("float" in to or "complex" in to):
            if "bfloat" in from_ and "float16" in to:
                return False
            return True

        elif startai.is_uint_dtype(from_) and (
            "int" in to or "float" in to or "complex" in to
        ):
            return True
        elif (
            startai.is_int_dtype(from_)
            and startai.is_int_dtype(to)
            and not startai.is_uint_dtype(to)
        ):
            return True
        elif "complex" in from_ and "bfloat16" in to:
            return True
        else:
            return to in jax_numpy_casting_table[from_]
    if casting == "unsafe":
        return True
    return False


@with_supported_dtypes(
    {"2.15.0 and below": ("float16", "float32", "float64")},
    "jax",
)
@to_startai_arrays_and_back
def finfo(dtype):
    return startai.finfo(dtype)


@with_supported_dtypes(
    {"2.15.0 and below": ("integer",)},
    "jax",
)
@to_startai_arrays_and_back
def iinfo(int_type):
    return startai.iinfo(int_type)


def promote_types(type1, type2, /):
    if isinstance(type1, np_dtype):
        type1 = type1._startai_dtype
    if isinstance(type2, np_dtype):
        type2 = type2._startai_dtype
    return np_dtype(promote_types_jax(type1, type2))


@to_startai_arrays_and_back
def result_type(*args):
    return startai.result_type(*args)
