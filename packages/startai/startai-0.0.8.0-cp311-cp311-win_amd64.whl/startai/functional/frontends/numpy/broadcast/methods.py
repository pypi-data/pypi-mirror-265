# local
import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back


class broadcast:
    @to_startai_arrays_and_back
    def __init__(self, *args):
        data = startai.broadcast_arrays(*map(startai.array, args))
        self._shape = data[0].shape
        self._ndim = data[0].ndim
        self._index = 0
        self._numiter = len(data)
        self._size = data[0].size
        self._data = (*zip(*(startai.flatten(i) for i in data)),)
        self._iters = tuple(iter(startai.flatten(i)) for i in data)

    @property
    def shape(self):
        return self._shape

    @property
    def ndim(self):
        return self._ndim

    @property
    def nd(self):
        return self._ndim

    @property
    def numiter(self):
        return self._numiter

    @property
    def size(self):
        return self._size

    @property
    def iters(self):
        return self._iters

    @property
    def index(self):
        return self._index

    def __next__(self):
        if self.index < self.size:
            self._index += 1
            return self._data[self.index - 1]
        raise StopIteration

    def __iter__(self):
        return self

    def reset(self):
        self._index = 0
