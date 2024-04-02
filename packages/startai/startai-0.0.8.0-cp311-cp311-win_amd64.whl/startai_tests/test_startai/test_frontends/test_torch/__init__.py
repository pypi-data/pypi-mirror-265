# import torch
from startai_tests.test_startai.test_frontends import NativeClass


torch_classes_to_startai_classes = {}


def convtorch(argument):
    """Convert NativeClass in argument to startai frontend counterpart for
    torch."""
    if isinstance(argument, NativeClass):
        return torch_classes_to_startai_classes.get(argument._native_class)
    return argument
