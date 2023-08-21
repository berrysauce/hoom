# Switch

The switch accessory type is the simplest accessory that can be turned on or off. It returns a `Switch.Response` object which contains the state of the switch, set by HomeKit.

```python
from hoom import Hoom
from hoom.accessory_types import Switch

hoom = Hoom()

@hoom.switch("Switch ")
def switch(response: Switch.Response):
    if response.on:
        print("Switch is now on")
    else:
        print("Switch is now off")
        
    return

hoom.run()
```

As with all other accessories, you can define your own logic on what happens, when you turn on or off the switch. 


## `Switch.Response`

The `Switch.Response` object contains the following attributes:

- `on` - A boolean value indicating whether the switch is turned on or off.

