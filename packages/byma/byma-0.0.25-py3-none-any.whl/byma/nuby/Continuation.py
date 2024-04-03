import numpy as np
import scipy.sparse as sp
from ..iteral.nonstationary import newton
from ..interface.BaseInterface import BaseInterface
from .Bifurcation import Bifurcation as Bf

def opts(interface={}, parameters={}, **kwargs):
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

    base_interface = BaseInterface(default_cls=Bf, params=parameters, interface=interface)
    interface_opts, params_opts = base_interface.opts(**kwargs)

    return interface_opts, params_opts

def step(x, df, dfmu, dx, dmu, **kwargs):
        """
    Perform one step of the continuation.

    Parameters:
        x (array_like): Current state.
        df (callable): Function to evaluate the Jacobian matrix with respect to state variable x.
        dfmu (callable): Function to evaluate the Jacobian matrix derivative with respect to parameter mu.
        dx (array_like): Current tangent with respect to state variable.
        dmu (float or array_like): Incremental change in the parameter value.
        **kwargs: Additional keyword arguments.

    Returns:
        tuple: A tuple containing the updated state x and the norm of the correction.

    Description:
    This function performs one step of the continuation, updating the state variable x and the tangent dx using the provided functions for evaluating the Jacobian matrix and its derivative with respect to the parameter.

    """
        
        # Predictor
        x += dmu * dx
        kwargs.update({'mode' : True})
        
        # Corrector 
        x, dxnorm = newton(x = x, f = dfmu, df = df, **kwargs)

        # Compute the tangent
        dfx1 = df(x)
        dfmu1 = dfmu(x)
        if sp.issparse(dfx1) and sp.issparse(dfmu1):
            dx = sp.linalg.spsolve(dfx1, -dfmu1)
            
        else:
            dx = np.linalg.solve(dfx1, -dfmu1)
            
        if abs(dx) < 1e-12:
            raise Exception('dx too small')

        
        return x, dxnorm

def cont(x0, dx0, start, df, dfmu, dmu=None, target=None, **kwargs):
    """
    Perform a continuation in parameter value from a starting value to a target value or until the maximum iteration is met, with constant step size.

    This function performs a continuation in parameter space from a starting value to a target value, or until the maximum iteration is met, adjusting the state variable x along the way. The continuation is carried out using the provided functions for evaluating the Jacobian matrix and its derivative with respect to the parameter.

    Parameters
    ----------
        x0 : array_like
            Initial state.
        dx0 : array_like
            Initial tangent with respect to state variable.
        start : float
            Starting parameter value.
        df : callable
            Function to evaluate the Jacobian matrix with respect to state variable x and parameter mu.
        dfmu : callable
            Function to evaluate the Jacobian matrix derivative with respect to parameter mu.
        dmu : float or array_like, optional
            Incremental change in the parameter value for each iteration. If None and target is None, raises ValueError.
        target : float or None, optional
            Target parameter value. If None, continuation is performed until maxit_con iterations.
        **kwargs : dict
            Additional keyword arguments for customization.
            maxit_con : int, optional
                Maximum number of continuation steps. Default is 1000.
            method : str, optional
                Continuation method ('normal' or 'pseudo-arclength'). Default is 'normal'.
            mode : str, optional
                Return mode ('partial' or 'full'). Default is 'partial'.
            Other keyword arguments : Additional parameters specific to the step function used internally.

    Returns
    -------
        tuple or array_like
            Depending on the mode specified in kwargs, returns either a tuple or an array.
            - In 'partial' mode, returns a tuple containing the final state x and the final parameter value mu.
            - In 'full' mode, returns an array containing all the states x, an array of the norm of the correction at each step, and the final parameter value mu (if target is None).

    Raises
    ------
        ValueError
            If either 'dmu' or 'target' should be not 'None' but are not provided.
        ValueError
            If the provided continuation method is invalid. Choose either 'normal' or 'pseudo-arclength'.

    Examples
    --------
    >>> # Define the functions df and dfmu
    >>> def df(x, mu0):
    >>>     # Compute the Jacobian matrix with respect to state variable x and parameter mu
    >>>     pass
    >>> def dfmu(x, mu0):
    >>>     # Compute the Jacobian matrix derivative with respect to parameter mu
    >>>     pass
    >>> 
    >>> # Define the initial state and tangent
    >>> x0 = np.array([1.0, 2.0])
    >>> dx0 = np.array([0.1, 0.1])
    >>> 
    >>> # Perform continuation from start value to target value
    >>> start = 0.0
    >>> target = 1.0
    >>> result = cont(x0, dx0, start, df, dfmu, target=target, maxit_con=1000, method='normal', mode='full')
    >>> print(result)
    """
    interface_opts, params_opts = opts(**kwargs)
    verbose = interface_opts['verbose']
    mode = interface_opts['mode']
    method = interface_opts['method']
    maxit_con = params_opts['maxit_cont']
    
    x = x0
    dx = dx0
    mu = start

    # Set some parameters
    if target is None:
        maxit = maxit_con
        if dmu is None:
            raise ValueError("Either 'dmu' or 'target' should be not 'None'")
    else:
        mus = np.linspace(mu, target, maxit_con)
        
    # Perform the continuation
    branch = []
    dxnorms = []

    for j in range(maxit):
        
        if target is None:
            mu0 = mu0 + dmu if isinstance(dmu, float) else mu0 + dmu[j]
        else:
            mu0 = mus[j]
            dmu = mu - mu0 if mu != start else mu0 - mus[j]

        df = lambda x: df(x = x, mu0 = mu0)
        dfmu = lambda x: dfmu(x = x, mu0 = mu0)
        
        if method == 'normal':
            x, dxnorm = step(x, df, dfmu, dx, dmu, **kwargs)
        elif method == 'pseudo-arclength':
            raise ValueError("Pseudo-arclength'conitnuation is not yet avialible")
        else:
            raise ValueError("Invalid continuation method. Choose either 'normal' or 'pseudo-arclength'.")

        branch.append(x)
        dxnorms.append(dxnorm)

    if mode == 'partial':
        return branch, mu0 if target is None else branch
    elif mode == 'full':
        return branch, dxnorms, mu0 if target is None else branch, dxnorms
    else:
        return x, mu0 if target is None else x