"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function
from datetime import datetime
from typing import List
import logging
import os

import grpc
import s3connect_pb2
import s3connect_pb2_grpc


def makeLocalWorkingDir(prefix="s3download", wdir="/tmp") -> str:
    """local helper function for makring local directory"""
    timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    dir_name = f"{wdir}/{prefix}-{timestamp}"

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    return dir_name


def download_to_location(stub: s3connect_pb2_grpc.s3connectStub):
    """Request download from S3 to be placed in shared location 'localdir'"""
    req = s3connect_pb2.S3request()
    req.args.endpoint = "http://s3.amazonaws.com"
    req.args.command = "download"
    req.args.bucketname = "libhub-readme"
    req.args.localdir = "/cnvrg"
    req.args.prefix = "pdf_extraction_data/"

    req.env.aws_access_key_id = "some__ID__ID"
    req.env.aws_secret_access_key = "some_secret_secret"

    res = stub.DownloadFilesToLocation(req)

    print(res)


def download_files(stub: s3connect_pb2_grpc.s3connectStub):
    """Request download from S3 and accept these files via server stream"""
    req = s3connect_pb2.S3request()
    req.args.endpoint = "http://s3.amazonaws.com"
    req.args.command = "download"
    req.args.bucketname = "libhub-readme"
    req.args.localdir = "/cnvrg"
    req.args.prefix = "pdf_extraction_data/"

    req.env.aws_access_key_id = "some__ID__ID"
    req.env.aws_secret_access_key = "some_secret_secret"

    file_path = makeLocalWorkingDir()
    files: List[str] = []
    for res in stub.GetFiles(req):
        if res.filename:
            print(f"{res.filename=}")
            filename = f"{file_path}/{res.filename}"
            files.append(filename)
        else:
            with open(filename, "ab") as rf:
                rf.write(res.data)

    print(f"Received: {files}")


def download_to_shared():
    """request files to be download to shared location"""
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = s3connect_pb2_grpc.s3connectStub(channel)
        print("---downloading files to shared location---")
        download_to_location(stub)


def download_to_stream():
    """request downloaded files to be streamed back to client"""
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = s3connect_pb2_grpc.s3connectStub(channel)
        print("---streamming requested files---")
        download_files(stub)


if __name__ == "__main__":
    logging.basicConfig()

    download_to_stream()
