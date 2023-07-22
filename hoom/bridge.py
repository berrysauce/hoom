import os
import logging
import signal
import threading
import colorama

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


# ---------------------------------
# CONFIGURATION
# ---------------------------------


version = "pre-0.1.2" 
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

# configure logging
logging.basicConfig(level=logging.INFO, format="[Hoom] %(message)s")

# disable standard uvicorn logging
uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_error.disabled = True
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

# read version from pyproject.toml
with open("./pyproject.toml", "r") as f:
    for line in f.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', '')

# global variables
xhm_uri = None
pin_code = None

            
# ---------------------------------
# MAIN CLASSES
# ---------------------------------


@cbv(router)
class Hoom():
    def __init__(self, name: str = "Hoom Bridge", server: bool = True, host: str = "localhost", port: int = 8553, interval: int = 3) -> None:
        global refresh_interval # is this possible in a different way else?
        
        self.name = name # bridge name
        self.server = server # run FastAPI server?
        self.host = host # server host
        self.port = port # server port
        self.interval = interval # refresh interval for accessories that support it (in seconds)
        
        self.driver = AccessoryDriver(port=51826, persist_file="hoom_bridge.state")
        
    def run(self):       
        print(
            colorama.Fore.BLUE + f"""
            HH   HH                           
            HH   HH  oooo   oooo  mm mm mmmm  
            HHHHHHH oo  oo oo  oo mmm  mm  mm 
            HH   HH oo  oo oo  oo mmm  mm  mm 
            HH   HH  oooo   oooo  mmm  mm  mm
            
            ---------------------------------
            
            Version: {version}
            Copyright 2023 foerstal.com
            Made possible by HAP-python
            
            ---------------------------------
            """ + colorama.Style.RESET_ALL
        )
        
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
            
                print("...... " + colorama.Fore.GREEN + "Hoom Bridge is running. Stop with Ctrl+C." + colorama.Style.RESET_ALL + "\n       Configure at http://localhost:8553")
            
                # join threads
                bridge_thread.join()
                server_thread.join()
            else:
                self.driver.start()
                print("...... " + colorama.Fore.GREEN + "Hoom Bridge is running. Stop with Ctrl+C." + colorama.Style.RESET_ALL + "\n       Configure at http://localhost:8553\n")
        except KeyboardInterrupt:
            print("\n...... " + colorama.Fore.RED + "Stopping Hoom Bridge..." + colorama.Style.RESET_ALL)
        
            # stop HAP driver
            self.driver.stop()
            
            # exit process
            os._exit(0)
    
        
    def accessory(self, accessory_name: str, accessory_type: classmethod):
        global xhm_uri
        global pin_code  
        
        # do this here to avoid double initialization
        bridge = Bridge(self.driver, self.name)
        bridge.set_info_service(firmware_revision=version, manufacturer="Foerstal", model="Hoom Bridge", serial_number="0000-0000-0000-0001")
        self.driver.add_accessory(accessory=bridge)
        # this as well...
        xhm_uri = Accessory.xhm_uri(self.driver.accessory)
        pin_code = str(self.driver.state.pincode, "utf-8")
        
        def decorator(func):
            accessory_instance = accessory_type(self.driver, accessory_name)
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
            "version": version
        })