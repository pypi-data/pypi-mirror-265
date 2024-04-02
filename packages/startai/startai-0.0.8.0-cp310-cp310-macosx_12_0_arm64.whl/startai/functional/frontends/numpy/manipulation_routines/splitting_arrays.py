# local
import startai
from startai.functional.frontends.numpy.func_wrapper import to_startai_arrays_and_back


@to_startai_arrays_and_back
def array_split(ary, indices_or_sections, axis=0):
    return startai.split(
        ary, num_or_size_splits=indices_or_sections, axis=axis, with_remainder=True
    )


@to_startai_arrays_and_back
def dsplit(ary, indices_or_sections):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[2]])
            .astype(startai.int8)
            .to_list()
        )
    return startai.dsplit(ary, indices_or_sections)


@to_startai_arrays_and_back
def hsplit(ary, indices_or_sections):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        if ary.ndim == 1:
            indices_or_sections = (
                startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[0]])
                .astype(startai.int8)
                .to_list()
            )
        else:
            indices_or_sections = (
                startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[1]])
                .astype(startai.int8)
                .to_list()
            )
    return startai.hsplit(ary, indices_or_sections)


@to_startai_arrays_and_back
def split(ary, indices_or_sections, axis=0):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[axis]])
            .astype(startai.int8)
            .to_list()
        )
    return startai.split(
        ary, num_or_size_splits=indices_or_sections, axis=axis, with_remainder=True
    )


@to_startai_arrays_and_back
def vsplit(ary, indices_or_sections):
    if isinstance(indices_or_sections, (list, tuple, startai.Array)):
        indices_or_sections = (
            startai.diff(indices_or_sections, prepend=[0], append=[ary.shape[0]])
            .astype(startai.int8)
            .to_list()
        )
    return startai.vsplit(ary, indices_or_sections)
