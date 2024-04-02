from startai_tests.test_startai.test_frontends import NativeClass


scipy_classes_to_startai_classes = {}


def convscipy(argument):
    """Convert NativeClass in argument to startai frontend counterpart for
    scipy."""
    if isinstance(argument, NativeClass):
        return scipy_classes_to_startai_classes.get(argument._native_class)
    return argument
