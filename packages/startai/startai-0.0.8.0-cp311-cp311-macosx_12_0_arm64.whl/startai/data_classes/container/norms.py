# global
from typing import Optional, List, Union

# local
import startai
from startai.data_classes.container.base import ContainerBase

# ToDo: implement all methods here as public instance methods


# noinspection PyMissingConstructor
class _ContainerWithNorms(ContainerBase):
    def layer_norm(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        normalized_idxs: List[Union[int, startai.Container]],
        /,
        *,
        scale: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        offset: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        eps: Union[float, startai.Container] = 1e-05,
        new_std: Union[float, startai.Container] = 1.0,
        out: Optional[Union[startai.Array, startai.Container]] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.layer_norm. This method
        simply wraps the function, and so the docstring for startai.layer_norm also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input container
        normalized_idxs
            Indices to apply the normalization to.
        scale
            Learnable gamma variables for elementwise post-multiplication,
            default is ``None``.
        offset
            Learnable beta variables for elementwise post-addition, default is ``None``.
        eps
            small constant to add to the denominator. Default is ``1e-05``.
        new_std
            The standard deviation of the new normalized values. Default is 1.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The layer after applying layer normalization.

        Examples
        --------
        With one :class:`startai.Container` input:
        >>> x = startai.Container({'a': startai.array([7., 10., 12.]),
        ...                    'b': startai.array([[1., 2., 3.], [4., 5., 6.]])})
        >>> normalized_idxs = [0]
        >>> norm = x.layer_norm(normalized_idxs, eps=1.25, scale=0.3)
        >>> print(norm)
        {
            a: startai.array([-0.34198591, 0.04274819, 0.29923761]),
            b: startai.array([[-0.24053511, -0.24053511, -0.24053511],
                          [0.24053511, 0.24053511, 0.24053511]])
        }
        With multiple :class:`startai.Container` inputs:
        >>> x = startai.Container({'a': startai.array([7., 10., 12.]),
        ...                    'b': startai.array([[1., 2., 3.], [4., 5., 6.]])})
        >>> normalized_idxs = startai.Container({'a': [0], 'b': [1]})
        >>> new_std = startai.Container({'a': 1.25, 'b': 1.5})
        >>> bias = startai.Container({'a': [0.2, 0.5, 0.7], 'b': 0.3})
        >>> norm = x.layer_norm(normalized_idxs, new_std=new_std, offset=1)
        >>> print(norm)
        {
            a: startai.array([-1.62221265, 0.20277636, 1.41943574]),
            b: startai.array([[-1.83710337, 0., 1.83710337],
                          [-1.83710337, 0., 1.83710337]])
        }
        """
        return startai.layer_norm(
            self,
            normalized_idxs,
            scale=scale,
            offset=offset,
            eps=eps,
            new_std=new_std,
            out=out,
        )
