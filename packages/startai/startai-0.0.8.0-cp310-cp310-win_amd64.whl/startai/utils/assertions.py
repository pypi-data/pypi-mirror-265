import startai


# Helpers #
# ------- #


def _broadcast_inputs(x1, x2):
    x1_, x2_ = x1, x2
    iterables = (list, tuple, startai.Shape)
    if not isinstance(x1_, iterables):
        x1_, x2_ = x2, x1
    if not isinstance(x1_, iterables):
        return [x1], [x2]
    if not isinstance(x2_, iterables):
        x1 = [x1] * len(x2)
    return x1, x2


# General with Custom Message #
# --------------------------- #


def check_less(x1, x2, allow_equal=False, message="", as_array=True):
    def comp_fn(x1, x2):
        return startai.any(x1 > x2), startai.any(x1 >= x2)

    if not as_array:

        def iter_comp_fn(x1_, x2_):
            return any(x1 > x2 for x1, x2 in zip(x1_, x2_)), any(
                x1 >= x2 for x1, x2 in zip(x1_, x2_)
            )

        def comp_fn(x1, x2):  # noqa F811
            return iter_comp_fn(*_broadcast_inputs(x1, x2))

    gt, gt_eq = comp_fn(x1, x2)
    # less_equal
    if allow_equal and gt:
        raise startai.utils.exceptions.StartaiException(
            f"{x1} must be lesser than or equal to {x2}" if message == "" else message
        )
    elif not allow_equal and gt_eq:
        raise startai.utils.exceptions.StartaiException(
            f"{x1} must be lesser than {x2}" if message == "" else message
        )


def check_greater(x1, x2, allow_equal=False, message="", as_array=True):
    def comp_fn(x1, x2):
        return startai.any(x1 < x2), startai.any(x1 <= x2)

    if not as_array:

        def iter_comp_fn(x1_, x2_):
            return any(x1 < x2 for x1, x2 in zip(x1_, x2_)), any(
                x1 <= x2 for x1, x2 in zip(x1_, x2_)
            )

        def comp_fn(x1, x2):  # noqa F811
            return iter_comp_fn(*_broadcast_inputs(x1, x2))

    lt, lt_eq = comp_fn(x1, x2)
    # greater_equal
    if allow_equal and lt:
        raise startai.utils.exceptions.StartaiException(
            f"{x1} must be greater than or equal to {x2}" if message == "" else message
        )
    elif not allow_equal and lt_eq:
        raise startai.utils.exceptions.StartaiException(
            f"{x1} must be greater than {x2}" if message == "" else message
        )


def check_equal(x1, x2, inverse=False, message="", as_array=True):
    # not_equal
    def eq_fn(x1, x2):
        return x1 == x2 if inverse else x1 != x2

    def comp_fn(x1, x2):
        return startai.any(eq_fn(x1, x2))

    if not as_array:

        def iter_comp_fn(x1_, x2_):
            return any(eq_fn(x1, x2) for x1, x2 in zip(x1_, x2_))

        def comp_fn(x1, x2):  # noqa F811
            return iter_comp_fn(*_broadcast_inputs(x1, x2))

    eq = comp_fn(x1, x2)
    if inverse and eq:
        raise startai.utils.exceptions.StartaiException(
            f"{x1} must not be equal to {x2}" if message == "" else message
        )
    elif not inverse and eq:
        raise startai.utils.exceptions.StartaiException(
            f"{x1} must be equal to {x2}" if message == "" else message
        )


def check_isinstance(x, allowed_types, message=""):
    if not isinstance(x, allowed_types):
        raise startai.utils.exceptions.StartaiException(
            f"type of x: {type(x)} must be one of the allowed types: {allowed_types}"
            if message == ""
            else message
        )


def check_exists(x, inverse=False, message=""):
    # not_exists
    if inverse and startai.exists(x):
        raise startai.utils.exceptions.StartaiException(
            "arg must be None" if message == "" else message
        )
    # exists
    elif not inverse and not startai.exists(x):
        raise startai.utils.exceptions.StartaiException(
            "arg must not be None" if message == "" else message
        )


def check_elem_in_list(elem, list, inverse=False, message=""):
    if inverse and elem in list:
        raise startai.utils.exceptions.StartaiException(
            message if message != "" else f"{elem} must not be one of {list}"
        )
    elif not inverse and elem not in list:
        raise startai.utils.exceptions.StartaiException(
            message if message != "" else f"{elem} must be one of {list}"
        )


def check_true(expression, message="expression must be True"):
    if not expression:
        raise startai.utils.exceptions.StartaiException(message)


def check_false(expression, message="expression must be False"):
    if expression:
        raise startai.utils.exceptions.StartaiException(message)


def check_all(results, message="one of the args is False", as_array=True):
    if (as_array and not startai.all(results)) or (not as_array and not all(results)):
        raise startai.utils.exceptions.StartaiException(message)


def check_any(results, message="all of the args are False", as_array=True):
    if (as_array and not startai.any(results)) or (not as_array and not any(results)):
        raise startai.utils.exceptions.StartaiException(message)


def check_all_or_any_fn(
    *args,
    fn,
    type="all",
    limit=(0,),
    message="args must exist according to type and limit given",
    as_array=True,
):
    if type == "all":
        check_all([fn(arg) for arg in args], message, as_array=as_array)
    elif type == "any":
        count = 0
        for arg in args:
            count = count + 1 if fn(arg) else count
        if count not in limit:
            raise startai.utils.exceptions.StartaiException(message)
    else:
        raise startai.utils.exceptions.StartaiException("type must be all or any")


def check_shape(x1, x2, message=""):
    message = (
        message
        if message != ""
        else (
            f"{x1} and {x2} must have the same shape ({startai.shape(x1)} vs"
            f" {startai.shape(x2)})"
        )
    )
    if startai.shape(x1)[:] != startai.shape(x2)[:]:
        raise startai.utils.exceptions.StartaiException(message)


def check_same_dtype(x1, x2, message=""):
    if startai.dtype(x1) != startai.dtype(x2):
        message = (
            message
            if message != ""
            else (
                f"{x1} and {x2} must have the same dtype ({startai.dtype(x1)} vs"
                f" {startai.dtype(x2)})"
            )
        )
        raise startai.utils.exceptions.StartaiException(message)


# Creation #
# -------- #


def check_unsorted_segment_valid_params(data, segment_ids, num_segments):
    if not isinstance(num_segments, int):
        raise TypeError("num_segments must be of integer type")

    valid_dtypes = [
        startai.int32,
        startai.int64,
    ]

    if startai.backend == "torch":
        import torch

        valid_dtypes = [
            torch.int32,
            torch.int64,
        ]
        if isinstance(num_segments, torch.Tensor):
            num_segments = num_segments.item()
    elif startai.backend == "paddle":
        import paddle

        valid_dtypes = [
            paddle.int32,
            paddle.int64,
        ]
        if isinstance(num_segments, paddle.Tensor):
            num_segments = num_segments.item()

    if segment_ids.dtype not in valid_dtypes:
        raise TypeError("segment_ids must have an integer dtype")

    if data.shape[0] != segment_ids.shape[0]:
        raise ValueError("The length of segment_ids should be equal to data.shape[0].")

    if startai.max(segment_ids) >= num_segments:
        error_message = (
            f"segment_ids[{startai.argmax(segment_ids)}] = "
            f"{startai.max(segment_ids)} is out of range [0, {num_segments})"
        )
        raise ValueError(error_message)
    if num_segments <= 0:
        raise ValueError("num_segments must be positive")


# General #
# ------- #


def check_gather_input_valid(params, indices, axis, batch_dims):
    if batch_dims > axis:
        raise startai.utils.exceptions.StartaiException(
            f"batch_dims ({batch_dims}) must be less than or equal to axis ({axis})."
        )
    if params.shape[0:batch_dims] != indices.shape[0:batch_dims]:
        raise startai.utils.exceptions.StartaiException(
            "batch dimensions must match in `params` and `indices`; saw"
            f" {params.shape[0:batch_dims]} vs. {indices.shape[0:batch_dims]}"
        )


def check_gather_nd_input_valid(params, indices, batch_dims):
    if batch_dims >= len(params.shape):
        raise startai.utils.exceptions.StartaiException(
            f"batch_dims = {batch_dims} must be less than rank(`params`) ="
            f" {len(params.shape)}."
        )
    if batch_dims >= len(indices.shape):
        raise startai.utils.exceptions.StartaiException(
            f"batch_dims = {batch_dims}  must be less than rank(`indices`) ="
            f" {len(indices.shape)}."
        )
    if params.shape[0:batch_dims] != indices.shape[0:batch_dims]:
        raise startai.utils.exceptions.StartaiException(
            "batch dimensions must match in `params` and `indices`; saw"
            f" {params.shape[0:batch_dims]} vs. {indices.shape[0:batch_dims]}"
        )
    if indices.shape[-1] > (len(params.shape[batch_dims:])):
        raise startai.utils.exceptions.StartaiException(
            "index innermost dimension length must be <= rank(`params[batch_dims:]`);"
            f" saw: {indices.shape[-1]} vs. {len(params.shape[batch_dims:])} ."
        )


def check_one_way_broadcastable(x1, x2):
    if len(x1) > len(x2):
        return False
    for a, b in zip(x1[::-1], x2[::-1]):
        if a in (1, b):
            pass
        else:
            return False
    return True


def check_inplace_sizes_valid(var, data):
    if not check_one_way_broadcastable(data.shape, var.shape):
        raise startai.utils.exceptions.StartaiException(
            f"Could not output values of shape {var.shape} into array with shape"
            f" {data.shape}."
        )


def check_shapes_broadcastable(var, data):
    if not check_one_way_broadcastable(var, data):
        raise startai.utils.exceptions.StartaiBroadcastShapeError(
            f"Could not broadcast shape {data} to shape {var}."
        )


def check_dimensions(x):
    if len(x.shape) <= 1:
        raise startai.utils.exceptions.StartaiException(
            f"input must have greater than one dimension;  {x} has"
            f" {len(x.shape)} dimensions"
        )


def check_kernel_padding_size(kernel_size, padding_size):
    for i in range(len(kernel_size)):
        if (
            padding_size[i][0] > kernel_size[i] // 2
            or padding_size[i][1] > kernel_size[i] // 2
        ):
            raise ValueError(
                "Padding size should be less than or equal to half of the kernel size."
                f" Got kernel_size: {kernel_size} and padding_size: {padding_size}"
            )


def check_dev_correct_formatting(device):
    assert device[0:3] in ["gpu", "tpu", "cpu"]
    if device != "cpu":
        assert device[3] == ":"
        assert device[4:].isnumeric()


# Jax Specific #
# ------- #


def _check_jax_x64_flag(dtype):
    if (
        startai.backend == "jax"
        and not startai.functional.backends.jax.jax.config.jax_enable_x64
    ):

        startai.utils.assertions.check_elem_in_list(
            dtype,
            ["float64", "int64", "uint64", "complex128"],
            inverse=True,
            message=(
                f"{dtype} output not supported while jax_enable_x64"
                " is set to False, please import jax and enable the flag using "
                "jax.config.update('jax_enable_x64', True)"
            ),
        )
