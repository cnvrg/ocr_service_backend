""" ocrservice server functiona """
from concurrent import futures
import coloredlogs, logging
import os
from datetime import datetime
import urllib.request
import requests
from typing import List, Tuple
import json

from inference.predict import predict
from signal import signal, SIGTERM, SIGINT
import time
import grpc
import ocrservice_pb2
import ocrservice_pb2_grpc
import s3connect_pb2
import s3connect_pb2_grpc

ocrlogs = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG, logger=ocrlogs)

def get_logfile_path(logfile_name:str) -> str:
    logdir: str = os.path.dirname(os.path.abspath(__file__))
    return  f"{logdir}/../logs/{logfile_name}"

def makeLocalWorkingDir(prefix="ocrResults", wdir="/tmp") -> str:
    """local helper function for makring local directory"""
    timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    dir_name = f"{wdir}/{prefix}-{timestamp}"

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    return dir_name


def get_s3files(s3req: ocrservice_pb2.S3request) -> Tuple[int, List[str]]:
    """s3connect client for fetching files from s3 clounds"""
    # with grpc.insecure_channel("localhost:50051") as channel:
    local_server_port = os.environ.get('LOCAL_SERVER_PORT')
    s3_service_address = os.environ.get('S3_SERVICE_ADDRESS')
    if local_server_port is None: 
        local_server_port = "50051"

    if s3_service_address is None:
        #print("Need S3_SERVICE_ADDRESS")
        ocrlogs.error("Need S3_SERVICE_ADDRESS")
        """ raise exception / return error """ 

    with grpc.insecure_channel(f"{s3_service_address}:{local_server_port}") as channel:
        stub = s3connect_pb2_grpc.s3connectStub(channel)

        file_path = makeLocalWorkingDir(prefix="s3files", wdir="/tmp")
        files: List[str] = []
        for res in stub.GetFiles(s3req):
            if res.filename:
                filename = f"{file_path}/{res.filename}"
                files.append(filename)
            else:
                with open(filename, "ab") as rf:
                    rf.write(res.data)

    #print(f"downloaded S3 files: {files}")
    ocrlogs.info(f"downloaded S3 files: {files}")
    status: int = 0
    # time.sleep(2)
    return status, files


def get_url_file(urls: List[str]) -> Tuple[int, List[str]]:
    """download puplic url file directly"""

    files: List[str] = []
    download_dir = makeLocalWorkingDir(prefix="httpDownload", wdir="/tmp")
    for url in urls:
        results = requests.get(url=url, stream=True, timeout=20)

        if results.status_code == requests.codes.ok:
            status = 0
        else:
            status = 1
        filename_url = url.split("/")[-1]
        # cleanup url junk: pdfreader get confused by them!
        filename = "".join(x for x in filename_url if x == "." or x.isalnum())
        filename = f"{download_dir}/{filename}"
        #print(f"{filename=} {filename_url}")
        loggin.info(f"{filename=} {filename_url}")
        with open(filename, "wb") as file:
            for seg in results.iter_content(chunk_size=1024):
                if seg:
                    file.write(seg)

        files.append(filename)
    return status, files


def get_inference_predictions(data: dict):
    """interface function calls the local infrence predict
    results retuend as json file
    """
    # print(f"{data=}")

    prediction = predict(data)
    json_pred = json.dumps(prediction, indent=4)

    #print(f"{json_pred=}")
    ocrlogs.debug(f"{json_pred=}")
    results_dir = makeLocalWorkingDir(prefix="ocrResults", wdir="/tmp")
    results_file = f"{results_dir}/results.json"

    with open(results_file, "w") as rf:
        rf.write(json_pred)

    return_status: int = 0
    time.sleep(2)
    return (return_status, results_file)


def process_inference_equest(
    req: ocrservice_pb2.OCRrequestInference,
) -> Tuple[int, str]:
    """demux function which download the files from various location
    and call the main interface function get_inference_prediction
    """
    #print(f"{req=}")
    ocrlogs.debug(f"{req=}")
    
    if req.HasField("s3Info"):
        __status, files = get_s3files(req.s3Info)
    elif req.httplink != []:
        __status, files = get_url_file(req.httplink)
    elif req.filename != []:
        __status, files = 0, req.filename
    else:
        #print(" no file information is set in the request ")
        ocrlogs.error(" no file information is set in the request ")

    data = dict(pdf=files)

    return get_inference_predictions(data)


def process_inference_fileUpload(request_iterator):
    """handle the direct file upload by the ocrservice client 'frontend'"""

    upload_dir = makeLocalWorkingDir(prefix="clientUpload", wdir="/tmp")

    files: List[str] = []
    for request in request_iterator:
        if request.filename:
            filename = f"{upload_dir}/{request.filename}"
            files.append(filename)
            data = bytearray()
            continue
        data.extend(request.data)
        with open(filename, "wb") as rf:
            rf.write(data)

    #print(f"received uploaded {files=}")
    ocrlogs.info(f"received uploaded {files=}")
    
    data = dict(pdf=files)

    return get_inference_predictions(data)


class ocrserviceServicer(ocrservice_pb2_grpc.ocrserviceServicer):
    def ProcessInfra(self, request, context):
        """Handle ProcessInfa rpc"""
        __error, filename = process_inference_equest(request)

        #print(f" results file = {filename}")
        ocrlogs.info(f" results file = {filename}")
        block_size: int = 1024

        with open(filename, "rb") as results_file:
            while True:
                segment = results_file.read(block_size)
                if segment:
                    #print("sent segment")
                    ocrlogs.debug("sent segment")
                    entry_response = ocrservice_pb2.OCRresponse(
                        status=ocrservice_pb2.OCRretunStatus.sucess, data=segment
                    )
                    yield entry_response
                else:
                    return

    def ProcessUpload(self, request_iterator, context):
        """Handle ProcessUpload rpc"""
        __error, filename = process_inference_fileUpload(request_iterator)

        ocrlogs.info(f" results file = {filename}")
        block_size: int = 1024

        with open(filename, "rb") as results_file:
            while True:
                segment = results_file.read(block_size)
                if segment:
                    ocrlogs.debug("sent segment")
                    entry_response = ocrservice_pb2.OCRresponse(
                        status=ocrservice_pb2.OCRretunStatus.sucess, data=segment
                    )
                    yield entry_response
                else:
                    return


def serve():
    local_server_port = os.environ.get('LOCAL_SERVER_PORT')
    if local_server_port is None: 
        local_server_port = "50051"
    
    local_server_address = "[::]"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ocrservice_pb2_grpc.add_ocrserviceServicer_to_server(ocrserviceServicer(), server)
    server.add_insecure_port(f"{local_server_address}:{local_server_port}")
    server.start()
    ocrlogs.info("ocr grpc server started")
    def sigterm_handler(*_):
        #print("received shutdown signal, Waiting 30 second to clear jobs")
        ocrlogs.info("received shutdown signal, Waiting 30 second to clear jobs")
        all_rpc_done_event = server.stop(30)
        all_rpc_done_event.wait(30)
        #print("completed gracefull shut down")
        ocrlogs.info("completed gracefull shut down")

    signal(SIGTERM, sigterm_handler)
    signal(SIGINT, sigterm_handler)
    server.wait_for_termination()


if __name__ == "__main__":
    ocrlogs.setLevel(logging.DEBUG)
    
    logfile = logging.FileHandler(filename=get_logfile_path("ocr_service.log"))
    logfile.setLevel(logging.DEBUG)
    logformat = logging.Formatter(fmt="%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
    logfile.setFormatter(logformat)
    ocrlogs.addHandler(logfile)
    
    logstream = logging.StreamHandler()
    #logstream.setLevel(logging.INFO)
    logstream.setLevel(logging.DEBUG)
    logstream.setFormatter(logformat)
    ocrlogs.addHandler(logstream)
    
    
    #logging.basicConfig(filename=get_logfile_path("ocr_service.log"),level=logging.DEBUG)
    serve()
