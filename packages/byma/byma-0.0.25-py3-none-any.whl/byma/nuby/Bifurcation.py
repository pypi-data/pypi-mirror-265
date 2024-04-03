
class Bifurcation:
    
    '''Defines default options for the Bifurcation package'''

    def __init__(self, interface=None, parameters=None):
        self.interface = {}
        self.parameters = {'maxit': 1e4, 'tol': 1e-4, 'method': 'general'}
        
        if interface:
            self.interface.update(interface)
        if parameters:
            self.parameters.update(parameters)