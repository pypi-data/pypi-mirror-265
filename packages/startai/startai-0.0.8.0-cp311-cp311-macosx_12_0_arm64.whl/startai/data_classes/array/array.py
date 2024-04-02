# flake8: noqa
# global
import copy
import numpy as np
from typing import Optional

# local
import startai
from .conversions import args_to_native, to_startai
from .activations import _ArrayWithActivations
from .creation import _ArrayWithCreation
from .data_type import _ArrayWithDataTypes
from .device import _ArrayWithDevice
from .elementwise import _ArrayWithElementwise
from .general import _ArrayWithGeneral
from .gradients import _ArrayWithGradients
from .image import _ArrayWithImage
from .layers import _ArrayWithLayers
from .linear_algebra import _ArrayWithLinearAlgebra
from .losses import _ArrayWithLosses
from .manipulation import _ArrayWithManipulation
from .norms import _ArrayWithNorms
from .random import _ArrayWithRandom
from .searching import _ArrayWithSearching
from .set import _ArrayWithSet
from .sorting import _ArrayWithSorting
from .statistical import _ArrayWithStatistical
from .utility import _ArrayWithUtility
from startai.func_wrapper import handle_view_indexing
from .experimental import (
    _ArrayWithSearchingExperimental,
    _ArrayWithActivationsExperimental,
    _ArrayWithConversionsExperimental,
    _ArrayWithCreationExperimental,
    _ArrayWithData_typeExperimental,
    _ArrayWithDeviceExperimental,
    _ArrayWithElementWiseExperimental,
    _ArrayWithGeneralExperimental,
    _ArrayWithGradientsExperimental,
    _ArrayWithImageExperimental,
    _ArrayWithLayersExperimental,
    _ArrayWithLinearAlgebraExperimental,
    _ArrayWithLossesExperimental,
    _ArrayWithManipulationExperimental,
    _ArrayWithNormsExperimental,
    _ArrayWithRandomExperimental,
    _ArrayWithSetExperimental,
    _ArrayWithSortingExperimental,
    _ArrayWithStatisticalExperimental,
    _ArrayWithUtilityExperimental,
)


class Array(
    _ArrayWithActivations,
    _ArrayWithCreation,
    _ArrayWithDataTypes,
    _ArrayWithDevice,
    _ArrayWithElementwise,
    _ArrayWithGeneral,
    _ArrayWithGradients,
    _ArrayWithImage,
    _ArrayWithLayers,
    _ArrayWithLinearAlgebra,
    _ArrayWithLosses,
    _ArrayWithManipulation,
    _ArrayWithNorms,
    _ArrayWithRandom,
    _ArrayWithSearching,
    _ArrayWithSet,
    _ArrayWithSorting,
    _ArrayWithStatistical,
    _ArrayWithUtility,
    _ArrayWithActivationsExperimental,
    _ArrayWithConversionsExperimental,
    _ArrayWithCreationExperimental,
    _ArrayWithData_typeExperimental,
    _ArrayWithDeviceExperimental,
    _ArrayWithElementWiseExperimental,
    _ArrayWithGeneralExperimental,
    _ArrayWithGradientsExperimental,
    _ArrayWithImageExperimental,
    _ArrayWithLayersExperimental,
    _ArrayWithLinearAlgebraExperimental,
    _ArrayWithLossesExperimental,
    _ArrayWithManipulationExperimental,
    _ArrayWithNormsExperimental,
    _ArrayWithRandomExperimental,
    _ArrayWithSearchingExperimental,
    _ArrayWithSetExperimental,
    _ArrayWithSortingExperimental,
    _ArrayWithStatisticalExperimental,
    _ArrayWithUtilityExperimental,
):
    def __init__(self, data, dynamic_backend=None):
        _ArrayWithActivations.__init__(self)
        _ArrayWithCreation.__init__(self)
        _ArrayWithDataTypes.__init__(self)
        _ArrayWithDevice.__init__(self)
        _ArrayWithElementwise.__init__(self)
        _ArrayWithGeneral.__init__(self)
        _ArrayWithGradients.__init__(self)
        _ArrayWithImage.__init__(self)
        _ArrayWithLayers.__init__(self)
        _ArrayWithLinearAlgebra.__init__(self)
        _ArrayWithLosses.__init__(self)
        _ArrayWithManipulation.__init__(self)
        _ArrayWithNorms.__init__(self)
        _ArrayWithRandom.__init__(self)
        _ArrayWithSearching.__init__(self)
        _ArrayWithSet.__init__(self)
        _ArrayWithSorting.__init__(self)
        _ArrayWithStatistical.__init__(self)
        _ArrayWithUtility.__init__(self)
        _ArrayWithActivationsExperimental.__init__(self),
        _ArrayWithConversionsExperimental.__init__(self),
        _ArrayWithCreationExperimental.__init__(self),
        _ArrayWithData_typeExperimental.__init__(self),
        _ArrayWithDeviceExperimental.__init__(self),
        _ArrayWithElementWiseExperimental.__init__(self),
        _ArrayWithGeneralExperimental.__init__(self),
        _ArrayWithGradientsExperimental.__init__(self),
        _ArrayWithImageExperimental.__init__(self),
        _ArrayWithLayersExperimental.__init__(self),
        _ArrayWithLinearAlgebraExperimental.__init__(self),
        _ArrayWithLossesExperimental.__init__(self),
        _ArrayWithManipulationExperimental.__init__(self),
        _ArrayWithNormsExperimental.__init__(self),
        _ArrayWithRandomExperimental.__init__(self),
        _ArrayWithSearchingExperimental.__init__(self),
        _ArrayWithSetExperimental.__init__(self),
        _ArrayWithSortingExperimental.__init__(self),
        _ArrayWithStatisticalExperimental.__init__(self),
        _ArrayWithUtilityExperimental.__init__(self),
        self._init(data, dynamic_backend)
        self._view_attributes(data)

    def _init(self, data, dynamic_backend=None):
        if startai.is_startai_array(data):
            self._data = data.data
        elif startai.is_native_array(data):
            self._data = data
        elif isinstance(data, np.ndarray):
            self._data = startai.asarray(data)._data
        elif isinstance(data, (list, tuple)):
            self._data = startai.asarray(data)._data
        elif startai.is_startai_sparse_array(data):
            self._data = data._data
        elif startai.is_native_sparse_array(data):
            self._data = data._data
        else:
            raise startai.utils.exceptions.StartaiException(
                "data must be startai array, native array or ndarray"
            )
        self._size = None
        self._strides = None
        self._itemsize = None
        self._dtype = None
        self._device = None
        self._dev_str = None
        self._pre_repr = None
        self._post_repr = None
        self._backend = startai.current_backend(self._data).backend
        if dynamic_backend is not None:
            self._dynamic_backend = dynamic_backend
        else:
            self._dynamic_backend = startai.dynamic_backend
        self.weak_type = False  # to handle 0-D jax front weak typed arrays

    def _view_attributes(self, data):
        self._base = None
        self._view_refs = []
        self._manipulation_stack = []
        self._torch_base = None
        self._torch_view_refs = []
        self._torch_manipulation = None

    # Properties #
    # ---------- #

    @property
    def backend(self):
        return self._backend

    @property
    def dynamic_backend(self):
        return self._dynamic_backend

    @dynamic_backend.setter
    def dynamic_backend(self, value):
        from startai.functional.startai.gradients import _variable
        from startai.utils.backend.handler import _data_to_new_backend, _get_backend_for_arg

        if value:
            startai_backend = startai.with_backend(self._backend)

            if startai_backend.gradients._is_variable(self.data):
                native_var = startai_backend.gradients._variable_data(
                    self,
                )
                data = _data_to_new_backend(native_var, startai_backend).data
                self._data = _variable(data).data

            else:
                self._data = _data_to_new_backend(self, startai_backend).data

            self._backend = startai.backend

        else:
            self._backend = _get_backend_for_arg(self.data.__class__.__module__).backend

        self._dynamic_backend = value

    @property
    def data(self) -> startai.NativeArray:
        """The native array being wrapped in self."""
        return self._data

    @property
    def dtype(self) -> startai.Dtype:
        """Data type of the array elements."""
        if self._dtype is None:
            self._dtype = startai.dtype(self._data)
        return self._dtype

    @property
    def device(self) -> startai.Device:
        """Hardware device the array data resides on."""
        if self._device is None:
            self._device = startai.dev(self._data)
        return self._device

    @property
    def mT(self) -> startai.Array:
        """Transpose of a matrix (or a stack of matrices).

        Returns
        -------
        ret
            array whose last two dimensions (axes) are permuted in reverse order
            relative to original array (i.e., for an array instance having shape
            ``(..., M, N)``, the returned array must have shape ``(..., N, M)``).
            The returned array must have the same data type as the original array.
        """
        startai.utils.assertions.check_greater(
            len(self._data.shape), 2, allow_equal=True, as_array=False
        )
        return startai.matrix_transpose(self._data)

    @property
    def ndim(self) -> int:
        """Number of array dimensions (axes)."""
        return len(tuple(self._data.shape))

    @property
    def shape(self) -> startai.Shape:
        """Array dimensions."""
        return startai.Shape(self._data.shape)

    @property
    def size(self) -> Optional[int]:
        """Number of elements in the array."""
        return startai.size(self)

    @property
    def itemsize(self) -> Optional[int]:
        """Size of array elements in bytes."""
        if self._itemsize is None:
            self._itemsize = startai.itemsize(self._data)
        return self._itemsize

    @property
    def strides(self) -> Optional[int]:
        """Get strides across each dimension."""
        if self._strides is None:
            # for this to work consistently for non-contiguous arrays
            # we must pass self to startai.strides, not self.data
            self._strides = startai.strides(self)
        return self._strides

    @property
    def T(self) -> startai.Array:
        """Transpose of the array.

        Returns
        -------
        ret
            two-dimensional array whose first and last dimensions (axes) are
            permuted in reverse order relative to original array.
        """
        startai.utils.assertions.check_equal(len(self._data.shape), 2, as_array=False)
        return startai.matrix_transpose(self._data)

    @property
    def base(self) -> startai.Array:
        """Original array referenced by view."""
        return self._base

    @property
    def real(self) -> startai.Array:
        """Real part of the array.

        Returns
        -------
        ret
            array containing the real part of each element in the array.
            The returned array must have the same shape and data type as
            the original array.
        """
        return startai.real(self._data)

    @property
    def imag(self) -> startai.Array:
        """Imaginary part of the array.

        Returns
        -------
        ret
            array containing the imaginary part of each element in the array.
            The returned array must have the same shape and data type as
            the original array.
        """
        return startai.imag(self._data)

    # Setters #
    # --------#

    @data.setter
    def data(self, data):
        startai.utils.assertions.check_true(
            startai.is_native_array(data), "data must be native array"
        )
        self._init(data)

    # Built-ins #
    # ----------#

    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs={}):
        args, kwargs = args_to_native(*args, **kwargs)
        return to_startai(func(*args, **kwargs))

    def __startai_array_function__(self, func, types, args, kwargs):
        # Cannot handle items that have __startai_array_function__ other than those of
        # startai arrays or native arrays.
        for t in types:
            if (
                hasattr(t, "__startai_array_function__")
                and (t.__startai_array_function__ is not startai.Array.__startai_array_function__)
                or (
                    hasattr(startai.NativeArray, "__startai_array_function__")
                    and (
                        t.__startai_array_function__
                        is not startai.NativeArray.__startai_array_function__
                    )
                )
            ):
                return NotImplemented

        # Arguments contain no overrides, so we can safely call the
        # overloaded function again.
        return func(*args, **kwargs)

    def __array__(self, *args, **kwargs):
        args, kwargs = args_to_native(*args, **kwargs)
        return self._data.__array__(*args, dtype=self.dtype, **kwargs)

    def __array_prepare__(self, *args, **kwargs):
        args, kwargs = args_to_native(*args, **kwargs)
        return self._data.__array_prepare__(*args, **kwargs)

    def __array_ufunc__(self, *args, **kwargs):
        args, kwargs = args_to_native(*args, **kwargs)
        return to_startai(self._data.__array_ufunc__(*args, **kwargs))

    def __array_wrap__(self, *args, **kwargs):
        args, kwargs = args_to_native(*args, **kwargs)
        return self._data.__array_wrap__(*args, **kwargs)

    def __array_namespace__(self, api_version=None):
        return startai

    def __repr__(self):
        if self._dev_str is None:
            self._dev_str = startai.as_startai_dev(self.device)
            self._pre_repr = "startai.array"
            if "gpu" in self._dev_str:
                self._post_repr = f", dev={self._dev_str})"
            else:
                self._post_repr = ")"
        sig_fig = startai.array_significant_figures
        dec_vals = startai.array_decimal_values
        if self.backend == "" or startai.is_local():
            # If the array was constructed using implicit backend
            backend = startai.current_backend()
        else:
            # Requirerd in the case that backend is different
            # from the currently set backend
            backend = startai.with_backend(self.backend)
        arr_np = backend.to_numpy(self._data)
        rep = (
            np.array(startai.vec_sig_fig(arr_np, sig_fig))
            if self.size > 0
            else np.array(arr_np)
        )
        with np.printoptions(precision=dec_vals):
            repr = rep.__repr__()[:-1].partition(", dtype")[0].partition(", dev")[0]
            return (
                self._pre_repr
                + repr[repr.find("(") :]
                + self._post_repr.format(startai.current_backend_str())
            )

    def __dir__(self):
        return self._data.__dir__()

    def __getattribute__(self, item):
        return super().__getattribute__(item)

    def __getattr__(self, item):
        try:
            attr = self._data.__getattribute__(item)
        except AttributeError:
            attr = self._data.__getattr__(item)
        return to_startai(attr)

    @handle_view_indexing
    def __getitem__(self, query):
        return startai.get_item(self._data, query)

    def __setitem__(self, query, val):
        self._data = startai.set_item(self._data, query, val)._data

    def __contains__(self, key):
        return self._data.__contains__(key)

    def __getstate__(self):
        data_dict = {}

        # only pickle the native array
        data_dict["data"] = self.data

        # also store the local startai framework that created this array
        data_dict["backend"] = self.backend
        data_dict["device_str"] = startai.as_startai_dev(self.device)

        return data_dict

    def __setstate__(self, state):
        # we can construct other details of startai.Array
        # just by re-creating the startai.Array using the native array

        # get the required backend
        (
            startai.set_backend(state["backend"])
            if state["backend"] is not None and len(state["backend"]) > 0
            else startai.current_backend(state["data"])
        )
        startai_array = startai.array(state["data"])
        startai.previous_backend()

        self.__dict__ = startai_array.__dict__

        # TODO: what about placement of the array on the right device ?
        # device = backend.as_native_dev(state["device_str"])
        # backend.to_device(self, device)

    def __pos__(self):
        return startai.positive(self._data)

    def __neg__(self):
        return startai.negative(self._data)

    def __pow__(self, power):
        """startai.Array special method variant of startai.pow. This method simply
        wraps the function, and so the docstring for startai.pow also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            Input array or float.
        power
            Array or float power. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        ret
            an array containing the element-wise sums. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x = startai.array([1, 2, 3])
        >>> y = x ** 2
        >>> print(y)
        startai.array([1, 4, 9])

        >>> x = startai.array([1.2, 2.1, 3.5])
        >>> y = x ** 2.9
        >>> print(y)
        startai.array([ 1.69678056,  8.59876156, 37.82660675])
        """
        return startai.pow(self._data, power)

    def __rpow__(self, power):
        return startai.pow(power, self._data)

    def __ipow__(self, power):
        return startai.pow(self._data, power)

    def __add__(self, other):
        """startai.Array special method variant of startai.add. This method simply
        wraps the function, and so the docstring for startai.add also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a numeric data type.
        other
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        ret
            an array containing the element-wise sums. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x + y
        >>> print(z)
        startai.array([5, 7, 9])
        """
        return startai.add(self._data, other)

    def __radd__(self, other):
        """startai.Array reverse special method variant of startai.add. This method
        simply wraps the function, and so the docstring for startai.add also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a numeric data type.
        other
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        ret
            an array containing the element-wise sums. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = 1
        >>> y = startai.array([4, 5, 6])
        >>> z = x + y
        >>> print(z)
        startai.array([5, 6, 7])
        """
        return startai.add(other, self._data)

    def __iadd__(self, other):
        return startai.add(self._data, other)

    def __sub__(self, other):
        """startai.Array special method variant of startai.subtract. This method simply
        wraps the function, and so the docstring for startai.subtract also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a numeric data type.
        other
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        ret
            an array containing the element-wise differences. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` instances only:

        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x - y
        >>> print(z)
        startai.array([-3, -3, -3])
        """
        return startai.subtract(self._data, other)

    def __rsub__(self, other):
        """startai.Array reverse special method variant of startai.subtract. This
        method simply wraps the function, and so the docstring for startai.subtract
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a numeric data type.
        other
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        ret
            an array containing the element-wise differences. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = 1
        >>> y = startai.array([4, 5, 6])
        >>> z = x - y
        >>> print(z)
        startai.array([-3, -4, -5])
        """
        return startai.subtract(other, self._data)

    def __isub__(self, other):
        return startai.subtract(self._data, other)

    def __mul__(self, other):
        return startai.multiply(self._data, other)

    def __rmul__(self, other):
        return startai.multiply(other, self._data)

    def __imul__(self, other):
        return startai.multiply(self._data, other)

    def __mod__(self, other):
        return startai.remainder(self._data, other)

    def __rmod__(self, other):
        return startai.remainder(other, self._data)

    def __imod__(self, other):
        return startai.remainder(self._data, other)

    def __divmod__(self, other):
        return startai.divide(self._data, other), startai.remainder(self._data, other)

    def __rdivmod__(self, other):
        return startai.divide(other, self._data), startai.remainder(other, self._data)

    def __truediv__(self, other):
        """startai.Array reverse special method variant of startai.divide. This method
        simply wraps the function, and so the docstring for startai.divide also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a numeric data type.
        other
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = startai.array([1, 2, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x / y
        >>> print(z)
        startai.array([0.25      , 0.40000001, 0.5       ])
        """
        return startai.divide(self._data, other)

    def __rtruediv__(self, other):
        return startai.divide(other, self._data)

    def __itruediv__(self, other):
        return startai.divide(self._data, other)

    def __floordiv__(self, other):
        return startai.floor_divide(self._data, other)

    def __rfloordiv__(self, other):
        return startai.floor_divide(other, self._data)

    def __ifloordiv__(self, other):
        return startai.floor_divide(self._data, other)

    def __matmul__(self, other):
        return startai.matmul(self._data, other)

    def __rmatmul__(self, other):
        return startai.matmul(other, self._data)

    def __imatmul__(self, other):
        return startai.matmul(self._data, other)

    def __abs__(self):
        """startai.Array special method variant of startai.abs. This method simply
        wraps the function, and so the docstring for startai.abs also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.

        Returns
        -------
        ret
            an array containing the absolute value of each element
            in ``self``. The returned array must have the same data
            type as ``self``.

        Examples
        --------
        With :class:`startai.Array` input:

        >>> x = startai.array([6, -2, 0, -1])
        >>> print(abs(x))
        startai.array([6, 2, 0, 1])

        >>> x = startai.array([-1.2, 1.2])
        >>> print(abs(x))
        startai.array([1.2, 1.2])
        """
        return startai.abs(self._data)

    def __float__(self):
        if hasattr(self._data, "__float__"):
            if "complex" in self.dtype:
                res = float(self.real)
            else:
                res = self._data.__float__()
        else:
            res = float(startai.to_scalar(self._data))
        if res is NotImplemented:
            return res
        return to_startai(res)

    def __int__(self):
        if hasattr(self._data, "__int__"):
            if "complex" in self.dtype:
                res = int(self.real)
            else:
                res = self._data.__int__()
        else:
            res = int(startai.to_scalar(self._data))
        if res is NotImplemented:
            return res
        return to_startai(res)

    def __complex__(self):
        res = complex(startai.to_scalar(self._data))
        if res is NotImplemented:
            return res
        return to_startai(res)

    def __bool__(self):
        return self._data.__bool__()

    def __dlpack__(self, stream=None):
        # Not completely supported yet as paddle and tf
        # doesn't support __dlpack__ and __dlpack_device__ dunders right now
        # created issues
        # paddle https://github.com/PaddlePaddle/Paddle/issues/56891
        # tf https://github.com/tensorflow/tensorflow/issues/61769
        return startai.to_dlpack(self)

    def __dlpack_device__(self):
        return self._data.__dlpack_device__()

    def __lt__(self, other):
        """startai.Array special method variant of startai.less. This method simply
        wraps the function, and so the docstring for startai.less also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        other
            second input array. Must be compatible with x1 (with Broadcasting). May have any
            data type.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have a
            data type of bool.

        Examples
        --------
        >>> x = startai.array([6, 2, 3])
        >>> y = startai.array([4, 5, 3])
        >>> z = x < y
        >>> print(z)
        startai.array([ False, True, False])
        """
        return startai.less(self._data, other)

    def __le__(self, other):
        """startai.Array special method variant of startai.less_equal. This method
        simply wraps the function, and so the docstring for startai.less_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        other
            second input array. Must be compatible with x1 (with Broadcasting). May have any
            data type.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have a
            data type of bool.

        Examples
        --------
        >>> x = startai.array([6, 2, 3])
        >>> y = startai.array([4, 5, 3])
        >>> z = x <= y
        >>> print(z)
        startai.array([ False, True, True])
        """
        return startai.less_equal(self._data, other)

    def __eq__(self, other):
        """startai.Array special method variant of startai.equal. This method simply
        wraps the function, and so the docstring for startai.equal also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        other
            second input array. Must be compatible with x1 (with Broadcasting). May have any
            data type.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have a
            data type of bool.

        Examples
        --------
        With :class:`startai.Array` instances:

        >>> x1 = startai.array([1, 0, 1, 1])
        >>> x2 = startai.array([1, 0, 0, -1])
        >>> y = x1 == x2
        >>> print(y)
        startai.array([True, True, False, False])

        >>> x1 = startai.array([1, 0, 1, 0])
        >>> x2 = startai.array([0, 1, 0, 1])
        >>> y = x1 == x2
        >>> print(y)
        startai.array([False, False, False, False])
        """
        return startai.equal(self._data, other)

    def __ne__(self, other):
        """startai.Array special method variant of startai.not_equal. This method
        simply wraps the function, and so the docstring for startai.not_equal also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        other
            second input array. Must be compatible with x1 (with Broadcasting). May have any
            data type.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have a
            data type of bool.

        Examples
        --------
        With :class:`startai.Array` instances:

        >>> x1 = startai.array([1, 0, 1, 1])
        >>> x2 = startai.array([1, 0, 0, -1])
        >>> y = x1 != x2
        >>> print(y)
        startai.array([False, False, True, True])

        >>> x1 = startai.array([1, 0, 1, 0])
        >>> x2 = startai.array([0, 1, 0, 1])
        >>> y = x1 != x2
        >>> print(y)
        startai.array([True, True, True, True])
        """
        return startai.not_equal(self._data, other)

    def __gt__(self, other):
        """startai.Array special method variant of startai.greater. This method simply
        wraps the function, and so the docstring for startai.greater also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        other
            second input array. Must be compatible with x1 (with Broadcasting). May have any
            data type.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have a
            data type of bool.

        Examples
        --------
        With :class:`startai.Array` instances:

        >>> x = startai.array([6, 2, 3])
        >>> y = startai.array([4, 5, 3])
        >>> z = x > y
        >>> print(z)
        startai.array([True,False,False])

        With mix of :class:`startai.Array` and :class:`startai.Container` instances:

        >>> x = startai.array([[5.1, 2.3, -3.6]])
        >>> y = startai.Container(a=startai.array([[4.], [5.1], [6.]]),b=startai.array([[-3.6], [6.], [7.]]))
        >>> z = x > y
        >>> print(z)
        {
            a: startai.array([[True, False, False],
                          [False, False, False],
                          [False, False, False]]),
            b: startai.array([[True, True, False],
                          [False, False, False],
                          [False, False, False]])
        }
        """
        return startai.greater(self._data, other)

    def __ge__(self, other):
        """startai.Array special method variant of startai.greater_equal. This method
        simply wraps the function, and so the docstring for startai.bitwise_xor
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        other
            second input array. Must be compatible with x1 (with Broadcasting). May have any
            data type.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have a
            data type of bool.

        Examples
        --------
        With :class:`startai.Array` instances:

        >>> x = startai.array([6, 2, 3])
        >>> y = startai.array([4, 5, 6])
        >>> z = x >= y
        >>> print(z)
        startai.array([True,False,False])

        With mix of :class:`startai.Array` and :class:`startai.Container` instances:

        >>> x = startai.array([[5.1, 2.3, -3.6]])
        >>> y = startai.Container(a=startai.array([[4.], [5.1], [6.]]),b=startai.array([[5.], [6.], [7.]]))
        >>> z = x >= y
        >>> print(z)
        {
            a: startai.array([[True, False, False],
                          [True, False, False],
                          [False, False, False]]),
            b: startai.array([[True, False, False],
                          [False, False, False],
                          [False, False, False]])
        }
        """
        return startai.greater_equal(self._data, other)

    def __and__(self, other):
        return startai.bitwise_and(self._data, other)

    def __rand__(self, other):
        return startai.bitwise_and(other, self._data)

    def __iand__(self, other):
        return startai.bitwise_and(self._data, other)

    def __or__(self, other):
        return startai.bitwise_or(self._data, other)

    def __ror__(self, other):
        return startai.bitwise_or(other, self._data)

    def __ior__(self, other):
        return startai.bitwise_or(self._data, other)

    def __invert__(self):
        return startai.bitwise_invert(self._data)

    def __xor__(self, other):
        """startai.Array special method variant of startai.bitwise_xor. This method
        simply wraps the function, and so the docstring for startai.bitwise_xor
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        other
            second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` instances:

        >>> a = startai.array([1, 2, 3])
        >>> b = startai.array([3, 2, 1])
        >>> y = a ^ b
        >>> print(y)
        startai.array([2,0,2])

        With mix of :class:`startai.Array` and :class:`startai.Container` instances:

        >>> x = startai.Container(a = startai.array([-67, 21]))
        >>> y = startai.array([12, 13])
        >>> z = x ^ y
        >>> print(z)
        {a: startai.array([-79, 24])}
        """
        return startai.bitwise_xor(self._data, other)

    def __rxor__(self, other):
        return startai.bitwise_xor(other, self._data)

    def __ixor__(self, other):
        return startai.bitwise_xor(self._data, other)

    def __lshift__(self, other):
        return startai.bitwise_left_shift(self._data, other)

    def __rlshift__(self, other):
        return startai.bitwise_left_shift(other, self._data)

    def __ilshift__(self, other):
        return startai.bitwise_left_shift(self._data, other)

    def __rshift__(self, other):
        """startai.Array special method variant of startai.bitwise_right_shift. This
        method simply wraps the function, and so the docstring for
        startai.bitwise_right_shift also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            first input array. Should have an integer data type.
        other
            second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`).
            Should have an integer data type. Each element must be greater than or equal
            to ``0``.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have
            a data type determined by :ref:`type-promotion`.

        Examples
        --------
        With :class:`startai.Array` instances only:

        >>> a = startai.array([2, 3, 4])
        >>> b = startai.array([0, 1, 2])
        >>> y = a >> b
        >>> print(y)
        startai.array([2, 1, 1])
        """
        return startai.bitwise_right_shift(self._data, other)

    def __rrshift__(self, other):
        """startai.Array reverse special method variant of startai.bitwise_right_shift.
        This method simply wraps the function, and so the docstring for
        startai.bitwise_right_shift also applies to this method with minimal
        changes.

        Parameters
        ----------
        self
            first input array. Should have an integer data type.
        other
            second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`).
            Should have an integer data type. Each element must be greater than or equal
            to ``0``.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must have
            a data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> a = 32
        >>> b = startai.array([0, 1, 2])
        >>> y = a >> b
        >>> print(y)
        startai.array([32, 16,  8])
        """
        return startai.bitwise_right_shift(other, self._data)

    def __irshift__(self, other):
        return startai.bitwise_right_shift(self._data, other)

    def __deepcopy__(self, memodict={}):
        try:
            return to_startai(self._data.__deepcopy__(memodict))
        except AttributeError:
            # ToDo: try and find more elegant solution to jax inability to
            #  deepcopy device arrays
            if startai.current_backend_str() == "jax":
                np_array = copy.deepcopy(self._data)
                jax_array = startai.array(np_array)
                return to_startai(jax_array)
            return to_startai(copy.deepcopy(self._data))
        except RuntimeError:
            from startai.functional.startai.gradients import _is_variable

            # paddle and torch don't support the deepcopy protocol on non-leaf tensors
            if _is_variable(self):
                return to_startai(copy.deepcopy(startai.stop_gradient(self)._data))
            return to_startai(copy.deepcopy(self._data))

    def __len__(self):
        if not len(self._data.shape):
            return 0
        try:
            return len(self._data)
        except TypeError:
            return self._data.shape[0]

    def __iter__(self):
        if self.ndim == 0:
            raise TypeError("iteration over a 0-d startai.Array not supported")
        if startai.current_backend_str() == "paddle":
            if self.dtype in ["int8", "int16", "uint8", "float16"]:
                return iter([to_startai(i) for i in startai.unstack(self._data)])
            elif self.ndim == 1:
                return iter([to_startai(i).squeeze(axis=0) for i in self._data])
        return iter([to_startai(i) for i in self._data])
