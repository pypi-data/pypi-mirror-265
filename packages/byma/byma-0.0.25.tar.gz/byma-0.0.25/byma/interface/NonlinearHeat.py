import numpy as np
import scipy.sparse as sp

class NonlinearHeat():
    '''
    Damped stationary heat equation
            u_xx + mu(u - 1/3 u^3)   x in [0,1]
            u(0) = 1, u(1) = 0
    discretize using finite difference method.
    
    The linearize version is
            u_xx + mu•u    x in [0,1]
            u(0) = 1, u(1) = 0
    discretize using finite difference method.
    
    functions:

        GL1(x, mu)
            inputs
                x   1d vector
                mu  scalar parameter
            Output
                checking if is x is a zero of the righ hand side
        
        fGL1(u,n,mu)
            inputs
                n   scalar determining the size of the matrix
                u   1d vector
                mu  scalar parameter
            Output
                eval    the resulting sparse matrix
            
        linGL1(n)
            inputs
                n   scalar determining the size of the matrix for the linearize version
            Output
                eval    1d float vector
    '''

    def GL1(self, x, mu):
        A = self.linGL1(n = len(x) + 1)
        return A @ x + mu * (x - x**3)

    def fGL1(self, **kwargs):
        u = kwargs.get('u')
        n = kwargs.get('n')
        assert type(n) == int, 'integer only'
        assert np.ndim(u) == 1, '1d only'
        
        mu = kwargs.get("mu", np.pi**2)
        A = self.linGL1(n = n)
        vec = mu*u  - (mu /3) * (u ** 3)
        
        return (A @ u + vec)
    
    def linGL1(self, **kwargs):
        n = kwargs.get('n')
        assert type(n) == int, 'integer only'
        
        top = np.full(n - 2, 1)
        mid = np.full(n - 1, -2)
        bot = np.full(n - 2, 1)
        h = 1/(n - 1)
        
        return (h**(-2)) * sp.csr_matrix(sp.diags([ top , mid , bot ] , [1 , 0 , -1]))
    
    def JacGL1(self, **kwargs):
        u = kwargs.get('u')
        n = kwargs.get('n', int(5))
        mu = kwargs.get("mu", np.pi)
        assert type(n) == int, 'integer only'
        # assert np.ndim(u) == 1, '1d only'
        
        A = self.linGL1(n = n)
        
        # top = np.full(n - 2, 1)
        # bot = np.full(n - 2, - 1)
        # B = ((2*h)**(-1)) * sp.csr_matrix(sp.diags([ top , bot ] , [1 , -1]))
        # vec = mu * B @ (1 - u**2)
       
        # ttop = np.full(n - 3, 1)
        # top = np.full(n - 2, - 2)
        # bot = np.full(n - 2, - 2)
        # bbot = np.full(n - 3, - 1)
        # C = ((2*(h**3))**(-1)) * sp.csr_matrix(sp.diags([ ttop, top , bot, bbot ] , [2, 1 , -1, -2]))
        # print(C == B @ A)
        
        # return (B @ A) @ u + vec
        return A + mu * (np.eye(n - 1) - np.diag(u**2))