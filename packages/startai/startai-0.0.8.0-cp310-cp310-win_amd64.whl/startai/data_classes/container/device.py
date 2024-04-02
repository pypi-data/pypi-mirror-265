# local
from typing import Union, Optional, Any, List, Dict

import startai
from startai.data_classes.container.base import ContainerBase


# ToDo: implement all methods here as public instance methods


class _ContainerWithDevice(ContainerBase):
    @staticmethod
    def _static_dev(
        x: startai.Container, /, *, as_native: Union[bool, startai.Container] = False
    ) -> startai.Container:
        """startai.Container static method variant of startai.dev. This method simply
        wraps the function, and so the docstring for startai.dev also applies to
        this method with minimal changes.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[2, 3], [3, 5]]),
        ...                   b=startai.native_array([1, 2, 4, 5, 7]))
        >>> as_native = startai.Container(a=True, b=False)
        >>> y = startai.Container.static_dev(x, as_native=as_native)
        >>> print(y)
        {
            a: device(type=cpu),
            b: cpu
        }
        """
        return ContainerBase.cont_multi_map_in_function("dev", x, as_native=as_native)

    def dev(
        self: startai.Container, as_native: Union[bool, startai.Container] = False
    ) -> startai.Container:
        """startai.Container instance method variant of startai.dev. This method simply
        wraps the function, and so the docstring for startai.dev also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            contaioner of arrays for which to get the device handle.
        as_native
            Whether or not to return the dev in native format. Default is ``False``.

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[2, 3, 1], [3, 5, 3]]),
        ...                   b=startai.native_array([[1, 2], [4, 5]]))
        >>> as_native = startai.Container(a=False, b=True)
        >>> y = x.dev(as_native=as_native)
        >>> print(y)
        {
            a:cpu,
            b:cpu
        }
        """
        return self._static_dev(self, as_native=as_native)

    @staticmethod
    def _static_to_device(
        x: Union[startai.Container, startai.Array, startai.NativeArray],
        device: Union[startai.Device, startai.NativeDevice, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        stream: Optional[Union[int, Any, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.to_device. This method
        simply wraps the function, and so the docstring for startai.to_device also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
           input array to be moved to the desired device
        device
            device to move the input array `x` to
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        stream
            stream object to use during copy. In addition to the types supported
            in array.__dlpack__(), implementations may choose to support any
            library-specific stream object with the caveat that any code using
            such an object would not be portable.
        out
            optional output array, for writing the result to. It must have a
            shape that the inputs broadcast to.

        Returns
        -------
        ret
            input array x placed on the desired device

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[2, 3, 1], [3, 5, 3]]),
        ...                   b=startai.native_array([[1, 2], [4, 5]]))
        >>> y = startai.Container.static_to_device(x, 'cpu')
        >>> print(y.a.device, y.b.device)
        cpu cpu
        """
        return ContainerBase.cont_multi_map_in_function(
            "to_device",
            x,
            device,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            stream=stream,
            out=out,
        )

    def to_device(
        self: startai.Container,
        device: Union[startai.Device, startai.NativeDevice, startai.Container],
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        *,
        stream: Optional[Union[int, Any, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.to_device. This method
        simply wraps the function, and so the docstring for startai.to_device also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
           input array to be moved to the desired device
        device
            device to move the input array `x` to
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If True, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``True``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        stream
            stream object to use during copy. In addition to the types supported
            in array.__dlpack__(), implementations may choose to support any
            library-specific stream object with the caveat that any code using
            such an object would not be portable.
        out
            optional output array, for writing the result to. It must have a
            shape that the inputs broadcast to.

        Returns
        -------
        ret
            input array x placed on the desired device

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[2, 3, 1], [3, 5, 3]]),
        ...                   b=startai.native_array([[1, 2], [4, 5]]))
        >>> y = x.to_device('cpu')
        >>> print(y.a.device, y.b.device)
        cpu cpu
        """
        return self._static_to_device(
            self,
            device,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            stream=stream,
            out=out,
        )
