<img src="https://bcdn.berrysauce.me/shared/hoom-banner-modified.png">

<br>

<h1 align="center">Hoom</h1>
<p align="center">Build your own HomeKit Bridge & Accessories with Hoom</p>
<p align="center">
    <img alt="CodeQL Status" src=https://github.com/berrysauce/hoom/actions/workflows/github-code-scanning/codeql/badge.svg>
    <img alt="PyPi Publishing Status" src=https://github.com/berrysauce/hoom/actions/workflows/python-publish.yml/badge.svg>
    <img alt="PyPi Python Versions" src=https://img.shields.io/pypi/pyversions/hoom>
    <img alt="PyPi Package Downloads" src=https://img.shields.io/pypi/dm/hoom?color=blue>
</p>

<br>

> 🚧 **Please note**: Hoom is still under development. It is not recommended at this point, to use Hoom in a production environment.

<br>

## ✨ Features
- [x] HomeKit Bridge
- [x] Minimalist Web UI
- [x] Create custom HomeKit Accessories with function decorators
- [x] Customizable
- [x] Easy to use

<br>

## 📦 Installation
Hoom is available on [PyPi](https://pypi.org/project/hoom/). You can easily install it using pip:

```bash
pip install hoom
```

> **Note**: Hoom requires Python 3.8 or higher

<br>

## 🚀 Getting started
Here's a demo script which shows how easy Hoom is to use:

```python
from hoom import Hoom
from hoom.accessory_types import Lightbulb

hoom = Hoom()

@hoom.accessory("Lamp", Lightbulb)
def lamp(response: Lightbulb.Response):
    if response.state: # either True or False
        print("Lamp is now on")
    else:
        print("Lamp is now off")
        
    return

hoom.run()
```

As you can see, Hoom is very similar to frameworks like FastAPI. No need for complicated classes with lots of methods. Just use the `@hoom.accessory` decorator and you're good to go.

<br>

## 📣 Credits
A special thanks goes out to these Python packages/frameworks and their authors:

- [HAP-python](https://github.com/ikalchev/HAP-python) - Hoom wouldn't be possible without this HomeKit Accessory Protocol implementation by [Ivan Kalchev](https://github.com/ikalchev)
- [FastAPI](https://github.com/tiangolo/fastapi) - Hoom uses FastAPI by [Sebastián Ramírez](https://github.com/tiangolo) for its web server & UI and is heavily inspired by it
