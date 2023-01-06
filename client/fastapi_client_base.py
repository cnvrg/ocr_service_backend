""" fastapi base client class """
import requests, random
import json
from pydantic import BaseModel
from typing import Optional, List, Dict

from datetime import datetime
import logging
from typing import List
from dataclasses import dataclass, field, asdict, replace
import coloredlogs, logging

clbaselogs = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG, logger=clbaselogs)

    
class base_logger:
    def __init__(self):
        self.locallogger = logging.getLogger(__name__)
        coloredlogs.install(level=logging.DEBUG, logger=self.locallogger) 
        self.locallogger.setLevel(logging.INFO)
    
        logformat = logging.Formatter(fmt="%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
        
        logstream = logging.StreamHandler()
        logstream.setLevel(logging.INFO)
        logstream.setFormatter(logformat)
        self.locallogger.addHandler(logstream)
        
    def get_logger(self):
        return self.locallogger

class base_fastapi_client(base_logger):
    def __init__(self, remote_service_address:str = None, remote_service_port: int = None):
        url, port = remote_service_address, remote_service_port        
        super().__init__()
        self.locallogger.debug("base is called")
        self.url = url  if url is not None else "localhost"
        self.url = 'http://' + self.url
        self.port = port if port is not None else 50051
        self.connection_url = f"{self.url}:{self.port}"
        self.timeout = 30
        self.setup_app_router()
        
    def setup_app_router(self):
        pass
        
    def connect(self):
        """ test connection to service endpoint """
        return requests.get(self.connection_url, timeout=self.timeout)
            
    def makeLocalWorkingDir(self, prefix: str, wdir: str) -> str:
        """local helper function for makring local directory"""
        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        dir_name = f"{wdir}/{prefix}-{timestamp}"

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        return dir_name


class InferenceIn(BaseModel):
    id: int = None
    remote_files: List[str]   
    
class ocr_fastapi_client(base_fastapi_client):

    def setup_app_router(self):
        self.route_extract: set = "extract"


    def get_inference_results_shared(
        self, shared_files: List[str]):
        
        """Request inference on files already present on shared volume"""
        connect_ocr = f"{self.connection_url}/{self.route_extract}"
        payload = InferenceIn(remote_files =  shared_files, id=random.randint(1, 100000))
        req = requests.post(connect_ocr, data = payload.json(), timeout= self.timeout)
        req_results = req.json()["results"]["json_extract_results"]
        return req_results


    def process_shared_files(self, files: List[str]):
        """handle shared files inference request"""
        results_json = self.get_inference_results_shared(files)        
        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"
        self.locallogger.info("----------send request for shared files inference------------")
        
        with open(results_file, "w") as rf:
            rf.write(json.dumps(results_json, indent=4))

        self.locallogger.info(f"-----------received: {results_file} -------------------")

        return results_file

