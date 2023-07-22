from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB

class Lightbulb(Accessory):
    category = CATEGORY_LIGHTBULB
    interval = None # ignore
    
    class Response():
        state: bool
        
        def __init__(self, state: bool):
            self.state = state
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_light = self.add_preload_service("Lightbulb")
        self.char_on = serv_light.configure_char(
            "On", setter_callback=self.set_bulb)
        
        self.callback_func = None

    def set_bulb(self, value):        
        if self.callback_func is not None:
            self.callback_func(self.Response(state=value))