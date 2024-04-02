# import jax
from startai_tests.test_startai.test_frontends import NativeClass


jax_classes_to_startai_classes = {}


def convjax(argument):
    """Convert NativeClass in argument to startai frontend counterpart for jax."""
    if isinstance(argument, NativeClass):
        return jax_classes_to_startai_classes.get(argument._native_class)
    return argument
