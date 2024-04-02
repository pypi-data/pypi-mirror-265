# local
import startai.functional.frontends.tensorflow as tf_frontend


class ResourceVariable(tf_frontend.Variable):
    def __repr__(self):
        return (
            repr(self._startai_array).replace(
                "startai.array",
                "startai.functional.frontends.tensorflow.python.ops.resource_variable_ops.ResourceVariable",
            )[:-1]
            + ", shape="
            + str(self._startai_array.shape)
            + ", dtype="
            + str(self._startai_array.dtype)
            + ")"
        )
