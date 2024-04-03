import numpy as np
from scipy.linalg import lu, inv, solve
from numpy.linalg import qr

from interface.BaseInterface import BaseInterface
from .Stationary import Stationary as St

def opts(interface={}, parameters={}, **kwargs):
    """
    Options handler for OSIM function.

    Keyword Arguments:
    interface (dict): Dictionary containing interface options.
    parameters (dict): Dictionary containing parameter options.

    Returns:
    dict: Interface options.
    dict: Parameter options.
    """
    params = {
        'stop': 'matrix',
        'maxit': 1e4,
        'tol': 1e-8,
        'method': 'standard'  # Default linear system solving method
    }
    intf = {
        'verbose': True,
    }
    parameters.update(params)
    interface.update(intf)

    base_interface = BaseInterface(default_cls=St, params=parameters, interface=interface)
    interface_opts, params_opts = base_interface.opts(**kwargs)

    return interface_opts, params_opts

    
def Z(V, A = None, P=None, L=None, U=None, method = 'standard'):
    if method == 'LU':
        y = solve(inv(U), P.dot(V))
        z = solve(inv(L), y)
    else:
        z = A @ V
    return z

def osim(A, V, **kwargs):
    """
    Orthogonal Subspace Iteration Method (OSIM).

    Args:
    A (numpy.ndarray): The matrix to compute the eigenvalues and eigenvectors for.
    V (numpy.ndarray): Initial guess of eigenvectors.

    Keyword Arguments:
    tol (float): Tolerance for convergence (default: 1e-6).
    maxit (int): Maximum number of iterations (default: 100).
    stop (str): Stopping criteria for convergence. Options are 'eig' (default), 'matrix', or 'residual'.
    method (str): Method for solving linear systems. Options are 'LU' (default) or any method supported by scipy.linalg.lu.

    Returns:
    numpy.ndarray: Matrix of eigenvectors.
    numpy.ndarray: Matrix of transformed eigenvectors.
    tuple: Tuple containing eigenvalues at each iteration.

    Notes:
    This function implements the Orthogonal Subspace Iteration Method (OSIM) to
    compute eigenvectors and eigenvalues of a matrix A.

    Examples:
    >>> import numpy as np
    >>> from iteral import stationary as st
    >>> A = np.array([[1, 0], [0, 1]])
    >>> V = np.array([[1], [0]])
    >>> V, BV, iter = st.osim(A, V, tol=1e-8, maxit=1000, stop='eig', method='LU')

    You can also pass keyword arguments using a dictionary. For example:
    >>> kwargs = {'tol': 1e-8, 'maxit': 1000, 'stop': 'eig', 'method': 'LU'}
    >>> V, BV, iter = osim(A, V, **kwargs)
    
    You can also pass keyword arguments using two separate dictionaries for parameters and interface. For example:
    >>> parameters = {'tol': 1e-8, 'maxit': 1000, 'stop': 'eig', 'method': 'LU'}
    >>> interface = {'verbose': True}
    >>> V, BV, iter = st.osim(A, V, parameters=parameters, interface=interface)
    """
    
    # Check if the number of rows of V matches the number of columns of A
    if V.shape[0] != A.shape[1]:
        raise ValueError("Number of rows of V must match the number of columns of A.")
    
    interface, parameters = opts(**kwargs)
    verbose = interface['verbose']
    tol = parameters['tol']
    maxit = int(parameters['maxit'])
    stop = parameters['stop']
    method = parameters['method']
    
    if verbose:
        print('------ OSIM initialization summary ------')
        print(f'tollerence: {tol}')
        print(f'maximum iter: {maxit}')
        print(f'stopping criteria: {stop}')
        print(f'Linear system solving method: {method}')
    
        print('------ Start iteration ------')
    
    if method == 'LU':
        P, L, U = lu(A.toarray())
    else:
        P = L = U = None

    B = lambda V: V.T @ Z(V = V, A = A, P = P, L = L, U = U, method = method)

    iter = []
    for n in range(maxit):
        Zn = Z(V = V, A = A, P = P, L = L, U = U, method = method)
        BV = B(V = V)
        eig = np.diag(BV)
        if verbose != False: 
            if (n % verbose == 0):
                print(f"Eigenvalues at n = {n}: {eig}")
        else:
            if (n % 5000 == 0):
                print(f"iteration n = {n}")
        
        if n > 0:
            iter.append(eig)
        
        V, _ = qr(Zn)

        if stop == 'eig':
            if n > 1:
                if abs(np.linalg.norm(eig - iter[n - 1])) < tol:
                    print(f'The Orthogonal Subspace Method has converged in {n} iterations.')
                    break
            else:
                pass
        elif stop == 'matrix':
            
            if n > 1:
                if np.linalg.norm(BV - B(V)) < tol:
                    print(f'The Orthogonal Subspace Method has converged in {n} iterations.')
                    break
        
        elif stop == 'residual':
            
            if np.linalg.norm(A @ V - V @ B(V)) < tol:
                print(f'The Orthogonal Subspace Method has converged in {n} iterations.')
                break
    
        if n >= maxit:
            print('The Orthogonal Subspace Method has not converged')
        
    return V, BV, tuple(iter)
        
        

    
    