# global

# local
import startai

# import startai.functional.frontends.onnx as onnx_frontend


class Tensor:
    def __init__(self, array):
        self._startai_array = (
            startai.array(array) if not isinstance(array, startai.Array) else array
        )

    def __len__(self):
        return len(self._startai_array)

    def __repr__(self):
        return str(self.startai_array.__repr__()).replace(
            "startai.array", "startai.frontends.onnx.Tensor"
        )

    # Properties #
    # ---------- #

    @property
    def startai_array(self):
        return self._startai_array

    @property
    def device(self):
        return self.startai_array.device

    @property
    def dtype(self):
        return self.startai_array.dtype

    @property
    def shape(self):
        return self.startai_array.shape

    @property
    def ndim(self):
        return self.startai_array.ndim

    # Setters #
    # --------#

    @startai_array.setter
    def startai_array(self, array):
        self._startai_array = (
            startai.array(array) if not isinstance(array, startai.Array) else array
        )
