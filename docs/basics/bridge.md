# Bridge

The Bridge is the main part of Hoom. It is responsible for the communication via the HomeKit Accessory Protocol (HAP). It also handles the creation of Accessories and their Services. The Bridge is resembled by the `Hoom` class.

## How to configure the Bridge

The Bridge has a few configuration options, which can be set while initializing the `Hoom` class.

```python
from hoom import Hoom

hoom = Hoom(
    name: "My HomeKit Bridge",
    server: True,
    host: "localhost",
    port: 8553,
    interval: 3
)

hoom.run()
```

## Configuration Options

- **Name**: Set the name of your HomeKit Bridge. This will be displayed in the Apple Home app. Defaults to `Hoom Bridge`.
- **Server**: Set to `True` if you want to enable the web server. This is required if you want to use the web UI. Hoom is capable of running without the web server. Defaults to `True`.
- **Host**: Set the host of the web server. Defaults to `localhost`.
- **Port**: Set the port of the web server. Defaults to `8553`.
- **Interval**: Set the interval in seconds, in which Hoom will check for changes in your accessories. Defaults to `3`.