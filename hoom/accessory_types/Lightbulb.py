from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB

class Lightbulb(Accessory):
    category = CATEGORY_LIGHTBULB
    dimable: bool = False
    colorable: bool = False
    
    class Response():
        on: bool
        brightness: int = None
        hue: str = None
        saturation: int = None
        
        def __init__(self, on: bool, brightness: int = None, hue: int = None, saturation: int = None):
            self.on = on
            self.brightness = brightness
            self.hue = hue
            self.saturation = saturation

    def __init__(self, *args, **kwargs): 
        
        # remove dimable and colorable from kwargs 
        # so they don't get passed to Accessory with super().__init__()
        try:
            self.dimable = kwargs["dimable"]
            del kwargs["dimable"]  
        except KeyError:
            pass
        
        try:
            self.colorable = kwargs["colorable"]    
            del kwargs["colorable"]
        except KeyError:
            pass
        
        super().__init__(*args, **kwargs)   

        serv_light = self.add_preload_service("Lightbulb", chars=["On", "Brightness", "Hue", "Saturation"])
        
        self.char_on = serv_light.configure_char("On", setter_callback=self.set_bulb)
        
        if self.dimable:
            self.char_brightness = serv_light.configure_char("Brightness", setter_callback=self.set_bulb)
        if self.colorable:
            self.char_hue = serv_light.configure_char("Hue", setter_callback=self.set_bulb)
            self.char_saturation = serv_light.configure_char("Saturation", setter_callback=self.set_bulb)
        
        self.callback_func = None

    def set_bulb(self, value):        
        if self.callback_func is not None:
            brightness = None
            hue = None
            saturation = None
            
            if self.dimable:
                brightness = self.char_brightness.value
            if self.colorable:
                hue = self.char_hue.value
                saturation = self.char_saturation.value
                
            self.callback_func(self.Response(on=self.char_on.value, brightness=brightness, hue=hue, saturation=saturation))