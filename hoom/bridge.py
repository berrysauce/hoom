import logging
import signal

# python-HAP imports
from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import (CATEGORY_LIGHTBULB,
                         CATEGORY_SENSOR)


# read version from pyproject.toml
with open("./pyproject.toml", "r") as f:
    for line in f.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', '')


class Hoom():
    def __init__(self, name: str = "Hoom Bridge", server: bool = True, host: str = "localhost", port: int = 8553, interval: int = 3) -> None:
        global refresh_interval # is this possible in a different way else?
        
        self.name = name # bridge name
        self.server = server # run FastAPI server?
        self.host = host # server host
        self.port = port # server port
        self.interval = interval # refresh interval for accessories that support it (in seconds)
        
        self.driver = AccessoryDriver(port=51826, persist_file="hoom_package_bridge.state")
        self.bridge = Bridge(self.driver, self.name)
        self.bridge.set_info_service(firmware_revision=version, manufacturer="Foerstal", model="Hoom Bridge", serial_number="0000-0000-0000-0001")
        
    def run(self):
        print("Starting Hoom...")
        self.driver.add_accessory(accessory=self.bridge)
        signal.signal(signal.SIGTERM, self.driver.signal_handler)
        self.driver.start()
        
    def accessory(self, accessory_name: str, accessory_type: classmethod):
        def decorator(func):
            print(f"Adding accessory '{accessory_name}'...")
            accessory_instance = accessory_type(self.driver, accessory_name)
            accessory_instance.callback_func = func
            self.bridge.add_accessory(accessory_instance)        
            return func

        return decorator