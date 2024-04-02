# import tensorflow
from startai_tests.test_startai.test_frontends import NativeClass


onnx_classes_to_startai_classes = {}


def convtensor(argument):
    """Convert NativeClass in argument to startai frontend counterpart for onnx."""
    if isinstance(argument, NativeClass):
        return onnx_classes_to_startai_classes.get(argument._native_class)
    return argument
