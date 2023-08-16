# Lightbulb

The `Lightbulb` accessory type is a simple accessory that can be turned on or off. It returns a `Lightbulb.Response` object which contains the state of the lightbulb, set by HomeKit. 

In contrast to the `Switch` accessory, the `Lightbulb` accessory can also be dimmed and set to a certain hue & saturation.

```python
from hoom import Hoom
from hoom.accessory_types import Lightbulb

hoom = Hoom()

@hoom.accessory("Lamp", Lightbulb, dimable=True, colorable=True)
def lamp(response: Lightbulb.Response):
    if response.on:
        print("Lamp is now on")
        # available when dimable=True
        print("Brightness: " + str(response.brightness))
        # available when colorable=True
        print("Hue: " + str(response.hue))
        print("Saturation: " + str(response.saturation))
    else:
        print("Lamp is now off")
        
    return

hoom.run()
```

As with all other accessories, you can define your own logic on how to turn on or off the lightbulb. 


## `Lightbulb.Response`

The `Lightbulb.Response` object contains the following attributes:

- `on` - A boolean value indicating whether the lightbulb is turned on or off.

If you set `dimable=True` in the decorator, the following attributes are also available:

- `brightness` - An integer value between `0` and `100` indicating the brightness of the lightbulb.

If you set `colorable=True` in the decorator, the following attributes are also available:

- `hue` - An integer value between `0` and `360` indicating the hue of the lightbulb.
- `saturation` - An integer value between `0` and `100` indicating the saturation of the lightbulb.
