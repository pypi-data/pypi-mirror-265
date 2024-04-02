import startai


# repeated utility function
def type_of_target(y, input_name="y"):
    # purely utility function
    unique_vals = len(startai.unique_values(y))
    if y.ndim == 2 and y.shape[1] > 1 and unique_vals <= 2:
        return "multilabel-indicator"
    if y.ndim not in (1, 2):
        return "unknown"
    if startai.is_float_dtype(y) and startai.any(startai.not_equal(y, y.astype("int64"))):
        return "continuous"
    else:
        if unique_vals > 2:
            return "multiclass"
        else:
            return "binary"
