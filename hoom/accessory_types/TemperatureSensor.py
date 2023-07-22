from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SENSOR

class TemperatureSensor(Accessory): 
    category = CATEGORY_SENSOR
    
    class Response():
        temp: float
        
        def __init__(self, temp: float):
            self.temp = temp

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        serv_temp = self.add_preload_service("TemperatureSensor")
        self.char_temp = serv_temp.configure_char("CurrentTemperature")
        
        self.callback_func = None
        
    @Accessory.run_at_interval(3)
    async def run(self):
        if self.callback_func is not None:
            temp = self.callback_func(self.Response(temp=self.char_temp.value)).temp
            self.char_temp.set_value(temp)