import startai
from startai.functional.frontends.tensorflow.func_wrapper import to_startai_arrays_and_back


# --- Helpers --- #
# --------------- #


def _binary_matches(y_true, y_pred, threshold=0.5):
    threshold = startai.astype(startai.array(threshold), y_pred.dtype)
    y_pred = startai.astype(startai.greater(y_pred, threshold), y_pred.dtype)
    return startai.astype(
        startai.equal(y_true, y_pred), startai.default_float_dtype(as_native=True)
    )


def _cond_convert_labels(y_true):
    are_zeros = startai.equal(y_true, 0.0)
    are_ones = startai.equal(y_true, 1.0)
    is_binary = startai.all(startai.logical_or(are_zeros, are_ones))
    # convert [0, 1] labels to [-1, 1]
    if is_binary:
        return 2.0 * y_true - 1
    return y_true


@to_startai_arrays_and_back
def _sparse_categorical_matches(y_true, y_pred):
    reshape = False
    y_true = startai.array(y_true)
    y_pred = startai.array(y_pred)
    y_true_org_shape = startai.shape(y_true)
    y_true_rank = y_true.ndim
    y_pred_rank = y_pred.ndim
    # y_true shape to (num_samples,)
    if (
        (y_true_rank is not None)
        and (y_pred_rank is not None)
        and (len(startai.shape(y_true)) == len(startai.shape(y_pred)))
    ):
        y_true = startai.squeeze(y_true, axis=-1)
        reshape = True
    y_pred = startai.argmax(y_pred, axis=-1)
    # cast prediction type to be the same as ground truth
    y_pred = startai.astype(y_pred, y_true.dtype, copy=False)
    matches = startai.astype(startai.equal(y_true, y_pred), startai.float32)
    if reshape:
        matches = startai.reshape(matches, shape=y_true_org_shape)
    return matches


@to_startai_arrays_and_back
def _sparse_top_k_categorical_matches(y_true, y_pred, k=5):
    # Temporary composition
    def _in_top_k(targets, predictions, topk):
        # Sanity check
        startai.utils.assertions.check_equal(
            targets.ndim,
            1,
            message="targets must be 1-dimensional",
            as_array=False,
        )
        startai.utils.assertions.check_equal(
            predictions.ndim,
            2,
            message="predictions must be 2-dimensional",
            as_array=False,
        )
        targets_batch = startai.shape(targets)[0]
        pred_batch = startai.shape(predictions)[0]
        startai.utils.assertions.check_equal(
            targets_batch,
            pred_batch,
            message=(
                f"first dim of predictions: {pred_batch} must match targets length:"
                f" {targets_batch}"
            ),
            as_array=False,
        )

        # return array of top k values from the input
        def _top_k(input, topk):
            x = startai.array(input)
            sort = startai.argsort(x, descending=True)
            topk = min(x.shape[-1], topk)

            # Safety check for equal values
            result = []
            for ind, li in enumerate(sort):
                temp = [x[ind, _] for _ in li[:topk]]
                result.append(temp)

            return startai.array(result)

        top_k = _top_k(predictions, topk)

        labels = startai.shape(predictions)[1]
        # float comparison?
        return startai.array(
            [
                (
                    0 <= res < labels
                    and startai.min(top_k[ind] - predictions[ind, res]) <= 1e-9
                )
                for ind, res in enumerate(targets)
            ]
        )

    reshape = False
    y_true = startai.array(y_true)
    y_pred = startai.array(y_pred)
    y_true_org_shape = startai.shape(y_true)
    y_true_rank = y_true.ndim
    y_pred_rank = y_pred.ndim

    # y_pred shape to (batch_size, num_samples), y_true shape to (num_samples,)
    if (y_true_rank is not None) and (y_pred_rank is not None):
        if y_pred_rank > 2:
            y_pred = startai.reshape(y_pred, shape=[-1, y_pred.shape[-1]])
        if y_true_rank > 1:
            reshape = True
            y_true = startai.reshape(y_true, shape=[-1])

    matches = startai.astype(
        _in_top_k(targets=startai.astype(y_true, startai.int32), predictions=y_pred, topk=k),
        startai.float32,
    )

    # return to original shape
    if reshape:
        return startai.reshape(matches, shape=y_true_org_shape)
    return matches


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def binary_accuracy(y_true, y_pred, threshold=0.5):
    return startai.mean(_binary_matches(y_true, y_pred, threshold), axis=-1)


@to_startai_arrays_and_back
def binary_crossentropy(
    y_true, y_pred, from_logits: bool = False, label_smoothing: float = 0.0
):
    y_pred = startai.asarray(y_pred)
    y_true = startai.asarray(y_true, dtype=y_pred.dtype)
    label_smoothing = startai.asarray(label_smoothing, dtype=y_pred.dtype)
    y_true = y_true * (1.0 - label_smoothing) + 0.5 * label_smoothing

    if from_logits:
        zeros = startai.zeros_like(y_pred, dtype=y_pred.dtype)
        cond = y_pred >= zeros
        relu_logits = startai.where(cond, y_pred, zeros)
        neg_abs_logits = startai.where(cond, -y_pred, y_pred)
        bce = startai.add(relu_logits - y_pred * y_true, startai.log1p(startai.exp(neg_abs_logits)))
    else:
        epsilon_ = 1e-7
        y_pred = startai.clip(y_pred, epsilon_, 1.0 - epsilon_)
        bce = y_true * startai.log(y_pred + epsilon_)
        bce += (1 - y_true) * startai.log(1 - y_pred + epsilon_)
        bce = -bce
    return startai.mean(bce, axis=-1).astype(y_pred.dtype)


@to_startai_arrays_and_back
def binary_focal_crossentropy(
    y_true, y_pred, gamma=2.0, from_logits=False, label_smoothing=0.0, axis=-1
):
    y_pred = startai.asarray(y_pred)
    y_true = startai.asarray(y_true, dtype=y_pred.dtype)
    label_smoothing = startai.asarray(label_smoothing, dtype=y_pred.dtype)
    gamma = startai.asarray(gamma, dtype=y_pred.dtype)

    if label_smoothing > 0.0:
        y_true = y_true * (1.0 - label_smoothing) + 0.5 * label_smoothing

    if from_logits:
        sigmoidal = startai.sigmoid(y_pred)
    else:
        sigmoidal = y_pred

    p_t = (y_true * sigmoidal) + ((1 - y_true) * (1 - sigmoidal))
    focal_factor = startai.pow(1.0 - p_t, gamma)

    if from_logits:
        zeros = startai.zeros_like(y_pred, dtype=y_pred.dtype)
        cond = y_pred >= zeros
        relu_logits = startai.where(cond, y_pred, zeros)
        neg_abs_logits = startai.where(cond, -y_pred, y_pred)
        bce = startai.add(relu_logits - y_pred * y_true, startai.log1p(startai.exp(neg_abs_logits)))
    else:
        epsilon_ = 1e-7
        y_pred = startai.clip(y_pred, epsilon_, 1.0 - epsilon_)
        bce = y_true * startai.log(y_pred + epsilon_)
        bce += (1 - y_true) * startai.log(1 - y_pred + epsilon_)
        bce = -bce
    bfce = focal_factor * bce
    return startai.mean(bfce, axis=startai.to_scalar(axis))


@to_startai_arrays_and_back
def categorical_accuracy(y_true, y_pred):
    return _sparse_categorical_matches(startai.argmax(y_true, axis=-1), y_pred)


@to_startai_arrays_and_back
def categorical_crossentropy(y_true, y_pred, from_logits=False, label_smoothing=0.0):
    if from_logits:
        y_pred = startai.softmax(y_pred)
    return startai.mean(startai.categorical_cross_entropy(y_true, y_pred, label_smoothing))


@to_startai_arrays_and_back
def cosine_similarity(y_true, y_pred):
    y_pred = startai.asarray(y_pred)
    y_true = startai.asarray(y_true)

    if len(y_pred.shape) == len(y_pred.shape) and len(y_true.shape) == 2:
        numerator = startai.sum(y_true * y_pred, axis=1)
    else:
        numerator = startai.vecdot(y_true, y_pred)
    denominator = startai.matrix_norm(y_true) * startai.matrix_norm(y_pred)
    return numerator / denominator


@to_startai_arrays_and_back
def hinge(y_true, y_pred):
    y_true = startai.astype(startai.array(y_true), y_pred.dtype, copy=False)
    y_true = _cond_convert_labels(y_true)
    return startai.mean(startai.maximum(1.0 - y_true * y_pred, 0.0), axis=-1)


@to_startai_arrays_and_back
def kl_divergence(y_true, y_pred):
    # clip to range but avoid div-0
    y_true = startai.clip(y_true, 1e-7, 1)
    y_pred = startai.clip(y_pred, 1e-7, 1)
    return startai.sum(y_true * startai.log(y_true / y_pred), axis=-1).astype(y_true.dtype)


@to_startai_arrays_and_back
def log_cosh(y_true, y_pred):
    y_true = startai.astype(y_true, y_pred.dtype)
    diff = y_pred - y_true
    log_val = startai.astype(startai.log(2.0), diff.dtype)
    return startai.mean(diff + startai.softplus(-2.0 * diff) - log_val, axis=-1)


@to_startai_arrays_and_back
def mean_absolute_error(y_true, y_pred):
    return startai.mean(startai.abs(y_true - y_pred), axis=-1)


@to_startai_arrays_and_back
def mean_absolute_percentage_error(y_true, y_pred):
    y_true = startai.astype(y_true, y_pred.dtype, copy=False)

    diff = startai.abs((y_true - y_pred) / startai.maximum(startai.abs(y_true), 1e-7))
    return 100.0 * startai.mean(diff, axis=-1)


@to_startai_arrays_and_back
def mean_squared_error(y_true, y_pred):
    return startai.mean(startai.square(startai.subtract(y_true, y_pred)), axis=-1)


@to_startai_arrays_and_back
def mean_squared_logarithmic_error(y_true, y_pred):
    y_true = startai.astype(y_true, y_pred.dtype)
    first_log = startai.log(startai.maximum(y_pred, 1e-7) + 1.0)
    second_log = startai.log(startai.maximum(y_true, 1e-7) + 1.0)
    return startai.mean(startai.square(startai.subtract(first_log, second_log)), axis=-1)


@to_startai_arrays_and_back
def poisson(y_true, y_pred):
    y_true = startai.astype(y_true, y_pred.dtype, copy=False)
    return startai.mean(y_pred - y_true * startai.log(y_pred + 1e-7), axis=-1)


@to_startai_arrays_and_back
def sparse_categorical_crossentropy(y_true, y_pred, from_logits=False, axis=-1):
    if from_logits:
        y_pred = startai.softmax(y_pred)
    return startai.sparse_cross_entropy(y_true, y_pred, axis=axis)


@to_startai_arrays_and_back
def sparse_top_k_categorical_accuracy(y_true, y_pred, k=5):
    return _sparse_top_k_categorical_matches(y_true, y_pred, k)


@to_startai_arrays_and_back
def squared_hinge(y_true, y_pred):
    y_true = startai.astype(startai.array(y_true), y_pred.dtype)
    y_true = _cond_convert_labels(y_true)
    return startai.mean(startai.square(startai.maximum(1.0 - y_true * y_pred, 0.0)), axis=-1)


kld = kl_divergence
kullback_leibler_divergence = kl_divergence
logcosh = log_cosh
mae = mean_absolute_error
mape = mean_absolute_percentage_error
mse = mean_squared_error
msle = mean_squared_logarithmic_error
