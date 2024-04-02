# global
import inspect
import abc

# local
import startai
from startai.functional.frontends.jax.func_wrapper import (
    to_startai_arrays_and_back,
)
from .creation import linspace, arange, array
from .manipulations import transpose, concatenate, expand_dims


class _AxisConcat(abc.ABC):
    axis: int
    ndmin: int
    trans1d: int

    def __getitem__(self, key):
        key_tup = key if isinstance(key, tuple) else (key,)

        params = [self.axis, self.ndmin, self.trans1d, -1]

        directive = key_tup[0]
        if isinstance(directive, str):
            key_tup = key_tup[1:]
            # check two special cases: matrix directives
            if directive == "r":
                params[-1] = 0
            elif directive == "c":
                params[-1] = 1
            else:
                vec = directive.split(",")
                k = len(vec)
                if k < 4:
                    vec += params[k:]
                else:
                    # ignore everything after the first three comma-separated ints
                    vec = vec[:3] + [params[-1]]
                try:
                    params = list(map(int, vec))
                except ValueError as err:
                    raise ValueError(
                        f"could not understand directive {directive!r}"
                    ) from err

        axis, ndmin, trans1d, matrix = params

        output = []
        for item in key_tup:
            if isinstance(item, slice):
                newobj = _make_1d_grid_from_slice(item)
                item_ndim = 0
            elif isinstance(item, str):
                raise TypeError("string directive must be placed at the beginning")
            else:
                newobj = array(item, copy=False)
                item_ndim = newobj.ndim

            newobj = array(newobj, copy=False, ndmin=ndmin)

            if trans1d != -1 and ndmin - item_ndim > 0:
                shape_obj = tuple(range(ndmin))
                # Calculate number of left shifts, with overflow protection by mod
                num_lshifts = ndmin - abs(ndmin + trans1d + 1) % ndmin
                shape_obj = tuple(shape_obj[num_lshifts:] + shape_obj[:num_lshifts])

                newobj = transpose(newobj, shape_obj)

            output.append(newobj)

        res = concatenate(tuple(output), axis=axis)

        if matrix != -1 and res.ndim == 1:
            # insert 2nd dim at axis 0 or 1
            res = expand_dims(res, matrix)

        return res

    def __len__(self) -> int:
        return 0


class RClass(_AxisConcat):
    axis = 0
    ndmin = 1
    trans1d = -1


class CClass(_AxisConcat):
    axis = -1
    ndmin = 2
    trans1d = 0


# --- Helpers --- #
# --------------- #


def _make_1d_grid_from_slice(s):
    step = 1 if s.step is None else s.step
    start = 0 if s.start is None else s.start
    if s.step is not None and startai.is_complex_dtype(s.step):
        newobj = linspace(start, s.stop, int(abs(step)))
    else:
        newobj = arange(start, s.stop, step)
    return newobj


# --- Main --- #
# ------------ #


@to_startai_arrays_and_back
def choose(arr, choices, out=None, mode="raise"):
    return startai.choose(arr, choices, out=out, mode=mode)


@to_startai_arrays_and_back
def diag(v, k=0):
    return startai.diag(v, k=k)


@to_startai_arrays_and_back
def diag_indices(n, ndim=2):
    idx = startai.arange(n, dtype=int)
    return (idx,) * ndim


@to_startai_arrays_and_back
def diag_indices_from(arr):
    print(arr)
    n = arr.shape[0]
    ndim = startai.get_num_dims(arr)
    if not all(arr.shape[i] == n for i in range(ndim)):
        raise ValueError("All dimensions of input must be of equal length")
    idx = startai.arange(n, dtype=int)
    return (idx,) * ndim


@to_startai_arrays_and_back
def diagonal(a, offset=0, axis1=0, axis2=1):
    return startai.diagonal(a, offset=offset, axis1=axis1, axis2=axis2)


@to_startai_arrays_and_back
def indices(dimensions, dtype=int, sparse=False):
    if sparse:
        return tuple(
            startai.arange(dim)
            .expand_dims(
                axis=[j for j in range(len(dimensions)) if i != j],
            )
            .astype(dtype)
            for i, dim in enumerate(dimensions)
        )
    else:
        grid = startai.meshgrid(*[startai.arange(dim) for dim in dimensions], indexing="ij")
        return startai.stack(grid, axis=0).astype(dtype)


@to_startai_arrays_and_back
def mask_indices(n, mask_func, k=0):
    mask_func_obj = inspect.unwrap(mask_func)
    mask_func_name = mask_func_obj.__name__
    try:
        startai_mask_func_obj = getattr(startai.functional.frontends.jax.numpy, mask_func_name)
        a = startai.ones((n, n))
        mask = startai_mask_func_obj(a, k=k)
        indices = startai.argwhere(mask.startai_array)
        return indices[:, 0], indices[:, 1]
    except AttributeError as e:
        print(f"Attribute error: {e}")


@to_startai_arrays_and_back
def take_along_axis(arr, indices, axis, mode="fill"):
    return startai.take_along_axis(arr, indices, axis, mode=mode)


@to_startai_arrays_and_back
def tril_indices(n, k=0, m=None):
    return startai.tril_indices(n, m, k)


@to_startai_arrays_and_back
def tril_indices_from(arr, k=0):
    return startai.tril_indices(arr.shape[-2], arr.shape[-1], k)


@to_startai_arrays_and_back
def triu_indices(n, k=0, m=None):
    return startai.triu_indices(n, m, k)


@to_startai_arrays_and_back
def triu_indices_from(arr, k=0):
    return startai.triu_indices(arr.shape[-2], arr.shape[-1], k)


@to_startai_arrays_and_back
def unravel_index(indices, shape):
    ret = [x.astype(indices.dtype) for x in startai.unravel_index(indices, shape)]
    return tuple(ret)


c_ = CClass()
r_ = RClass()
