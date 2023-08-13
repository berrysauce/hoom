from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH

class Switch(Accessory):
    category = CATEGORY_SWITCH
    interval = None # ignore
    
    class Response():
        state: bool
        
        def __init__(self, state: bool):
            self.state = state

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_switch = self.add_preload_service("Switch")
        self.char_on = serv_switch.configure_char(
            "On", setter_callback=self.set_switch)
        
        self.callback_func = None
        
    def set_switch(self, value):        
        if self.callback_func is not None:
            self.callback_func(self.Response(state=value))