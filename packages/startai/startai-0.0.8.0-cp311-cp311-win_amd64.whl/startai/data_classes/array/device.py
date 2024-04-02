# global
import abc
from typing import Union, Optional, Any

import startai


# ToDo: implement all methods here as public instance methods


class _ArrayWithDevice(abc.ABC):
    def dev(
        self: startai.Array, *, as_native: bool = False
    ) -> Union[startai.Device, startai.NativeDevice]:
        """startai.Array instance method variant of startai.dev. This method simply
        wraps the function, and so the docstring for startai.dev also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            array for which to get the device handle.
        as_native
            Whether or not to return the dev in native format. Default is ``False``.

        Examples
        --------
        >>> x = startai.array([[2, 5, 4, 1], [3, 1, 5, 2]])
        >>> y = x.dev(as_native=True)
        >>> print(y)
        cpu
        """
        return startai.dev(self, as_native=as_native)

    def to_device(
        self: startai.Array,
        device: Union[startai.Device, startai.NativeDevice],
        *,
        stream: Optional[Union[int, Any]] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.to_device. This method
        simply wraps the function, and so the docstring for startai.to_device also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array to be moved to the desired device
        device
            device to move the input array `x` to
        stream
            stream object to use during copy. In addition to the types
            supported in array.__dlpack__(), implementations may choose to
            support any library-specific stream object with the caveat that
            any code using such an object would not be portable.
        out
            optional output array, for writing the result to. It must have
            a shape that the inputs broadcast to.

        Examples
        --------
        >>> x = startai.array([2, 5, 4, 1])
        >>> y = x.to_device('cpu')
        >>> print(y.device)
        cpu
        """
        return startai.to_device(self._data, device, stream=stream, out=out)
