# Responses

Responses are a way to receive and send data to and from your Hoom Bridge in a standardised way.


## How to use Responses

You can receive data by defining a function with a response as an argument. The response will be passed to the function when the accessory is triggered.

```python
@hoom.lightbulb("Light")
def light(response: Lightbulb.Response):
    print(response.on) # boolean value
    ...

    return
```

In this case, we've set the `response` argument of the `light` function to be of the type `Lightbulb.Response`. This means that the `response` object will have the attributes of the `Lightbulb.Response` object, wich are passed on everytime the accessory is triggered, e.g. when it's turned on or off.

We can also return data to the Hoom Bridge by returning a response object from the function.

```python
from random import randint
...

@hoom.temperature_sensor("Temperature Sensor")
def temperature_sensor(response: TemperatureSensor.Response):
    ...
    new_temp = randint(10, 30)

    return TemperatureSensor.Response(temp=new_temp)
```

In this case, we're setting the `temp` attribute of the `TemperatureSensor.Response` object to a random value between 10 and 30. This data will then be sent to the Hoom Bridge and then to HomeKit.


## Response types & attributes

You can learn more about the individual response types in the "Accessories" section of these docs.