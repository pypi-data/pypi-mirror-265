# global

# local
import startai
import startai.functional.frontends.mxnet as mxnet_frontend


class ndarray:
    def __init__(self, array):
        self._startai_array = (
            startai.array(array) if not isinstance(array, startai.Array) else array
        )

    def __repr__(self):
        return str(self.startai_array.__repr__()).replace(
            "startai.array", "startai.frontends.mxnet.numpy.array"
        )

    # Properties #
    # ---------- #

    @property
    def startai_array(self):
        return self._startai_array

    @property
    def dtype(self):
        return self.startai_array.dtype

    @property
    def shape(self):
        return self.startai_array.shape

    # Instance Methods #
    # ---------------- #

    def __add__(self, other):
        return mxnet_frontend.numpy.add(self, other)
