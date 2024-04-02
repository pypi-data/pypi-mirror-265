import numpy as np
from interface.BaseInterface import BaseInterface
from .NonStationary import NonStationary as NonSt

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

    base_interface = BaseInterface(default_cls=NonSt, params=parameters, interface=interface)
    interface_opts, params_opts = base_interface.opts(**kwargs)

    return interface_opts, params_opts

def newton(x, f, df, **kwargs):
    """
    Newton iterations
    """
    
    interface, parameters = opts(**kwargs)
    verbose = interface['verbose']
    tol = parameters['tol']
    maxit = int(parameters['maxit'])
    stop = parameters['stop']
    method = parameters['method']
    
    if verbose:
        print('------ Newton initialization summary ------')
        print(f'tollerence: {tol}')
        print(f'maximum iter: {maxit}')
        print(f'stopping criteria: {stop}')
        print(f'Linear system solving method: {method}')
    
        print('------ Start iteration ------')
    iter = 0
    nrmdx = np.inf
    normdx = []
    while nrmdx > tol and iter < maxit:
        iter += 1

        dx = -np.linalg.solve(df(x), f(x))
        x = x + dx.reshape((len(dx),))
    
        nrmdx = np.linalg.norm(dx)
        normdx.append(nrmdx)
        if verbose != False: 
            if (iter % verbose == 0):
                print(f'iter= {iter}, norm correction = {nrmdx:12.5e}')
    if iter == maxit and nrmdx > tol:
        print('WARNING in Newton.py, maximum iterations reached but not converged yet')
    return x, iter, normdx
