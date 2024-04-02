"""Collection of tests for the demos."""

# global
import pytest

# local
import startai
import startai.functional.backends.numpy


# functional api
def test_array(on_device):
    import jax.numpy as jnp

    assert startai.concat((jnp.ones((1,)), jnp.ones((1,))), axis=-1).shape == (2,)
    import tensorflow as tf

    assert startai.concat((tf.ones((1,)), tf.ones((1,))), axis=-1).shape == (2,)
    import numpy as np

    assert startai.concat((np.ones((1,)), np.ones((1,))), axis=-1).shape == (2,)
    import torch

    assert startai.concat((torch.ones((1,)), torch.ones((1,))), axis=-1).shape == (2,)
    import paddle

    assert startai.concat((paddle.ones((1,)), paddle.ones((1,))), axis=-1).shape == (2,)


# Tests #
# ------#


# training
def test_training_demo(on_device, backend_fw):
    if backend_fw == "numpy":
        # numpy does not support gradients
        pytest.skip()

    startai.set_backend(backend_fw)

    class MyModel(startai.Module):
        def __init__(self):
            self.linear0 = startai.Linear(3, 64)
            self.linear1 = startai.Linear(64, 1)
            startai.Module.__init__(self)

        def _forward(self, x):
            x = startai.relu(self.linear0(x))
            return startai.sigmoid(self.linear1(x))

    model = MyModel()
    optimizer = startai.Adam(1e-4)
    x_in = startai.array([1.0, 2.0, 3.0])
    target = startai.array([0.0])

    def loss_fn(v):
        out = model(x_in, v=v)
        return startai.mean((out - target) ** 2)

    for step in range(100):
        loss, grads = startai.execute_with_gradients(loss_fn, model.v)
        model.v = optimizer.step(model.v, grads)

    startai.previous_backend()
