
import numpy as np


def krylov_basis(A, b, m):
    """
    Generates a numerical basis for the m-dimensional Krylov subspace.
    
    """
    n = A.shape[0]
    
    result = np.empty((n, m), dtype=np.float64)
    
    result[:, 0] = b
    
    for index in range(1, m):
        result[:, index] = A @ result[:, index - 1]
        
    return result


