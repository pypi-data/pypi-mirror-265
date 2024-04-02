# global
from typing import Union, Optional, List, Dict, Tuple, Sequence, Literal

# local
from startai.data_classes.container.base import ContainerBase
import startai


class _ContainerWithLinearAlgebraExperimental(ContainerBase):
    @staticmethod
    def static_eigh_tridiagonal(
        alpha: Union[startai.Array, startai.NativeArray, startai.Container],
        beta: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        eigvals_only: Union[bool, startai.Container] = True,
        select: Union[str, startai.Container] = "a",
        select_range: Optional[
            Union[Tuple[int, int], List[int], startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        tol: Optional[Union[float, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Union[startai.Container, Tuple[startai.Container, startai.Container]]:
        """startai.Container static method variant of startai.eigh_tridiagonal. This
        method simply wraps the function, and so the docstring for
        startai.eigh_tridiagonal also applies to this method with minimal changes.

        Parameters
        ----------
        alpha
            An array or a container of real or complex arrays each of
            shape (n), the diagonal elements of the matrix.
        beta
            An array or a container of real or complex arrays each of shape (n-1),
            containing the elements of the first super-diagonal of the matrix.
        eigvals_only
            If False, both eigenvalues and corresponding eigenvectors are computed.
            If True, only eigenvalues are computed. Default is True.
        select
            Optional string with values in {'a', 'v', 'i'}
            (default is 'a') that determines which eigenvalues
            to calculate: 'a': all eigenvalues. 'v': eigenvalues
            in the interval (min, max] given by select_range.
            'i': eigenvalues with indices min <= i <= max.
        select_range
            Size 2 tuple or list or array specifying the range of
            eigenvalues to compute together with select. If select
            is 'a', select_range is ignored.
        tol
            Optional scalar. Ignored when backend is not Tensorflow. The
            absolute tolerance to which each eigenvalue is required. An
            eigenvalue (or cluster) is considered to have converged if
            it lies in an interval of this width. If tol is None (default),
            the value eps*|T|_2 is used where eps is the machine precision,
            and |T|_2 is the 2-norm of the matrix T.

        Returns
        -------
        eig_vals
            The eigenvalues of the matrix in non-decreasing order.
        eig_vectors
            If eigvals_only is False the eigenvectors are returned in the second
            output argument.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> alpha = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([2., 2., 2.]))
        >>> beta = startai.array([0.,2.])
        >>> y = startai.Container.static_eigh_tridiagonal(alpha, beta)
        >>> print(y)
        {
            a: startai.array([-0.56155, 0., 3.56155]),
            b: startai.array([0., 2., 4.])
        }

        >>> alpha = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([2., 2., 2.]))
        >>> beta = startai.Container(a=startai.array([0.,2.]), b=startai.array([2.,2.]))
        >>> y = startai.Container.static_eigh_tridiagonal(alpha, beta)
        >>> print(y)
        {
            a: startai.array([-0.56155, 0., 3.56155]),
            b: startai.array([-0.82842, 2., 4.82842])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "eigh_tridiagonal",
            alpha,
            beta,
            eigvals_only=eigvals_only,
            select=select,
            select_range=select_range,
            tol=tol,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def eigh_tridiagonal(
        self: startai.Container,
        beta: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        eigvals_only: Union[bool, startai.Container] = True,
        select: Union[str, startai.Container] = "a",
        select_range: Optional[
            Union[Tuple[int, int], List[int], startai.Array, startai.NativeArray, startai.Container]
        ] = None,
        tol: Optional[Union[float, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Union[startai.Container, Tuple[startai.Container, startai.Container]]:
        """startai.Container instance method variant of startai.eigh_tridiagonal. This
        method simply wraps the function, and so the docstring for
        startai.eigh_tridiagonal also applies to this method with minimal changes.

        Parameters
        ----------
        self
            A container of real or complex arrays each of shape (n),
            the diagonal elements of the matrix.
        beta
            An array or a container of real or complex arrays each of shape
            (n-1), containing the elements of the first super-diagonal of the matrix.
        eigvals_only
            If False, both eigenvalues and corresponding eigenvectors are computed.
            If True, only eigenvalues are computed. Default is True.
        select
            Optional string with values in {'a', 'v', 'i'} (default is 'a') that
            determines which eigenvalues to calculate: 'a': all eigenvalues.
            'v': eigenvalues in the interval (min, max] given by select_range.
            'i': eigenvalues with indices min <= i <= max.
        select_range
            Size 2 tuple or list or array specifying the range of eigenvalues to
            compute together with select. If select is 'a', select_range is ignored.
        tol
            Optional scalar. Ignored when backend is not Tensorflow. The absolute
            tolerance to which each eigenvalue is required. An eigenvalue (or cluster)
            is considered to have converged if it lies in an interval of this width.
            If tol is None (default), the value eps*|T|_2 is used where eps is the
            machine precision, and |T|_2 is the 2-norm of the matrix T.

        Returns
        -------
        eig_vals
            The eigenvalues of the matrix in non-decreasing order.
        eig_vectors
            If eigvals_only is False the eigenvectors are returned in
            the second output argument.

        Examples
        --------
        >>> alpha = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([2., 2., 2.]))
        >>> beta = startai.array([0.,2.])
        >>> y = alpha.eigh_tridiagonal(beta)
        >>> print(y)
        {
            a: startai.array([-0.56155, 0., 3.56155]),
            b: startai.array([0., 2., 4.])
        }

        >>> alpha = startai.Container(a=startai.array([0., 1., 2.]), b=startai.array([2., 2., 2.]))
        >>> beta = startai.Container(a=startai.array([0.,2.]), b=startai.array([2.,2.]))
        >>> y = alpha.eigh_tridiagonal(beta)
        >>> print(y)
        {
            a: startai.array([-0.56155, 0., 3.56155]),
            b: startai.array([-0.82842, 2., 4.82842])
        }
        """
        return self.static_eigh_tridiagonal(
            self,
            beta,
            eigvals_only=eigvals_only,
            select=select,
            select_range=select_range,
            tol=tol,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_diagflat(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        offset: Union[int, startai.Container] = 0,
        padding_value: Union[float, startai.Container] = 0,
        align: Union[str, startai.Container] = "RIGHT_LEFT",
        num_rows: Union[int, startai.Container] = -1,
        num_cols: Union[int, startai.Container] = -1,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        return ContainerBase.cont_multi_map_in_function(
            "diagflat",
            x,
            offset=offset,
            padding_value=padding_value,
            align=align,
            num_rows=num_rows,
            num_cols=num_cols,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def diagflat(
        self: startai.Container,
        /,
        *,
        offset: Union[int, startai.Container] = 0,
        padding_value: Union[float, startai.Container] = 0,
        align: Union[str, startai.Container] = "RIGHT_LEFT",
        num_rows: Union[int, startai.Container] = -1,
        num_cols: Union[int, startai.Container] = -1,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.diagflat. This method
        simply wraps the function, and so the docstring for startai.diagflat also
        applies to this method with minimal changes.

        Examples
        --------
        >>> x = startai.Container(a=[1,2])
        >>> startai.diagflat(x, k=1)
        {
            a: startai.array([[0, 1, 0],
                          [0, 0, 2],
                          [0, 0, 0]])
        }
        """
        return self.static_diagflat(
            self,
            offset=offset,
            padding_value=padding_value,
            align=align,
            num_rows=num_rows,
            num_cols=num_cols,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_kron(
        a: Union[startai.Array, startai.NativeArray, startai.Container],
        b: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.kron. This method simply
        wraps the function, and so the docstring for startai.kron also applies to
        this method with minimal changes.

        Parameters
        ----------
        a
            first container with input arrays.
        b
            second container with input arrays
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including arrays corresponding to the Kronecker product of
            the arrays in the input containers, computed element-wise

        Examples
        --------
        >>> a = startai.Container(x=startai.array([1,2]), y=startai.array(50))
        >>> b = startai.Container(x=startai.array([3,4]), y=startai.array(9))
        >>> startai.Container.static_kron(a, b)
        {
            a: startai.array([3, 4, 6, 8])
            b: startai.array([450])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "kron",
            a,
            b,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def kron(
        self: startai.Container,
        b: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.kron. This method
        simply wraps the function, and so the docstring for startai.kron also
        applies to this method with minimal changes.

        Examples
        --------
        >>> a = startai.Container(x=startai.array([1,2]), y=startai.array([50]))
        >>> b = startai.Container(x=startai.array([3,4]), y=startai.array(9))
        >>> a.kron(b)
        {
            a: startai.array([3, 4, 6, 8])
            b: startai.array([450])
        }
        """
        return self.static_kron(
            self,
            b,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_matrix_exp(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        return ContainerBase.cont_multi_map_in_function(
            "matrix_exp",
            x,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
        )

    def matrix_exp(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.diagflat. This method
        simply wraps the function, and so the docstring for startai.diagflat also
        applies to this method with minimal changes.

        Examples
        --------
        >>> x = startai.array([[[1., 0.],
                            [0., 1.]],
                            [[2., 0.],
                            [0., 2.]]])
        >>> startai.matrix_exp(x)
        startai.array([[[2.7183, 1.0000],
                    [1.0000, 2.7183]],
                    [[7.3891, 1.0000],
                    [1.0000, 7.3891]]])
        """
        return self.static_matrix_exp(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            out=out,
        )

    @staticmethod
    def static_eig(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.eig. This method simply
        wraps the function, and so the docstring for startai.eig also applies to
        this method with minimal changes.

        Parameters
        ----------
            x
                container with input arrays.

        Returns
        -------
            ret
                container including tuple of arrays corresponding to
                eigenvealues and eigenvectors of input array

        Examples
        --------
        >>> x = startai.array([[1,2], [3,4]])
        >>> c = startai.Container({'x':{'xx':x}})
        >>> startai.Container.eig(c)
        {
            x:  {
                    xx: (tuple(2), <class startai.array.array.Array>, shape=[2, 2])
                }
        }
        >>> startai.Container.eig(c)['x']['xx']
        (
            startai.array([-0.37228107+0.j,  5.3722816 +0.j]),
            startai.array([
                    [-0.8245648 +0.j, -0.41597357+0.j],
                    [0.56576747+0.j, -0.9093767 +0.j]
                ])
        )
        """
        return ContainerBase.cont_multi_map_in_function(
            "eig",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def eig(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.eig. This method simply
        wraps the function, and so the docstring for startai.eig also applies to
        this method with minimal changes.

        Parameters
        ----------
            x
                container with input arrays.

        Returns
        -------
            ret
                container including arrays corresponding
                eigenvealues and eigenvectors of input arrays

        Examples
        --------
        >>> x = startai.array([[1,2], [3,4]])
        >>> c = startai.Container({'x':{'xx':x}})
        >>> c.eig()
        {
            x:  {
                    xx: (tuple(2), <class startai.array.array.Array>, shape=[2, 2])
                }
        }
        >>>c.eig()['x']['xx']
        (
            startai.array([-0.37228107+0.j,  5.3722816 +0.j]),
            startai.array([
                    [-0.8245648 +0.j, -0.41597357+0.j],
                    [0.56576747+0.j, -0.9093767 +0.j]
                ])
        )
        """
        return self.static_eig(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_eigvals(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.eigvals. This method
        simply wraps the function, and so the docstring for startai.eigvals also
        applies to this method with minimal changes.

        Parameters
        ----------
            x
                container with input arrays.

        Returns
        -------
            ret
                container including array corresponding
                to eigenvalues of input array

        Examples
        --------
        >>> x = startai.array([[1,2], [3,4]])
        >>> c = startai.Container({'x':{'xx':x}})
        >>> startai.Container.eigvals(c)
        {
            x: {
                xx: startai.array([-0.37228132+0.j, 5.37228132+0.j])
            }
        }
        >>> startai.Container.eigvals(c)['x']['xx']
        startai.array([-0.37228132+0.j,  5.37228132+0.j])
        """
        return ContainerBase.cont_multi_map_in_function(
            "eigvals",
            x,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def eigvals(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.eigvals. This method
        simply wraps the function, and so the docstring for startai.eigvals also
        applies to this method with minimal changes.

        Parameters
        ----------
            x
                container with input arrays.

        Returns
        -------
            ret
                container including array corresponding
                to eigenvalues of input array

        Examples
        --------
        >>> x = startai.array([[1,2], [3,4]])
        >>> c = startai.Container({'x':{'xx':x}})
        >>> c.eigvals()
        {
            x: {
                xx: startai.array([-0.37228132+0.j, 5.37228132+0.j])
            }
        }
        >>> c.eigvals()['x']['xx']
        startai.array([-0.37228132+0.j,  5.37228132+0.j])
        """
        return self.static_eigvals(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_adjoint(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ):
        """startai.Container static method variant of startai.adjoint. This method
        simply wraps the function, and so the docstring for startai.adjoint also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            container with input arrays of dimensions greater than 1.
        out
            optional output container, for writing the result to.

        Returns
        -------
        ret
            container including arrays corresponding to the conjugate transpose of
            the arrays in the input container

        Examples
        --------
        >>> x = np.array([[1.-1.j, 2.+2.j],
                          [3.+3.j, 4.-4.j]])
        >>> y = np.array([[1.-2.j, 3.+4.j],
                          [1.-0.j, 2.+6.j]])
        >>> c = startai.Container(a=startai.array(x), b=startai.array(y))
        >>> startai.Container.static_adjoint(c)
        {
            a: startai.array([[1.+1.j, 3.-3.j],
                          [2.-2.j, 4.+4.j]]),
            b: startai.array([[1.+2.j, 1.-0.j],
                          [3.-4.j, 2.-6.j]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "adjoint",
            x,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
        )

    def adjoint(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ):
        """startai.Container instance method variant of startai.adjoint. This method
        simply wraps the function, and so the docstring for startai.adjoint also
        applies to this method with minimal changes.

        Examples
        --------
        >>> x = np.array([[1.-1.j, 2.+2.j],
                          [3.+3.j, 4.-4.j]])
        >>> c = startai.Container(a=startai.array(x))
        >>> c.adjoint()
        {
            a: startai.array([[1.+1.j, 3.-3.j],
                          [2.-2.j, 4.+4.j]])
        }
        """
        return self.static_adjoint(
            self, key_chains=key_chains, to_apply=to_apply, out=out
        )

    @staticmethod
    def static_multi_dot(
        x: Sequence[Union[startai.Container, startai.Array, startai.NativeArray]],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.multi_dot. This method
        simply wraps the function, and so the docstring for startai.multi_dot also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            sequence of matrices to multiply.
        out
            optional output array, for writing the result to. It must have a valid
            shape, i.e. the resulting shape after applying regular matrix multiplication
            to the inputs.

        Returns
        -------
        ret
            dot product of the arrays.

        Examples
        --------
        With :class:`startai.Container` input:

        >>> a = startai.Container(x=startai.arange(2 * 3).reshape((2, 3)),
        ...                   y=startai.arange(2 * 3).reshape((2, 3)))
        >>> b = startai.Container(x=startai.arange(3 * 2).reshape((3, 2)),
        ...                   y=startai.arange(3 * 2).reshape((3, 2)))
        >>> c = startai.Container(x=startai.arange(2 * 2).reshape((2, 2)),
        ...                   y=startai.arange(2 * 2).reshape((2, 2)))
        >>> startai.Container.static_multi_dot((a, b, c))
        {
            x: startai.array([[26, 49],
                          [80, 148]]),
            y: startai.array([[26, 49],
                          [80, 148]])
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "multi_dot",
            x,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def multi_dot(
        self: startai.Container,
        arrays: Sequence[Union[startai.Container, startai.Array, startai.NativeArray]],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = True,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.multi_dot. This method
        simply wraps the function, and so the docstring for startai.multi_dot also
        applies to this method with minimal changes.

        Examples
        --------
        >>> a = startai.Container(x=startai.arange(2 * 3).reshape((2, 3)),
        ...                   y=startai.arange(2 * 3).reshape((2, 3)))
        >>> b = startai.Container(x=startai.arange(3 * 2).reshape((3, 2)),
        ...                   y=startai.arange(3 * 2).reshape((3, 2)))
        >>> c = startai.Container(x=startai.arange(2 * 2).reshape((2, 2)),
        ...                   y=startai.arange(2 * 2).reshape((2, 2)))
        >>> a.multi_dot((b, c))
        {
            x: startai.array([[26, 49],
                          [80, 148]]),
            y: startai.array([[26, 49],
                          [80, 148]])
        }
        """
        return self.static_multi_dot(
            (self, *arrays),
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_cond(
        x: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        p: Optional[Union[int, float, None, startai.Container]] = None,
        out: Optional[startai.Container] = None,
    ):
        """startai.Container static method variant of startai.cond. This method simply
        wraps the function, and so the docstring for startai.cond also applies to
        this method with minimal changes.

        Parameters
        ----------
            x
                container with input arrays.
            p
                order of the norm of the matrix (see startai.norm).

        Returns
        -------
            ret
                container including array corresponding
                to condition number of input array

        Examples
        --------
        >>> x = startai.array([[1,2], [3,4]])
        >>> startai.Container.static_cond(x)
        startai.array(14.933034)
        """
        return ContainerBase.cont_multi_map_in_function(
            "cond",
            x,
            p=p,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def cond(
        self: startai.Container,
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        p: Optional[Union[int, float, None, startai.Container]] = None,
    ):
        """startai.Container instance method variant of startai.cond. This method
        simply wraps the function, and so the docstring for startai.cond also
        applies to this method with minimal changes.

        Parameters
        ----------
            self
                container with input arrays.
            p
                order of the norm of the matrix (see startai.norm).

        Returns
        -------
            ret
                container including array corresponding
                to condition number of input array

        Examples
        --------
        >>> x = startai.array([[1,2], [3,4]])
        >>> c = startai.Container(a=x)
        >>> c.cond()
        startai.array(14.933034)

        >>> x = startai.array([[1,2], [3,4]])
        >>> c = startai.Container(a=x)
        >>> c.cond(p=1)
        startai.array(21.0)

        With :class:`startai.Container` input:

        >>> a = startai.Container(x=startai.arange(2 * 3).reshape((2, 3)),
        ...                   y=startai.arange(2 * 3).reshape((2, 3)))
        >>> a.cond()
        {
            x: startai.array(14.933034),
            y: startai.array(14.933034)
        }
        """
        return self.static_cond(
            self,
            p=p,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_mode_dot(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        matrix_or_vector: Union[startai.Array, startai.NativeArray, startai.Container],
        mode: Union[int, startai.Container],
        transpose: Optional[Union[bool, startai.Container]] = False,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.mode_dot. This method
        simply wraps the function, and so the docstring for startai.mode_dot also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            tensor of shape ``(i_1, ..., i_k, ..., i_N)``
        matrix_or_vector
            1D or 2D array of shape ``(J, i_k)`` or ``(i_k, )``
            matrix or vectors to which to n-mode multiply the tensor
        mode
            int in the range(1, N)
        transpose
            If True, the matrix is transposed.
            For complex tensors, the conjugate transpose is used.
        out
            optional output array, for writing the result to.
            It must have a shape that the result can broadcast to.

        Returns
        -------
        startai.Container
            `mode`-mode product of `tensor` by `matrix_or_vector`
            * of shape :math:`(i_1, ..., i_{k-1}, J, i_{k+1}, ..., i_N)`
            if matrix_or_vector is a matrix
            * of shape :math:`(i_1, ..., i_{k-1}, i_{k+1}, ..., i_N)`
            if matrix_or_vector is a vector
        """
        return ContainerBase.cont_multi_map_in_function(
            "mode_dot",
            x,
            matrix_or_vector,
            mode,
            transpose,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def mode_dot(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        matrix_or_vector: Union[startai.Array, startai.NativeArray, startai.Container],
        mode: Union[int, startai.Container],
        transpose: Optional[Union[bool, startai.Container]] = False,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ):
        """startai.Container instance method variant of startai.mode_dot. This method
        simply wraps the function, and so the docstring for startai.mode_dot also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            tensor of shape ``(i_1, ..., i_k, ..., i_N)``
        matrix_or_vector
            1D or 2D array of shape ``(J, i_k)`` or ``(i_k, )``
            matrix or vectors to which to n-mode multiply the tensor
        mode
            int in the range(1, N)
        transpose
            If True, the matrix is transposed.
            For complex tensors, the conjugate transpose is used.
        out
            optional output array, for writing the result to.
            It must have a shape that the result can broadcast to.

        Returns
        -------
        startai.Container
            `mode`-mode product of `tensor` by `matrix_or_vector`
            * of shape :math:`(i_1, ..., i_{k-1}, J, i_{k+1}, ..., i_N)`
            if matrix_or_vector is a matrix
            * of shape :math:`(i_1, ..., i_{k-1}, i_{k+1}, ..., i_N)`
            if matrix_or_vector is a vector
        """
        return self.static_mode_dot(
            self,
            matrix_or_vector,
            mode,
            transpose,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_multi_mode_dot(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        mat_or_vec_list: Sequence[Union[startai.Array, startai.NativeArray, startai.Container]],
        /,
        modes: Optional[Union[Sequence[int], startai.Container]] = None,
        skip: Optional[Union[Sequence[int], startai.Container]] = None,
        transpose: Optional[Union[bool, startai.Container]] = False,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.multi_mode_dot. This
        method simply wraps the function, and so the docstring for
        startai.multi_mode_dot also applies to this method with minimal changes.

        Parameters
        ----------
        x
            the input tensor

        mat_or_vec_list
            sequence of matrices or vectors of length ``tensor.ndim``

        skip
            None or int, optional, default is None
            If not None, index of a matrix to skip.

        modes
            None or int list, optional, default is None

        transpose
            If True, the matrices or vectors in in the list are transposed.
            For complex tensors, the conjugate transpose is used.
        out
            optional output array, for writing the result to.
            It must have a shape that the result can broadcast to.

        Returns
        -------
        startai.Container
            tensor times each matrix or vector in the list at mode `mode`
        """
        return ContainerBase.cont_multi_map_in_function(
            "multi_mode_dot",
            x,
            mat_or_vec_list,
            skip,
            modes,
            transpose,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def multi_mode_dot(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        mat_or_vec_list: Sequence[Union[startai.Array, startai.NativeArray, startai.Container]],
        /,
        modes: Optional[Union[Sequence[int], startai.Container]] = None,
        skip: Optional[Union[Sequence[int], startai.Container]] = None,
        transpose: Optional[Union[bool, startai.Container]] = False,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.multi_mode_dot. This
        method simply wraps the function, and so the docstring for
        startai.multi_mode_dot also applies to this method with minimal changes.

        Parameters
        ----------
        self
            the input tensor

        mat_or_vec_list
            sequence of matrices or vectors of length ``tensor.ndim``

        modes
            None or int list, optional, default is None

        skip
            None or int, optional, default is None
            If not None, index of a matrix to skip.

        transpose
            If True, the matrices or vectors in in the list are transposed.
            For complex tensors, the conjugate transpose is used.
        out
            optional output array, for writing the result to.
            It must have a shape that the result can broadcast to.

        Returns
        -------
        startai.Container
            tensor times each matrix or vector in the list at mode `mode`
        """
        return self.static_multi_mode_dot(
            self,
            mat_or_vec_list,
            skip,
            modes,
            transpose,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_svd_flip(
        U: Union[startai.Array, startai.NativeArray, startai.Container],
        V: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        u_based_decision: Optional[Union[bool, startai.Container]] = True,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, startai.Container]:
        """startai.Container static method variant of startai.svd_flip. This method
        simply wraps the function, and so the docstring for startai.svd_flip also
        applies to this method with minimal changes.

        Parameters
        ----------
        U
            left singular matrix output of SVD
        V
            right singular matrix output of SVD
        u_based_decision
            If True, use the columns of u as the basis for sign flipping.
            Otherwise, use the rows of v. The choice of which variable to base the
            decision on is generally algorithm dependent.

        Returns
        -------
        u_adjusted, v_adjusted : container with the same dimensions as the input.
        """
        return ContainerBase.cont_multi_map_in_function(
            "svd_flip",
            U,
            V,
            u_based_decision,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def svd_flip(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        V: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        u_based_decision: Optional[Union[bool, startai.Container]] = True,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, startai.Container]:
        """startai.Container instance method variant of startai.svd_flip. This method
        simply wraps the function, and so the docstring for startai.svd_flip
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            left singular matrix output of SVD
        V
            right singular matrix output of SVD
        u_based_decision
            If True, use the columns of u as the basis for sign flipping.
            Otherwise, use the rows of v. The choice of which variable to base the
            decision on is generally algorithm dependent.

        Returns
        -------
        u_adjusted, v_adjusted : container with the same dimensions as the input.
        """
        return self.static_svd_flip(
            self,
            V,
            u_based_decision,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_make_svd_non_negative(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        U: Union[startai.Array, startai.NativeArray, startai.Container],
        S: Union[startai.Array, startai.NativeArray, startai.Container],
        V: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        nntype: Optional[Union[Literal["nndsvd", "nndsvda"], startai.Container]] = "nndsvd",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, startai.Container]:
        """startai.Container static method variant of startai.make_svd_non_negative.
        This method simply wraps the function, and so the docstring for
        startai.make_svd_non_negative also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            tensor being decomposed.
        U
            left singular matrix from SVD.
        S
            diagonal matrix from SVD.
        V
            right singular matrix from SVD.
        nntype
            whether to fill small values with 0.0 (nndsvd),
            or the tensor mean (nndsvda, default).

        [1]: Boutsidis & Gallopoulos. Pattern Recognition, 41(4): 1350-1362, 2008.
        """
        return ContainerBase.cont_multi_map_in_function(
            "make_svd_non_negative",
            x,
            U,
            S,
            V,
            nntype=nntype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def make_svd_non_negative(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        U: Union[startai.Array, startai.NativeArray, startai.Container],
        S: Union[startai.Array, startai.NativeArray, startai.Container],
        V: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        nntype: Optional[Union[Literal["nndsvd", "nndsvda"], startai.Container]] = "nndsvd",
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, startai.Container]:
        """startai.Container instance method variant of startai.make_svd_non_negative.
        This method simply wraps the function, and so the docstring for
        startai.make_svd_non_negative applies to this method with minimal changes.

        Parameters
        ----------
        self
            tensor being decomposed.
        U
            left singular matrix from SVD.
        S
            diagonal matrix from SVD.
        V
            right singular matrix from SVD.
        nntype
            whether to fill small values with 0.0 (nndsvd),
            or the tensor mean (nndsvda, default).

        [1]: Boutsidis & Gallopoulos. Pattern Recognition, 41(4): 1350-1362, 2008.
        """
        return self.static_make_svd_non_negative(
            self,
            U,
            S,
            V,
            nntype=nntype,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_tensor_train(
        input_tensor: Union[startai.Array, startai.NativeArray, startai.Container],
        rank: Union[Sequence[int], startai.Container],
        /,
        *,
        svd: Optional[Union[Literal["truncated_svd"], startai.Container]] = "truncated_svd",
        verbose: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, Sequence[startai.Container]]:
        """startai.Container static method variant of startai.tensor_train. This method
        simply wraps the function, and so the docstring for startai.tensor_train
        also applies to this method with minimal changes.

        Parameters
        ----------
        input_tensor
            tensor to be decomposed.
        rank
            maximum allowable TT-ranks of the decomposition.
        svd
            SVD method to use.
        verbose
            level of verbosity.
        """
        return ContainerBase.cont_multi_map_in_function(
            "tensor_train",
            input_tensor,
            rank,
            svd=svd,
            verbose=verbose,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def tensor_train(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        rank: Union[Sequence[int], startai.Container],
        /,
        *,
        svd: Optional[Union[Literal["truncated_svd"], startai.Container]] = "truncated_svd",
        verbose: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, Sequence[startai.Container]]:
        """startai.Container instance method variant of startai.tensor_train. This
        method simply wraps the function, and so the docstring for
        startai.tensor_train also applies to this method with minimal changes.

        Parameters
        ----------
        input_tensor
            tensor to be decomposed.
        rank
            maximum allowable TT-ranks of the decomposition.
        svd
            SVD method to use.
        verbose
            level of verbosity.
        """
        return self.static_tensor_train(
            self,
            rank,
            svd=svd,
            verbose=verbose,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_truncated_svd(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        compute_uv: Union[bool, startai.Container] = True,
        n_eigenvecs: Optional[Union[int, startai.Container]] = None,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Union[startai.Container, Tuple[startai.Container, startai.Container, startai.Container]]:
        """startai.Container static method variant of startai.truncated_svd. This
        method simply wraps the function, and so the docstring for
        startai.truncated_svd also applies to this method with minimal changes.

        Parameters
        ----------
        x
            Container of 2D-arrays
        compute_uv
            If ``True`` then left and right singular vectors
            will be computed and returned in ``U`` and ``Vh``,
            respectively. Otherwise, only the singular values
            will be computed, which can be significantly faster.
        n_eigenvecs
            if specified, number of eigen[vectors-values] to return
            else full matrices will be returned

        Returns
        -------
        ret
            a namedtuple ``(U, S, Vh)``
            Each returned container must have the same
             floating-point data type as ``x``.
        """
        return ContainerBase.cont_multi_map_in_function(
            "truncated_svd",
            x,
            compute_uv,
            n_eigenvecs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def truncated_svd(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        compute_uv: Union[bool, startai.Container] = True,
        n_eigenvecs: Optional[Union[int, startai.Container]] = None,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Union[startai.Container, Tuple[startai.Container, startai.Container, startai.Container]]:
        """startai.Container instance method variant of startai.truncated_svd. This
        method simply wraps the function, and so the docstring for
        startai.truncated_svd also applies to this method with minimal changes.

        Parameters
        ----------
        x
            Container of 2D-arrays
        compute_uv
            If ``True`` then left and right singular vectors
            will be computed and returned in ``U`` and ``Vh``
            respectively. Otherwise, only the singular values will
            be computed, which can be significantly faster.
        n_eigenvecs
            if specified, number of eigen[vectors-values] to return
            else full matrices will be returned

        Returns
        -------
        ret
            a namedtuple ``(U, S, Vh)``
            Each returned container must have the
            same floating-point data type as ``x``.
        """
        return self.static_truncated_svd(
            self,
            compute_uv,
            n_eigenvecs,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_initialize_tucker(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        rank: Union[Sequence[int], startai.Container],
        modes: Union[Sequence[int], startai.Container],
        /,
        *,
        init: Optional[
            Union[Literal["svd", "random"], startai.TuckerTensor, startai.Container]
        ] = "svd",
        seed: Optional[Union[int, startai.Container]] = None,
        svd: Optional[Union[Literal["truncated_svd"], startai.Container]] = "truncated_svd",
        non_negative: Optional[Union[bool, startai.Container]] = False,
        mask: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        svd_mask_repeats: Optional[Union[int, startai.Container]] = 5,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, Sequence[startai.Container]]:
        """startai.Container static method variant of startai.initialize_tucker. This
        method simply wraps the function, and so the docstring for
        startai.initialize_tucker also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input tensor
        rank
            number of components
        modes
            modes to consider in the input tensor
        seed
            Used to create a random seed distribution
            when init == 'random'
        init
            initialization scheme for tucker decomposition.
        svd
            function to use to compute the SVD
        non_negative
            if True, non-negative factors are returned
        mask
            array of booleans with the same shape as ``tensor`` should be 0 where
            the values are missing and 1 everywhere else. Note:  if tensor is
            sparse, then mask should also be sparse with a fill value of 1 (or
            True).
        svd_mask_repeats
            number of iterations for imputing the values in the SVD matrix when
            mask is not None

        Returns
        -------
        core
            initialized core tensor
        factors
            list of factors
        """
        return ContainerBase.cont_multi_map_in_function(
            "initialize_tucker",
            x,
            rank,
            modes,
            seed=seed,
            init=init,
            svd=svd,
            non_negative=non_negative,
            mask=mask,
            svd_mask_repeats=svd_mask_repeats,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def initialize_tucker(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        rank: Union[Sequence[int], startai.Container],
        modes: Union[Sequence[int], startai.Container],
        /,
        *,
        init: Optional[
            Union[Literal["svd", "random"], startai.TuckerTensor, startai.Container]
        ] = "svd",
        seed: Optional[Union[int, startai.Container]] = None,
        svd: Optional[Union[Literal["truncated_svd"], startai.Container]] = "truncated_svd",
        non_negative: Optional[Union[bool, startai.Container]] = False,
        mask: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        svd_mask_repeats: Optional[Union[int, startai.Container]] = 5,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, Sequence[startai.Container]]:
        """startai.Container instance method variant of startai.initialize_tucker. This
        method simply wraps the function, and so the docstring for
        startai.initialize_tucker also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input tensor
        rank
            number of components
        modes
            modes to consider in the input tensor
        seed
            Used to create a random seed distribution
            when init == 'random'
        init
            initialization scheme for tucker decomposition.
        svd
            function to use to compute the SVD
        non_negative
            if True, non-negative factors are returned
        mask
            array of booleans with the same shape as ``tensor`` should be 0 where
            the values are missing and 1 everywhere else. Note:  if tensor is
            sparse, then mask should also be sparse with a fill value of 1 (or
            True).
        svd_mask_repeats
            number of iterations for imputing the values in the SVD matrix when
            mask is not None

        Returns
        -------
        core
            initialized core tensor
        factors
            list of factors
        """
        return self.static_initialize_tucker(
            self,
            rank,
            modes,
            seed=seed,
            init=init,
            svd=svd,
            non_negative=non_negative,
            mask=mask,
            svd_mask_repeats=svd_mask_repeats,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_partial_tucker(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        rank: Union[Sequence[int], startai.Container],
        modes: Union[Sequence[int], startai.Container],
        /,
        *,
        n_iter_max: Optional[Union[int, startai.Container]] = 100,
        init: Optional[
            Union[Literal["svd", "random"], startai.TuckerTensor, startai.Container]
        ] = "svd",
        svd: Optional[Union[Literal["truncated_svd"], startai.Container]] = "truncated_svd",
        seed: Optional[Union[int, startai.Container]] = None,
        mask: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        svd_mask_repeats: Optional[Union[int, startai.Container]] = 5,
        tol: Optional[Union[float, startai.Container]] = 10e-5,
        verbose: Optional[Union[bool, startai.Container]] = False,
        return_errors: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, Sequence[startai.Container]]:
        """startai.Container static method variant of startai.partial_tucker. This
        method simply wraps the function, and so the docstring for
        startai.partial_tucker also applies to this method with minimal changes.

        Parameters
        ----------
        x
            input tensor
        rank
            number of components
        modes
            modes to consider in the input tensor
        seed
            Used to create a random seed distribution
            when init == 'random'
        init
            initialization scheme for tucker decomposition.
        svd
            function to use to compute the SVD
        mask
            array of booleans with the same shape as ``tensor`` should be 0 where
            the values are missing and 1 everywhere else. Note:  if tensor is
            sparse, then mask should also be sparse with a fill value of 1 (or
            True).
        svd_mask_repeats
            number of iterations for imputing the values in the SVD matrix when
            mask is not None

        Returns
        -------
        core
            initialized core tensor
        factors
            list of factors
        """
        return ContainerBase.cont_multi_map_in_function(
            "partial_tucker",
            x,
            rank,
            modes,
            seed=seed,
            init=init,
            svd=svd,
            n_iter_max=n_iter_max,
            mask=mask,
            svd_mask_repeats=svd_mask_repeats,
            tol=tol,
            verbose=verbose,
            return_errors=return_errors,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def partial_tucker(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        rank: Union[Sequence[int], startai.Container],
        modes: Union[Sequence[int], startai.Container],
        /,
        *,
        n_iter_max: Optional[Union[int, startai.Container]] = 100,
        init: Optional[
            Union[Literal["svd", "random"], startai.TuckerTensor, startai.Container]
        ] = "svd",
        svd: Optional[Union[Literal["truncated_svd"], startai.Container]] = "truncated_svd",
        seed: Optional[Union[int, startai.Container]] = None,
        mask: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        svd_mask_repeats: Optional[Union[int, startai.Container]] = 5,
        tol: Optional[Union[float, startai.Container]] = 10e-5,
        verbose: Optional[Union[bool, startai.Container]] = False,
        return_errors: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, Sequence[startai.Container]]:
        """startai.Container static method variant of startai.partial_tucker. This
        method simply wraps the function, and so the docstring for
        startai.partial_tucker also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input tensor
        rank
            number of components
        modes
            modes to consider in the input tensor
        seed
            Used to create a random seed distribution
            when init == 'random'
        init
            initialization scheme for tucker decomposition.
        svd
            function to use to compute the SVD
        mask
            array of booleans with the same shape as ``tensor`` should be 0 where
            the values are missing and 1 everywhere else. Note:  if tensor is
            sparse, then mask should also be sparse with a fill value of 1 (or
            True).
        svd_mask_repeats
            number of iterations for imputing the values in the SVD matrix when
            mask is not None

        Returns
        -------
        core
            initialized core tensor
        factors
            list of factors
        """
        return self.static_partial_tucker(
            self,
            rank,
            modes,
            n_iter_max=n_iter_max,
            init=init,
            svd=svd,
            seed=seed,
            mask=mask,
            svd_mask_repeats=svd_mask_repeats,
            tol=tol,
            verbose=verbose,
            return_errors=return_errors,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_tucker(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        rank: Union[Sequence[int], startai.Container],
        /,
        *,
        fixed_factors: Optional[Union[Sequence[int], startai.Container]] = None,
        n_iter_max: Optional[Union[int, startai.Container]] = 100,
        init: Optional[
            Union[Literal["svd", "random"], startai.TuckerTensor, startai.Container]
        ] = "svd",
        svd: Optional[Union[Literal["truncated_svd"], startai.Container]] = "truncated_svd",
        seed: Optional[Union[int, startai.Container]] = None,
        mask: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        svd_mask_repeats: Optional[Union[int, startai.Container]] = 5,
        tol: Optional[Union[float, startai.Container]] = 10e-5,
        verbose: Optional[Union[bool, startai.Container]] = False,
        return_errors: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, Sequence[startai.Container]]:
        """startai.Container static method variant of startai.tucker. This method
        simply wraps the function, and so the docstring for startai.tucker also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input tensor
        rank
            size of the core tensor, ``(len(ranks) == tensor.ndim)``
            if int, the same rank is used for all modes
        fixed_factors
            if not None, list of modes for which to keep the factors fixed.
            Only valid if a Tucker tensor is provided as init.
        n_iter_max
            maximum number of iteration
        init
            {'svd', 'random'}, or TuckerTensor optional
            if a TuckerTensor is provided, this is used for initialization
        svd
            str, default is 'truncated_svd'
            function to use to compute the SVD,
        seed
            Used to create a random seed distribution
            when init == 'random'
        mask
            array of booleans with the same shape as ``tensor`` should be 0 where
            the values are missing and 1 everywhere else. Note:  if tensor is
            sparse, then mask should also be sparse with a fill value of 1 (or
            True).
        svd_mask_repeats
            number of iterations for imputing the values in the SVD matrix when
            mask is not None
        tol
            tolerance: the algorithm stops when the variation in
            the reconstruction error is less than the tolerance
        verbose
            if True, different in reconstruction errors are returned at each
            iteration.

        return_errors
            Indicates whether the algorithm should return all reconstruction errors
            and computation time of each iteration or not
            Default: False

        Returns
        -------
             Container of startai.TuckerTensors or startai.TuckerTensors and
            container of reconstruction errors if return_errors is True.

        References
        ----------
        .. [1] tl.G.Kolda and B.W.Bader, "Tensor Decompositions and Applications",
        SIAM REVIEW, vol. 51, n. 3, pp. 455-500, 2009.
        """
        return ContainerBase.cont_multi_map_in_function(
            "tucker",
            x,
            rank,
            fixed_factors=fixed_factors,
            seed=seed,
            init=init,
            svd=svd,
            n_iter_max=n_iter_max,
            mask=mask,
            svd_mask_repeats=svd_mask_repeats,
            tol=tol,
            verbose=verbose,
            return_errors=return_errors,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def tucker(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        rank: Union[Sequence[int], startai.Container],
        /,
        *,
        fixed_factors: Optional[Union[Sequence[int], startai.Container]] = None,
        n_iter_max: Optional[Union[int, startai.Container]] = 100,
        init: Optional[
            Union[Literal["svd", "random"], startai.TuckerTensor, startai.Container]
        ] = "svd",
        svd: Optional[Union[Literal["truncated_svd"], startai.Container]] = "truncated_svd",
        seed: Optional[Union[int, startai.Container]] = None,
        mask: Optional[Union[startai.Array, startai.NativeArray, startai.Container]] = None,
        svd_mask_repeats: Optional[Union[int, startai.Container]] = 5,
        tol: Optional[Union[float, startai.Container]] = 10e-5,
        verbose: Optional[Union[bool, startai.Container]] = False,
        return_errors: Optional[Union[bool, startai.Container]] = False,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Tuple[startai.Container, Sequence[startai.Container]]:
        """startai.Container static method variant of startai.tucker. This method
        simply wraps the function, and so the docstring for startai.tucker also
        applies to this method with minimal changes.

        Parameters
        ----------
        x
            input tensor
        rank
            size of the core tensor, ``(len(ranks) == tensor.ndim)``
            if int, the same rank is used for all modes
        fixed_factors
            if not None, list of modes for which to keep the factors fixed.
            Only valid if a Tucker tensor is provided as init.
        n_iter_max
            maximum number of iteration
        init
            {'svd', 'random'}, or TuckerTensor optional
            if a TuckerTensor is provided, this is used for initialization
        svd
            str, default is 'truncated_svd'
            function to use to compute the SVD,
        seed
            Used to create a random seed distribution
            when init == 'random'
        mask
            array of booleans with the same shape as ``tensor`` should be 0 where
            the values are missing and 1 everywhere else. Note:  if tensor is
            sparse, then mask should also be sparse with a fill value of 1 (or
            True).
        svd_mask_repeats
            number of iterations for imputing the values in the SVD matrix when
            mask is not None
        tol
            tolerance: the algorithm stops when the variation in
            the reconstruction error is less than the tolerance
        verbose
            if True, different in reconstruction errors are returned at each
            iteration.

        return_errors
            Indicates whether the algorithm should return all reconstruction errors
            and computation time of each iteration or not
            Default: False

        Returns
        -------
             Container of startai.TuckerTensors or startai.TuckerTensors and
            container of reconstruction errors if return_errors is True.

        References
        ----------
        .. [1] tl.G.Kolda and B.W.Bader, "Tensor Decompositions and Applications",
        SIAM REVIEW, vol. 51, n. 3, pp. 455-500, 2009.
        """
        return self.static_tucker(
            self,
            rank,
            fixed_factors=fixed_factors,
            n_iter_max=n_iter_max,
            init=init,
            svd=svd,
            seed=seed,
            mask=mask,
            svd_mask_repeats=svd_mask_repeats,
            tol=tol,
            verbose=verbose,
            return_errors=return_errors,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_dot(
        a: Union[startai.Array, startai.NativeArray, startai.Container],
        b: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        out: Optional[Union[startai.Array, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Union[startai.Array, startai.Container]:
        """Compute the dot product between two arrays `a` and `b` using the
        current backend's implementation. The dot product is defined as the sum
        of the element- wise product of the input arrays.

        Parameters
        ----------
        a
            First input array.
        b
            Second input array.
        out
            Optional output array. If provided, the output array to store the result.

        Returns
        -------
        ret
            The dot product of the input arrays.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> a = startai.array([1, 2, 3])
        >>> b = startai.array([4, 5, 6])
        >>> result = startai.dot(a, b)
        >>> print(result)
        startai.array(32)

        >>> a = startai.array([[1, 2], [3, 4]])
        >>> b = startai.array([[5, 6], [7, 8]])
        >>> c = startai.empty_like(a)
        >>> startai.dot(a, b, out=c)
        >>> print(c)
        startai.array([[19, 22],
            [43, 50]])

        >>> a = startai.array([[1.1, 2.3, -3.6]])
        >>> b = startai.array([[-4.8], [5.2], [6.1]])
        >>> c = startai.zeros((1, 1))
        >>> startai.dot(a, b, out=c)
        >>> print(c)
        startai.array([[-15.28]])
        """
        return ContainerBase.cont_multi_map_in_function(
            "dot",
            a,
            b,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def dot(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        b: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        out: Optional[Union[startai.Array, startai.Container]] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> Union[startai.Array, startai.Container]:
        """Compute the dot product between two arrays `a` and `b` using the
        current backend's implementation. The dot product is defined as the sum
        of the element- wise product of the input arrays.

        Parameters
        ----------
        self
            First input array.
        b
            Second input array.
        out
            Optional output array. If provided, the output array to store the result.

        Returns
        -------
        ret
            The dot product of the input arrays.

        Examples
        --------
        With :class:`startai.Array` inputs:

        >>> a = startai.array([1, 2, 3])
        >>> b = startai.array([4, 5, 6])
        >>> result = startai.dot(a, b)
        >>> print(result)
        startai.array(32)

        >>> a = startai.array([[1, 2], [3, 4]])
        >>> b = startai.array([[5, 6], [7, 8]])
        >>> c = startai.empty_like(a)
        >>> startai.dot(a, b, out=c)
        >>> print(c)
        startai.array([[19, 22],
            [43, 50]])

        >>> a = startai.array([[1.1, 2.3, -3.6]])
        >>> b = startai.array([[-4.8], [5.2], [6.1]])
        >>> c = startai.zeros((1, 1))
        >>> startai.dot(a, b, out=c)
        >>> print(c)
        startai.array([[-15.28]])
        """
        return self.static_dot(
            self,
            b,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_tt_matrix_to_tensor(
        tt_matrix: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container static method variant of startai.tt_matrix_to_tensor. This
        method simply wraps the function, and so the docstring for
        startai.tt_matrix_to_tensor also applies to this method with minimal
        changes.

        Parameters
        ----------
        tt_matrix
                array of 4D-arrays
                TT-Matrix factors (known as core) of shape
                (rank_k, left_dim_k, right_dim_k, rank_{k+1})

        out
            optional output container, for writing the result to.

        Returns
        -------
        output_tensor
                    tensor whose TT-Matrix decomposition was given by 'factors'

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[[[[0.49671414],
        ...                      [-0.1382643]],
        ...
        ...                     [[0.64768857],
        ...                      [1.5230298]]]],
        ...                   [[[[-0.23415337],
        ...                      [-0.23413695]],
        ...
        ...                     [[1.57921278],
        ...                      [0.76743472]]]]])))
        >>> y = startai.Container.static_tt_matrix_to_tensor(x)
        >>> print(y["a"])
        startai.array([[[[-0.1163073 , -0.11629914],
        [ 0.03237505,  0.03237278]],

        [[ 0.78441733,  0.38119566],
        [-0.21834874, -0.10610882]]],


        [[[-0.15165846, -0.15164782],
        [-0.35662258, -0.35659757]],

        [[ 1.02283812,  0.49705869],
        [ 2.40518808,  1.16882598]]]])
        """
        return ContainerBase.cont_multi_map_in_function(
            "tt_matrix_to_tensor",
            tt_matrix,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def tt_matrix_to_tensor(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        /,
        *,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
        out: Optional[startai.Container] = None,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.tt_matrix_to_tensor.
        This method simply wraps the function, and so the docstring for
        startai.tt_matrix_to_tensor also applies to this method with minimal
        changes.

        Parameters
        ----------
        tt_matrix
                array of 4D-arrays
                TT-Matrix factors (known as core) of shape
                (rank_k, left_dim_k, right_dim_k, rank_{k+1})

        out
            optional output container, for writing the result to.

        Returns
        -------
        output_tensor
                    tensor whose TT-Matrix decomposition was given by 'factors'

        Examples
        --------
        >>> x = startai.Container(a=startai.array([[[[[0.49671414],
        ...                      [-0.1382643]],
        ...
        ...                     [[0.64768857],
        ...                      [1.5230298]]]],
        ...                   [[[[-0.23415337],
        ...                      [-0.23413695]],
        ...
        ...                     [[1.57921278],
        ...                      [0.76743472]]]]])))
        >>> y = startai.Container.tt_matrix_to_tensor(x)
        >>> print(y["a"])
        startai.array([[[[-0.1163073 , -0.11629914],
        [ 0.03237505,  0.03237278]],

        [[ 0.78441733,  0.38119566],
        [-0.21834874, -0.10610882]]],


        [[[-0.15165846, -0.15164782],
        [-0.35662258, -0.35659757]],

        [[ 1.02283812,  0.49705869],
        [ 2.40518808,  1.16882598]]]])
        """
        return self.static_tt_matrix_to_tensor(
            self,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def static_higher_order_moment(
        x: Union[startai.Array, startai.NativeArray, startai.Container],
        order: Union[Sequence[int], startai.Container],
        /,
        *,
        out: Optional[startai.Array] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.higher_order_moment. This
        method simply wraps the function, and so the docstring for
        startai.higher_order_moment also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            matrix of size (n_samples, n_features)
            or tensor of size(n_samples, D1, ..., DN)

        order
            number of the higher-order moment to compute

        Returns
        -------
        tensor
            if tensor is a matrix of size (n_samples, n_features),
            tensor of size (n_features, )*order
        """
        return ContainerBase.cont_multi_map_in_function(
            "higher_order_moment",
            x,
            order,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def higher_order_moment(
        self: Union[startai.Array, startai.NativeArray, startai.Container],
        order: Union[Sequence[int], startai.Container],
        /,
        *,
        out: Optional[startai.Array] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.higher_order_moment.
        This method simply wraps the function, and so the docstring for
        startai.higher_order_moment also applies to this method with minimal
        changes.

        Parameters
        ----------
        x
            matrix of size (n_samples, n_features)
            or tensor of size(n_samples, D1, ..., DN)

        order
            number of the higher-order moment to compute

        Returns
        -------
        tensor
            if tensor is a matrix of size (n_samples, n_features),
            tensor of size (n_features, )*order

        Examples
        --------
        >>> a = startai.array([[1, 2], [3, 4]])
        >>> result = startai.higher_order_moment(a, 3)
        >>> print(result)
        startai.array([[
            [14, 19],
            [19, 26]],
           [[19, 26],
            [26, 36]
        ]])
        """
        return self.static_higher_order_moment(
            self,
            order,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    @staticmethod
    def static_batched_outer(
        tensors: Sequence[Union[startai.Array, startai.NativeArray, startai.Container]],
        /,
        *,
        out: Optional[startai.Array] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container static method variant of startai.batched_outer. This
        method simply wraps the function, and so the docstring for
        startai.batched_outer also applies to this method with minimal changes.

        Parameters
        ----------
        tensors
            list of tensors of shape (n_samples, J1, ..., JN) ,
            (n_samples, K1, ..., KM) ...

        Returns
        -------
        outer product of tensors
            of shape (n_samples, J1, ..., JN, K1, ..., KM, ...)

        Examples
        --------
        >>> a = startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        >>> b = startai.array([[[.1, .2], [.3, .4]], [[.5, .6], [.7, .8]]])
        >>> result = startai.batched_outer(a, b)
        >>> print(result)
        startai.array([[[[[0.1, 0.2],
              [0.30000001, 0.40000001]],
             [[0.2       , 0.40000001],
              [0.60000002, 0.80000001]]],
            [[[0.3       , 0.60000001],
              [0.90000004, 1.20000002]],
             [[0.40000001, 0.80000001],
              [1.20000005, 1.60000002]]]],
           [[[[2.5       , 3.00000012],
              [3.49999994, 4.00000006]],
             [[3.        , 3.60000014],
              [4.19999993, 4.80000007]]],
            [[[3.5       , 4.20000017],
              [4.89999992, 5.60000008]],
             [[4.        , 4.80000019],
              [5.5999999 , 6.4000001 ]]]]])
        """
        return ContainerBase.cont_multi_map_in_function(
            "batched_outer",
            tensors,
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )

    def batched_outer(
        self: startai.Container,
        tensors: Sequence[Union[startai.Container, startai.Array, startai.NativeArray]],
        /,
        *,
        out: Optional[startai.Array] = None,
        key_chains: Optional[Union[List[str], Dict[str, str], startai.Container]] = None,
        to_apply: Union[bool, startai.Container] = True,
        prune_unapplied: Union[bool, startai.Container] = False,
        map_sequences: Union[bool, startai.Container] = False,
    ) -> startai.Container:
        """startai.Container instance method variant of startai.batched_outer. This
        method simply wraps the function, and so the docstring for
        startai.batched_outer also applies to this method with minimal changes.

        Parameters
        ----------
        tensors
            list of tensors of shape (n_samples, J1, ..., JN) ,
            (n_samples, K1, ..., KM) ...

        Returns
        -------
        outer product of tensors
            of shape (n_samples, J1, ..., JN, K1, ..., KM, ...)

        Examples
        --------
        >>> a = startai.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        >>> b = startai.array([[[.1, .2], [.3, .4]], [[.5, .6], [.7, .8]]])
        >>> result = startai.batched_outer(a, b)
        >>> print(result)
        startai.array([[[[[0.1, 0.2],
              [0.30000001, 0.40000001]],
             [[0.2       , 0.40000001],
              [0.60000002, 0.80000001]]],
            [[[0.3       , 0.60000001],
              [0.90000004, 1.20000002]],
             [[0.40000001, 0.80000001],
              [1.20000005, 1.60000002]]]],
           [[[[2.5       , 3.00000012],
              [3.49999994, 4.00000006]],
             [[3.        , 3.60000014],
              [4.19999993, 4.80000007]]],
            [[[3.5       , 4.20000017],
              [4.89999992, 5.60000008]],
             [[4.        , 4.80000019],
              [5.5999999 , 6.4000001 ]]]]])
        """
        return self.static_batched_outer(
            (self, *tensors),
            out=out,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
        )
