<img src="https://bcdn.berrysauce.me/shared/hoom-banner-modified.png">
<img src="https://bcdn.berrysauce.me/shared/hoom-ad-modified.png">

<br>

# 🏡 Hoom
Build your own HomeKit Bridge & Accessories with Hoom

### ✨ Features
- [x] HomeKit Bridge
- [x] Minimalist Web UI
- [x] Create custom HomeKit Accessories with function decorators
- [x] Customizable
- [x] Easy to use

### 📦 Installation
You can easily install Hoom using pip:

```bash
pip install hoom
```

> **Note**: Hoom requires Python 3.8 or higher

### How to use
Here's a demo script which shows how easy Hoom is to use:

```python
from hoom import Hoom
from hoom.accessory_types import Lightbulb

hoom = Hoom(name="Hoom Bridge")

@hoom.accessory("Lamp", Lightbulb)
def lamp(response: Lightbulb.Response):
    if response.state:
        print("Lamp is now on")
    else:
        print("Lamp is now off")
        
    return

hoom.run()
```

As you can see, Hoom is very similar to frameworks like FastAPI. No need for complicated classes with lots of methods. Just use the `@hoom.accessory` decorator and you're good to go.

### 📣 Credits
A special thanks goes out to these Python packages/frameworks and their authors:

- [HAP-python](https://github.com/ikalchev/HAP-python) - Hoom wouldn't be possible without this HomeKit Accessory Protocol implementation by [Ivan Kalchev](https://github.com/ikalchev)
- [FastAPI](https://github.com/tiangolo/fastapi) - Hoom uses FastAPI by [Sebastián Ramírez](https://github.com/tiangolo) for its web server & UI and is heavily inspired by it
