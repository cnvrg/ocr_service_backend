import coloredlogs, logging, os
from typing import Optional, List, Dict
from datetime import datetime

class BaseLogger:
    def __init__(self):
        self.locallogger = logging.getLogger(__name__)
        coloredlogs.install(level=logging.DEBUG, logger=self.locallogger)
        self.locallogger.setLevel(logging.INFO)

        logformat = logging.Formatter(
            fmt="%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S"
        )

        logstream = logging.StreamHandler()
        logstream.setLevel(logging.INFO)
        logstream.setFormatter(logformat)
        self.locallogger.addHandler(logstream)

    def get_logger(self):
        return self.locallogger
    
    def makeLocalWorkingDir(self, prefix: str, wdir: str) -> str:
        """local helper function for makring local directory"""
        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        dir_name = f"{wdir}/{prefix}-{timestamp}"

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        return dir_name


class BaseClient(BaseLogger):
    def __init__(self, 
                 remote_service_address: str = "localhost",
                 remote_service_port: str = None):
        super().__init__()
        self.locallogger.debug("base is called")
        self.remote_service_address = remote_service_address
        self.remote_service_port = remote_service_port
        
    def get_inference_fileUpload_jsonResults(self, filename: str):
        pass
    
    def get_inference_fileUpload(self, filename: str):
        pass
    
    def get_inference_manyFilesUpload(self, file_list: List[str]):
        pass