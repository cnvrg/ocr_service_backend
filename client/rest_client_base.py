""" rest base client class """
import requests
import random
import json
import logging
import os
import shutil
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from dataclasses import dataclass, field, asdict, replace
import coloredlogs, logging


class base_logger:
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


class base_rest_client(base_logger):
    def __init__(
        self, remote_service_address: str = None, remote_service_port: int = None
    ):
        url, port = remote_service_address, remote_service_port
        super().__init__()
        self.locallogger.debug("base is called")
        self.url = url if url is not None else "localhost"
        self.url = "http://" + self.url
        self.port = port if port is not None else 50051
        self.connection_url = f"{self.url}:{self.port}"
        self.timeout = 30
        self.setup_app_router()

    def setup_app_router(self):
        pass

    def connect(self):
        """test connection to service endpoint"""
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


class OcrRestClient(base_rest_client):
    """handle ocr rest connections"""

    def setup_app_router(self):
        self.route_extract: str = "ocr/extract"

    def get_infrance_fileUpload_jsonResults(self, filename: str):
        """upload a single file for text extraction, response is json body"""
        self.locallogger.info(f" sent {filename} for text extraction ")
        connect_ocr = f"{self.connection_url}/{self.route_extract}"
        files = {"file": (open(filename, "rb"))}

        req = requests.post(connect_ocr, files=files, stream=True, timeout=self.timeout)
        return req.text

    def get_infrance_fileUpload(self, filename: str):
        """upload a single file for text extraction, response is file"""

        self.locallogger.info(f" sent {filename} for text extraction ")
        connect_ocr = f"{self.connection_url}/{self.route_extract}/file"
        files = {"file": (open(filename, "rb"))}

        req = requests.post(connect_ocr, files=files, stream=True, timeout=self.timeout)

        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"
        with open(results_file, "wb") as rf:
            for chunk in req.iter_content(chunk_size=128):
                rf.write(chunk)

        self.locallogger.info(f"received results! Saved to file {results_file}")

        return results_file

    def get_infrance_manyFilesUpload(self, fileList: List[str]):
        """upload many files for text extraction processing"""

        self.locallogger.info(f" sent {fileList} for text extraction ")
        connect_ocr = f"{self.connection_url}/{self.route_extract}/files"
        # files = {"file": (open(filename, "rb"))}
        files = [("files", (open(fitem, "rb"))) for n, fitem in enumerate(fileList)]
        # files = {f"files": (open(fitem, "rb")) for n, fitem in enumerate(fileList)}

        req = requests.post(connect_ocr, files=files, stream=True)

        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"
        with open(results_file, "wb") as rf:
            for chunk in req.iter_content(chunk_size=128):
                rf.write(chunk)

        self.locallogger.info(f"received results! Saved to file {results_file}")

        return results_file
