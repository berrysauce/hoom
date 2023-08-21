# Quickstart

Here's a little script which shows how easy Hoom is to use:

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

As you can see, Hoom is very similar to frameworks like [FastAPI](https://github.com/tiangolo/fastapi). No need for complicated classes with lots of methods. Just use the `@hoom.<<accessory>>` decorator and you're good to go.

Hoom takes over the job of communicating with HomeKit and establishing your function as a HomeKit accessory. You just have to write the code for your accessory.


## Running the script

Start Hoom by running your script, e.g. with:

```bash
python3 my-bridge.py
```

Hoom will start a web server at http://localhost:8553 by default. You can change this by passing the `host` and `port` argument to the `Hoom` class. When visiting the web server you'll see a small UI with the configuation instructions.