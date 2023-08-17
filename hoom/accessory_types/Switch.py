from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH

from hoom.exceptions import InvalidArgumentError

class Switch(Accessory):
    category = CATEGORY_SWITCH
    
    class Response():
        on: bool
        
        def __init__(self, on: bool):
            self.on = on

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)   
        except TypeError:
            raise InvalidArgumentError(f"Invalid argument(s) passed to the Accessory class: {kwargs}")

        serv_switch = self.add_preload_service("Switch")
        
        self.char_on = serv_switch.configure_char("On", setter_callback=self.set_switch)
        
        self.callback_func = None
        
    def set_switch(self, value):        
        if self.callback_func is not None:
            self.callback_func(self.Response(on=value))