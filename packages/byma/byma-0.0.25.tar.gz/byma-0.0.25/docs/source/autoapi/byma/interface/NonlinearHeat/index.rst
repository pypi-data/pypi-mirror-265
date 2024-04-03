:py:mod:`byma.interface.NonlinearHeat`
======================================

.. py:module:: byma.interface.NonlinearHeat


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   byma.interface.NonlinearHeat.NonlinearHeat




.. py:class:: NonlinearHeat


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

   .. py:method:: GL1(x, mu)


   .. py:method:: fGL1(**kwargs)


   .. py:method:: linGL1(**kwargs)


   .. py:method:: JacGL1(**kwargs)



