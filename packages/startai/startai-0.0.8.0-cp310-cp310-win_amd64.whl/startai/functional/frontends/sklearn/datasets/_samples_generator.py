import startai
import numbers
from startai.functional.frontends.numpy.func_wrapper import outputs_to_frontend_arrays


@outputs_to_frontend_arrays
def make_circles(
    n_samples=100, *, shuffle=True, noise=None, random_state=None, factor=0.8
):
    # numbers.Integral also includes bool
    if isinstance(n_samples, numbers.Integral):
        n_samples_out = n_samples // 2
        n_samples_in = n_samples - n_samples_out
    elif isinstance(n_samples, tuple):
        n_samples_out, n_samples_in = n_samples

    outer_circ_x = startai.cos(
        startai.linspace(0, 2 * startai.pi, num=n_samples_out, endpoint=False)
    )
    outer_circ_y = startai.sin(
        startai.linspace(0, 2 * startai.pi, num=n_samples_out, endpoint=False)
    )
    inner_circ_x = (
        startai.cos(startai.linspace(0, 2 * startai.pi, num=n_samples_in, endpoint=False)) * factor
    )
    inner_circ_y = (
        startai.sin(startai.linspace(0, 2 * startai.pi, num=n_samples_in, endpoint=False)) * factor
    )
    X = startai.concat(
        [
            startai.stack([outer_circ_x, outer_circ_y], axis=1),
            startai.stack([inner_circ_x, inner_circ_y], axis=1),
        ],
        axis=0,
    )
    y = startai.concat(
        [
            startai.zeros(n_samples_out, dtype=startai.int32),
            startai.ones(n_samples_in, dtype=startai.int32),
        ],
        axis=0,
    )
    return X, y


@outputs_to_frontend_arrays
def make_moons(n_samples=100, *, shuffle=True, noise=None, random_state=None):
    if isinstance(n_samples, numbers.Integral):
        n_samples_out = n_samples // 2
        n_samples_in = n_samples - n_samples_out
    elif isinstance(n_samples, tuple):
        n_samples_out, n_samples_in = n_samples

    outer_circ_x = startai.cos(startai.linspace(0, startai.pi, n_samples_out))
    outer_circ_y = startai.sin(startai.linspace(0, startai.pi, n_samples_out))
    inner_circ_x = 1 - startai.cos(startai.linspace(0, startai.pi, n_samples_in))
    inner_circ_y = 1 - startai.sin(startai.linspace(0, startai.pi, n_samples_in)) - 0.5

    X = startai.concat(
        [
            startai.stack([outer_circ_x, outer_circ_y], axis=1),
            startai.stack([inner_circ_x, inner_circ_y], axis=1),
        ],
        axis=0,
    )
    y = startai.concat(
        [
            startai.zeros(n_samples_out, dtype=startai.int32),
            startai.ones(n_samples_in, dtype=startai.int32),
        ],
        axis=0,
    )

    return X, y
