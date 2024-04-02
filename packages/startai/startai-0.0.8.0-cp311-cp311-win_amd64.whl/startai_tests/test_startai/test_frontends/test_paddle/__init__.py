# import paddle
from startai_tests.test_startai.test_frontends import NativeClass


paddle_classes_to_startai_classes = {}


def convpaddle(argument):
    """Convert NativeClass in argument to startai frontend counter part for
    paddle."""
    if isinstance(argument, NativeClass):
        return paddle_classes_to_startai_classes.get(argument._native_class)
    return argument
