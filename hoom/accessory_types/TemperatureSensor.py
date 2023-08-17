from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SENSOR

from hoom.exceptions import InvalidArgumentError

class TemperatureSensor(Accessory): 
    category = CATEGORY_SENSOR
    interval: int = 3
    
    class Response():
        temp: float
        
        def __init__(self, temp: float):
            self.temp = temp

    def __init__(self, *args, **kwargs):
        # remove interval from kwargs
        # so it doesn't get passed to Accessory with super().__init__()
        try:
            self.interval = kwargs["interval"]
            del kwargs["interval"]  
        except KeyError:
            pass
        
        try:
            super().__init__(*args, **kwargs)   
        except TypeError:
            raise InvalidArgumentError(f"Invalid argument(s) passed to the Accessory class: {kwargs}")
        
        serv_temp = self.add_preload_service("TemperatureSensor")
        self.char_temp = serv_temp.configure_char("CurrentTemperature")
        
        self.callback_func = None
        
    @Accessory.run_at_interval(interval)
    async def run(self):
        if self.callback_func is not None:
            temp = self.callback_func(self.Response(temp=self.char_temp.value)).temp
            self.char_temp.set_value(temp)