import startai


def coordinate_delta(sum_grad, sum_hess, w, reg_alpha, reg_lambda):
    mask = startai.where(sum_hess < 1e-5, 0.0, 1.0)

    sum_grad_l2 = sum_grad + reg_lambda * w
    sum_hess_l2 = sum_hess + reg_lambda
    tmp = w - sum_grad_l2 / sum_hess_l2
    return startai.where(
        tmp >= 0,
        startai.fmax(-(sum_grad_l2 + reg_alpha) / sum_hess_l2, -w) * mask,
        startai.fmin(-(sum_grad_l2 - reg_alpha) / sum_hess_l2, -w) * mask,
    )


def coordinate_delta_bias(sum_grad, sum_hess):
    return -sum_grad / sum_hess


def get_bias_gradient(gpair):
    # filter out pairs with negative hessians(should not be included in the sum)
    mask = startai.where(gpair[:, 1] < 0.0, 0.0, 1.0)

    sum_grad = startai.sum(gpair[:, 0] * mask)
    sum_hess = startai.sum(gpair[:, 1] * mask)
    return sum_grad, sum_hess


def update_bias_residual(dbias, gpair):
    # ToDo: skip update where dbias==0 and modify for several biases
    # filter out updates where hessians are less than zero
    mask = startai.where(gpair[:, 1] < 0.0, 0.0, 1.0)

    # we only update gradients, hessians remain the same
    return startai.expand_dims(gpair[:, 0] + gpair[:, 1] * mask * dbias, axis=1)
