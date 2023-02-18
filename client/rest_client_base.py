""" rest base client class """
import requests
import json
import os, shutil
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from dataclasses import dataclass, field, asdict, replace
from base_logger import BaseClient


class InferenceIn(BaseModel):
    id: int = None
    remote_files: List[str]


class OcrRestClient(BaseClient):
    """handle ocr rest connections"""

    def __init__(self, remote_service_address, remote_service_port):
        super().__init__(remote_service_address, remote_service_port)
        self.url = "http://" + self.remote_service_address
        self.port = (
            self.remote_service_port if self.remote_service_port is not None else 40051
        )
        self.connection_url = f"{self.url}:{self.port}"
        self.timeout = 500
        self.setup_app_router()

    def setup_app_router(self):
        self.route_extract: str = "ocr/extract"

    def base_connect(self):
        """test connection to service endpoint"""
        return requests.get(self.connection_url, timeout=self.timeout)

    def get_inference_fileUpload_jsonResults(self, filename: str):
        """upload a single file for text extraction, response is json body"""
        self.locallogger.info(f" sent {filename} for text extraction ")
        connect_ocr = f"{self.connection_url}/{self.route_extract}"

        files = {"file": (open(filename, "rb"))}
        req = requests.post(connect_ocr, files=files, stream=True, timeout=self.timeout)
        files["file"].close()  # close files after uploading

        return req.text

    def get_inference_fileUpload(self, filename: str):
        """upload a single file for text extraction, response is file"""

        self.locallogger.info(f" sent {filename} for text extraction ")
        connect_ocr = f"{self.connection_url}/{self.route_extract}/file"

        files = {"file": (open(filename, "rb"))}
        req = requests.post(connect_ocr, files=files, stream=True, timeout=self.timeout)
        files["file"].close()  # close files after uploading

        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"
        with open(results_file, "wb") as rf:
            for chunk in req.iter_content(chunk_size=128):
                rf.write(chunk)

        self.locallogger.info(f"received results! Saved to file {results_file}")

        return results_file

    def get_inference_manyFilesUpload(self, file_list: List[str]):
        """upload many files for text extraction processing"""

        self.locallogger.info(f" sent {file_list} for text extraction ")
        connect_ocr = f"{self.connection_url}/{self.route_extract}/files"

        files = [("files", (open(fitem, "rb"))) for n, fitem in enumerate(file_list)]
        req = requests.post(connect_ocr, files=files, stream=True)
        [f.close() for (fname, f) in files]  # close files after uploading

        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"
        with open(results_file, "wb") as rf:
            for chunk in req.iter_content(chunk_size=128):
                rf.write(chunk)

        self.locallogger.info(f"received results! Saved to file {results_file}")

        return results_file
