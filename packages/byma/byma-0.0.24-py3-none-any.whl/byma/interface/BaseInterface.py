import numpy as np 


class BaseInterface:
    '''Defines a base interface'''

    def __init__(self, default_cls, params=None, interface=None, **kwargs):
        self.cls = default_cls
        self.params = params or {}
        self.interface = interface or {}
        self.kwargs = kwargs

    def opts(self, usr_interface=None, usr_params=None, **kwargs):
        interface = self.interface.copy()
        params = self.params.copy()
        
        if usr_interface is not None:
            interface.update(usr_interface)

        if usr_params is not None:
            params.update(usr_params)

        # Construct instance of default class with the updated interface and parameters
        default_instance = self.cls(interface = interface, parameters = params)
        interface_default = default_instance.interface.copy()
        params_default = default_instance.parameters.copy()

        interface_default.update(kwargs)
        params_default.update(kwargs)

        return interface_default, params_default