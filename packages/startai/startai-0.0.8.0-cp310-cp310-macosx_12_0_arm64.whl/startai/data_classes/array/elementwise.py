# global
import abc
from typing import Optional, Union, Literal

# local
import startai


# noinspection PyUnresolvedReferences
class _ArrayWithElementwise(abc.ABC):
    def abs(
        self: Union[float, startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:  # noqa
        """startai.Array instance method variant of startai.abs. This method simply
        wraps the function, and so the docstring for startai.abs also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the absolute value of each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([2.6, -6.6, 1.6, -0])
        >>> y = x.abs()
        >>> print(y)
        startai.array([ 2.6, 6.6, 1.6, 0.])
        """
        return startai.abs(self, out=out)

    def acosh(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.acosh. This method simply
        wraps the function, and so the docstring for startai.acosh also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent the area of a hyperbolic sector.
            Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse hyperbolic cosine
            of each element in ``self``.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([2., 10.0, 1.0])
        >>> y = x.acosh()
        >>> print(y)
        startai.array([1.32, 2.99, 0.  ])
        """
        return startai.acosh(self._data, out=out)

    def acos(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.acos. This method simply
        wraps the function, and so the docstring for startai.acos also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse cosine of each element in ``self``.
            The  returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([1.0, 0.0, -0.9])
        >>> y = x.acos()
        >>> print(y)
        startai.array([0.  , 1.57, 2.69])
        """
        return startai.acos(self._data, out=out)

    def add(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        alpha: Optional[Union[int, float]] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.add. This method simply
        wraps the function, and so the docstring for startai.add also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a numeric data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.
        alpha
            optional scalar multiplier for ``x2``.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise sums. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x.add(y)
        >>> print(z)
        startai.array([5, 7, 9])

        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x.add(y, alpha=2)
        >>> print(z)
        startai.array([9, 12, 15])
        """
        return startai.add(self._data, x2, alpha=alpha, out=out)

    def asin(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.asin. This method simply
        wraps the function, and so the docstring for startai.asin also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse sine of each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([-1., 1., 4., 0.8])
        >>> y = x.asin()
        >>> print(y)
        startai.array([-1.57, 1.57, nan, 0.927])

        >>> x = startai.array([-3., -0.9, 1.5, 2.8])
        >>> y = startai.zeros(4)
        >>> x.asin(out=y)
        >>> print(y)
        startai.array([nan, -1.12, nan, nan])
        """
        return startai.asin(self._data, out=out)

    def asinh(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.asinh. This method simply
        wraps the function, and so the docstring for startai.asinh also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent the area of a hyperbolic sector.
            Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse hyperbolic sine of each element in ``self``.
            The returned array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([-1., 0., 3.])
        >>> y = x.asinh()
        >>> print(y)
        startai.array([-0.881,  0.   ,  1.82 ])
        """
        return startai.asinh(self._data, out=out)

    def atan(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.atan. This method simply
        wraps the function, and so the docstring for startai.atan also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse tangent of each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([1.0, 0.5, -0.5])
        >>> y = x.atan()
        >>> print(y)
        startai.array([ 0.785,  0.464, -0.464])
        """
        return startai.atan(self._data, out=out)

    def atan2(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.atan2. This method simply
        wraps the function, and so the docstring for startai.atan2 also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array corresponding to the y-coordinates.
            Should have a real-valued floating-point data type.
        x2
            second input array corresponding to the x-coordinates.
            Must be compatible with ``self``(see :ref:`broadcasting`).
            Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse tangent of the quotient ``self/x2``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1.0, 0.5, 0.0, -0.5, 0.0])
        >>> y = startai.array([1.0, 2.0, -1.5, 0, 1.0])
        >>> z = x.atan2(y)
        >>> print(z)
        startai.array([ 0.785,  0.245,  3.14 , -1.57 ,  0.   ])

        >>> x = startai.array([1.0, 2.0])
        >>> y = startai.array([-2.0, 3.0])
        >>> z = startai.zeros(2)
        >>> x.atan2(y, out=z)
        >>> print(z)
        startai.array([2.68 , 0.588])

        >>> nan = float("nan")
        >>> x = startai.array([nan, 1.0, 1.0, -1.0, -1.0])
        >>> y = startai.array([1.0, +0, -0, +0, -0])
        >>> x.atan2(y)
        startai.array([  nan,  1.57,  1.57, -1.57, -1.57])

        >>> x = startai.array([+0, +0, +0, +0, -0, -0, -0, -0])
        >>> y = startai.array([1.0, +0, -0, -1.0, 1.0, +0, -0, -1.0])
        >>> x.atan2(y)
        startai.array([0.  , 0.  , 0.  , 3.14, 0.  , 0.  , 0.  , 3.14])
        >>> y.atan2(x)
        startai.array([ 1.57,  0.  ,  0.  , -1.57,  1.57,  0.  ,  0.  , -1.57])

        >>> inf = float("infinity")
        >>> x = startai.array([inf, -inf, inf, inf, -inf, -inf])
        >>> y = startai.array([1.0, 1.0, inf, -inf, inf, -inf])
        >>> z = x.atan2(y)
        >>> print(z)
        startai.array([ 1.57 , -1.57 ,  0.785,  2.36 , -0.785, -2.36 ])

        >>> x = startai.array([2.5, -1.75, 3.2, 0, -1.0])
        >>> y = startai.array([-3.5, 2, 0, 0, 5])
        >>> z = x.atan2(y)
        >>> print(z)
        startai.array([ 2.52 , -0.719,  1.57 ,  0.   , -0.197])

        >>> x = startai.array([[1.1, 2.2, 3.3], [-4.4, -5.5, -6.6]])
        >>> y = x.atan2(x)
        >>> print(y)
        startai.array([[ 0.785,  0.785,  0.785],
            [-2.36 , -2.36 , -2.36 ]])
        """
        return startai.atan2(self._data, x2, out=out)

    def atanh(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.atanh. This method simply
        wraps the function, and so the docstring for startai.atanh also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent the area of a hyperbolic sector.
            Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse hyperbolic tangent of each element
            in ``self``. The returned array must have a floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([0.0, 0.5, -0.9])
        >>> y = x.atanh()
        >>> print(y)
        startai.array([ 0.   ,  0.549, -1.47 ])
        """
        return startai.atanh(self._data, out=out)

    def bitwise_and(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.bitwise_and. This method
        simply wraps the function, and so the docstring for startai.bitwise_and
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([True, False])
        >>> y = startai.array([True, True])
        >>> x.bitwise_and(y, out=y)
        >>> print(y)
        startai.array([ True, False])

        >>> x = startai.array([[7],[8],[9]])
        >>> y = startai.native_array([[10],[11],[12]])
        >>> z = x.bitwise_and(y)
        >>> print(z)
        startai.array([[2],[8],[8]])
        """
        return startai.bitwise_and(self._data, x2, out=out)

    def bitwise_left_shift(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.bitwise_left_shift. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_left_shift also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.
        """
        return startai.bitwise_left_shift(self._data, x2, out=out)

    def bitwise_invert(
        self: startai.Array, *, out: Optional[startai.Array] = None
    ) -> startai.Array:
        """startai.Array instance method variant of startai.bitwise_invert. This method
        simply wraps the function, and so the docstring for startai.bitiwse_invert
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have an integer or boolean data type.

        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([1, 6, 9])
        >>> y = x.bitwise_invert()
        >>> print(y)
        startai.array([-2, -7, -10])

        >>> x = startai.array([False, True])
        >>> y = x.bitwise_invert()
        >>> print(y)
        startai.array([True, False])
        """
        return startai.bitwise_invert(self._data, out=out)

    def bitwise_or(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.bitwise_or. This method
        simply wraps the function, and so the docstring for startai.bitwise_or also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``

        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x.bitwise_or(y)
        >>> print(z)
        startai.array([5, 7, 7])
        """
        return startai.bitwise_or(self._data, x2, out=out)

    def bitwise_right_shift(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.bitwise_right_shift. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_right_shift also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> a = startai.array([[2, 3, 4], [5, 10, 64]])
        >>> b = startai.array([0, 1, 2])
        >>> y = a.bitwise_right_shift(b)
        >>> print(y)
        startai.array([[ 2,  1,  1],
                    [ 5,  5, 16]])
        """
        return startai.bitwise_right_shift(self._data, x2, out=out)

    def bitwise_xor(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.bitwise_xor. This method
        simply wraps the function, and so the docstring for startai.bitwise_xor
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> a = startai.array([[89, 51, 32], [14, 18, 19]])
        >>> b = startai.array([[[19, 26, 27], [22, 23, 20]]])
        >>> y = a.bitwise_xor(b)
        >>> print(y)
        startai.array([[[74,41,59],[24,5,7]]])
        """
        return startai.bitwise_xor(self._data, x2, out=out)

    def ceil(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.ceil. This method simply
        wraps the function, and so the docstring for startai.ceil also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rounded result for each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([5.5, -2.5, 1.5, -0])
        >>> y = x.ceil()
        >>> print(y)
        startai.array([ 6., -2.,  2.,  0.])
        """
        return startai.ceil(self._data, out=out)

    def cos(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.cos. This method simply
        wraps the function, and so the docstring for startai.cos also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements are each expressed in radians. Should have a
            floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the cosine of each element in ``self``. The returned
            array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x = startai.array([1., 0., 2.,])
        >>> y = x.cos()
        >>> print(y)
        startai.array([0.54, 1., -0.416])

        >>> x = startai.array([-3., 0., 3.])
        >>> y = startai.zeros(3)
        >>> x.cos(out=y)
        >>> print(y)
        startai.array([-0.99,  1.  , -0.99])

        >>> x = startai.array([[0., 1.,], [2., 3.]])
        >>> y = x.cos()
        >>> print(y)
        startai.array([[1., 0.540], [-0.416, -0.990]])
        """
        return startai.cos(self._data, out=out)

    def cosh(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.cosh. This method simply
        wraps the function, and so the docstring for startai.cosh also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent a hyperbolic angle.
            Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the hyperbolic cosine of each element in ``self``.
            The returned array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1., 2., 3.])
        >>> print(x.cosh())
            startai.array([1.54, 3.76, 10.1])

        >>> x = startai.array([0.23, 3., -1.2])
        >>> y = startai.zeros(3)
        >>> print(x.cosh(out=y))
            startai.array([1.03, 10.1, 1.81])
        """
        return startai.cosh(self._data, out=out)

    def divide(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.divide. This method simply
        wraps the function, and so the docstring for startai.divide also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array. Should have a real-valued data type.
        x2
            divisor input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x1 = startai.array([2., 7., 9.])
        >>> x2 = startai.array([2., 2., 2.])
        >>> y = x1.divide(x2)
        >>> print(y)
        startai.array([1., 3.5, 4.5])

        With mixed :class:`startai.Array` and `startai.NativeArray` inputs:

        >>> x1 = startai.array([2., 7., 9.])
        >>> x2 = startai.native_array([2., 2., 2.])
        >>> y = x1.divide(x2)
        >>> print(y)
        startai.array([1., 3.5, 4.5])
        """
        return startai.divide(self._data, x2, out=out)

    def equal(
        self: startai.Array,
        x2: Union[float, startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.equal. This method simply
        wraps the function, and so the docstring for startai.equal also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            May have any data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x1 = startai.array([2., 7., 9.])
        >>> x2 = startai.array([1., 7., 9.])
        >>> y = x1.equal(x2)
        >>> print(y)
        startai.array([False, True, True])

        With mixed :class:`startai.Array` and :class:`startai.NativeArray` inputs:

        >>> x1 = startai.array([2.5, 7.3, 9.375])
        >>> x2 = startai.native_array([2.5, 2.9, 9.375])
        >>> y = x1.equal(x2)
        >>> print(y)
        startai.array([True, False,  True])

        With mixed :class:`startai.Array` and `float` inputs:

        >>> x1 = startai.array([2.5, 7.3, 9.375])
        >>> x2 = 7.3
        >>> y = x1.equal(x2)
        >>> print(y)
        startai.array([False, True, False])

        With mixed :class:`startai.Container` and :class:`startai.Array` inputs:

        >>> x1 = startai.array([3., 1., 0.9])
        >>> x2 = startai.Container(a=startai.array([12., 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> y = x1.equal(x2)
        >>> print(y)
        {
            a: startai.array([False, False, False]),
            b: startai.array([True, True, True])
        }
        """
        return startai.equal(self._data, x2, out=out)

    def exp(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.exp. This method simply
        wraps the function, and so the docstring for startai.exp also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated exponential function result for
            each element in ``self``. The returned array must have a floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1., 2., 3.])
        >>> print(x.exp())
        startai.array([ 2.71828198,  7.38905573, 20.08553696])
        """
        return startai.exp(self._data, out=out)

    def expm1(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.expm1. This method simply
        wraps the function, and so the docstring for startai.expm1 also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have
            a shape that the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``x``.
            The returned array must have a floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([5.5, -2.5, 1.5, -0])
        >>> y = x.expm1()
        >>> print(y)
        startai.array([244.   ,  -0.918,   3.48 ,   0.   ])

        >>> y = startai.array([0., 0.])
        >>> x = startai.array([5., 0.])
        >>> _ = x.expm1(out=y)
        >>> print(y)
        startai.array([147.,   0.])
        """
        return startai.expm1(self._data, out=out)

    def floor(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.floor. This method simply
        wraps the function, and so the docstring for startai.floor also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rounded result for each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([5.5, -2.5, 1.5, -0])
        >>> y = x.floor()
        >>> print(y)
        startai.array([ 5., -3.,  1.,  0.])
        """
        return startai.floor(self._data, out=out)

    def floor_divide(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.floor_divide. This method
        simply wraps the function, and so the docstring for startai.floor_divide
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array. Should have a real-valued data type.
        x2
            divisor input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x1 = startai.array([13., 7., 8.])
        >>> x2 = startai.array([3., 2., 7.])
        >>> y = x1.floor_divide(x2)
        >>> print(y)
        startai.array([4., 3., 1.])

        With mixed :class:`startai.Array` and :class:`startai.NativeArray` inputs:

        >>> x1 = startai.array([13., 7., 8.])
        >>> x2 = startai.native_array([3., 2., 7.])
        >>> y = x1.floor_divide(x2)
        >>> print(y)
        startai.array([4., 3., 1.])
        """
        return startai.floor_divide(self._data, x2, out=out)

    def fmin(
        self: startai.Array,
        x2: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.fmin. This method simply
        wraps the function, and so the docstring for startai.fmin also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            First input array.
        x2
            Second input array
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Array with element-wise minimums.

        Examples
        --------
        >>> x1 = startai.array([2, 3, 4])
        >>> x2 = startai.array([1, 5, 2])
        >>> startai.fmin(x1, x2)
        startai.array([1, 3, 2])

        >>> x1 = startai.array([startai.nan, 0, startai.nan])
        >>> x2 = startai.array([0, startai.nan, startai.nan])
        >>> x1.fmin(x2)
        startai.array([ 0.,  0., nan])
        """
        return startai.fmin(self._data, x2, out=out)

    def greater(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.greater. This method simply
        wraps the function, and so the docstring for startai.greater also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must
            have a data type of ``bool``.

        Examples
        --------
        >>> x1 = startai.array([2., 5., 15.])
        >>> x2 = startai.array([3., 2., 4.])
        >>> y = x1.greater(x2)
        >>> print(y)
        startai.array([False,  True,  True])
        """
        return startai.greater(self._data, x2, out=out)

    def greater_equal(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.greater_equal. This method
        simply wraps the function, and so the docstring for startai.greater_equal
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x.greater_equal(y)
        >>> print(z)
        startai.array([False,False,False])
        """
        return startai.greater_equal(self._data, x2, out=out)

    def isfinite(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.isfinite. This method
        simply wraps the function, and so the docstring for startai.isfinite also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing test results. An element ``out_i`` is ``True``
            if ``self_i`` is finite and ``False`` otherwise.
            The returned array must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.array([0, startai.nan, -startai.inf, float('inf')])
        >>> y = x.isfinite()
        >>> print(y)
        startai.array([ True, False, False, False])
        """
        return startai.isfinite(self._data, out=out)

    def isinf(
        self: startai.Array,
        *,
        detect_positive: bool = True,
        detect_negative: bool = True,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.isinf. This method simply
        wraps the function, and so the docstring for startai.isinf also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        detect_positive
            if ``True``, positive infinity is detected.
        detect_negative
            if ``True``, negative infinity is detected.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing test results. An element ``out_i`` is ``True``
            if ``self_i`` is either positive or negative infinity and ``False``
            otherwise. The returned array must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x = startai.array([1, 2, 3])
        >>> x.isinf()
        startai.array([False, False, False])

        >>> x = startai.array([[1.1, 2.3, -3.6]])
        >>> x.isinf()
        startai.array([[False, False, False]])

        >>> x = startai.array([[[1.1], [float('inf')], [-6.3]]])
        >>> x.isinf()
        startai.array([[[False],[True],[False]]])

        >>> x = startai.array([[-float('inf'), float('inf'), 0.0]])
        >>> x.isinf()
        startai.array([[ True, True, False]])

        >>> x = startai.zeros((3, 3))
        >>> x.isinf()
        startai.array([[False, False, False],
            [False, False, False],
            [False, False, False]])
        """
        return startai.isinf(
            self._data,
            detect_positive=detect_positive,
            detect_negative=detect_negative,
            out=out,
        )

    def isnan(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.isnan. This method simply
        wraps the function, and so the docstring for startai.isnan also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing test results. An element ``out_i`` is ``True``
            if ``self_i`` is ``NaN`` and ``False`` otherwise.
            The returned array should have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x = startai.array([1, 2, 3])
        >>> x.isnan()
        startai.array([False, False, False])

        >>> x = startai.array([[1.1, 2.3, -3.6]])
        >>> x.isnan()
        startai.array([[False, False, False]])

        >>> x = startai.array([[[1.1], [float('inf')], [-6.3]]])
        >>> x.isnan()
        startai.array([[[False],
                [False],
                [False]]])

        >>> x = startai.array([[-float('nan'), float('nan'), 0.0]])
        >>> x.isnan()
        startai.array([[ True, True, False]])

        >>> x = startai.array([[-float('nan'), float('inf'), float('nan'), 0.0]])
        >>> x.isnan()
        startai.array([[ True, False,  True, False]])

        >>> x = startai.zeros((3, 3))
        >>> x.isnan()
        startai.array([[False, False, False],
            [False, False, False],
            [False, False, False]])
        """
        return startai.isnan(self._data, out=out)

    def less(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.less. This method simply
        wraps the function, and so the docstring for startai.less also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.

        Examples
        --------
        >>> x1 = startai.array([2., 5., 15.])
        >>> x2 = startai.array([3., 2., 4.])
        >>> y = x1.less(x2)
        >>> print(y)
        startai.array([ True, False, False])
        """
        return startai.less(self._data, x2, out=out)

    def less_equal(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.less_equal. This method
        simply wraps the function, and so the docstring for startai.less_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.

        Examples
        --------
        With :code:'startai.Array' inputs:

        >>> x1 = startai.array([1, 2, 3])
        >>> x2 = startai.array([2, 2, 1])
        >>> y = x1.less_equal(x2)
        >>> print(y)
        startai.array([True, True, False])

        With mixed :code:'startai.Array' and :code:'startai.NativeArray' inputs:

        >>> x1 = startai.array([2.5, 3.3, 9.24])
        >>> x2 = startai.native_array([2.5, 1.1, 9.24])
        >>> y = x1.less_equal(x2)
        >>> print(y)
        startai.array([True, False, True])

        With mixed :code:'startai.Container' and :code:'startai.Array' inputs:

        >>> x1 = startai.array([3., 1., 0.8])
        >>> x2 = startai.Container(a=startai.array([2., 1., 0.7]), b=startai.array([3., 0.6, 1.2]))
        >>> y = x1.less_equal(x2)
        >>> print(y)
        {
            a: startai.array([False, True, False]),
            b: startai.array([True, False, True])
        }
        """
        return startai.less_equal(self._data, x2, out=out)

    def log(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.log. This method simply
        wraps the function, and so the docstring for startai.log also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([4.0, 1, -0.0, -5.0])
        >>> y = x.log()
        >>> print(y)
        startai.array([1.39, 0., -inf, nan])

        >>> x = startai.array([float('nan'), -5.0, -0.0, 1.0, 5.0, float('+inf')])
        >>> y = x.log()
        >>> print(y)
        startai.array([nan, nan, -inf, 0., 1.61, inf])

        >>> x = startai.array([[float('nan'), 1, 5.0, float('+inf')],
        ...                [+0, -1.0, -5, float('-inf')]])
        >>> y = x.log()
        >>> print(y)
        startai.array([[nan, 0., 1.61, inf],
                   [-inf, nan, nan, nan]])
        """
        return startai.log(self._data, out=out)

    def log1p(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.log1p. This method simply
        wraps the function, and so the docstring for startai.log1p also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1., 2., 3.])
        >>> y = x.log1p()
        >>> print(y)
        startai.array([0.693, 1.1  , 1.39 ])

        >>> x = startai.array([0.1 , .001 ])
        >>> x.log1p(out = x)
        >>> print(x)
        startai.array([0.0953, 0.001 ])
        """
        return startai.log1p(self._data, out=out)

    def log2(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.log2. This method simply
        wraps the function, and so the docstring for startai.log2 also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated base ``2`` logarithm for each element
            in ``self``. The returned array must have a real-valued floating-point
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        Using :code:`startai.Array` instance method:

        >>> x = startai.array([5.0, 1, -0.0, -6.0])
        >>> y = startai.log2(x)
        >>> print(y)
        startai.array([2.32, 0., -inf, nan])

        >>> x = startai.array([float('nan'), -5.0, -0.0, 1.0, 5.0, float('+inf')])
        >>> y = x.log2()
        >>> print(y)
        startai.array([nan, nan, -inf, 0., 2.32, inf])

        >>> x = startai.array([[float('nan'), 1, 5.0, float('+inf')],\
                            [+0, -2.0, -5, float('-inf')]])
        >>> y = x.log2()
        >>> print(y)
        startai.array([[nan, 0., 2.32, inf],
                   [-inf, nan, nan, nan]])
        """
        return startai.log2(self._data, out=out)

    def log10(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.log10. This method simply
        wraps the function, and so the docstring for startai.log10 also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated base ``10`` logarithm for each element
            in ``self``. The returned array must have a real-valued
            floating-point data type determined by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([4.0, 1, -0.0, -5.0])
        >>> y = x.log10()
        >>> print(y)
        startai.array([0.602, 0., -inf, nan])

        >>> x = startai.array([float('nan'), -5.0, -0.0, 1.0, 5.0, float('+inf')])
        >>> y = x.log10()
        >>> print(y)
        startai.array([nan, nan, -inf, 0., 0.699, inf])

        >>> x = startai.array([[float('nan'), 1, 5.0, float('+inf')],
        ...                [+0, -1.0, -5, float('-inf')]])
        >>> y = x.log10()
        >>> print(y)
        startai.array([[nan, 0., 0.699, inf],
                   [-inf, nan, nan, nan]])
        """
        return startai.log10(self._data, out=out)

    def logaddexp(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.logaddexp. This method
        simply wraps the function, and so the docstring for startai.logaddexp also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a real-valued floating-point data
            type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([2., 5., 15.])
        >>> y = startai.array([3., 2., 4.])
        >>> z = x.logaddexp(y)
        >>> print(z)
        startai.array([ 3.31,  5.05, 15.  ])
        """
        return startai.logaddexp(self._data, x2, out=out)

    def logaddexp2(
        self: Union[startai.Array, float, list, tuple],
        x2: Union[startai.Array, float, list, tuple],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.logaddexp2. This method
        simply wraps the function, and so the docstring for startai.logaddexp2 also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            First array-like input.
        x2
            Second array-like input
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Element-wise logaddexp2 of x1 and x2.

        Examples
        --------
        >>> x1 = startai.array([1, 2, 3])
        >>> x2 = startai.array([4, 5, 6])
        >>> x1.logaddexp2(x2)
        startai.array([4.169925, 5.169925, 6.169925])
        """
        return startai.logaddexp2(self._data, x2, out=out)

    def logical_and(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.logical_and. This method
        simply wraps the function, and so the docstring for startai.logical_and
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.

        Examples
        --------
        Using 'startai.Array' instance:

        >>> x = startai.array([True, False, True, False])
        >>> y = startai.array([True, True, False, False])
        >>> z = x.logical_and(y)
        >>> print(z)
        startai.array([True, False, False, False])
        """
        return startai.logical_and(self._data, x2, out=out)

    def logical_not(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.logical_not. This method
        simply wraps the function, and so the docstring for startai.logical_not
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a boolean data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x=startai.array([0,1,1,0])
        >>> x.logical_not()
        startai.array([ True, False, False,  True])

        >>> x=startai.array([2,0,3,9])
        >>> x.logical_not()
        startai.array([False,  True, False, False])
        """
        return startai.logical_not(self._data, out=out)

    def logical_or(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.logical_or. This method
        simply wraps the function, and so the docstring for startai.logical_or also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.

        This function conforms to the `Array API Standard
        <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of
        the `docstring <https://data-apis.org/array-api/latest/
        API_specification/generated/array_api.logical_or.html>`_
        in the standard.

        Both the description and the type hints above assumes an array input for
        simplicity, but this function is *nestable*, and therefore also
        accepts :class:`startai.Container` instances in place of any of the arguments.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([False, 3, 0])
        >>> y = startai.array([2, True, False])
        >>> z = x.logical_or(y)
        >>> print(z)
        startai.array([ True,  True, False])
        """
        return startai.logical_or(self._data, x2, out=out)

    def logical_xor(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.logical_xor. This method
        simply wraps the function, and so the docstring for startai.logical_xor
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.array([True, False, True, False])
        >>> y = startai.array([True, True, False, False])
        >>> z = x.logical_xor(y)
        >>> print(z)
        startai.array([False,  True,  True, False])
        """
        return startai.logical_xor(self._data, x2, out=out)

    def multiply(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.multiply. This method
        simply wraps the function, and so the docstring for startai.multiply also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with the first input array.
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise products.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :code:`startai.Array` inputs:

        >>> x1 = startai.array([3., 5., 7.])
        >>> x2 = startai.array([4., 6., 8.])
        >>> y = x1.multiply(x2)
        >>> print(y)
        startai.array([12., 30., 56.])

        With mixed :code:`startai.Array` and `startai.NativeArray` inputs:

        >>> x1 = startai.array([8., 6., 7.])
        >>> x2 = startai.native_array([1., 2., 3.])
        >>> y = x1.multiply(x2)
        >>> print(y)
        startai.array([ 8., 12., 21.])
        """
        return startai.multiply(self._data, x2, out=out)

    def maximum(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        use_where: bool = True,
        out: Optional[startai.Array] = None,
    ):
        """startai.Array instance method variant of startai.maximum. This method simply
        wraps the function, and so the docstring for startai.maximum also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            Input array containing elements to maximum threshold.
        x2
            Tensor containing maximum values, must be broadcastable to x1.
        use_where
            Whether to use :func:`where` to calculate the maximum. If ``False``, the
            maximum is calculated using the ``(x + y + |x - y|)/2`` formula. Default is
            ``True``.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            An array with the elements of x1, but clipped to not be lower than the x2
            values.

        Examples
        --------
        With :class:`startai.Array` inputs:
        >>> x = startai.array([7, 9, 5])
        >>> y = startai.array([9, 3, 2])
        >>> z = x.maximum(y)
        >>> print(z)
        startai.array([9, 9, 5])

        >>> x = startai.array([1, 5, 9, 8, 3, 7])
        >>> y = startai.array([[9], [3], [2]])
        >>> z = startai.zeros((3, 6))
        >>> x.maximum(y, out=z)
        >>> print(z)
        startai.array([[9.,9.,9.,9.,9.,9.],
                   [3.,5.,9.,8.,3.,7.],
                   [2.,5.,9.,8.,3.,7.]])

        >>> x = startai.array([[7, 3]])
        >>> y = startai.array([0, 7])
        >>> x.maximum(y, out=x)
        >>> print(x)
        startai.array([[7, 7]])
        """
        return startai.maximum(self, x2, use_where=use_where, out=out)

    def minimum(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        use_where: bool = True,
        out: Optional[startai.Array] = None,
    ):
        """startai.Array instance method variant of startai.minimum. This method simply
        wraps the function, and so the docstring for startai.minimum also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            Input array containing elements to minimum threshold.
        x2
            Tensor containing minimum values, must be broadcastable to x1.
        use_where
            Whether to use :func:`where` to calculate the minimum. If ``False``, the
            minimum is calculated using the ``(x + y - |x - y|)/2`` formula. Default is
            ``True``.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            An array with the elements of x1, but clipped to not exceed the x2 values.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x = startai.array([7, 9, 5])
        >>> y = startai.array([9, 3, 2])
        >>> z = x.minimum(y)
        >>> print(z)
        startai.array([7, 3, 2])

        >>> x = startai.array([1, 5, 9, 8, 3, 7])
        >>> y = startai.array([[9], [3], [2]])
        >>> z = startai.zeros((3, 6))
        >>> x.minimum(y, out=z)
        >>> print(z)
        startai.array([[1.,5.,9.,8.,3.,7.],
                   [1.,3.,3.,3.,3.,3.],
                   [1.,2.,2.,2.,2.,2.]])

        >>> x = startai.array([[7, 3]])
        >>> y = startai.array([0, 7])
        >>> x.minimum(y, out=x)
        >>> print(x)
        startai.array([[0, 3]])
        """
        return startai.minimum(self, x2, use_where=use_where, out=out)

    def negative(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.negative. This method
        simply wraps the function, and so the docstring for startai.negative also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x = startai.array([2, 3 ,5, 7])
        >>> y = x.negative()
        >>> print(y)
        startai.array([-2, -3, -5, -7])

        >>> x = startai.array([0,-1,-0.5,2,3])
        >>> y = startai.zeros(5)
        >>> x.negative(out=y)
        >>> print(y)
        startai.array([-0. ,  1. ,  0.5, -2. , -3. ])

        >>> x = startai.array([[1.1, 2.2, 3.3],
        ...                [-4.4, -5.5, -6.6]])
        >>> x.negative(out=x)
        >>> print(x)
        startai.array([[ -1.1, -2.2, -3.3],
        [4.4, 5.5, 6.6]])
        """
        return startai.negative(self._data, out=out)

    def not_equal(
        self: startai.Array,
        x2: Union[float, startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.not_equal. This method
        simply wraps the function, and so the docstring for startai.not_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned
            array must have a data type of ``bool``.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x1 = startai.array([2., 7., 9.])
        >>> x2 = startai.array([1., 7., 9.])
        >>> y = x1.not_equal(x2)
        >>> print(y)
        startai.array([True, False, False])

        With mixed :class:`startai.Array` and :class:`startai.NativeArray` inputs:

        >>> x1 = startai.array([2.5, 7.3, 9.375])
        >>> x2 = startai.native_array([2.5, 2.9, 9.375])
        >>> y = x1.not_equal(x2)
        >>> print(y)
        startai.array([False, True,  False])

        With mixed :class:`startai.Array` and `float` inputs:

        >>> x1 = startai.array([2.5, 7.3, 9.375])
        >>> x2 = 7.3
        >>> y = x1.not_equal(x2)
        >>> print(y)
        startai.array([True, False, True])

        With mixed :class:`startai.Container` and :class:`startai.Array` inputs:

        >>> x1 = startai.array([3., 1., 0.9])
        >>> x2 = startai.Container(a=startai.array([12., 3.5, 6.3]), b=startai.array([3., 1., 0.9]))
        >>> y = x1.not_equal(x2)
        >>> print(y)
        {
            a: startai.array([True, True, True]),
            b: startai.array([False, False, False])
        }
        """
        return startai.not_equal(self._data, x2, out=out)

    def positive(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.positive. This method
        simply wraps the function, and so the docstring for startai.positive also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x = startai.array([2, 3 ,5, 7])
        >>> y = x.positive()
        >>> print(y)
        startai.array([2, 3, 5, 7])

        >>> x = startai.array([0, -1, -0.5, 2, 3])
        >>> y = startai.zeros(5)
        >>> x.positive(out=y)
        >>> print(y)
        startai.array([0., -1., -0.5,  2.,  3.])

        >>> x = startai.array([[1.1, 2.2, 3.3],
        ...                [-4.4, -5.5, -6.6]])
        >>> x.positive(out=x)
        >>> print(x)
        startai.array([[ 1.1,  2.2,  3.3],
        [-4.4, -5.5, -6.6]])
        """
        return startai.positive(self._data, out=out)

    def pow(
        self: startai.Array,
        x2: Union[int, float, startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.pow. This method simply
        wraps the function, and so the docstring for startai.pow also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array whose elements correspond to the exponentiation base.
            Should have a real-valued data type.
        x2
            second input array whose elements correspond to the exponentiation
            exponent. Must be compatible with ``self`` (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x = startai.array([1, 2, 3])
        >>> y = x.pow(3)
        >>> print(y)
        startai.array([1, 8, 27])

        >>> x = startai.array([1.5, -0.8, 0.3])
        >>> y = startai.zeros(3)
        >>> x.pow(2, out=y)
        >>> print(y)
        startai.array([2.25, 0.64, 0.09])
        """
        return startai.pow(self._data, x2, out=out)

    def real(self: startai.Array, /, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.real. This method simply
        wraps the function, and so the docstring for startai.real also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to.
            It must have a shape that the inputs broadcast to.

        Returns
        -------
        ret
            an array containing test results. If input in an
            array is real then, it is returned unchanged. on the
            other hand, if it is complex then, it returns real part from it

        Examples
        --------
        >>> x = startai.array([4+3j, 6+2j, 1-6j])
        >>> x.real()
        startai.array([4., 6., 1.])
        """
        return startai.real(self._data, out=out)

    def remainder(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        modulus: bool = True,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.remainder. This method
        simply wraps the function, and so the docstring for startai.remainder also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array. Should have a real-valued data type.
        x2
            divisor input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        modulus
            whether to compute the modulus instead of the remainder.
            Default is ``True``.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            Each element-wise result must have the same sign as the respective
            element ``x2_i``. The returned array must have a data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x1 = startai.array([2., 5., 15.])
        >>> x2 = startai.array([3., 2., 4.])
        >>> y = x1.remainder(x2)
        >>> print(y)
        startai.array([2., 1., 3.])

        With mixed :class:`startai.Array` and :class:`startai.NativeArray` inputs:

        >>> x1 = startai.array([11., 4., 18.])
        >>> x2 = startai.native_array([2., 5., 8.])
        >>> y = x1.remainder(x2)
        >>> print(y)
        startai.array([1., 4., 2.])
        """
        return startai.remainder(self._data, x2, modulus=modulus, out=out)

    def round(
        self: startai.Array, *, decimals: int = 0, out: Optional[startai.Array] = None
    ) -> startai.Array:
        """startai.Array instance method variant of startai.round. This method simply
        wraps the function, and so the docstring for startai.round also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        decimals
            number of decimal places to round to. Default is ``0``.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rounded result for each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([6.3, -8.1, 0.5, -4.2, 6.8])
        >>> y = x.round()
        >>> print(y)
        startai.array([ 6., -8.,  0., -4.,  7.])

        >>> x = startai.array([-94.2, 256.0, 0.0001, -5.5, 36.6])
        >>> y = x.round()
        >>> print(y)
        startai.array([-94., 256., 0., -6., 37.])

        >>> x = startai.array([0.23, 3., -1.2])
        >>> y = startai.zeros(3)
        >>> x.round(out=y)
        >>> print(y)
        startai.array([ 0.,  3., -1.])

        >>> x = startai.array([[ -1., -67.,  0.,  15.5,  1.], [3, -45, 24.7, -678.5, 32.8]])
        >>> y = x.round()
        >>> print(y)
        startai.array([[-1., -67., 0., 16., 1.],
        [3., -45., 25., -678., 33.]])
        """
        return startai.round(self._data, decimals=decimals, out=out)

    def sign(
        self: startai.Array,
        *,
        np_variant: Optional[bool] = True,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.sign. This method simply
        wraps the function, and so the docstring for startai.sign also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = startai.array([5.7, -7.1, 0, -0, 6.8])
        >>> y = x.sign()
        >>> print(y)
        startai.array([ 1., -1.,  0.,  0.,  1.])

        >>> x = startai.array([-94.2, 256.0, 0.0001, -0.0001, 36.6])
        >>> y = x.sign()
        >>> print(y)
        startai.array([-1.,  1.,  1., -1.,  1.])

        >>> x = startai.array([[ -1., -67.,  0.,  15.5,  1.], [3, -45, 24.7, -678.5, 32.8]])
        >>> y = x.sign()
        >>> print(y)
        startai.array([[-1., -1.,  0.,  1.,  1.],
        [ 1., -1.,  1., -1.,  1.]])
        """
        return startai.sign(self._data, np_variant=np_variant, out=out)

    def sin(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.sin. This method simply
        wraps the function, and so the docstring for startai.sin also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements are each expressed in radians. Should have a
            floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the sine of each element in ``self``. The returned
            array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([0., 1., 2., 3.])
        >>> y = x.sin()
        >>> print(y)
        startai.array([0., 0.841, 0.909, 0.141])
        """
        return startai.sin(self._data, out=out)

    def sinh(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.sinh. This method simply
        wraps the function, and so the docstring for startai.sinh also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent a hyperbolic angle.
            Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the hyperbolic sine of each element in ``self``. The
            returned array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1., 2., 3.])
        >>> print(x.sinh())
            startai.array([1.18, 3.63, 10.])

        >>> x = startai.array([0.23, 3., -1.2])
        >>> y = startai.zeros(3)
        >>> print(x.sinh(out=y))
            startai.array([0.232, 10., -1.51])
        """
        return startai.sinh(self._data, out=out)

    def square(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.square. This method simply
        wraps the function, and so the docstring for startai.square also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the square of each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` instance method:

        >>> x = startai.array([1, 2, 3])
        >>> y = x.square()
        >>> print(y)
        startai.array([1, 4, 9])

        >>> x = startai.array([[1.2, 2, 3.1], [-1, -2.5, -9]])
        >>> x.square(out=x)
        >>> print(x)
        startai.array([[1.44,4.,9.61],[1.,6.25,81.]])
        """
        return startai.square(self._data, out=out)

    def sqrt(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.sqrt. This method simply
        wraps the function, and so the docstring for startai.sqrt also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the square root of each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        Using :class:`startai.Array` instance method:

        >>> x = startai.array([[1., 2.],  [3., 4.]])
        >>> y = x.sqrt()
        >>> print(y)
        startai.array([[1.  , 1.41],
                   [1.73, 2.  ]])
        """
        return startai.sqrt(self._data, out=out)

    def subtract(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        alpha: Optional[Union[int, float]] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.subtract. This method
        simply wraps the function, and so the docstring for startai.subtract also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        alpha
            optional scalar multiplier for ``x2``.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise differences. The returned array
            must have a data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([5, 2, 3])
        >>> y = startai.array([1, 2, 6])
        >>> z = x.subtract(y)
        >>> print(z)
        startai.array([4, 0, -3])

        >>> x = startai.array([5., 5, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x.subtract(y, alpha=2)
        >>> print(z)
        startai.array([-3., -5., -9.])
        """
        return startai.subtract(self._data, x2, alpha=alpha, out=out)

    def trapz(
        self: startai.Array,
        /,
        *,
        x: Optional[startai.Array] = None,
        dx: float = 1.0,
        axis: int = -1,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.trapz. This method simply
        wraps the function, and so the docstring for startai.trapz also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            The array that should be integrated.
        x
            The sample points corresponding to the input array values.
            If x is None, the sample points are assumed to be evenly spaced
            dx apart. The default is None.
        dx
            The spacing between sample points when x is None. The default is 1.
        axis
            The axis along which to integrate.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Definite integral of n-dimensional array as approximated along
            a single axis by the trapezoidal rule. If the input array is a
            1-dimensional array, then the result is a float. If n is greater
            than 1, then the result is an n-1 dimensional array.

        Examples
        --------
        >>> y = startai.array([1, 2, 3])
        >>> startai.trapz(y)
        4.0
        >>> y = startai.array([1, 2, 3])
        >>> x = startai.array([4, 6, 8])
        >>> startai.trapz(y, x=x)
        8.0
        >>> y = startai.array([1, 2, 3])
        >>> startai.trapz(y, dx=2)
        8.0
        """
        return startai.trapz(self._data, x=x, dx=dx, axis=axis, out=out)

    def tan(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.tan. This method simply
        wraps the function, and so the docstring for startai.tan also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements are expressed in radians. Should have a
            floating-point data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the tangent of each element in ``self``.
            The return must have a floating-point data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([0., 1., 2.])
        >>> y = x.tan()
        >>> print(y)
        startai.array([0., 1.56, -2.19])
        """
        return startai.tan(self._data, out=out)

    def tanh(
        self: startai.Array,
        *,
        complex_mode: Literal["split", "magnitude", "jax"] = "jax",
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.tanh. This method simply
        wraps the function, and so the docstring for startai.tanh also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent a hyperbolic angle.
            Should have a real-valued floating-point data type.
        complex_mode
            optional specifier for how to handle complex data types. See
            ``startai.func_wrapper.handle_complex_input`` for more detail.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the hyperbolic tangent of each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([0., 1., 2.])
        >>> y = x.tanh()
        >>> print(y)
        startai.array([0., 0.762, 0.964])
        """
        return startai.tanh(self._data, complex_mode=complex_mode, out=out)

    def trunc(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.trunc. This method simply
        wraps the function, and so the docstring for startai.trunc also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rounded result for each element in ``self``.
            The returned array must have the same data type as ``self``

        Examples
        --------
        >>> x = startai.array([-1, 0.54, 3.67, -0.025])
        >>> y = x.trunc()
        >>> print(y)
        startai.array([-1.,  0.,  3., -0.])
        """
        return startai.trunc(self._data, out=out)

    def erf(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.erf. This method simply
        wraps the function, and so the docstring for startai.erf also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array to compute exponential for.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the Gauss error of ``self``.

        Examples
        --------
        >>> x = startai.array([0, 0.3, 0.7, 1.0])
        >>> x.erf()
        startai.array([0., 0.328, 0.677, 0.842])
        """
        return startai.erf(self._data, out=out)

    def exp2(
        self: Union[startai.Array, float, list, tuple],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.exp2. This method simply
        wraps the function, and so the docstring for startai.exp2 also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Array-like input.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Element-wise 2 to the power x. This is a scalar if x is a scalar.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> x.exp2()
        startai.array([2.,    4.,   8.])
        >>> x = [5, 6, 7]
        >>> x.exp2()
        startai.array([32.,   64.,  128.])
        """
        return startai.exp2(self._data, out=out)

    def gcd(
        self: Union[startai.Array, int, list, tuple],
        x2: Union[startai.Array, int, list, tuple],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.gcd. This method simply
        wraps the function, and so the docstring for startai.gcd also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            First array-like input.
        x2
            Second array-like input
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Element-wise gcd of |x1| and |x2|.

        Examples
        --------
        >>> x1 = startai.array([1, 2, 3])
        >>> x2 = startai.array([4, 5, 6])
        >>> x1.gcd(x2)
        startai.array([1.,    1.,   3.])
        >>> x1 = startai.array([1, 2, 3])
        >>> x1.gcd(10)
        startai.array([1.,   2.,  1.])
        """
        return startai.gcd(self._data, x2, out=out)

    def nan_to_num(
        self: startai.Array,
        /,
        *,
        copy: bool = True,
        nan: Union[float, int] = 0.0,
        posinf: Optional[Union[float, int]] = None,
        neginf: Optional[Union[float, int]] = None,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.nan_to_num. This method
        simply wraps the function, and so the docstring for startai.nan_to_num also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            Array input.
        copy
            Whether to create a copy of x (True) or to replace values in-place (False).
            The in-place operation only occurs if casting to an array does not require
            a copy. Default is True.
        nan
            Value to be used to fill NaN values. If no value is passed then NaN values
            will be replaced with 0.0.
        posinf
            Value to be used to fill positive infinity values. If no value is passed
            then positive infinity values will be replaced with a very large number.
        neginf
            Value to be used to fill negative infinity values.
            If no value is passed then negative infinity values
            will be replaced with a very small (or negative) number.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Array with the non-finite values replaced.
            If copy is False, this may be x itself.

        Examples
        --------
        >>> x = startai.array([1, 2, 3, nan])
        >>> x.nan_to_num()
        startai.array([1.,    1.,   3.,   0.0])
        >>> x = startai.array([1, 2, 3, inf])
        >>> x.nan_to_num(posinf=5e+100)
        startai.array([1.,   2.,   3.,   5e+100])
        """
        return startai.nan_to_num(
            self._data, copy=copy, nan=nan, posinf=posinf, neginf=neginf, out=out
        )

    def angle(
        self: startai.Array,
        /,
        *,
        deg: bool = False,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.angle. This method simply
        wraps the function, and so the docstring for startai.angle also applies to
        this method with minimal changes.

        Parameters
        ----------
        z
            Array-like input.
        deg
            optional bool.
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            Returns an array of angles for each complex number in the input.
            If def is False(default), angle is calculated in radian and if
            def is True, then angle is calculated in degrees.

        Examples
        --------
        >>> startai.set_backend('tensorflow')
        >>> z = startai.array([-1 + 1j, -2 + 2j, 3 - 3j])
        >>> z
        startai.array([-1.+1.j, -2.+2.j,  3.-3.j])
        >>> startai.angle(z)
        startai.array([ 2.35619449,  2.35619449, -0.78539816])
        >>> startai.set_backend('numpy')
        >>> startai.angle(z,deg=True)
        startai.array([135., 135., -45.])
        """
        return startai.angle(self._data, deg=deg, out=out)

    def reciprocal(
        self: startai.Array,
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.reciprocal.This method
        simply wraps the function, and so the docstring for startai.reciprocal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array to compute the element-wise reciprocal for.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise reciprocal of ``self``.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = x.reciprocal()
        >>> print(y)
        startai.array([1., 0.5, 0.333])
        """
        return startai.reciprocal(self._data, out=out)

    def deg2rad(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.deg2rad. This method simply
        wraps the function, and so the docstring for startai.deg2rad also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array. to be converted from degrees to radians.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise conversion from degrees to radians.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x=startai.array([90,180,270,360])
        >>> y=x.deg2rad()
        >>> print(y)
        startai.array([1.57, 3.14, 4.71, 6.28])
        """
        return startai.deg2rad(self._data, out=out)

    def rad2deg(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.rad2deg. This method simply
        wraps the function, and so the docstring for startai.rad2deg also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array. to be converted from degrees to radians.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise conversion from radians to degrees.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x=startai.array([1., 5., 8., 10.])
        >>> y=x.rad2deg()
        >>> print(y)
        startai.array([ 57.3, 286. , 458. , 573. ])
        """
        return startai.rad2deg(self._data, out=out)

    def trunc_divide(
        self: startai.Array,
        x2: Union[startai.Array, startai.NativeArray],
        /,
        *,
        out: Optional[startai.Array] = None,
    ) -> startai.Array:
        """startai.Array instance method variant of startai.trunc_divide. This method
        simply wraps the function, and so the docstring for startai.trunc_divide
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array. Should have a real-valued data type.
        x2
            divisor input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> x1 = startai.array([2., 7., 9.])
        >>> x2 = startai.array([2., -2., 2.])
        >>> y = x1.trunc_divide(x2)
        >>> print(y)
        startai.array([ 1., -3.,  4.])
        """
        return startai.trunc_divide(self._data, x2, out=out)

    def isreal(self: startai.Array, *, out: Optional[startai.Array] = None) -> startai.Array:
        """startai.Array instance method variant of startai.isreal. This method simply
        wraps the function, and so the docstring for startai.isreal also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing test results. An element ``out_i`` is ``True``
            if ``self_i`` is real number and ``False`` otherwise.
            The returned array should have a data type of ``bool``.

        Examples
        --------
        >>> x = startai.array([1j, 2+5j, 3.7-6j])
        >>> x.isreal()
        startai.array([False, False, False])
        """
        return startai.isreal(self._data, out=out)

    def lcm(
        self: startai.Array, x2: startai.Array, *, out: Optional[startai.Array] = None
    ) -> startai.Array:
        """startai.Array instance method variant of startai.lcm. This method simply
        wraps the function, and so the docstring for startai.lcm also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array.
        x2
            second input array
        out
            optional output array, for writing the result to.

        Returns
        -------
        ret
            an array that includes the element-wise least common multiples
            of 'self' and x2

        Examples
        --------
        >>> x1=startai.array([2, 3, 4])
        >>> x2=startai.array([5, 8, 15])
        >>> x1.lcm(x2)
        startai.array([10, 21, 60])
        """
        return startai.lcm(self, x2, out=out)
