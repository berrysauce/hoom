# Temperature Sensor

The `TemperatureSensor` accessory type is an accessory, that provides data to HomeKit, rather than receive it. It returns a `TemperatureSensor.Response` object which contains the previous set temperature. 

Since the `TemperatureSensor` accessory supplies data, you can optionally set an interval for the polling rate of the accessory in seconds. This can be especially helpful if you receive data from an external source, like an API, and you're required to comply with rate limits.

```python
from hoom import Hoom
from hoom.accessory_types import TemperatureSensor

from random import randint

hoom = Hoom()

@hoom.temperature_sensor("Standard Temperature Sensor", interval=10)
def standard_temperature_sensor(response: TemperatureSensor.Response):
    print("Previous Temperature: " + str(response.temp))
    new_temp = randint(10, 30)

    return TemperatureSensor.Response(temp=new_temp)

hoom.run()
```

As with all other accessories, you can define your own logic on how to receive the temperature.


## `TemperatureSensor.Response`

The `TemperatureSensor.Response` object contains the following attributes:

- `temp` - A float value indicating the temperature.