# Switch

The switch accessory type is the simplest accessory that can be turned on or off. It returns a `Switch.Response` object which contains the state of the switch, set by HomeKit.

```python
from hoom import Hoom
from hoom.accessory_types import Switch

hoom = Hoom()

@hoom.accessory("Switch", Switch)
def switch(response: Switch.Response):
    if response.on: # boolean value
        print("Switch is now on")
    else:
        print("Switch is now off")
        
    return

hoom.run()
```

As with all other accessories, you can define your own logic on how to turn on or off the switch. 


## `Switch.Response`

The `Switch.Response` object contains the following attributes:

- `on` - A boolean value indicating whether the switch is turned on or off.

