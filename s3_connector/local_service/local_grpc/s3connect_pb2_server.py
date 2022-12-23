"""The Python implementation of the gRPC route guide server."""

from concurrent import futures
import logging, coloredlogs
from typing import List
from signal import signal, SIGTERM, SIGINT

# import math
# import time
import subprocess
import os


import grpc
import s3connect_pb2
import s3connect_pb2_grpc

s3logs = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG, logger=s3logs)

def get_logfile_path(logfile_name:str) -> str:
    logdir: str = os.path.dirname(os.path.abspath(__file__))
    return  f"{logdir}/../logs/{logfile_name}"

def run_cmd(cmd: str, run_env: dict):
    """cmd runner"""

    try:
        output = subprocess.check_output(cmd, shell=True, env=run_env)

        output = output.decode("utf-8")

        return output

    except subprocess.CalledProcessError as e:
        s3logs.error(f" returned error: {e.returncode}, output: {e.output.decode()}")
        return e.returncode


def get_results(req: s3connect_pb2.S3request) -> List[str]:
    """build the s3 download cmd and execute it"""
    s3logs.debug(f"{req=}")
    os_env = os.environ.copy()
    run_env = {
        "aws_access_key_id": req.env.aws_access_key_id,
        "aws_secret_access_key ": req.env.aws_secret_access_key,
    }
    os_env.update(run_env)

    endpoint = req.args.endpoint
    command = req.args.command
    bucketname = req.args.bucketname
    file = req.args.file if req.args.HasField("file") else None
    bucketname = req.args.bucketname
    localdir = req.args.localdir
    prefix = req.args.prefix if req.args.HasField("prefix") else None

    cmd = "python3 ../s3connector.py"
    cmd = f"{cmd} --endpoint {endpoint} {command}"
    cmd = f"{cmd} --bucketname {bucketname}"
    cmd = f"{cmd} --localdir {localdir}"

    if file is not None:
        cmd = f"{cmd} --file {file}"
    else:
        cmd = f"{cmd} --prefix {prefix}"

    # run_cmd(cmd, os_env)

    files = [
        f"{localdir}/{file}"
        for file in os.listdir(localdir)
        if os.path.isfile(os.path.join(localdir, file))
    ]
    return files


class s3connectServicer(s3connect_pb2_grpc.s3connectServicer):
    """Provides methods that implement functionality of s3connet server."""

    def DownloadFilesToLocation(self, request, context):
        """Handle rpc download files to shared location"""
        files = get_results(request)
        s3logs.info("DownloadFilesToLocation")
        ret_response = s3connect_pb2.S3response()
        ret_response.request.CopyFrom(request.args)
        if files == []:
            ret_response.status = 1

        else:
            ret_response.status = 0
            ret_response.files.extend(files)

        return ret_response

    def GetFiles(self, request, context):
        """Handle rpc to stream downloaded files back to client"""
        segment_size = 1024
        files = get_results(request)
        s3logs.info("GetFiles")

        for file in files:
            file_name_no_path = file.split("/")[-1]
            # send file name first
            s3logs.info(f"{file=}, {file_name_no_path=}")
            yield s3connect_pb2.S3FilesResponse(filename=file_name_no_path)
            # then stream the file it self
            with open(file, mode="rb") as fs:
                streaming_on = True
                while streaming_on:
                    segment = fs.read(segment_size)
                    if segment:
                        entry_request = s3connect_pb2.S3FilesResponse(data=segment)
                        yield entry_request
                    else:
                        streaming_on = False
        return


def serve():
    local_server_port = os.environ.get('LOCAL_SERVER_PORT')
    if local_server_port is None: 
        local_server_port = "50051"
    
    local_server_address = "[::]"
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    s3connect_pb2_grpc.add_s3connectServicer_to_server(s3connectServicer(), server)
    server.add_insecure_port(f"{local_server_address}:{local_server_port}")
    server.start()
    s3logs.info("s3 grpc server started")
    
    def sigterm_handler(*_):
        s3logs.info("received shutdown signal, Waiting 30 second to clear jobs")
        all_rpc_done_event = server.stop(30)
        all_rpc_done_event.wait(30)
        s3logs.info("completed gracefull shut down")

    signal(SIGTERM, sigterm_handler)
    signal(SIGINT, sigterm_handler)

    server.wait_for_termination()


if __name__ == "__main__":
    s3logs.setLevel(logging.DEBUG)
    
    logfile = logging.FileHandler(filename=get_logfile_path("s3_service.log"))
    logfile.setLevel(logging.DEBUG)
    logformat = logging.Formatter(fmt="%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
    logfile.setFormatter(logformat)
    s3logs.addHandler(logfile)
    
    logstream = logging.StreamHandler()
    #logstream.setLevel(logging.INFO)
    logstream.setLevel(logging.DEBUG)
    logstream.setFormatter(logformat)
    s3logs.addHandler(logstream)
    
    #logging.basicConfig()
    serve()
