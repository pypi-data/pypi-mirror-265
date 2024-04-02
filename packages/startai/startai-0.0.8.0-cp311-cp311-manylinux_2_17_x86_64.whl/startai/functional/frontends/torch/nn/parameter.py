import startai
from startai.functional.frontends.torch.tensor import Tensor
import startai.functional.frontends.torch as torch_frontend
from startai.functional.startai.gradients import _variable, _is_variable, _variable_data


class Parameter(Tensor):
    def __init__(self, data=None, device=None, requires_grad=True):
        if data is None:
            data = torch_frontend.empty(0)
        startai_array = (
            startai.array(data) if not hasattr(data, "_startai_array") else data.startai_array
        )
        startai_array = _variable(startai_array) if not _is_variable(data) else startai_array
        self._startai_array = startai.to_device(startai_array, device) if device else startai_array
        self._data = Tensor(_variable_data(self._startai_array), _init_overload=True)
        self._requires_grad = requires_grad
        self._is_leaf = True
        self._grads = None
        self.grad_fn = None

    def __deepcopy__(self, memo):
        if id(self) in memo:
            return memo[id(self)]
        else:
            result = type(self)(self.data.clone(), self.requires_grad)
            memo[id(self)] = result
            return result

    def __repr__(self):
        return "Parameter containing:\n" + super().__repr__()
