import numpy as np
import scipy.sparse as sp
from scipy.linalg import eig
from hw_1.problem_2 import Damped_heat
from iteral.nonstationary import newton
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt

from interface.BaseInterface import BaseInterface
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

def init(k, n, **kwargs):
    """
    Function that computes the non-trivial solutions after a bifurcation point
    
    Parameters:
        k (int): the amount of branches.
        n (int): the number of unknowns.
    
    **kwargs: 
        func (class): class containing the ode problem.
        lin  (str): name of the linearize problem in func.
        nonlin (str): name of the nonlinearize problem in func.
        gamma  (float): parameter
    """
    from hw_1.problem_2 import zerofGL1
    
    n = int(n)
    k = int(k)
    func = kwargs.get('func', Damped_heat())
    lin = getattr(func, kwargs.get('lin', 'linGL1'))
    nonlin = getattr(func, kwargs.get('lin', 'fGL1'))
    gamma = kwargs.get('gamma', 0.1)
    
    A = lin(n = n)
    eigenValues, eigenVectors = np.linalg.eig(- A.toarray())
    # eigenValues, eigenVectors = eigs(- A)
    idx = eigenValues.argsort()
    eigenValues = np.real(eigenValues[idx])
    eigenVectors = np.real(eigenVectors[:,idx])

    epsk = 2 * np.sqrt(gamma / (1 + gamma))
    
    # uk = lambda k: eigenVectors[:, k]/np.linalg.norm(eigenVectors[:, k])
    uk = lambda k: eigenVectors[:, k] 
    u = lambda k: epsk * uk(k) 
    
    muk = lambda k: eigenValues[k]
    mu = lambda k: muk(k) * (gamma + 1)
    
    us = []
    mus = [] 
    
    for i in range(0, k):
        print(u(i))
        usol, _ , _ = zerofGL1(u = u(i) / max(abs(u(i))) , n = n, mu = mu(i))
        print('usol', usol)
        us.append(usol)
        mus.append(mu(i))
        
    return us, mus


def cont(mu, u, **kwargs):
    """
    Function that performs natural continuation
    
    Parameters:
        mu (float): starting parameter, eigenvalue
        u  (1d-array): solution u
        mu_end (float): ending paramter, eigenvalue
    
    kwargs:
        steps (int): numper of steps between starting and ending mu
        udot (1d-array): direction vector
        func (class): class containing the ode problem.
    """
    from hw_1.problem_2 import zerofGL1
    
    mu_end = kwargs.get('mu_end', 200)
    udot = kwargs.get('udot', u - (1/3) * u**3)
    fmu = lambda u: u - (1/3) * u**3
    x = np.linspace(0, 1, len(u) + 2)[1:-1]
    feps = lambda u: x*(1 - x)
    falpha = kwargs.get('falpha', None)
    wrt_eps = kwargs.get('wrt_eps', False)
    homotopy = kwargs.get('homotopy', False)
    eps = kwargs.get('eps', 0.01)
    eps_end = kwargs.get('eps_end', 0)
    if wrt_eps == True:
        steps = np.linspace(eps, eps_end, kwargs.get('steps', 10))
    elif homotopy == True: 
        steps = np.linspace(kwargs.get('alpha', 0), kwargs.get('alpha_end', 1), kwargs.get('steps', 10))
    else: 
        steps = np.linspace(mu, mu_end , kwargs.get('steps', 10)) 
    func = kwargs.get('func', Damped_heat())
    jac = getattr(func, kwargs.get('jac', 'JacGL1'))
    f = kwargs.get('f', 'fGL1')
    u_branch = []
    iter_list = []

    for i, cur in enumerate(steps):
        
        u1 = u + abs(cur - steps[i - 1]) * udot if i != 0 else u + abs(cur - steps[i + 1]) * udot

        if wrt_eps:
            u1, iter , _ = zerofGL1(u = u1, n = len(u) + 1, mu = mu, func = func, eps = cur)
            udot = -np.linalg.solve(jac(u = u1, mu = mu, n = len(u) + 1), feps(u = u1))
       
        elif homotopy:
            u1, iter , _ = zerofGL1(u = u1, n = len(u) + 1, mu = mu, func = func, eps = eps, f = f, alpha = cur)
            udot = -np.linalg.solve(jac(u = u1, mu = mu, n = len(u) + 1), falpha)
            
        else:
            u1, iter , _ = zerofGL1(u = u1, n = len(u) + 1, mu = cur, func = func)
            udot = -np.linalg.solve(jac(u = u1, mu = cur, n = len(u) + 1), fmu(u = u1))
        
        if len(u_branch) == 0:  # If u_branch is empty, create the first column
            u_branch = np.expand_dims(u1, axis=1)
        else:
            u_branch = np.column_stack((u_branch, u1))  # Append usol as a new column to u_branch

        u = u_branch[:, i]
        iter_list.append(iter)
        
    
    return u_branch, iter_list