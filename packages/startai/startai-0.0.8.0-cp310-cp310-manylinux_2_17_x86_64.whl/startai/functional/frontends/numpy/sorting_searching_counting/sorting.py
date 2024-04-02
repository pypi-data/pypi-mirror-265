# global
import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def argsort(
    x,
    /,
    *,
    axis=-1,
    kind=None,
    order=None,
):
    return startai.argsort(x, axis=axis)


@to_startai_arrays_and_back
def lexsort(keys, /, *, axis=-1):
    return startai.lexsort(keys, axis=axis)


@to_startai_arrays_and_back
def msort(a):
    return startai.msort(a)


@to_startai_arrays_and_back
def partition(a, kth, axis=-1, kind="introselect", order=None):
    sorted_arr = startai.sort(a, axis=axis)
    for k in kth:
        index_to_remove = startai.argwhere(a == sorted_arr[k])[0, 0]
        if len(a) == 1:
            a = startai.array([], dtype=a.dtype)
        else:
            a = startai.concat((a[:index_to_remove], a[index_to_remove + 1 :]))
        left = startai.array([], dtype=a.dtype)
        right = startai.array([], dtype=a.dtype)
        equal = startai.array([], dtype=a.dtype)
        for i in range(len(a)):
            if a[i] < sorted_arr[k]:
                left = startai.concat((left, startai.array([a[i]], dtype=a.dtype)))
            elif a[i] > sorted_arr[k]:
                right = startai.concat((right, startai.array([a[i]], dtype=a.dtype)))
            else:
                equal = startai.concat((equal, startai.array([a[i]], dtype=a.dtype)))
        for j in range(len(equal)):
            if len(left) == len(sorted_arr[:k]):
                right = startai.concat((right, startai.array([equal[j]], dtype=a.dtype)))
            else:
                left = startai.concat((left, startai.array([equal[j]], dtype=a.dtype)))
        a = startai.concat((left, startai.array([sorted_arr[k]], dtype=a.dtype), right))
    return a


@to_startai_arrays_and_back
def sort(a, axis=-1, kind=None, order=None):
    return startai.sort(a, axis=axis)


@to_startai_arrays_and_back
def sort_complex(a):
    return startai.sort(a)
