import os
import logging
import signal
import threading
import colorama
import datetime

# python-HAP imports
from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import *

# FastAPI imports
import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from .accessory_types import *


# ---------------------------------
# CONFIGURATION
# ---------------------------------


# configure logging
logging.basicConfig(level=logging.INFO, format="[Hoom] %(message)s")

try:
    # read version from pyproject.toml
    with open("./pyproject.toml", "r") as f:
        for line in f.readlines():
            if "version" in line:
                version = line.split("=")[1].strip().replace('"', '')
except Exception as e:
    logging.error(f"Could not read version from pyproject.toml: {e}")
    version = "0.0.0"
    
year = datetime.datetime.now().year
app = FastAPI(
    title="Hoom",
    version=version,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)
router = InferringRouter()
templates = Jinja2Templates(directory="hoom/pages")

# mount static assets for web UI
app.mount("/assets", StaticFiles(directory="hoom/pages/assets"), name="assets")

# disable standard uvicorn logging
uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_error.disabled = True
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

# global variables
bridge = None
xhm_uri = None
pin_code = None


# ---------------------------------
# MAIN FUCTIONS
# ---------------------------------


def init_accessory(driver: AccessoryDriver):
    global xhm_uri
    global pin_code
    global bridge
    
    # do this here to avoid double initialization
    driver.add_accessory(accessory=bridge)
    
    # this as well...
    xhm_uri = Accessory.xhm_uri(driver.accessory)
    pin_code = str(driver.state.pincode, "utf-8")
    
    return

            
# ---------------------------------
# MAIN CLASSES
# ---------------------------------


@cbv(router)
class Hoom():
    def __init__(self, name: str = "Hoom Bridge", server: bool = True, host: str = "localhost", port: int = 8553) -> None:
        """
        Initializes the Hoom Bridge.

        Args:
            name (str, optional): Name for your Bride, displayed in the Apple Home app (Default: "Hoom Bridge")
            server (bool, optional): Defines whether the web server should be started (Default: True)
            host (str, optional): Defines the host for the web server (Default: "localhost")
            port (int, optional): Defines the port for the web server (Default: 8553)
        """
        
        global bridge
        global refresh_interval # is this possible in a different way else?
        
        self.name = name # bridge name
        self.server = server # run FastAPI server?
        self.host = host # server host
        self.port = port # server port
        
        # do this here to avoid double initialization
        self.driver = AccessoryDriver(port=51826, persist_file="hoom_bridge.state")
        bridge = Bridge(self.driver, self.name)
        bridge.set_info_service(firmware_revision=version, manufacturer="Hoom", model="Hoom Bridge", serial_number="0000-0000-0000-0001")
        
        
    def run(self):
        """
        Starts the Hoom Bridge.
        
        Args:
            None
        """
             
        print(colorama.Fore.BLUE + f"\n---------------------------" + colorama.Style.RESET_ALL)  
        print(colorama.Fore.BLUE + f"        hoom v{version}    " + colorama.Style.RESET_ALL)
        print(colorama.Fore.BLUE + f"---------------------------\n" + colorama.Style.RESET_ALL)  
        
        logging.info("Starting Hoom Bridge...")
        signal.signal(signal.SIGTERM, self.driver.signal_handler)
        
        def run_server():
            app.include_router(router)
            uvicorn.run(app, host=self.host, port=self.port)
    
        if self.server:
            bridge_thread = threading.Thread(target=self.driver.start, args=())
            server_thread = threading.Thread(target=run_server, args=())
        
        try:
            if self.server:
                # start threads
                bridge_thread.start()
                server_thread.start()
            
                print("...... " + colorama.Fore.GREEN + "Hoom Bridge is running. Stop with Ctrl+C." + "\n       Configure at http://localhost:8553" + colorama.Style.RESET_ALL)
            
                # join threads
                bridge_thread.join()
                server_thread.join()
            else:
                self.driver.start()
                print("...... " + colorama.Fore.GREEN + "Hoom Bridge is running. Stop with Ctrl+C." + colorama.Style.RESET_ALL + "\n       Configure at http://localhost:8553 \n")
        except KeyboardInterrupt:
            print("\n...... " + colorama.Fore.RED + "Stopping Hoom Bridge..." + colorama.Style.RESET_ALL)
        
            # stop HAP driver
            self.driver.stop()
            
            # exit process
            os._exit(0)
    
    
    # ---------------------------------
    # ACCESSORY DECORATORS
    # ---------------------------------
    
    
    def lightbulb(self, accessory_name: str, dimmable: bool = False, colorable: bool = False, *args, **kwargs):
        """
        Creates a Lightbulb accessory from the given function.

        Args:
            accessory_name (str): Name for your accessory
            dimmable (bool, optional): Defines whether the lightbulb is dimmable (Default: False)
            colorable (bool, optional): Defines whether the lightbulb is colorable (Default: False)
        """
        
        # initialize accessory
        init_accessory(self.driver)
        
        def decorator(func):
            accessory_instance = Lightbulb(self.driver, accessory_name, *args, dimmable=dimmable, colorable=colorable, **kwargs)
            accessory_instance.callback_func = func
            bridge.add_accessory(accessory_instance)
        
            logging.info(colorama.Fore.BLUE + f"Initialized accessory '{accessory_name}'" + colorama.Style.RESET_ALL)   
            return func

        return decorator
    
    
    def switch(self, accessory_name: str, *args, **kwargs):
        """
        Creates a Switch accessory from the given function.

        Args:
            accessory_name (str): Name for your accessory
        """
        
        # initialize accessory
        init_accessory(self.driver)
        
        def decorator(func):
            accessory_instance = Switch(self.driver, accessory_name, *args, **kwargs)
            accessory_instance.callback_func = func
            bridge.add_accessory(accessory_instance)
        
            logging.info(colorama.Fore.BLUE + f"Initialized accessory '{accessory_name}'" + colorama.Style.RESET_ALL)   
            return func

        return decorator
    
    
    def temperature_sensor(self, accessory_name: str, *args, interval: int = 3, **kwargs):
        """
        Creates a Temperature Sensor accessory from the given function.

        Args:
            accessory_name (str): Name for your accessory
            interval (int): Refresh interval in seconds (Default: 3)
        """
        
        # initialize accessory
        init_accessory(self.driver)
        
        def decorator(func):
            accessory_instance = TemperatureSensor(self.driver, accessory_name, *args, interval=interval, **kwargs)
            accessory_instance.callback_func = func
            bridge.add_accessory(accessory_instance)
        
            logging.info(colorama.Fore.BLUE + f"Initialized accessory '{accessory_name}'" + colorama.Style.RESET_ALL)   
            return func

        return decorator
    
    
    # ---------------------------------
    # FASTAPI ROUTES
    # ---------------------------------


    @router.get("/")
    async def get_root(self, request: Request):
        return templates.TemplateResponse("connect.html", {
            "request": request,
            "bridge_name": self.name,
            "code": pin_code,
            "qrcode": xhm_uri,
            "version": version,
            "year": year
        })