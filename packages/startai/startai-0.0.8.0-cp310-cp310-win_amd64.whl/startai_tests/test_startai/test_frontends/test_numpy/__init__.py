import numpy
from startai_tests.test_startai.test_frontends import NativeClass


numpy_classes_to_startai_classes = {numpy._NoValue: None}


def convnumpy(argument):
    """Convert NativeClass in argument to startai frontend counterpart for
    numpy."""
    if isinstance(argument, NativeClass):
        return numpy_classes_to_startai_classes.get(argument._native_class)
    return argument
