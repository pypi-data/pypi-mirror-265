:py:mod:`byma.iteral.nonstationary.Newton`
==========================================

.. py:module:: byma.iteral.nonstationary.Newton


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   byma.iteral.nonstationary.Newton.opts
   byma.iteral.nonstationary.Newton.newton



.. py:function:: opts(interface={}, parameters={}, **kwargs)


.. py:function:: newton(x, f, df, **kwargs)

   Newton iterations.

   Parameters:
       x (array_like): Initial guess for the root.
       f (callable): Function to evaluate the residuals.
       df (callable): Function to evaluate the Jacobian matrix.
       **kwargs: Additional keyword arguments for customization.
           - tol (float): Tolerance for convergence. Default is 1e-8.
           - maxit (int): Maximum number of iterations. Default is 10000.
           - verbose (bool): If True, prints iteration information. Default is True.
           - mode (bool): If True, returns additional iteration information. Default is True.


   Returns:
       tuple: Tuple containing the root and optionally the number of iterations and norm of correction.
              If mode is True, returns (root, iterations, norm_correction), otherwise just returns root.

   Raises:
       ValueError: If the maximum number of iterations or tolerance is not a positive integer.

   Examples:
   >>> # Example 1: Basic usage
   >>> root, iterations, norm_correction = newton(2.0, lambda x: x**2 - 4, lambda x: 2 * x, verbose=True)
   >>> print("Root:", root, "Iterations:", iterations, "Norm of correction:", norm_correction)
       
   >>> # Example 2: Usage with kwargs provided as a dictionary
   >>> kwargs = {'verbose': True, 'tol': 1e-6, 'maxit': 20}
   >>> root, iterations, norm_correction = newton(3.0, lambda x: x**3 - 27, lambda x: 3 * x**2, **kwargs)
   >>> print("Root:", root, "Iterations:", iterations, "Norm of correction:", norm_correction)


