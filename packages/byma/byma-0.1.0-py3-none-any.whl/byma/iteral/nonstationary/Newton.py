import numpy as np
from ...interface.BaseInterface import BaseInterface as bs
from .NonStationary import NonStationary as NonSt
import scipy.sparse as sp

_DEFAULT_OPTS = {
    'stop': 'normal', 
    'maxit': 1e4, 
    'tol': 1e-8, 
    'verbose': False,
    'mode': None, 
    'method': 'normal',
    }


@bs.set_defaults(default_cls = NonSt, default_opts=_DEFAULT_OPTS)
def newton(x, f, df, **kwargs):
    """
    Perform Newton iterations to find the root of a given function.
    
    :param x: array_like
        Initial guess for the root.
    :param f: callable
        Function to evaluate the residuals.
    :param df: callable
        Function to evaluate the Jacobian matrix.
    :param kwargs: dict
        Additional keyword arguments for customization.
        - tol (float): Tolerance for convergence. Default is 1e-8.
        - maxit (int): Maximum number of iterations. Default is 10000.
        - verbose (bool): If True, prints iteration information. Default is True.
        - mode (bool): If True, returns additional iteration information. Default is True.

    :return: tuple
        Tuple containing the root and optionally the number of iterations and norm of correction.
        If mode is True, returns (root, iterations, norm_correction), otherwise just returns root.

    Raises
    ============
        ValueError: If the maximum number of iterations or tolerance is not a positive integer.

    Examples
    ============
        Example 1: Basic usage
        >>> root, iterations, norm_correction = newton(2.0, lambda x: x**2 - 4, lambda x: 2 * x, verbose=True)
        >>> print("Root:", root, "Iterations:", iterations, "Norm of correction:", norm_correction)
        
        Example 2: Usage with kwargs provided as a dictionary
        >>> kwargs = {'verbose': True, 'tol': 1e-6, 'maxit': 20}
        >>> root, iterations, norm_correction = newton(3.0, lambda x: x**3 - 27, lambda x: 3 * x**2, **kwargs)
        >>> print("Root:", root, "Iterations:", iterations, "Norm of correction:", norm_correction)
    """
    _opts = bs.opts(**kwargs)
    verbose = _opts['verbose']
    mode = _opts['mode']
    tol = _opts['tol']
    maxit = int(_opts['maxit'])
    stop = _opts['stop']
    
    if maxit <= 0 or not isinstance(maxit, int):
        raise ValueError("Maximum number of iterations 'maxit' must be a positive integer.")
    if tol <= 0:
        raise ValueError("Tolerance 'tol' must be a positive value.")
    
    if verbose:
        print('------ Newton Method summary ------')
        print(f'tollerence: {tol}')
        print(f'maximum iter: {maxit}')
        print(f'stopping criteria: {stop}')
        print(f'starting guess: {x}')
    
        print('------ Start iteration ------')

    for iter in range(maxit):
        f_value = f(x)
        df_value = df(x)
        
        if sp.issparse(df_value) and sp.issparse(df_value):
            dx = sp.linalg.spsolve(df_value, -f_value)
            dxnorm = sp.linalg.norm(dx)
            fnorm = sp.linalg.norm(f_value)
        else:
            dx = np.linalg.solve(df_value, -f_value)
            dxnorm = np.linalg.norm(dx)
            fnorm = np.linalg.norm(f_value)
        
        x += dx
        
        if sp.issparse(df_value) and sp.issparse(df_value):
            fnorm = sp.linalg.norm(df(x)-f(x))
        else:
            fnorm = np.linalg.norm(df(x) - f(x))
        
        if (fnorm < tol and stop == 'residual-check'):
            if verbose:
                print(f'Newton converged in {iter + 1} iterations with ||F|| = {fnorm}')
            return x, dxnorm if mode else x
        
        if (dxnorm < tol and stop == 'normal'):
            if verbose:
                print(f'Newton converged in {iter + 1} iterations with ||dx|| = {dxnorm}')
            return x, dxnorm if mode else x
        
        if verbose:
            print(f'Newton status at iteration {iter + 1}: ||F|| = {fnorm}, ||dx|| = {dxnorm}')

    if verbose:
        print(f'Newton did not converge within {maxit} iterations')

    return x, dxnorm if mode else x
