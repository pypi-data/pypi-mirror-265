import startai
from startai.functional.frontends.mxnet.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def beta(a, b, size=None, dtype=None, device=None):
    return startai.experimental.beta(a, b, shape=size, dtype=dtype, device=device)


@to_startai_arrays_and_back
def chisquare(df, size=None, dtype=None, device=None):
    return startai.experimental.gamma(
        df * 0.5,
        0.5,
        shape=size,
        dtype=dtype,
        device=device,
    )


@to_startai_arrays_and_back
def gamma(shape, scale=1.0, size=None, dtype=None, device=None, out=None):
    return startai.experimental.gamma(
        shape, scale, shape=size, dtype=dtype, device=device, out=out
    )


@to_startai_arrays_and_back
def multinomial(n, pvals, size=None, **kwargs):
    num_samples = startai.prod(size)
    assert not startai.exists(size) or (len(size) > 0 and len(size) < 3)
    batch_size = 1
    if startai.exists(size):
        if len(size) == 2:
            batch_size = size[0]
            num_samples = size[1]
        else:
            num_samples = size[0]
    else:
        num_samples = len(pvals)
    return startai.multinomial(n, num_samples, batch_size=batch_size, probs=pvals, **kwargs)


@to_startai_arrays_and_back
def normal(loc=0.0, scale=1.0, size=None, dtype=None, device=None, out=None):
    return startai.random_normal(
        mean=loc, std=scale, shape=size, device=device, dtype=dtype, out=out
    )


@to_startai_arrays_and_back
def power(a, size=None, dtype=None, device=None, out=None):
    # special case of beta function
    b = startai.ones_like(a)
    return startai.experimental.beta(a, b, shape=size, dtype=dtype, device=device, out=out)


@to_startai_arrays_and_back
def rand(*size, **kwargs):
    return startai.random_uniform(shape=size, **kwargs)


@to_startai_arrays_and_back
def randint(low, high=None, size=None, dtype=None, device=None, out=None):
    return startai.randint(low, high, shape=size, device=device, dtype=dtype, out=out)


@to_startai_arrays_and_back
def shuffle(x, axis=0):
    startai.shuffle(x, axis)


@to_startai_arrays_and_back
def uniform(low=0.0, high=1.0, size=None, dtype=None, device=None, out=None):
    return startai.random_uniform(
        low=low, high=high, shape=size, device=device, dtype=dtype, out=out
    )
