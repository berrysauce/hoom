from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SENSOR

import time

from hoom.exceptions import InvalidArgumentError

class TemperatureSensor(Accessory): 
    category = CATEGORY_SENSOR
    interval: int
    
    class Response():
        temp: float
        
        def __init__(self, temp: float):
            self.temp = temp

    def __init__(self, *args, interval: int = 3, **kwargs):
        self.interval = interval
        
        try:
            super().__init__(*args, **kwargs)   
        except TypeError:
            raise InvalidArgumentError(f"Invalid argument(s) passed to the Accessory class: {kwargs}")
        
        serv_temp = self.add_preload_service("TemperatureSensor")
        self.char_temp = serv_temp.configure_char("CurrentTemperature")
        
        self.callback_func = None
    
    # @Accessory.run_at_interval(interval) <- Doesn't work
    def run(self):        
        # wait interval
        while not self.driver.stop_event.wait(self.interval):
            if self.callback_func is not None:
                temp = self.callback_func(self.Response(temp=self.char_temp.value)).temp
                self.char_temp.set_value(temp)
        return