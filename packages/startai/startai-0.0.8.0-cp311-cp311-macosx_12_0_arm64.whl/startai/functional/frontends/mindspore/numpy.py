import startai


def array(obj, dtype=None, copy=True, ndmin=4):
    ret = startai.array(obj, dtype=dtype, copy=copy)
    while ndmin > len(ret.shape):
        ret = startai.expand_dims(ret, axis=0)
    return ret
